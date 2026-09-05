from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.validate_repo import frontmatter, validate_repo

ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
    def test_skill_metadata_uses_yaml_semantics(self) -> None:
        cases = [
            ('name: sample\ndescription: "Flow: durable requirements"', "Flow: durable requirements"),
            ("name: sample\ndescription: >-\n  Flow with\n  durable requirements", "Flow with durable requirements"),
            ("name: sample\ndescription: Flow: durable requirements", None),
            ("name: sample\ndescription: 42", None),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with mock.patch("tools.validate_repo.ROOT", root):
                for metadata, expected in cases:
                    with self.subTest(metadata=metadata):
                        path = root / "SKILL.md"
                        path.write_text(f"---\n{metadata}\n---\n# Sample\n", encoding="utf-8")
                        failures: list[str] = []
                        actual = frontmatter(path, failures)
                        if expected is None:
                            self.assertTrue(failures)
                            self.assertEqual(actual, {})
                        else:
                            self.assertEqual(failures, [])
                            self.assertEqual(actual["description"], expected)

    def test_user_documents_and_generated_views_are_current(self) -> None:
        failures: list[str] = []
        validate_repo(failures)
        self.assertEqual([], failures)

    def test_lifecycle_template_labels_are_japanese(self) -> None:
        content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "docs" / "templates").glob("*.md"))
        )
        for phrase in ["Work item:", "Canonical source:", "Base catalog revision:", "Change set:", "rollback"]:
            self.assertNotIn(phrase, content)


if __name__ == "__main__":
    unittest.main()
