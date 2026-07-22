from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


class SkillContractTest(unittest.TestCase):
    def test_adversarial_review_seeks_defects_without_becoming_security_red_teaming(self) -> None:
        skill = SKILLS / "adversarial-review"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        research = (skill / "references" / "research-basis.md").read_text(encoding="utf-8")
        playbook = (skill / "references" / "challenge-playbook.md").read_text(encoding="utf-8")
        for required in [
            "falsifiable claims",
            "smallest observation that would prove this wrong",
            "authoritative source",
            "independently",
            "positive assertions",
            "metamorphic",
            "swap pairwise order",
            "not proof of correctness",
            "not security red teaming",
        ]:
            self.assertIn(required, text)
        for source in ["QuickCheck", "Metamorphic Testing", "Mutation Testing", "Active Design Reviews", "Perspective-Based Reading", "NASA"]:
            self.assertIn(source, research)
        for target in ["Requirements", "Architecture", "Implementation", "Tests", "Document/change set"]:
            self.assertIn(target, playbook)
        for security_specific in ["prompt injection", "jailbreak", "exfiltration", "attacker goal", "threat model"]:
            self.assertNotIn(security_specific, text.lower())

    def test_skills_catalog_matches_skill_directories(self) -> None:
        text = (ROOT / "docs" / "guides" / "getting-started.md").read_text(encoding="utf-8")
        listed = set(__import__("re").findall(r"^\| `([a-z0-9-]+)` \|", text, __import__("re").MULTILINE))
        actual = {path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}
        self.assertEqual(listed, actual)

    def test_chat_first_skill_owns_adaptive_setup_and_delivery(self) -> None:
        skill = SKILLS / "chat-first-development"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        reference = (skill / "references" / "bootstrap-and-conversation.md").read_text(encoding="utf-8")
        for required in [
            "ordinary natural-language conversation",
            "direct",
            "assured",
            "regulated",
            "Commit Comment",
            "governance/reviews",
            "PRを作成",
            "GitHub Actions",
            ".devflow/run/",
        ]:
            self.assertIn(required, text)
        for required in [
            "repository-local",
            "利用者へfileのコピーやinstallation commandの実行を求めて作業を停止しない",
            "`direct`と`assured`では、恒久的な`work/<id>/`を作成しない",
            "direct",
            "assured",
            "regulated",
            ".devflow/run/",
            "公開API",
            "authority boundary",
            "明示的な権限なしにmergeしない",
        ]:
            self.assertIn(required, reference)
        for forbidden in [
            "Lightweight record",
            "Create `work/<id>/`",
            "初回承認を一度だけ記録する",
            "日付+slug計画書を作成する",
        ]:
            self.assertNotIn(forbidden, reference)

    def test_as_built_standard_is_connected_without_a_second_orchestrator(self) -> None:
        standard = (ROOT / "docs" / "standards" / "AS-BUILT-DESIGN.md").read_text(encoding="utf-8")
        selection = (
            SKILLS
            / "verify-against-engineering-standards"
            / "references"
            / "as-built-design-check-selection.md"
        ).read_text(encoding="utf-8")
        chat = (SKILLS / "chat-first-development" / "SKILL.md").read_text(encoding="utf-8")
        sizing = (SKILLS / "right-size-execution" / "SKILL.md").read_text(encoding="utf-8")
        for required in [
            "docs/design/generated/",
            ".gen.md",
            "FAST-006",
            "FAST-016",
            "FAST-019",
            "C0命令網羅95%以上",
            "C1分岐網羅90%以上",
            "repositoryへ実行結果を保存しない",
            "公開API変更だけを理由にユーザー承認を要求しない",
        ]:
            self.assertIn(required, standard)
        for check_id in [
            "FAST-016",
            "FAST-017",
            "FAST-018",
            "FAST-019",
            "FAST-020",
            "FAST-021",
            "FAST-022",
            "FAST-023",
            "AUD-008",
        ]:
            self.assertIn(check_id, selection)
        self.assertIn("as-built-design-check-selection.md", chat)
        self.assertIn("日付+slug計画書", sizing)
        self.assertNotIn("計画書を軸に段階的スキル", standard)

    def test_contribution_surfaces_follow_profile_and_authority_boundaries(self) -> None:
        contributing = (ROOT / ".github" / "CONTRIBUTING.md").read_text(encoding="utf-8")
        pull_request = (ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        combined = contributing + "\n" + pull_request
        for required in [
            "direct",
            "assured",
            "regulated",
            "governance/reviews",
            "公開API",
            "authority boundary",
        ]:
            self.assertIn(required, combined)
        for forbidden in [
            "1. `tools/devflow.py init`でwork itemを作成する。",
            "work item ID",
            "当該工程の全チェック項目",
            "現行ダイジェストに対する必要承認",
        ]:
            self.assertNotIn(forbidden, combined)

    def test_right_size_execution_selects_an_auditable_adaptive_profile(self) -> None:
        skill = SKILLS / "right-size-execution"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        policy = json.loads((skill / "assets" / "execution-policy.json").read_text(encoding="utf-8"))
        for required in [
            "direct",
            "assured",
            "regulated",
            "Soft budget",
            ".devflow/run/",
            "同時拡張",
            "scope",
            "assurance",
            "compute",
            "mode",
            "成功条件",
        ]:
            self.assertIn(required, text)
        self.assertEqual(policy["max_metadata_probes"], 1)
        self.assertEqual(policy["expansion_axes"], ["scope", "assurance", "verification", "review", "compute"])
        self.assertNotIn("max_expansions", policy)
        self.assertIn("governance", policy["assurance_floors"]["elevated"])
        self.assertEqual(policy["rollout_phase"], "shadow")

    def test_root_instructions_make_commands_and_artifacts_ai_owned(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for required in [
            "$chat-first-development",
            "direct",
            "assured",
            "regulated",
            "Commit Comment",
            "governance/reviews",
            ".devflow/run/",
            "spec/requirements/requirements.json",
            "CI結果",
        ]:
            self.assertIn(required, text)
        self.assertIn("利用者へSkill名", (SKILLS / "chat-first-development" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertIn("通常変更で恒久的な`work/<id>/`", text)

    def test_three_pillar_skills_have_deterministic_contracts(self) -> None:
        requirements = (SKILLS / "maintain-canonical-requirements" / "SKILL.md").read_text(encoding="utf-8")
        design = (SKILLS / "generate-implementation-design" / "SKILL.md").read_text(encoding="utf-8")
        standards = (SKILLS / "verify-against-engineering-standards" / "SKILL.md").read_text(encoding="utf-8")
        for required in [
            "永続要件の唯一の正本",
            "add",
            "update",
            "retire",
            "主体",
            "行為",
            "対象",
            "acceptance criteria",
            "Commit Comment",
        ]:
            self.assertIn(required, requirements)
        for required in ["router.py", "functions.py", "OpenAPI", "SQLGlot AST", "CloudFormation", "SHA-256", "--check"]:
            self.assertIn(required, design)
        for required in [
            "official",
            "version",
            "Invariant",
            "Risk-selected",
            "Advisory",
            "Periodic",
            "Pass",
            "N/A",
            "Fail",
            "review YAML",
            "GitHub Actions",
        ]:
            self.assertIn(required, standards)

    def test_requirement_research_supports_listening_divergence_and_review_perspectives(self) -> None:
        research = (SKILLS / "maintain-canonical-requirements" / "references" / "research-basis.md").read_text(encoding="utf-8")
        for required in ["Design Council", "Double Diamond", "SWEBOK", "NASA", "Perspective-Based Reading", "stakeholder", "tester"]:
            self.assertIn(required, research)

    def test_single_authorization_policy_has_no_later_phase_approvals(self) -> None:
        policy = json.loads((ROOT / "governance" / "policy.json").read_text(encoding="utf-8"))
        authorization = policy["authorization"]
        self.assertEqual(authorization, {
            "phase": "requirements",
            "role": "requester",
            "title": "初回自律実行承認",
        })
        for phase, definition in policy["phases"].items():
            expected = ["requester"] if phase == "requirements" else []
            self.assertEqual(definition["required_approvals"], expected, phase)
        self.assertIn(
            "docs/01-execution-plan.md",
            policy["phases"]["requirements"]["required_docs"],
        )

    def test_listening_skill_exposes_all_progressive_disclosure_references(self) -> None:
        skill = SKILLS / "calibrated-collaborative-listening"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        references = {
            "semantic-articulation-protocol.md",
            "japanese-response-patterns.md",
            "evaluation-rubric.md",
            "evidence-map.md",
        }
        for name in references:
            self.assertIn(f"references/{name}", text)
            self.assertTrue((skill / "references" / name).is_file())

    def test_semantic_protocol_protects_precision_and_logical_limiters(self) -> None:
        path = SKILLS / "calibrated-collaborative-listening" / "references" / "semantic-articulation-protocol.md"
        text = path.read_text(encoding="utf-8")
        for required in [
            "Prohibition",
            "negation",
            "condition",
            "exception",
            "number",
            "date",
            "attribution",
            "Semantic checksum",
        ]:
            self.assertIn(required, text)

    def test_listening_rubric_blocks_sycophancy_and_meaning_loss(self) -> None:
        path = SKILLS / "calibrated-collaborative-listening" / "references" / "evaluation-rubric.md"
        text = path.read_text(encoding="utf-8")
        for required in [
            "Non-sycophancy",
            "Non-patronizing",
            "Completeness",
            "Faithfulness",
            "Critical failures",
            "22/28",
        ]:
            self.assertIn(required, text)

    def test_governance_instructions_do_not_reference_removed_workflows(self) -> None:
        paths = [
            ROOT / "AGENTS.md",
            ROOT / "README.md",
            ROOT / "docs" / "reference" / "development.md",
        ]
        paths.extend(path for path in SKILLS.glob("*/SKILL.md"))
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for removed in [
            "$record-governance-approval",
            "improvement-approve",
            "improvement-apply",
        ]:
            self.assertNotIn(removed, combined)

    def test_custom_reviewers_use_minimal_cost_bounded_models(self) -> None:
        allowed_effort = {"low", "medium", "high"}
        for path in sorted((ROOT / ".codex" / "agents").glob("*.toml")):
            value = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value["model"], "gpt-5.6-terra", path.name)
            self.assertIn(value["model_reasoning_effort"], allowed_effort, path.name)
            self.assertEqual(value["model_verbosity"], "low", path.name)
            self.assertLessEqual(len(value["developer_instructions"]), 900, path.name)

    def test_development_reference_preserves_stable_outcome_and_checks(self) -> None:
        text = (ROOT / "docs" / "reference" / "development.md").read_text(encoding="utf-8")
        for required in [
            "利用者が得る結果",
            "権限境界",
            "決定的な検証",
            "必要な能力",
            "selected check",
        ]:
            self.assertIn(required, text)
        user_docs = [ROOT / "README.md", *(ROOT / "docs").rglob("*.md")]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in user_docs)
        self.assertNotIn("gpt-5.6-terra", combined)
        self.assertNotIn("gpt-5.6-luna", combined)


if __name__ == "__main__":
    unittest.main()
