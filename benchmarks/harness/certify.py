from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

from .fixture import load_fixture
from .io import BenchmarkError, load_json, write_json
from .schema import load_and_validate, validate_repository_inputs
from .scoring import score_observed


def _resolve_test(root: Path, reference: str) -> None:
    path_text, symbol = reference.split("::", 1)
    class_name, method_name = symbol.split(".", 1)
    path = root / path_text
    if not path.is_file():
        raise BenchmarkError(f"acceptance test file does not exist: {reference}")
    spec = importlib.util.spec_from_file_location(f"acceptance_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise BenchmarkError(f"cannot import acceptance test: {reference}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    test_class = getattr(module, class_name, None)
    if test_class is None or not callable(getattr(test_class, method_name, None)):
        raise BenchmarkError(f"acceptance test symbol does not exist: {reference}")


def validate_acceptance_matrix(root: Path) -> dict[str, Any]:
    matrix = load_and_validate(root, "acceptance-matrix", root / "benchmarks" / "repository" / "acceptance-matrix.json")
    identifiers: set[str] = set()
    for criterion in matrix["criteria"]:
        if criterion["id"] in identifiers:
            raise BenchmarkError(f"duplicate acceptance criterion: {criterion['id']}")
        identifiers.add(criterion["id"])
        for evidence in criterion["evidence"]:
            path = root / evidence.split("::", 1)[0]
            if not path.exists():
                raise BenchmarkError(f"acceptance evidence does not exist: {evidence}")
        for test in criterion["tests"]:
            _resolve_test(root, test)
    expected = {f"I22-AC-{index:02d}" for index in range(1, 17)} | {f"I22-RV-{index:02d}" for index in range(1, 16)}
    if identifiers != expected:
        raise BenchmarkError(f"acceptance matrix IDs differ: missing={sorted(expected-identifiers)} extra={sorted(identifiers-expected)}")
    return matrix


def certify_task(root: Path, task_id: str) -> dict[str, Any]:
    task = load_and_validate(root, "task", root / "benchmarks" / "tasks" / task_id / "task.json")
    oracle = load_and_validate(root, "oracle", root / "benchmarks" / "oracles" / task_id / "oracle.json")
    results: dict[str, dict[str, Any]] = {}
    for variant in ("base", "gold", "mutation"):
        state_root, observed = load_fixture(root, task_id, variant)
        results[variant] = score_observed(root, task, oracle, observed, state_root=state_root)
    if results["gold"]["strict_e2e_pass"] is not True:
        raise BenchmarkError(f"{task_id}: gold does not Strict Pass")
    base_failed = {name for name, value in results["base"]["gates"].items() if not value}
    mutation_failed = {name for name, value in results["mutation"]["gates"].items() if not value}
    if not set(oracle["certification"]["base_failed_gates"]).issubset(base_failed):
        raise BenchmarkError(f"{task_id}: base does not fail intended Gate")
    if not set(oracle["certification"]["mutation_failed_gates"]).issubset(mutation_failed):
        raise BenchmarkError(f"{task_id}: mutation does not fail intended Gate")
    return {
        "task_id": task_id,
        "conditions": task["conditions"],
        "gold_pass": True,
        "base_failed_gates": sorted(base_failed),
        "mutation_failed_gates": sorted(mutation_failed),
        "physical_fixture_discrimination": True,
    }


def certification_report(root: Path) -> dict[str, Any]:
    counts = validate_repository_inputs(root)
    matrix = validate_acceptance_matrix(root)
    tasks = [certify_task(root, f"B{index:02d}") for index in range(1, 9)]
    return {
        "schema_version": 1,
        "tasks": tasks,
        "oracle_discrimination": {
            "gold_passes": sum(item["gold_pass"] for item in tasks),
            "base_failures": sum(bool(item["base_failed_gates"]) for item in tasks),
            "mutation_failures": sum(bool(item["mutation_failed_gates"]) for item in tasks),
            "mutation_score": sum(bool(item["mutation_failed_gates"]) for item in tasks) / len(tasks),
        },
        "acceptance": {
            "verified": len(matrix["criteria"]),
            "criterion_ids": [item["id"] for item in matrix["criteria"]],
            "evidence_references": sum(len(item["evidence"]) for item in matrix["criteria"]),
            "test_references": sum(len(item["tests"]) for item in matrix["criteria"]),
        },
        "inputs": counts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = certification_report(args.root.resolve())
        target = args.root / "benchmarks" / "repository" / "certification-cases.json"
        if args.write:
            write_json(target, report)
        if args.check:
            if not target.is_file() or load_json(target) != report:
                raise BenchmarkError("benchmark certification cases drift")
            print("benchmark certification cases current")
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
    except BenchmarkError as exc:
        print(f"ERROR: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
