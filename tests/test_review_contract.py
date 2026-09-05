from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

import yaml

import tools.validate_repo as validate_repo_module

ROOT = Path(__file__).resolve().parents[1]


class ReviewContractBoundaryTest(unittest.TestCase):
    def test_gate_auditor_uses_activation_context_not_retired_profiles(self) -> None:
        text = (ROOT / ".codex/agents/gate-auditor.toml").read_text(encoding="utf-8")
        for retired in [
            "For direct or assured work",
            "For regulated work",
            "selected execution profile",
        ]:
            self.assertNotIn(retired, text)
        self.assertIn("three pillars applicable to the current change", text)
        self.assertIn("concrete regulated duty activation context", text)
        self.assertIn("extra gate", text)

    def test_current_documentation_uses_concrete_duty_not_retired_profile_trigger(self) -> None:
        for relative in [
            "docs/README.md",
            "docs/standards/REQUIREMENT-CLASSIFICATION.md",
        ]:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertNotIn("regulated profile", text)
                self.assertIn("具体的", text)

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

    def test_current_check_catalog_has_no_default_selection_or_ci_only_evidence(self) -> None:
        catalog = yaml.safe_load((ROOT / "governance/checks/catalog.yaml").read_text(encoding="utf-8"))
        self.assertEqual(catalog["portable_default_selection"], [])
        self.assertEqual(catalog["current_namespaces"], ["IMP", "FAST", "AUD"])
        self.assertEqual(catalog["historical_namespaces"], ["REV", "MRG", "DEP"])
        self.assertEqual(
            {item["id"].split("-", 1)[0] for item in catalog["items"]},
            set(catalog["current_namespaces"]),
        )
        current = [
            item
            for item in catalog["items"]
            if item["id"].split("-", 1)[0] in catalog["current_namespaces"]
        ]
        for item in current:
            evidence = str(item.get("required_evidence", ""))
            self.assertNotEqual(evidence, "GitHub Actions", item["id"])
            self.assertNotEqual(evidence, "CI外部サービス", item["id"])
        report = next(item for item in current if item["id"] == "FAST-023")
        self.assertIn("ローカルsummary", report["acceptance"])
        self.assertIn("新しいCIや外部report基盤を要求せず", report["acceptance"])

    def test_legacy_review_files_are_explicitly_historical(self) -> None:
        text = (ROOT / "governance/reviews/README.md").read_text(encoding="utf-8")
        for required in [
            "過去のレビュー証跡",
            "現行のportable guardrail",
            "新しい変更に`governance/reviews/<change-id>.yaml`を作成しません",
            "installerと`distribution/manifest.json`は、このdirectoryをどの配布collectionにも含めません",
        ]:
            self.assertIn(required, text)

    def test_source_repository_verify_includes_bounded_model_checking(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        verify = next(line for line in makefile.splitlines() if line.startswith("verify:"))
        self.assertIn("quint-verify", verify)
        self.assertNotIn("quint-test", verify)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        adr = (
            ROOT / "docs/decisions/ADR-0004-quint-three-pillar-portability.md"
        ).read_text(encoding="utf-8")
        for text in [readme, adr]:
            self.assertIn("4 step", text)
            self.assertIn("3 step", text)

    def test_repository_validator_invokes_complete_typed_catalog_validator(self) -> None:
        failures: list[str] = []
        with mock.patch.object(
            validate_repo_module,
            "validate_contract_catalog",
            side_effect=ValueError("typed-catalog-sentinel"),
        ) as validator:
            validate_repo_module.validate_skills(failures)
        validator.assert_called_once()
        self.assertTrue(any("typed-catalog-sentinel" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
