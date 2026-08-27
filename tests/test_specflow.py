from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

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
    def test_generated_json_is_valid_and_markdown_is_current(self) -> None:
        catalog = specflow.validate_catalog(
            specflow.read_json(ROOT / "spec/requirements/requirements.json")
        )
        generated = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        self.assertEqual(generated, specflow.render(catalog))
        self.assertEqual(catalog["catalog_revision"], 10)
        self.assertEqual(len(catalog["requirements"]), 57)
        self.assertEqual(sum(item["status"] == "active" for item in catalog["requirements"]), 54)
        self.assertIn("正本: `spec/requirements/requirements.qnt`", generated)

    def test_composite_action_and_clause_are_rejected(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        invalid = copy.deepcopy(catalog)
        invalid["requirements"][0]["action"] = "separate and persist"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)
        invalid = copy.deepcopy(catalog)
        invalid["requirements"][0]["object"] += "; and another obligation"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

    def test_retirement_requires_an_explicit_tombstone(self) -> None:
        catalog = specflow.read_json(ROOT / "spec/requirements/requirements.json")
        invalid = copy.deepcopy(catalog)
        item = next(value for value in invalid["requirements"] if value["id"] == "REQ-REPO-001")
        del item["retirement_reason"]
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

    def test_json_cli_cannot_mutate_the_quint_authority(self) -> None:
        choices = specflow.parser()._subparsers._group_actions[0].choices
        self.assertEqual(set(choices), {"validate", "generate", "check"})
        self.assertNotIn("apply", choices)


if __name__ == "__main__":
    unittest.main()
