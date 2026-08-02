from __future__ import annotations

import copy
import unittest
from pathlib import Path

from benchmarks.harness.fixture import load_answer_variant, load_fixture
from benchmarks.harness.io import load_json
from benchmarks.harness.scoring import default_execution, score_observed

ROOT = Path(__file__).resolve().parents[2]


class ScoringTest(unittest.TestCase):
    def score(self, task_id: str, variant: str = "gold", **kwargs):
        task = load_json(ROOT / f"benchmarks/tasks/{task_id}/task.json")
        oracle = load_json(ROOT / f"benchmarks/oracles/{task_id}/oracle.json")
        state_root, observed = load_fixture(ROOT, task_id, variant)
        return score_observed(ROOT, task, oracle, observed, state_root=state_root, **kwargs)

    def test_gold_base_and_mutation_discriminate_all_eight_tasks(self) -> None:
        for index in range(1, 9):
            task_id = f"B{index:02d}"
            oracle = load_json(ROOT / f"benchmarks/oracles/{task_id}/oracle.json")
            gold = self.score(task_id, "gold")
            base = self.score(task_id, "base")
            mutation = self.score(task_id, "mutation")
            self.assertTrue(gold["strict_e2e_pass"], task_id)
            for gate in oracle["certification"]["base_failed_gates"]:
                self.assertFalse(base["gates"][gate], (task_id, gate))
            for gate in oracle["certification"]["mutation_failed_gates"]:
                self.assertFalse(mutation["gates"][gate], (task_id, gate))

    def test_b02_requires_one_key_question_and_integrates_variant(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B02/task.json")
        oracle = load_json(ROOT / "benchmarks/oracles/B02/oracle.json")
        for variant in ["soft-delete", "hard-delete"]:
            state_root, observed = load_answer_variant(ROOT, "B02", variant)
            result = score_observed(ROOT, task, oracle, observed, state_root=state_root)
            self.assertTrue(result["gates"]["interaction"], variant)
            self.assertTrue(result["gates"]["requirements"], variant)
        state_root, observed = load_fixture(ROOT, "B02", "gold")
        observed["interaction"]["rounds"] = 2
        self.assertFalse(score_observed(ROOT, task, oracle, observed, state_root=state_root)["gates"]["interaction"])

    def test_b03_no_ask_is_blocking(self) -> None:
        self.assertTrue(self.score("B03", "gold")["gates"]["interaction"])
        self.assertFalse(self.score("B03", "base")["gates"]["interaction"])

    def test_llm_judge_cannot_change_a_blocking_decision(self) -> None:
        result = self.score(
            "B01",
            "base",
            llm_judge={"used": True, "advisory_only": True, "model": "judge", "confidence": 1.0, "evidence_spans": ["looks good"]},
        )
        self.assertFalse(result["strict_e2e_pass"])
        self.assertFalse(result["gates"]["implementation"])

    def test_noncompleted_status_can_never_strict_pass(self) -> None:
        for status in ["provider_error", "timeout", "tool_crash", "cancelled", "missing"]:
            result = self.score("B01", "gold", status=status)
            self.assertTrue(all(result["gates"].values()))
            self.assertFalse(result["strict_e2e_pass"], status)

    def test_sandboxed_tool_executor_and_valid_audit_are_blocking(self) -> None:
        execution = default_execution()
        execution["sandbox"]["network_enforced"] = False
        result = self.score("B01", "gold", execution=execution)
        self.assertFalse(result["gates"]["safety_authority"])
        execution = default_execution()
        execution["sandbox"]["tool_audit_valid"] = False
        self.assertFalse(self.score("B01", "gold", execution=execution)["gates"]["safety_authority"])

    def test_strict_pass_is_logical_and_not_weighted_compensation(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B01/task.json")
        oracle = load_json(ROOT / "benchmarks/oracles/B01/oracle.json")
        state_root, observed = load_fixture(ROOT, "B01", "gold")
        observed = copy.deepcopy(observed)
        observed["implementation"]["f2p"]["test_slug_trailing_hyphen"] = False
        result = score_observed(ROOT, task, oracle, observed, state_root=state_root)
        self.assertEqual(sum(result["sub_scores"].values()), 5.0)
        self.assertFalse(result["strict_e2e_pass"])
