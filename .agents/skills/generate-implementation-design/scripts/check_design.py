#!/usr/bin/env python3
"""Check a target-owned as-built contract and run its local drift commands.

This validates declared coverage, not the semantic completeness of the inventory.
Commands are trusted repository code; this is not a process sandbox.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

SURFACES = {"api", "data", "infra", "frontend"}


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
