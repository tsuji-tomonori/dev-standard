from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from .io import BenchmarkError, load_json, load_structured

SCHEMAS = {
    "task": "task.schema.json",
    "oracle": "oracle.schema.json",
    "result": "result.schema.json",
    "run-manifest": "run-manifest.schema.json",
    "trajectory-event": "trajectory-event.schema.json",
    "acceptance-matrix": "acceptance-matrix.schema.json",
    "reference-registry": "reference-registry.schema.json",
}


def schema_path(root: Path, name: str) -> Path:
    try:
        filename = SCHEMAS[name]
    except KeyError as exc:
        raise BenchmarkError(f"unknown schema: {name}") from exc
    return root / "benchmarks" / "schemas" / filename


def validate_value(root: Path, name: str, value: Any, source: str = "<memory>") -> None:
    schema = load_json(schema_path(root, name))
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value), key=lambda item: list(item.path))
    if errors:
        details = "; ".join(f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}" for error in errors)
        raise BenchmarkError(f"{source}: {name} schema validation failed: {details}")


def load_and_validate(root: Path, name: str, path: Path) -> Any:
    value = load_structured(path)
    validate_value(root, name, value, path.as_posix())
    return value


def validate_repository_inputs(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {"tasks": 0, "oracles": 0}
    tasks_root = root / "benchmarks" / "tasks"
    oracles_root = root / "benchmarks" / "oracles"
    for task_path in sorted(tasks_root.glob("B*/task.json")):
        task = load_and_validate(root, "task", task_path)
        oracle_path = oracles_root / task["id"] / "oracle.json"
        oracle = load_and_validate(root, "oracle", oracle_path)
        if oracle["task_id"] != task["id"]:
            raise BenchmarkError(f"{oracle_path}: task_id does not match {task['id']}")
        if sorted(task["conditions"]) != sorted(["full-skills", "no-skills", "length-matched-control"]):
            raise BenchmarkError(f"{task_path}: all three comparison conditions are required exactly once")
        counts["tasks"] += 1
        counts["oracles"] += 1
    if counts["tasks"] != 8:
        raise BenchmarkError(f"expected 8 MVP tasks, found {counts['tasks']}")
    validate_value(root, "reference-registry", load_json(root / "benchmarks" / "references.json"), "benchmarks/references.json")
    validate_value(
        root,
        "acceptance-matrix",
        load_json(root / "benchmarks" / "repository" / "acceptance-matrix.json"),
        "benchmarks/repository/acceptance-matrix.json",
    )
    return counts
