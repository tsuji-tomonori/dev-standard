from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReferenceRepositoryContractTest(unittest.TestCase):
    def test_repository_does_not_store_live_work_items(self) -> None:
        self.assertFalse((ROOT / "work").exists())
        self.assertIn(".devflow/run/", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))

    def test_markdown_is_grouped_by_audience(self) -> None:
        self.assertEqual({"README.md", "AGENTS.md"}, {path.name for path in ROOT.glob("*.md")})
        self.assertEqual({"README.md"}, {path.name for path in (ROOT / "docs").glob("*.md")})

    def test_quint_is_the_only_edited_requirements_authority(self) -> None:
        for path in [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / ".agents/skills/maintain-canonical-requirements/SKILL.md",
            ROOT / "docs/decisions/ADR-0001-as-built-design-authority-and-scope.md",
            ROOT / "docs/standards/AS-BUILT-DESIGN.md",
            ROOT / "docs/standards/REQUIREMENT-CLASSIFICATION.md",
            ROOT / "docs/templates/00-request.md",
            ROOT / "docs/templates/01-traceability.md",
        ]:
            self.assertIn("spec/requirements/requirements.qnt", path.read_text(encoding="utf-8"), path)
        generated = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        self.assertIn("requirements.qntを編集すること", generated)
        self.assertIn("機械可読view", generated)

    def test_new_portability_requirements_are_active_and_branch_contracts_retired(self) -> None:
        catalog = json.loads((ROOT / "spec/requirements/requirements.json").read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in catalog["requirements"]}
        for active in ["REQ-QUINT-001", "REQ-QUINT-002", "REQ-QUINT-003", "REQ-PORTABLE-002", "REQ-QUALITY-004"]:
            self.assertEqual(by_id[active]["status"], "active")
        for retired in ["REQ-REPO-001", "REQ-REPO-002", "REQ-REPO-003"]:
            self.assertEqual(by_id[retired]["status"], "retired")
            self.assertTrue(by_id[retired]["retirement_reason"])

    def test_governance_workflow_is_one_lightweight_job(self) -> None:
        workflow = (ROOT / ".github/workflows/governance.yml").read_text(encoding="utf-8")
        jobs = workflow.split("jobs:\n", 1)[1]
        self.assertEqual(re.findall(r"^  ([a-zA-Z0-9_-]+):$", jobs, re.MULTILINE), ["verify"])
        for removed in ["branch-policy", "evidence:", "integration:", "needs:"]:
            self.assertNotIn(removed, jobs)

    def test_adr_records_the_current_decision_and_formal_limit(self) -> None:
        adr = (ROOT / "docs/decisions/ADR-0004-quint-three-pillar-portability.md").read_text(
            encoding="utf-8"
        )
        for required in ["Accepted", "Quint", "3本", "CI workflow", "絶対的に証明"]:
            self.assertIn(required, adr)


if __name__ == "__main__":
    unittest.main()
