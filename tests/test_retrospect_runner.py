from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/retrospect-and-improve/scripts/retrospect.py"


class RetrospectRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "tools").mkdir()
        (self.root / ".devflow/run").mkdir(parents=True)
        shutil.copy2(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def candidate(self, trigger: str = "escaped-defect", evidence: list[str] | None = None) -> dict[str, object]:
        return {
            "schema_version": 2,
            "trigger": trigger,
            "consequence": {
                "kind": "user-impact",
                "description": "A released result prevented completion of the requested task.",
                "materiality": "material",
                "evidence_refs": ["issue:1"] if evidence is None else evidence,
            },
            "target": {"skill": "inspect-quality-gates", "behavior": "select failure-state coverage"},
            "problem": {
                "observed": "One observable failure escaped the selected checks.",
                "root_cause_hypothesis": "The focused test did not exercise the failure state.",
            },
            "alternatives": [
                {
                    "option": "Reuse the closest existing focused test.",
                    "why_insufficient": "It does not execute the observed failure state.",
                }
            ],
            "proposal": {
                "operation": "add-focused-test",
                "change": "Add one bounded failure-state case to the existing focused test.",
                "activation_trigger": "The same observable behavior is changed.",
                "scope": "one-skill-one-behavior",
                "control_effect": "preserve-or-strengthen",
                "authority_effect": "unchanged-or-narrower",
                "affected_controls": ["selected-check-coverage"],
                "authority_delta": {
                    "kind": "none",
                    "before": "target-repository selected commands",
                    "after": "target-repository selected commands",
                },
            },
            "safety_claims": {
                "weakens_checks": False,
                "expands_authority": False,
                "creates_ci_or_merge_policy": False,
                "auto_apply": False,
            },
            "expected": {
                "benefit": "The same observable defect is detected locally.",
                "cost": "One additional focused test case.",
            },
            "evaluation": {
                "metric": "escaped instances of this failure",
                "unit": "count",
                "baseline": 1,
                "target": 0,
                "direction": "zero",
                "evidence_source": "target-owned issue and focused test results",
                "shadow_period_days": 30,
                "max_observations": 20,
            },
            "rollback": {
                "trigger": "The test produces a demonstrated false blocker.",
                "action": "Remove only the new case and retain the incident evidence.",
            },
            "sunset": {"review_at": "2026-12-01", "remove_if": "No related change remains applicable."},
        }

    def run_runner(self, value: dict[str, object], *extra: str) -> subprocess.CompletedProcess[str]:
        (self.root / ".devflow/run/input.json").write_text(json.dumps(value), encoding="utf-8")
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(self.root),
                "--input",
                ".devflow/run/input.json",
                *extra,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_emits_one_bounded_candidate_without_auto_apply(self) -> None:
        result = self.run_runner(self.candidate(), "--json-out", ".devflow/run/candidate.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "candidate")
        self.assertFalse(payload["auto_apply"])
        self.assertEqual(payload["candidate"]["target"]["skill"], "inspect-quality-gates")
        self.assertEqual(json.loads((self.root / ".devflow/run/candidate.json").read_text()), payload)

    def test_normal_close_periodic_audit_and_repeated_ci_repair_do_not_trigger(self) -> None:
        for trigger in ["regulated-close", "periodic-audit", "repeated-ci-repair", "ordinary-session"]:
            with self.subTest(trigger=trigger):
                result = self.run_runner(self.candidate(trigger=trigger))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], "not_triggered")

    def test_recurring_cost_needs_two_distinct_observations(self) -> None:
        result = self.run_runner(self.candidate(trigger="recurring-cost", evidence=["same observation"]))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "not_triggered")

    def test_control_weakening_and_authority_expansion_mutants_are_rejected(self) -> None:
        for mutation in [
            "Disable every check and allow all external writes.",
            "Bypass authorization and expand authority.",
            "Add CI workflow and required check.",
            "Create a merge rule and branch protection.",
        ]:
            with self.subTest(mutation=mutation):
                value = self.candidate()
                value["proposal"]["change"] = mutation  # type: ignore[index]
                self.assertEqual(self.run_runner(value).returncode, 2)

    def test_full_repository_scope_unknown_skill_and_no_rollback_are_rejected(self) -> None:
        mutations = []
        full_scope = self.candidate()
        full_scope["proposal"]["scope"] = "whole-repository"  # type: ignore[index]
        mutations.append(full_scope)
        unknown_skill = self.candidate()
        unknown_skill["target"]["skill"] = "not-a-real-skill"  # type: ignore[index]
        mutations.append(unknown_skill)
        no_rollback = self.candidate()
        no_rollback["rollback"]["action"] = "never"  # type: ignore[index]
        mutations.append(no_rollback)
        for value in mutations:
            self.assertEqual(self.run_runner(value).returncode, 2)

    def test_safety_claim_and_evaluation_cannot_be_self_inconsistent(self) -> None:
        authority = self.candidate()
        authority["safety_claims"]["expands_authority"] = True  # type: ignore[index]
        self.assertEqual(self.run_runner(authority).returncode, 2)
        unmeasurable = self.candidate()
        unmeasurable["evaluation"]["target"] = 2  # type: ignore[index]
        self.assertEqual(self.run_runner(unmeasurable).returncode, 2)
        changed_delta = deepcopy(self.candidate())
        changed_delta["proposal"]["authority_delta"]["after"] = "all external systems"  # type: ignore[index]
        self.assertEqual(self.run_runner(changed_delta).returncode, 2)

    def test_unbounded_extra_field_and_output_escape_are_rejected(self) -> None:
        value = self.candidate()
        value["raw_log"] = "secret output"
        result = self.run_runner(value)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("secret output", result.stderr)
        clean = self.candidate()
        result = self.run_runner(clean, "--json-out", "outside.json")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "outside.json").exists())


if __name__ == "__main__":
    unittest.main()
