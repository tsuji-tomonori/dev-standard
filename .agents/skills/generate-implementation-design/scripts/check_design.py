#!/usr/bin/env python3
"""Check a target-owned as-built contract and run its local drift commands.

This validates declared coverage, not the semantic completeness of the inventory.
Commands are trusted repository code; this is not a process sandbox.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import types
from pathlib import Path

SURFACES = {"api", "data", "infra", "frontend"}
API_DOCUMENTS = {"detail-design", "interface", "messages", "query", "sequence", "unit-test"}
HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}


def confined(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError(f"invalid relative path: {value!r}")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"invalid relative path: {value}")
    path = root
    for part in parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed: {value}")
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"path escapes repository: {value}")
    return path


def strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ValueError(f"{label}: expected nonempty string array")
    return value


def snapshot(root: Path, outputs: list[str]) -> dict[str, bytes]:
    result = {}
    for value in outputs:
        path = confined(root, value)
        if path.suffix.lower() != ".md" or not path.is_file():
            raise ValueError(f"missing Markdown design: {value}")
        content = path.read_bytes()
        if not content.decode("utf-8").strip():
            raise ValueError(f"empty Markdown design: {value}")
        result[value] = content
    return result


def helper(name):
    """同梱した共通検査を独自adapterからも利用する。"""
    path = Path(__file__).absolute().with_name(name + ".py")
    if path.is_symlink():
        raise ValueError("symlink helper")
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


def check_structure(root, surface, document):
    """選択したprofileの章・階層・CRUD集合をdrift commandとは別に検査する。"""
    if "structure_model" not in surface:
        return
    model = json.loads(confined(root, surface["structure_model"]).read_text(encoding="utf-8"))
    base = confined(root, surface["structure_root"])
    files = {}
    for path in base.rglob("*"):
        relative = path.relative_to(root).as_posix()
        confined(root, relative)
        if path.is_file() and path.name != "manifest.json":
            files[path.relative_to(base).as_posix()] = path.read_text(encoding="utf-8")
    structure = helper("api_structure")
    structure.validate_structure(files, model, document)
    for operation in model["operations"]:
        expected = {kind: (base / name).relative_to(root).as_posix()
                    for kind, name in structure.names(model, operation).items()}
        if surface["operation_documents"][operation["id"]] != expected:
            raise ValueError("operation mapping differs from selected hierarchy")
    index = helper("api_layout").Index(root, model["python_root"])
    expected_crud = structure.render_crud(structure.crud(model, root, index))
    # Markdown bannerはgeneratorの出力のみ除去する。
    for name, expected in expected_crud.items():
        actual = files.get(name, "")
        if actual.startswith("<!-- AUTO-GENERATED."):
            actual = actual.split("-->\n\n", 1)[-1]
        if name.endswith(".json"):
            same = json.loads(actual) == json.loads(expected) if actual else False
        else:
            same = actual == expected
        if not same:
            raise ValueError(f"CRUD model/output drift: {name}")
    print("API structure and CRUD conformance passed (semantic completeness requires adapter tests)")


def api_outputs(root: Path, surface: dict) -> list[str]:
    """全OpenAPI operationについて6帳票の宣言漏れを拒否する。"""
    path = confined(root, surface.get("openapi"))
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("paths"), dict):
        raise ValueError("api: exported OpenAPI paths are required")
    ids = []
    for item in document["paths"].values():
        if not isinstance(item, dict) or "$ref" in item:
            raise ValueError("api: resolve OpenAPI path references before inventory")
        for method, operation in item.items():
            if method.lower() not in HTTP_METHODS:
                continue
            identity = operation.get("operationId") if isinstance(operation, dict) else None
            if not isinstance(identity, str) or not identity.strip():
                raise ValueError("api: every operation requires operationId")
            ids.append(identity)
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("api: empty or duplicate operation inventory")
    mapping = surface.get("operation_documents")
    if not isinstance(mapping, dict) or set(mapping) != set(ids):
        raise ValueError("api: operation_documents must exactly match OpenAPI operations")
    outputs = []
    for identity, documents in mapping.items():
        if not isinstance(documents, dict) or set(documents) != API_DOCUMENTS:
            raise ValueError(f"api {identity}: all six document kinds are required")
        paths = strings(list(documents.values()), f"api {identity}.documents")
        if len(set(paths)) != len(API_DOCUMENTS):
            raise ValueError(f"api {identity}: six distinct documents are required")
        outputs.extend(paths)
    if not set(outputs).issubset(strings(surface.get("markdown"), "api.markdown")):
        raise ValueError("api: operation documents are absent from Markdown drift inventory")
    if len(outputs) != len(set(outputs)):
        raise ValueError("documents shared by multiple operations")
    check_structure(root, surface, document)
    if "layout_config" in surface:
        config = json.loads(confined(root, surface["layout_config"]).read_text(encoding="utf-8"))
        helper("api_layout").inspect(root, config, document)
        print("API layout conformance passed (static scope)")
    return outputs


def check(root: Path, contract: str) -> None:
    root = root.resolve(strict=True)
    data = json.loads(confined(root, contract).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("design contract schema_version must be 1")
    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict) or not SURFACES.issubset(surfaces):
        raise ValueError("classify api, data, infra and frontend; add other surfaces as needed")
    commands = []
    outputs = []
    for name, surface in surfaces.items():
        if not isinstance(surface, dict):
            raise ValueError(f"{name}: invalid surface")
        status = surface.get("status")
        if status == "not-applicable":
            reason = surface.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{name}: not-applicable requires a reviewed reason")
            continue
        if status != "required":
            raise ValueError(f"{name}: incomplete design ({status!r})")
        for source in strings(surface.get("sources"), f"{name}.sources"):
            if not confined(root, source).exists():
                raise ValueError(f"{name}: missing implementation source {source}")
        if name == "api":
            api_outputs(root, surface)
        outputs.extend(strings(surface.get("markdown"), f"{name}.markdown"))
        strings(surface.get("generate"), f"{name}.generate")
        argv = strings(surface.get("check"), f"{name}.check")
        if argv not in commands:
            commands.append(argv)
    before = snapshot(root, outputs)
    for argv in commands:
        result = subprocess.run(argv, cwd=root, check=False, timeout=300)
        if result.returncode:
            raise ValueError(f"design drift command failed ({result.returncode}): {argv}")
        if snapshot(root, outputs) != before:
            raise ValueError(f"check command rewrote generated Markdown: {argv}")
    print(f"as-built check passed: {len(commands)} commands, {len(before)} Markdown files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--contract", default=".dev-standard/design.json")
    args = parser.parse_args()
    try:
        check(args.root, args.contract)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"as-built incomplete: {exc}\n")


if __name__ == "__main__":
    main()
