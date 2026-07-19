from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

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
            ROOT / "governance" / "reviews" / "CHG-20260718-artifact-governance.yaml"
        )

    def validate_copy(self, value: dict[str, object]) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "CHG-20260718-test.yaml"
            path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")
            review_contract.validate_review(ROOT, path, self.schema, self.catalog, self.checks)

    def test_catalog_is_unique_and_contains_all_restructured_checks(self) -> None:
        self.assertEqual(self.catalog["item_count"], 59)
        self.assertEqual(len(self.checks), 59)
        self.assertEqual(self.checks["REV-007"]["class"], "Invariant")
        self.assertEqual(self.checks["AUD-007"]["class"], "Periodic")

    def test_current_repository_contract_is_valid(self) -> None:
        review_contract.validate_repository(ROOT, "HEAD")

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
        value["selected_checks"].append(
            {"id": "REV-015", "class": "Advisory", "result": "fail", "evidence": [], "note": "ADR判断を持越す"}
        )
        value["advisories"] = [{"id": "REV-015", "disposition": "issue", "note": "Issueで追跡"}]
        with self.assertRaisesRegex(review_contract.ContractError, "schema validation failed"):
            self.validate_copy(value)

        value["advisories"] = [
            {
                "id": "REV-015",
                "disposition": "residual-risk",
                "note": "残存リスクとして受容",
                "risk": "ADR判断が未完了",
            }
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
