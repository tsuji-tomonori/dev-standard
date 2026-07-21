from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
CLASSIFICATION_STANDARD = ROOT / "docs" / "standards" / "REQUIREMENT-CLASSIFICATION.md"


def load_specflow():
    path = SKILLS / "maintain-canonical-requirements" / "scripts" / "specflow.py"
    spec = importlib.util.spec_from_file_location("specflow_reference_contract", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


specflow = load_specflow()


class ReferenceRepositoryContractTest(unittest.TestCase):
    def test_repository_does_not_store_live_work_items(self) -> None:
        self.assertFalse((ROOT / "work").exists())
        for path in [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "docs" / "GOVERNANCE.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("top-level", text)
            self.assertIn("work/", text)

    def test_meta_skill_defines_portability_and_documentation_lenses(self) -> None:
        skill = (SKILLS / "maintain-reference-repository" / "SKILL.md").read_text(encoding="utf-8")
        standard = CLASSIFICATION_STANDARD.read_text(encoding="utf-8")
        for required in [
            "sample / reference collection",
            "product / project",
            "functional / nonfunctional",
            "Documentation as project NFR",
            "top-levelの`work/`",
            "Distribution boundary",
            "Meta review questions",
        ]:
            self.assertIn(required, skill)
        for required in [
            "software product requirements",
            "software project requirements",
            "functional requirements",
            "nonfunctional requirements",
            "Audience",
            "Update trigger",
            "Retirement condition",
            "project / nonfunctional",
        ]:
            self.assertIn(required, standard)

    def test_documentation_example_is_a_valid_project_nfr(self) -> None:
        example_path = (
            SKILLS
            / "maintain-canonical-requirements"
            / "assets"
            / "documentation-project-nfr.example.json"
        )
        example = json.loads(example_path.read_text(encoding="utf-8"))
        specflow.validate_requirement(example, set())
        self.assertEqual(example["scope"], "project")
        self.assertEqual(example["category"], "nonfunctional")
        rendered = specflow.render(
            {
                "schema_version": 1,
                "catalog_revision": 1,
                "product": "example",
                "updated_at": "2026-07-21",
                "requirements": [example],
            }
        )
        self.assertIn("分類: `project` / `nonfunctional`", rendered)

    def test_scope_and_category_are_an_atomic_pair(self) -> None:
        example_path = (
            SKILLS
            / "maintain-canonical-requirements"
            / "assets"
            / "documentation-project-nfr.example.json"
        )
        example = json.loads(example_path.read_text(encoding="utf-8"))
        del example["category"]
        with self.assertRaises(specflow.SpecError):
            specflow.validate_requirement(example, set())

    def test_meta_skill_is_not_in_portable_default_profiles(self) -> None:
        manifest = json.loads((ROOT / "distribution" / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("maintain-reference-repository", manifest["inventory"]["skills"])
        classification_source = "docs/standards/REQUIREMENT-CLASSIFICATION.md"
        for profile in ["default", "chat-first", "development-framework", "frontend-development", "requirements"]:
            sources = {entry["source"] for entry in manifest["profiles"][profile]}
            self.assertNotIn(".agents/skills/maintain-reference-repository", sources, profile)
            self.assertIn(classification_source, sources, profile)
        maintenance_sources = {
            entry["source"]
            for entry in manifest["profiles"]["reference-repository-maintenance"]
        }
        self.assertEqual(
            maintenance_sources,
            {
                ".agents/skills/maintain-reference-repository",
                classification_source,
            },
        )
        for profile, entries in manifest["profiles"].items():
            self.assertNotIn("work", {entry["source"] for entry in entries}, profile)

    def test_root_guidance_routes_reference_repository_changes(self) -> None:
        for path in [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CONTRIBUTING.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("maintain-reference-repository", text)
            self.assertIn("project", text)
            self.assertIn("nonfunctional", text)


if __name__ == "__main__":
    unittest.main()
