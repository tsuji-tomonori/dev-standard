#!/usr/bin/env python3
"""Validate the lightweight three-pillar reference repository contract."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    from .render_skills import (
        REPOSITORY_POLICY_FIELDS,
        validate_contract_catalog,
        validate_policy_file,
    )
except ImportError:  # Support direct execution as ``python tools/validate_repo.py``.
    from render_skills import (
        REPOSITORY_POLICY_FIELDS,
        validate_contract_catalog,
        validate_policy_file,
    )

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
DEFAULT_SKILLS = {
    "chat-first-development",
    "generate-implementation-design",
    "inspect-quality-gates",
    "maintain-canonical-requirements",
}
GUARDRAILS = {
    "generate-implementation-design",
    "inspect-quality-gates",
    "maintain-canonical-requirements",
}
IGNORED_PARTS = {"__pycache__"}

_FORBIDDEN_PORTABLE_SEGMENTS = {
    ".buildkite",
    ".circleci",
    ".github",
    ".gitlab",
    ".githooks",
    ".husky",
    "branch-policy",
    "branch-protection",
    "merge-policy",
    "merge-queue",
    "merge-request-templates",
    "merge_request_templates",
    "pull_request_template",
    "pull-request-templates",
    "pull_request_templates",
    "rulesets",
}
_FORBIDDEN_PORTABLE_NAMES = {
    ".drone.yml",
    ".gitlab-ci.yml",
    ".mergify.yml",
    ".pre-commit-config.yaml",
    ".travis.yml",
    ".woodpecker.yml",
    "applypatch-msg",
    "appveyor.yml",
    "azure-pipelines.yml",
    "bitbucket-pipelines.yml",
    "buildspec.yml",
    "codeowners",
    "commit-msg",
    "fsmonitor-watchman",
    "jenkinsfile",
    "merge_request_template.md",
    "p4-changelist",
    "p4-post-changelist",
    "p4-prepare-changelist",
    "p4-pre-submit",
    "post-applypatch",
    "post-checkout",
    "post-commit",
    "post-index-change",
    "post-merge",
    "post-receive",
    "post-rewrite",
    "post-update",
    "pre-commit",
    "pre-merge-commit",
    "pre-push",
    "pre-rebase",
    "pre-receive",
    "prepare-commit-msg",
    "pull_request_template.md",
    "push-to-checkout",
    "sendemail-validate",
    "teamcity-settings.kts",
    "wercker.yml",
}
_FORBIDDEN_CONFIG_NAME = re.compile(
    r"(?:^|[._-])(?:branch[-_]?protection|branch[-_]?policy|merge[-_]?(?:config|policy|queue)|"
    r"(?:pull[-_]?request|merge[-_]?request)[-_]?templates?|required[-_]?checks?|"
    r"rulesets?)(?:[._-]|$)",
    re.IGNORECASE,
)
_CI_CONFIG_NAME = re.compile(
    r"^(?:ci(?:[-_](?:config|pipeline|workflow))?|pipeline)\.(?:json|toml|ya?ml)$",
    re.IGNORECASE,
)
_COMMITLINT_CONFIG_NAME = re.compile(
    r"^(?:\.commitlintrc(?:\..+)?|commitlint\.config\..+)$",
    re.IGNORECASE,
)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_json(path: Path, failures: list[str]) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}", failures)
        return {}
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: root must be an object", failures)
        return {}
    return value


def _relative_manifest_path(value: object, label: str, failures: list[str]) -> PurePosixPath | None:
    if not isinstance(value, str) or not value or value == "." or "\\" in value:
        fail(f"{label}: path must be a non-root portable POSIX path: {value!r}", failures)
        return None
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail(f"{label}: path escapes or aliases the repository root: {value!r}", failures)
        return None
    return path


def _forbidden_portable_path(path: PurePosixPath) -> str | None:
    lowered = tuple(part.lower() for part in path.parts)
    name = lowered[-1] if lowered else ""
    if ".git" in lowered and "hooks" in lowered:
        return "Git hook"
    if any(part in _FORBIDDEN_PORTABLE_SEGMENTS for part in lowered):
        return "repository policy directory"
    if len(lowered) >= 2 and lowered[-2:] == ("governance", "reviews"):
        return "per-change review records"
    if "governance" in lowered and "reviews" in lowered:
        return "per-change review records"
    if (
        name in _FORBIDDEN_PORTABLE_NAMES
        or _CI_CONFIG_NAME.fullmatch(name)
        or _COMMITLINT_CONFIG_NAME.fullmatch(name)
        or re.fullmatch(r"(?:pull|merge)[-_]request[-_]template(?:\..+)?", name)
    ):
        return "CI, hook, ownership, or pull-request configuration"
    if _FORBIDDEN_CONFIG_NAME.search(name):
        return "branch, ruleset, required-check, or merge configuration"
    return None


def _runner_local_mappings(
    runtime: dict[str, Any],
    root: Path,
    failures: list[str],
    *,
    destination_root: PurePosixPath | None = None,
) -> list[dict[str, str]]:
    runner = runtime.get("runner")
    if (
        not isinstance(runner, dict)
        or set(runner) != {"source", "destination", "local_imports"}
        or runner.get("local_imports") != "derive-from-_load_pinned_tool-calls"
    ):
        fail("portable runtime runner mapping is invalid", failures)
        return []
    source = _relative_manifest_path(runner.get("source"), "portable runtime runner source", failures)
    if source is None:
        return []
    source_path = root.joinpath(*source.parts)
    try:
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        fail(f"portable runtime runner import closure is unreadable: {exc}", failures)
        return []
    names: set[str] = set()
    for node in ast.walk(tree):
        if (
            not isinstance(node, ast.Call)
            or not isinstance(node.func, ast.Name)
            or node.func.id != "_load_pinned_tool"
            or len(node.args) != 1
        ):
            continue
        try:
            name = ast.literal_eval(node.args[0])
        except (ValueError, TypeError):
            fail("portable runtime runner has a dynamic pinned tool import", failures)
            continue
        if not isinstance(name, str) or not name.isidentifier():
            fail(f"portable runtime runner has an invalid pinned tool import: {name!r}", failures)
            continue
        names.add(name)
    if not names:
        fail("portable runtime runner has no auditable pinned tool imports", failures)
    return [
        {
            "source": f"tools/{name}.py",
            "destination": (
                (destination_root / f"tools/{name}.py").as_posix()
                if destination_root is not None
                else f"tools/{name}.py"
            ),
        }
        for name in sorted(names)
    ]


def _manifest_mappings(
    manifest: dict[str, Any],
    root: Path,
    failures: list[str],
) -> Iterable[tuple[str, dict[str, Any]]]:
    profiles = manifest.get("profiles")
    if not isinstance(profiles, dict):
        fail("manifest profiles are invalid", failures)
    else:
        for profile, entries in profiles.items():
            if not isinstance(entries, list):
                fail(f"{profile}: mappings must be a list", failures)
                continue
            for entry in entries:
                if not isinstance(entry, dict):
                    fail(f"{profile}: invalid mapping", failures)
                    continue
                yield f"profile {profile}", entry

    formal = manifest.get("formal_skill_contracts")
    if not isinstance(formal, dict) or not isinstance(formal.get("mappings"), list):
        fail("formal Skill contract mappings are invalid", failures)
    else:
        for entry in formal["mappings"]:
            if not isinstance(entry, dict):
                fail("formal Skill contract mapping is invalid", failures)
                continue
            yield "formal Skill contract", entry

    runtime = manifest.get("portable_runtime")
    if not isinstance(runtime, dict) or not isinstance(runtime.get("mappings"), list):
        fail("portable runtime mappings are invalid", failures)
        return
    runner = runtime.get("runner")
    if isinstance(runner, dict):
        yield "portable runtime runner", runner
    for entry in runtime["mappings"]:
        if not isinstance(entry, dict):
            fail("portable runtime mapping is invalid", failures)
            continue
        yield "portable runtime", entry
    for entry in _runner_local_mappings(runtime, root, failures):
        yield "portable runtime derived import", entry

    support = manifest.get("skill_runner_support")
    if support is None:
        return
    dependency = support.get("dependency_runtime") if isinstance(support, dict) else None
    if not isinstance(dependency, dict):
        fail("Skill dependency runtime is invalid", failures)
        return
    runtime_root = _relative_manifest_path(
        dependency.get("runtime_root"),
        "Skill dependency runtime root",
        failures,
    )
    runner = dependency.get("runner")
    if runtime_root is None or not isinstance(runner, dict):
        fail("Skill dependency runtime runner is invalid", failures)
        return
    effective_runner = dict(runner)
    destination = _relative_manifest_path(
        runner.get("destination"),
        "Skill dependency runtime runner destination",
        failures,
    )
    if destination is None:
        return
    effective_runner["destination"] = (runtime_root / destination).as_posix()
    yield "Skill dependency runtime runner", effective_runner
    for entry in _runner_local_mappings(
        dependency,
        root,
        failures,
        destination_root=runtime_root,
    ):
        yield "Skill dependency runtime derived import", entry


def _expanded_mapping_leaves(
    root: Path,
    label: str,
    mapping: dict[str, Any],
    failures: list[str],
) -> Iterable[tuple[Path, PurePosixPath, PurePosixPath]]:
    allowed = {"source", "destination"}
    if label.endswith("runtime runner"):
        allowed.add("local_imports")
    if set(mapping) != allowed:
        fail(f"{label}: invalid mapping fields: {sorted(mapping)}", failures)
        return
    source = _relative_manifest_path(mapping.get("source"), f"{label} source", failures)
    destination = _relative_manifest_path(mapping.get("destination"), f"{label} destination", failures)
    if source is None or destination is None:
        return
    for role, path in (("source", source), ("destination", destination)):
        reason = _forbidden_portable_path(path)
        if reason:
            fail(f"{label}: {role} is protected ({reason}): {path}", failures)
    source_path = root.joinpath(*source.parts)
    current = root
    for part in source.parts:
        current = current / part
        if current.is_symlink():
            fail(f"{label}: source traverses a symlink: {source}", failures)
            return
    if not source_path.exists():
        fail(f"{label}: missing source {source}", failures)
        return
    if source_path.is_file():
        yield source_path, source, destination
        return
    if not source_path.is_dir():
        fail(f"{label}: source is not a regular file or directory: {source}", failures)
        return
    for leaf in sorted(source_path.rglob("*")):
        relative = leaf.relative_to(source_path)
        if IGNORED_PARTS.intersection(relative.parts) or leaf.suffix == ".pyc":
            continue
        if leaf.is_symlink():
            fail(f"{label}: mapped tree contains a symlink: {source / relative.as_posix()}", failures)
            continue
        if not leaf.is_file():
            continue
        source_leaf = source / PurePosixPath(relative.as_posix())
        destination_leaf = destination / PurePosixPath(relative.as_posix())
        yield leaf, source_leaf, destination_leaf


def validate_manifest_document(
    manifest: dict[str, Any],
    root: Path,
    failures: list[str],
) -> None:
    """Expand every portable mapping and audit its actual source/destination leaves."""

    scanned_sources: set[Path] = set()
    destinations: dict[PurePosixPath, tuple[PurePosixPath, str]] = {}
    for label, mapping in _manifest_mappings(manifest, root, failures):
        for source_path, source_leaf, destination_leaf in _expanded_mapping_leaves(
            root,
            label,
            mapping,
            failures,
        ):
            for role, path in (("source", source_leaf), ("destination", destination_leaf)):
                reason = _forbidden_portable_path(path)
                if reason:
                    fail(f"{label}: expanded {role} is protected ({reason}): {path}", failures)
            previous = destinations.get(destination_leaf)
            if previous is None:
                destinations[destination_leaf] = (source_leaf, label)
            elif previous[0] != source_leaf:
                fail(
                    f"{label}: destination collision at {destination_leaf}: "
                    f"{previous[0]} ({previous[1]}) vs {source_leaf}",
                    failures,
                )
            if source_path in scanned_sources:
                continue
            scanned_sources.add(source_path)
            failures.extend(validate_policy_file(source_path, source_leaf.as_posix()))


def frontmatter(path: Path, failures: list[str]) -> dict[str, str]:
    import yaml

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: YAML frontmatter missing", failures)
        return {}
    try:
        values = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"{path.relative_to(ROOT)}: invalid YAML frontmatter: {exc}", failures)
        return {}
    if not isinstance(values, dict) or any(
        not isinstance(values.get(key), str) for key in ("name", "description")
    ):
        fail(f"{path.relative_to(ROOT)}: name and description must be YAML strings", failures)
        return {}
    return {key: values[key] for key in ("name", "description")}


def validate_skills(failures: list[str]) -> None:
    actual = {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    manifest = load_json(ROOT / "distribution" / "manifest.json", failures)
    inventory = set(manifest.get("inventory", {}).get("skills", [])) if manifest else set()
    formal = load_json(ROOT / "spec" / "skills" / "skills.json", failures)
    contracts = formal.get("contracts", []) if formal else []
    try:
        validate_contract_catalog(contracts)
    except ValueError as exc:
        fail(f"formal Skill catalog is invalid: {exc}", failures)
    formal_names = {
        item.get("name")
        for item in contracts
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    if actual != inventory:
        fail(f"Skill inventory drift: tree={sorted(actual)} manifest={sorted(inventory)}", failures)
    if actual != formal_names:
        fail(f"Skill formalization drift: tree={sorted(actual)} formal={sorted(formal_names)}", failures)

    for name in sorted(actual):
        skill = SKILLS_ROOT / name / "SKILL.md"
        metadata = frontmatter(skill, failures)
        if metadata.get("name") != name:
            fail(f"{name}: frontmatter name does not match directory", failures)
        if len(metadata.get("description", "")) < 40:
            fail(f"{name}: description is incomplete", failures)
        text = skill.read_text(encoding="utf-8")
        if "spec/skills/skills.qnt" not in text or f'name: "{name}"' not in text:
            fail(f"{name}: Quint trace missing", failures)
        openai = SKILLS_ROOT / name / "agents" / "openai.yaml"
        if not openai.is_file():
            fail(f"{name}: agents/openai.yaml missing", failures)
        elif f"${name}" not in openai.read_text(encoding="utf-8"):
            fail(f"{name}: agents/openai.yaml default prompt must name ${name}", failures)

    guardrails = {
        item["name"]
        for item in contracts
        if isinstance(item, dict) and item.get("guardrail") is True
    }
    defaults = {
        item["name"]
        for item in contracts
        if isinstance(item, dict) and item.get("defaultPortable") is True
    }
    if guardrails != GUARDRAILS:
        fail(f"formal guardrails must be exactly three: {sorted(guardrails)}", failures)
    if defaults != DEFAULT_SKILLS:
        fail(f"formal default portable set must contain four Skills: {sorted(defaults)}", failures)
    for item in contracts:
        if not isinstance(item, dict):
            fail("Skill contract must be an object", failures)
            continue
        policy = item.get("repositoryPolicy")
        if not isinstance(policy, dict) or set(policy) != set(REPOSITORY_POLICY_FIELDS):
            fail(f"{item.get('name')}: repository policy fields are incomplete", failures)
        elif any(type(policy[field]) is not bool or policy[field] for field in REPOSITORY_POLICY_FIELDS):
            fail(f"{item.get('name')}: portable repository policy must remain host-owned", failures)
        if type(item.get("repositoryBlocking")) is not bool or item.get("repositoryBlocking") != item.get("guardrail"):
            fail(f"{item.get('name')}: repository blocking must match the three guardrails", failures)
        if type(item.get("defaultPortable")) is not bool:
            fail(f"{item.get('name')}: defaultPortable must be boolean", failures)
        if type(item.get("externalEffect")) is not bool:
            fail(f"{item.get('name')}: externalEffect must be boolean", failures)
        contexts = item.get("activationContexts")
        if not isinstance(contexts, list) or not contexts or not all(isinstance(value, str) and value for value in contexts):
            fail(f"{item.get('name')}: activationContexts must be a non-empty string list", failures)


def validate_manifest(failures: list[str]) -> None:
    manifest = load_json(ROOT / "distribution" / "manifest.json", failures)
    if manifest.get("schema_version") != 4:
        fail("manifest schema_version must be 4", failures)
    protected = manifest.get("protected_repository_paths")
    if not isinstance(protected, list) or not protected or not all(isinstance(value, str) for value in protected):
        fail("manifest protected_repository_paths must be a non-empty string list", failures)
    validate_manifest_document(manifest, ROOT, failures)

    profiles = manifest.get("profiles", {}) if manifest else {}
    if not isinstance(profiles, dict):
        fail("manifest profiles are invalid", failures)
        return

    for profile in ["default", "chat-first"]:
        entries = profiles.get(profile, [])
        names = {
            Path(str(entry["source"])).name
            for entry in entries
            if str(entry.get("source", "")).startswith(".agents/skills/")
        }
        if names != DEFAULT_SKILLS:
            fail(f"{profile}: must contain only the entry Skill and three pillars", failures)


def validate_repo(failures: list[str]) -> None:
    validate_skills(failures)
    validate_manifest(failures)

    required = [
        "AGENTS.md",
        "README.md",
        "package.json",
        "package-lock.json",
        "spec/requirements/requirements.qnt",
        "spec/requirements/requirements.json",
        "spec/skills/skills.qnt",
        "spec/skills/skills.json",
        "docs/requirements/REQUIREMENTS.md",
        "tools/quintflow.py",
        ".github/workflows/governance.yml",
    ]
    for path in required:
        if not (ROOT / path).is_file():
            fail(f"required repository file missing: {path}", failures)
    for removed in [".github/branch-policy.json", "tools/branch_policy.py", "tests/test_branch_policy.py"]:
        if (ROOT / removed).exists():
            fail(f"retired branch enforcement remains: {removed}", failures)

    requirements = load_json(ROOT / "spec" / "requirements" / "requirements.json", failures)
    by_id = {
        item.get("id"): item
        for item in requirements.get("requirements", [])
        if isinstance(item, dict)
    }
    for retired in ["REQ-REPO-001", "REQ-REPO-002", "REQ-REPO-003"]:
        if by_id.get(retired, {}).get("status") != "retired":
            fail(f"{retired}: branch enforcement requirement must be retired", failures)
    for active in ["REQ-QUINT-001", "REQ-QUINT-002", "REQ-QUINT-003", "REQ-PORTABLE-002", "REQ-QUALITY-004"]:
        if by_id.get(active, {}).get("status") != "active":
            fail(f"{active}: new three-pillar requirement must be active", failures)

    workflow = (ROOT / ".github" / "workflows" / "governance.yml").read_text(encoding="utf-8")
    jobs = workflow.split("jobs:\n", 1)[1] if "jobs:\n" in workflow else ""
    if len(re.findall(r"^  [a-zA-Z0-9_-]+:\s*$", jobs, re.MULTILINE)) != 1:
        fail("Governance workflow must contain one job", failures)
    for required_text in ["  verify:", "python-version: \"3.12\"", "node-version: \"24\"", "make verify"]:
        if required_text not in workflow:
            fail(f"Governance workflow missing: {required_text}", failures)
    for forbidden in ["branch-policy", "needs:", "required check", "governance/reviews"]:
        if forbidden in workflow:
            fail(f"Governance workflow contains retired enforcement: {forbidden}", failures)

    root_markdown = {path.name for path in ROOT.glob("*.md")}
    if root_markdown != {"README.md", "AGENTS.md"}:
        fail(f"root Markdown layout is invalid: {sorted(root_markdown)}", failures)
    docs_list = (ROOT / "docs" / "guides" / "getting-started.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", docs_list, re.MULTILINE))
    if listed != DEFAULT_SKILLS:
        fail("getting-started default Skill inventory drift", failures)



def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--skills-only", action="store_true")
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    failures: list[str] = []
    if args.skills_only:
        validate_skills(failures)
    else:
        validate_repo(failures)
    if failures:
        for message in failures:
            print(f"ERROR: {message}")
        return 2
    print("repository contract valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
