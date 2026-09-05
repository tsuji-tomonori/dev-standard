#!/usr/bin/env python3
"""Select, evolve, and verify a lightweight execution profile.

Runtime state is optional, advisory, and confined to ``.devflow/run``.  The
selector never installs CI or merge policy and never imports the repository's
large governance checklist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import types
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).absolute().parents[1]
REPO_ROOT = SKILL_ROOT.parents[2]
POLICY_PATH = SKILL_ROOT / "assets" / "execution-policy.json"
PROFILE_SCHEMA_PATH = SKILL_ROOT / "assets" / "execution-profile.schema.json"
POLICY_SCHEMA_PATH = SKILL_ROOT / "assets" / "execution-policy.schema.json"
BENCHMARK_PATH = SKILL_ROOT / "assets" / "benchmark-cases.json"
CONSTRAINTS_PATH = SKILL_ROOT / "assets" / "behavior-constraints.json"
RUN_DIRECTORY = Path(".devflow/run")

RISK_KEYWORDS = {
    "security": ["security", "セキュリティ", "脆弱性"],
    "authentication": ["authentication", "認証"],
    "authorization": ["authorization", "認可", "許可されていない"],
    "permissions": ["permission", "権限", "最小権限"],
    "data-loss": ["data loss", "データ損失", "データ削除"],
    "database-schema": ["database schema", "db schema", "dbスキーマ", "テーブル定義"],
    "migration": ["migration", "マイグレーション"],
    "public-api": ["public api", "公開api", "api contract"],
    "event-contract": ["event contract", "イベント契約"],
    "iac": ["iac", "cloudformation", "terraform", "cdk", "インフラ"],
    "network": ["network", "ネットワーク", "vpc"],
    "dependency": ["dependency", "依存ライブラリ", "間接依存", "依存関係"],
    "lockfile": ["lockfile", "lock file", "ロックファイル"],
    "durable-requirements": ["durable requirement", "永続要件", "正本要件"],
    "governance": ["governance", "ガバナンス", "実行基盤"],
    "generator": ["generator", "生成器"],
    "confidential": ["confidential", "機密"],
    "pii": ["pii", "個人情報", "個人データ"],
    "external-side-effect": ["external side effect", "外部副作用", "送信", "deploy", "デプロイ"],
    "irreversible": ["irreversible", "不可逆", "rollback困難", "ロールバック困難"],
    "production-operation": ["本番操作", "production operation"],
}
MECHANICAL_WORDS = ["mechanical", "機械的", "一括置換", "rename", "誤字", "文言"]
SEMANTIC_WORDS = ["architecture", "設計", "意味的", "リファクタリング", "矛盾", "認可", "認証", "契約", "migration"]


class ExecutionError(RuntimeError):
    """The execution profile or runtime path violated its contract."""


def utcnow() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def rendered_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def read_json(path: Path) -> Any:
    """Read a package-owned immutable asset, never runtime state."""

    return json.loads(path.read_bytes())


def _without(value: dict[str, Any], field: str) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != field}


def _bootstrap_module(path: Path, *, root: Path, module_name: str) -> types.ModuleType:
    root = root.absolute()
    path = path.absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise ExecutionError(f"runtime escapes repository root: {path}") from exc
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
        root_identity = (os.fstat(descriptor).st_dev, os.fstat(descriptor).st_ino)
        for part in parts[:-1]:
            next_descriptor = os.open(part, directory_flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        source_descriptor = os.open(parts[-1], os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0), dir_fd=descriptor)
        try:
            if not stat.S_ISREG(os.fstat(source_descriptor).st_mode):
                raise ExecutionError(f"runtime is not a regular file: {path}")
            chunks: list[bytes] = []
            while chunk := os.read(source_descriptor, 1024 * 1024):
                chunks.append(chunk)
        finally:
            os.close(source_descriptor)
    finally:
        os.close(descriptor)
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module._bootstrap_root_identity = root_identity
    sys.modules[module_name] = module
    exec(compile(b"".join(chunks), str(path), "exec"), module.__dict__)
    return module


def _safe_io(root: Path) -> types.ModuleType:
    return _bootstrap_module(root / "tools" / "safe_io.py", root=root, module_name="dev_standard_execution_safe_io")


def _runtime_path(root: Path, raw: str) -> Path:
    """Return a lexical path strictly below ``root/.devflow/run``."""

    candidate = Path(raw)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise ExecutionError("runtime paths must be relative and may not contain dot segments")
    if len(candidate.parts) <= len(RUN_DIRECTORY.parts) or candidate.parts[: len(RUN_DIRECTORY.parts)] != RUN_DIRECTORY.parts:
        raise ExecutionError("runtime paths must name a file below .devflow/run")
    return root.absolute() / candidate


def _read_runtime_json(
    path: Path,
    *,
    root: Path,
    safe_io: types.ModuleType,
    root_fd: int,
) -> tuple[dict[str, Any], Any]:
    before = safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd)
    if not before.exists:
        raise ExecutionError(f"runtime file does not exist: {path.relative_to(root)}")
    try:
        value = json.loads(safe_io.read_bytes_nofollow_pinned(path, root=root, root_fd=root_fd))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExecutionError(f"runtime file is not valid UTF-8 JSON: {path.relative_to(root)}") from exc
    if safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) != before:
        raise ExecutionError(f"runtime file changed while reading: {path.relative_to(root)}")
    if not isinstance(value, dict):
        raise ExecutionError("runtime JSON must be an object")
    return value, before


def _write_runtime(
    path: Path,
    value: dict[str, Any],
    *,
    root: Path,
    safe_io: types.ModuleType,
    root_fd: int,
    expected: Any | None = None,
    read_preconditions: dict[Path, Any] | None = None,
) -> None:
    before = safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) if expected is None else expected
    safe_io.atomic_batch_write_cas(
        {path: rendered_json(value)},
        {path: before},
        root=root,
        lock_name=".devflow/run/execution.lock",
        pinned_root_fd=root_fd,
        read_preconditions=read_preconditions,
    )


def csv_values(value: str | None) -> list[str]:
    return sorted({item.strip() for item in (value or "").split(",") if item.strip()})


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    policy = read_json(path)
    required = {
        "schema_version",
        "policy_revision",
        "selector_version",
        "rollout_phase",
        "repository_blocking",
        "max_metadata_probes",
        "scope_order",
        "assurance_order",
        "compute_order",
        "mode_order",
        "expansion_axes",
        "assurance_floors",
        "artifact_assurance_floors",
        "scope_profiles",
        "artifact_verification",
        "risk_verification",
        "budget_multipliers",
        "compute_profiles",
        "minimum_modes",
        "stagnation",
    }
    if set(policy) != required:
        raise ExecutionError(f"execution policy fields invalid: {sorted(set(policy) ^ required)}")
    if policy["schema_version"] != 3 or policy["repository_blocking"] is not False or policy["rollout_phase"] != "shadow":
        raise ExecutionError("execution policy must be schema 3, advisory, and shadow")
    return policy


def infer_risk_tags(request: str) -> list[str]:
    lowered = request.lower()
    return sorted(tag for tag, words in RISK_KEYWORDS.items() if any(word.lower() in lowered for word in words))


def infer_path_tags(paths: list[str]) -> tuple[list[str], list[str]]:
    artifacts: set[str] = set()
    risks: set[str] = set()
    for raw in paths:
        path = raw.lower()
        if "requirements" in path or path.startswith("spec/"):
            artifacts.add("requirements")
            risks.add("durable-requirements")
        if "governance" in path or "checklist" in path:
            artifacts.add("governance")
            risks.add("governance")
        if "migration" in path or path.endswith(".sql"):
            artifacts.add("database")
            risks.add("migration")
        if any(term in path for term in ["cdk", "terraform", "cloudformation", "infra/"]):
            artifacts.add("iac")
            risks.add("iac")
        if any(term in path for term in ["lock", "requirements.txt", "pyproject.toml"]):
            artifacts.add("dependency")
            risks.add("dependency")
        if any(term in path for term in ["auth", "permission", "policy"]):
            risks.add("authorization")
    return sorted(artifacts), sorted(risks)


def assurance_floor(risk_tags: list[str], artifact_tags: list[str], policy: dict[str, Any]) -> tuple[str, list[str]]:
    risk_set = set(risk_tags)
    artifact_set = set(artifact_tags)
    for level in ("critical", "elevated"):
        reasons = [
            *(f"risk:{tag}" for tag in sorted(risk_set.intersection(policy["assurance_floors"][level]))),
            *(f"artifact:{tag}" for tag in sorted(artifact_set.intersection(policy["artifact_assurance_floors"][level]))),
        ]
        if reasons:
            return level, reasons
    return "standard", ["no elevated or critical risk feature"]


def determine_scope(expected_files: int, domains: list[str], changed_paths: list[str]) -> tuple[str, list[str]]:
    domain_count = len(set(domains))
    path_count = len(set(changed_paths))
    if expected_files > 8 or domain_count > 1 or path_count > 8:
        return "repository", [f"expected_files={expected_files}", f"domains={domain_count}", f"changed_paths={path_count}"]
    if expected_files == 1 and domain_count <= 1 and path_count <= 1:
        return "local", ["one expected file", "at most one domain", "at most one explicit path"]
    return "module", [f"bounded impact: expected_files={expected_files}", f"domains={domain_count}"]


def determine_compute(request: str, scope: str, tags: list[str], policy: dict[str, Any]) -> dict[str, Any]:
    lowered = request.lower()
    mechanical = any(word.lower() in lowered for word in MECHANICAL_WORDS)
    semantic = any(word.lower() in lowered for word in SEMANTIC_WORDS)
    if mechanical and not semantic:
        tier, evidence = "economy", ["mechanical transformation is explicit"]
    elif semantic and scope == "repository":
        tier, evidence = "capable", ["cross-repository semantic interaction is explicit"]
    elif semantic or set(tags).intersection({"security", "authentication", "authorization", "permissions", "migration", "public-api", "event-contract"}):
        tier, evidence = "standard", ["semantic policy or contract reasoning is required"]
    else:
        tier, evidence = "standard", ["no calibrated evidence supports economy or capable routing"]
    return {"model_tier": tier, "reasoning_effort": policy["compute_profiles"][tier]["reasoning_effort"], "evidence": evidence}


def determine_mode(scope: str, assurance: str, policy: dict[str, Any]) -> dict[str, Any]:
    minimum = policy["minimum_modes"][assurance]
    if minimum == "agent-with-review":
        return {"value": minimum, "evidence": ["critical assurance requires independent review"]}
    if minimum == "agent" or scope != "local":
        return {"value": "agent", "evidence": [f"{assurance} assurance or {scope} scope requires governed agent execution"]}
    return {"value": "direct-edit", "evidence": ["local standard change has no delegation requirement"]}


def confidence_features(
    expected_files: int,
    domains: list[str],
    artifacts: list[str],
    changed_paths: list[str],
    acceptance: list[str],
) -> dict[str, Any]:
    evidence: list[str] = []
    for condition, label in [
        (expected_files > 0, "expected file count supplied"),
        (bool(domains), "affected domain supplied"),
        (bool(artifacts), "artifact type supplied"),
        (bool(changed_paths), "changed path supplied"),
        (bool(acceptance), "acceptance criteria supplied"),
    ]:
        if condition:
            evidence.append(label)
    if not evidence:
        evidence.append("no deterministic sizing feature supplied")
    band = "high" if len(evidence) >= 4 else ("medium" if len(evidence) >= 2 else "low")
    return {"band": band, "method": "deterministic-features-v1", "score": None, "evidence": evidence}


def scaled_budget(values: dict[str, int], multiplier: float) -> dict[str, int]:
    return {key: max(1 if value else 0, int(value * multiplier + 0.999)) for key, value in values.items()}


def _checks_for_tags(tags: list[str], mapping: dict[str, list[str]]) -> list[str]:
    return sorted({check for tag in tags for check in mapping.get(tag, [])})


def verification_projection(
    artifact_tags: list[str],
    risk_tags: list[str],
    acceptance: list[str],
    repository_required_gates: list[str],
    diagnostic_checks: list[str],
    policy: dict[str, Any],
) -> dict[str, Any]:
    """Project only evidence directly owned by acceptance, risk, artifact, or target."""

    components = {
        "artifact": _checks_for_tags(artifact_tags, policy["artifact_verification"]),
        "risk": _checks_for_tags(risk_tags, policy["risk_verification"]),
        "acceptance": [f"acceptance:{digest(item)[:16]}" for item in acceptance],
        "target_owned": sorted(set(repository_required_gates)),
    }
    required: list[str] = []
    for name in ("artifact", "risk", "acceptance", "target_owned"):
        for check in components[name]:
            if check not in required:
                required.append(check)
    projection = {"components": components, "required": required, "diagnostic": sorted(set(diagnostic_checks))}
    projection["required_digest"] = digest({"components": components, "required": required})
    return projection


def estimate_profile(
    request: str,
    *,
    expected_files: int,
    domains: list[str],
    artifact_tags: list[str],
    risk_tags: list[str],
    changed_paths: list[str] | None = None,
    acceptance_criteria: list[str] | None = None,
    metadata_probes: list[dict[str, Any]] | None = None,
    repository_required_gates: list[str] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy()
    if expected_files < 0:
        raise ExecutionError("expected file count must be non-negative")
    paths = sorted(set(changed_paths or []))
    acceptance = sorted(set(acceptance_criteria or []))
    probes = deepcopy(metadata_probes or [])
    if len(probes) > policy["max_metadata_probes"]:
        raise ExecutionError("metadata probe exceeds policy maximum")
    for probe in probes:
        if not isinstance(probe, dict) or not str(probe.get("evidence", "")).strip() or float(probe.get("cost", 0)) < 0:
            raise ExecutionError("metadata probe requires reusable evidence and non-negative cost")
    gates = sorted(set(repository_required_gates or []))
    if any(not isinstance(gate, str) or not gate.strip() for gate in gates):
        raise ExecutionError("target-owned gate must be a non-empty identifier")
    path_artifacts, path_risks = infer_path_tags(paths)
    artifacts = sorted(set(artifact_tags).union(path_artifacts))
    risks = sorted(set(risk_tags).union(infer_risk_tags(request), path_risks))
    scope, scope_evidence = determine_scope(expected_files, domains, paths)
    assurance, floor_reasons = assurance_floor(risks, artifacts, policy)
    multiplier = float(policy["budget_multipliers"][assurance])
    projection = verification_projection(artifacts, risks, acceptance, gates, [], policy)
    estimate = {
        "scope": {"value": scope, "evidence": scope_evidence},
        "assurance": {"value": assurance, "floor_reasons": floor_reasons},
        "compute": determine_compute(request, scope, risks, policy),
        "mode": determine_mode(scope, assurance, policy),
        "confidence": confidence_features(expected_files, domains, artifacts, paths, acceptance),
        "budget_profile": f"{scope}-{assurance}-v1",
        "context_budget": scaled_budget(policy["scope_profiles"][scope]["context_budget"], multiplier),
        "tool_budget": scaled_budget(policy["scope_profiles"][scope]["tool_budget"], multiplier),
        "required_verification": projection["required"],
        "verification_projection": projection,
        "diagnostic_checks": [],
        "repository_required_gates": gates,
        "expected_files": expected_files,
        "expected_domains": sorted(set(domains)),
        "artifact_tags": artifacts,
        "risk_tags": risks,
        "changed_paths": paths,
        "acceptance_criteria": acceptance,
        "metadata_probes": probes,
    }
    now = utcnow()
    state = {
        "schema_version": 2,
        "policy_revision": policy["policy_revision"],
        "selector_revision": policy["selector_version"],
        "rollout_phase": policy["rollout_phase"],
        "status": "estimated",
        "created_at": now,
        "updated_at": now,
        "state_revision": 1,
        "estimate": estimate,
        "expansions": [],
        "observations": [],
        "selection": {},
        "actual": {
            "input_tokens": None,
            "output_tokens": None,
            "wall_clock_seconds": 0.0,
            "tool_calls": 0,
            "search_calls": 0,
            "unique_files_read": [],
            "read_bytes": 0,
            "read_ranges": 0,
            "duplicate_read_bytes": 0,
            "metadata_probe_cost": round(sum(float(probe.get("cost", 0)) for probe in probes), 3),
            "estimate_overhead": round(sum(float(probe.get("cost", 0)) for probe in probes), 3),
            "subagent_calls": 0,
            "model_escalations": 0,
            "expansion_count": 0,
            "time_to_first_valid_patch": None,
            "post_success_activity": 0,
            "verification_result": None,
            "escaped_defect": False,
            "success": False,
        },
        "stop": None,
        "state_commitment": {},
    }
    seal_state(state, advance=False)
    return state


def state_projection(state: dict[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in state.items() if key != "state_commitment"}


def seal_state(state: dict[str, Any], *, advance: bool = True) -> None:
    if advance:
        state["state_revision"] = int(state.get("state_revision", 0)) + 1
    state["state_commitment"] = {
        "algorithm": "sha256",
        "revision": state["state_revision"],
        "projection_digest": digest(state_projection(state)),
    }


def validate_expansion_chain(expansions: Any) -> list[str]:
    if not isinstance(expansions, list):
        return ["expansions must be an array"]
    errors: list[str] = []
    previous = "0" * 64
    failures: set[str] = set()
    for index, event in enumerate(expansions, start=1):
        if not isinstance(event, dict):
            errors.append(f"expansion {index} must be an object")
            continue
        if event.get("sequence") != index or event.get("previous_expansion_digest") != previous:
            errors.append(f"expansion {index} sequence or predecessor mismatch")
        if event.get("expansion_digest") != digest(_without(event, "expansion_digest")):
            errors.append(f"expansion {index} digest mismatch")
        failure = event.get("failure_identity")
        if failure and failure in failures:
            errors.append(f"expansion {index} repeats a stable failure identity")
        if failure:
            failures.add(failure)
        previous = str(event.get("expansion_digest", ""))
    return errors


def build_selection(state: dict[str, Any]) -> dict[str, Any]:
    estimate = state["estimate"]
    selected = list(estimate["required_verification"])
    selection = {
        "schema_version": 1,
        "estimate_digest": digest(estimate),
        "projection_digest": estimate["verification_projection"]["required_digest"],
        "selected_checks": selected,
        "selected_checks_digest": digest(selected),
    }
    selection["manifest_digest"] = digest(selection)
    return selection


def _selection_errors(selection: Any, estimate: dict[str, Any]) -> list[str]:
    if selection == {}:
        return []
    required = {"schema_version", "estimate_digest", "projection_digest", "selected_checks", "selected_checks_digest", "manifest_digest"}
    if not isinstance(selection, dict) or set(selection) != required:
        return ["selection fields invalid"]
    errors: list[str] = []
    if selection["schema_version"] != 1:
        errors.append("selection schema invalid")
    if selection["manifest_digest"] != digest(_without(selection, "manifest_digest")):
        errors.append("selection manifest digest mismatch")
    if selection["estimate_digest"] != digest(estimate):
        errors.append("selection is stale for the current estimate")
    if selection["projection_digest"] != estimate["verification_projection"]["required_digest"]:
        errors.append("selection projection mismatch")
    if selection["selected_checks"] != estimate["required_verification"]:
        errors.append("selection differs from required verification")
    if selection["selected_checks_digest"] != digest(selection["selected_checks"]):
        errors.append("selection check digest mismatch")
    return errors


def stop_digest(stop: dict[str, Any]) -> str:
    return digest(_without(stop, "stop_digest"))


def validate_profile(state: dict[str, Any], policy: dict[str, Any] | None = None, *, allow_legacy: bool = True) -> list[str]:
    policy = policy or load_policy()
    if state.get("schema_version") == 1 and allow_legacy:
        return []
    if state.get("schema_version") != 2:
        return ["unsupported execution profile schema_version"]
    errors: list[str] = []
    required_top = {
        "schema_version",
        "policy_revision",
        "selector_revision",
        "rollout_phase",
        "status",
        "created_at",
        "updated_at",
        "state_revision",
        "estimate",
        "expansions",
        "observations",
        "selection",
        "actual",
        "stop",
        "state_commitment",
    }
    if set(state) != required_top:
        errors.append(f"profile fields invalid: {sorted(set(state) ^ required_top)}")
    if state.get("policy_revision") != policy["policy_revision"] or state.get("selector_revision") != policy["selector_version"]:
        errors.append("execution policy or selector revision mismatch")
    if state.get("rollout_phase") != "shadow" or state.get("status") not in {"estimated", "executing", "verification-failed", "success"}:
        errors.append("rollout phase or status invalid")
    if not isinstance(state.get("state_revision"), int) or state["state_revision"] < 1:
        errors.append("state revision invalid")
    estimate = state.get("estimate")
    if not isinstance(estimate, dict):
        return errors + ["estimate must be an object"]
    required_estimate = {
        "scope",
        "assurance",
        "compute",
        "mode",
        "confidence",
        "budget_profile",
        "context_budget",
        "tool_budget",
        "required_verification",
        "verification_projection",
        "diagnostic_checks",
        "repository_required_gates",
        "expected_files",
        "expected_domains",
        "artifact_tags",
        "risk_tags",
        "changed_paths",
        "acceptance_criteria",
        "metadata_probes",
    }
    if set(estimate) != required_estimate:
        errors.append(f"estimate fields invalid: {sorted(set(estimate) ^ required_estimate)}")
    scope = (estimate.get("scope") or {}).get("value")
    assurance = (estimate.get("assurance") or {}).get("value")
    mode = (estimate.get("mode") or {}).get("value")
    compute = estimate.get("compute") or {}
    if scope not in policy["scope_order"]:
        errors.append("invalid scope")
    if assurance not in policy["assurance_order"]:
        errors.append("invalid assurance")
    if mode not in policy["mode_order"]:
        errors.append("invalid mode")
    if compute.get("model_tier") not in policy["compute_order"]:
        errors.append("invalid compute model tier")
    confidence = estimate.get("confidence") or {}
    if confidence.get("method") != "deterministic-features-v1" or confidence.get("score") is not None:
        errors.append("uncalibrated confidence score is forbidden")
    probes = estimate.get("metadata_probes")
    if not isinstance(probes, list) or len(probes) > policy["max_metadata_probes"]:
        errors.append("metadata probe limit exceeded")
    if scope in policy["scope_order"] and assurance in policy["assurance_order"]:
        expected_projection = verification_projection(
            estimate.get("artifact_tags") or [],
            estimate.get("risk_tags") or [],
            estimate.get("acceptance_criteria") or [],
            estimate.get("repository_required_gates") or [],
            estimate.get("diagnostic_checks") or [],
            policy,
        )
        if estimate.get("verification_projection") != expected_projection or estimate.get("required_verification") != expected_projection["required"]:
            errors.append("verification projection differs from direct inputs")
        floor, reasons = assurance_floor(estimate.get("risk_tags") or [], estimate.get("artifact_tags") or [], policy)
        if policy["assurance_order"].index(assurance) < policy["assurance_order"].index(floor):
            errors.append(f"assurance floor violated: required={floor}")
        if assurance == floor and set((estimate.get("assurance") or {}).get("floor_reasons") or []) != set(reasons):
            errors.append("assurance floor evidence differs from risk and artifact union")
    errors.extend(validate_expansion_chain(state.get("expansions")))
    errors.extend(_selection_errors(state.get("selection"), estimate))
    if not isinstance(state.get("observations"), list) or any(not isinstance(item, dict) for item in state.get("observations", [])):
        errors.append("observations must be an array of objects")
    actual = state.get("actual")
    if not isinstance(actual, dict):
        errors.append("actual must be an object")
    elif actual.get("expansion_count") != len(state.get("expansions") or []):
        errors.append("actual expansion count mismatch")
    stop = state.get("stop")
    if state.get("status") == "success":
        expected_stop_fields = {
            "timestamp",
            "reason",
            "profile_digest",
            "verification_projection_digest",
            "completed_checks_digest",
            "diagnostic_checks_digest",
            "assurance_floor_digest",
            "selection_digest",
            "expansion_chain_head",
            "stop_digest",
        }
        if not isinstance(stop, dict) or set(stop) != expected_stop_fields:
            errors.append("success requires an exact stop record")
        elif stop["stop_digest"] != stop_digest(stop):
            errors.append("stop digest mismatch")
        else:
            if stop["profile_digest"] != digest(estimate) or stop["verification_projection_digest"] != estimate["verification_projection"]["required_digest"]:
                errors.append("stop does not bind the current estimate")
            if stop["selection_digest"] != (state.get("selection") or {}).get("manifest_digest", ""):
                errors.append("stop does not bind the current selection")
            head = state["expansions"][-1]["expansion_digest"] if state.get("expansions") else "0" * 64
            if stop["expansion_chain_head"] != head:
                errors.append("stop does not bind the full expansion chain")
        if not (actual or {}).get("success") or (actual or {}).get("verification_result") != "pass":
            errors.append("success state does not match actual verification")
    elif stop is not None:
        errors.append("non-success state may not contain a stop record")
    commitment = state.get("state_commitment")
    if not isinstance(commitment, dict) or set(commitment) != {"algorithm", "revision", "projection_digest"}:
        errors.append("state commitment fields invalid")
    elif (
        commitment.get("algorithm") != "sha256"
        or commitment.get("revision") != state.get("state_revision")
        or commitment.get("projection_digest") != digest(state_projection(state))
    ):
        errors.append("state commitment mismatch")
    return errors


def refresh_derived(estimate: dict[str, Any], policy: dict[str, Any]) -> None:
    scope = estimate["scope"]["value"]
    assurance = estimate["assurance"]["value"]
    multiplier = float(policy["budget_multipliers"][assurance])
    estimate["budget_profile"] = f"{scope}-{assurance}-v1"
    estimate["context_budget"] = scaled_budget(policy["scope_profiles"][scope]["context_budget"], multiplier)
    estimate["tool_budget"] = scaled_budget(policy["scope_profiles"][scope]["tool_budget"], multiplier)
    projection = verification_projection(
        estimate.get("artifact_tags") or [],
        estimate.get("risk_tags") or [],
        estimate.get("acceptance_criteria") or [],
        estimate.get("repository_required_gates") or [],
        estimate.get("diagnostic_checks") or [],
        policy,
    )
    estimate["required_verification"] = projection["required"]
    estimate["verification_projection"] = projection


def budget_overruns(state: dict[str, Any]) -> dict[str, dict[str, float]]:
    estimate, actual = state["estimate"], state["actual"]
    values = {
        "unique_files_read": (len(actual.get("unique_files_read") or []), estimate["context_budget"]["unique_files"]),
        "read_bytes": (actual.get("read_bytes", 0), estimate["context_budget"]["read_bytes"]),
        "read_ranges": (actual.get("read_ranges", 0), estimate["context_budget"]["read_ranges"]),
        "search_calls": (actual.get("search_calls", 0), estimate["tool_budget"]["search_calls"]),
        "tool_calls": (actual.get("tool_calls", 0), estimate["tool_budget"]["tool_calls"]),
        "subagent_calls": (actual.get("subagent_calls", 0), estimate["tool_budget"]["subagent_calls"]),
    }
    return {key: {"actual": float(observed), "budget": float(limit)} for key, (observed, limit) in values.items() if observed > limit}


def record_observation(state: dict[str, Any], metrics: dict[str, Any], *, kind: str, evidence: str) -> None:
    errors = validate_profile(state, allow_legacy=False)
    if errors:
        raise ExecutionError("; ".join(errors))
    if not kind.strip() or not evidence.strip():
        raise ExecutionError("observation requires kind and evidence")
    actual = state["actual"]
    positive = False
    for key in [
        "wall_clock_seconds",
        "tool_calls",
        "search_calls",
        "read_bytes",
        "read_ranges",
        "duplicate_read_bytes",
        "metadata_probe_cost",
        "estimate_overhead",
        "subagent_calls",
    ]:
        value = metrics.get(key)
        if value is not None:
            if isinstance(value, bool) or float(value) < 0:
                raise ExecutionError(f"{key} must be non-negative")
            actual[key] = round(float(actual.get(key, 0)) + float(value), 3)
            positive = positive or float(value) > 0
    for key in ["input_tokens", "output_tokens", "time_to_first_valid_patch", "escaped_defect"]:
        if metrics.get(key) is not None:
            actual[key] = metrics[key]
    files = sorted(set(actual.get("unique_files_read") or []).union(metrics.get("unique_files_read") or []))
    positive = positive or len(files) > len(actual.get("unique_files_read") or [])
    actual["unique_files_read"] = files
    observation = {"timestamp": utcnow(), "kind": kind, "evidence": evidence, "metrics": deepcopy(metrics)}
    if state["status"] == "success" and positive:
        observation["post_success_activity"] = True
        actual["post_success_activity"] += 1
    state["observations"].append(observation)
    if state["status"] == "estimated":
        state["status"] = "executing"
    state["updated_at"] = utcnow()
    seal_state(state)


REASON_AXES = {
    "verification-failed": {"verification", "scope", "assurance"},
    "impact-surface-exceeded": {"scope"},
    "dependency-discovered": {"scope"},
    "contract-impact-discovered": {"scope", "assurance"},
    "assurance-floor-insufficient": {"assurance"},
    "requirements-conflict": {"scope", "assurance", "verification"},
    "evidence-insufficient": {"verification", "scope"},
    "compute-insufficient": {"compute"},
    "review-required": {"review"},
}


def _execution_axes(estimate: dict[str, Any]) -> dict[str, Any]:
    return {
        "scope": deepcopy(estimate["scope"]),
        "assurance": deepcopy(estimate["assurance"]),
        "verification": deepcopy(estimate["diagnostic_checks"]),
        "review": deepcopy(estimate["mode"]),
        "compute": deepcopy(estimate["compute"]),
    }


def stable_failure_identity(value: str) -> str:
    normalized = " ".join(value.strip().split())
    if not normalized:
        raise ExecutionError("stable failure identity must be non-empty")
    return digest({"failure_identity": normalized})


def expand_profile(
    state: dict[str, Any],
    *,
    axis: str,
    reason_code: str,
    evidence: str,
    actor: str,
    failure_identity: str | None = None,
) -> None:
    policy = load_policy()
    errors = validate_profile(state, policy, allow_legacy=False)
    if errors:
        raise ExecutionError("; ".join(errors))
    if state["status"] == "success":
        raise ExecutionError("cannot expand after decisive success")
    if axis not in policy["expansion_axes"] or axis not in REASON_AXES.get(reason_code, set()) or not evidence.strip() or not actor.strip():
        raise ExecutionError("expansion requires an allowed reason, matching axis, actor, and evidence")
    if reason_code == "verification-failed" and not failure_identity:
        raise ExecutionError("verification-failed expansion requires a stable failure identity")
    failure_digest = stable_failure_identity(failure_identity) if failure_identity else ""
    if failure_digest and any(event.get("failure_identity") == failure_digest for event in state["expansions"]):
        raise ExecutionError("stagnation: stable failure identity already expanded")
    signature = digest({"axis": axis, "reason_code": reason_code, "evidence": evidence.strip()})
    if any(event.get("evidence_signature") == signature for event in state["expansions"]):
        raise ExecutionError("stagnation: duplicate expansion evidence")
    estimate = state["estimate"]
    before = deepcopy(estimate)
    before_axes = _execution_axes(before)
    if axis == "scope":
        order = policy["scope_order"]
        current = estimate["scope"]["value"]
        if current == order[-1]:
            raise ExecutionError("stagnation: scope cannot expand further")
        estimate["scope"] = {"value": order[order.index(current) + 1], "evidence": [*estimate["scope"]["evidence"], evidence]}
        refresh_derived(estimate, policy)
    elif axis == "assurance":
        order = policy["assurance_order"]
        current = estimate["assurance"]["value"]
        if current == order[-1]:
            raise ExecutionError("stagnation: assurance cannot expand further")
        estimate["assurance"] = {"value": order[order.index(current) + 1], "floor_reasons": [*estimate["assurance"]["floor_reasons"], evidence]}
        refresh_derived(estimate, policy)
    elif axis == "verification":
        estimate["diagnostic_checks"].append(f"diagnostic:{(failure_digest or signature)[:16]}")
        refresh_derived(estimate, policy)
    elif axis == "review":
        order = policy["mode_order"]
        current = estimate["mode"]["value"]
        if current == order[-1]:
            raise ExecutionError("stagnation: review mode cannot expand further")
        estimate["mode"] = {"value": order[order.index(current) + 1], "evidence": [*estimate["mode"]["evidence"], evidence]}
    elif axis == "compute":
        order = policy["compute_order"]
        current = estimate["compute"]["model_tier"]
        if current == order[-1]:
            raise ExecutionError("stagnation: compute cannot expand further")
        tier = order[order.index(current) + 1]
        estimate["compute"] = {
            "model_tier": tier,
            "reasoning_effort": policy["compute_profiles"][tier]["reasoning_effort"],
            "evidence": [*estimate["compute"]["evidence"], evidence],
        }
        state["actual"]["model_escalations"] += 1
    after_axes = _execution_axes(estimate)
    changed = sorted(name for name in before_axes if digest(before_axes[name]) != digest(after_axes[name]))
    if changed != [axis]:
        raise ExecutionError(f"expansion must change exactly one execution axis: {changed}")
    event = {
        "sequence": len(state["expansions"]) + 1,
        "timestamp": utcnow(),
        "axis": axis,
        "reason_code": reason_code,
        "evidence": evidence,
        "evidence_signature": signature,
        "failure_identity": failure_digest,
        "actor": actor,
        "before_axis_digest": digest(before_axes[axis]),
        "after_axis_digest": digest(after_axes[axis]),
        "before_profile_digest": digest(before),
        "after_profile_digest": digest(estimate),
        "projection_digest": estimate["verification_projection"]["required_digest"],
        "previous_expansion_digest": state["expansions"][-1]["expansion_digest"] if state["expansions"] else "0" * 64,
    }
    event["expansion_digest"] = digest(event)
    state["expansions"].append(event)
    state["selection"] = {}
    state["actual"]["expansion_count"] = len(state["expansions"])
    state["status"] = "executing"
    state["updated_at"] = utcnow()
    seal_state(state)


def record_selection(state: dict[str, Any], selection: dict[str, Any]) -> None:
    errors = validate_profile(state, allow_legacy=False)
    if errors:
        raise ExecutionError("; ".join(errors))
    selection_errors = _selection_errors(selection, state["estimate"])
    if selection_errors:
        raise ExecutionError("; ".join(selection_errors))
    if not selection:
        raise ExecutionError("selection may not be empty")
    state["selection"] = deepcopy(selection)
    state["updated_at"] = utcnow()
    seal_state(state)


def mark_verification(
    state: dict[str, Any],
    *,
    result: str,
    evidence: str,
    summary: str,
    completed_checks: list[str],
    completed_diagnostics: list[str] | None = None,
    failure_identity: str | None = None,
) -> None:
    errors = validate_profile(state, allow_legacy=False)
    if errors:
        raise ExecutionError("; ".join(errors))
    if state["status"] == "success":
        raise ExecutionError("verification is already complete")
    if result not in {"pass", "fail"} or not evidence.strip() or not summary.strip():
        raise ExecutionError("verification needs pass/fail, evidence, and summary")
    required = state["estimate"]["required_verification"]
    completed = sorted(set(completed_checks))
    missing = sorted(set(required) - set(completed))
    unexpected = sorted(set(completed) - set(required))
    diagnostics = sorted(set(completed_diagnostics or []))
    unknown_diagnostics = sorted(set(diagnostics) - set(state["estimate"]["diagnostic_checks"]))
    advisory_findings: list[str] = []
    if missing:
        advisory_findings.append("missing selected checks: " + ", ".join(missing))
    if not required:
        advisory_findings.append("no acceptance/risk/artifact/target-owned check was selected")
    if unexpected:
        advisory_findings.append("unselected checks were reported: " + ", ".join(unexpected))
    if unknown_diagnostics:
        advisory_findings.append("unknown diagnostics were reported: " + ", ".join(unknown_diagnostics))
    mode_sufficient = True
    if result == "pass":
        policy = load_policy()
        minimum = policy["minimum_modes"][state["estimate"]["assurance"]["value"]]
        mode = state["estimate"]["mode"]["value"]
        if policy["mode_order"].index(mode) < policy["mode_order"].index(minimum):
            mode_sufficient = False
            advisory_findings.append(f"review mode below advisory minimum: expected={minimum} actual={mode}")
        if not state["selection"]:
            state["selection"] = build_selection(state)
    failure_digest = stable_failure_identity(failure_identity or f"{evidence}\n{summary}") if result == "fail" else ""
    state["observations"].append(
        {
            "timestamp": utcnow(),
            "kind": "verification",
            "result": result,
            "evidence": evidence,
            "summary": summary,
            "completed_checks": completed,
            "completed_diagnostics": diagnostics,
            "missing_checks": missing,
            "unexpected_checks": unexpected,
            "advisory_findings": advisory_findings,
            "failure_identity": failure_digest,
        }
    )
    state["actual"]["verification_result"] = result
    decisive = result == "pass" and bool(required) and not missing and mode_sufficient
    if decisive:
        state["status"] = "success"
        state["actual"]["success"] = True
        stop = {
            "timestamp": utcnow(),
            "reason": "selected-change-relevant-checks-passed",
            "profile_digest": digest(state["estimate"]),
            "verification_projection_digest": state["estimate"]["verification_projection"]["required_digest"],
            "completed_checks_digest": digest(completed),
            "diagnostic_checks_digest": digest(diagnostics),
            "assurance_floor_digest": digest(state["estimate"]["assurance"]),
            "selection_digest": state["selection"]["manifest_digest"],
            "expansion_chain_head": state["expansions"][-1]["expansion_digest"] if state["expansions"] else "0" * 64,
        }
        stop["stop_digest"] = stop_digest(stop)
        state["stop"] = stop
    elif result == "fail":
        state["status"] = "verification-failed"
        state["actual"]["success"] = False
    else:
        state["status"] = "executing"
        state["actual"]["success"] = False
    state["updated_at"] = utcnow()
    seal_state(state)


def audit_profile(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("schema_version") == 1:
        return {
            "schema_version": 3,
            "profile_digest": digest(state),
            "enforcement": "legacy-advisory",
            "repository_blocking": False,
            "errors": [],
            "diagnostics": [],
            "warnings": ["legacy profile; migrate only if the current work needs runtime state"],
            "overruns": {},
        }
    diagnostics = validate_profile(state, allow_legacy=False)
    diagnostics.extend(
        finding for observation in state.get("observations", []) if isinstance(observation, dict) for finding in observation.get("advisory_findings", [])
    )
    overruns = budget_overruns(state) if isinstance(state.get("actual"), dict) and isinstance(state.get("estimate"), dict) else {}
    warnings: list[str] = []
    if overruns and not state.get("expansions"):
        warnings.append("advisory budget overrun has no recorded decision")
    if any(item.get("post_success_activity") for item in state.get("observations", []) if isinstance(item, dict)):
        warnings.append("positive-cost activity continued after decisive success")
    return {
        "schema_version": 3,
        "profile_digest": digest(state),
        "enforcement": "shadow",
        "repository_blocking": False,
        "errors": [],
        "diagnostics": diagnostics,
        "warnings": warnings,
        "overruns": overruns,
    }


def efficiency_report(state: dict[str, Any]) -> dict[str, Any]:
    audit = audit_profile(state)
    ratios = {key: round((value["actual"] - value["budget"]) / value["budget"], 4) if value["budget"] else 1.0 for key, value in audit["overruns"].items()}
    return {
        "schema_version": 3,
        "generated_at": utcnow(),
        "status": state["status"],
        "success": state["actual"].get("success", False),
        "estimate": state["estimate"],
        "actual": state["actual"],
        "expansions": state["expansions"],
        "execution_overrun_ratio": ratios,
        "audit": audit,
        "acrr": None,
        "acrr_note": "C_min oracleがない実案件ではACRRを算出しない",
    }


def run_benchmark(path: Path = BENCHMARK_PATH) -> dict[str, Any]:
    """Run only package-owned deterministic cases; no repository catalog is read."""

    suite = read_json(path)
    profiles: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    for case in suite["cases"]:
        state = estimate_profile(
            case["request"],
            expected_files=case["expected_files"],
            domains=case["domains"],
            artifact_tags=case["artifact_tags"],
            risk_tags=case["risk_tags"],
            changed_paths=case.get("changed_paths", []),
            acceptance_criteria=case.get("acceptance_criteria", []),
        )
        profiles[case["id"]] = state
        actual = {
            "scope": state["estimate"]["scope"]["value"],
            "assurance": state["estimate"]["assurance"]["value"],
            "model_tier": state["estimate"]["compute"]["model_tier"],
            "mode": state["estimate"]["mode"]["value"],
        }
        passed = actual == case["expected"]
        if case.get("expansion"):
            specification = case["expansion"]
            expand_profile(
                state,
                axis=specification["axis"],
                reason_code=specification["reason_code"],
                evidence=specification["evidence"],
                actor="benchmark",
            )
            passed = passed and state["estimate"][specification["axis"]]["value"] == specification["expected_value"]
        results.append({"id": case["id"], "expected": case["expected"], "actual": actual, "passed": passed})

    behavior: dict[str, bool] = {}
    evidence: dict[str, str] = {}
    local_critical = profiles["authorization-local-critical"]
    behavior["RSE-PROFILE-001"] = local_critical["estimate"]["scope"]["value"] == "local" and local_critical["estimate"]["assurance"]["value"] == "critical"
    evidence["RSE-PROFILE-001"] = digest(local_critical["estimate"])
    artifact_floor = estimate_profile(
        "one file change",
        expected_files=1,
        domains=["data"],
        artifact_tags=["database"],
        risk_tags=[],
        changed_paths=["src/data/value.py"],
        acceptance_criteria=["behavior is preserved"],
    )
    behavior["RSE-FLOOR-001"] = artifact_floor["estimate"]["assurance"]["value"] == "elevated"
    evidence["RSE-FLOOR-001"] = digest(artifact_floor["estimate"]["assurance"])
    behavior["RSE-CONFIDENCE-001"] = all(state["estimate"]["confidence"]["score"] is None for state in profiles.values())
    evidence["RSE-CONFIDENCE-001"] = digest([state["estimate"]["confidence"] for state in profiles.values()])
    expanded = estimate_profile(
        "module change", expected_files=2, domains=["core"], artifact_tags=["implementation"], risk_tags=[], acceptance_criteria=["works"]
    )
    expand_profile(expanded, axis="verification", reason_code="verification-failed", evidence="failure-A", actor="benchmark", failure_identity="failure-A")
    expand_profile(expanded, axis="review", reason_code="review-required", evidence="failure-B", actor="benchmark")
    expand_profile(expanded, axis="compute", reason_code="compute-insufficient", evidence="failure-C", actor="benchmark")
    behavior["RSE-EXPAND-001"] = len(expanded["expansions"]) == 3
    evidence["RSE-EXPAND-001"] = expanded["expansions"][-1]["expansion_digest"]
    try:
        expand_profile(
            expanded, axis="verification", reason_code="verification-failed", evidence="changed wording", actor="benchmark", failure_identity="failure-A"
        )
        behavior["RSE-STAGNATION-001"] = False
    except ExecutionError:
        behavior["RSE-STAGNATION-001"] = True
    evidence["RSE-STAGNATION-001"] = stable_failure_identity("failure-A")
    components = expanded["estimate"]["verification_projection"]["components"]
    behavior["RSE-PROJECTION-001"] = set(components) == {"artifact", "risk", "acceptance", "target_owned"} and not set(
        expanded["estimate"]["diagnostic_checks"]
    ).intersection(expanded["estimate"]["required_verification"])
    evidence["RSE-PROJECTION-001"] = expanded["estimate"]["verification_projection"]["required_digest"]
    behavior["RSE-CHAIN-001"] = not validate_expansion_chain(expanded["expansions"])
    evidence["RSE-CHAIN-001"] = expanded["expansions"][-1]["expansion_digest"]
    selected = build_selection(expanded)
    record_selection(expanded, selected)
    expand_profile(expanded, axis="scope", reason_code="dependency-discovered", evidence="new dependency", actor="benchmark")
    behavior["RSE-SELECTION-001"] = expanded["selection"] == {}
    evidence["RSE-SELECTION-001"] = selected["manifest_digest"]
    stop_state = profiles["wording-local"]
    mark_verification(
        stop_state,
        result="pass",
        evidence="benchmark",
        summary="selected checks passed",
        completed_checks=stop_state["estimate"]["required_verification"],
    )
    try:
        expand_profile(stop_state, axis="scope", reason_code="dependency-discovered", evidence="late", actor="benchmark")
        behavior["RSE-STOP-001"] = False
    except ExecutionError:
        behavior["RSE-STOP-001"] = True
    evidence["RSE-STOP-001"] = stop_state["stop"]["stop_digest"]
    invalid = deepcopy(local_critical)
    invalid["estimate"]["assurance"] = {"value": "standard", "floor_reasons": ["none"]}
    refresh_derived(invalid["estimate"], load_policy())
    seal_state(invalid)
    audit = audit_profile(invalid)
    behavior["RSE-ROLLOUT-001"] = audit["repository_blocking"] is False and bool(audit["diagnostics"]) and not audit["errors"]
    evidence["RSE-ROLLOUT-001"] = digest(audit)
    ordinary = estimate_profile(
        "local wording",
        expected_files=1,
        domains=["docs"],
        artifact_tags=["documentation"],
        risk_tags=[],
        changed_paths=["README.md"],
        acceptance_criteria=["wording corrected"],
    )
    behavior["RSE-OPTIONAL-001"] = ordinary["status"] == "estimated" and ordinary["observations"] == [] and ordinary["actual"]["tool_calls"] == 0
    evidence["RSE-OPTIONAL-001"] = ordinary["state_commitment"]["projection_digest"]
    groups: dict[str, set[str]] = {}
    for case in suite["cases"]:
        if group := case.get("paraphrase_group"):
            groups.setdefault(group, set()).add(profiles[case["id"]]["estimate"]["assurance"]["value"])
    constraints = {item["id"] for item in read_json(CONSTRAINTS_PATH)["constraints"]}
    covered = sorted(key for key, passed in behavior.items() if passed)
    return {
        "schema_version": 3,
        "suite": BENCHMARK_PATH.name,
        "passed": all(item["passed"] for item in results) and constraints == set(covered) and all(len(values) == 1 for values in groups.values()),
        "evaluation_stage": "shadow-deterministic-contract",
        "deployment_gate_ready": False,
        "case_count": len(results),
        "results": results,
        "behavior_constraint_count": len(constraints),
        "behavior_constraints_covered": covered,
        "behavior_constraint_evidence": {key: evidence[key] for key in sorted(evidence)},
        "behavior_coverage": round(len(covered) / len(constraints), 4) if constraints else 1.0,
        "paraphrase_assurance_consistent": all(len(values) == 1 for values in groups.values()),
        "repository_catalog_read": False,
        "claim_boundary": "shadow diagnostics are advisory and do not create a fourth repository blocker",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="trusted target repository root")
    sub = parser.add_subparsers(dest="command", required=True)
    estimate = sub.add_parser("estimate")
    estimate.add_argument("--request", required=True)
    estimate.add_argument("--out", required=True)
    estimate.add_argument("--expected-files", type=int, default=0)
    estimate.add_argument("--domains", default="")
    estimate.add_argument("--artifact-tags", default="")
    estimate.add_argument("--risk-tags", default="")
    estimate.add_argument("--changed-path", action="append", default=[])
    estimate.add_argument("--acceptance-criterion", action="append", default=[])
    estimate.add_argument("--metadata-probe", action="append", default=[])
    estimate.add_argument("--repository-required-gate", action="append", default=[])
    expand = sub.add_parser("expand")
    expand.add_argument("--profile", required=True)
    expand.add_argument("--axis", required=True)
    expand.add_argument("--reason-code", required=True)
    expand.add_argument("--evidence", required=True)
    expand.add_argument("--actor", required=True)
    expand.add_argument("--failure-identity")
    observe = sub.add_parser("observe")
    observe.add_argument("--profile", required=True)
    observe.add_argument("--kind", default="execute")
    observe.add_argument("--evidence", required=True)
    for name in ["tool-calls", "search-calls", "read-bytes", "read-ranges", "duplicate-read-bytes", "subagent-calls"]:
        observe.add_argument(f"--{name}", type=int, default=0)
    observe.add_argument("--wall-clock-seconds", type=float, default=0)
    observe.add_argument("--metadata-probe-cost", type=float, default=0)
    observe.add_argument("--estimate-overhead", type=float, default=0)
    observe.add_argument("--input-tokens", type=int)
    observe.add_argument("--output-tokens", type=int)
    observe.add_argument("--time-to-first-valid-patch", type=float)
    observe.add_argument("--unique-file-read", action="append", default=[])
    verify = sub.add_parser("verification")
    verify.add_argument("--profile", required=True)
    verify.add_argument("--result", choices=["pass", "fail"], required=True)
    verify.add_argument("--evidence", required=True)
    verify.add_argument("--summary", required=True)
    verify.add_argument("--completed-check", action="append", default=[])
    verify.add_argument("--completed-diagnostic", action="append", default=[])
    verify.add_argument("--failure-identity")
    finalize = sub.add_parser("finalize")
    finalize.add_argument("--profile", required=True)
    finalize.add_argument("--out", required=True)
    audit = sub.add_parser("audit")
    audit.add_argument("--profile", required=True)
    audit.add_argument("--mode", choices=["soft", "strict"], default="soft", help="deprecated; findings remain advisory")
    select = sub.add_parser("select-checks")
    select.add_argument("--profile", required=True)
    select.add_argument("--out", required=True)
    benchmark = sub.add_parser("benchmark")
    benchmark.add_argument("--out")
    return parser


def _dispatch(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    if args.command == "estimate":
        output = _runtime_path(root, args.out)
        output_before = safe_io.snapshot_file_pinned(output, root=root, root_fd=root_fd)
        if output_before.exists:
            raise ExecutionError(f"runtime output already exists: {output.relative_to(root)}")
        state = estimate_profile(
            args.request,
            expected_files=args.expected_files,
            domains=csv_values(args.domains),
            artifact_tags=csv_values(args.artifact_tags),
            risk_tags=csv_values(args.risk_tags),
            changed_paths=args.changed_path,
            acceptance_criteria=args.acceptance_criterion,
            metadata_probes=[{"evidence": value} for value in args.metadata_probe],
            repository_required_gates=args.repository_required_gate,
        )
        _write_runtime(output, state, root=root, safe_io=safe_io, root_fd=root_fd, expected=output_before)
        print(json.dumps({"status": state["status"], "profile": str(output.relative_to(root))}, sort_keys=True))
    elif args.command in {"expand", "observe", "verification"}:
        profile_path = _runtime_path(root, args.profile)
        state, before = _read_runtime_json(profile_path, root=root, safe_io=safe_io, root_fd=root_fd)
        if args.command == "expand":
            expand_profile(
                state, axis=args.axis, reason_code=args.reason_code, evidence=args.evidence, actor=args.actor, failure_identity=args.failure_identity
            )
        elif args.command == "observe":
            metrics = {
                "tool_calls": args.tool_calls,
                "search_calls": args.search_calls,
                "read_bytes": args.read_bytes,
                "read_ranges": args.read_ranges,
                "duplicate_read_bytes": args.duplicate_read_bytes,
                "subagent_calls": args.subagent_calls,
                "wall_clock_seconds": args.wall_clock_seconds,
                "metadata_probe_cost": args.metadata_probe_cost,
                "estimate_overhead": args.estimate_overhead,
                "input_tokens": args.input_tokens,
                "output_tokens": args.output_tokens,
                "time_to_first_valid_patch": args.time_to_first_valid_patch,
                "unique_files_read": args.unique_file_read,
            }
            record_observation(state, metrics, kind=args.kind, evidence=args.evidence)
        else:
            mark_verification(
                state,
                result=args.result,
                evidence=args.evidence,
                summary=args.summary,
                completed_checks=args.completed_check,
                completed_diagnostics=args.completed_diagnostic,
                failure_identity=args.failure_identity,
            )
        _write_runtime(profile_path, state, root=root, safe_io=safe_io, root_fd=root_fd, expected=before)
        print(json.dumps({"status": state["status"], "revision": state["state_revision"]}, sort_keys=True))
    elif args.command == "finalize":
        profile_path = _runtime_path(root, args.profile)
        output = _runtime_path(root, args.out)
        if output == profile_path:
            raise ExecutionError("finalize output must differ from its profile input")
        state, profile_before = _read_runtime_json(profile_path, root=root, safe_io=safe_io, root_fd=root_fd)
        _write_runtime(
            output,
            efficiency_report(state),
            root=root,
            safe_io=safe_io,
            root_fd=root_fd,
            read_preconditions={profile_path: profile_before},
        )
        print(json.dumps({"report": str(output.relative_to(root)), "repository_blocking": False}, sort_keys=True))
    elif args.command == "audit":
        profile_path = _runtime_path(root, args.profile)
        state, profile_before = _read_runtime_json(profile_path, root=root, safe_io=safe_io, root_fd=root_fd)
        report = audit_profile(state)
        if safe_io.snapshot_file_pinned(profile_path, root=root, root_fd=root_fd) != profile_before:
            raise ExecutionError("profile changed after audit")
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    elif args.command == "select-checks":
        profile_path = _runtime_path(root, args.profile)
        output = _runtime_path(root, args.out)
        if output == profile_path:
            raise ExecutionError("selection output must differ from its profile input")
        state, state_before = _read_runtime_json(profile_path, root=root, safe_io=safe_io, root_fd=root_fd)
        selection = build_selection(state)
        record_selection(state, selection)
        output_before = safe_io.snapshot_file_pinned(output, root=root, root_fd=root_fd)
        safe_io.atomic_batch_write_cas(
            {profile_path: rendered_json(state), output: rendered_json(selection)},
            {profile_path: state_before, output: output_before},
            root=root,
            lock_name=".devflow/run/execution.lock",
            pinned_root_fd=root_fd,
        )
        print(json.dumps({"selected": len(selection["selected_checks"]), "manifest_digest": selection["manifest_digest"]}, sort_keys=True))
    elif args.command == "benchmark":
        report = run_benchmark()
        if args.out:
            _write_runtime(_runtime_path(root, args.out), report, root=root, safe_io=safe_io, root_fd=root_fd)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 0 if report["passed"] else 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).absolute()
    try:
        safe_io = _safe_io(root)
        with safe_io.trusted_root(root) as root_fd:
            identity = (os.fstat(root_fd).st_dev, os.fstat(root_fd).st_ino)
            if identity != safe_io._bootstrap_root_identity:
                raise ExecutionError("repository root changed after runtime bootstrap")
            return _dispatch(args, root, safe_io, root_fd)
    except Exception as exc:  # CLI boundary: safe-I/O refusal types are loaded dynamically.
        print(json.dumps({"error": str(exc), "status": "rejected"}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
