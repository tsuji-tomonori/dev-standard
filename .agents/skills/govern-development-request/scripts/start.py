#!/usr/bin/env python3
"""Pinned convenience entrypoint for ``regulatedflow init``."""

from __future__ import annotations

import os
import stat
import sys
import types
from pathlib import Path


def _bootstrap_module(path: Path, *, root: Path, module_name: str) -> types.ModuleType:
    """Load one source file below a trusted root without following links."""

    root = root.absolute()
    path = path.absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise RuntimeError(f"module escapes repository root: {path}") from exc
    portable = sys.modules.get("_dev_standard_portable_imports")
    if portable is not None:
        return portable.load_relative("/".join(parts), module_name)
    directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(os.sep, directory_flags)
    try:
        for component in root.parts[1:]:
            next_descriptor = os.open(component, directory_flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        for part in parts[:-1]:
            next_descriptor = os.open(part, directory_flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        source_descriptor = os.open(
            parts[-1],
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            dir_fd=descriptor,
        )
        try:
            info = os.fstat(source_descriptor)
            if not stat.S_ISREG(info.st_mode):
                raise RuntimeError(f"module is not a regular file: {path}")
            chunks: list[bytes] = []
            while chunk := os.read(source_descriptor, 1024 * 1024):
                chunks.append(chunk)
        finally:
            os.close(source_descriptor)
    finally:
        os.close(descriptor)
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    sys.modules[module_name] = module
    exec(compile(b"".join(chunks), str(path), "exec"), module.__dict__)
    return module


def main(argv: list[str] | None = None) -> int:
    root = Path.cwd().absolute()
    flow = _bootstrap_module(
        Path(__file__).absolute().parent / "regulatedflow.py",
        root=root,
        module_name="dev_standard_regulatedflow",
    )
    return int(flow.main(["--root", str(root), "init", *(argv if argv is not None else sys.argv[1:])]))


if __name__ == "__main__":
    raise SystemExit(main())
