#!/usr/bin/env python3
"""Generate deterministic, untracked host packages from canonical Skills and reviewers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS_PATH = ROOT / "distribution" / "host-adapters.json"
MANIFEST_PATH = ROOT / "distribution" / "manifest.json"
MANAGED_BY = "dev-standard-host-generator"
IGNORED_PARTS = {"__pycache__"}


class HostAssetError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def adapters() -> dict[str, Any]:
    value = load_json(ADAPTERS_PATH)
    if value.get("schema_version") != 1 or not isinstance(value.get("hosts"), dict):
        raise HostAssetError("distribution/host-adapters.json is invalid")
    return value


def inventory() -> tuple[list[str], list[str]]:
    value = load_json(MANIFEST_PATH).get("inventory", {})
    skills = value.get("skills")
    reviewers = value.get("agents")
    if not isinstance(skills, list) or not isinstance(reviewers, list):
        raise HostAssetError("distribution manifest inventory is invalid")
    return sorted(map(str, skills)), sorted(map(str, reviewers))


def generated_root(config: dict[str, Any]) -> Path:
    root = (ROOT / str(config["generated_root"])).resolve(strict=False)
    if root == ROOT or ROOT not in root.parents:
        raise HostAssetError("generated host root must remain inside the repository")
    for parent in (ROOT, *root.parents):
        if parent == ROOT.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise HostAssetError(f"generated host ancestor is symlinked: {parent}")
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve(strict=True)


def iter_skill_files(skill_name: str, *, include_openai_metadata: bool) -> list[Path]:
    skill = ROOT / ".agents" / "skills" / skill_name
    if not (skill / "SKILL.md").is_file() or skill.is_symlink():
        raise HostAssetError(f"canonical Skill is missing or symlinked: {skill_name}")
    result: list[Path] = []
    for path in sorted(skill.rglob("*")):
        if not path.is_file() or path.is_symlink() or IGNORED_PARTS.intersection(path.parts) or path.suffix == ".pyc":
            continue
        if not include_openai_metadata and path.relative_to(skill).as_posix() == "agents/openai.yaml":
            continue
        result.append(path)
    return result


def render_claude_reviewer(path: Path) -> str:
    value = tomllib.loads(path.read_text(encoding="utf-8"))
    name = str(value.get("name", ""))
    description = str(value.get("description", ""))
    instructions = str(value.get("developer_instructions", "")).strip()
    if not name or not description or not instructions:
        raise HostAssetError(f"reviewer definition is incomplete: {path.relative_to(ROOT)}")
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "tools: Read, Grep, Glob\n"
        "---\n\n"
        f"{instructions}\n"
    )


def copy_file(source: Path, destination: Path, source_records: list[dict[str, str]]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    source_records.append({"path": source.relative_to(ROOT).as_posix(), "sha256": sha256(source)})


def populate(host: str, destination: Path, config: dict[str, Any]) -> None:
    host_config = config["hosts"].get(host)
    if not isinstance(host_config, dict):
        raise HostAssetError(f"unknown host: {host}")
    skills, reviewers = inventory()
    sources: list[dict[str, str]] = []
    include_openai_metadata = host == "codex"
    skill_destination = Path(str(host_config["skills_destination"]))
    for skill_name in skills:
        source_root = ROOT / ".agents" / "skills" / skill_name
        for source in iter_skill_files(skill_name, include_openai_metadata=include_openai_metadata):
            copy_file(source, destination / skill_destination / skill_name / source.relative_to(source_root), sources)

    reviewer_destination = destination / str(host_config["reviewers_destination"])
    reviewer_format = host_config.get("reviewer_format")
    for reviewer in reviewers:
        source = ROOT / ".codex" / "agents" / f"{reviewer}.toml"
        if not source.is_file() or source.is_symlink():
            raise HostAssetError(f"canonical reviewer is missing or symlinked: {reviewer}")
        if reviewer_format == "codex-toml":
            copy_file(source, reviewer_destination / source.name, sources)
        elif reviewer_format == "claude-markdown":
            reviewer_destination.mkdir(parents=True, exist_ok=True)
            (reviewer_destination / f"{reviewer}.md").write_text(render_claude_reviewer(source), encoding="utf-8", newline="\n")
            sources.append({"path": source.relative_to(ROOT).as_posix(), "sha256": sha256(source)})
        else:
            raise HostAssetError(f"unsupported reviewer format: {reviewer_format}")

    snippet = ROOT / str(config["canonical"]["instruction_snippet"])
    instruction_name = str(host_config["instruction_name"])
    instruction = snippet.read_text(encoding="utf-8").replace("`AGENTS.md`", f"`{instruction_name.removesuffix('.snippet.md')}.md`")
    (destination / instruction_name).write_text(instruction, encoding="utf-8", newline="\n")
    sources.append({"path": snippet.relative_to(ROOT).as_posix(), "sha256": sha256(snippet)})
    generated = sorted(path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file())
    manifest = {
        "schema_version": 1,
        "managed_by": MANAGED_BY,
        "host": host,
        "official_reference": host_config["official_reference"],
        "sources": sorted(sources, key=lambda item: item["path"]),
        "generated": generated,
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_existing(destination: Path, host: str) -> None:
    manifest_path = destination / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise HostAssetError(f"refusing to replace unmanaged generated host directory: {destination}")
    manifest = load_json(manifest_path)
    if manifest.get("managed_by") != MANAGED_BY or manifest.get("host") != host:
        raise HostAssetError(f"generated host manifest owner mismatch: {destination}")


def replace_directory(candidate: Path, destination: Path, host: str, root: Path) -> None:
    backup: Path | None = None
    if destination.exists():
        if destination.is_symlink() or not destination.is_dir():
            raise HostAssetError(f"generated host destination is unsafe: {destination}")
        validate_existing(destination, host)
        backup = Path(tempfile.mkdtemp(prefix=f".{host}.backup-", dir=root))
        backup.rmdir()
        os.replace(destination, backup)
    try:
        os.replace(candidate, destination)
    except Exception:
        if backup is not None and backup.exists() and not destination.exists():
            os.replace(backup, destination)
        raise
    if backup is not None and backup.exists():
        shutil.rmtree(backup)


def generate(host: str) -> Path:
    config = adapters()
    root = generated_root(config)
    destination = root / host
    candidate = Path(tempfile.mkdtemp(prefix=f".{host}.candidate-", dir=root))
    try:
        populate(host, candidate, config)
        replace_directory(candidate, destination, host, root)
    finally:
        if candidate.exists():
            shutil.rmtree(candidate)
    return destination


def file_snapshot(root: Path) -> dict[str, bytes]:
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def validate_no_tracked_generated(config: dict[str, Any]) -> None:
    forbidden = [str(config["generated_root"])]
    for name, host in config["hosts"].items():
        if name == "codex":
            continue
        forbidden.extend([str(host["skills_destination"]), str(host["reviewers_destination"])])
    result = subprocess.run(["git", "ls-files", "--", *sorted(set(forbidden))], cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        raise HostAssetError(f"git tracked-file inspection failed: {result.stderr.strip()}")
    tracked = [line for line in result.stdout.splitlines() if line]
    if tracked:
        raise HostAssetError("generated host assets must not be committed: " + ", ".join(tracked))


def check(hosts: list[str]) -> None:
    config = adapters()
    validate_no_tracked_generated(config)
    root = generated_root(config)
    for host in hosts:
        with tempfile.TemporaryDirectory(prefix=f".{host}.check-a-", dir=root) as first_dir, tempfile.TemporaryDirectory(prefix=f".{host}.check-b-", dir=root) as second_dir:
            first = Path(first_dir)
            second = Path(second_dir)
            populate(host, first, config)
            populate(host, second, config)
            if file_snapshot(first) != file_snapshot(second):
                raise HostAssetError(f"host generation is not deterministic: {host}")


def build_parser() -> argparse.ArgumentParser:
    config = adapters()
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    generate_parser = sub.add_parser("generate")
    generate_parser.add_argument("--host", action="append", choices=sorted(config["hosts"]), required=True)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--host", action="append", choices=sorted(config["hosts"]))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            for host in args.host:
                print(f"generated host assets: {generate(host)}")
        else:
            config = adapters()
            hosts = args.host or sorted(config["hosts"])
            check(hosts)
            print("host asset generation OK: " + ", ".join(hosts))
        return 0
    except (HostAssetError, OSError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
