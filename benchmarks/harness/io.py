from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


class BenchmarkError(RuntimeError):
    """Raised when benchmark input or execution violates the contract."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BenchmarkError(f"duplicate key: {key}")
        result[key] = value
    return result


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    loader.flatten_mapping(node)
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise BenchmarkError("YAML mapping keys must be strings")
        if key in result:
            raise BenchmarkError(f"duplicate key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (OSError, json.JSONDecodeError) as exc:
        raise BenchmarkError(f"cannot load JSON {path}: {exc}") from exc


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError, BenchmarkError) as exc:
        raise BenchmarkError(f"cannot load YAML {path}: {exc}") from exc


def load_structured(path: Path) -> Any:
    if path.suffix.lower() == ".json":
        return load_json(path)
    if path.suffix.lower() in {".yaml", ".yml"}:
        return load_yaml(path)
    raise BenchmarkError(f"unsupported structured file: {path}")


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def digest_value(value: Any) -> str:
    return digest_bytes(canonical_json(value))


def digest_file(path: Path) -> str:
    try:
        return digest_bytes(path.read_bytes())
    except OSError as exc:
        raise BenchmarkError(f"cannot hash {path}: {exc}") from exc


def safe_path(root: Path, relative: str, *, require_exists: bool = False, reject_symlink: bool = True) -> Path:
    root = root.resolve()
    candidate = root / relative
    if reject_symlink:
        current = root
        for part in Path(relative).parts:
            if part in {"", "."}:
                continue
            if part == "..":
                raise BenchmarkError(f"path escapes root: {relative}")
            current = current / part
            if current.is_symlink():
                raise BenchmarkError(f"symlink is not allowed: {relative}")
    resolved = candidate.resolve(strict=False)
    if resolved != root and root not in resolved.parents:
        raise BenchmarkError(f"path escapes root: {relative}")
    if require_exists and not resolved.exists():
        raise BenchmarkError(f"path does not exist: {relative}")
    return resolved


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")
