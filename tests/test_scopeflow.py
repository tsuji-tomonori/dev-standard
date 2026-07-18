from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".agents" / "skills" / "right-size-execution" / "scripts" / "scopeflow.py"
SPEC = importlib.util.spec_from_file_location("scopeflow", PATH)
assert SPEC and SPEC.loader
scopeflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scopeflow)


class ScopeflowTest(unittest.TestCase):
    def test_local_and_bounded_estimates_use_smallest_level(self) -> None:
        local = scopeflow.estimate_scope("READMEの誤字修正", expected_files=1, domains=["docs"], artifact_tags=["documentation"], risk_tags=[])
        bounded = scopeflow.estimate_scope("moduleとtestを更新", expected_files=4, domains=["module"], artifact_tags=["implementation", "test"], risk_tags=[])
        self.assertEqual(local["estimate"]["scope_level"], 1)
        self.assertEqual(local["estimate"]["model_tier"], "light")
        self.assertEqual(bounded["estimate"]["scope_level"], 2)
        unknown = scopeflow.estimate_scope("不具合を直す", expected_files=0, domains=[], artifact_tags=[], risk_tags=[])
        self.assertEqual(unknown["estimate"]["scope_level"], 2)

    def test_high_risk_floor_is_l3_even_for_one_file(self) -> None:
        state = scopeflow.estimate_scope("認可policyを1 fileで変更", expected_files=1, domains=["security"], artifact_tags=["implementation"], risk_tags=[])
        self.assertEqual(state["estimate"]["scope_level"], 3)
        self.assertEqual(state["estimate"]["risk"], "high")
        self.assertEqual(scopeflow.validate_scope(state), [])

    def test_probe_limit_and_capability_evidence_are_enforced(self) -> None:
        with self.assertRaises(scopeflow.ScopeError):
            scopeflow.estimate_scope("曖昧", expected_files=0, domains=[], artifact_tags=[], risk_tags=[], metadata_probes=2)
        state = scopeflow.estimate_scope("module修正", expected_files=2, domains=["module"], artifact_tags=["implementation"], risk_tags=[])
        with self.assertRaises(scopeflow.ScopeError):
            scopeflow.expand_scope(state, axis="capability", reason_code="estimate-exceeded", evidence="model failed", actor="test")
        scopeflow.expand_scope(state, axis="dependencies", reason_code="dependency-discovered", evidence="call graph hit", actor="test")
        self.assertEqual(state["actual"]["expansion_count"], 1)

    def test_overrun_and_post_success_activity_are_auditable(self) -> None:
        state = scopeflow.estimate_scope("local fix", expected_files=1, domains=["module"], artifact_tags=["implementation"], risk_tags=[])
        scopeflow.record_observation(state, {"tool_calls": 20, "searches": 0, "read_bytes": 0, "read_ranges": 0, "duplicate_read_bytes": 0, "subagents": 0, "wall_clock_seconds": 1, "unique_files": []}, kind="execute", evidence="tool ledger")
        self.assertIn("tool_calls", scopeflow.budget_overruns(state))
        scopeflow.mark_verification(state, result="pass", evidence="pytest", summary="target test passed")
        scopeflow.record_observation(state, {"tool_calls": 1, "searches": 0, "read_bytes": 0, "read_ranges": 0, "duplicate_read_bytes": 0, "subagents": 0, "wall_clock_seconds": 0, "unique_files": []}, kind="extra", evidence="unnecessary")
        audit = scopeflow.audit_scope(state)
        self.assertIn("exploration continued after decisive success", audit["warnings"])
        self.assertIsNone(scopeflow.efficiency_report(state)["acrr"])

    def test_selector_is_reproducible_and_task_specific(self) -> None:
        catalog = json.loads((ROOT / "governance" / "checklist" / "catalog.json").read_text(encoding="utf-8"))
        state = scopeflow.estimate_scope("要件とgeneratorを変更", expected_files=3, domains=["governance"], artifact_tags=["requirements", "generator"], risk_tags=["governance"])
        first = scopeflow.select_catalog_items(catalog, state, profiles=["CORE"], phases=["requirements", "implementation", "verification"])
        second = scopeflow.select_catalog_items(catalog, state, profiles=["CORE"], phases=["requirements", "implementation", "verification"])
        self.assertEqual(first, second)
        self.assertGreater(first["selected_count"], 0)
        self.assertLess(first["selected_count"], catalog["item_count"])
        self.assertEqual(len(first["selection_sha256"]), 64)

    def test_benchmark_and_cli_round_trip(self) -> None:
        report = scopeflow.run_benchmark()
        self.assertTrue(report["passed"])
        self.assertEqual(report["case_count"], 7)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "scope.json"
            result = scopeflow.main(["estimate", "--request", "README修正", "--expected-files", "1", "--domains", "docs", "--artifact-tags", "documentation", "--out", str(path)])
            self.assertEqual(result, 0)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["estimate"]["scope_level"], 1)


if __name__ == "__main__":
    unittest.main()
