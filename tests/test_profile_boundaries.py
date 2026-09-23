from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileBoundaryContractTest(unittest.TestCase):
    def test_no_profile_distributes_repository_policy(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        collections = dict(manifest["profiles"])
        collections["portable_runtime"] = manifest["portable_runtime"]["mappings"]
        collections["formal_skill_contracts"] = manifest["formal_skill_contracts"]["mappings"]
        collections["portable_runner"] = [manifest["portable_runtime"]["runner"]]
        for profile, entries in collections.items():
            for entry in entries:
                combined = f"{entry['source']}\n{entry['destination']}".lower()
                for forbidden in [
                    ".github/",
                    "branch-policy",
                    "governance/reviews",
                    "tools/devflow.py",
                    "required-check",
                    "ruleset",
                ]:
                    self.assertNotIn(forbidden, combined, profile)

    def test_runtime_is_pinned_and_only_attached_to_declared_profiles(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        adapters = json.loads((ROOT / "distribution/host-adapters.json").read_text(encoding="utf-8"))
        runtime = manifest["portable_runtime"]
        self.assertEqual(runtime["quint_version"], "0.32.0")
        self.assertEqual(adapters["portable_runtime"]["quint_version"], "0.32.0")
        self.assertTrue(adapters["portable_runtime"]["host_independent"])
        self.assertEqual(runtime["activation_skill"], "maintain-canonical-requirements")
        self.assertEqual(
            runtime["runner"]["local_imports"],
            "derive-from-_load_pinned_tool-calls",
        )
        destinations = {
            mapping["destination"] for mapping in runtime["mappings"]
        } | {
            runtime["runner"]["destination"],
            "tools/safe_io.py",
            "tools/spec_mapping.py",
            "tools/render_requirements.py",
            "tools/render_skills.py",
        }
        self.assertEqual(
            destinations,
            {
                "tools/quintflow.py",
                "tools/safe_io.py",
                "tools/spec_mapping.py",
                "tools/render_requirements.py",
                "tools/render_skills.py",
                ".dev-standard/quint/source/package.json",
                ".dev-standard/quint/source/package-lock.json",
            },
        )
        self.assertEqual(
            {
                item["destination"]
                for item in manifest["formal_skill_contracts"]["mappings"]
            },
            {"spec/skills/skills.qnt", "spec/skills/skills.json"},
        )
        self.assertNotIn("dependency_runtime", manifest["skill_runner_support"])

    def test_legacy_design_profile_is_a_language_independent_alias(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["profiles"]["aws-cdk-implementation-design"],
            manifest["profiles"]["implementation-design"],
        )
        design_root = ROOT / ".agents/skills/generate-implementation-design"
        self.assertFalse((design_root / "requirements.txt").exists())
        for removed in ["designflow.py", "qualityflow.py"]:
            self.assertFalse((design_root / "scripts" / removed).exists())
        self.assertFalse((ROOT / "tools/portable_python.py").exists())

    def test_manifest_has_explicit_repository_policy_denylist(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        protected = "\n".join(manifest["protected_repository_paths"])
        for value in ["workflows", "PULL_REQUEST_TEMPLATE", "rulesets", "commitlint"]:
            self.assertIn(value, protected)

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
