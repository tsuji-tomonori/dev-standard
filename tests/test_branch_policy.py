from __future__ import annotations

import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools import branch_policy

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / ".github" / "branch-policy.json"
REPOSITORY_POLICY = branch_policy.load_policy(ROOT)
POLICY = copy.deepcopy(REPOSITORY_POLICY)
POLICY["trial"]["phase"] = "bootstrap"
TRIAL_POLICY = copy.deepcopy(REPOSITORY_POLICY)
TRIAL_POLICY["trial"]["phase"] = "trial"


def run(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise AssertionError((result.stdout + result.stderr).strip())
    return result.stdout.strip()


def write(root: Path, path: str, content: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    run(root, "add", path)


def policy_text(policy: dict[str, object]) -> str:
    return json.dumps(policy, ensure_ascii=False, indent=2) + "\n"


def commit(root: Path, message: str, files: dict[str, str] | None = None) -> str:
    for path, content in (files or {}).items():
        write(root, path, content)
    run(root, "commit", "-m", message)
    return run(root, "rev-parse", "HEAD")


def pr_event(
    base: str,
    head: str,
    base_sha: str,
    head_sha: str,
    body: str = "Refs #999\n",
    *,
    head_repository: str = "tsuji-tomonori/dev-standard",
) -> dict[str, object]:
    return {
        "pull_request": {
            "body": body,
            "base": {
                "ref": base,
                "sha": base_sha,
                "repo": {"full_name": "tsuji-tomonori/dev-standard"},
            },
            "head": {
                "ref": head,
                "sha": head_sha,
                "repo": {"full_name": head_repository},
            },
        }
    }


def release_manifest_text(
    release_type: str,
    review_path: str,
    *,
    included_pr: str = "#101",
    closing_issue: str = "#501",
    subject: str | None = None,
    extra_markers: list[str] | None = None,
) -> str:
    lines: list[str] = []
    if subject is not None:
        lines.extend([subject, ""])
    lines.extend(extra_markers or [])
    lines.extend(
        [
            f"Release-Type: {release_type}",
            f"Release-Review: {review_path}",
            f"Included-PRs: {included_pr}",
            f"Review-Checklist: {review_path}",
            f"Closes {closing_issue}",
            "",
            "## 含まれるPR",
            included_pr,
            "## 要件・設計影響",
            "要件・設計影響をrelease reviewへ集約する。",
            "## 互換性・rollback",
            "互換性を確認し、必要時はrevertまたはforward fixする。",
            "## 残存リスク",
            "既知の制約をrelease reviewへ記録する。",
        ]
    )
    return "\n".join(lines)


def bootstrap_release_manifest_text(
    review_path: str,
    *,
    subject: str | None = None,
) -> str:
    lines: list[str] = []
    if subject is not None:
        lines.extend([subject, ""])
    lines.extend(
        [
            "Branch-Policy-Bootstrap: true",
            "Release-Type: bootstrap",
            f"Release-Review: {review_path}",
            "Included-PRs: #26",
            f"Review-Checklist: {review_path}",
            "Refs #20",
            "",
            "## 含まれるPR",
            "#26",
            "## 要件・設計影響",
            "branch policyのbootstrap導入をdevからmainへ昇格する。",
            "## 互換性・rollback",
            "bootstrapのまま維持し、trial有効化は別変更で行う。",
            "## 残存リスク",
            "cross-branch lockは原子的ではないため単一operatorで実行する。",
        ]
    )
    return "\n".join(lines)


class Repository:
    def __init__(
        self,
        root: Path,
        *,
        policy: dict[str, object] | None = POLICY,
        with_dev: bool = True,
    ) -> None:
        self.root = root
        run(root, "init", "-b", "main")
        run(root, "config", "user.name", "Branch Policy Test")
        run(root, "config", "user.email", "branch-policy@example.invalid")
        files = {"state.txt": "base\n"}
        if policy is not None:
            files[".github/branch-policy.json"] = policy_text(policy)
        commit(root, "🧪 test(branches): 初期状態を作成する", files)
        if with_dev:
            run(root, "branch", "dev", "main")

    def sha(self, ref: str) -> str:
        return run(self.root, "rev-parse", ref)

    def checkout(self, branch: str, *, create: bool = False, start: str | None = None) -> None:
        if create:
            args = ["checkout", "-b", branch]
            if start:
                args.append(start)
            run(self.root, *args)
        else:
            run(self.root, "checkout", branch)

    def merge(self, ref: str, subject: str) -> str:
        run(self.root, "merge", "--no-ff", ref, "-m", subject)
        return self.sha("HEAD")

    def squash(self, ref: str, message: str) -> str:
        run(self.root, "merge", "--squash", ref)
        return commit(self.root, message)

    def synthetic_merge(self, base: str, head: str) -> str:
        base_sha = self.sha(base)
        head_sha = self.sha(head)
        run(self.root, "checkout", "--detach", base_sha)
        run(self.root, "merge", "--no-ff", head_sha, "-m", "Synthetic merge")
        merge_sha = self.sha("HEAD")
        self.assert_parents(merge_sha, [base_sha, head_sha])
        return merge_sha

    def assert_parents(self, commit_sha: str, expected: list[str]) -> None:
        actual = run(self.root, "show", "-s", "--format=%P", commit_sha).split()
        if actual != expected:
            raise AssertionError((actual, expected))


class BranchPolicyTest(unittest.TestCase):
    def new_repository(
        self,
        *,
        policy: dict[str, object] | None = POLICY,
        with_dev: bool = True,
    ) -> Repository:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Repository(Path(temporary.name), policy=policy, with_dev=with_dev)

    def test_policy_is_repository_specific_and_matches_workflow_jobs(self) -> None:
        self.assertEqual(REPOSITORY_POLICY["repository"], "tsuji-tomonori/dev-standard")
        self.assertIn(REPOSITORY_POLICY["trial"]["phase"], {"bootstrap", "trial"})
        self.assertEqual(POLICY["trial"]["phase"], "bootstrap")
        self.assertEqual(TRIAL_POLICY["trial"]["phase"], "trial")
        self.assertEqual(REPOSITORY_POLICY["trial"]["release_cycles"], 2)
        self.assertFalse(REPOSITORY_POLICY["trial"]["portable_default"])
        self.assertTrue(REPOSITORY_POLICY["trial"]["single_release_operator"])
        self.assertFalse(REPOSITORY_POLICY["trial"]["atomic_cross_branch_lock"])
        for branch in ["main", "dev"]:
            self.assertEqual(
                REPOSITORY_POLICY["branches"][branch]["required_checks"],
                ["integration", "evidence", "branch-policy"],
            )
        self.assertEqual(REPOSITORY_POLICY["branches"]["main"]["merge_method"], "squash")
        self.assertEqual(REPOSITORY_POLICY["branches"]["dev"]["merge_method"], "merge")
        self.assertEqual(REPOSITORY_POLICY["pull_requests"]["reconciliation_prefixes"], ["reconcile/"])
        self.assertTrue(REPOSITORY_POLICY["pull_requests"]["issue_reference_pattern"])
        self.assertEqual(
            REPOSITORY_POLICY["trial"]["activation_requirements"],
            branch_policy.ACTIVATION_REQUIREMENTS,
        )

        workflow = (ROOT / ".github" / "workflows" / "governance.yml").read_text(encoding="utf-8")
        for required in [
            'git show "$base:$source"',
            'git show "$governing:$source"',
            '"$before:governance/reviews/validate.py"',
            "  verify:",
            "needs: [integration, evidence, branch-policy]",
        ]:
            self.assertIn(required, workflow)

        invalid_cycles = copy.deepcopy(REPOSITORY_POLICY)
        invalid_cycles["trial"]["release_cycles"] = 3
        with self.assertRaisesRegex(branch_policy.PolicyError, "exactly two"):
            branch_policy.validate_policy(invalid_cycles, "test")
        invalid_activation = copy.deepcopy(REPOSITORY_POLICY)
        invalid_activation["trial"]["activation_requirements"] = invalid_activation["trial"][
            "activation_requirements"
        ][:-1]
        with self.assertRaisesRegex(branch_policy.PolicyError, "approved bootstrap gate"):
            branch_policy.validate_policy(invalid_activation, "test")

    def test_first_policy_bootstrap_requires_marker_issue_reference_and_same_repository(self) -> None:
        repo = self.new_repository(policy=None, with_dev=False)
        base = repo.sha("main")
        repo.checkout("agent/issue-20", create=True, start="main")
        head = commit(
            repo.root,
            "✨ feat(branches): 二層branch契約を追加する",
            {
                ".github/branch-policy.json": policy_text(POLICY),
                "policy.txt": "candidate\n",
            },
        )
        body = "Branch-Policy-Bootstrap: true\nRefs #20\n"
        event = pr_event("main", "agent/issue-20", base, head, body)
        self.assertEqual(branch_policy.classify_pull_request(POLICY, event), "bootstrap")
        self.assertEqual(branch_policy.validate_pull_request(repo.root, POLICY, event, "head").kind, "bootstrap")

        invalid_bodies = [
            "Refs #20\n",
            "Branch-Policy-Bootstrap: true\n",
            "Branch-Policy-Bootstrap: false\nRefs #20\n",
            "<!--\nBranch-Policy-Bootstrap: true\n-->\nRefs #20\n",
        ]
        for invalid_body in invalid_bodies:
            with self.subTest(body=invalid_body), self.assertRaises(branch_policy.PolicyError):
                branch_policy.validate_pull_request(
                    repo.root,
                    POLICY,
                    pr_event("main", "agent/issue-20", base, head, invalid_body),
                    "head",
                )
        with self.assertRaisesRegex(branch_policy.PolicyError, "same repository"):
            branch_policy.validate_pull_request(
                repo.root,
                POLICY,
                pr_event(
                    "main",
                    "agent/issue-20",
                    base,
                    head,
                    body,
                    head_repository="someone/fork",
                ),
                "head",
            )

    def test_initial_policy_can_merge_to_synced_dev_then_open_bootstrap_release(self) -> None:
        repo = self.new_repository(policy=None)
        review_path = "governance/reviews/CHG-20260724-two-layer-branch-trial.yaml"

        repo.checkout("legacy/topic", create=True, start="main")
        commit(
            repo.root,
            "🧪 test(branches): reconciliation前の履歴を作成する",
            {"legacy.txt": "shared tree\n"},
        )
        repo.checkout("dev")
        repo.merge("legacy/topic", "🔀 test(branches): legacy履歴をdevへ統合する")
        repo.checkout("main")
        main = repo.squash(
            "legacy/topic",
            "🧪 test(branches): legacy履歴をmainへsquashする",
        )
        repo.checkout("dev")
        before_dev = repo.merge(
            "main",
            "🔄 test(branches): mainをdevへreconciliationする",
        )
        self.assertTrue(branch_policy.is_ancestor(repo.root, main, before_dev))
        self.assertTrue(branch_policy.trees_equal(repo.root, main, before_dev))

        repo.checkout("agent/issue-20", create=True, start="main")
        topic_head = commit(
            repo.root,
            (
                "🧭 feat(branches): 二層branch試行契約を実装する\n\n"
                "Branch-Policy-Bootstrap: true\n"
                "Review-Checklist: governance/reviews/CHG-20260724-two-layer-branch-trial.yaml\n"
                "Refs: #20"
            ),
            {
                ".github/branch-policy.json": policy_text(POLICY),
                review_path: "change_id: CHG-20260724-two-layer-branch-trial\n",
                "bootstrap.txt": "candidate\n",
            },
        )
        topic_body = "Branch-Policy-Bootstrap: true\nRefs #20\n"
        topic_event = pr_event("dev", "agent/issue-20", before_dev, topic_head, topic_body)
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, POLICY, topic_event, "head").kind,
            "bootstrap-topic",
        )
        repo.synthetic_merge("dev", "agent/issue-20")
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, POLICY, topic_event, "integration").kind,
            "bootstrap-topic",
        )

        repo.checkout("dev")
        before_push = repo.sha("dev")
        after_push = repo.merge("agent/issue-20", "🔀 feat(branches): bootstrap契約をdevへ統合する")
        candidate = branch_policy.load_policy(repo.root)
        dev_event = {
            "ref": "refs/heads/dev",
            "before": before_push,
            "after": after_push,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(
            branch_policy.validate_push(repo.root, candidate, dev_event).kind,
            "bootstrap-topic",
        )

        release_body = bootstrap_release_manifest_text(review_path)
        release_event = pr_event("main", "dev", main, after_push, release_body)
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, candidate, release_event, "head").kind,
            "bootstrap-release",
        )
        repo.synthetic_merge("main", "dev")
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, candidate, release_event, "integration").kind,
            "bootstrap-release",
        )

        repo.checkout("main")
        before_main = repo.sha("main")
        after_main = repo.squash(
            "dev",
            bootstrap_release_manifest_text(
                review_path,
                subject="🧭 feat(branches): bootstrap契約をmainへ昇格する",
            ),
        )
        main_event = {
            "ref": "refs/heads/main",
            "before": before_main,
            "after": after_main,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, candidate, main_event).kind, "main")
        self.assertTrue(branch_policy.trees_equal(repo.root, after_main, after_push))

    def test_bootstrap_blocks_topics_and_allows_main_synchronization(self) -> None:
        repo = self.new_repository(policy=POLICY)
        before_main = repo.sha("main")
        before_dev = repo.sha("dev")

        repo.checkout("feature/not-active", create=True, start="dev")
        topic_head = commit(
            repo.root,
            "✨ feat(core): activation前の変更を追加する",
            {"blocked.txt": "blocked\n"},
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "bootstrap phase rejects"):
            branch_policy.validate_pull_request(
                repo.root,
                POLICY,
                pr_event("dev", "feature/not-active", before_dev, topic_head, "Refs #20\n"),
                "head",
            )

        repo.checkout("main")
        after_main = commit(
            repo.root,
            "🛠️ fix(branches): bootstrap検査を補正する\n\nBranch-Policy-Bootstrap: true\nRefs: #20",
            {"bootstrap-fix.txt": "fixed\n"},
        )
        main_event = {
            "ref": "refs/heads/main",
            "before": before_main,
            "after": after_main,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, POLICY, main_event).kind, "main")

        body = "Reconciliation-Type: bootstrap\nSource-PR: #200\n"
        event = pr_event("dev", "main", before_dev, after_main, body)
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, POLICY, event, "head").kind,
            "reconciliation",
        )
        repo.synthetic_merge("dev", "main")
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, POLICY, event, "integration").kind,
            "reconciliation",
        )

        repo.checkout("dev")
        before_push = repo.sha("dev")
        after_push = repo.merge("main", "🔀 chore(branches): bootstrap修正を同期する")
        dev_event = {
            "ref": "refs/heads/dev",
            "before": before_push,
            "after": after_push,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(
            branch_policy.validate_push(repo.root, POLICY, dev_event).kind,
            "reconciliation-bootstrap",
        )
        self.assertTrue(branch_policy.trees_equal(repo.root, after_main, after_push))

    def test_bootstrap_to_trial_requires_every_activation_attestation(self) -> None:
        repo = self.new_repository(policy=POLICY)
        base = repo.sha("main")
        repo.checkout("agent/activate-trial", create=True, start="main")
        review_path = "governance/reviews/CHG-20260724-activate-trial.yaml"
        head = commit(
            repo.root,
            (
                "🔧 chore(branches): 二層branch試行を有効化する\n\n"
                f"Review-Checklist: {review_path}\n"
                "Refs: #20"
            ),
            {
                ".github/branch-policy.json": policy_text(TRIAL_POLICY),
                review_path: "change_id: CHG-20260724-activate-trial\n",
            },
        )
        checks = "\n".join(
            f"Activation-Check: {item}" for item in POLICY["trial"]["activation_requirements"]
        )
        body = (
            "Branch-Policy-Bootstrap: true\n"
            "Trial-Activation: true\n"
            f"{checks}\n"
            "Refs #20\n"
        )
        candidate = branch_policy.load_policy(repo.root)
        result = branch_policy.validate_pull_request(
            repo.root,
            candidate,
            pr_event("main", "agent/activate-trial", base, head, body),
            "head",
        )
        self.assertEqual(result.kind, "bootstrap")

        missing = body.replace(
            f"Activation-Check: {POLICY['trial']['activation_requirements'][-1]}\n",
            "",
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "attest every Activation-Check"):
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                pr_event("main", "agent/activate-trial", base, head, missing),
                "head",
            )

        extra = commit(
            repo.root,
            (
                "📝 docs(branches): activationへ無関係な変更を混在させる\n\n"
                f"Review-Checklist: {review_path}"
            ),
            {"unrelated.md": "not allowed\n"},
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "active review YAML"):
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                pr_event("main", "agent/activate-trial", base, extra, body),
                "head",
            )

    def test_activation_main_and_bootstrap_reconciliation_propagate_identical_policy(self) -> None:
        repo = self.new_repository(policy=POLICY)
        before_main = repo.sha("main")
        before_dev = repo.sha("dev")
        review_path = "governance/reviews/CHG-20260724-activate-transaction.yaml"
        attestations = "\n".join(
            f"Activation-Check: {item}" for item in POLICY["trial"]["activation_requirements"]
        )
        activation_message = "\n".join(
            [
                "🔧 chore(branches): 二層branch試行を有効化する",
                "",
                "Branch-Policy-Bootstrap: true",
                "Trial-Activation: true",
                attestations,
                f"Review-Checklist: {review_path}",
                "Refs: #20",
            ]
        )
        after_main = commit(
            repo.root,
            activation_message,
            {
                ".github/branch-policy.json": policy_text(TRIAL_POLICY),
                review_path: "change_id: CHG-20260724-activate-transaction\n",
            },
        )
        candidate = branch_policy.load_policy(repo.root)
        main_event = {
            "ref": "refs/heads/main",
            "before": before_main,
            "after": after_main,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, candidate, main_event).kind, "main")

        body = "Reconciliation-Type: bootstrap\nSource-PR: #201\n"
        event = pr_event("dev", "main", before_dev, after_main, body)
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, candidate, event, "head").kind,
            "reconciliation",
        )
        repo.synthetic_merge("dev", "main")
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, candidate, event, "integration").kind,
            "reconciliation",
        )

        repo.checkout("dev")
        before_push = repo.sha("dev")
        after_push = repo.merge("main", "🔀 chore(branches): activation policyを同期する")
        candidate = branch_policy.load_policy(repo.root)
        dev_event = {
            "ref": "refs/heads/dev",
            "before": before_push,
            "after": after_push,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(
            branch_policy.validate_push(repo.root, candidate, dev_event).kind,
            "reconciliation-bootstrap",
        )
        self.assertTrue(branch_policy.is_ancestor(repo.root, after_main, after_push))
        self.assertTrue(branch_policy.trees_equal(repo.root, after_main, after_push))

    def test_trial_direction_matrix_and_same_repository_release_heads(self) -> None:
        base = "1" * 40
        head = "2" * 40
        self.assertEqual(
            branch_policy.classify_pull_request(TRIAL_POLICY, pr_event("dev", "feature/example", base, head)),
            "topic",
        )
        self.assertEqual(
            branch_policy.classify_pull_request(TRIAL_POLICY, pr_event("main", "dev", base, head)),
            "release",
        )
        self.assertEqual(
            branch_policy.classify_pull_request(TRIAL_POLICY, pr_event("main", "hotfix/urgent", base, head)),
            "hotfix",
        )
        self.assertEqual(
            branch_policy.classify_pull_request(TRIAL_POLICY, pr_event("dev", "main", base, head)),
            "reconciliation",
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "trial phase rejects"):
            branch_policy.classify_pull_request(
                TRIAL_POLICY,
                pr_event("main", "feature/bypass", base, head),
            )
        with self.assertRaisesRegex(branch_policy.PolicyError, "this repository"):
            branch_policy.classify_pull_request(
                TRIAL_POLICY,
                pr_event("main", "dev", base, head, head_repository="someone/fork"),
            )

    def test_subject_contract_requires_gitmoji_conventional_and_japanese_without_wip(self) -> None:
        branch_policy.validate_subject(POLICY, "✨ feat(core): 日本語の変更を追加する", "good")
        branch_policy.validate_subject(POLICY, "♻️ refactor(core): 構造を整理する", "good-variation")
        invalid = [
            "feat(core): 日本語の変更を追加する",
            "fixup! ✨ feat(core): 日本語の変更を追加する",
            "squash! ✨ feat(core): 日本語の変更を追加する",
            "✨ feat(core): WIP 作業中",
            "✨ feat(core): checkpoint 仮",
            "✨ feat(core): add branch policy",
            "plain subject",
            "🚧 chore(core): 作業中の変更を保存する",
        ]
        for subject in invalid:
            with self.subTest(subject=subject), self.assertRaises(branch_policy.PolicyError):
                branch_policy.validate_subject(POLICY, subject, "bad")

    def test_subject_range_checks_nested_merge_commits(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        base = repo.sha("dev")
        repo.checkout("feature/nested", create=True, start="dev")
        commit(repo.root, "✨ feat(core): 最初の変更を追加する", {"first.txt": "first\n"})
        repo.checkout("feature/side", create=True, start="dev")
        commit(repo.root, "✨ feat(core): 側方の変更を追加する", {"side.txt": "side\n"})
        repo.checkout("feature/nested")
        run(repo.root, "merge", "--no-ff", "feature/side", "-m", "Merge feature/side")
        head = repo.sha("HEAD")
        with self.assertRaisesRegex(branch_policy.PolicyError, "Gitmoji"):
            branch_policy.validate_subject_range(repo.root, TRIAL_POLICY, base, head)

    def test_hidden_template_text_cannot_satisfy_markers_or_headings(self) -> None:
        hidden_samples = [
            "<!--\nRelease-Type: regular\n## 含まれるPR\n#100\n-->\n",
            "```text\nRelease-Type: regular\n## 含まれるPR\n#100\n```\n",
            "~~~markdown\nRelease-Type: regular\n## 含まれるPR\n#100\n~~~\n",
        ]
        for hidden in hidden_samples:
            with self.subTest(hidden=hidden):
                self.assertEqual(branch_policy.marker_values(hidden, "Release-Type"), [])
                with self.assertRaisesRegex(branch_policy.PolicyError, "exactly one"):
                    branch_policy.required_marker(hidden, "Release-Type")
                with self.assertRaisesRegex(branch_policy.PolicyError, "exactly one heading"):
                    branch_policy.heading_content(hidden, "## 含まれるPR")

    def test_policy_cannot_relax_its_own_contract(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        base = repo.sha("dev")
        repo.checkout("feature/relax", create=True, start="dev")
        relaxed = copy.deepcopy(TRIAL_POLICY)
        relaxed["commit_subject"]["conventional_pattern"] = "^.+$"
        relaxed["commit_subject"]["japanese_pattern"] = ".*"
        write(repo.root, ".github/branch-policy.json", policy_text(relaxed))
        head = commit(repo.root, "✨ feat(branches): policyを緩和する")
        event = pr_event("dev", "feature/relax", base, head)

        with self.assertRaisesRegex(branch_policy.PolicyError, "approved two-release trial"):
            branch_policy.load_policy(repo.root)
        with self.assertRaisesRegex(branch_policy.PolicyError, "immutable except for trial.phase"):
            branch_policy.validate_pull_request(repo.root, relaxed, event, "head")

    def test_topic_integration_checks_head_evidence_and_synthetic_merge(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        base = repo.sha("dev")
        repo.checkout("feature/topic", create=True, start="dev")
        head = commit(repo.root, "✨ feat(core): topic変更を追加する", {"topic.txt": "topic\n"})
        event = pr_event("dev", "feature/topic", base, head, "Refs #20\n")
        result = branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "head")
        self.assertEqual(result.kind, "topic")
        self.assertEqual(result.evidence_commit, head)

        repo.synthetic_merge("dev", "feature/topic")
        integration = branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "integration")
        self.assertEqual(integration.kind, "topic")

    def test_topic_pull_request_requires_refs_and_rejects_closing_keywords(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        base = repo.sha("dev")
        repo.checkout("feature/topic-reference", create=True, start="dev")
        head = commit(
            repo.root,
            "✨ feat(core): Issue参照を検査する変更を追加する",
            {"topic-reference.txt": "topic\n"},
        )

        for body in ["", "Issue #20\n", "<!-- Refs #20 -->\n"]:
            with self.subTest(body=body), self.assertRaisesRegex(
                branch_policy.PolicyError,
                "must reference at least one Issue with Refs",
            ):
                branch_policy.validate_pull_request(
                    repo.root,
                    TRIAL_POLICY,
                    pr_event("dev", "feature/topic-reference", base, head, body),
                    "head",
                )

        with self.assertRaisesRegex(branch_policy.PolicyError, "must use Refs"):
            branch_policy.validate_pull_request(
                repo.root,
                TRIAL_POLICY,
                pr_event("dev", "feature/topic-reference", base, head, "Closes #20\n"),
                "head",
            )

        self.assertEqual(
            branch_policy.validate_pull_request(
                repo.root,
                TRIAL_POLICY,
                pr_event("dev", "feature/topic-reference", base, head, "Refs: #20, #21\n"),
                "head",
            ).kind,
            "topic",
        )

    def test_release_requires_current_main_ancestor_manifest_and_fresh_review(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        main = repo.sha("main")
        repo.checkout("feature/change", create=True, start="dev")
        commit(repo.root, "✨ feat(core): release対象を追加する", {"feature.txt": "value\n"})
        repo.checkout("dev")
        repo.merge("feature/change", "🔀 chore(core): release対象を統合する")
        repo.checkout("chore/release-review", create=True, start="dev")
        review_path = "governance/reviews/CHG-20260724-release-one.yaml"
        commit(
            repo.root,
            "📝 docs(release): release reviewを追加する",
            {review_path: "change_id: CHG-20260724-release-one\n"},
        )
        repo.checkout("dev")
        repo.merge("chore/release-review", "🔀 chore(release): release reviewを統合する")
        head = repo.sha("dev")
        body = "\n".join(
            [
                "Release-Type: regular",
                f"Release-Review: {review_path}",
                "Included-PRs: #101",
                "Closes #501",
                "",
                "## 含まれるPR",
                "#101",
                "## 要件・設計影響",
                "REQ-REPO-001",
                "## 互換性・rollback",
                "互換性あり。revertで戻す。",
                "## 残存リスク",
                "既知の制約を記録済み。",
            ]
        )
        event = pr_event("main", "dev", main, head, body)
        result = branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "head")
        self.assertEqual(result.kind, "release")
        self.assertEqual(result.review_path, review_path)
        self.assertTrue(result.review_commit)

        repo.synthetic_merge("main", "dev")
        result = branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "integration")
        self.assertEqual(result.kind, "release")

        missing = body.replace("## 残存リスク", "## リスク")
        with self.assertRaisesRegex(branch_policy.PolicyError, "exactly one heading"):
            branch_policy.validate_pull_request(
                repo.root,
                TRIAL_POLICY,
                pr_event("main", "dev", main, head, missing),
                "integration",
            )

        inconsistent = body.replace("Included-PRs: #101", "Included-PRs: #999")
        with self.assertRaisesRegex(branch_policy.PolicyError, "same pull requests"):
            branch_policy.validate_pull_request(
                repo.root,
                TRIAL_POLICY,
                pr_event("main", "dev", main, head, inconsistent),
                "integration",
            )

        without_close = body.replace("Closes #501\n", "")
        with self.assertRaisesRegex(branch_policy.PolicyError, "close at least one Issue"):
            branch_policy.validate_pull_request(
                repo.root,
                TRIAL_POLICY,
                pr_event("main", "dev", main, head, without_close),
                "integration",
            )

    def test_release_reconciliation_restores_tree_and_ancestor_but_keeps_detail_commits(self) -> None:
        repo = self.new_repository()
        initial = repo.sha("main")
        repo.checkout("feature/first", create=True, start="dev")
        first_a = commit(repo.root, "✨ feat(core): 一回目の変更Aを追加する", {"first-a.txt": "a\n"})
        first_b = commit(repo.root, "✨ feat(core): 一回目の変更Bを追加する", {"first-b.txt": "b\n"})
        repo.checkout("dev")
        first_merge = repo.merge("feature/first", "🔀 chore(core): 一回目のtopicを統合する")

        repo.checkout("main")
        first_release = repo.squash("dev", "🚀 feat(release): 一回目の変更を公開する")
        self.assertTrue(branch_policy.trees_equal(repo.root, first_release, first_merge))
        self.assertFalse(branch_policy.is_ancestor(repo.root, first_release, first_merge))

        repo.checkout("dev")
        first_reconciliation = repo.merge("main", "🔀 chore(release): 一回目のreleaseを同期する")
        self.assertTrue(branch_policy.is_ancestor(repo.root, first_release, first_reconciliation))
        self.assertTrue(branch_policy.trees_equal(repo.root, first_release, first_reconciliation))
        detailed = set(run(repo.root, "rev-list", "main..dev").splitlines())
        self.assertTrue({first_a, first_b}.issubset(detailed))

        repo.checkout("feature/second", create=True, start="dev")
        second = commit(repo.root, "✨ feat(core): 二回目の変更を追加する", {"second.txt": "second\n"})
        repo.checkout("dev")
        second_merge = repo.merge("feature/second", "🔀 chore(core): 二回目のtopicを統合する")
        self.assertEqual(run(repo.root, "diff", "--name-only", "main", "dev"), "second.txt")
        self.assertEqual(run(repo.root, "diff", "--name-only", "main...dev"), "second.txt")
        detailed = set(run(repo.root, "rev-list", "main..dev").splitlines())
        self.assertTrue({first_a, first_b, second}.issubset(detailed))

        repo.checkout("main")
        second_release = repo.squash("dev", "🚀 feat(release): 二回目の変更を公開する")
        self.assertTrue(branch_policy.trees_equal(repo.root, second_release, second_merge))
        repo.checkout("dev")
        second_reconciliation = repo.merge("main", "🔀 chore(release): 二回目のreleaseを同期する")
        self.assertTrue(branch_policy.is_ancestor(repo.root, second_release, second_reconciliation))
        self.assertTrue(branch_policy.trees_equal(repo.root, second_release, second_reconciliation))
        self.assertTrue(branch_policy.is_ancestor(repo.root, initial, second_reconciliation))

    def test_delayed_release_reconciliation_can_conflict(self) -> None:
        repo = self.new_repository()
        repo.checkout("dev")
        commit(repo.root, "✨ feat(core): 公開対象の行を変更する", {"state.txt": "released\n"})
        repo.checkout("main")
        repo.squash("dev", "🚀 feat(release): 公開対象を反映する")
        repo.checkout("dev")
        commit(repo.root, "✨ feat(core): 同じ行へ未公開変更を追加する", {"state.txt": "unreleased\n"})
        result = subprocess.run(
            ["git", "merge", "--no-ff", "main", "-m", "Delayed reconciliation"],
            cwd=repo.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("CONFLICT", result.stdout + result.stderr)

    def test_release_reconciliation_requires_tree_equality_but_hotfix_does_not(self) -> None:
        hotfix_repo = self.new_repository(policy=TRIAL_POLICY)
        hotfix_repo.checkout("dev")
        dev = commit(hotfix_repo.root, "✨ feat(core): 未公開変更を追加する", {"unreleased.txt": "pending\n"})
        hotfix_repo.checkout("main")
        main = commit(
            hotfix_repo.root,
            "🩹 fix(core): 緊急修正を追加する\n\nRelease-Type: hotfix",
            {"hotfix.txt": "fixed\n"},
        )
        hotfix = pr_event(
            "dev",
            "main",
            dev,
            main,
            "Reconciliation-Type: hotfix\nSource-PR: #102\n",
        )
        self.assertEqual(
            branch_policy.validate_pull_request(hotfix_repo.root, TRIAL_POLICY, hotfix, "head").kind,
            "reconciliation",
        )
        hotfix_repo.synthetic_merge("dev", "main")
        self.assertEqual(
            branch_policy.validate_pull_request(
                hotfix_repo.root,
                TRIAL_POLICY,
                hotfix,
                "integration",
            ).kind,
            "reconciliation",
        )

        release_repo = self.new_repository(policy=TRIAL_POLICY)
        release_repo.checkout("dev")
        release_dev = commit(
            release_repo.root,
            "✨ feat(core): 未公開変更を追加する",
            {"unreleased.txt": "pending\n"},
        )
        release_repo.checkout("main")
        release_main = commit(
            release_repo.root,
            "🚀 feat(release): 通常releaseを記録する\n\nRelease-Type: regular",
            {"released.txt": "released\n"},
        )
        release = pr_event(
            "dev",
            "main",
            release_dev,
            release_main,
            "Reconciliation-Type: release\nSource-PR: #101\n",
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "equal main and dev"):
            branch_policy.validate_pull_request(release_repo.root, TRIAL_POLICY, release, "head")

    def test_hotfix_conflict_resolution_branch_preserves_both_histories_and_tree(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        hotfix_base = repo.sha("main")
        repo.checkout("dev")
        prior_dev = commit(
            repo.root,
            "✨ feat(core): 未公開の競合変更を追加する",
            {"state.txt": "dev\n"},
        )
        repo.checkout("main")
        main_sha = commit(
            repo.root,
            "🩹 fix(core): 緊急の競合修正を追加する\n\nRelease-Type: hotfix",
            {"state.txt": "hotfix\n"},
        )
        self.assertEqual(branch_policy.parents(repo.root, main_sha), [hotfix_base])

        repo.checkout("reconcile/hotfix-conflict", create=True, start="dev")
        conflict = subprocess.run(
            ["git", "merge", "--no-ff", "main", "-m", "Resolve hotfix conflict"],
            cwd=repo.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(conflict.returncode, 0)
        write(repo.root, "state.txt", "dev+hotfix\n")
        run(repo.root, "commit", "--no-edit")
        resolution_head = repo.sha("HEAD")
        repo.assert_parents(resolution_head, [prior_dev, main_sha])

        body = "Reconciliation-Type: hotfix\nSource-PR: #410\n"
        event = pr_event(
            "dev",
            "reconcile/hotfix-conflict",
            prior_dev,
            resolution_head,
            body,
        )
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "head").kind,
            "reconciliation",
        )

        repo.synthetic_merge("dev", "reconcile/hotfix-conflict")
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, TRIAL_POLICY, event, "integration").kind,
            "reconciliation",
        )

        repo.checkout("dev")
        after = repo.merge(
            "reconcile/hotfix-conflict",
            "🔀 chore(branches): hotfix競合解消を統合する",
        )
        push_event = {
            "ref": "refs/heads/dev",
            "before": prior_dev,
            "after": after,
            "forced": False,
            "deleted": False,
        }
        result = branch_policy.validate_push(repo.root, TRIAL_POLICY, push_event)
        self.assertEqual(result.kind, "reconciliation-hotfix-resolved")
        self.assertTrue(branch_policy.is_ancestor(repo.root, main_sha, after))
        self.assertEqual((repo.root / "state.txt").read_text(encoding="utf-8"), "dev+hotfix\n")

    def test_hotfix_reconciliation_rejects_ours_merge_that_drops_the_fix(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        repo.checkout("dev")
        prior_dev = commit(
            repo.root,
            "✨ feat(core): 未公開の競合変更を追加する",
            {"state.txt": "dev\n"},
        )
        repo.checkout("main")
        commit(
            repo.root,
            "🩹 fix(core): 緊急の競合修正を追加する\n\nRelease-Type: hotfix",
            {"state.txt": "hotfix\n"},
        )
        repo.checkout("dev")
        run(
            repo.root,
            "merge",
            "--no-ff",
            "-s",
            "ours",
            "main",
            "-m",
            "🔀 chore(branches): hotfixをoursで破棄する",
        )
        after = repo.sha("HEAD")
        event = {
            "ref": "refs/heads/dev",
            "before": prior_dev,
            "after": after,
            "forced": False,
            "deleted": False,
        }
        with self.assertRaisesRegex(branch_policy.PolicyError, "explicit integrated result"):
            branch_policy.validate_push(repo.root, TRIAL_POLICY, event)

    def test_push_audit_requires_one_main_commit_and_merge_only_dev_updates(self) -> None:
        repo = self.new_repository()
        before_main = repo.sha("main")
        repo.checkout("main")
        after_main = commit(
            repo.root,
            "📝 docs(core): mainの変更を追加する\n\nBranch-Policy-Bootstrap: true\nRefs: #20",
            {"main.txt": "one\n"},
        )
        main_event = {
            "ref": "refs/heads/main",
            "before": before_main,
            "after": after_main,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, POLICY, main_event).kind, "main")
        second = commit(
            repo.root,
            "📝 docs(core): 二つ目の変更を追加する\n\nBranch-Policy-Bootstrap: true\nRefs: #20",
            {"main-two.txt": "two\n"},
        )
        multi = {"ref": "refs/heads/main", "before": before_main, "after": second, "forced": False, "deleted": False}
        with self.assertRaisesRegex(branch_policy.PolicyError, "exactly one"):
            branch_policy.validate_push(repo.root, POLICY, multi)

        repo = self.new_repository(policy=TRIAL_POLICY)
        repo.checkout("feature/topic", create=True, start="dev")
        commit(repo.root, "✨ feat(core): topic変更を追加する", {"topic.txt": "topic\n"})
        repo.checkout("dev")
        before_dev = repo.sha("dev")
        after_dev = repo.merge("feature/topic", "🔀 chore(core): topic変更を統合する")
        topic_event = {
            "ref": "refs/heads/dev",
            "before": before_dev,
            "after": after_dev,
            "forced": False,
            "deleted": False,
        }
        result = branch_policy.validate_push(repo.root, TRIAL_POLICY, topic_event)
        self.assertEqual(result.kind, "topic")
        self.assertEqual(result.evidence_commit, repo.sha("feature/topic"))

        direct = commit(repo.root, "✨ feat(core): devへ直接変更を追加する", {"direct.txt": "bad\n"})
        direct_event = {
            "ref": "refs/heads/dev",
            "before": after_dev,
            "after": direct,
            "forced": False,
            "deleted": False,
        }
        with self.assertRaisesRegex(branch_policy.PolicyError, "merge commit"):
            branch_policy.validate_push(repo.root, TRIAL_POLICY, direct_event)

    def test_trial_main_push_audits_release_markers_review_and_frozen_tree(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        review_path = "governance/reviews/CHG-20260724-release-push.yaml"
        repo.checkout("feature/release", create=True, start="dev")
        commit(
            repo.root,
            "✨ feat(core): 公開対象を追加する",
            {
                "released.txt": "released\n",
                review_path: "change_id: CHG-20260724-release-push\n",
            },
        )
        repo.checkout("dev")
        repo.merge("feature/release", "🔀 chore(core): 公開対象を統合する")
        before = repo.sha("main")
        repo.checkout("main")
        message = "\n".join(
            [
                "🚀 feat(release): 通常releaseを公開する",
                "",
                "Release-Type: regular",
                f"Release-Review: {review_path}",
                "Included-PRs: #101",
                "Closes #501",
                "",
                "## 含まれるPR",
                "#101",
                "## 要件・設計影響",
                "REQ-REPO-001",
                "## 互換性・rollback",
                "互換性あり。revertで戻す。",
                "## 残存リスク",
                "既知の制約を記録済み。",
                f"Review-Checklist: {review_path}",
            ]
        )
        after = repo.squash("dev", message)
        event = {"ref": "refs/heads/main", "before": before, "after": after, "forced": False, "deleted": False}
        self.assertEqual(branch_policy.validate_push(repo.root, TRIAL_POLICY, event).kind, "main")

        invalid_repo = self.new_repository(policy=TRIAL_POLICY)
        invalid_repo.checkout("dev")
        commit(invalid_repo.root, "✨ feat(core): 公開対象を追加する", {"released.txt": "released\n"})
        invalid_before = invalid_repo.sha("main")
        invalid_repo.checkout("main")
        invalid_after = invalid_repo.squash("dev", "🚀 feat(release): markerなしで公開する")
        invalid_event = {
            "ref": "refs/heads/main",
            "before": invalid_before,
            "after": invalid_after,
            "forced": False,
            "deleted": False,
        }
        with self.assertRaisesRegex(branch_policy.PolicyError, "Release-Type"):
            branch_policy.validate_push(invalid_repo.root, TRIAL_POLICY, invalid_event)

        no_close_repo = self.new_repository(policy=TRIAL_POLICY)
        no_close_review = "governance/reviews/CHG-20260724-no-close-release.yaml"
        no_close_repo.checkout("feature/release", create=True, start="dev")
        commit(
            no_close_repo.root,
            "✨ feat(core): Issue closeなしの公開対象を追加する",
            {
                "released.txt": "released\n",
                no_close_review: "change_id: CHG-20260724-no-close-release\n",
            },
        )
        no_close_repo.checkout("dev")
        no_close_repo.merge("feature/release", "🔀 chore(core): 公開対象を統合する")
        no_close_before = no_close_repo.sha("main")
        no_close_repo.checkout("main")
        no_close_message = release_manifest_text(
            "regular",
            no_close_review,
            subject="🚀 feat(release): Issue closeなしで公開する",
        ).replace("Closes #501\n", "")
        no_close_after = no_close_repo.squash("dev", no_close_message)
        no_close_event = {
            "ref": "refs/heads/main",
            "before": no_close_before,
            "after": no_close_after,
            "forced": False,
            "deleted": False,
        }
        with self.assertRaisesRegex(branch_policy.PolicyError, "close at least one Issue"):
            branch_policy.validate_push(no_close_repo.root, TRIAL_POLICY, no_close_event)

        stale_repo = self.new_repository(policy=TRIAL_POLICY)
        stale_review = "governance/reviews/CHG-20260724-stale-release.yaml"
        stale_repo.checkout("main")
        commit(
            stale_repo.root,
            "📝 docs(release): 古いrelease reviewを追加する",
            {stale_review: "change_id: CHG-20260724-stale-release\n"},
        )
        run(stale_repo.root, "branch", "-f", "dev", "main")
        stale_repo.checkout("feature/release", create=True, start="dev")
        commit(
            stale_repo.root,
            "✨ feat(core): review更新なしの公開対象を追加する",
            {"released.txt": "released\n"},
        )
        stale_repo.checkout("dev")
        stale_repo.merge("feature/release", "🔀 chore(core): 公開対象を統合する")
        stale_before = stale_repo.sha("main")
        stale_repo.checkout("main")
        stale_message = "\n".join(
            [
                "🚀 feat(release): 古いreviewで通常releaseする",
                "",
                "Release-Type: regular",
                f"Release-Review: {stale_review}",
                "Included-PRs: #103",
                "Closes #503",
                "",
                "## 含まれるPR",
                "#103",
                "## 要件・設計影響",
                "REQ-REPO-001",
                "## 互換性・rollback",
                "互換性あり。revertで戻す。",
                "## 残存リスク",
                "古いreviewを意図的に参照する。",
                f"Review-Checklist: {stale_review}",
            ]
        )
        stale_after = stale_repo.squash("dev", stale_message)
        stale_event = {
            "ref": "refs/heads/main",
            "before": stale_before,
            "after": stale_after,
            "forced": False,
            "deleted": False,
        }
        with self.assertRaisesRegex(branch_policy.PolicyError, "created or updated after"):
            branch_policy.validate_push(stale_repo.root, TRIAL_POLICY, stale_event)

    def test_trial_rollback_hotfix_and_reconciliation_restore_bootstrap_phase(self) -> None:
        repo = self.new_repository(policy=TRIAL_POLICY)
        before_main = repo.sha("main")
        before_dev = repo.sha("dev")
        review_path = "governance/reviews/CHG-20260724-trial-rollback.yaml"
        rollback_message = "\n".join(
            [
                "🩹 fix(branches): 二層branch試行をrollbackする",
                "",
                "Trial-Rollback: true",
                "Release-Type: hotfix",
                f"Release-Review: {review_path}",
                "Included-PRs: #301",
                "Closes #302",
                "",
                "## 含まれるPR",
                "#301",
                "## 要件・設計影響",
                "branch trialをbootstrapへ戻す。",
                "## 互換性・rollback",
                "devをreconciliation後に凍結する。",
                "## 残存リスク",
                "未release変更とのconflictをPR上で解消する。",
                f"Review-Checklist: {review_path}",
            ]
        )
        repo.checkout("hotfix/trial-rollback", create=True, start="main")
        hotfix_head = commit(
            repo.root,
            rollback_message,
            {
                ".github/branch-policy.json": policy_text(POLICY),
                review_path: "change_id: CHG-20260724-trial-rollback\n",
            },
        )
        candidate = branch_policy.load_policy(repo.root)
        body = "\n".join(
            [
                "Trial-Rollback: true",
                "Release-Type: hotfix",
                f"Release-Review: {review_path}",
                "Included-PRs: #301",
                "Closes #302",
                "",
                "## 含まれるPR",
                "#301",
                "## 要件・設計影響",
                "branch trialをbootstrapへ戻す。",
                "## 互換性・rollback",
                "devをreconciliation後に凍結する。",
                "## 残存リスク",
                "未release変更とのconflictをPR上で解消する。",
            ]
        )
        hotfix_event = pr_event(
            "main",
            "hotfix/trial-rollback",
            before_main,
            hotfix_head,
            body,
        )
        self.assertEqual(
            branch_policy.validate_pull_request(repo.root, candidate, hotfix_event, "head").kind,
            "hotfix",
        )

        unrelated_head = commit(
            repo.root,
            (
                "📝 docs(branches): rollbackへ無関係な変更を混在させる\n\n"
                f"Review-Checklist: {review_path}"
            ),
            {"unrelated.md": "not allowed\n"},
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "phase transition may change only"):
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                pr_event(
                    "main",
                    "hotfix/trial-rollback",
                    before_main,
                    unrelated_head,
                    body,
                ),
                "head",
            )
        run(repo.root, "reset", "--hard", hotfix_head)

        run(repo.root, "branch", "-f", "main", hotfix_head)
        repo.checkout("main")
        main_event = {
            "ref": "refs/heads/main",
            "before": before_main,
            "after": hotfix_head,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, candidate, main_event).kind, "main")

        reconciliation_body = "Reconciliation-Type: hotfix\nSource-PR: #301\n"
        reconciliation_event = pr_event(
            "dev",
            "main",
            before_dev,
            hotfix_head,
            reconciliation_body,
        )
        self.assertEqual(
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                reconciliation_event,
                "head",
            ).kind,
            "reconciliation",
        )
        repo.synthetic_merge("dev", "main")
        self.assertEqual(
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                reconciliation_event,
                "integration",
            ).kind,
            "reconciliation",
        )

        repo.checkout("dev")
        before_push = repo.sha("dev")
        after_push = repo.merge("main", "🔀 chore(branches): rollback policyを同期する")
        candidate = branch_policy.load_policy(repo.root)
        dev_event = {
            "ref": "refs/heads/dev",
            "before": before_push,
            "after": after_push,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(
            branch_policy.validate_push(repo.root, candidate, dev_event).kind,
            "reconciliation-hotfix",
        )
        self.assertEqual(candidate["trial"]["phase"], "bootstrap")

        repo.checkout("feature/blocked-after-rollback", create=True, start="dev")
        blocked_head = commit(
            repo.root,
            "✨ feat(core): rollback後の変更を追加する",
            {"blocked-after-rollback.txt": "blocked\n"},
        )
        with self.assertRaisesRegex(branch_policy.PolicyError, "bootstrap phase rejects"):
            branch_policy.validate_pull_request(
                repo.root,
                candidate,
                pr_event("dev", "feature/blocked-after-rollback", after_push, blocked_head),
                "head",
            )

    def test_initial_dev_creation_and_forced_push_boundaries(self) -> None:
        repo = self.new_repository(with_dev=False)
        main = repo.sha("main")
        event = {
            "ref": "refs/heads/dev",
            "before": branch_policy.ZERO_SHA,
            "after": main,
            "created": True,
            "forced": False,
            "deleted": False,
        }
        self.assertEqual(branch_policy.validate_push(repo.root, POLICY, event).kind, "dev-bootstrap")
        forced = dict(event, before=main, created=False, forced=True)
        with self.assertRaisesRegex(branch_policy.PolicyError, "force push"):
            branch_policy.validate_push(repo.root, POLICY, forced)


if __name__ == "__main__":
    unittest.main()
