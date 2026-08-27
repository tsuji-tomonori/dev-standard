from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileBoundaryContractTest(unittest.TestCase):
    def test_no_profile_distributes_repository_policy(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        for profile, entries in manifest["profiles"].items():
            for entry in entries:
                combined = f"{entry['source']}\n{entry['destination']}".lower()
                for forbidden in [".github/", "branch-policy", "governance/reviews", "tools/devflow.py"]:
                    self.assertNotIn(forbidden, combined, profile)

    def test_default_and_chat_first_have_four_skill_sources(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        expected = {
            ".agents/skills/chat-first-development",
            ".agents/skills/maintain-canonical-requirements",
            ".agents/skills/generate-implementation-design",
            ".agents/skills/inspect-quality-gates",
        }
        for profile in ["default", "chat-first"]:
            self.assertEqual({item["source"] for item in manifest["profiles"][profile]}, expected)

    def test_user_surfaces_state_the_host_owned_policy_boundary(self) -> None:
        paths = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "docs/reference/development.md",
            ROOT / "distribution/snippets/AGENTS.governance.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for required in ["3本", "requirements.qnt", "CI", "merge"]:
            self.assertIn(required, combined)
        self.assertIn("追加も変更もしません", combined)

    def test_branch_trial_is_historical_and_enforcer_is_removed(self) -> None:
        adr = (ROOT / "docs/decisions/ADR-0002-two-layer-branch-history.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Superseded by ADR-0004", adr)
        self.assertIn("現行policyではない", adr)
        for removed in [".github/branch-policy.json", "tools/branch_policy.py", "tests/test_branch_policy.py"]:
            self.assertFalse((ROOT / removed).exists())


if __name__ == "__main__":
    unittest.main()
