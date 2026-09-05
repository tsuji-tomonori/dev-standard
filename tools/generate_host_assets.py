#!/usr/bin/env python3
"""Generate deterministic, untracked host packages from canonical Skills and reviewers."""

from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import tomllib
import uuid
from pathlib import Path
from typing import Any

try:
    from tools import safe_io
except ModuleNotFoundError:  # Direct execution.
    import safe_io  # type: ignore[no-redef]

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
    if value.get("schema_version") != 3 or not isinstance(value.get("hosts"), dict):
        raise HostAssetError("distribution/host-adapters.json is invalid")
    runtime = value.get("portable_runtime")
    manifest_runtime = load_json(MANIFEST_PATH).get("portable_runtime")
    if (
        not isinstance(runtime, dict)
        or not isinstance(manifest_runtime, dict)
        or runtime.get("manifest_key") != "portable_runtime"
        or runtime.get("quint_version") != manifest_runtime.get("quint_version")
        or runtime.get("host_independent") is not True
    ):
        raise HostAssetError("portable runtime host contract is invalid")
    return value


def inventory() -> tuple[list[str], list[str]]:
    value = load_json(MANIFEST_PATH).get("inventory", {})
    skills = value.get("skills")
    reviewers = value.get("agents")
    if not isinstance(skills, list) or not isinstance(reviewers, list):
        raise HostAssetError("distribution manifest inventory is invalid")
    return sorted(map(str, skills)), sorted(map(str, reviewers))


