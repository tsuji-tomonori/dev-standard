from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "governance" / "reviews" / "validate.py"
SPEC = importlib.util.spec_from_file_location("review_contract", MODULE_PATH)
assert SPEC and SPEC.loader
review_contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_contract)


class ReviewContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog, cls.checks = review_contract.load_catalog(ROOT / "governance" / "checks" / "catalog.yaml")
        cls.schema = json.loads(
            (ROOT / "governance" / "reviews" / "review-result.schema.json").read_text(encoding="utf-8")
        )
        cls.current = review_contract.load_yaml(
            ROOT / "governance" / "reviews" / "CHG-20260721-as-built-design.yaml"
        )

    def validate_copy(self, value: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "CHG-20260718-test.yaml"
            path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")
            review_contract.validate_review(ROOT, path, self.schema, self.catalog, self.checks, "HEAD")

    def test_catalog_is_unique_and_contains_all_restructured_checks(self) -> None:
        self.assertEqual(self.catalog["item_count"], 68)
        self.assertEqual(len(self.checks), 68)
        self.assertEqual(self.checks["REV-007"]["class"], "Invariant")
        self.assertEqual(self.checks["AUD-007"]["class"], "Periodic")
        self.assertEqual(self.checks["FAST-016"]["class"], "Risk-selected")
        self.assertEqual(self.checks["FAST-019"]["class"], "Advisory")
        self.assertEqual(self.checks["FAST-022"]["trigger"], "定量閾値変更時")
        self.assertEqual(self.checks["FAST-023"]["class"], "Advisory")
        self.assertEqual(self.checks["AUD-008"]["class"], "Periodic")

    def test_as_built_trigger_flags_select_only_the_declared_controls(self) -> None:
        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["completed_timings"] = ["implementation"]
        value["impact_flags"] = {key: False for key in value["impact_flags"]}
        value["impact_flags"]["as_built_adoption"] = True
        required = review_contract.required_check_ids(value, self.checks)
        self.assertEqual({"FAST-007", "FAST-019", "FAST-020", "FAST-021", "FAST-023"}, required)

        value["impact_flags"]["quality_threshold_change"] = True
        required = review_contract.required_check_ids(value, self.checks)
        self.assertIn("FAST-022", required)
        self.assertNotIn("FAST-016", required)
        self.assertNotIn("FAST-018", required)

        value["impact_flags"] = {key: False for key in value["impact_flags"]}
        value["impact_flags"]["e2e_change"] = True
        required = review_contract.required_check_ids(value, self.checks)
        self.assertEqual({"FAST-007", "FAST-018"}, required)

    def test_current_repository_contract_is_valid(self) -> None:
        review_contract.validate_repository(ROOT, "HEAD")

    def test_only_active_review_is_revalidated(self) -> None:
        active_review = review_contract.validate_commit(ROOT, "HEAD")
        with mock.patch.object(
            review_contract, "validate_review", wraps=review_contract.validate_review
        ) as validate_review:
            review_contract.validate_repository(ROOT, "HEAD")
        validate_review.assert_called_once()
        self.assertEqual(validate_review.call_args.args[1], active_review)

    def test_catalog_digest_and_self_bound_workflow_step_are_validated(self) -> None:
        stale = yaml.safe_load(yaml.safe_dump(self.current))
        stale["catalog_digest"] = "sha256:" + ("0" * 64)
        with self.assertRaisesRegex(review_contract.ContractError, "catalog_digest"):
            self.validate_copy(stale)

        review_contract.validate_evidence(ROOT, "commit:self", "HEAD")
        review_contract.validate_evidence(ROOT, "workflow:Governance#Secret scan", "HEAD")
        with self.assertRaisesRegex(review_contract.ContractError, "workflow step"):
            review_contract.validate_evidence(ROOT, "workflow:Governance#Missing", "HEAD")

    def test_required_check_omission_is_rejected(self) -> None:
        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["selected_checks"] = [item for item in value["selected_checks"] if item["id"] != "IMP-001"]
        with self.assertRaisesRegex(review_contract.ContractError, "missing required checks: IMP-001"):
            self.validate_copy(value)

    def test_fix_commit_requires_bug_fix_flag(self) -> None:
        self.assertEqual(
            review_contract.conventional_commit_type("🛡️ fix(governance): 契約の選択漏れを防ぐ"),
            "fix",
        )
        self.assertEqual(
            review_contract.conventional_commit_type("✨ feat(governance): 契約を追加する"),
            "feat",
        )

        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["impact_flags"]["bug_fix"] = False
        with self.assertRaisesRegex(review_contract.ContractError, "fix commit requires"):
            review_contract.validate_commit_type_flags("fix(governance): 回帰を修正する", value)

    def test_unknown_check_and_class_mismatch_are_rejected(self) -> None:
        unknown = yaml.safe_load(yaml.safe_dump(self.current))
        unknown["selected_checks"][0]["id"] = "REV-999"
        with self.assertRaisesRegex(review_contract.ContractError, "unknown check id"):
            self.validate_copy(unknown)

        mismatch = yaml.safe_load(yaml.safe_dump(self.current))
        mismatch["selected_checks"][0]["class"] = "Advisory"
        with self.assertRaisesRegex(review_contract.ContractError, "class must be"):
            self.validate_copy(mismatch)

    def test_blocking_fail_is_rejected(self) -> None:
        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["selected_checks"][0]["result"] = "fail"
        value["selected_checks"][0]["evidence"] = []
        with self.assertRaisesRegex(review_contract.ContractError, "blocking check"):
            self.validate_copy(value)

    def test_advisory_issue_and_residual_risk_require_linkage(self) -> None:
        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["advisories"] = [
            {"id": "FAST-019", "disposition": "issue", "note": "Issueで追跡"},
            *[item for item in value["advisories"] if item["id"] != "FAST-019"],
        ]
        with self.assertRaisesRegex(review_contract.ContractError, "schema validation failed"):
            self.validate_copy(value)

        value = yaml.safe_load(yaml.safe_dump(self.current))
        value["advisories"] = [
            {
                "id": "FAST-019",
                "disposition": "residual-risk",
                "note": "残存リスクとして受容",
                "risk": "未登録のcoverage risk",
            },
            *[item for item in value["advisories"] if item["id"] != "FAST-019"],
        ]
        with self.assertRaisesRegex(review_contract.ContractError, "absent from residual_risks"):
            self.validate_copy(value)

    def test_pass_and_na_require_direct_evidence_or_note(self) -> None:
        no_evidence = yaml.safe_load(yaml.safe_dump(self.current))
        no_evidence["selected_checks"][0]["evidence"] = []
        with self.assertRaisesRegex(review_contract.ContractError, "schema validation failed"):
            self.validate_copy(no_evidence)

        no_note = yaml.safe_load(yaml.safe_dump(self.current))
        no_note["selected_checks"][0]["result"] = "na"
        no_note["selected_checks"][0]["evidence"] = []
        no_note["selected_checks"][0].pop("note")
        with self.assertRaisesRegex(review_contract.ContractError, "schema validation failed"):
            self.validate_copy(no_note)


if __name__ == "__main__":
    unittest.main()
