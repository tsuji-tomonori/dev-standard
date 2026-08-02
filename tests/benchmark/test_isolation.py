from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from benchmarks.harness.io import BenchmarkError, load_json
from benchmarks.harness.isolation import assert_no_oracle_leakage, context_material, prepare_workspace

ROOT = Path(__file__).resolve().parents[2]


class IsolationTest(unittest.TestCase):
    def test_all_three_conditions_have_equal_nonzero_control_volume(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sizes = []
            digests = []
            for condition in ["full-skills", "no-skills", "length-matched-control"]:
                result = prepare_workspace(ROOT, "B01", condition, Path(directory) / condition)
                sizes.append(result.context_bytes)
                digests.append(result.context_digest)
            self.assertEqual(len(set(sizes)), 1)
            self.assertGreater(sizes[0], 0)
            self.assertEqual(len(set(digests)), 3)

    def test_oracle_and_simulated_answers_never_enter_agent_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            prepare_workspace(ROOT, "B02", "full-skills", workspace)
            material = b"".join(path.read_bytes() for path in workspace.rglob("*") if path.is_file())
            oracle = load_json(ROOT / "benchmarks/oracles/B02/oracle.json")
            self.assertNotIn(oracle["leak_sentinel"].encode(), material)
            for variant in oracle["interaction"]["answer_variants"].values():
                self.assertNotIn(variant["answer"].encode(), material)
            self.assertFalse((workspace / "state.json").exists())

    def test_repository_relative_paths_and_skill_ids_fail_closed(self) -> None:
        task = copy.deepcopy(load_json(ROOT / "benchmarks/tasks/B01/task.json"))
        task["agent_visible"]["selected_skill_ids"] = ["../secret"]
        with self.assertRaises(BenchmarkError):
            context_material(ROOT, task, "full-skills")

    def test_sentinel_detection_rejects_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory) / "workspace"
            workspace.mkdir()
            oracle = load_json(ROOT / "benchmarks/oracles/B01/oracle.json")
            (workspace / "leak.txt").write_text(oracle["leak_sentinel"], encoding="utf-8")
            with self.assertRaises(BenchmarkError):
                assert_no_oracle_leakage(ROOT, workspace)

    def test_workspace_destination_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "target"
            target.mkdir()
            link = root / "link"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(BenchmarkError):
                prepare_workspace(ROOT, "B01", "full-skills", link)

    def test_workspace_ignores_runtime_python_cache_material(self) -> None:
        cache = ROOT / "benchmarks/fixtures/B01/base/__pycache__"
        cache.mkdir(exist_ok=True)
        (cache / "secret.pyc").write_bytes(b"runtime cache")
        try:
            with tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "workspace"
                prepare_workspace(ROOT, "B01", "full-skills", workspace)
                self.assertFalse((workspace / "__pycache__").exists())
        finally:
            (cache / "secret.pyc").unlink(missing_ok=True)
            cache.rmdir()
