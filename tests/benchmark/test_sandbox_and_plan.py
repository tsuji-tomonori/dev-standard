from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from benchmarks.harness.fixture import load_fixture
from benchmarks.harness.io import BenchmarkError
from benchmarks.harness.isolation import prepare_workspace
from benchmarks.harness.run import counterbalanced_order
from benchmarks.harness.sandbox import network_namespace_probe, write_tool_audit

ROOT = Path(__file__).resolve().parents[2]


class SandboxAndPlanTest(unittest.TestCase):
    def test_all_gold_results_assert_network_policy_enforcement(self) -> None:
        for index in range(1, 9):
            _, observed = load_fixture(ROOT, f"B{index:02d}", "gold")
            self.assertTrue(observed["safety"]["network_enforced"])
            self.assertTrue(observed["safety"]["tool_audit_valid"])

    def test_audit_path_inside_agent_workspace_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            with self.assertRaises(BenchmarkError):
                write_tool_audit(workspace / "audit.json", workspace=workspace, argv=["true"], environment={}, status="completed")

    def test_counterbalanced_order_is_deterministic_and_complete(self) -> None:
        for seed in range(12):
            self.assertEqual(counterbalanced_order(seed), counterbalanced_order(seed))
            self.assertEqual(set(counterbalanced_order(seed)), {"full-skills", "no-skills", "length-matched-control"})
        self.assertGreater(len({tuple(counterbalanced_order(seed)) for seed in range(6)}), 2)

    def test_network_namespace_fails_closed_and_denies_egress(self) -> None:
        def denied(*args, **kwargs):
            return subprocess.CompletedProcess(args[0], 0, "", "")

        def unavailable(*args, **kwargs):
            return subprocess.CompletedProcess(args[0], 1, "", "unshare denied")

        self.assertTrue(network_namespace_probe(denied))
        self.assertFalse(network_namespace_probe(unavailable))

    def test_prepare_cli_path_keeps_oracle_metadata_outside_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            prepare_workspace(ROOT, "B02", "no-skills", workspace)
            self.assertFalse((workspace / "benchmarks/oracles").exists())
            self.assertFalse((workspace / "state.json").exists())

    def test_tool_audit_is_outside_agent_workspace_and_redacts_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "workspace"
            workspace.mkdir()
            audit = root / "audit" / "tool.json"
            write_tool_audit(audit, workspace=workspace, argv=["python", "agent.py"], environment={"API_TOKEN": "secret", "LANG": "C"}, status="completed")
            value = json.loads(audit.read_text(encoding="utf-8"))
            self.assertEqual(value["environment"]["API_TOKEN"], "<redacted>")
            self.assertEqual(value["environment"]["LANG"], "C")
