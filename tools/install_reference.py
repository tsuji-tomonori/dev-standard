#!/usr/bin/env python3
"""Safely copy selected reference assets into another repository."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "distribution" / "manifest.json"
IGNORED_PARTS = {"__pycache__"}


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class CopyItem:
    source: Path
    destination: Path


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def safe_source(relative: str) -> Path:
    source = (ROOT / relative).resolve()
    if source != ROOT and ROOT not in source.parents:
        raise InstallError(f"source escapes repository: {relative}")
    if not source.exists() or source.is_symlink():
        raise InstallError(f"source is missing or symlinked: {relative}")
    return source


def expand_mapping(target: Path, source_text: str, destination_text: str) -> list[CopyItem]:
    source = safe_source(source_text)
    destination = target / destination_text
    resolved_destination = destination.resolve(strict=False)
    if resolved_destination != target and target not in resolved_destination.parents:
        raise InstallError(f"destination escapes target repository: {destination_text}")
    if source.is_file():
        return [CopyItem(source, destination)]
    items: list[CopyItem] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink() or IGNORED_PARTS.intersection(path.parts) or path.suffix == ".pyc":
            continue
        if path.parent.name == "reviews" and path.name.startswith("CHG-") and path.suffix in {".yaml", ".yml"}:
            continue
        items.append(CopyItem(path, destination / path.relative_to(source)))
    return items


def plan(target: Path, profiles: list[str], manifest: dict[str, object]) -> list[CopyItem]:
    profile_map = manifest.get("profiles")
    if not isinstance(profile_map, dict):
        raise InstallError("manifest profiles are invalid")
    items: dict[Path, CopyItem] = {}
    for profile in profiles:
        mappings = profile_map.get(profile)
        if not isinstance(mappings, list):
            raise InstallError(f"unknown profile: {profile}")
        for mapping in mappings:
            if not isinstance(mapping, dict):
                raise InstallError(f"invalid mapping in profile: {profile}")
            for item in expand_mapping(target, str(mapping["source"]), str(mapping["destination"])):
                previous = items.get(item.destination)
                if previous and previous.source != item.source:
                    raise InstallError(f"multiple sources target: {item.destination}")
                items[item.destination] = item
    return [items[path] for path in sorted(items)]


def install(target: Path, profiles: list[str], *, apply: bool, force: bool) -> tuple[int, int, int]:
    target = target.resolve()
    if target in {Path("/"), Path.home().resolve()}:
        raise InstallError("target must be a repository directory, not root or home")
    if not target.is_dir():
        raise InstallError(f"target directory does not exist: {target}")
    items = plan(target, profiles, load_manifest())
    conflicts = [item for item in items if item.destination.exists() and not filecmp.cmp(item.source, item.destination, shallow=False)]
    if conflicts and not force:
        for item in conflicts:
            print(f"CONFLICT {item.destination}")
        raise InstallError("existing files differ; rerun with --force only after reviewing the dry-run")
    copied = unchanged = 0
    for item in items:
        if item.destination.exists() and filecmp.cmp(item.source, item.destination, shallow=False):
            unchanged += 1
            print(f"UNCHANGED {item.destination}")
            continue
        action = "COPY" if apply else "WOULD_COPY"
        print(f"{action} {item.source.relative_to(ROOT)} -> {item.destination}")
        if apply:
            item.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item.source, item.destination)
        copied += 1
    return copied, unchanged, len(conflicts)


def build_parser() -> argparse.ArgumentParser:
    manifest = load_manifest()
    profiles = sorted(manifest["profiles"])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--profile", required=True, action="append", choices=profiles)
    parser.add_argument("--apply", action="store_true", help="perform copies; default is dry-run")
    parser.add_argument("--force", action="store_true", help="replace reviewed conflicting files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        copied, unchanged, conflicts = install(args.target, args.profile, apply=args.apply, force=args.force)
    except InstallError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    mode = "applied" if args.apply else "dry-run"
    print(f"{mode}: copy={copied} unchanged={unchanged} conflicts={conflicts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
