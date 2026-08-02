from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from benchmarks.harness.io import BenchmarkError, load_json
from benchmarks.harness.run import (
    build_environment,
    paired_plan,
    parse_adapter_command,
    run_identity,
    run_paired,
    run_phase,
    validate_conditions,
)
from benchmarks.harness.schema import validate_value

ROOT = Path(__file__).resolve().parents[2]


class RunProtocolTest(unittest.TestCase):
    def test_adapter_command_is_argv_not_shell_text(self) -> None:
        self.assertEqual(parse_adapter_command('["python", "agent.py"]'), ("python", "agent.py"))
        with self.assertRaises(BenchmarkError):
            parse_adapter_command("python agent.py")
        with self.assertRaises(BenchmarkError):
            parse_adapter_command(["python", ""])

    def test_adapter_environment_is_allowlisted_and_benchmark_values_are_explicit(self) -> None:
        environment = build_environment({"PATH": "/bin", "LANG": "C", "AWS_SECRET_ACCESS_KEY": "secret", "BENCHMARK_TASK": "B01"})
        self.assertEqual(environment, {"PATH": "/bin", "LANG": "C"})
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", environment)
        self.assertNotIn("BENCHMARK_TASK", environment)

    def test_benchmark_variables_cannot_be_imported_via_allowlist(self) -> None:
        environment = build_environment({"BENCHMARK_ORACLE": "leak", "DEVSTD_BENCH_TASK": "B01", "HOME": "/tmp"})
        self.assertEqual(environment, {"HOME": "/tmp"})

    def test_external_adapter_result_matches_phase_structured_execution_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            adapter = [sys.executable, "-m", "benchmarks.harness.reference_adapter"]
            old = os.environ.get("PYTHONPATH")
            os.environ["PYTHONPATH"] = str(ROOT)
            try:
                results = run_paired(ROOT, "B01", 0, adapter, output, "smoke")
            finally:
                if old is None:
                    os.environ.pop("PYTHONPATH", None)
                else:
                    os.environ["PYTHONPATH"] = old
            self.assertEqual(len(results), 3)
            for result in results:
                validate_value(ROOT, "result", result)
                self.assertTrue(result["execution"]["phases"])

    def test_paired_command_runs_each_condition_exactly_once(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B01/task.json")
        order = paired_plan(task, 17)
        self.assertEqual(len(order), 3)
        self.assertEqual({condition: order.count(condition) for condition in order}, {condition: 1 for condition in order})

    def test_paired_conditions_must_declare_all_three_arms_exactly_once(self) -> None:
        self.assertEqual(len(validate_conditions(["full-skills", "no-skills", "length-matched-control"])), 3)
        for invalid in [
            ["full-skills", "no-skills"],
            ["full-skills", "no-skills", "no-skills"],
            ["full-skills", "no-skills", "unknown"],
        ]:
            with self.assertRaises(BenchmarkError):
                validate_conditions(invalid)

    def test_provider_error_is_the_only_retryable_phase_failure(self) -> None:
        calls = []

        def runner(*args, **kwargs):
            calls.append(1)
            return subprocess.CompletedProcess(args[0], 75 if len(calls) == 1 else 0, "", "")

        phase = run_phase("execute", ["adapter"], runner=runner, max_provider_retries=1)
        self.assertEqual(phase["status"], "completed")
        self.assertEqual(phase["attempts"], 2)

    def test_run_identity_ignores_clock_but_changes_with_fixed_input_digest(self) -> None:
        first = run_identity({"task": "B01", "seed": 1, "started_at": "a"})
        second = run_identity({"task": "B01", "seed": 1, "started_at": "b"})
        third = run_identity({"task": "B01", "seed": 2, "started_at": "a"})
        self.assertEqual(first, second)
        self.assertNotEqual(first, third)

    def test_tool_crash_and_timeout_are_not_retried(self) -> None:
        timeout_calls = []

        def timeout_runner(*args, **kwargs):
            timeout_calls.append(1)
            raise subprocess.TimeoutExpired(args[0], 1)

        self.assertEqual(run_phase("execute", ["adapter"], runner=timeout_runner)["attempts"], 1)
        crash_calls = []

        def crash_runner(*args, **kwargs):
            crash_calls.append(1)
            raise OSError("crash")

        self.assertEqual(run_phase("execute", ["adapter"], runner=crash_runner)["attempts"], 1)
