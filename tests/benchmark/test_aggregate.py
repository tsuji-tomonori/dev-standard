from __future__ import annotations

import unittest
from pathlib import Path

from benchmarks.harness.io import BenchmarkError, load_json
from benchmarks.harness.statistics import flake_report, paired_report

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = load_json(ROOT / "benchmarks/protocol.json")


def value(seed: int, condition: str, passed: bool, run_type: str = "utility") -> dict:
    return {"task_id": "B01", "seed": seed, "condition": condition, "strict_e2e_pass": passed, "status": "completed", "run_type": run_type}


class AggregateTest(unittest.TestCase):
    def test_completed_utility_results_are_scored_and_paired(self) -> None:
        values = []
        for seed in range(30):
            values.extend([value(seed, "full-skills", True), value(seed, "no-skills", False), value(seed, "length-matched-control", False)])
        report = paired_report(values, PROTOCOL)
        self.assertEqual(report["primary"]["complete_pairs"], 30)
        self.assertEqual(report["primary"]["delta"], 1.0)

    def test_status_mode_rejects_duplicate_arm(self) -> None:
        values = [value(0, "full-skills", True, "flake"), value(0, "full-skills", True, "flake")]
        with self.assertRaises(BenchmarkError):
            flake_report(values)

    def test_status_mode_reports_flake_health_without_utility_inference(self) -> None:
        values = [value(0, "full-skills", True, "flake"), value(0, "no-skills", False, "flake")]
        report = flake_report(values)
        self.assertFalse(report["utility_inference"])
        self.assertEqual(report["failure_rate"], 0.0)
