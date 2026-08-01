from __future__ import annotations

import unittest
from pathlib import Path

from benchmarks.harness.io import BenchmarkError
from benchmarks.harness.simulator import UserSimulator

ROOT = Path(__file__).resolve().parents[2]


class UserSimulatorTest(unittest.TestCase):
    def test_both_answer_variants_are_controller_only_and_distinct(self) -> None:
        simulator = UserSimulator(ROOT)
        soft = simulator.answer("B02", "soft-delete", ["削除方式と復元可能性"])
        hard = simulator.answer("B02", "hard-delete", ["削除方式と復元可能性"])
        self.assertNotEqual(soft.answer, hard.answer)
        self.assertNotEqual(soft.expected_outcome, hard.expected_outcome)

    def test_forbidden_reversible_question_is_rejected(self) -> None:
        with self.assertRaises(BenchmarkError):
            UserSimulator(ROOT).answer("B02", "soft-delete", ["削除方式と復元可能性", "ボタンの色"])
