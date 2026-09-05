#!/usr/bin/env python3
"""Safely copy selected reference assets into another repository."""

from __future__ import annotations

import argparse
import ast
import atexit
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

try:
    from tools import safe_io
except ModuleNotFoundError:  # Direct `python tools/install_reference.py` execution.
    import safe_io  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "distribution" / "manifest.json"
IGNORED_PARTS = {"__pycache__"}
HOST_ADAPTERS = ROOT / "distribution" / "host-adapters.json"
INSTRUCTION_PROFILES = {"default", "chat-first", "development-framework", "frontend-development", "full", "skills"}
INSTRUCTION_START = "<!-- dev-standard:begin -->"
INSTRUCTION_END = "<!-- dev-standard:end -->"
_TEMP_HOST_PACKAGES: list[tempfile.TemporaryDirectory[str]] = []


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class CopyItem:
    source: Path
    destination: Path
    source_root: Path
    mode: int


def load_manifest() -> dict[str, object]:
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if value.get("schema_version") != 4:
        raise InstallError("distribution manifest schema is invalid")
    return value


def load_host_adapters() -> dict[str, object]:
    return json.loads(HOST_ADAPTERS.read_text(encoding="utf-8"))


def prepare_host_source(host: str) -> Path:
    adapters = load_host_adapters()
    hosts = adapters.get("hosts")
    if not isinstance(hosts, dict) or host not in hosts:
        raise InstallError(f"unknown host: {host}")
    if host == "codex":
        return ROOT
    temporary = tempfile.TemporaryDirectory(prefix=f"dev-standard-{host}-package-")
    _TEMP_HOST_PACKAGES.append(temporary)
    atexit.register(temporary.cleanup)
    generated = Path(temporary.name) / host
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "generate_host_assets.py"),
            "package",
            "--host",
            host,
            "--output",
            str(generated),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise InstallError(f"host asset generation failed: {(result.stdout + result.stderr).strip()}")
    if not generated.is_dir():
        raise InstallError(f"generated host package is missing: {host}")
    return generated


def _mapping(value: object, label: str) -> tuple[str, str]:
    if not isinstance(value, dict) or set(value) != {"source", "destination"}:
        raise InstallError(f"{label} mapping is invalid")
    return str(value["source"]), str(value["destination"])


def _protected(destination: str, manifest: dict[str, object]) -> bool:
    path = PurePosixPath(destination).as_posix()
    while path.startswith("./"):
        path = path[2:]
    if path in {"", "."}:
        return True
    patterns = manifest.get("protected_repository_paths")
    if not isinstance(patterns, list) or not all(isinstance(value, str) for value in patterns):
        raise InstallError("protected repository path denylist is invalid")
    for pattern in patterns:
        prefix = pattern.removesuffix("/**")
        if (
            path == prefix
            or path.startswith(prefix + "/")
            or prefix.startswith(path.rstrip("/") + "/")
            or PurePosixPath(path).match(pattern)
        ):
            return True
    return False


def _runner_local_modules(
    source: Path,
    *,
    required: frozenset[str] = frozenset(
        {"safe_io", "spec_mapping", "render_requirements", "render_skills"}
    ),
) -> list[str]:
    """Derive the portable runner's local import closure from pinned-load calls."""

    try:
        tree = ast.parse(source.read_text(encoding="utf-8"))
    except (OSError, SyntaxError) as exc:
        raise InstallError(f"cannot inspect portable runner import closure: {exc}") from exc
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id != "_load_pinned_tool" or len(node.args) != 1:
            continue
        try:
            name = ast.literal_eval(node.args[0])
        except (ValueError, TypeError):
            raise InstallError("portable runner has a dynamic pinned tool import") from None
        if not isinstance(name, str) or not name.isidentifier():
            raise InstallError(f"portable runner has an invalid pinned tool import: {name!r}")
        names.add(name)
    if names != required:
        raise InstallError(
            f"portable runner import closure drift: missing={sorted(required - names)} "
            f"extra={sorted(names - required)}"
        )
    return sorted(names)


