from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/inspect-quality-gates/scripts/inspect.py"


class InspectRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "tools").mkdir()
        (self.root / ".devflow/run").mkdir(parents=True)
        shutil.copy2(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_registry(self, checks: list[dict[str, object]]) -> None:
        (self.root / ".devflow/run/registry.json").write_text(json.dumps({"schema_version": 1, "checks": checks}), encoding="utf-8")

    def registry_check(
        self,
        command_id: str,
        command: list[str],
        *,
        effect: str = "read-only",
        acceptance_ids: list[str] | None = None,
        risk_tags: list[str] | None = None,
        authority_reference: str | None = None,
        output_roots: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "command_id": command_id,
            "command": command,
            "acceptance_ids": acceptance_ids if acceptance_ids is not None else ["AC-1"],
            "risk_tags": risk_tags if risk_tags is not None else [],
            "effect": effect,
            "authority": "target-repository",
            "authority_reference": authority_reference,
            "output_roots": output_roots or [],
        }

    def write_plan(self, checks: list[dict[str, object]], *, residual: list[str] | None = None) -> None:
        (self.root / ".devflow/run/plan.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "scope": "one changed module",
                    "residual_risks": residual or [],
                    "no_applicable_reason": None if checks else "No target-owned command applies to this metadata-only change.",
                    "checks": checks,
                }
            ),
            encoding="utf-8",
        )

    def plan_check(
        self,
        command_id: str,
        *,
        acceptance_ids: list[str] | None = None,
        risk_tags: list[str] | None = None,
        timeout: int | None = None,
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "command_id": command_id,
            "acceptance_ids": acceptance_ids if acceptance_ids is not None else ["AC-1"],
            "risk_tags": risk_tags if risk_tags is not None else [],
        }
        if timeout is not None:
            value["timeout_seconds"] = timeout
        return value

    def run_runner(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--root",
                str(self.root),
                "--registry",
                ".devflow/run/registry.json",
                "--plan",
                ".devflow/run/plan.json",
                *extra,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_runs_registered_command_and_persists_no_raw_output(self) -> None:
        self.write_registry([self.registry_check("focused", [sys.executable, "-c", "print('secret raw output')"])])
        self.write_plan([self.plan_check("focused")], residual=["RISK-known"])
        result = self.run_runner("--json-out", ".devflow/run/result.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["covered_acceptance"], ["AC-1"])
        self.assertEqual(payload["residual_risk"], ["RISK-known", "process-effect-not-isolated:focused"])
        self.assertFalse(payload["raw_output_persisted"])
        self.assertFalse(payload["process_effect_isolation_provided"])
        self.assertFalse(payload["process_effect_detection_provided"])
        self.assertNotIn("secret raw output", result.stdout)
        self.assertNotIn("stdout", payload["results"][0])
        self.assertNotIn("undeclared_effect_detected", payload["results"][0])
        self.assertFalse(payload["results"][0]["process_effect_isolated"])
        self.assertEqual(payload["results"][0]["process_effect_detection"], "not-provided")
        self.assertTrue(payload["results"][0]["executable"]["fd_pinned"])
        self.assertTrue(payload["results"][0]["executable_identity_stable"])
        self.assertEqual(json.loads((self.root / ".devflow/run/result.json").read_text()), payload)

    def test_plan_cannot_supply_arbitrary_argv(self) -> None:
        self.write_registry([self.registry_check("focused", [sys.executable, "-c", "pass"])])
        item = self.plan_check("focused")
        item["command"] = [sys.executable, "-c", "Path('escaped').touch()"]
        self.write_plan([item])
        result = self.run_runner()
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "escaped").exists())

    def test_external_effect_needs_authority_and_reports_residual_risk(self) -> None:
        external = self.registry_check("publish", [sys.executable, "-c", "pass"], effect="external")
        self.write_registry([external])
        self.write_plan([self.plan_check("publish")])
        self.assertEqual(self.run_runner().returncode, 2)
        authorized = self.registry_check(
            "publish",
            [sys.executable, "-c", "pass"],
            effect="target-declared-external",
            authority_reference="target-change-record:42",
        )
        self.write_registry([authorized])
        result = self.run_runner()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("process-effect-not-isolated:publish", json.loads(result.stdout)["residual_risk"])

    def test_all_declared_effect_classes_report_unisolated_process_effects(self) -> None:
        checks = [
            self.registry_check("read", [sys.executable, "-c", "pass"]),
            self.registry_check(
                "build",
                [sys.executable, "-c", "pass"],
                effect="repository-build-artifacts",
                output_roots=["build"],
                acceptance_ids=["AC-2"],
            ),
            self.registry_check(
                "external",
                [sys.executable, "-c", "pass"],
                effect="target-declared-external",
                authority_reference="target-change-record:42",
                acceptance_ids=["AC-3"],
            ),
        ]
        self.write_registry(checks)
        self.write_plan(
            [
                self.plan_check("read"),
                self.plan_check("build", acceptance_ids=["AC-2"]),
                self.plan_check("external", acceptance_ids=["AC-3"]),
            ]
        )
        result = self.run_runner()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["residual_risk"],
            [
                "process-effect-not-isolated:build",
                "process-effect-not-isolated:external",
                "process-effect-not-isolated:read",
            ],
        )

    def test_empty_relevance_is_rejected(self) -> None:
        self.write_registry([self.registry_check("focused", [sys.executable, "-c", "pass"], acceptance_ids=[], risk_tags=[])])
        self.write_plan([self.plan_check("focused", acceptance_ids=[], risk_tags=[])])
        self.assertEqual(self.run_runner().returncode, 2)

    def test_source_mutation_is_a_declaration_violation(self) -> None:
        command = [sys.executable, "-c", "from pathlib import Path; Path('source.py').write_text('changed')"]
        self.write_registry([self.registry_check("mutates", command)])
        self.write_plan([self.plan_check("mutates")])
        result = self.run_runner()
        self.assertEqual(result.returncode, 1, result.stderr)
        observed = json.loads(result.stdout)["results"][0]
        self.assertEqual(observed["status"], "declaration-violation")
        self.assertTrue(observed["source_mutation_detected"])

    def test_registry_and_plan_mutation_during_execution_are_rejected(self) -> None:
        for target in ["registry.json", "plan.json"]:
            with self.subTest(target=target):
                command = [
                    sys.executable,
                    "-c",
                    f"from pathlib import Path; Path('.devflow/run/{target}').write_text('{{}}')",
                ]
                self.write_registry([self.registry_check("mutates-input", command)])
                self.write_plan([self.plan_check("mutates-input")])
                result = self.run_runner("--json-out", ".devflow/run/result.json")
                self.assertEqual(result.returncode, 2)
                self.assertIn("registry or plan changed after selection", result.stderr)
                self.assertFalse((self.root / ".devflow/run/result.json").exists())

    def test_missing_primary_executable_is_bounded_without_false_identity_drift(self) -> None:
        self.write_registry([self.registry_check("missing", ["dev-standard-command-does-not-exist"])])
        self.write_plan([self.plan_check("missing")])
        result = self.run_runner()
        self.assertEqual(result.returncode, 1, result.stderr)
        observed = json.loads(result.stdout)["results"][0]
        self.assertEqual(observed["status"], "cannot-start")
        self.assertIsNone(observed["executable_identity_stable"])

    def test_timeout_kills_the_whole_process_group(self) -> None:
        child = (
            "import subprocess,sys,time; "
            "subprocess.Popen([sys.executable,'-c',\"import time; from pathlib import Path; "
            "time.sleep(2); Path('.devflow/run/escaped').touch()\"]); time.sleep(30)"
        )
        self.write_registry(
            [
                self.registry_check(
                    "timeout",
                    [sys.executable, "-c", child],
                    effect="repository-build-artifacts",
                    output_roots=["build"],
                )
            ]
        )
        self.write_plan([self.plan_check("timeout", timeout=1)])
        result = self.run_runner()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(json.loads(result.stdout)["results"][0]["status"], "timeout")
        time.sleep(2.2)
        self.assertFalse((self.root / ".devflow/run/escaped").exists())

    def test_declared_build_output_is_allowed_but_other_mutation_is_not(self) -> None:
        allowed = [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('build').mkdir(); Path('build/result.txt').write_text('ok')",
        ]
        self.write_registry(
            [
                self.registry_check(
                    "build",
                    allowed,
                    effect="repository-build-artifacts",
                    output_roots=["build"],
                )
            ]
        )
        self.write_plan([self.plan_check("build")])
        self.assertEqual(self.run_runner().returncode, 0)
        (self.root / "build").unlink(missing_ok=True) if (self.root / "build").is_file() else shutil.rmtree(self.root / "build")
        outside = [
            sys.executable,
            "-c",
            "from pathlib import Path; Path('build').mkdir(); Path('settings.ini').write_text('changed')",
        ]
        self.write_registry(
            [
                self.registry_check(
                    "build",
                    outside,
                    effect="repository-build-artifacts",
                    output_roots=["build"],
                )
            ]
        )
        result = self.run_runner()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(json.loads(result.stdout)["results"][0]["source_mutation_detected"])

    def test_no_applicable_check_is_an_explicit_successful_noop(self) -> None:
        self.write_registry([self.registry_check("focused", [sys.executable, "-c", "raise SystemExit(99)"])])
        self.write_plan([], residual=["RISK-none-applicable"])
        result = self.run_runner()
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "skipped")
        self.assertEqual(payload["selected_count"], 0)

    def test_symlinked_registry_and_output_escape_are_rejected(self) -> None:
        outside = self.root / "outside.json"
        outside.write_text(json.dumps({"schema_version": 1, "checks": []}), encoding="utf-8")
        (self.root / ".devflow/run/registry.json").symlink_to(outside)
        self.write_plan([self.plan_check("missing")])
        self.assertEqual(self.run_runner().returncode, 2)
        (self.root / ".devflow/run/registry.json").unlink()
        self.write_registry([self.registry_check("focused", [sys.executable, "-c", "pass"])])
        self.write_plan([self.plan_check("focused")])
        result = self.run_runner("--json-out", "outside-result.json")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / "outside-result.json").exists())


if __name__ == "__main__":
    unittest.main()
