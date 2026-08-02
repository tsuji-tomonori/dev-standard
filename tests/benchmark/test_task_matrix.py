from __future__ import annotations

import unittest
from pathlib import Path

from benchmarks.harness.io import load_json

ROOT = Path(__file__).resolve().parents[2]


class TaskMatrixTest(unittest.TestCase):
    def test_b04_updates_existing_id_instead_of_duplicate_add(self) -> None:
        oracle = load_json(ROOT / "benchmarks/oracles/B04/oracle.json")
        self.assertEqual(oracle["requirements"]["operation"], "update")
        self.assertEqual(oracle["requirements"]["target_ids"], ["REQ-SHIPPING-001"])
        self.assertIn("duplicate-add", oracle["requirements"]["forbidden_operations"])
        self.assertEqual(oracle["requirements"]["semantic_slots"]["threshold"]["value"], 6000)

    def test_b05_is_project_nonfunctional_and_path_is_trace_not_obligation(self) -> None:
        oracle = load_json(ROOT / "benchmarks/oracles/B05/oracle.json")
        self.assertEqual(oracle["requirements"]["classification"], {"scope": "project", "category": "nonfunctional"})
        self.assertEqual(oracle["requirements"]["semantic_slots"]["object"]["value"], "migration guide")
        self.assertEqual(oracle["requirements"]["trace_paths"], ["docs/guides/migration.md"])
        self.assertIn("path-is-trace-not-obligation", oracle["requirements"]["quality_flags"])

    def test_b06_and_b07_require_source_facts_digest_determinism_and_drift(self) -> None:
        for task_id in ["B06", "B07"]:
            design = load_json(ROOT / f"benchmarks/oracles/{task_id}/oracle.json")["design"]
            self.assertTrue(design["source_digest_required"])
            self.assertTrue(design["byte_determinism"])
            self.assertTrue(design["required_facts"])
            self.assertTrue(design["drift_mutations"])

    def test_b08_uses_required_forbidden_and_admissible_check_sets(self) -> None:
        governance = load_json(ROOT / "benchmarks/oracles/B08/oracle.json")["governance"]
        self.assertTrue(governance["required_checks"])
        self.assertTrue(governance["forbidden_checks"])
        self.assertTrue(governance["admissible_checks"])
        self.assertTrue(set(governance["required_checks"]).isdisjoint(governance["forbidden_checks"]))