def _dependency_runtime(
    manifest: dict[str, object], selected_skills: list[str]
) -> dict[str, object] | None:
    """Return the isolated Python runtime contract when a selected Skill needs it."""

    support = manifest.get("skill_runner_support")
    runtime = support.get("dependency_runtime") if isinstance(support, dict) else None
    if (
        not isinstance(runtime, dict)
        or set(runtime) != {"schema_version", "activation", "runtime_root", "runner"}
        or runtime.get("schema_version") != 1
        or runtime.get("activation") != "selected-skill-has-requirements.txt"
        or runtime.get("runtime_root") != ".dev-standard/python/runtime"
    ):
        raise InstallError("Skill dependency runtime contract is invalid")
    active = False
    for name in selected_skills:
        relative = f".agents/skills/{name}/requirements.txt"
        path = ROOT / relative
        try:
            info = os.lstat(path)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise InstallError(f"Skill requirements are unsafe: {relative}")
        safe_io.read_bytes_nofollow(path, root=ROOT)
        active = True
    return runtime if active else None


def _skill_runner_modules(
    manifest: dict[str, object], selected_skills: list[str]
) -> list[str]:
    """Derive repository-root tool dependencies from selected Skill scripts."""

    support = manifest.get("skill_runner_support")
    if (
        not isinstance(support, dict)
        or support.get("schema_version") != 1
        or support.get("activation") != "derive-from-selected-skill-python-sources"
        or support.get("module_destination") != "tools/<module>.py"
        or not isinstance(support.get("allowed_modules"), list)
    ):
        raise InstallError("Skill runner support contract is invalid")
    allowed = set(map(str, support["allowed_modules"]))
    discovered: set[str] = set()
    for name in selected_skills:
        scripts = ROOT / ".agents/skills" / name / "scripts"
        if not scripts.exists():
            continue
        for path in sorted(scripts.rglob("*.py")):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"))
            except (OSError, SyntaxError) as exc:
                raise InstallError(f"cannot inspect Skill runner dependency {path}: {exc}") from exc
            constants = {
                node.value
                for node in ast.walk(tree)
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
            }
            for module in allowed:
                if (
                    f"{module}.py" in constants
                    or f"tools/{module}.py" in constants
                    or any(
                        isinstance(node, ast.ImportFrom)
                        and node.module == "tools"
                        and any(alias.name == module for alias in node.names)
                        for node in ast.walk(tree)
                    )
                    or any(
                        isinstance(node, ast.Import)
                        and any(alias.name == f"tools.{module}" for alias in node.names)
                        for node in ast.walk(tree)
                    )
                ):
                    discovered.add(module)
    missing = [name for name in discovered if not (ROOT / "tools" / f"{name}.py").is_file()]
    if missing:
        raise InstallError(f"Skill runner support modules are missing: {sorted(missing)}")
    return sorted(discovered)


def _selected_skills(manifest: dict[str, object], profiles: list[str]) -> list[str]:
    profile_map = manifest.get("profiles")
    inventory = manifest.get("inventory")
    if not isinstance(profile_map, dict) or not isinstance(inventory, dict):
        raise InstallError("manifest profiles or inventory are invalid")
    known = set(map(str, inventory.get("skills", [])))
    selected: set[str] = set()
    for profile in profiles:
        mappings = profile_map.get(profile)
        if not isinstance(mappings, list):
            raise InstallError(f"unknown profile: {profile}")
        for value in mappings:
            source, _ = _mapping(value, profile)
            if source == ".agents/skills":
                selected.update(known)
            elif source.startswith(".agents/skills/"):
                name = PurePosixPath(source).parts[2]
                if name not in known:
                    raise InstallError(f"profile references an unknown Skill: {name}")
                selected.add(name)

    try:
        catalog = json.loads((ROOT / "spec/skills/skills.json").read_text(encoding="utf-8"))
        contracts = {item["name"]: item for item in catalog["contracts"]}
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise InstallError(f"formal Skill contract view is invalid: {exc}") from exc
    if set(contracts) != known:
        raise InstallError("Skill inventory and formal contracts differ")
    pending = list(selected)
    while pending:
        name = pending.pop()
        dependencies = contracts[name].get("dependencies")
        if not isinstance(dependencies, list) or not all(value in contracts for value in dependencies):
            raise InstallError(f"{name}: formal Skill dependency closure is invalid")
        for dependency in dependencies:
            if dependency not in selected:
                selected.add(dependency)
                pending.append(dependency)
    return sorted(selected)


