from __future__ import annotations

import unittest
from pathlib import Path

from benchmarks.harness.io import BenchmarkError, load_json
from benchmarks.harness.statistics import exact_mcnemar, paired_bootstrap_interval, paired_report, wilson_interval

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = load_json(ROOT / "benchmarks/protocol.json")


def result(task: str, seed: int, condition: str, passed: bool, *, status: str = "completed", run_type: str = "utility") -> dict:
    return {"task_id": task, "seed": seed, "condition": condition, "strict_e2e_pass": passed, "status": status, "run_type": run_type}


class StatisticsProtocolTest(unittest.TestCase):
    def test_duplicate_task_seed_condition_is_rejected(self) -> None:
        values = [result("B01", 0, "full-skills", True), result("B01", 0, "full-skills", False)]
        with self.assertRaises(BenchmarkError):
            paired_report(values, PROTOCOL)

    def test_missing_and_provider_error_arms_are_reported_and_inconclusive(self) -> None:
        values = [
            result("B01", 0, "full-skills", False, status="provider_error"),
            result("B01", 0, "no-skills", False, status="missing"),
            result("B01", 0, "length-matched-control", True),
        ]
        report = paired_report(values, PROTOCOL)
        self.assertTrue(report["primary"]["inconclusive"])
        self.assertEqual(report["primary"]["complete_pairs"], 0)

    def test_precision_does_not_enable_optional_stopping_before_fixed_plan(self) -> None:
        values = []
        for seed in range(10):
            values.extend([result("B01", seed, "full-skills", True), result("B01", seed, "no-skills", False), result("B01", seed, "length-matched-control", False)])
        report = paired_report(values, PROTOCOL)
        self.assertFalse(report["primary"]["fixed_plan_met"])
        self.assertFalse(report["primary"]["optional_stopping"])
        self.assertTrue(report["primary"]["inconclusive"])

    def test_predeclared_fixed_plan_primary_and_length_control_are_reported(self) -> None:
        values = []
        for seed in range(30):
            values.extend([result("B01", seed, "full-skills", seed % 3 != 0), result("B01", seed, "no-skills", seed % 2 == 0), result("B01", seed, "length-matched-control", seed % 5 == 0)])
        report = paired_report(values, PROTOCOL)
        self.assertTrue(report["primary"]["fixed_plan_met"])
        self.assertTrue(report["length_matched_control"]["fixed_plan_met"])
        self.assertEqual(report["claim_boundary"], PROTOCOL["claim_boundary"])

    def test_small_sample_methods_are_bounded(self) -> None:
        low, high = wilson_interval(1, 2)
        self.assertTrue(0 <= low <= high <= 1)
        self.assertTrue(0 <= exact_mcnemar(1, 0) <= 1)
        low, high = paired_bootstrap_interval([1.0, -1.0, 0.0], samples=100)
        self.assertTrue(-1 <= low <= high <= 1)

    def test_smoke_results_are_rejected_for_utility_inference(self) -> None:
        values = [result("B01", 0, "full-skills", True, run_type="smoke")]
        with self.assertRaises(BenchmarkError):
            paired_report(values, PROTOCOL)
