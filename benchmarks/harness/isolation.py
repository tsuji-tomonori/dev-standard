from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .io import BenchmarkError, digest_bytes, load_json, safe_path

CONDITIONS = ("full-skills", "no-skills", "length-matched-control")
IGNORED_PARTS = {"__pycache__", ".pytest_cache"}


@dataclass(frozen=True)
class PreparedWorkspace:
    path: Path
    condition: str
    context_bytes: int
    context_digest: str


def _validate_condition(condition: str) -> None:
    if condition not in CONDITIONS:
        raise BenchmarkError(f"unsupported benchmark condition: {condition}")


def _copy_fixture(source: Path, destination: Path) -> None:
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        if IGNORED_PARTS.intersection(relative.parts) or path.suffix == ".pyc":
            continue
        target = destination / relative
        if path.is_symlink():
            raise BenchmarkError(f"fixture symlink is not allowed: {relative}")
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.name not in {"state.json"}:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def _skill_material(root: Path, skill_ids: Iterable[str]) -> bytes:
    pieces: list[bytes] = []
    for skill_id in skill_ids:
        if not skill_id or "/" in skill_id or ".." in skill_id:
            raise BenchmarkError(f"invalid Skill id: {skill_id}")
        path = safe_path(root, f".agents/skills/{skill_id}/SKILL.md", require_exists=True)
        if not path.is_file():
            raise BenchmarkError(f"Skill path is not a file: {skill_id}")
        pieces.extend([f"\n## Skill: {skill_id}\n".encode(), path.read_bytes()])
    material = b"".join(pieces)
    if not material:
        raise BenchmarkError("selected Skill material must be non-empty")
    return material


def _fit_bytes(source: bytes, size: int, filler: bytes) -> bytes:
    if size <= 0:
        raise BenchmarkError("context size must be positive")
    data = source[:size]
    if len(data) < size:
        repeats = (size - len(data) + len(filler) - 1) // len(filler)
        data += (filler * repeats)[: size - len(data)]
    return data


def context_material(root: Path, task: dict, condition: str, target_size: int | None = None) -> bytes:
    _validate_condition(condition)
    full = _skill_material(root, task["agent_visible"]["selected_skill_ids"])
    target_size = target_size or len(full)
    if condition == "full-skills":
        return _fit_bytes(full, target_size, b"\n")
    if condition == "no-skills":
        return _fit_bytes(b"No task-specific procedural guidance is provided.\n", target_size, b"neutral context\n")
    docs = (root / "README.md").read_bytes() + b"\n" + (root / "docs" / "reference" / "development.md").read_bytes()
    return _fit_bytes(docs, target_size, b"retrieval-only context\n")


def prepare_workspace(root: Path, task_id: str, condition: str, destination: Path) -> PreparedWorkspace:
    root = root.resolve()
    _validate_condition(condition)
    if destination.is_symlink():
        raise BenchmarkError(f"workspace destination is a symlink: {destination}")
    if destination.exists() and any(destination.iterdir()):
        raise BenchmarkError(f"workspace destination is not empty: {destination}")
    task = load_json(safe_path(root, f"benchmarks/tasks/{task_id}/task.json", require_exists=True))
    fixture = safe_path(root, task["base"]["fixture"], require_exists=True)
    destination.mkdir(parents=True, exist_ok=True)
    _copy_fixture(fixture, destination)
    target_size = len(_skill_material(root, task["agent_visible"]["selected_skill_ids"]))
    material = context_material(root, task, condition, target_size)
    context_path = destination / ".benchmark-context" / "context.bin"
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_bytes(material)
    assert_no_oracle_leakage(root, destination)
    return PreparedWorkspace(destination.resolve(), condition, len(material), digest_bytes(material))


def assert_no_oracle_leakage(root: Path, workspace: Path) -> None:
    sentinels: list[bytes] = []
    for path in sorted((root / "benchmarks" / "oracles").glob("B*/oracle.json")):
        value = load_json(path)
        sentinels.append(str(value["leak_sentinel"]).encode("utf-8"))
        for variant in value["interaction"]["answer_variants"].values():
            sentinels.append(str(variant["answer"]).encode("utf-8"))
    for path in sorted(workspace.rglob("*")):
        if not path.is_file() or path.suffix == ".pyc" or IGNORED_PARTS.intersection(path.parts):
            continue
        content = path.read_bytes()
        for sentinel in sentinels:
            if sentinel and sentinel in content:
                raise BenchmarkError(f"oracle material leaked into agent workspace: {path}")