def safe_source(relative: str) -> Path:
    relative_path = Path(relative)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise InstallError(f"source escapes repository: {relative}")
    source = ROOT / relative_path
    try:
        info = os.lstat(source)
    except FileNotFoundError as exc:
        raise InstallError(f"source is missing: {relative}") from exc
    if stat.S_ISLNK(info.st_mode):
        raise InstallError(f"source is missing or symlinked: {relative}")
    return source


def host_mapping(
    host: str,
    source_text: str,
    destination_text: str,
    host_source: Path,
) -> tuple[Path, str, Path]:
    adapters = load_host_adapters()
    host_config = adapters["hosts"][host]
    if source_text == ".agents/skills" or source_text.startswith(".agents/skills/"):
        suffix = source_text.removeprefix(".agents/skills").lstrip("/")
        source = host_source / str(host_config["skills_destination"]) / suffix
        destination = str(Path(str(host_config["skills_destination"])) / suffix)
        return source, destination, host_source
    if source_text == ".codex/agents" or source_text.startswith(".codex/agents/"):
        suffix = source_text.removeprefix(".codex/agents").lstrip("/")
        source = host_source / str(host_config["reviewers_destination"]) / suffix
        destination = str(Path(str(host_config["reviewers_destination"])) / suffix)
        return source, destination, host_source
    return safe_source(source_text), destination_text, ROOT


def expand_mapping(target: Path, source_text: str, destination_text: str, *, host: str, host_source: Path) -> list[CopyItem]:
    source, destination_text, source_root = host_mapping(host, source_text, destination_text, host_source)
    try:
        source.relative_to(source_root)
    except ValueError as exc:
        raise InstallError(f"host source escapes package: {source_text}") from exc
    try:
        source_info = os.lstat(source)
    except FileNotFoundError as exc:
        raise InstallError(f"source is missing: {source_text}") from exc
    if stat.S_ISLNK(source_info.st_mode):
        raise InstallError(f"host source escapes package: {source_text}")
    destination_relative = Path(destination_text)
    if destination_relative.is_absolute() or ".." in destination_relative.parts:
        raise InstallError(f"destination escapes target repository: {destination_text}")
    destination = target / destination_relative
    if source.is_file():
        safe_io.read_bytes_nofollow(source, root=source_root)
        return [CopyItem(source, destination, source_root, stat.S_IMODE(source_info.st_mode))]
    safe_io.validate_tree_nofollow(source, root=source_root)
    items: list[CopyItem] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file() or path.is_symlink() or IGNORED_PARTS.intersection(path.parts) or path.suffix == ".pyc":
            continue
        if path.parent.name == "reviews" and path.name.startswith("CHG-") and path.suffix in {".yaml", ".yml"}:
            continue
        info = os.lstat(path)
        items.append(
            CopyItem(
                path,
                destination / path.relative_to(source),
                source_root,
                stat.S_IMODE(info.st_mode),
            )
        )
    return items


