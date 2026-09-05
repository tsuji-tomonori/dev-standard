from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents" / "skills" / "right-size-execution"
PATH = SKILL_ROOT / "scripts" / "executionflow.py"
SPEC = importlib.util.spec_from_file_location("executionflow", PATH)
assert SPEC and SPEC.loader
executionflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executionflow)


class ExecutionflowTest(unittest.TestCase):
    def estimate(
        self,
        request: str,
        *,
        files: int = 1,
        domains: list[str] | None = None,
        artifacts: list[str] | None = None,
        risks: list[str] | None = None,
        paths: list[str] | None = None,
        acceptance: list[str] | None = None,
        gates: list[str] | None = None,
    ) -> dict:
        return executionflow.estimate_profile(
            request,
            expected_files=files,
            domains=domains if domains is not None else ["core"],
            artifact_tags=artifacts if artifacts is not None else ["implementation"],
            risk_tags=risks or [],
            changed_paths=paths if paths is not None else (["src/core/value.py"] if files == 1 else []),
            acceptance_criteria=acceptance if acceptance is not None else ["期待する挙動を満たす"],
            repository_required_gates=gates or [],
        )

    def complete(self, state: dict, **kwargs: object) -> None:
        executionflow.mark_verification(
            state,
            result="pass",
            evidence="selected local verification",
            summary="選択範囲が成功",
            completed_checks=state["estimate"]["required_verification"],
            **kwargs,
        )

    def test_scope_assurance_compute_and_mode_are_independent(self) -> None:
        critical_local = self.estimate("認可ロジックを局所修正", risks=["authorization"])
        broad_mechanical = self.estimate(
            "repository全体の識別子を機械的にrename",
            files=30,
            domains=["api", "web"],
            artifacts=["implementation"],
        )
        self.assertEqual(critical_local["estimate"]["scope"]["value"], "local")
        self.assertEqual(critical_local["estimate"]["assurance"]["value"], "critical")
        self.assertEqual(critical_local["estimate"]["mode"]["value"], "agent-with-review")
        self.assertEqual(broad_mechanical["estimate"]["scope"]["value"], "repository")
        self.assertEqual(broad_mechanical["estimate"]["assurance"]["value"], "standard")
        self.assertEqual(broad_mechanical["estimate"]["compute"]["model_tier"], "economy")
        self.assertEqual(executionflow.validate_profile(critical_local, allow_legacy=False), [])

    def test_assurance_floor_uses_risk_and_artifact_union(self) -> None:
        artifact_only = self.estimate("one local change", artifacts=["database"], risks=[])
        risk_wins = self.estimate("one local change", artifacts=["database"], risks=["authorization"])
        self.assertEqual(artifact_only["estimate"]["assurance"]["value"], "elevated")
        self.assertIn("artifact:database", artifact_only["estimate"]["assurance"]["floor_reasons"])
        self.assertEqual(risk_wins["estimate"]["assurance"]["value"], "critical")
        self.assertIn("risk:authorization", risk_wins["estimate"]["assurance"]["floor_reasons"])
        self.assertEqual(risk_wins["estimate"]["scope"]["value"], "local")

    def test_estimate_and_confidence_are_deterministic(self) -> None:
        first = self.estimate("局所修正")
        second = self.estimate("局所修正")
        self.assertEqual(first["estimate"], second["estimate"])
        confidence = first["estimate"]["confidence"]
        self.assertEqual(confidence["method"], "deterministic-features-v1")
        self.assertIsNone(confidence["score"])
        self.assertTrue(confidence["evidence"])

    def test_empty_features_still_have_deterministic_low_confidence(self) -> None:
        state = executionflow.estimate_profile("曖昧", expected_files=0, domains=[], artifact_tags=[], risk_tags=[])
        self.assertEqual(state["estimate"]["confidence"]["band"], "low")
        self.assertEqual(
            state["estimate"]["confidence"]["evidence"],
            ["no deterministic sizing feature supplied"],
        )

    def test_uncalibrated_score_and_state_tampering_are_diagnosed(self) -> None:
        state = self.estimate("局所修正")
        state["estimate"]["confidence"]["score"] = 0.86
        errors = executionflow.validate_profile(state, allow_legacy=False)
        self.assertIn("uncalibrated confidence score is forbidden", errors)
        self.assertIn("state commitment mismatch", errors)

    def test_profile_contract_rejects_missing_or_extra_fields(self) -> None:
        state = self.estimate("局所修正")
        del state["estimate"]["mode"]
        state["estimate"]["unexpected"] = True
        errors = executionflow.validate_profile(state, allow_legacy=False)
        self.assertTrue(any("estimate fields invalid" in error for error in errors))

    def test_probe_limit_reusable_evidence_and_cost(self) -> None:
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.estimate_profile(
                "曖昧",
                expected_files=0,
                domains=[],
                artifact_tags=[],
                risk_tags=[],
                metadata_probes=[{"evidence": "one"}, {"evidence": "two"}],
            )
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.estimate_profile(
                "曖昧",
                expected_files=0,
                domains=[],
                artifact_tags=[],
                risk_tags=[],
                metadata_probes=[{"evidence": "", "cost": 1}],
            )
        state = executionflow.estimate_profile(
            "曖昧",
            expected_files=0,
            domains=[],
            artifact_tags=[],
            risk_tags=[],
            metadata_probes=[{"evidence": "manifest digest", "cost": 0.25, "reused": True}],
        )
        self.assertEqual(state["actual"]["metadata_probe_cost"], 0.25)
        self.assertNotIn("llm", state["estimate"]["confidence"]["method"])

    def test_verification_projection_is_exact_and_component_evidenced(self) -> None:
        state = self.estimate(
            "公開API dependencyを更新",
            artifacts=["public-api"],
            risks=["dependency"],
            acceptance=["OpenAPI contractが一致する"],
            gates=["target-owned:lint"],
        )
        projection = state["estimate"]["verification_projection"]
        self.assertEqual(state["estimate"]["required_verification"], projection["required"])
        self.assertIn("affected-contract", projection["components"]["artifact"])
        self.assertIn("dependency-resolution-check", projection["components"]["risk"])
        self.assertEqual(projection["components"]["target_owned"], ["target-owned:lint"])
        self.assertEqual(len(projection["components"]["acceptance"]), 1)
        self.assertFalse(any(check.lower() == "ci" for check in projection["required"]))

    def test_incomplete_or_unselected_check_reports_remain_advisory(self) -> None:
        state = self.estimate("局所修正")
        executionflow.mark_verification(
            state,
            result="pass",
            evidence="pytest",
            summary="一部だけ成功",
            completed_checks=state["estimate"]["required_verification"][:-1],
        )
        self.assertEqual(state["status"], "executing")
        self.assertFalse(state["actual"]["success"])
        self.assertTrue(state["observations"][-1]["advisory_findings"])
        executionflow.mark_verification(
            state,
            result="pass",
            evidence="pytest",
            summary="余分な検査も報告",
            completed_checks=[*state["estimate"]["required_verification"], "full-repository-scan"],
        )
        self.assertEqual(state["status"], "success")
        self.assertTrue(state["observations"][-1]["advisory_findings"])

    def test_diagnostics_are_unbounded_but_never_become_blocking_projection(self) -> None:
        state = self.estimate("局所修正")
        required = deepcopy(state["estimate"]["required_verification"])
        for index in range(12):
            executionflow.expand_profile(
                state,
                axis="verification",
                reason_code="verification-failed",
                evidence=f"failure evidence {index}",
                actor="test",
                failure_identity=f"failure-{index}",
            )
        self.assertEqual(state["actual"]["expansion_count"], 12)
        self.assertEqual(state["estimate"]["required_verification"], required)
        self.assertEqual(len(state["estimate"]["diagnostic_checks"]), 12)
        self.complete(state, completed_diagnostics=state["estimate"]["diagnostic_checks"])

    def test_assurance_expansion_changes_one_axis_and_requires_separate_review(self) -> None:
        state = self.estimate("local standard fix")
        original_mode = deepcopy(state["estimate"]["mode"])
        executionflow.expand_profile(
            state,
            axis="assurance",
            reason_code="assurance-floor-insufficient",
            evidence="new impact needs elevated assurance",
            actor="test",
        )
        self.assertEqual(state["estimate"]["mode"], original_mode)
        self.assertEqual(state["estimate"]["assurance"]["value"], "elevated")
        self.complete(state)
        self.assertEqual(state["status"], "executing")
        self.assertTrue(state["observations"][-1]["advisory_findings"])
        executionflow.expand_profile(
            state,
            axis="review",
            reason_code="review-required",
            evidence="elevated assurance needs agent mode",
            actor="test",
        )
        self.complete(state)

    def test_stable_failure_identity_rejects_changed_wording(self) -> None:
        state = self.estimate("module修正", files=2)
        executionflow.expand_profile(
            state,
            axis="verification",
            reason_code="verification-failed",
            evidence="timeout at 12:00",
            actor="test",
            failure_identity="TEST-TIMEOUT-network-boundary",
        )
        with self.assertRaisesRegex(executionflow.ExecutionError, "stable failure identity"):
            executionflow.expand_profile(
                state,
                axis="verification",
                reason_code="verification-failed",
                evidence="timeout at 12:01 with another stack line",
                actor="test",
                failure_identity="TEST-TIMEOUT-network-boundary",
            )

    def test_verification_failure_records_identity_for_followup_expansion(self) -> None:
        state = self.estimate("局所修正")
        executionflow.mark_verification(
            state,
            result="fail",
            evidence="pytest case A",
            summary="境界値で失敗",
            completed_checks=state["estimate"]["required_verification"][:-1],
            failure_identity="CASE-A-boundary",
        )
        identity = state["observations"][-1]["failure_identity"]
        self.assertEqual(identity, executionflow.stable_failure_identity("CASE-A-boundary"))
        executionflow.expand_profile(
            state,
            axis="verification",
            reason_code="verification-failed",
            evidence="pytest case A",
            actor="test",
            failure_identity="CASE-A-boundary",
        )

    def test_expansion_chain_detects_tampering(self) -> None:
        state = self.estimate("module修正", files=2)
        executionflow.expand_profile(
            state,
            axis="scope",
            reason_code="dependency-discovered",
            evidence="別moduleのcall graph edge",
            actor="test",
        )
        executionflow.expand_profile(
            state,
            axis="compute",
            reason_code="compute-insufficient",
            evidence="constraint interaction exceeded current reasoning",
            actor="test",
        )
        self.assertEqual(executionflow.validate_expansion_chain(state["expansions"]), [])
        tampered = deepcopy(state)
        tampered["expansions"][0]["evidence"] = "rewritten"
        executionflow.seal_state(tampered)
        self.assertTrue(any("expansion 1 digest mismatch" in error for error in executionflow.validate_profile(tampered, allow_legacy=False)))

    def test_stop_digest_binds_full_expansion_chain(self) -> None:
        state = self.estimate("局所修正")
        executionflow.expand_profile(
            state,
            axis="verification",
            reason_code="verification-failed",
            evidence="one defect",
            actor="test",
            failure_identity="one-defect",
        )
        self.complete(state)
        self.assertEqual(state["stop"]["expansion_chain_head"], state["expansions"][-1]["expansion_digest"])
        self.assertEqual(executionflow.validate_profile(state, allow_legacy=False), [])
        state["stop"]["reason"] = "rewritten"
        executionflow.seal_state(state)
        self.assertIn("stop digest mismatch", executionflow.validate_profile(state, allow_legacy=False))

    def test_success_stops_expansion_and_audits_positive_cost_activity(self) -> None:
        state = self.estimate("local fix")
        self.complete(state)
        with self.assertRaises(executionflow.ExecutionError):
            executionflow.expand_profile(
                state,
                axis="scope",
                reason_code="dependency-discovered",
                evidence="late",
                actor="test",
            )
        executionflow.record_observation(
            state,
            {"tool_calls": 1, "unique_files_read": ["late.txt"]},
            kind="explore",
            evidence="late read",
        )
        audit = executionflow.audit_profile(state)
        self.assertEqual(state["actual"]["post_success_activity"], 1)
        self.assertTrue(any("after decisive success" in warning for warning in audit["warnings"]))

    def test_shadow_findings_are_diagnostic_and_not_repository_blocking(self) -> None:
        state = self.estimate("認可修正", risks=["authorization"])
        state["estimate"]["assurance"] = {
            "value": "standard",
            "floor_reasons": ["no elevated or critical risk feature"],
        }
        executionflow.refresh_derived(state["estimate"], executionflow.load_policy())
        executionflow.seal_state(state)
        audit = executionflow.audit_profile(state)
        self.assertEqual(audit["enforcement"], "shadow")
        self.assertIs(audit["repository_blocking"], False)
        self.assertEqual(audit["errors"], [])
        self.assertTrue(any("assurance floor violated" in item for item in audit["diagnostics"]))

    def test_efficiency_overruns_remain_advisory(self) -> None:
        state = self.estimate("local fix")
        executionflow.record_observation(
            state,
            {
                "tool_calls": 100,
                "search_calls": 0,
                "read_bytes": 0,
                "read_ranges": 0,
                "duplicate_read_bytes": 0,
                "subagent_calls": 0,
                "wall_clock_seconds": 1,
                "unique_files_read": [],
            },
            kind="execute",
            evidence="optional metrics",
        )
        audit = executionflow.audit_profile(state)
        self.assertEqual(audit["errors"], [])
        self.assertIs(audit["repository_blocking"], False)
        self.assertTrue(audit["warnings"])

    def test_selection_is_self_contained_and_bound_to_current_estimate(self) -> None:
        state = self.estimate("認可修正", risks=["authorization"])
        first = executionflow.build_selection(state)
        second = executionflow.build_selection(state)
        self.assertEqual(first, second)
        self.assertEqual(first["estimate_digest"], executionflow.digest(state["estimate"]))
        self.assertEqual(first["selected_checks"], state["estimate"]["required_verification"])
        self.assertEqual(len(first["manifest_digest"]), 64)

    def test_record_selection_reseals_state_and_manifest_tampering_is_diagnostic(self) -> None:
        state = self.estimate("要件更新", artifacts=["requirements"])
        revision = state["state_revision"]
        selection = executionflow.build_selection(state)
        executionflow.record_selection(state, selection)
        self.assertGreater(state["state_revision"], revision)
        self.assertEqual(executionflow.validate_profile(state, allow_legacy=False), [])
        state["selection"]["selected_checks"] = []
        executionflow.seal_state(state)
        audit = executionflow.audit_profile(state)
        self.assertIn("selection manifest digest mismatch", audit["diagnostics"])

    def test_expansion_invalidates_selection(self) -> None:
        state = self.estimate("module fix", files=2)
        executionflow.record_selection(state, executionflow.build_selection(state))
        executionflow.expand_profile(
            state,
            axis="scope",
            reason_code="dependency-discovered",
            evidence="another module consumes the result",
            actor="test",
        )
        self.assertEqual(state["selection"], {})
        self.assertEqual(executionflow.validate_profile(state, allow_legacy=False), [])

    def test_cli_rejects_absolute_escape_and_symlinked_run_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/safe_io.py", root / "tools/safe_io.py")
            outside = root / "outside"
            outside.mkdir()
            (root / ".devflow").mkdir()
            (root / ".devflow/run").symlink_to(outside, target_is_directory=True)
            arguments = [
                "--root",
                str(root),
                "estimate",
                "--request",
                "fix",
                "--expected-files",
                "1",
                "--acceptance-criterion",
                "works",
                "--out",
                ".devflow/run/profile.json",
            ]
            self.assertEqual(executionflow.main(arguments), 2)
            self.assertFalse((outside / "profile.json").exists())
            arguments[-1] = str(root / "absolute.json")
            self.assertEqual(executionflow.main(arguments), 2)

    def test_normal_estimate_does_not_create_a_ledger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = list(root.iterdir())
            state = self.estimate("局所修正")
            self.assertEqual(before, list(root.iterdir()))
            self.assertEqual(state["observations"], [])
            self.assertEqual(state["actual"]["tool_calls"], 0)

    def test_benchmark_covers_every_behavior_constraint(self) -> None:
        report = executionflow.run_benchmark()
        constraints = json.loads((SKILL_ROOT / "assets" / "behavior-constraints.json").read_text(encoding="utf-8"))
        self.assertTrue(report["passed"])
        self.assertEqual(report["case_count"], 12)
        self.assertFalse(report["repository_catalog_read"])
        self.assertEqual(report["behavior_coverage"], 1.0)
        self.assertEqual(
            set(report["behavior_constraint_evidence"]),
            {item["id"] for item in constraints["constraints"]},
        )
        self.assertTrue(report["paraphrase_assurance_consistent"])
        self.assertFalse(report["deployment_gate_ready"])

    def test_policy_has_no_implicit_ci_merge_or_branch_gate(self) -> None:
        policy = executionflow.load_policy()
        checks = [check for profile in policy["scope_profiles"].values() for check in profile["functional_verification"]]
        self.assertFalse(policy["repository_blocking"])
        self.assertNotIn("ci", {check.lower() for check in checks})
        serialized = json.dumps(policy, ensure_ascii=False).lower()
        self.assertNotIn("merge queue", serialized)
        self.assertNotIn("branch protection", serialized)

    def test_readme_typo_selects_only_direct_artifact_and_acceptance_checks(self) -> None:
        state = self.estimate(
            "READMEの誤字を直す",
            artifacts=["documentation"],
            paths=["README.md"],
            acceptance=["誤字がなくなる"],
        )
        self.assertEqual(
            set(state["estimate"]["verification_projection"]["components"]),
            {"artifact", "risk", "acceptance", "target_owned"},
        )
        self.assertEqual(
            state["estimate"]["required_verification"],
            ["affected-document-check", state["estimate"]["verification_projection"]["components"]["acceptance"][0]],
        )

    def test_cli_round_trip_is_create_only_and_cas_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tools").mkdir()
            shutil.copy2(ROOT / "tools/safe_io.py", root / "tools/safe_io.py")
            path = root / ".devflow/run/execution-profile.json"
            argv = [
                "--root",
                str(root),
                "estimate",
                "--request",
                "README修正",
                "--expected-files",
                "1",
                "--domains",
                "docs",
                "--artifact-tags",
                "documentation",
                "--changed-path",
                "README.md",
                "--acceptance-criterion",
                "文言が直る",
                "--out",
                ".devflow/run/execution-profile.json",
            ]
            self.assertEqual(executionflow.main(argv), 0)
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved["schema_version"], 2)
            self.assertEqual(saved["estimate"]["scope"]["value"], "local")
            self.assertEqual(executionflow.validate_profile(saved, allow_legacy=False), [])
            self.assertEqual(executionflow.main(argv), 2)
            for command in ["select-checks", "finalize"]:
                with self.subTest(command=command):
                    self.assertEqual(
                        executionflow.main(
                            [
                                "--root",
                                str(root),
                                command,
                                "--profile",
                                ".devflow/run/execution-profile.json",
                                "--out",
                                ".devflow/run/execution-profile.json",
                            ]
                        ),
                        2,
                    )
                    self.assertEqual(json.loads(path.read_text(encoding="utf-8")), saved)


if __name__ == "__main__":
    unittest.main()
