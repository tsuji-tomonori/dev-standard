from __future__ import annotations

import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from benchmarks.harness.certify import validate_acceptance_matrix
from benchmarks.harness.io import BenchmarkError, load_json

ROOT = Path(__file__).resolve().parents[2]


class RepositoryPolicyTest(unittest.TestCase):
    def test_acceptance_matrix_has_no_unverified_item(self) -> None:
        matrix = validate_acceptance_matrix(ROOT)
        self.assertEqual(len(matrix["criteria"]), 31)
        self.assertTrue(all(item["status"] == "verified" for item in matrix["criteria"]))

    def test_acceptance_matrix_rejects_duplicate_and_unresolvable_test_symbols(self) -> None:
        matrix = load_json(ROOT / "benchmarks/repository/acceptance-matrix.json")
        duplicate = copy.deepcopy(matrix)
        duplicate["criteria"][1]["id"] = duplicate["criteria"][0]["id"]
        with patch("benchmarks.harness.certify.load_and_validate", return_value=duplicate):
            with self.assertRaises(BenchmarkError):
                validate_acceptance_matrix(ROOT)
        unresolved = copy.deepcopy(matrix)
        unresolved["criteria"][0]["tests"] = ["tests/benchmark/test_missing.py::Missing.test_missing"]
        with patch("benchmarks.harness.certify.load_and_validate", return_value=unresolved):
            with self.assertRaises(BenchmarkError):
                validate_acceptance_matrix(ROOT)

    def test_all_fixtures_are_explicitly_synthetic(self) -> None:
        states = sorted((ROOT / "benchmarks/fixtures").glob("B*/**/state.json"))
        self.assertGreaterEqual(len(states), 26)
        for path in states:
            value = load_json(path)
            self.assertTrue(value["synthetic"], path)
            self.assertTrue((path.parent / "SYNTHETIC_FIXTURE").is_file(), path)

    def test_change_has_adr_review_and_canonical_requirement_trace(self) -> None:
        adr = ROOT / "docs/decisions/ADR-0003-skills-e2e-benchmark.md"
        review = ROOT / "governance/reviews/CHG-20260724-skills-e2e-benchmark.yaml"
        requirements = load_json(ROOT / "spec/requirements/requirements.json")
        requirement = next(item for item in requirements["requirements"] if item["id"] == "REQ-BENCH-001")
        self.assertTrue(adr.is_file())
        self.assertTrue(review.is_file())
        self.assertIn(adr.relative_to(ROOT).as_posix(), requirement["traces"]["design"])
        self.assertIn("tests/benchmark/test_scoring.py", requirement["traces"]["tests"])

    def test_no_live_run_records_or_work_directory_are_committed(self) -> None:
        forbidden = ["work", "trajectory.jsonl", "run-result.json", "utility-report.json", "tool-audit.json"]
        tracked = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
        for value in tracked:
            self.assertFalse(value.startswith("work/"), value)
            self.assertNotIn(Path(value).name, forbidden, value)

    def test_promotion_thresholds_are_predeclared(self) -> None:
        policy = load_json(ROOT / "benchmarks/promotion-policy.json")
        thresholds = policy["blocking_promotion_requires"]
        for key in ["minimum_runs", "infrastructure_flake_rate_max", "provider_failure_rate_max", "oracle_leakage_incidents", "reproduction_rate_min", "human_annotation_agreement_min"]:
            self.assertIn(key, thresholds)
        self.assertEqual(policy["agent_smoke_initial_mode"], "advisory")

    def test_skills_benchmark_distribution_excludes_repository_and_live_evidence(self) -> None:
        manifest = load_json(ROOT / "distribution/manifest.json")
        mappings = manifest["profiles"]["skills-benchmark"]
        sources = {item["source"] for item in mappings}
        self.assertIn("benchmarks/harness", sources)
        self.assertIn("benchmarks/schemas", sources)
        self.assertNotIn("benchmarks/repository", sources)
        self.assertFalse(any("governance/reviews/CHG-" in source for source in sources))

    def test_utility_claim_is_conditioned_to_fixed_context(self) -> None:
        protocol = load_json(ROOT / "benchmarks/protocol.json")
        self.assertIn("固定model", protocol["claim_boundary"])
        self.assertIn("条件付き増分効果", protocol["claim_boundary"])
        self.assertNotIn("普遍", protocol["claim_boundary"])

    def test_workflow_boundaries_separate_smoke_flake_utility_and_trusted_oracle(self) -> None:
        workflows = {path.name: path.read_text(encoding="utf-8") for path in (ROOT / ".github/workflows").glob("benchmark-*.yml")}
        self.assertEqual(set(workflows), {"benchmark-conformance.yml", "benchmark-agent-smoke.yml", "benchmark-flake.yml", "benchmark-utility.yml", "benchmark-heldout.yml"})
        self.assertIn("pull_request", workflows["benchmark-conformance.yml"])
        self.assertIn("continue-on-error: true", workflows["benchmark-agent-smoke.yml"])
        self.assertIn("schedule", workflows["benchmark-flake.yml"])
        self.assertIn("schedule", workflows["benchmark-utility.yml"])
        self.assertNotIn("pull_request", workflows["benchmark-heldout.yml"])
        self.assertIn("environment: benchmark-heldout", workflows["benchmark-heldout.yml"])
        for name in ["benchmark-agent-smoke.yml", "benchmark-flake.yml", "benchmark-utility.yml", "benchmark-heldout.yml"]:
            self.assertNotIn("archive: false", workflows[name], name)
            self.assertIn("if-no-files-found: error", workflows[name], name)

    def test_cloudformation_intrinsic_yaml_is_checked_by_the_domain_parser(self) -> None:
        config = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        self.assertIn("benchmarks/fixtures/B07", config)
        self.assertIn("check-yaml", config)