def plan(target: Path, profiles: list[str], manifest: dict[str, object], *, host: str = "codex") -> list[CopyItem]:
    profile_map = manifest.get("profiles")
    if not isinstance(profile_map, dict):
        raise InstallError("manifest profiles are invalid")
    host_source = prepare_host_source(host)
    selected_skills = _selected_skills(manifest, profiles)
    items: dict[Path, CopyItem] = {}
    for profile in profiles:
        mappings = profile_map.get(profile)
        if not isinstance(mappings, list):
            raise InstallError(f"unknown profile: {profile}")
        for mapping in mappings:
            source_text, destination_text = _mapping(mapping, profile)
            if _protected(destination_text, manifest):
                raise InstallError(f"profile destination is repository-policy protected: {destination_text}")
            for item in expand_mapping(target, source_text, destination_text, host=host, host_source=host_source):
                previous = items.get(item.destination)
                if previous and previous.source != item.source:
                    raise InstallError(f"multiple sources target: {item.destination}")
                items[item.destination] = item
    # Profiles describe their entry Skills; formal dependencies are closed from
    # the Quint-derived contract rather than duplicated in JSON profile lists.
    for name in selected_skills:
        destination = f".agents/skills/{name}"
        for item in expand_mapping(
            target,
            destination,
            destination,
            host=host,
            host_source=host_source,
        ):
            previous = items.get(item.destination)
            if previous and previous.source != item.source:
                raise InstallError(f"multiple sources target: {item.destination}")
            items[item.destination] = item

    formal = manifest.get("formal_skill_contracts")
    if selected_skills:
        if not isinstance(formal, dict) or formal.get("activation") != "every-profile-containing-a-skill":
            raise InstallError("formal Skill distribution contract is invalid")
        for mapping in formal.get("mappings", []):
            source_text, destination_text = _mapping(mapping, "formal Skill contract")
            if _protected(destination_text, manifest):
                raise InstallError(f"formal contract destination is protected: {destination_text}")
            for item in expand_mapping(
                target,
                source_text,
                destination_text,
                host=host,
                host_source=host_source,
            ):
                previous = items.get(item.destination)
                if previous and previous.source != item.source:
                    raise InstallError(f"multiple sources target: {item.destination}")
                items[item.destination] = item

    for module in _skill_runner_modules(manifest, selected_skills):
        for item in expand_mapping(
            target,
            f"tools/{module}.py",
            f"tools/{module}.py",
            host=host,
            host_source=host_source,
        ):
            previous = items.get(item.destination)
            if previous and previous.source != item.source:
                raise InstallError(f"multiple sources target: {item.destination}")
            items[item.destination] = item

    dependency_runtime = _dependency_runtime(manifest, selected_skills)
    if dependency_runtime is not None:
        runner = dependency_runtime.get("runner")
        if (
            not isinstance(runner, dict)
            or set(runner) != {"source", "destination", "local_imports"}
            or runner.get("local_imports")
            != "derive-from-_load_pinned_tool-calls"
        ):
            raise InstallError("Skill dependency runner mapping is invalid")
        runner_source = str(runner["source"])
        mappings = [(runner_source, str(runner["destination"]))]
        mappings.extend(
            (f"tools/{name}.py", f"tools/{name}.py")
            for name in _runner_local_modules(
                ROOT / runner_source, required=frozenset({"safe_io"})
            )
        )
        for source_text, destination_text in mappings:
            if _protected(destination_text, manifest):
                raise InstallError(
                    f"Skill dependency runtime destination is protected: {destination_text}"
                )
            for item in expand_mapping(
                target,
                source_text,
                destination_text,
                host=host,
                host_source=host_source,
            ):
                previous = items.get(item.destination)
                if previous and previous.source != item.source:
                    raise InstallError(f"multiple sources target: {item.destination}")
                items[item.destination] = item

    runtime = manifest.get("portable_runtime")
    if not isinstance(runtime, dict) or runtime.get("schema_version") != 2:
        raise InstallError("portable runtime manifest is invalid")
    activation = runtime.get("activation_skill")
    if not isinstance(activation, str):
        raise InstallError("portable runtime activation Skill is invalid")
    if activation in selected_skills:
        runner = runtime.get("runner")
        if (
            not isinstance(runner, dict)
            or set(runner) != {"source", "destination", "local_imports"}
            or runner.get("local_imports") != "derive-from-_load_pinned_tool-calls"
        ):
            raise InstallError("portable runner mapping is invalid")
        runner_source = str(runner["source"])
        runner_destination = str(runner["destination"])
        runtime_mappings = runtime.get("mappings")
        if not isinstance(runtime_mappings, list):
            raise InstallError("portable runtime mappings are invalid")
        mappings: list[tuple[str, str]] = [(runner_source, runner_destination)]
        mappings.extend(_mapping(value, "portable runtime") for value in runtime_mappings)
        mappings.extend(
            (f"tools/{name}.py", f"tools/{name}.py")
            for name in _runner_local_modules(ROOT / runner_source)
        )
        for source_text, destination_text in mappings:
            if _protected(destination_text, manifest):
                raise InstallError(f"runtime destination is protected: {destination_text}")
            for item in expand_mapping(
                target,
                source_text,
                destination_text,
                host=host,
                host_source=host_source,
            ):
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
        prefix = before.rstrip()
        suffix = after.lstrip()
        return (
            (prefix + "\n\n" if prefix else "")
            + block
            + ("\n" + suffix if suffix else "\n")
        ).rstrip() + "\n"
    if not existing.strip():
        return block + "\n"
    return existing.rstrip() + "\n\n" + block + "\n"