def generated_root(config: dict[str, Any]) -> Path:
    relative = Path(str(config["generated_root"]))
    if relative.is_absolute() or ".." in relative.parts or relative in {Path(""), Path(".")}:
        raise HostAssetError("generated host root must remain inside the repository")
    root = ROOT / relative
    try:
        with safe_io.directory_nofollow(root, root=ROOT, create=True):
            pass
    except safe_io.SafeIOError as exc:
        raise HostAssetError(f"generated host root is unsafe: {exc}") from exc
    return root


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

    distribution = load_json(MANIFEST_PATH)
    runtime = distribution.get("portable_runtime")
    formal = distribution.get("formal_skill_contracts")
    support = distribution.get("skill_runner_support")
    dependency_runtime = (
        support.get("dependency_runtime") if isinstance(support, dict) else None
    )
    if (
        not isinstance(runtime, dict)
        or not isinstance(runtime.get("mappings"), list)
        or not isinstance(formal, dict)
        or not isinstance(formal.get("mappings"), list)
        or not isinstance(dependency_runtime, dict)
    ):
        raise HostAssetError("portable runtime mappings are invalid")
    runner = runtime.get("runner")
    dependency_runner = dependency_runtime.get("runner")
    if not isinstance(runner, dict) or not isinstance(dependency_runner, dict):
        raise HostAssetError("portable runner mapping is invalid")
    mappings = [
        *formal["mappings"],
        *runtime["mappings"],
        runner,
        dependency_runner,
    ]
    for current_runner, required_modules in [
        (runner, {"safe_io", "spec_mapping", "render_requirements", "render_skills"}),
        (dependency_runner, {"safe_io"}),
    ]:
        runner_source = ROOT / str(current_runner.get("source"))
        try:
            tree = ast.parse(runner_source.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            raise HostAssetError(f"cannot derive portable runner imports: {exc}") from exc
        local_modules: set[str] = set()
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_load_pinned_tool"
                and len(node.args) == 1
            ):
                try:
                    name = ast.literal_eval(node.args[0])
                except (ValueError, TypeError):
                    raise HostAssetError("portable runner pinned import must be static") from None
                if not isinstance(name, str) or not name.isidentifier():
                    raise HostAssetError("portable runner pinned import name is invalid")
                local_modules.add(name)
        if local_modules != required_modules:
            raise HostAssetError("portable runner local import closure is incomplete")
        mappings.extend(
            {"source": f"tools/{name}.py", "destination": f"tools/{name}.py"}
            for name in sorted(local_modules)
        )
    unique_mappings: dict[str, dict[str, Any]] = {}
    for mapping in mappings:
        if not isinstance(mapping, dict) or "destination" not in mapping:
            raise HostAssetError("portable runtime mapping is invalid")
        destination_text = str(mapping["destination"])
        previous = unique_mappings.get(destination_text)
        if previous is not None and previous.get("source") != mapping.get("source"):
            raise HostAssetError(f"portable runtime mapping collision: {destination_text}")
        unique_mappings[destination_text] = mapping
    for mapping in unique_mappings.values():
        allowed = {"source", "destination"}
        if mapping is runner or mapping is dependency_runner:
            allowed.add("local_imports")
        if not isinstance(mapping, dict) or set(mapping) != allowed:
            raise HostAssetError("portable runtime mapping is invalid")
        source = ROOT / str(mapping["source"])
        if not source.is_file() or source.is_symlink():
            raise HostAssetError(f"portable runtime source is unsafe: {mapping['source']}")
        destination_path = Path(str(mapping["destination"]))
        if destination_path.is_absolute() or ".." in destination_path.parts:
            raise HostAssetError(f"portable runtime destination is unsafe: {mapping['destination']}")
        copy_file(source, destination / destination_path, sources)

    generated = sorted(path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file())
    manifest = {
        "schema_version": 1,
        "managed_by": MANAGED_BY,
        "host": host,
        "quint_version": runtime["quint_version"],
        "interface_policy": host_config["interface_policy"],
        "official_reference": host_config["official_reference"],
        "sources": sorted(sources, key=lambda item: item["path"]),
        "generated": generated,
    }
    (destination / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # A generated archive is directly runnable after the adopter initializes
    # requirements.qnt from the included template. Bind the exact package just
    # like install_reference does; no repository CI or merge settings appear.
    asset_paths = sorted(
        path
        for path in destination.rglob("*")
        if path.is_file() and ".dev-standard/install" not in path.relative_to(destination).as_posix()
    )
    assets = [
        {
            "path": path.relative_to(destination).as_posix(),
            "sha256": sha256(path),
        }
        for path in asset_paths
    ]
    receipt = {
        "schema_version": 2,
        "managed_by": "dev-standard-reference-installer",
        "host": host,
        "interface_policy": host_config["interface_policy"],
        "profiles": ["full"],
        "skills": skills,
        "quint_version": runtime["quint_version"],
        "assets": assets,
    }
    receipt_bytes = (
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    commitment = {
        "schema_version": 2,
        "managed_by": "dev-standard-reference-installer",
        "receipt": ".dev-standard/install/receipt.json",
        "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "assets_sha256": hashlib.sha256(
            (
                json.dumps(assets, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode()
        ).hexdigest(),
    }
    metadata = destination / ".dev-standard/install"
    metadata.mkdir(parents=True)
    (metadata / "receipt.json").write_bytes(receipt_bytes)
    (metadata / "commitment.json").write_text(
        json.dumps(commitment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_existing(
    destination: Path,
    host: str,
    *,
    root: Path | None = None,
    root_fd: int | None = None,
) -> None:
    manifest_path = destination / "manifest.json"
    try:
        content = (
            safe_io.read_bytes_nofollow_pinned(
                manifest_path, root=root, root_fd=root_fd
            )
            if root is not None and root_fd is not None
            else safe_io.read_bytes_nofollow(manifest_path, root=destination)
        )
        manifest = json.loads(content)
    except (OSError, json.JSONDecodeError, safe_io.SafeIOError) as exc:
        raise HostAssetError(
            f"refusing to replace unmanaged generated host directory: {destination}: {exc}"
        ) from exc
    if manifest.get("managed_by") != MANAGED_BY or manifest.get("host") != host:
        raise HostAssetError(f"generated host manifest owner mismatch: {destination}")


def replace_directory(candidate: Path, destination: Path, host: str, root: Path) -> None:
    backup_name: str | None = None
    with safe_io.trusted_root(root) as root_fd, safe_io.locked_repository_pinned(
        root, root_fd, f".{host}.generation.lock"
    ):
        try:
            destination_info = os.stat(host, dir_fd=root_fd, follow_symlinks=False)
        except FileNotFoundError:
            destination_info = None
        if destination_info is not None:
            if not stat.S_ISDIR(destination_info.st_mode) or stat.S_ISLNK(destination_info.st_mode):
                raise HostAssetError(f"generated host destination is unsafe: {destination}")
            safe_io.tree_digest_nofollow_pinned(
                destination, root=root, root_fd=root_fd
            )
            validate_existing(destination, host, root=root, root_fd=root_fd)
            backup_name = f".{host}.backup-{uuid.uuid4().hex}"
            os.rename(host, backup_name, src_dir_fd=root_fd, dst_dir_fd=root_fd)
        try:
            os.rename(candidate.name, host, src_dir_fd=root_fd, dst_dir_fd=root_fd)
            os.fsync(root_fd)
        except BaseException:
            if backup_name is not None:
                with contextlib.suppress(FileNotFoundError):
                    os.rename(backup_name, host, src_dir_fd=root_fd, dst_dir_fd=root_fd)
                    os.fsync(root_fd)
            raise
        if backup_name is not None:
            safe_io.remove_tree_nofollow(
                root / backup_name, root=root, pinned_root_fd=root_fd
            )


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
            safe_io.remove_tree_nofollow(candidate, root=root)
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
    package_parser = sub.add_parser("package")
    package_parser.add_argument("--host", choices=sorted(config["hosts"]), required=True)
    package_parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            for host in args.host:
                print(f"generated host assets: {generate(host)}")
        elif args.command == "check":
            config = adapters()
            hosts = args.host or sorted(config["hosts"])
            check(hosts)
            print("host asset generation OK: " + ", ".join(hosts))
        else:
            output = args.output if args.output.is_absolute() else Path.cwd() / args.output
            if output.exists():
                raise HostAssetError(f"package output must not already exist: {output}")
            output.mkdir(parents=True)
            populate(args.host, output, adapters())
            print(f"generated host package: {output}")
        return 0
    except (HostAssetError, OSError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
