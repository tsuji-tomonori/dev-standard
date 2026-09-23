from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/audit_consistency.py"
SPEC = importlib.util.spec_from_file_location("audit_consistency", PATH)
assert SPEC and SPEC.loader
audit_consistency = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_consistency)


class AuditConsistencyTest(unittest.TestCase):
    def test_audit_docs_rejects_retired_fixed_profile_triggers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs/reference").mkdir(parents=True)
            (root / "docs/requirements").mkdir(parents=True)
            (root / ".agents/skills").mkdir(parents=True)
            (root / "AGENTS.md").write_text("Current instructions.\n", encoding="utf-8")
            (root / "README.md").write_text("Current overview.\n", encoding="utf-8")
            (root / "docs/guide.md").write_text(
                "Create work state for the regulated profile.\n",
                encoding="utf-8",
            )
            (root / "docs/reference/skill-evidence-audit.md").write_text(
                "tools/audit_consistency.py 2026-08-29\n",
                encoding="utf-8",
            )
            findings: list[dict[str, str]] = []
            with mock.patch.object(audit_consistency, "ROOT", root):
                audit_consistency.audit_docs(findings, {})
            self.assertTrue(
                any(item["check_id"] == "AUD-RETIRED-PROFILE" for item in findings)
            )

    def adapter_contract_fixture(self, root: Path) -> None:
        skill = ".agents/skills/generate-implementation-design"
        files = {
            f"{skill}/scripts/check_design.py": "# portable adapter checker\n",
            f"{skill}/scripts/reference_inventory.py": "# inventory checker\n",
            "tests/test_design_adoption.py": "# behavioral contract fixtures\n",
            "tests/test_reference_inventory.py": "# inventory fixtures\n",
            f"{skill}/assets/api-document-profile-v1.json": '{"version": 1}',
            "distribution/manifest.json": json.dumps({"profiles": {
                name: [{"source": skill}] for name in ("default", "chat-first")}}),
        }
        schema = json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema",
                             "type": "object", "required": ["version"],
                             "properties": {"version": {"type": "integer"}}})
        for name in ("adapter-manifest", "reference-inventory"):
            files[f"{skill}/assets/{name}.schema.json"] = schema
        for name in ("governance/checks/catalog.yaml",
                     ".agents/skills/inspect-quality-gates/scripts/inspect.py",
                     "tests/test_inspect_runner.py"):
            files[name] = (ROOT / name).read_text()
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def test_adapter_contract_audit_needs_no_language_executor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.adapter_contract_fixture(root)
            findings = []
            with mock.patch.object(audit_consistency, "ROOT", root):
                audit_consistency.audit_generated_design(findings)
            self.assertEqual(findings, [])

    def test_adapter_contract_audit_detects_missing_asset_schema_and_distribution(self) -> None:
        mutations = (
            ("AUD-DESIGN-CONTRACT", lambda root: (root / ".agents/skills/generate-implementation-design/scripts/reference_inventory.py").unlink()),
            ("AUD-DESIGN-SCHEMA", lambda root: (root / ".agents/skills/generate-implementation-design/assets/adapter-manifest.schema.json").write_text('{"type":"object"}')),
            ("AUD-DESIGN-DISTRIBUTION", lambda root: (root / "distribution/manifest.json").write_text('{"profiles":{"default":[],"chat-first":[]}}')),
        )
        for check_id, mutate in mutations:
            with self.subTest(check_id=check_id), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.adapter_contract_fixture(root)
                mutate(root)
                findings = []
                with mock.patch.object(audit_consistency, "ROOT", root):
                    audit_consistency.audit_generated_design(findings)
                self.assertIn(check_id, {item["check_id"] for item in findings})

    def test_current_skills_docs_traces_and_generators_pass(self) -> None:
        result = audit_consistency.run_audit()
        catalog = json.loads(
            (ROOT / "spec/requirements/requirements.json").read_text(encoding="utf-8")
        )
        active_ids = {
            item["id"]
            for item in catalog["requirements"]
            if item["status"] == "active"
        }
        self.assertEqual(result["overall"], "合格", result["findings"])
        self.assertEqual(result["blocking_findings"], 0)
        self.assertEqual(result["metrics"]["skill_count"], 18)
        self.assertEqual(result["metrics"]["requirement_count"], len(active_ids))
        self.assertLessEqual(audit_consistency.AUTO_REQUIREMENTS, active_ids)
        self.assertEqual(
            result["metrics"]["auto_generation_requirement_count"],
            len(audit_consistency.AUTO_REQUIREMENTS),
        )
        self.assertEqual(result["metrics"]["missing_trace_count"], 0)
        self.assertLessEqual(result["metrics"]["skill_description_characters"], 5000)


if __name__ == "__main__":
    unittest.main()
