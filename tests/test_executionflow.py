from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".agents" / "skills" / "right-size-execution" / "scripts" / "executionflow.py"
SPEC = importlib.util.spec_from_file_location("executionflow", PATH)
assert SPEC and SPEC.loader
executionflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executionflow)


class ExecutionflowTest(unittest.TestCase):
    def estimate(self, request: str, *, files: int = 1, domains: list[str] | None = None, artifacts: list[str] | None = None, risks: list[str] | None = None) -> dict:
        return executionflow.estimate_profile(
            request,
            expected_files=files,
            domains=domains or ["core"],
            artifact_tags=artifacts or ["implementation"],
            risk_tags=risks or [],
            changed_paths=["src/core/value.py"] if files == 1 else [],
            acceptance_criteria=["期待する挙動を満たす"],
        )

    def test_scope_assurance_compute_and_mode_are_independent(self) -> None:
        critical_local = self.estimate("認可ロジックを局所修正", risks=["authorization"])
        broad_mechanical = self.estimate(
            "repository全体の識別子を機械的にrename", files=30,
            domains=["api", "web"], artifacts=["implementation"],
        )
        self.assertEqual(critical_local["estimate"]["scope"]["value"], "local")
        self.assertEqual(critical_local["estimate"]["assurance"]["value"], "critical")
        self.assertEqual(critical_local["estimate"]["mode"]["value"], "agent-with-review")
        self.assertEqual(broad_mechanical["estimate"]["scope"]["value"], "repository")
        self.assertEqual(broad_mechanical["estimate"]["assurance"]["value"], "standard")
        self.assertEqual(broad_mechanical["estimate"]["compute"]["model_tier"], "economy")
        self.assertEqual(executionflow.validate_profile(critical_local, allow_legacy=False), [])

    def test_confidence_is_feature_evidence_not_self_report(self) -> None:
        state = self.estimate("局所修正")
        confidence = state["estimate"]["confidence"]
        self.assertEqual(confidence["method"], "deterministic-features-v1")
        self.assertIsNone(confidence["score"])
        self.assertTrue(confidence["evidence"])
        state["estimate"]["confidence"]["score"] = 0.86
        self.assertIn("uncalibrated confidence score is forbidden", executionflow.validate_profile(state, allow_legacy=False))

    def test_profile_contract_rejects_missing_or_extra_fields(self) -> None:
        state = self.estimate("局所修正")
        del state["estimate"]["mode"]
        state["estimate"]["unexpected"] = True
        errors = executionflow.validate_profile(state, allow_legacy=False)
        self.assertTrue(any("estimate fields invalid" in error for error in errors))

    def test_probe_limit_and_no_dedicated_llm_estimate_contract(self) -> None:
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.estimate_profile(
                "曖昧", expected_files=0, domains=[], artifact_tags=[], risk_tags=[],
                metadata_probes=[{"evidence": "one"}, {"evidence": "two"}],
            )
        state = executionflow.estimate_profile("曖昧", expected_files=0, domains=[], artifact_tags=[], risk_tags=[])
        self.assertEqual(state["estimate"]["metadata_probes"], [])
        self.assertNotIn("llm", state["estimate"]["confidence"]["method"])

    def test_expand_has_no_global_count_cap_and_rejects_stagnation(self) -> None:
        state = self.estimate("module修正", files=2)
        executionflow.expand_profile(state, axis="verification", reason_code="verification-failed", evidence="failure-A", actor="test")
        executionflow.expand_profile(state, axis="review", reason_code="review-required", evidence="failure-B", actor="test")
        executionflow.expand_profile(state, axis="compute", reason_code="compute-insufficient", evidence="failure-C", actor="test")
        self.assertEqual(state["actual"]["expansion_count"], 3)
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.expand_profile(state, axis="compute", reason_code="compute-insufficient", evidence="failure-C", actor="test")

    def test_decisive_success_requires_all_derived_checks_and_stops(self) -> None:
        state = self.estimate("認可修正", risks=["authorization"])
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.mark_verification(state, result="pass", evidence="pytest", summary="一部だけ成功", completed_checks=["targeted-test"])
        checks = state["estimate"]["required_verification"]
        executionflow.mark_verification(state, result="pass", evidence="full gate", summary="全検証成功", completed_checks=checks)
        self.assertEqual(state["status"], "success")
        self.assertIsNotNone(state["stop"])
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.expand_profile(state, axis="scope", reason_code="dependency-discovered", evidence="late", actor="test")

    def test_shadow_mode_keeps_efficiency_findings_advisory(self) -> None:
        state = self.estimate("local fix")
        executionflow.record_observation(
            state,
            {"tool_calls": 100, "search_calls": 0, "read_bytes": 0, "read_ranges": 0, "duplicate_read_bytes": 0, "subagent_calls": 0, "wall_clock_seconds": 1, "unique_files_read": []},
            kind="execute", evidence="ledger",
        )
        audit = executionflow.audit_profile(state)
        self.assertEqual(audit["enforcement"], "shadow")
        self.assertEqual(audit["errors"], [])
        self.assertTrue(audit["warnings"])

    def test_selector_records_exclusions_and_zero_curated_misses(self) -> None:
        catalog = json.loads((ROOT / "governance" / "checklist" / "catalog.json").read_text(encoding="utf-8"))
        state = self.estimate("認可修正", risks=["authorization"])
        first = executionflow.select_catalog_items(
            catalog, state, profiles=["CORE"], phases=[], mandatory_ids=["DES-021", "CON-044", "SEC-106"],
        )
        second = executionflow.select_catalog_items(
            catalog, state, profiles=["CORE"], phases=[], mandatory_ids=["DES-021", "CON-044", "SEC-106"],
        )
        self.assertEqual(first, second)
        self.assertEqual(first["mandatory_missed_ids"], [])
        self.assertGreater(first["excluded_count"], 0)
        self.assertTrue(first["audit_sample_ids"])
        self.assertEqual(len(first["manifest_digest"]), 64)

    def test_benchmark_and_cli_round_trip(self) -> None:
        report = executionflow.run_benchmark()
        self.assertTrue(report["passed"])
        self.assertEqual(report["case_count"], 12)
        self.assertEqual(report["selector_false_negative_count"], 0)
        self.assertEqual(report["behavior_coverage"], 1.0)
        self.assertTrue(report["paraphrase_assurance_consistent"])
        self.assertFalse(report["deployment_gate_ready"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "execution-profile.json"
            result = executionflow.main([
                "estimate", "--request", "README修正", "--expected-files", "1",
                "--domains", "docs", "--artifact-tags", "documentation",
                "--changed-path", "README.md", "--acceptance-criterion", "文言が直る", "--out", str(path),
            ])
            self.assertEqual(result, 0)
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved["schema_version"], 2)
            self.assertEqual(saved["estimate"]["scope"]["value"], "local")


if __name__ == "__main__":
    unittest.main()
