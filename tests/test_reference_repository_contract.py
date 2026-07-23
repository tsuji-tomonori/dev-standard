from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
CLASSIFICATION_STANDARD = ROOT / "docs" / "standards" / "REQUIREMENT-CLASSIFICATION.md"
DEVELOPMENT_REFERENCE = ROOT / "docs" / "reference" / "development.md"


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
        for path in [ROOT / "AGENTS.md", DEVELOPMENT_REFERENCE]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("work", text)
            self.assertIn(".devflow/run/", text)

    def test_markdown_is_grouped_by_audience(self) -> None:
        self.assertEqual(
            {"README.md", "AGENTS.md"},
            {path.name for path in ROOT.glob("*.md")},
        )
        self.assertEqual(
            {"README.md"},
            {path.name for path in (ROOT / "docs").glob("*.md")},
        )
        for path in [
            ROOT / ".github" / "CONTRIBUTING.md",
            ROOT / ".github" / "SECURITY.md",
            ROOT / "docs" / "guides" / "getting-started.md",
            DEVELOPMENT_REFERENCE,
            ROOT / "docs" / "reference" / "commit-message.md",
        ]:
            self.assertTrue(path.is_file(), path)

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

    def test_readme_states_three_pillars(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for required in [
            "## このリポジトリが担保する3本柱",
            "### 1. 対話から原子的な永続要件を維持する",
            "### 2. 実装と1対1のas-built設計を生成する",
            "### 3. 必要なチェックだけを、適切な時点で行う",
        ]:
            self.assertIn(required, readme)

    def test_user_guidance_routes_to_current_documents(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        contributing = (ROOT / ".github" / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("docs/guides/getting-started.md", readme)
        self.assertIn("docs/reference/development.md", readme)
        self.assertIn("$maintain-reference-repository", agents)
        self.assertIn("maintain-reference-repository", contributing)


if __name__ == "__main__":
    unittest.main()
