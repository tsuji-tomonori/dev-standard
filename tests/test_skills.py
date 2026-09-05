from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


class SkillContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.formal = json.loads((ROOT / "spec/skills/skills.json").read_text(encoding="utf-8"))
        cls.contracts = {item["name"]: item for item in cls.formal["contracts"]}
        cls.actual = {path.name for path in SKILLS.iterdir() if (path / "SKILL.md").is_file()}

    def test_every_skill_has_exactly_one_quint_contract_and_trace(self) -> None:
        self.assertEqual(set(self.contracts), self.actual)
        self.assertEqual(len(self.actual), 18)
        for name in self.actual:
            text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("spec/skills/skills.qnt", text, name)
            self.assertEqual(text.count(f'name: "{name}"'), 1, name)

    def test_only_three_pillars_are_guardrails(self) -> None:
        guardrails = {
            name: contract["pillar"]
            for name, contract in self.contracts.items()
            if contract["guardrail"]
        }
        self.assertEqual(
            guardrails,
            {
                "maintain-canonical-requirements": "requirements",
                "generate-implementation-design": "design",
                "inspect-quality-gates": "checks",
            },
        )
        for name, contract in self.contracts.items():
            with self.subTest(skill=name):
                self.assertIs(type(contract["repositoryBlocking"]), bool)
                self.assertEqual(
                    contract["repositoryBlocking"],
                    contract["guardrail"],
                )

    def test_default_contract_is_entry_plus_three_pillars(self) -> None:
        for name, item in self.contracts.items():
            with self.subTest(skill=name):
                self.assertIs(type(item["defaultPortable"]), bool)
        defaults = {
            name for name, item in self.contracts.items() if item["defaultPortable"]
        }
        self.assertEqual(
            defaults,
            {
                "chat-first-development",
                "maintain-canonical-requirements",
                "generate-implementation-design",
                "inspect-quality-gates",
            },
        )

    def test_repository_policy_is_host_owned_for_all_skills(self) -> None:
        expected_fields = {
            "ciWorkflow",
            "requiredCheck",
            "branchProtection",
            "ruleset",
            "mergeStrategy",
            "prTemplate",
            "commitFormat",
        }
        for name, contract in self.contracts.items():
            with self.subTest(skill=name):
                policy = contract["repositoryPolicy"]
                self.assertEqual(set(policy), expected_fields)
                for field in expected_fields:
                    self.assertIs(type(policy[field]), bool, field)
                    self.assertFalse(policy[field], field)

    def test_skill_catalog_matches_directories(self) -> None:
        guide = (ROOT / "docs/guides/getting-started.md").read_text(encoding="utf-8")
        listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", guide, re.MULTILINE))
        self.assertEqual(listed, self.actual)

    def test_three_pillar_human_contracts_match_formal_authority(self) -> None:
        requirements = (SKILLS / "maintain-canonical-requirements/SKILL.md").read_text(encoding="utf-8")
        design = (SKILLS / "generate-implementation-design/SKILL.md").read_text(encoding="utf-8")
        checks = (SKILLS / "inspect-quality-gates/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("requirements.qnt → requirements.json → REQUIREMENTS.md", requirements)
        self.assertIn("実装artifact", design)
        self.assertIn("byte一致", design)
        self.assertIn("CIがないこと自体を失敗にしない", checks)
        for text in [requirements, design, checks]:
            self.assertIn("merge rule", text)

    def test_optional_commit_style_is_not_a_gate(self) -> None:
        text = (SKILLS / "japanese-git-commit-gitmoji/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("場合だけ使用", text)
        self.assertIn("portable default", text)
        self.assertFalse(self.contracts["japanese-git-commit-gitmoji"]["guardrail"])


if __name__ == "__main__":
    unittest.main()
