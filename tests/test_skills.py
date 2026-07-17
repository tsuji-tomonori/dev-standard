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
        text = (ROOT / "docs" / "SKILLS.md").read_text(encoding="utf-8")
        listed = set(__import__("re").findall(r"^\| `([a-z0-9-]+)` \|", text, __import__("re").MULTILINE))
        actual = {path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}
        self.assertEqual(listed, actual)

    def test_chat_first_skill_owns_setup_and_full_delivery(self) -> None:
        skill = SKILLS / "chat-first-development"
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        reference = (skill / "references" / "bootstrap-and-conversation.md").read_text(encoding="utf-8")
        for required in [
            "ordinary natural-language conversation",
            "Automatically prepare",
            "Never ask the user to run Python",
            "one explicit approve/reject decision",
            "PR creation",
            "CI verification",
            "lightweight",
        ]:
            self.assertIn(required, text)
        for required in ["repository-local", "Do not stop", "Lightweight record", "Do not merge"]:
            self.assertIn(required, reference)

    def test_root_instructions_make_commands_ai_owned(self) -> None:
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("$chat-first-development", text)
        self.assertIn("Never ask the user to run setup", text)
        self.assertIn("AI-owned commands", text)
        self.assertIn("ordinary conversation", text)
        self.assertIn("spec/requirements/requirements.json", text)
        self.assertIn("`work/<id>/` is noncanonical", text)

    def test_three_pillar_skills_have_deterministic_contracts(self) -> None:
        requirements = (SKILLS / "maintain-canonical-requirements" / "SKILL.md").read_text(encoding="utf-8")
        design = (SKILLS / "generate-implementation-design" / "SKILL.md").read_text(encoding="utf-8")
        standards = (SKILLS / "verify-against-engineering-standards" / "SKILL.md").read_text(encoding="utf-8")
        for required in ["only durable requirements authority", "add", "update", "retire", "subject", "action", "object", "initial requester authorization"]:
            self.assertIn(required, requirements)
        for required in ["router.py", "functions.py", "OpenAPI", "SQLGlot AST", "CloudFormation", "SHA-256", "--check"]:
            self.assertIn(required, design)
        for required in [
            "official",
            "version",
            "fresh",
            "Pass",
            "N/A",
            "Fail",
            "direct Pass evidence",
            "project severity",
            "remediation plan",
            "recheck",
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
        paths = [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "docs" / "FLOW.md"]
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

    def test_ai_operating_policy_preserves_outcome_and_checks(self) -> None:
        text = (ROOT / "docs" / "AI-OPERATING-POLICY.md").read_text(encoding="utf-8")
        for required in [
            "達成結果",
            "成功条件",
            "権限境界",
            "gpt-5.6-terra",
            "gpt-5.6-luna",
            "決定的な検証契約",
            "最小指示の回帰チェック",
        ]:
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
