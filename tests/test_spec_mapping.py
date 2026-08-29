from __future__ import annotations

import unittest
from pathlib import Path

from tools.quintflow import extract_state
from tools.spec_mapping import (
    MappingError,
    assert_bijective_catalog,
    catalog_from_json,
    catalog_to_json,
)

ROOT = Path(__file__).resolve().parents[1]


def raw_requirement(rid: str, *, empty_lifecycle_fields: bool) -> dict[str, object]:
    return {
        "id": rid,
        "revision": 7,
        "status": "active" if empty_lifecycle_fields else "retired",
        "kind": "functional",
        "title": f"title-{rid}",
        "subject": f"subject-{rid}",
        "actionName": "generate",
        "objectName": f"object-{rid}",
        "rationale": f"rationale-{rid}",
        "sourceRefs": [f"source-b-{rid}", f"source-a-{rid}"],
        "acceptanceCriteria": [
            {
                "id": f"AC-{rid}-2",
                "given": "given-2",
                "when_": "when-2",
                "expected": "then-2",
            },
            {
                "id": f"AC-{rid}-1",
                "given": "given-1",
                "when_": "when-1",
                "expected": "then-1",
            },
        ],
        "verification": {"method": f"method-{rid}", "evidence": f"evidence-{rid}"},
        "traces": {
            "design": [f"design-b-{rid}", f"design-a-{rid}"],
            "implementation": [f"implementation-b-{rid}", f"implementation-a-{rid}"],
            "tests": [f"tests-b-{rid}", f"tests-a-{rid}"],
            "standards": [f"standard-b-{rid}", f"standard-a-{rid}"],
        },
        "lastChangedBy": f"change-{rid}",
        "retirementReason": "" if empty_lifecycle_fields else f"retired-{rid}",
        "supersededBy": "",
        "scopeName": "" if empty_lifecycle_fields else "project",
        "categoryName": "" if empty_lifecycle_fields else "nonfunctional",
    }


class SpecMappingTest(unittest.TestCase):
    def test_real_quint_fixture_matches_the_full_field_oracle(self) -> None:
        raw = extract_state(ROOT / "tests/fixtures/requirements_mapping.qnt", "catalog")
        self.assertEqual(
            {
                "schemaVersion": 1,
                "catalogRevision": 9,
                "product": "mapping-fixture",
                "updatedAt": "2026-08-29",
                "requirements": [
                    raw_requirement("REQ-Z-001", empty_lifecycle_fields=True),
                    raw_requirement("REQ-A-001", empty_lifecycle_fields=False),
                ],
            },
            raw,
        )
        self.assertEqual(raw, catalog_from_json(catalog_to_json(raw)))

    def test_all_fields_empty_values_and_every_list_order_round_trip(self) -> None:
        raw = {
            "schemaVersion": 1,
            "catalogRevision": 9,
            "product": "mapping-fixture",
            "updatedAt": "2026-08-29",
            "requirements": [
                raw_requirement("REQ-Z-001", empty_lifecycle_fields=True),
                raw_requirement("REQ-A-001", empty_lifecycle_fields=False),
            ],
        }
        mapped = assert_bijective_catalog(raw)
        self.assertEqual(["REQ-Z-001", "REQ-A-001"], [item["id"] for item in mapped["requirements"]])
        self.assertEqual("", mapped["requirements"][0]["retirement_reason"])
        self.assertEqual("", mapped["requirements"][0]["scope"])
        self.assertEqual(
            ["source-b-REQ-Z-001", "source-a-REQ-Z-001"],
            mapped["requirements"][0]["source_refs"],
        )
        self.assertEqual(raw, catalog_from_json(catalog_to_json(raw)))

    def test_unknown_or_missing_field_breaks_exact_mapping(self) -> None:
        raw = {
            "schemaVersion": 1,
            "catalogRevision": 1,
            "product": "mapping-fixture",
            "updatedAt": "2026-08-29",
            "requirements": [raw_requirement("REQ-A-001", empty_lifecycle_fields=True)],
            "unknown": True,
        }
        with self.assertRaises(MappingError):
            catalog_to_json(raw)


if __name__ == "__main__":
    unittest.main()
