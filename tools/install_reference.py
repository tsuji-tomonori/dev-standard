#!/usr/bin/env python3
"""Safely copy selected reference assets into another repository."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "distribution" / "manifest.json"
IGNORED_PARTS = {"__pycache__"}
HOST_ADAPTERS = ROOT / "distribution" / "host-adapters.json"
INSTRUCTION_PROFILES = {"default", "chat-first", "development-framework", "frontend-development", "full", "skills"}
INSTRUCTION_START = "<!-- dev-standard:begin -->"
INSTRUCTION_END = "<!-- dev-standard:end -->"


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class CopyItem:
    source: Path
    destination: Path


def load_manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_host_adapters() -> dict[str, object]:
    return json.loads(HOST_ADAPTERS.read_text(encoding="utf-8"))


def prepare_host_source(host: str) -> Path:
    adapters = load_host_adapters()
    hosts = adapters.get("hosts")
    if not isinstance(hosts, dict) or host not in hosts:
        raise InstallError(f"unknown host: {host}")
    if host == "codex":
        return ROOT
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "generate_host_assets.py"), "generate", "--host", host],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise InstallError(f"host asset generation failed: {(result.stdout + result.stderr).strip()}")
    generated = ROOT / str(adapters["generated_root"]) / host
    if not generated.is_dir():
        raise InstallError(f"generated host package is missing: {host}")
    return generated


def safe_source(relative: str) -> Path:
    source = (ROOT / relative).resolve()
    if source != ROOT and ROOT not in source.parents:
        raise InstallError(f"source escapes repository: {relative}")
    if not source.exists() or source.is_symlink():
        raise InstallError(f"source is missing or symlinked: {relative}")
    return source


def host_mapping(host: str, source_text: str, destination_text: str, host_source: Path) -> tuple[Path, str]:
    adapters = load_host_adapters()
    host_config = adapters["hosts"][host]
    if source_text == ".agents/skills" or source_text.startswith(".agents/skills/"):
        suffix = source_text.removeprefix(".agents/skills").lstrip("/")
        source = host_source / str(host_config["skills_destination"]) / suffix
        destination = str(Path(str(host_config["skills_destination"])) / suffix)
        return source, destination
    if source_text == ".codex/agents" or source_text.startswith(".codex/agents/"):
        suffix = source_text.removeprefix(".codex/agents").lstrip("/")
        source = host_source / str(host_config["reviewers_destination"]) / suffix
        destination = str(Path(str(host_config["reviewers_destination"])) / suffix)
        return source, destination
    return safe_source(source_text), destination_text


def expand_mapping(target: Path, source_text: str, destination_text: str, *, host: str, host_source: Path) -> list[CopyItem]:
    source, destination_text = host_mapping(host, source_text, destination_text, host_source)
    source = source.resolve()
    allowed_roots = {ROOT.resolve(), host_source.resolve()}
    if not any(source == allowed or allowed in source.parents for allowed in allowed_roots):
        raise InstallError(f"host source escapes package: {source_text}")
    if not source.exists() or source.is_symlink():
        raise InstallError(f"source is missing or symlinked: {source_text}")
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


def plan(target: Path, profiles: list[str], manifest: dict[str, object], *, host: str = "codex") -> list[CopyItem]:
    profile_map = manifest.get("profiles")
    if not isinstance(profile_map, dict):
        raise InstallError("manifest profiles are invalid")
    host_source = prepare_host_source(host)
    items: dict[Path, CopyItem] = {}
    for profile in profiles:
        mappings = profile_map.get(profile)
        if not isinstance(mappings, list):
            raise InstallError(f"unknown profile: {profile}")
        for mapping in mappings:
            if not isinstance(mapping, dict):
                raise InstallError(f"invalid mapping in profile: {profile}")
            for item in expand_mapping(target, str(mapping["source"]), str(mapping["destination"]), host=host, host_source=host_source):
                previous = items.get(item.destination)
                if previous and previous.source != item.source:
                    raise InstallError(f"multiple sources target: {item.destination}")
                items[item.destination] = item
    return [items[path] for path in sorted(items)]


def instruction_path(target: Path, host: str) -> Path:
    return target / ("AGENTS.md" if host == "codex" else "CLAUDE.md")


def merged_instructions(existing: str, snippet: str) -> str:
    block = f"{INSTRUCTION_START}\n{snippet.strip()}\n{INSTRUCTION_END}"
    has_start = INSTRUCTION_START in existing
    has_end = INSTRUCTION_END in existing
    if has_start != has_end:
        raise InstallError("existing instruction integration marker is incomplete")
    if has_start:
        before, remainder = existing.split(INSTRUCTION_START, 1)
        _, after = remainder.split(INSTRUCTION_END, 1)
        return (before.rstrip() + "\n\n" + block + "\n" + after.lstrip()).rstrip() + "\n"
    if not existing.strip():
        return block + "\n"
    return existing.rstrip() + "\n\n" + block + "\n"


def integrate_instructions(target: Path, host: str, *, apply: bool) -> bool:
    path = instruction_path(target, host)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    snippet = (ROOT / "distribution" / "snippets" / "AGENTS.governance.md").read_text(encoding="utf-8")
    snippet = snippet.replace("`AGENTS.md`", f"`{path.name}`")
    merged = merged_instructions(existing, snippet)
    if existing == merged:
        print(f"UNCHANGED {path}")
        return False
    print(f"{'UPDATE' if apply else 'WOULD_UPDATE'} {path}")
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(merged, encoding="utf-8", newline="\n")
    return True


def install(target: Path, profiles: list[str], *, apply: bool, force: bool, host: str = "codex") -> tuple[int, int, int]:
    target = target.resolve()
    if target in {Path("/"), Path.home().resolve()}:
        raise InstallError("target must be a repository directory, not root or home")
    if not target.is_dir():
        raise InstallError(f"target directory does not exist: {target}")
    if INSTRUCTION_PROFILES.intersection(profiles):
        path = instruction_path(target, host)
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        snippet = (ROOT / "distribution" / "snippets" / "AGENTS.governance.md").read_text(encoding="utf-8")
        snippet = snippet.replace("`AGENTS.md`", f"`{path.name}`")
        merged_instructions(existing, snippet)
    items = plan(target, profiles, load_manifest(), host=host)
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
    if INSTRUCTION_PROFILES.intersection(profiles) and integrate_instructions(target, host, apply=apply):
        copied += 1
    return copied, unchanged, len(conflicts)


def build_parser() -> argparse.ArgumentParser:
    manifest = load_manifest()
    profiles = sorted(manifest["profiles"])
    hosts = sorted(load_host_adapters()["hosts"])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--profile", required=True, action="append", choices=profiles)
    parser.add_argument("--host", choices=hosts, default="codex")
    parser.add_argument("--apply", action="store_true", help="perform copies; default is dry-run")
    parser.add_argument("--force", action="store_true", help="replace reviewed conflicting files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        copied, unchanged, conflicts = install(args.target, args.profile, apply=args.apply, force=args.force, host=args.host)
    except InstallError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    mode = "applied" if args.apply else "dry-run"
    print(f"{mode}: copy={copied} unchanged={unchanged} conflicts={conflicts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
