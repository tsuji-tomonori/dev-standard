from __future__ import annotations

import copy
import unittest
from pathlib import Path

from benchmarks.harness.certify import certify_task
from benchmarks.harness.designfacts import derive_fastapi_sql_facts
from benchmarks.harness.fixture import load_answer_variant, load_fixture
from benchmarks.harness.io import load_json
from benchmarks.harness.scoring import score_observed

ROOT = Path(__file__).resolve().parents[2]


class PhysicalFixtureStateTest(unittest.TestCase):
    def test_b01_base_gold_and_mutation(self) -> None:
        result = certify_task(ROOT, "B01")
        self.assertEqual(result["base_failed_gates"], ["implementation"])
        self.assertEqual(result["mutation_failed_gates"], ["implementation"])

    def test_b02_both_user_variants_have_distinct_valid_outcomes(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B02/task.json")
        oracle = load_json(ROOT / "benchmarks/oracles/B02/oracle.json")
        outcomes = set()
        for variant in ["soft-delete", "hard-delete"]:
            state_root, observed = load_answer_variant(ROOT, "B02", variant)
            result = score_observed(ROOT, task, oracle, observed, state_root=state_root)
            self.assertTrue(result["strict_e2e_pass"])
            outcomes.add(observed["interaction"]["integrated_outcome"])
        self.assertEqual(len(outcomes), 2)

    def test_b03_to_b08_each_have_a_discriminating_physical_state(self) -> None:
        for index in range(3, 9):
            result = certify_task(ROOT, f"B{index:02d}")
            self.assertTrue(result["physical_fixture_discrimination"])
            self.assertTrue(result["base_failed_gates"])
            self.assertTrue(result["mutation_failed_gates"])

    def test_fixture_python_is_parsed_without_executing_agent_code(self) -> None:
        state_root, _ = load_fixture(ROOT, "B06", "gold")
        dangerous = state_root / "dangerous_fixture.py"
        self.assertIn("raise RuntimeError", dangerous.read_text(encoding="utf-8"))
        result = derive_fastapi_sql_facts(state_root)
        self.assertEqual(result["adapter"], "fastapi-sql")

    def test_governance_evidence_cannot_escape_fixture_and_malformed_checks_fail_closed(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B08/task.json")
        oracle = load_json(ROOT / "benchmarks/oracles/B08/oracle.json")
        state_root, observed = load_fixture(ROOT, "B08", "mutation")
        self.assertFalse(score_observed(ROOT, task, oracle, observed, state_root=state_root)["gates"]["governance"])
        state_root, observed = load_fixture(ROOT, "B08", "gold")
        malformed = copy.deepcopy(observed)
        malformed["governance"]["selected_checks"] = "FAST-006"
        self.assertFalse(score_observed(ROOT, task, oracle, malformed, state_root=state_root)["gates"]["governance"])