def integrate_instructions(target: Path, host: str, *, apply: bool) -> bool:
    path = instruction_path(target, host)
    before = safe_io.snapshot_file(path, root=target)
    existing = safe_io.read_bytes_nofollow(path, root=target).decode("utf-8") if before.exists else ""
    snippet = safe_io.read_bytes_nofollow(
        ROOT / "distribution" / "snippets" / "AGENTS.governance.md",
        root=ROOT,
    ).decode("utf-8")
    snippet = snippet.replace("`AGENTS.md`", f"`{path.name}`")
    merged = merged_instructions(existing, snippet)
    if existing == merged:
        print(f"UNCHANGED {path}")
        return False
    print(f"{'UPDATE' if apply else 'WOULD_UPDATE'} {path}")
    if apply:
        safe_io.atomic_write_cas(path, merged.encode("utf-8"), before, root=target)
    return True


def _installation_records(
    target: Path,
    profiles: list[str],
    host: str,
    managed_assets: dict[Path, bytes],
    runtime_version: str | None,
    skills: list[str],
) -> dict[Path, bytes]:
    adapters = load_host_adapters()
    host_config = adapters["hosts"][host]
    assets = [
        {
            "path": path.relative_to(target).as_posix(),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        for path, content in sorted(managed_assets.items(), key=lambda item: str(item[0]))
    ]
    receipt = {
        "schema_version": 2,
        "managed_by": "dev-standard-reference-installer",
        "host": host,
        "interface_policy": host_config["interface_policy"],
        "profiles": sorted(set(profiles)),
        "skills": skills,
        "quint_version": runtime_version,
        "assets": assets,
    }
    receipt_bytes = (json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    commitment = {
        "schema_version": 2,
        "managed_by": "dev-standard-reference-installer",
        "receipt": ".dev-standard/install/receipt.json",
        "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest(),
        "assets_sha256": hashlib.sha256(
            (json.dumps(assets, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        ).hexdigest(),
    }
    return {
        target / ".dev-standard" / "install" / "receipt.json": receipt_bytes,
        target / ".dev-standard" / "install" / "commitment.json": (
            json.dumps(commitment, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8"),
    }


def _parse_metadata_file(content: bytes, path: Path) -> dict[str, object]:
    try:
        value = json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise InstallError(f"installer metadata is invalid: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise InstallError(f"installer metadata must be an object: {path}")
    return value


def _validate_existing_metadata(
    target: Path,
    root_fd: int,
    requested_profiles: list[str],
    host: str,
) -> list[Path]:
    """Validate commitment -> receipt -> every recorded asset before upgrade."""

    commitment_path = target / ".dev-standard/install/commitment.json"
    receipt_path = target / ".dev-standard/install/receipt.json"
    commitment_snapshot = safe_io.snapshot_file_pinned(commitment_path, root=target, root_fd=root_fd)
    receipt_snapshot = safe_io.snapshot_file_pinned(receipt_path, root=target, root_fd=root_fd)
    if commitment_snapshot.exists != receipt_snapshot.exists:
        raise InstallError("installer metadata is incomplete; commitment and receipt must coexist")
    if not commitment_snapshot.exists:
        return []
    commitment_bytes = safe_io.read_bytes_nofollow_pinned(
        commitment_path, root=target, root_fd=root_fd
    )
    receipt_bytes = safe_io.read_bytes_nofollow_pinned(receipt_path, root=target, root_fd=root_fd)
    commitment = _parse_metadata_file(commitment_bytes, commitment_path)
    receipt = _parse_metadata_file(receipt_bytes, receipt_path)
    if set(commitment) != {
        "schema_version",
        "managed_by",
        "receipt",
        "receipt_sha256",
        "assets_sha256",
    } or commitment.get("schema_version") != 2:
        raise InstallError("existing installer commitment schema is invalid")
    if (
        commitment.get("managed_by") != "dev-standard-reference-installer"
        or commitment.get("receipt") != ".dev-standard/install/receipt.json"
        or commitment.get("receipt_sha256") != hashlib.sha256(receipt_bytes).hexdigest()
    ):
        raise InstallError("existing installer commitment does not bind the receipt")
    if set(receipt) != {
        "schema_version",
        "managed_by",
        "host",
        "interface_policy",
        "profiles",
        "skills",
        "quint_version",
        "assets",
    } or receipt.get("schema_version") != 2:
        raise InstallError("existing installer receipt schema is invalid")
    if receipt.get("managed_by") != "dev-standard-reference-installer":
        raise InstallError("existing installer receipt owner is invalid")
    if receipt.get("host") != host:
        raise InstallError("changing an installed host adapter in place is refused")
    expected_interface = load_host_adapters()["hosts"][host]["interface_policy"]
    if receipt.get("interface_policy") != expected_interface:
        raise InstallError("existing installer host interface policy is invalid")
    old_profiles = receipt.get("profiles")
    if (
        not isinstance(old_profiles, list)
        or not all(isinstance(value, str) for value in old_profiles)
        or old_profiles != sorted(set(old_profiles))
    ):
        raise InstallError("existing installer profiles are invalid")
    removed = set(old_profiles) - set(requested_profiles)
    if removed:
        raise InstallError(f"profile shrink is refused; retained profiles required: {sorted(removed)}")
    old_skills = receipt.get("skills")
    if (
        not isinstance(old_skills, list)
        or not all(isinstance(value, str) for value in old_skills)
        or old_skills != sorted(set(old_skills))
    ):
        raise InstallError("existing installer Skill subset is invalid")
    manifest = load_manifest()
    known_skills = set(map(str, manifest["inventory"]["skills"]))
    if not set(old_skills).issubset(known_skills):
        raise InstallError("existing installer Skill subset contains unknown names")
    contracts = {
        item["name"]: item
        for item in json.loads(
            (ROOT / "spec/skills/skills.json").read_text(encoding="utf-8")
        )["contracts"]
    }
    for name in old_skills:
        dependencies = contracts[name].get("dependencies")
        if not isinstance(dependencies, list) or not set(dependencies).issubset(old_skills):
            raise InstallError(f"existing installer Skill dependency closure is invalid: {name}")
    version = receipt.get("quint_version")
    if version not in {None, "0.32.0"}:
        raise InstallError("existing installer Quint version is invalid")
    activation = manifest["portable_runtime"]["activation_skill"]
    if (activation in old_skills) != (version == "0.32.0"):
        raise InstallError("existing installer runtime activation is inconsistent")
    assets = receipt.get("assets")
    if not isinstance(assets, list):
        raise InstallError("existing installer asset inventory is invalid")
    canonical_assets = json.dumps(
        assets, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    if commitment.get("assets_sha256") != hashlib.sha256(canonical_assets.encode()).hexdigest():
        raise InstallError("existing installer commitment does not bind the asset inventory")
    drift: list[Path] = []
    seen: set[str] = set()
    for entry in assets:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
            raise InstallError("existing installer asset entry is invalid")
        relative = entry.get("path")
        digest = entry.get("sha256")
        if (
            not isinstance(relative, str)
            or relative in seen
            or PurePosixPath(relative).is_absolute()
            or any(part in {"", ".", ".."} for part in PurePosixPath(relative).parts)
            or not isinstance(digest, str)
            or len(digest) != 64
        ):
            raise InstallError("existing installer asset path or digest is invalid")
        seen.add(relative)
        if _protected(relative, manifest):
            raise InstallError(f"existing installer asset is repository-policy protected: {relative}")
        path = target / Path(*PurePosixPath(relative).parts)
        try:
            content = safe_io.read_bytes_nofollow_pinned(path, root=target, root_fd=root_fd)
        except FileNotFoundError:
            drift.append(path)
            continue
        if hashlib.sha256(content).hexdigest() != digest:
            drift.append(path)
    skill_prefix = ".agents/skills" if host == "codex" else ".claude/skills"
    required_paths = {
        f"{skill_prefix}/{name}/SKILL.md" for name in old_skills
    }
    if old_skills:
        required_paths.update({"spec/skills/skills.qnt", "spec/skills/skills.json"})
    if version is not None:
        required_paths.update(
            {
                "tools/quintflow.py",
                "tools/safe_io.py",
                "tools/spec_mapping.py",
                "tools/render_requirements.py",
                "tools/render_skills.py",
                ".dev-standard/quint/source/package.json",
                ".dev-standard/quint/source/package-lock.json",
            }
        )
    if _dependency_runtime(manifest, old_skills) is not None:
        required_paths.update({"tools/portable_python.py", "tools/safe_io.py"})
    missing_records = required_paths - seen
    if missing_records:
        raise InstallError(
            f"existing installer receipt omits required assets: {sorted(missing_records)}"
        )
    return drift


def install(target: Path, profiles: list[str], *, apply: bool, force: bool, host: str = "codex") -> tuple[int, int, int]:
    manifest = load_manifest()
    # ``Path`` preserves ``..``. Reject it before constructing an absolute
    # target so aliases such as /tmp/.. cannot collapse to filesystem root.
    if ".." in target.parts:
        raise InstallError("target must not contain '..' aliases")
    target = target if target.is_absolute() else Path.cwd() / target
    try:
        with safe_io.trusted_root(target) as target_fd:
            identity = os.fstat(target_fd)
            root_identity = os.stat(Path("/"))
            home_identity = os.stat(Path.home())
            if (identity.st_dev, identity.st_ino) in {
                (root_identity.st_dev, root_identity.st_ino),
                (home_identity.st_dev, home_identity.st_ino),
            }:
                raise InstallError("target must be a repository directory, not root or home")

            metadata_drift = _validate_existing_metadata(
                target, target_fd, profiles, host
            )
            if metadata_drift and not force:
                for path in metadata_drift:
                    print(f"CONFLICT {path}")
                raise InstallError(
                    "managed assets drifted; rerun with --force only after reviewing the dry-run"
                )

            items = plan(target, profiles, manifest, host=host)
            selected_skills = _selected_skills(manifest, profiles)
            managed_assets: dict[Path, bytes] = {
                item.destination: safe_io.read_bytes_nofollow(item.source, root=item.source_root)
                for item in items
            }
            desired = dict(managed_assets)
            modes: dict[Path, int] = {item.destination: item.mode for item in items}
            instruction: Path | None = None
            if INSTRUCTION_PROFILES.intersection(profiles):
                instruction = instruction_path(target, host)
                before = safe_io.snapshot_file_pinned(
                    instruction, root=target, root_fd=target_fd
                )
                existing = (
                    safe_io.read_bytes_nofollow_pinned(
                        instruction, root=target, root_fd=target_fd
                    ).decode("utf-8")
                    if before.exists
                    else ""
                )
                snippet = safe_io.read_bytes_nofollow(
                    ROOT / "distribution" / "snippets" / "AGENTS.governance.md",
                    root=ROOT,
                ).decode("utf-8")
                snippet = snippet.replace("`AGENTS.md`", f"`{instruction.name}`")
                desired[instruction] = merged_instructions(existing, snippet).encode("utf-8")
                modes[instruction] = before.mode or 0o644

            runtime = manifest["portable_runtime"]
            runtime_version = (
                str(runtime["quint_version"])
                if runtime["activation_skill"] in selected_skills
                else None
            )
            records = _installation_records(
                target,
                profiles,
                host,
                managed_assets,
                runtime_version,
                selected_skills,
            )
            desired.update(records)
            modes.update({path: 0o644 for path in records})
            snapshots = {
                path: safe_io.snapshot_file_pinned(path, root=target, root_fd=target_fd)
                for path in desired
            }
            conflicts = [
                item
                for item in items
                if snapshots[item.destination].exists
                and safe_io.read_bytes_nofollow_pinned(
                    item.destination, root=target, root_fd=target_fd
                )
                != desired[item.destination]
            ]
            if conflicts and not force:
                for item in conflicts:
                    print(f"CONFLICT {item.destination}")
                raise InstallError(
                    "existing files differ; rerun with --force only after reviewing the dry-run"
                )

            copied = unchanged = 0
            for item in items:
                if snapshots[item.destination].exists and safe_io.read_bytes_nofollow_pinned(
                    item.destination, root=target, root_fd=target_fd
                ) == desired[item.destination]:
                    unchanged += 1
                    print(f"UNCHANGED {item.destination}")
                    continue
                action = "COPY" if apply else "WOULD_COPY"
                try:
                    source_label = item.source.relative_to(ROOT)
                except ValueError:
                    source_label = item.source
                print(f"{action} {source_label} -> {item.destination}")
                copied += 1
            if instruction is not None:
                if snapshots[instruction].exists and safe_io.read_bytes_nofollow_pinned(
                    instruction, root=target, root_fd=target_fd
                ) == desired[instruction]:
                    print(f"UNCHANGED {instruction}")
                    unchanged += 1
                else:
                    print(f"{'UPDATE' if apply else 'WOULD_UPDATE'} {instruction}")
                    copied += 1
            for path in records:
                if snapshots[path].exists and safe_io.read_bytes_nofollow_pinned(
                    path, root=target, root_fd=target_fd
                ) == desired[path]:
                    unchanged += 1
                else:
                    copied += 1
            if apply:
                receipt = target / ".dev-standard/install/receipt.json"
                commitment = target / ".dev-standard/install/commitment.json"
                ordinary = sorted(set(desired) - {receipt, commitment}, key=str)
                safe_io.atomic_batch_write_cas(
                    desired,
                    snapshots,
                    root=target,
                    lock_name=".dev-standard/install/.install.lock",
                    modes=modes,
                    publication_order=[*ordinary, receipt, commitment],
                    pinned_root_fd=target_fd,
                )
            return copied, unchanged, len(conflicts) + len(metadata_drift)
    except (FileNotFoundError, NotADirectoryError, safe_io.SafeIOError) as exc:
        raise InstallError(f"target directory is unsafe or unavailable: {target}: {exc}") from exc


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
