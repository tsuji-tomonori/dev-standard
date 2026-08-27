from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReviewContractBoundaryTest(unittest.TestCase):
    def test_legacy_review_harness_is_not_a_portable_guardrail(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        sources = {
            entry["source"]
            for entries in manifest["profiles"].values()
            for entry in entries
        }
        self.assertNotIn("governance/reviews", sources)
        self.assertNotIn("governance/checks", sources)

    def test_pr_template_does_not_require_review_yaml_or_ci(self) -> None:
        template = (ROOT / ".github/PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
        self.assertNotIn("Review YAML", template)
        self.assertNotIn("required check", template)
        self.assertIn("実行したcommand", template)


if __name__ == "__main__":
    unittest.main()
