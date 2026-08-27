from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QuintFlowContractTest(unittest.TestCase):
    def test_requirements_quint_declares_atomicity_and_retirement_invariants(self) -> None:
        text = (ROOT / "spec/requirements/requirements.qnt").read_text(encoding="utf-8")
        for invariant in [
            "requirementIdsAreUnique",
            "requirementsAreAtomicAndVerifiable",
            "classificationIsPaired",
            "retirementIsExplicit",
            "catalogWellFormed",
        ]:
            self.assertIn(invariant, text)

    def test_distributed_requirement_template_is_quint_and_not_json(self) -> None:
        assets = ROOT / ".agents/skills/maintain-canonical-requirements/assets"
        template = assets / "requirements.template.qnt"
        self.assertTrue(template.is_file())
        self.assertFalse((assets / "requirements.template.json").exists())
        text = template.read_text(encoding="utf-8")
        for invariant in [
            "requirementIdsAreUnique",
            "requirementsAreAtomicAndVerifiable",
            "classificationIsPaired",
            "retirementIsExplicit",
            "catalogWellFormed",
        ]:
            self.assertIn(invariant, text)

    def test_skill_quint_declares_portability_and_three_pillar_invariants(self) -> None:
        text = (ROOT / "spec/skills/skills.qnt").read_text(encoding="utf-8")
        for invariant in [
            "contractsAreComplete",
            "threePillarsOnly",
            "repositoryPolicyIsHostOwned",
            "defaultProfileIsMinimal",
            "workflowOrderIsConsistent",
            "portablePolicyIsUntouched",
        ]:
            self.assertIn(invariant, text)

    def test_derived_documents_declare_their_sources(self) -> None:
        skills = json.loads((ROOT / "spec/skills/skills.json").read_text(encoding="utf-8"))
        self.assertEqual(skills["source"], "spec/skills/skills.qnt")
        self.assertEqual(skills["quint_version"], "0.32.0")
        requirements_doc = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        skills_doc = (ROOT / "docs/reference/FORMAL-SPECIFICATIONS.md").read_text(encoding="utf-8")
        self.assertIn("requirements.qntを編集すること", requirements_doc)
        self.assertIn("skills.qntを編集すること", skills_doc)


if __name__ == "__main__":
    unittest.main()
