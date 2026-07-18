from __future__ import annotations

import unittest
from pathlib import Path

from tools.validate_repo import validate_repo

ROOT = Path(__file__).resolve().parents[1]


class RepositoryValidationTests(unittest.TestCase):
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
