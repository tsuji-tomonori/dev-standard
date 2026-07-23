from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"
    spec = importlib.util.spec_from_file_location("specflow", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


specflow = load_module()


class SpecflowTest(unittest.TestCase):
    def test_self_hosted_catalog_is_valid_and_generated_view_is_current(self) -> None:
        catalog = specflow.validate_catalog(specflow.read_json(ROOT / "spec/requirements/requirements.json"))
        generated = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        self.assertEqual(generated, specflow.render(catalog))
        self.assertEqual(len(catalog["requirements"]), 49)
        self.assertIn("# dev-standard 要件一覧", generated)
        by_id = {item["id"]: item for item in catalog["requirements"]}
        self.assertEqual(by_id["REQ-DESIGN-006"]["revision"], 3)
        self.assertEqual(by_id["REQ-ASBUILT-016"]["object"], "C0命令網羅95%以上とC1分岐網羅90%以上のcoverage")
        self.assertEqual(by_id["REQ-ASBUILT-019"]["type"], "operational")
        self.assertEqual(by_id["REQ-DISC-005"]["scope"], "product")
        self.assertEqual(by_id["REQ-DISC-005"]["category"], "functional")
        self.assertEqual(by_id["REQ-DISC-005"]["last_changed_by"], "CHG-20260724-solution-neutral-requirements")
        self.assertIn("issue:25", by_id["REQ-DISC-005"]["source_refs"])

    def test_json_schema_matches_runtime_classification_contract(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        schema = specflow.read_json(
            ROOT / ".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"
        )
        validator = Draft202012Validator(schema)
        self.assertEqual([], list(validator.iter_errors(catalog)))

        requirement_schema = schema["properties"]["requirements"]["items"]
        self.assertEqual(["product", "project"], requirement_schema["properties"]["scope"]["enum"])
        self.assertEqual(
            ["functional", "nonfunctional"],
            requirement_schema["properties"]["category"]["enum"],
        )
        self.assertEqual(
            {"scope": ["category"], "category": ["scope"]},
            requirement_schema["dependentRequired"],
        )

        invalid = copy.deepcopy(catalog)
        item = next(value for value in invalid["requirements"] if value["id"] == "REQ-DISC-005")
        del item["category"]
        self.assertTrue(list(validator.iter_errors(invalid)))
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

    def test_composite_action_and_clause_are_rejected(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        catalog["requirements"][0]["action"] = "separate and persist"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(catalog)
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        catalog["requirements"][0]["action"] = "separate_and_persist"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(catalog)
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        catalog["requirements"][0]["object"] += "; and another obligation"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(catalog)

    def test_update_is_version_checked_and_does_not_mutate_input_on_failure(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        original = copy.deepcopy(catalog)
        change = {
            "base_catalog_revision": catalog["catalog_revision"],
            "changed_at": "2026-07-18",
            "work_item": "WI-TEST-UPDATE",
            "operations": [{
                "op": "update",
                "id": "REQ-FRAME-001",
                "expected_revision": 2,
                "changes": {"rationale": "テストで更新した根拠。"},
            }],
        }
        updated = specflow.apply_change(catalog, change)
        item = next(value for value in updated["requirements"] if value["id"] == "REQ-FRAME-001")
        self.assertEqual(item["revision"], 3)
        self.assertEqual(updated["catalog_revision"], catalog["catalog_revision"] + 1)
        self.assertEqual(catalog, original)
        stale = copy.deepcopy(change)
        stale["base_catalog_revision"] = 0
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(catalog, stale)
        self.assertEqual(catalog, original)

    def test_retire_preserves_tombstone_and_apply_regenerates_docs(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        change = {
            "base_catalog_revision": catalog["catalog_revision"],
            "changed_at": "2026-07-18",
            "work_item": "WI-TEST-RETIRE",
            "operations": [{
                "op": "retire",
                "id": "REQ-FRAME-001",
                "expected_revision": 2,
                "reason": "ライフサイクルテストで置換されたため",
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "requirements.json"
            delta = root / "change.json"
            output = root / "REQUIREMENTS.md"
            source.write_text(specflow.canonical_json(catalog), encoding="utf-8")
            delta.write_text(json.dumps(change), encoding="utf-8")
            result = specflow.main(["apply", "--spec", str(source), "--change", str(delta), "--out", str(output)])
            self.assertEqual(result, 0)
            retired = specflow.read_json(source)
            item = next(value for value in retired["requirements"] if value["id"] == "REQ-FRAME-001")
            self.assertEqual(item["status"], "retired")
            self.assertIn("置換", item["retirement_reason"])
            self.assertEqual(output.read_text(encoding="utf-8"), specflow.render(retired))


if __name__ == "__main__":
    unittest.main()
