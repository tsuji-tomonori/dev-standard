from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from benchmarks.harness.fixture import load_fixture
from benchmarks.harness.io import BenchmarkError, load_json, load_yaml
from benchmarks.harness.run import create_manifest
from benchmarks.harness.schema import load_and_validate, validate_repository_inputs, validate_value
from benchmarks.harness.scoring import score_observed

ROOT = Path(__file__).resolve().parents[2]


class SchemaContractTest(unittest.TestCase):
    def test_all_tasks_oracles_and_results_validate(self) -> None:
        self.assertEqual(validate_repository_inputs(ROOT), {"tasks": 8, "oracles": 8})
        for index in range(1, 9):
            task_id = f"B{index:02d}"
            task = load_and_validate(ROOT, "task", ROOT / "benchmarks" / "tasks" / task_id / "task.json")
            oracle = load_and_validate(ROOT, "oracle", ROOT / "benchmarks" / "oracles" / task_id / "oracle.json")
            state_root, observed = load_fixture(ROOT, task_id, "gold")
            result = score_observed(ROOT, task, oracle, observed, state_root=state_root)
            validate_value(ROOT, "result", result, task_id)

    def test_completed_result_rejects_incomplete_execution_record(self) -> None:
        task = load_json(ROOT / "benchmarks/tasks/B01/task.json")
        oracle = load_json(ROOT / "benchmarks/oracles/B01/oracle.json")
        state_root, observed = load_fixture(ROOT, "B01", "gold")
        result = score_observed(ROOT, task, oracle, observed, state_root=state_root)
        result["execution"]["phases"] = []
        with self.assertRaises(BenchmarkError):
            validate_value(ROOT, "result", result)

    def test_machine_readable_inputs_reject_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            json_path = Path(directory) / "duplicate.json"
            json_path.write_text('{"a": 1, "a": 2}\n', encoding="utf-8")
            yaml_path = Path(directory) / "duplicate.yaml"
            yaml_path.write_text("a: 1\na: 2\n", encoding="utf-8")
            with self.assertRaises(BenchmarkError):
                load_json(json_path)
            with self.assertRaises(BenchmarkError):
                load_yaml(yaml_path)

    def test_reference_registry_is_machine_readable_and_uses_deveval(self) -> None:
        registry = load_and_validate(ROOT, "reference-registry", ROOT / "benchmarks/references.json")
        reference = next(item for item in registry["references"] if item["paper_id"] == "arXiv:2403.08604")
        self.assertIn("Full Software Development Lifecycle", reference["title"])
        self.assertNotIn("DevBench", reference["title"])
        self.assertIn("DevEval", reference["limitation"])
        for item in registry["references"]:
            for field in ["paper_id", "version", "date", "publication_status", "adopted_claim", "limitation"]:
                self.assertTrue(item[field])

    def test_run_manifest_and_execution_contract_capture_reproducibility_fields(self) -> None:
        manifest = create_manifest(
            ROOT,
            "B01",
            "full-skills",
            7,
            model_id="test-model",
            model_revision="revision-1",
            repository_commit="8174ec455e7062e5a7eb45f91d2fba60aafc7fcb",
            arm_order=["no-skills", "length-matched-control", "full-skills"],
            started_at="2026-07-24T00:00:00+00:00",
        )
        validate_value(ROOT, "run-manifest", manifest)
        for field in [
            "harness_version",
            "system_prompt_digest",
            "developer_prompt_digest",
            "tool_schema_digest",
            "skill_digests",
            "repository_commit",
            "task_digest",
            "oracle_digest",
        ]:
            self.assertIn(field, manifest)
        self.assertEqual(manifest["environment"]["network_policy"], "deny-agent-workspace-egress")

    def test_semantic_slots_and_check_oracle_are_explicit(self) -> None:
        for index in range(1, 9):
            oracle = load_json(ROOT / f"benchmarks/oracles/B{index:02d}/oracle.json")
            statuses = {slot["status"] for slot in oracle["requirements"]["semantic_slots"].values()}
            self.assertTrue(statuses <= {"required", "optional", "not_applicable"})
            self.assertEqual(
                set(oracle["governance"]),
                {"profile", "required_checks", "forbidden_checks", "admissible_checks", "evidence_paths"},
            )

    def test_task_schema_rejects_missing_control_condition(self) -> None:
        task = copy.deepcopy(load_json(ROOT / "benchmarks/tasks/B01/task.json"))
        task["conditions"].remove("length-matched-control")
        with self.assertRaises(BenchmarkError):
            validate_value(ROOT, "task", task)

    def test_acceptance_matrix_has_its_own_schema(self) -> None:
        schema = load_json(ROOT / "benchmarks/schemas/acceptance-matrix.schema.json")
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        matrix = load_and_validate(ROOT, "acceptance-matrix", ROOT / "benchmarks/repository/acceptance-matrix.json")
        self.assertEqual(matrix["issue"], 22)
