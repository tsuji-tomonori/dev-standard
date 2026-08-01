from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from .designfacts import derive_cloudformation_facts, derive_fastapi_sql_facts
from .io import BenchmarkError, load_json, safe_path

VARIANTS = {"base", "gold", "mutation"}


def fixture_root(root: Path, task_id: str, variant: str) -> Path:
    if variant not in VARIANTS:
        raise BenchmarkError(f"unsupported fixture variant: {variant}")
    return safe_path(root, f"benchmarks/fixtures/{task_id}/{variant}", require_exists=True)


def load_fixture(root: Path, task_id: str, variant: str) -> tuple[Path, dict[str, Any]]:
    state_root = fixture_root(root, task_id, variant)
    marker = safe_path(state_root, "SYNTHETIC_FIXTURE", require_exists=True)
    if "synthetic benchmark fixture" not in marker.read_text(encoding="utf-8"):
        raise BenchmarkError(f"{marker}: fixture marker is invalid")
    state_path = safe_path(state_root, "state.json", require_exists=True)
    state = load_json(state_path)
    if not isinstance(state, dict):
        raise BenchmarkError(f"{state_path}: root must be an object")
    if state.get("schema_version") != 1 or state.get("synthetic") is not True:
        raise BenchmarkError(f"{state_path}: fixture must be schema v1 and explicitly synthetic")
    if state.get("task_id") != task_id or state.get("variant") != variant:
        raise BenchmarkError(f"{state_path}: fixture identity mismatch")
    observed = state.get("observed")
    if not isinstance(observed, dict):
        raise BenchmarkError(f"{state_path}: observed must be an object")
    return state_root, copy.deepcopy(observed)


def load_answer_variant(root: Path, task_id: str, variant: str) -> tuple[Path, dict[str, Any]]:
    state_root = safe_path(root, f"benchmarks/fixtures/{task_id}/variants/{variant}", require_exists=True)
    marker = safe_path(state_root, "SYNTHETIC_FIXTURE", require_exists=True)
    if "synthetic benchmark fixture" not in marker.read_text(encoding="utf-8"):
        raise BenchmarkError(f"{marker}: fixture marker is invalid")
    state = load_json(safe_path(state_root, "state.json", require_exists=True))
    if not isinstance(state, dict) or state.get("task_id") != task_id or state.get("variant") != variant:
        raise BenchmarkError(f"{state_root}: answer variant identity mismatch")
    observed = state.get("observed")
    if not isinstance(observed, dict):
        raise BenchmarkError(f"{state_root}: observed must be an object")
    return state_root, copy.deepcopy(observed)


def derive_design(root: Path, adapter: str, state_root: Path) -> dict[str, Any] | None:
    if adapter == "fastapi-sql":
        return derive_fastapi_sql_facts(state_root)
    if adapter == "cloudformation":
        return derive_cloudformation_facts(state_root)
    if adapter in {"none", "governance"}:
        return None
    raise BenchmarkError(f"unsupported design adapter: {adapter}")


def validate_evidence_paths(state_root: Path, paths: list[str]) -> None:
    for value in paths:
        path = safe_path(state_root, value, require_exists=True)
        if not path.is_file():
            raise BenchmarkError(f"evidence is not a file: {value}")


def validate_changed_paths(paths: list[str], forbidden: list[str]) -> bool:
    for value in paths:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            return False
        normalized = path.as_posix()
        for blocked in forbidden:
            blocked_path = Path(blocked).as_posix().rstrip("/")
            if normalized == blocked_path or normalized.startswith(blocked_path + "/"):
                return False
    return True
