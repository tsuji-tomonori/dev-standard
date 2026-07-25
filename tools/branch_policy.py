#!/usr/bin/env python3
"""Validate the repository-specific main/dev branch contract."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ZERO_SHA = "0" * 40
POLICY_PATH = Path(".github/branch-policy.json")
PHASES = {"bootstrap", "trial"}
ACTIVATION_REQUIREMENTS = [
    "dev-created-from-current-main",
    "main-and-dev-rulesets-configured",
    "required-checks-configured",
    "squash-message-title-and-description",
    "open-pr-12-migrated",
    "dev-tree-equals-main-before-activation",
    "branch-graph-regression-passed",
    "single-release-operator-confirmed",
]
EXPECTED_PULL_REQUESTS = {
    "bootstrap_marker": "Branch-Policy-Bootstrap",
    "activation_marker": "Trial-Activation",
    "activation_check_marker": "Activation-Check",
    "rollback_marker": "Trial-Rollback",
    "release_type_marker": "Release-Type",
    "release_review_marker": "Release-Review",
    "included_prs_marker": "Included-PRs",
    "reconciliation_type_marker": "Reconciliation-Type",
    "source_pr_marker": "Source-PR",
    "topic_prefixes": [
        "agent/",
        "feature/",
        "fix/",
        "refactor/",
        "perf/",
        "docs/",
        "test/",
        "build/",
        "ci/",
        "chore/",
        "topic/",
    ],
    "hotfix_prefixes": ["hotfix/"],
    "reconciliation_prefixes": ["reconcile/"],
    "issue_reference_pattern": r"(?i)^\s*(?:[-*]\s*)?Refs(?::|\s)\s*#\d+(?:\s*,\s*#\d+)*\s*$",
    "release_required_headings": [
        "## 含まれるPR",
        "## 要件・設計影響",
        "## 互換性・rollback",
        "## 残存リスク",
    ],
    "closing_issue_pattern": r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+",
}
EXPECTED_COMMIT_SUBJECT = {
    "conventional_pattern": r"^(?P<gitmoji>\S+)\s+[a-z]+(?:\([^)]+\))?!?:\s+.+$",
    "japanese_pattern": "[ぁ-んァ-ヶ一-龠々]",
    "forbidden_patterns": [
        r"(?i)^fixup!",
        r"(?i)^squash!",
        r"(?i):\s*(?:WIP|tmp|temp|checkpoint)(?:[:\s]|$)",
        r"^🚧(?:️)?(?:\s|$)",
    ],
}


class PolicyError(RuntimeError):
    """Raised when the branch contract is invalid or violated."""


@dataclass(frozen=True)
class PolicyResult:
    kind: str
    evidence_commit: str = ""
    review_path: str = ""
    review_commit: str = ""


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise PolicyError((result.stdout + result.stderr).strip() or f"git {' '.join(args)} failed")
    return result


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PolicyError(f"{path}: root must be an object")
    return value


def validate_policy(policy: dict[str, Any], label: str) -> dict[str, Any]:
    expected = {"schema_version", "repository", "trial", "branches", "pull_requests", "commit_subject"}
    if set(policy) != expected or policy.get("schema_version") != 1:
        raise PolicyError(f"{label}: unsupported policy schema")
    if policy.get("repository") != "tsuji-tomonori/dev-standard":
        raise PolicyError(f"{label}: policy is bound to the wrong repository")

    trial = policy.get("trial")
    if not isinstance(trial, dict):
        raise PolicyError(f"{label}: trial must be an object")
    expected_trial = {
        "issue",
        "phase",
        "release_cycles",
        "portable_default",
        "single_release_operator",
        "atomic_cross_branch_lock",
        "activation_requirements",
    }
    if set(trial) != expected_trial:
        raise PolicyError(f"{label}: trial fields are invalid")
    if trial["issue"] != 20 or trial["phase"] not in PHASES:
        raise PolicyError(f"{label}: trial must remain linked to Issue #20 and use bootstrap/trial phase")
    if trial["release_cycles"] != 2:
        raise PolicyError(f"{label}: trial must cover exactly two release cycles")
    if trial["portable_default"] is not False:
        raise PolicyError(f"{label}: the trial must not become a portable default")
    if trial["single_release_operator"] is not True:
        raise PolicyError(f"{label}: the trial requires one release operator")
    if trial["atomic_cross_branch_lock"] is not False:
        raise PolicyError(f"{label}: CI must not claim an atomic cross-branch lock")
    activation = trial["activation_requirements"]
    if not isinstance(activation, list) or not activation or any(not isinstance(item, str) or not item for item in activation):
        raise PolicyError(f"{label}: activation_requirements must be a non-empty string list")
    if activation != ACTIVATION_REQUIREMENTS:
        raise PolicyError(f"{label}: activation_requirements do not match the approved bootstrap gate")

    branches = policy.get("branches")
    if not isinstance(branches, dict) or set(branches) != {"main", "dev"}:
        raise PolicyError(f"{label}: main and dev branch definitions are required")
    expected_branches = {
        "main": {"merge_method": "squash", "linear_history": True},
        "dev": {"merge_method": "merge", "linear_history": False},
    }
    for name, expected_branch in expected_branches.items():
        rule = branches[name]
        if not isinstance(rule, dict):
            raise PolicyError(f"{label}: branches.{name} must be an object")
        expected_fields = {
            "merge_method",
            "linear_history",
            "require_pull_request",
            "required_checks",
            "allow_deletion",
            "allow_force_push",
        }
        if set(rule) != expected_fields:
            raise PolicyError(f"{label}: branches.{name} fields are invalid")
        for key, value in expected_branch.items():
            if rule[key] is not value and rule[key] != value:
                raise PolicyError(f"{label}: branches.{name}.{key} must be {value!r}")
        if rule["require_pull_request"] is not True:
            raise PolicyError(f"{label}: {name}.require_pull_request must be true")
        if rule["allow_deletion"] is not False or rule["allow_force_push"] is not False:
            raise PolicyError(f"{label}: {name} deletion and force push must be prohibited")
        if rule["required_checks"] != ["integration", "evidence", "branch-policy"]:
            raise PolicyError(f"{label}: {name} required checks must be integration/evidence/branch-policy")

    pull_requests = policy.get("pull_requests")
    if not isinstance(pull_requests, dict):
        raise PolicyError(f"{label}: pull_requests must be an object")
    expected_pr_fields = {
        "bootstrap_marker",
        "activation_marker",
        "activation_check_marker",
        "rollback_marker",
        "release_type_marker",
        "release_review_marker",
        "included_prs_marker",
        "reconciliation_type_marker",
        "source_pr_marker",
        "topic_prefixes",
        "hotfix_prefixes",
        "reconciliation_prefixes",
        "issue_reference_pattern",
        "release_required_headings",
        "closing_issue_pattern",
    }
    if set(pull_requests) != expected_pr_fields:
        raise PolicyError(f"{label}: pull_requests fields are invalid")
    if pull_requests != EXPECTED_PULL_REQUESTS:
        raise PolicyError(f"{label}: pull request contract differs from the approved two-release trial")
    re.compile(pull_requests["closing_issue_pattern"])
    re.compile(pull_requests["issue_reference_pattern"])

    commit_subject = policy.get("commit_subject")
    if not isinstance(commit_subject, dict) or set(commit_subject) != {
        "conventional_pattern",
        "japanese_pattern",
        "forbidden_patterns",
    }:
        raise PolicyError(f"{label}: commit_subject fields are invalid")
    if commit_subject != EXPECTED_COMMIT_SUBJECT:
        raise PolicyError(f"{label}: commit subject contract differs from the approved two-release trial")
    for pattern in [commit_subject["conventional_pattern"], commit_subject["japanese_pattern"]]:
        re.compile(pattern)
    for pattern in commit_subject["forbidden_patterns"]:
        re.compile(pattern)
    return policy


def load_policy(root: Path, path: Path | None = None) -> dict[str, Any]:
    policy_path = path or root / POLICY_PATH
    return validate_policy(load_json(policy_path), str(policy_path))


def load_policy_at_ref(root: Path, ref: str) -> dict[str, Any] | None:
    result = git(root, "show", f"{ref}:{POLICY_PATH.as_posix()}", check=False)
    if result.returncode:
        return None
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PolicyError(f"{ref}:{POLICY_PATH}: invalid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise PolicyError(f"{ref}:{POLICY_PATH}: root must be an object")
    return validate_policy(value, f"{ref}:{POLICY_PATH}")


def safe_repo_path(root: Path, value: str) -> Path:
    candidate = (root / value).resolve(strict=False)
    resolved_root = root.resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise PolicyError(f"path escapes repository: {value}")
    return candidate


def resolve_branch(root: Path, name: str) -> str | None:
    for candidate in [f"refs/remotes/origin/{name}", f"refs/heads/{name}", name]:
        result = git(root, "rev-parse", "--verify", f"{candidate}^{{commit}}", check=False)
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    return git(root, "merge-base", "--is-ancestor", ancestor, descendant, check=False).returncode == 0


def trees_equal(root: Path, left: str, right: str) -> bool:
    return git(root, "diff", "--quiet", left, right, "--", check=False).returncode == 0


def tree_entry(root: Path, commit: str, path: str) -> str | None:
    result = git(root, "rev-parse", "--verify", f"{commit}:{path}", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def validate_hotfix_result(root: Path, prior_dev: str, main_sha: str, result_sha: str) -> None:
    """Ensure a hotfix is not topology-only and discarded during reconciliation."""
    main_parents = parents(root, main_sha)
    if len(main_parents) != 1:
        raise PolicyError("hotfix source on main must be one linear commit")
    hotfix_base = main_parents[0]
    if not is_ancestor(root, hotfix_base, prior_dev):
        raise PolicyError("hotfix reconciliation requires the hotfix base to be an ancestor of prior dev")
    changed_paths = git_text(
        root,
        "diff",
        "--name-only",
        "--no-renames",
        hotfix_base,
        main_sha,
        "--",
    ).splitlines()
    if not changed_paths:
        raise PolicyError("hotfix source must change at least one tracked path")
    for path in changed_paths:
        base_entry = tree_entry(root, hotfix_base, path)
        dev_entry = tree_entry(root, prior_dev, path)
        main_entry = tree_entry(root, main_sha, path)
        result_entry = tree_entry(root, result_sha, path)
        if dev_entry == base_entry or dev_entry == main_entry:
            if result_entry != main_entry:
                raise PolicyError(f"hotfix reconciliation dropped an uncontested change: {path}")
        elif result_entry in {dev_entry, base_entry}:
            raise PolicyError(f"hotfix conflict resolution must preserve an explicit integrated result: {path}")


def parents(root: Path, commit: str) -> list[str]:
    value = git_text(root, "show", "-s", "--format=%P", commit)
    return value.split() if value else []


def commit_message(root: Path, commit: str) -> str:
    return git_text(root, "show", "-s", "--format=%B", commit)


def visible_markdown(text: str) -> str:
    """Remove non-visible template text and fenced examples before parsing policy fields."""
    without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    visible: list[str] = []
    fence: str | None = None
    for line in without_comments.splitlines():
        stripped = line.lstrip()
        marker = next((token for token in ("```", "~~~") if stripped.startswith(token)), None)
        if fence is None and marker is not None:
            fence = marker
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        visible.append(line)
    return "\n".join(visible)


def marker_values(body: str, key: str) -> list[str]:
    pattern = re.compile(rf"(?mi)^\s*(?:[-*]\s*)?{re.escape(key)}:\s*(.*?)\s*$")
    return [match.group(1).strip().strip("`") for match in pattern.finditer(visible_markdown(body))]


def required_marker(body: str, key: str) -> str:
    values = marker_values(body, key)
    if len(values) != 1 or not values[0]:
        raise PolicyError(f"PR or commit message must contain exactly one `{key}: <value>` marker")
    return values[0]


def optional_true_marker(body: str, key: str) -> bool:
    values = marker_values(body, key)
    if not values:
        return False
    if len(values) != 1 or values[0].casefold() != "true":
        raise PolicyError(f"{key} must appear once with value true")
    return True


def same_repository(event: dict[str, Any], expected: str) -> bool:
    head_repo = event["pull_request"]["head"].get("repo") or {}
    return head_repo.get("full_name") == expected


def contains_issue_reference(text: str, issue: int) -> bool:
    """Return whether a visible Refs line names the trial Issue."""
    pattern = re.compile(rf"(?mi)^\s*(?:[-*]\s*)?Refs(?::|\s)\s*.*(?<!\d)#{issue}(?!\d).*$")
    return pattern.search(visible_markdown(text)) is not None


def starts_with_any(value: str, prefixes: list[str]) -> bool:
    return any(value.startswith(prefix) for prefix in prefixes)


def heading_content(body: str, heading: str) -> str:
    lines = visible_markdown(body).splitlines()
    indexes = [index for index, line in enumerate(lines) if line.strip() == heading]
    if len(indexes) != 1:
        raise PolicyError(f"release PR body must contain exactly one heading: {heading}")
    start = indexes[0] + 1
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("## ")), len(lines))
    content = "\n".join(lines[start:end])
    content = content.strip()
    if not content:
        raise PolicyError(f"release PR heading has no content: {heading}")
    return content


def pull_request_numbers(value: str) -> list[str]:
    return re.findall(r"#\d+", value)


def has_issue_reference(policy: dict[str, Any], body: str) -> bool:
    return re.search(policy["pull_requests"]["issue_reference_pattern"], visible_markdown(body), flags=re.MULTILINE) is not None


def validate_release_manifest(
    policy: dict[str, Any],
    body: str,
    expected_type: str,
    *,
    require_closing_issue: bool = True,
) -> None:
    rules = policy["pull_requests"]
    release_type = required_marker(body, rules["release_type_marker"])
    if release_type != expected_type:
        raise PolicyError(f"Release-Type must be {expected_type}")
    included = required_marker(body, rules["included_prs_marker"])
    included_numbers = pull_request_numbers(included)
    if not included_numbers:
        raise PolicyError("Included-PRs must contain at least one pull request number")
    if len(included_numbers) != len(set(included_numbers)):
        raise PolicyError("Included-PRs must not contain duplicate pull request numbers")
    content = {heading: heading_content(body, heading) for heading in rules["release_required_headings"]}
    heading_numbers = pull_request_numbers(content["## 含まれるPR"])
    if not heading_numbers:
        raise PolicyError("## 含まれるPR must identify at least one pull request")
    if len(heading_numbers) != len(set(heading_numbers)):
        raise PolicyError("## 含まれるPR must not contain duplicate pull request numbers")
    if set(included_numbers) != set(heading_numbers):
        raise PolicyError("Included-PRs and ## 含まれるPR must identify the same pull requests")
    if require_closing_issue and not re.search(rules["closing_issue_pattern"], visible_markdown(body)):
        raise PolicyError("release PR or squash commit must close at least one Issue")


def validate_bootstrap_markers(policy: dict[str, Any], text: str) -> None:
    """Require the explicit marker and Issue reference for bootstrap delivery."""
    rules = policy["pull_requests"]
    if not optional_true_marker(text, rules["bootstrap_marker"]):
        raise PolicyError("bootstrap delivery requires Branch-Policy-Bootstrap: true")
    if not contains_issue_reference(text, policy["trial"]["issue"]):
        raise PolicyError(f"bootstrap delivery must contain `Refs #{policy['trial']['issue']}`")


def classify_pull_request(policy: dict[str, Any], event: dict[str, Any]) -> str:
    pull = event.get("pull_request")
    if not isinstance(pull, dict):
        raise PolicyError("pull_request event payload is required")
    base = str(pull["base"]["ref"])
    head = str(pull["head"]["ref"])
    expected_repo = policy["repository"]
    rules = policy["pull_requests"]
    phase = policy["trial"]["phase"]
    body = str(pull.get("body") or "")

    if phase == "bootstrap":
        if base == "main" and head == "dev" and optional_true_marker(body, rules["bootstrap_marker"]):
            if not same_repository(event, expected_repo):
                raise PolicyError("bootstrap release head must be this repository's dev branch")
            return "bootstrap-release"
        if base == "main" and (starts_with_any(head, rules["topic_prefixes"]) or starts_with_any(head, rules["hotfix_prefixes"])):
            if not same_repository(event, expected_repo):
                raise PolicyError("bootstrap PR head must be in the same repository")
            return "bootstrap"
        if base == "dev" and head == "main":
            if not same_repository(event, expected_repo):
                raise PolicyError("reconciliation PR head must be this repository's main branch")
            return "reconciliation"
        if base == "dev" and starts_with_any(head, rules["topic_prefixes"]) and optional_true_marker(
            body,
            rules["bootstrap_marker"],
        ):
            if not same_repository(event, expected_repo):
                raise PolicyError("bootstrap topic head must be in the same repository")
            return "bootstrap-topic"
        raise PolicyError(f"bootstrap phase rejects pull request direction: {head} -> {base}")

    if base == "main" and head == "dev":
        if not same_repository(event, expected_repo):
            raise PolicyError("release PR head must be this repository's dev branch")
        return "release"
    if base == "main" and starts_with_any(head, rules["hotfix_prefixes"]):
        if not same_repository(event, expected_repo):
            raise PolicyError("hotfix PR head must be in the same repository")
        return "hotfix"
    if base == "dev" and (head == "main" or starts_with_any(head, rules["reconciliation_prefixes"])):
        if not same_repository(event, expected_repo):
            raise PolicyError("reconciliation PR head must be in this repository")
        return "reconciliation"
    if base == "dev" and starts_with_any(head, rules["topic_prefixes"]):
        return "topic"
    raise PolicyError(f"trial phase rejects pull request direction: {head} -> {base}")


def contains_emoji(value: str) -> bool:
    """Return whether a token contains a Unicode symbol used by common Gitmoji."""
    ranges = (
        (0x2300, 0x23FF),
        (0x2600, 0x27BF),
        (0x2B00, 0x2BFF),
        (0x1F1E6, 0x1F1FF),
        (0x1F300, 0x1FAFF),
    )
    return any(any(start <= ord(character) <= end for start, end in ranges) for character in value)


def validate_subject(policy: dict[str, Any], subject: str, commit: str) -> None:
    contract = policy["commit_subject"]
    if any(re.search(pattern, subject) for pattern in contract["forbidden_patterns"]):
        raise PolicyError(f"{commit}: forbidden temporary commit subject: {subject}")
    match = re.match(contract["conventional_pattern"], subject)
    if match is None:
        raise PolicyError(f"{commit}: subject must use Gitmoji + Conventional Commit: {subject}")
    gitmoji = match.groupdict().get("gitmoji", "")
    if not contains_emoji(gitmoji):
        raise PolicyError(f"{commit}: subject must start with a Gitmoji token: {subject}")
    summary = subject.split(":", 1)[1] if ":" in subject else ""
    if not re.search(contract["japanese_pattern"], summary):
        raise PolicyError(f"{commit}: subject summary must contain Japanese text: {subject}")


def validate_subject_range(root: Path, policy: dict[str, Any], base: str, head: str) -> None:
    commits = git_text(root, "rev-list", "--reverse", head, f"^{base}").splitlines()
    if not commits:
        raise PolicyError(f"commit range is empty: {base}..{head}")
    for commit in commits:
        validate_subject(policy, git_text(root, "show", "-s", "--format=%s", commit), commit)


def validate_merge_checkout(root: Path, base_sha: str, head_sha: str) -> str:
    checkout = git_text(root, "rev-parse", "HEAD")
    checkout_parents = parents(root, checkout)
    if checkout_parents != [base_sha, head_sha]:
        raise PolicyError(
            "integration checkout must be the synthetic merge with "
            f"parents base={base_sha} head={head_sha}; got {checkout_parents}"
        )
    return checkout


def release_boundary(root: Path, base_sha: str, head_sha: str) -> str:
    """Return the latest reconciliation boundary for a regular release range."""
    first_parent = git_text(root, "rev-list", "--first-parent", head_sha).splitlines()
    for commit in first_parent:
        commit_parents = parents(root, commit)
        if len(commit_parents) == 2 and commit_parents[1] == base_sha:
            return commit
        if commit == base_sha:
            return base_sha
    raise PolicyError("release head does not contain a reconciliation boundary for current main")


def validate_review_path(root: Path, boundary: str, head_sha: str, path_text: str) -> tuple[str, str]:
    if not re.fullmatch(r"governance/reviews/CHG-[A-Za-z0-9._-]+\.ya?ml", path_text):
        raise PolicyError(f"invalid release review path: {path_text}")
    path = safe_repo_path(root, path_text)
    if not path.is_file():
        raise PolicyError(f"release review does not exist in checkout: {path_text}")
    if git(root, "cat-file", "-e", f"{head_sha}:{path_text}", check=False).returncode:
        raise PolicyError(f"release review does not exist at PR head: {path_text}")
    review_commit = git_text(root, "log", "-1", "--format=%H", head_sha, "--", path_text)
    if not review_commit or review_commit == boundary or not is_ancestor(root, boundary, review_commit):
        raise PolicyError("release review must be created or updated after the release boundary")
    if not is_ancestor(root, review_commit, head_sha):
        raise PolicyError("release review commit is not reachable from the release head")
    return path_text, review_commit


def validate_bootstrap_review_path(
    root: Path,
    boundary: str,
    head_sha: str,
    path_text: str,
) -> tuple[str, str]:
    """Bind a dev-first bootstrap review to the merge that introduced it after reconciliation."""
    if not re.fullmatch(r"governance/reviews/CHG-[A-Za-z0-9._-]+\.ya?ml", path_text):
        raise PolicyError(f"invalid bootstrap review path: {path_text}")
    path = safe_repo_path(root, path_text)
    if not path.is_file():
        raise PolicyError(f"bootstrap review does not exist in checkout: {path_text}")
    if not is_ancestor(root, boundary, head_sha):
        raise PolicyError("bootstrap release boundary is not an ancestor of dev")
    head_entry = tree_entry(root, head_sha, path_text)
    if head_entry is None:
        raise PolicyError(f"bootstrap review does not exist at dev head: {path_text}")
    if tree_entry(root, boundary, path_text) == head_entry:
        raise PolicyError("bootstrap review must be introduced after the reconciliation boundary")

    integrations: list[str] = []
    first_parent_commits = git_text(
        root,
        "rev-list",
        "--first-parent",
        "--reverse",
        head_sha,
        f"^{boundary}",
    ).splitlines()
    for commit in first_parent_commits:
        commit_parents = parents(root, commit)
        if len(commit_parents) != 2:
            continue
        first_parent, second_parent = commit_parents
        if tree_entry(root, commit, path_text) != head_entry:
            continue
        if tree_entry(root, first_parent, path_text) == head_entry:
            continue
        if tree_entry(root, second_parent, path_text) != head_entry:
            continue
        integrations.append(commit)
    if len(integrations) != 1:
        raise PolicyError(
            "bootstrap review must be introduced by exactly one dev first-parent merge after reconciliation"
        )
    return path_text, integrations[0]


def review_path_from_commit(root: Path, commit: str) -> str:
    """Return a valid active review path referenced by a commit message."""
    path_text = required_marker(commit_message(root, commit), "Review-Checklist")
    if not re.fullmatch(r"governance/reviews/CHG-[A-Za-z0-9._-]+\.ya?ml", path_text):
        raise PolicyError(f"invalid Review-Checklist path: {path_text}")
    if git(root, "cat-file", "-e", f"{commit}:{path_text}", check=False).returncode:
        raise PolicyError(f"Review-Checklist does not exist at {commit}: {path_text}")
    return path_text


def validate_phase_transition_payload(root: Path, base_sha: str, head_sha: str) -> str:
    """Limit a phase transition to policy plus its selected-check evidence."""
    review_path = review_path_from_commit(root, head_sha)
    changed = set(git_text(root, "diff", "--name-only", base_sha, head_sha).splitlines())
    expected = {POLICY_PATH.as_posix(), review_path}
    if changed != expected:
        raise PolicyError(
            "trial phase transition may change only .github/branch-policy.json and its active review YAML; "
            f"got {sorted(changed)}"
        )
    return review_path


def validate_activation_attestations(policy: dict[str, Any], text: str) -> None:
    rules = policy["pull_requests"]
    if not optional_true_marker(text, rules["activation_marker"]):
        raise PolicyError("trial activation requires Trial-Activation: true")
    observed = marker_values(text, rules["activation_check_marker"])
    required = policy["trial"]["activation_requirements"]
    if len(observed) != len(set(observed)) or sorted(observed) != sorted(required):
        raise PolicyError("activation must attest every Activation-Check exactly once")


def policy_contract_without_phase(policy: dict[str, Any]) -> dict[str, Any]:
    """Return the approved trial contract with only its lifecycle phase normalized."""
    return {
        **policy,
        "trial": {
            **policy["trial"],
            "phase": "<lifecycle-phase>",
        },
    }


def validate_policy_contract_unchanged(
    governing: dict[str, Any],
    candidate: dict[str, Any],
) -> None:
    """Allow activation and rollback to change phase, but no other trial contract field."""
    if policy_contract_without_phase(governing) != policy_contract_without_phase(candidate):
        raise PolicyError("the approved two-release branch contract is immutable except for trial.phase")


def validate_policy_transition(
    root: Path,
    governing: dict[str, Any] | None,
    candidate: dict[str, Any],
    body: str,
    kind: str,
    head_sha: str,
) -> None:
    if governing is None:
        if candidate["trial"]["phase"] != "bootstrap":
            raise PolicyError("the first branch policy must enter bootstrap phase")
        return
    validate_policy_contract_unchanged(governing, candidate)
    old_phase = governing["trial"]["phase"]
    new_phase = candidate["trial"]["phase"]
    if old_phase == new_phase:
        return
    rules = governing["pull_requests"]
    if old_phase == "bootstrap" and new_phase == "trial":
        if kind == "bootstrap":
            validate_activation_attestations(governing, body)
            return
        if kind == "reconciliation" and required_marker(body, rules["reconciliation_type_marker"]) == "bootstrap":
            validate_activation_attestations(governing, commit_message(root, head_sha))
            return
        raise PolicyError("bootstrap -> trial requires an activation PR and bootstrap reconciliation")
    if old_phase == "trial" and new_phase == "bootstrap":
        if kind == "hotfix" and optional_true_marker(body, rules["rollback_marker"]):
            return
        if kind == "reconciliation":
            reconciliation_type = required_marker(body, rules["reconciliation_type_marker"])
            source_message = commit_message(root, head_sha)
            if reconciliation_type == "hotfix" and optional_true_marker(
                source_message,
                rules["rollback_marker"],
            ):
                return
        raise PolicyError(
            "trial rollback must use a hotfix PR with Trial-Rollback: true and then reconcile main to dev"
        )
    raise PolicyError(f"unsupported trial phase transition: {old_phase} -> {new_phase}")


def validate_pull_request(
    root: Path,
    candidate_policy: dict[str, Any],
    event: dict[str, Any],
    checkout_mode: str,
) -> PolicyResult:
    pull = event.get("pull_request")
    if not isinstance(pull, dict):
        raise PolicyError("pull_request event payload is required")
    base_sha = str(pull["base"]["sha"])
    head_sha = str(pull["head"]["sha"])
    head_ref = str(pull["head"]["ref"])
    body = str(pull.get("body") or "")
    governing_policy = load_policy_at_ref(root, base_sha)
    policy = governing_policy or candidate_policy
    kind = classify_pull_request(policy, event)
    main_sha = resolve_branch(root, "main")
    transition_source = main_sha if kind == "reconciliation" and head_ref != "main" else head_sha
    if transition_source is None:
        raise PolicyError("current main branch is required for reconciliation")
    validate_policy_transition(root, governing_policy, candidate_policy, body, kind, transition_source)
    if governing_policy is not None:
        old_phase = governing_policy["trial"]["phase"]
        new_phase = candidate_policy["trial"]["phase"]
        if old_phase == "bootstrap" and new_phase == "trial" and kind == "bootstrap":
            validate_phase_transition_payload(root, base_sha, head_sha)
        if old_phase == "trial" and new_phase == "bootstrap" and kind == "hotfix":
            validate_phase_transition_payload(root, base_sha, head_sha)
    rules = policy["pull_requests"]
    review_path = ""
    review_commit = ""

    if kind == "bootstrap":
        validate_bootstrap_markers(policy, body)
        if not is_ancestor(root, base_sha, head_sha):
            raise PolicyError("bootstrap branch must contain its main base")
        validate_subject_range(root, policy, base_sha, head_sha)
    elif kind == "bootstrap-topic":
        if governing_policy is not None:
            raise PolicyError("bootstrap topic delivery is allowed only before dev contains branch policy")
        validate_bootstrap_markers(policy, body)
        if main_sha is None or not is_ancestor(root, main_sha, base_sha):
            raise PolicyError("bootstrap topic delivery requires current main to be an ancestor of dev")
        if not trees_equal(root, main_sha, base_sha):
            raise PolicyError("bootstrap topic delivery requires synchronized main/dev tip trees")
        if not is_ancestor(root, main_sha, head_sha):
            raise PolicyError("bootstrap topic branch must contain current main")
        validate_subject_range(root, policy, main_sha, head_sha)
    elif kind == "bootstrap-release":
        if governing_policy is not None:
            raise PolicyError("bootstrap release is allowed only before main contains branch policy")
        validate_bootstrap_markers(policy, body)
        if not is_ancestor(root, base_sha, head_sha):
            raise PolicyError("bootstrap release requires current main to be an ancestor of dev")
        validate_release_manifest(policy, body, "bootstrap", require_closing_issue=False)
        boundary = release_boundary(root, base_sha, head_sha)
        review_path, review_commit = validate_bootstrap_review_path(
            root,
            boundary,
            head_sha,
            required_marker(body, rules["release_review_marker"]),
        )
    elif kind == "topic":
        if main_sha is None or not is_ancestor(root, main_sha, base_sha):
            raise PolicyError("topic PR is blocked until current main is an ancestor of dev")
        if re.search(rules["closing_issue_pattern"], visible_markdown(body)):
            raise PolicyError("topic PRs to dev must use Refs instead of closing keywords")
        if not has_issue_reference(policy, body):
            raise PolicyError("topic PRs to dev must reference at least one Issue with Refs")
        validate_subject_range(root, policy, base_sha, head_sha)
    elif kind in {"release", "hotfix"}:
        expected_type = "regular" if kind == "release" else "hotfix"
        if not is_ancestor(root, base_sha, head_sha):
            raise PolicyError(f"{kind} PR requires its main base to be an ancestor of the head")
        validate_release_manifest(policy, body, expected_type)
        if kind == "release":
            boundary = release_boundary(root, base_sha, head_sha)
        else:
            validate_subject_range(root, policy, base_sha, head_sha)
            boundary = base_sha
        review_path, review_commit = validate_review_path(
            root,
            boundary,
            head_sha,
            required_marker(body, rules["release_review_marker"]),
        )
    else:
        reconciliation_type = required_marker(body, rules["reconciliation_type_marker"])
        if reconciliation_type not in {"bootstrap", "release", "hotfix"}:
            raise PolicyError("Reconciliation-Type must be bootstrap, release, or hotfix")
        source_pr = required_marker(body, rules["source_pr_marker"])
        if not re.fullmatch(r"#\d+", source_pr):
            raise PolicyError("Source-PR must be a pull request number such as #42")
        direct_reconciliation = head_ref == "main"
        if not direct_reconciliation and reconciliation_type != "hotfix":
            raise PolicyError("only hotfix reconciliation may use a reconcile/* conflict-resolution branch")
        source_main = head_sha if direct_reconciliation else main_sha
        if source_main is None:
            raise PolicyError("current main branch is required for reconciliation")
        if is_ancestor(root, source_main, base_sha):
            raise PolicyError("reconciliation is unnecessary because main is already an ancestor of dev")
        if not direct_reconciliation:
            resolution_parents = parents(root, head_sha)
            if resolution_parents != [base_sha, source_main]:
                raise PolicyError(
                    "reconcile/* head must be one conflict-resolution merge with parents prior dev and current main"
                )
            source_policy = load_policy_at_ref(root, source_main)
            if source_policy is None or candidate_policy != source_policy:
                raise PolicyError("hotfix conflict-resolution branch must propagate current main policy exactly")
        source_message = commit_message(root, source_main)
        if reconciliation_type == "bootstrap":
            if not direct_reconciliation:
                raise PolicyError("bootstrap reconciliation head must be main")
            source_policy = load_policy_at_ref(root, source_main)
            if source_policy is None or candidate_policy != source_policy:
                raise PolicyError("bootstrap reconciliation must propagate the main policy exactly")
            old_phase = policy["trial"]["phase"]
            new_phase = candidate_policy["trial"]["phase"]
            if old_phase == "bootstrap" and new_phase == "trial":
                validate_activation_attestations(policy, source_message)
                source_parents = parents(root, source_main)
                if len(source_parents) != 1:
                    raise PolicyError("activation source on main must be one linear commit")
                validate_phase_transition_payload(root, source_parents[0], source_main)
            elif old_phase == "bootstrap" and new_phase == "bootstrap":
                if not optional_true_marker(source_message, rules["bootstrap_marker"]):
                    raise PolicyError("bootstrap synchronization requires Branch-Policy-Bootstrap: true")
            else:
                raise PolicyError("bootstrap reconciliation is allowed only while bootstrap is active or activating")
        else:
            source_release_type = required_marker(source_message, rules["release_type_marker"])
            expected_source_type = "regular" if reconciliation_type == "release" else "hotfix"
            if source_release_type != expected_source_type:
                raise PolicyError("Reconciliation-Type does not match the main release commit")
            if reconciliation_type == "release":
                if not direct_reconciliation:
                    raise PolicyError("regular release reconciliation head must be main")
                if not trees_equal(root, base_sha, source_main):
                    raise PolicyError("release reconciliation requires equal main and dev tip trees before merge")

    if checkout_mode == "integration":
        merge_sha = validate_merge_checkout(root, base_sha, head_sha)
        if kind in {"release", "hotfix", "bootstrap-topic", "bootstrap-release"} and not trees_equal(
            root,
            merge_sha,
            head_sha,
        ):
            raise PolicyError(f"{kind} integration tree must equal the head tree")
        if kind == "reconciliation":
            reconciliation_type = required_marker(body, rules["reconciliation_type_marker"])
            source_main = head_sha if head_ref == "main" else main_sha
            if source_main is None or not is_ancestor(root, source_main, merge_sha):
                raise PolicyError("reconciliation must make current main an ancestor of the merge result")
            if reconciliation_type == "release" and not (
                trees_equal(root, merge_sha, base_sha) and trees_equal(root, merge_sha, source_main)
            ):
                raise PolicyError("release reconciliation must not change the shared tip tree")
            if reconciliation_type == "bootstrap" and not trees_equal(root, merge_sha, source_main):
                raise PolicyError("bootstrap reconciliation merge tree must equal activated main")
            if reconciliation_type == "hotfix":
                if head_ref != "main" and not trees_equal(root, merge_sha, head_sha):
                    raise PolicyError("reconcile/* PR merge must preserve its conflict-resolution head tree")
                validate_hotfix_result(root, base_sha, source_main, merge_sha)
    elif checkout_mode == "head":
        checkout = git_text(root, "rev-parse", "HEAD")
        if checkout != head_sha:
            raise PolicyError(f"head checkout must equal PR head {head_sha}; got {checkout}")
    else:
        raise PolicyError(f"unsupported checkout mode: {checkout_mode}")

    return PolicyResult(
        kind=kind,
        evidence_commit=head_sha if kind in {"bootstrap", "bootstrap-topic", "topic", "hotfix"} else "",
        review_path=review_path,
        review_commit=review_commit,
    )


def validate_single_linear_push(root: Path, before: str, after: str) -> None:
    commits = git_text(root, "rev-list", "--reverse", after, f"^{before}").splitlines()
    if commits != [after]:
        raise PolicyError("main push must introduce exactly one squash, hotfix, or bootstrap commit")
    if parents(root, after) != [before]:
        raise PolicyError("main must remain linear and advance directly from the audited before SHA")


def validate_release_commit(root: Path, policy: dict[str, Any], before: str, after: str) -> str:
    rules = policy["pull_requests"]
    message = commit_message(root, after)
    release_type = required_marker(message, rules["release_type_marker"])
    if release_type not in {"regular", "hotfix"}:
        raise PolicyError("main release commit requires Release-Type: regular or hotfix")
    validate_release_manifest(policy, message, release_type)
    review_path = required_marker(message, rules["release_review_marker"])
    checklist = required_marker(message, "Review-Checklist")
    if review_path != checklist:
        raise PolicyError("Release-Review and Review-Checklist must reference the same YAML")
    path = safe_repo_path(root, review_path)
    if not path.is_file() or git(root, "cat-file", "-e", f"{after}:{review_path}", check=False).returncode:
        raise PolicyError("release review must exist in the main release commit")
    if release_type == "regular":
        dev_sha = resolve_branch(root, "dev")
        if dev_sha is None or not trees_equal(root, after, dev_sha):
            raise PolicyError("regular release main tree must equal the frozen dev tree")
        boundary = release_boundary(root, before, dev_sha)
        validate_review_path(root, boundary, dev_sha, review_path)
    else:
        validate_review_path(root, before, after, review_path)
    return release_type


def validate_bootstrap_release_commit(
    root: Path,
    policy: dict[str, Any],
    before: str,
    after: str,
) -> None:
    """Validate the one-time dev-first delivery of the initial bootstrap policy."""
    rules = policy["pull_requests"]
    message = commit_message(root, after)
    validate_bootstrap_markers(policy, message)
    validate_release_manifest(policy, message, "bootstrap", require_closing_issue=False)
    review_path = required_marker(message, rules["release_review_marker"])
    checklist = required_marker(message, "Review-Checklist")
    if review_path != checklist:
        raise PolicyError("bootstrap Release-Review and Review-Checklist must reference the same YAML")
    dev_sha = resolve_branch(root, "dev")
    if dev_sha is None:
        raise PolicyError("bootstrap release requires the synchronized dev branch")
    dev_policy = load_policy_at_ref(root, dev_sha)
    if dev_policy is None or dev_policy != policy:
        raise PolicyError("bootstrap release must promote the exact policy already integrated in dev")
    if not is_ancestor(root, before, dev_sha):
        raise PolicyError("bootstrap release requires current main to be an ancestor of dev")
    if not trees_equal(root, after, dev_sha):
        raise PolicyError("bootstrap release main tree must equal the frozen dev tree")
    boundary = release_boundary(root, before, dev_sha)
    validate_bootstrap_review_path(root, boundary, dev_sha, review_path)


def validate_main_policy_transition(
    governing: dict[str, Any] | None,
    candidate: dict[str, Any],
    message: str,
) -> None:
    rules = (governing or candidate)["pull_requests"]
    if governing is None:
        if candidate["trial"]["phase"] != "bootstrap":
            raise PolicyError("initial main policy commit must use bootstrap phase")
        if not optional_true_marker(message, rules["bootstrap_marker"]):
            raise PolicyError("initial main policy commit requires Branch-Policy-Bootstrap: true")
        if not contains_issue_reference(message, candidate["trial"]["issue"]):
            raise PolicyError("initial main policy commit must reference Issue #20")
        return
    old_phase = governing["trial"]["phase"]
    new_phase = candidate["trial"]["phase"]
    if old_phase == "bootstrap":
        if not optional_true_marker(message, rules["bootstrap_marker"]):
            raise PolicyError("main commits during bootstrap require Branch-Policy-Bootstrap: true")
        if not contains_issue_reference(message, governing["trial"]["issue"]):
            raise PolicyError("main commits during bootstrap must reference Issue #20")
        if new_phase == "trial":
            validate_activation_attestations(governing, message)
        elif new_phase != "bootstrap":
            raise PolicyError(f"unsupported main policy phase: {new_phase}")
        return
    if new_phase == "bootstrap":
        if not optional_true_marker(message, rules["rollback_marker"]):
            raise PolicyError("trial rollback main commit requires Trial-Rollback: true")
    elif new_phase != "trial":
        raise PolicyError(f"unsupported main policy phase: {new_phase}")


def validate_push(root: Path, candidate_policy: dict[str, Any], event: dict[str, Any]) -> PolicyResult:
    ref = event.get("ref")
    branch = ref.removeprefix("refs/heads/") if isinstance(ref, str) else ""
    if branch not in {"main", "dev"}:
        raise PolicyError(f"unsupported protected branch push: {ref}")
    if event.get("deleted") or event.get("forced"):
        raise PolicyError(f"{branch} deletion and force push are forbidden")
    before = str(event.get("before") or ZERO_SHA)
    after = str(event.get("after") or ZERO_SHA)
    if after == ZERO_SHA:
        raise PolicyError(f"{branch} cannot be deleted")
    checkout = git_text(root, "rev-parse", "HEAD")
    if checkout != after:
        raise PolicyError(f"push checkout must equal event after SHA {after}; got {checkout}")

    governing_policy = load_policy_at_ref(root, before) if before != ZERO_SHA else None
    if governing_policy is not None:
        validate_policy_contract_unchanged(governing_policy, candidate_policy)
    policy = governing_policy or candidate_policy
    old_phase = policy["trial"]["phase"]
    new_phase = candidate_policy["trial"]["phase"]

    if branch == "main":
        if before == ZERO_SHA:
            raise PolicyError("main bootstrap is outside this trial")
        validate_single_linear_push(root, before, after)
        message = commit_message(root, after)
        validate_main_policy_transition(governing_policy, candidate_policy, message)
        if governing_policy is None and marker_values(message, policy["pull_requests"]["release_type_marker"]):
            validate_bootstrap_release_commit(root, candidate_policy, before, after)
        if old_phase == "bootstrap" and new_phase == "trial":
            validate_phase_transition_payload(root, before, after)
        if old_phase == "trial":
            release_type = validate_release_commit(root, policy, before, after)
            if new_phase == "bootstrap":
                if release_type != "hotfix":
                    raise PolicyError("trial rollback must be delivered as a hotfix release")
                validate_phase_transition_payload(root, before, after)
        return PolicyResult(kind="main", evidence_commit=after)

    main_sha = resolve_branch(root, "main")
    if main_sha is None:
        raise PolicyError("main branch is required")
    if before == ZERO_SHA or event.get("created"):
        if old_phase != "bootstrap" or after != main_sha or not trees_equal(root, after, main_sha):
            raise PolicyError("initial dev branch must point to the current main commit during bootstrap")
        return PolicyResult(kind="dev-bootstrap")

    after_parents = parents(root, after)
    if len(after_parents) != 2 or after_parents[0] != before:
        raise PolicyError("dev updates must contain one merge commit whose first parent is prior dev")
    second_parent = after_parents[1]

    if governing_policy is None:
        if old_phase != "bootstrap" or new_phase != "bootstrap":
            raise PolicyError("initial dev policy delivery must remain in bootstrap phase")
        source_policy = load_policy_at_ref(root, second_parent)
        if source_policy is None or source_policy != candidate_policy:
            raise PolicyError("initial dev policy delivery must merge the exact candidate policy")
        validate_bootstrap_markers(candidate_policy, commit_message(root, second_parent))
        if not is_ancestor(root, main_sha, before):
            raise PolicyError("initial dev policy delivery requires current main to be an ancestor of prior dev")
        if not trees_equal(root, before, main_sha):
            raise PolicyError("initial dev policy delivery requires synchronized main/dev tip trees")
        if not is_ancestor(root, main_sha, second_parent):
            raise PolicyError("initial dev policy topic must contain current main")
        if not trees_equal(root, after, second_parent):
            raise PolicyError("initial dev policy merge must preserve the bootstrap topic tree")
        validate_subject_range(root, candidate_policy, main_sha, second_parent)
        return PolicyResult(kind="bootstrap-topic", evidence_commit=second_parent)

    resolution_parents = parents(root, second_parent)
    direct_reconciliation = second_parent == main_sha
    resolved_hotfix_reconciliation = resolution_parents == [before, main_sha]
    if direct_reconciliation or resolved_hotfix_reconciliation:
        main_policy = load_policy_at_ref(root, main_sha)
        if main_policy is None or candidate_policy != main_policy:
            raise PolicyError("reconciliation must propagate the current main branch policy exactly")
        source_message = commit_message(root, main_sha)
        if resolved_hotfix_reconciliation:
            release_type = required_marker(source_message, policy["pull_requests"]["release_type_marker"])
            if release_type != "hotfix":
                raise PolicyError("reconcile/* conflict-resolution merge is allowed only for a hotfix source")
            if not trees_equal(root, after, second_parent):
                raise PolicyError("dev merge must preserve the reconcile/* conflict-resolution tree")
            if old_phase == "trial" and new_phase == "bootstrap":
                if not optional_true_marker(source_message, policy["pull_requests"]["rollback_marker"]):
                    raise PolicyError("trial rollback reconciliation requires a marked hotfix source")
                source_parents = parents(root, main_sha)
                if len(source_parents) != 1:
                    raise PolicyError("rollback source on main must be one linear commit")
                validate_phase_transition_payload(root, source_parents[0], main_sha)
            elif new_phase != old_phase:
                raise PolicyError("hotfix reconciliation cannot change phase without Trial-Rollback: true")
            if not is_ancestor(root, main_sha, after):
                raise PolicyError("hotfix reconciliation must make main an ancestor of dev")
            validate_hotfix_result(root, before, main_sha, after)
            return PolicyResult(kind="reconciliation-hotfix-resolved")

        if main_policy["trial"]["phase"] == "bootstrap" and old_phase == "bootstrap":
            if marker_values(source_message, policy["pull_requests"]["activation_marker"]):
                raise PolicyError("activation source must carry trial phase policy")
            if not optional_true_marker(source_message, policy["pull_requests"]["bootstrap_marker"]):
                raise PolicyError("bootstrap synchronization requires Branch-Policy-Bootstrap: true")
            if not trees_equal(root, after, main_sha):
                raise PolicyError("bootstrap synchronization merge tree must equal main")
            if not is_ancestor(root, main_sha, after):
                raise PolicyError("bootstrap synchronization must make main an ancestor of dev")
            return PolicyResult(kind="reconciliation-bootstrap")
        if marker_values(source_message, policy["pull_requests"]["activation_marker"]):
            if old_phase != "bootstrap" or new_phase != "trial":
                raise PolicyError("bootstrap reconciliation requires bootstrap -> trial phase transition")
            validate_activation_attestations(policy, source_message)
            source_parents = parents(root, main_sha)
            if len(source_parents) != 1:
                raise PolicyError("activation source on main must be one linear commit")
            validate_phase_transition_payload(root, source_parents[0], main_sha)
            if not trees_equal(root, after, main_sha):
                raise PolicyError("bootstrap reconciliation merge tree must equal activated main")
            if not is_ancestor(root, main_sha, after):
                raise PolicyError("bootstrap reconciliation must make activated main an ancestor of dev")
            return PolicyResult(kind="reconciliation-bootstrap")

        release_type = required_marker(source_message, policy["pull_requests"]["release_type_marker"])
        if release_type not in {"regular", "hotfix"}:
            raise PolicyError("reconciliation source main commit lacks a valid Release-Type")
        if old_phase == "trial" and new_phase == "bootstrap":
            if release_type != "hotfix" or not optional_true_marker(
                source_message,
                policy["pull_requests"]["rollback_marker"],
            ):
                raise PolicyError("trial rollback reconciliation requires a marked hotfix source")
            source_parents = parents(root, main_sha)
            if len(source_parents) != 1:
                raise PolicyError("rollback source on main must be one linear commit")
            validate_phase_transition_payload(root, source_parents[0], main_sha)
        if not is_ancestor(root, main_sha, after):
            raise PolicyError("reconciliation must make main an ancestor of dev")
        if release_type == "regular" and not (
            trees_equal(root, before, main_sha)
            and trees_equal(root, after, before)
            and trees_equal(root, after, main_sha)
        ):
            raise PolicyError("regular reconciliation must preserve the identical main/dev tip tree")
        if release_type == "hotfix":
            validate_hotfix_result(root, before, main_sha, after)
        return PolicyResult(kind=f"reconciliation-{release_type}")

    if old_phase == "bootstrap":
        raise PolicyError("topic merges are blocked until bootstrap reconciliation activates the trial")
    if new_phase != old_phase:
        raise PolicyError("topic merges cannot change the branch trial phase")
    if not is_ancestor(root, main_sha, before):
        raise PolicyError("topic merge is blocked until current main is an ancestor of prior dev")
    validate_subject_range(root, policy, before, second_parent)
    return PolicyResult(kind="topic", evidence_commit=second_parent)


def write_outputs(path: Path | None, result: PolicyResult) -> None:
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        for key, value in [
            ("kind", result.kind),
            ("evidence_commit", result.evidence_commit),
            ("review_path", result.review_path),
            ("review_commit", result.review_commit),
        ]:
            handle.write(f"{key}={value}\n")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--root", type=Path, default=Path("."))
    root.add_argument("--policy", type=Path)
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("config")
    pull_request = sub.add_parser("pull-request")
    pull_request.add_argument("--event-path", type=Path, required=True)
    pull_request.add_argument("--checkout", choices=["integration", "head"], required=True)
    pull_request.add_argument("--github-output", type=Path)
    push = sub.add_parser("push")
    push.add_argument("--event-path", type=Path, required=True)
    push.add_argument("--github-output", type=Path)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    try:
        candidate_policy = load_policy(root, args.policy)
        if args.command == "config":
            result = PolicyResult(kind="config")
        elif args.command == "pull-request":
            result = validate_pull_request(root, candidate_policy, load_json(args.event_path), args.checkout)
        else:
            result = validate_push(root, candidate_policy, load_json(args.event_path))
        write_outputs(getattr(args, "github_output", None), result)
        print(f"branch policy OK: {result.kind}")
        return 0
    except (PolicyError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
