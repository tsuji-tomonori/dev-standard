#!/usr/bin/env python3
"""Record one explicitly triggered regulated duty as a strict event replay."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import types
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
EVENT_ORDER = ["init", "authorize", "verify", "close"]
DUTY_KINDS = {"law", "contract", "safety", "production", "audit", "user-mandated"}
AUTHORITY_EVIDENCE_KIND = "target-owned-authorization"
MAX_TEXT = 2_000
MAX_ITEMS = 16


class RegulatedFlowError(RuntimeError):
    """A regulated transition was malformed, stale, or outside authority."""


def _bootstrap_module(path: Path, *, root: Path, module_name: str) -> types.ModuleType:
    root = root.absolute()
    path = path.absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise RegulatedFlowError(f"module escapes repository root: {path}") from exc
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
                raise RegulatedFlowError(f"module is not a regular file: {path}")
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
    return _bootstrap_module(root / "tools" / "safe_io.py", root=root, module_name="dev_standard_regulated_safe_io")


def _canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _instant(label: str, value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RegulatedFlowError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise RegulatedFlowError(f"{label} must include a timezone")
    return parsed


def _bounded(label: str, value: Any, *, maximum: int = MAX_TEXT) -> str:
    if not isinstance(value, str):
        raise RegulatedFlowError(f"{label} must be text")
    normalized = value.strip()
    if not normalized or len(normalized) > maximum:
        raise RegulatedFlowError(f"{label} must contain 1..{maximum} characters")
    return normalized


def _bounded_list(label: str, value: Any, *, required: bool = True) -> list[str]:
    if not isinstance(value, list) or len(value) > MAX_ITEMS or (required and not value):
        lower = 1 if required else 0
        raise RegulatedFlowError(f"{label} must contain {lower}..{MAX_ITEMS} entries")
    normalized = [_bounded(f"{label} entry", item, maximum=512) for item in value]
    if len(set(normalized)) != len(normalized):
        raise RegulatedFlowError(f"{label} entries must be unique")
    return normalized


def _work_paths(root: Path, work_id: str) -> tuple[Path, Path, Path]:
    if not ID_PATTERN.fullmatch(work_id) or work_id in {".", ".."}:
        raise RegulatedFlowError("work ID must be a bounded portable identifier")
    directory = root / "work" / work_id / "regulated"
    return directory / "state.json", directory / "events.jsonl", directory / "anchor.json"


def _authority_evidence_path(root: Path, work_id: str, raw: str) -> tuple[Path, str]:
    candidate = Path(_bounded("authority evidence path", raw, maximum=512))
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise RegulatedFlowError("authority evidence path must be repository-relative without dot segments")
    if candidate.suffix != ".json":
        raise RegulatedFlowError("authority evidence path must name a JSON file")
    if candidate.parts[0] == ".devflow":
        raise RegulatedFlowError("authority evidence must not come from runner-owned .devflow state")
    regulated = ("work", work_id, "regulated")
    if candidate.parts[: len(regulated)] == regulated:
        raise RegulatedFlowError("authority evidence must be external to runner-owned regulated state")
    return root / candidate, candidate.as_posix()


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RegulatedFlowError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_json(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data, object_pairs_hook=_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RegulatedFlowError(f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise RegulatedFlowError(f"{label} must be a JSON object")
    return value


def _event(sequence: int, kind: str, at: str, payload: dict[str, Any], previous: str) -> dict[str, Any]:
    base = {"at": at, "kind": kind, "payload": payload, "previous_digest": previous, "sequence": sequence}
    return {**base, "digest": hashlib.sha256(_canonical(base)).hexdigest()}


def _authorization_payload(
    *,
    work_id: str,
    authority_boundary: str,
    authority_evidence_path: str,
    authority_identity: str,
    authority_evidence_digest: str,
    approval_reference: str,
    authorized_scope: str,
    result_boundary: str,
    effects: list[str],
    rollback: str,
    stop_conditions: list[str],
    expires_at: str,
    nonce: str,
) -> dict[str, Any]:
    if not DIGEST_PATTERN.fullmatch(authority_evidence_digest):
        raise RegulatedFlowError("authority evidence digest must be 64 lowercase hexadecimal characters")
    _instant("authorization expiry", expires_at)
    payload = {
        "work_id": work_id,
        "authority_boundary": authority_boundary,
        "authority_evidence_path": authority_evidence_path,
        "authority_identity": authority_identity,
        "authority_evidence_digest": authority_evidence_digest,
        "approval_reference": approval_reference,
        "authorized_scope": authorized_scope,
        "result_boundary": result_boundary,
        "effects": effects,
        "rollback": rollback,
        "stop_conditions": stop_conditions,
        "expires_at": expires_at,
        "nonce": nonce,
    }
    payload["authorization_digest"] = hashlib.sha256(_canonical(payload)).hexdigest()
    return payload


def _normalize_authority_evidence(
    value: dict[str, Any],
    *,
    work_id: str,
    authority_boundary: str,
) -> dict[str, Any]:
    fields = {
        "schema_version",
        "evidence_kind",
        "work_id",
        "authority_boundary",
        "authority_identity",
        "approval_reference",
        "authorized_scope",
        "result_boundary",
        "effects",
        "rollback",
        "stop_conditions",
        "expires_at",
        "nonce",
    }
    if set(value) != fields or value.get("schema_version") != 1 or value.get("evidence_kind") != AUTHORITY_EVIDENCE_KIND:
        raise RegulatedFlowError("authority evidence schema or kind mismatch")
    normalized = {
        "schema_version": 1,
        "evidence_kind": AUTHORITY_EVIDENCE_KIND,
        "work_id": _bounded("authorized work ID", value["work_id"], maximum=64),
        "authority_boundary": _bounded("authorized authority boundary", value["authority_boundary"]),
        "authority_identity": _bounded("authority identity", value["authority_identity"], maximum=512),
        "approval_reference": _bounded("approval reference", value["approval_reference"], maximum=512),
        "authorized_scope": _bounded("authorized scope", value["authorized_scope"]),
        "result_boundary": _bounded("result boundary", value["result_boundary"]),
        "effects": _bounded_list("authorized effects", value["effects"]),
        "rollback": _bounded("rollback", value["rollback"]),
        "stop_conditions": _bounded_list("stop conditions", value["stop_conditions"]),
        "expires_at": _bounded("authorization expiry", value["expires_at"], maximum=64),
        "nonce": _bounded("authorization nonce", value["nonce"], maximum=256),
    }
    _instant("authorization expiry", normalized["expires_at"])
    if normalized["work_id"] != work_id or normalized["authority_boundary"] != authority_boundary:
        raise RegulatedFlowError("authority evidence is bound to another work item or authority boundary")
    return normalized


def _load_authority_evidence(
    path: Path,
    *,
    work_id: str,
    authority_boundary: str,
    root: Path,
    safe_io: types.ModuleType,
    root_fd: int,
) -> tuple[dict[str, Any], str, Any]:
    before = safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd)
    if not before.exists:
        raise RegulatedFlowError("target-owned authority evidence does not exist")
    value = _parse_json(
        safe_io.read_bytes_nofollow_pinned(path, root=root, root_fd=root_fd),
        "authority evidence",
    )
    if safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) != before:
        raise RegulatedFlowError("authority evidence changed while reading")
    normalized = _normalize_authority_evidence(
        value,
        work_id=work_id,
        authority_boundary=authority_boundary,
    )
    return normalized, hashlib.sha256(_canonical(normalized)).hexdigest(), before


def _authorization_from_evidence(
    evidence: dict[str, Any],
    *,
    authority_evidence_path: str,
    authority_evidence_digest: str,
) -> dict[str, Any]:
    return _authorization_payload(
        work_id=evidence["work_id"],
        authority_boundary=evidence["authority_boundary"],
        authority_evidence_path=authority_evidence_path,
        authority_identity=evidence["authority_identity"],
        authority_evidence_digest=authority_evidence_digest,
        approval_reference=evidence["approval_reference"],
        authorized_scope=evidence["authorized_scope"],
        result_boundary=evidence["result_boundary"],
        effects=evidence["effects"],
        rollback=evidence["rollback"],
        stop_conditions=evidence["stop_conditions"],
        expires_at=evidence["expires_at"],
        nonce=evidence["nonce"],
    )


def _validate_authorization(payload: Any, *, work_id: str, authority_boundary: str) -> dict[str, Any]:
    fields = {
        "work_id",
        "authority_boundary",
        "authority_evidence_path",
        "authority_identity",
        "authority_evidence_digest",
        "approval_reference",
        "authorized_scope",
        "result_boundary",
        "effects",
        "rollback",
        "stop_conditions",
        "expires_at",
        "nonce",
        "authorization_digest",
    }
    if not isinstance(payload, dict) or set(payload) != fields:
        raise RegulatedFlowError("authorize payload schema mismatch")
    normalized = _authorization_payload(
        work_id=_bounded("authorized work ID", payload["work_id"], maximum=64),
        authority_boundary=_bounded("authorized authority boundary", payload["authority_boundary"]),
        authority_evidence_path=_bounded("authority evidence path", payload["authority_evidence_path"], maximum=512),
        authority_identity=_bounded("authority identity", payload["authority_identity"], maximum=512),
        authority_evidence_digest=_bounded("authority evidence digest", payload["authority_evidence_digest"], maximum=64),
        approval_reference=_bounded("approval reference", payload["approval_reference"], maximum=512),
        authorized_scope=_bounded("authorized scope", payload["authorized_scope"]),
        result_boundary=_bounded("result boundary", payload["result_boundary"]),
        effects=_bounded_list("authorized effects", payload["effects"]),
        rollback=_bounded("rollback", payload["rollback"]),
        stop_conditions=_bounded_list("stop conditions", payload["stop_conditions"]),
        expires_at=_bounded("authorization expiry", payload["expires_at"], maximum=64),
        nonce=_bounded("authorization nonce", payload["nonce"], maximum=256),
    )
    if normalized["work_id"] != work_id or normalized["authority_boundary"] != authority_boundary:
        raise RegulatedFlowError("authorization is bound to another work item or authority boundary")
    _, normalized_path = _authority_evidence_path(Path("/"), work_id, normalized["authority_evidence_path"])
    if normalized_path != normalized["authority_evidence_path"]:
        raise RegulatedFlowError("authorization evidence path is not canonical")
    if not isinstance(payload["authorization_digest"], str) or payload["authorization_digest"] != normalized["authorization_digest"]:
        raise RegulatedFlowError("authorization digest mismatch")
    return normalized


def _parse_events(data: bytes) -> list[dict[str, Any]]:
    try:
        lines = data.decode().splitlines()
    except UnicodeDecodeError as exc:
        raise RegulatedFlowError("events.jsonl is not UTF-8") from exc
    if not lines:
        raise RegulatedFlowError("event chain is empty")
    previous = "0" * 64
    previous_at: datetime | None = None
    events: list[dict[str, Any]] = []
    fields = {"at", "kind", "payload", "previous_digest", "sequence", "digest"}
    for sequence, line in enumerate(lines, start=1):
        event = _parse_json(line.encode(), f"event {sequence}")
        if set(event) != fields or event.get("sequence") != sequence or event.get("previous_digest") != previous:
            raise RegulatedFlowError(f"event {sequence} has invalid shape, sequence, or predecessor")
        if sequence > len(EVENT_ORDER) or event.get("kind") != EVENT_ORDER[sequence - 1]:
            raise RegulatedFlowError(f"event {sequence} violates init-authorize-verify-close order")
        timestamp = _instant(
            f"event {sequence} timestamp",
            _bounded(f"event {sequence} timestamp", event.get("at"), maximum=64),
        )
        if previous_at is not None and timestamp < previous_at:
            raise RegulatedFlowError(f"event {sequence} timestamp precedes its predecessor")
        if not isinstance(event.get("payload"), dict):
            raise RegulatedFlowError(f"event {sequence} payload must be an object")
        expected = hashlib.sha256(_canonical({key: event[key] for key in fields - {"digest"}})).hexdigest()
        if event.get("digest") != expected:
            raise RegulatedFlowError(f"event {sequence} digest mismatch")
        previous = expected
        previous_at = timestamp
        events.append(event)
    return events


def _replay(work_id: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    initial = events[0]["payload"]
    initial_fields = {"work_id", "duty_kind", "duty_reference", "obligation", "authority_boundary", "retention", "external_anchor_required"}
    if set(initial) != initial_fields or initial.get("work_id") != work_id:
        raise RegulatedFlowError("init payload schema or work identity mismatch")
    if initial["duty_kind"] not in DUTY_KINDS:
        raise RegulatedFlowError("duty_kind must name a concrete regulated duty class")
    duty_reference = _bounded("duty reference", initial["duty_reference"], maximum=256)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9:._/-]{2,255}", duty_reference):
        raise RegulatedFlowError("duty reference must be a concrete portable reference")
    obligation = _bounded("obligation", initial["obligation"])
    if obligation.lower() in {"authentication", "authorization", "auth", "pii", "security", "sensitive data"}:
        raise RegulatedFlowError("a risk signal alone is not a concrete regulated obligation")
    authority = _bounded("authority boundary", initial["authority_boundary"])
    retention = _bounded("retention", initial["retention"], maximum=512)
    if not isinstance(initial["external_anchor_required"], bool):
        raise RegulatedFlowError("external_anchor_required must be boolean")
    state = {
        "schema_version": 3,
        "id": work_id,
        "duty_kind": initial["duty_kind"],
        "duty_reference": duty_reference,
        "obligation": obligation,
        "authority_boundary": authority,
        "retention": retention,
        "external_anchor_required": initial["external_anchor_required"],
        "status": "active",
        "final_event_digest": events[0]["digest"],
        "authorization_digest": "",
    }
    if len(events) >= 2:
        authorization = _validate_authorization(events[1]["payload"], work_id=work_id, authority_boundary=authority)
        state["status"] = "authorized"
        state["authorization_digest"] = authorization["authorization_digest"]
        state["final_event_digest"] = events[1]["digest"]
    if len(events) >= 3:
        verification = events[2]["payload"]
        fields = {"authorization_digest", "result", "summary", "evidence_refs", "observed_scope", "observed_result", "observed_effects"}
        if not isinstance(verification, dict) or set(verification) != fields:
            raise RegulatedFlowError("verify payload schema mismatch")
        if verification["authorization_digest"] != state["authorization_digest"]:
            raise RegulatedFlowError("verification does not bind the current authorization")
        if verification["result"] not in {"pass", "fail"}:
            raise RegulatedFlowError("verification result must be pass or fail")
        _bounded("verification summary", verification["summary"])
        _bounded_list("evidence references", verification["evidence_refs"], required=verification["result"] == "pass")
        observed_scope = _bounded("observed scope", verification["observed_scope"])
        observed_result = _bounded("observed result", verification["observed_result"])
        observed_effects = _bounded_list("observed effects", verification["observed_effects"])
        authorization = _validate_authorization(events[1]["payload"], work_id=work_id, authority_boundary=authority)
        if _instant("verify timestamp", events[2]["at"]) > _instant("authorization expiry", authorization["expires_at"]):
            raise RegulatedFlowError("authorization expired before verification")
        if observed_scope != authorization["authorized_scope"] or observed_result != authorization["result_boundary"]:
            raise RegulatedFlowError("verification scope or result is outside authorization")
        if not set(observed_effects).issubset(authorization["effects"]):
            raise RegulatedFlowError("verification reports an effect outside authorization")
        state["status"] = "verified" if verification["result"] == "pass" else "blocked"
        state["final_event_digest"] = events[2]["digest"]
    if len(events) == 4:
        close = events[3]["payload"]
        if state["status"] != "verified" or set(close) != {"authorization_digest"}:
            raise RegulatedFlowError("close requires one passing verify event")
        if close["authorization_digest"] != state["authorization_digest"]:
            raise RegulatedFlowError("close does not bind the current authorization")
        authorization = _validate_authorization(events[1]["payload"], work_id=work_id, authority_boundary=authority)
        if _instant("close timestamp", events[3]["at"]) > _instant("authorization expiry", authorization["expires_at"]):
            raise RegulatedFlowError("authorization expired before close")
        state["status"] = "closed"
        state["final_event_digest"] = events[3]["digest"]
    return state


def _anchor(state: dict[str, Any]) -> dict[str, Any]:
    anchor = {
        "schema_version": 3,
        "id": state["id"],
        "final_event_digest": state["final_event_digest"],
        "authorization_digest": state["authorization_digest"],
        "external_anchor_required": state["external_anchor_required"],
    }
    anchor["anchor_digest"] = hashlib.sha256(_canonical(anchor)).hexdigest()
    return anchor


def _load(
    root: Path,
    work_id: str,
    safe_io: types.ModuleType,
    root_fd: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[Path, Any], dict[Path, Any]]:
    state_path, events_path, anchor_path = _work_paths(root, work_id)
    snapshots = {path: safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) for path in (state_path, events_path, anchor_path)}
    if not snapshots[state_path].exists or not snapshots[events_path].exists:
        raise RegulatedFlowError(f"regulated work item does not exist: {work_id}")
    state = _parse_json(safe_io.read_bytes_nofollow_pinned(state_path, root=root, root_fd=root_fd), "state.json")
    events = _parse_events(safe_io.read_bytes_nofollow_pinned(events_path, root=root, root_fd=root_fd))
    replayed = _replay(work_id, events)
    if state != replayed:
        raise RegulatedFlowError("state.json differs from strict event replay")
    read_preconditions: dict[Path, Any] = {}
    if len(events) >= 2:
        authorization = _validate_authorization(
            events[1]["payload"],
            work_id=work_id,
            authority_boundary=state["authority_boundary"],
        )
        evidence_path, evidence_reference = _authority_evidence_path(
            root,
            work_id,
            authorization["authority_evidence_path"],
        )
        evidence, evidence_digest, evidence_snapshot = _load_authority_evidence(
            evidence_path,
            work_id=work_id,
            authority_boundary=state["authority_boundary"],
            root=root,
            safe_io=safe_io,
            root_fd=root_fd,
        )
        read_preconditions[evidence_path] = evidence_snapshot
        if _authorization_from_evidence(
            evidence,
            authority_evidence_path=evidence_reference,
            authority_evidence_digest=evidence_digest,
        ) != authorization:
            raise RegulatedFlowError("current target-owned authority evidence differs from the bound authorization")
    if any(safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) != snapshots[path] for path in (state_path, events_path, anchor_path)):
        raise RegulatedFlowError("regulated files changed while reading")
    if state["status"] == "closed":
        if not snapshots[anchor_path].exists:
            raise RegulatedFlowError("closed work item is missing its local anchor")
        anchor = _parse_json(
            safe_io.read_bytes_nofollow_pinned(anchor_path, root=root, root_fd=root_fd),
            "anchor.json",
        )
        if anchor != _anchor(state):
            raise RegulatedFlowError("local anchor differs from strict replay")
    elif snapshots[anchor_path].exists:
        raise RegulatedFlowError("open work item unexpectedly has an anchor")
    return state, events, snapshots, read_preconditions


def _publish(
    root: Path,
    safe_io: types.ModuleType,
    root_fd: int,
    updates: dict[Path, bytes],
    snapshots: dict[Path, Any],
    *,
    read_preconditions: dict[Path, Any] | None = None,
) -> None:
    safe_io.atomic_batch_write_cas(
        updates,
        {path: snapshots[path] for path in updates},
        root=root,
        lock_name=".devflow/run/regulated.lock",
        pinned_root_fd=root_fd,
        read_preconditions=read_preconditions,
    )


def _result(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


def command_init(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    state_path, events_path, anchor_path = _work_paths(root, args.id)
    snapshots = {path: safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) for path in (state_path, events_path, anchor_path)}
    if any(snapshot.exists for snapshot in snapshots.values()):
        raise RegulatedFlowError(f"regulated work item already exists: {args.id}")
    payload = {
        "work_id": args.id,
        "duty_kind": args.duty_kind,
        "duty_reference": _bounded("duty reference", args.duty_reference, maximum=256),
        "obligation": _bounded("obligation", args.obligation),
        "authority_boundary": _bounded("authority", args.authority),
        "retention": _bounded("retention", args.retention, maximum=512),
        "external_anchor_required": args.external_anchor_required,
    }
    event = _event(1, "init", _now(), payload, "0" * 64)
    state = _replay(args.id, [event])
    _publish(root, safe_io, root_fd, {state_path: _canonical(state), events_path: _canonical(event)}, snapshots)
    _result({"id": args.id, "status": state["status"], "final_event_digest": event["digest"]})
    return 0


def command_authorize(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    state_path, events_path, _ = _work_paths(root, args.id)
    state, events, snapshots, read_preconditions = _load(root, args.id, safe_io, root_fd)
    if state["status"] != "active" or len(events) != 1:
        raise RegulatedFlowError(f"cannot authorize from status {state['status']}")
    evidence_path, evidence_reference = _authority_evidence_path(root, args.id, args.authority_evidence)
    evidence, evidence_digest, evidence_snapshot = _load_authority_evidence(
        evidence_path,
        work_id=args.id,
        authority_boundary=state["authority_boundary"],
        root=root,
        safe_io=safe_io,
        root_fd=root_fd,
    )
    read_preconditions[evidence_path] = evidence_snapshot
    payload = _authorization_from_evidence(
        evidence,
        authority_evidence_path=evidence_reference,
        authority_evidence_digest=evidence_digest,
    )
    event_at = _now()
    if _instant("authorization timestamp", event_at) > _instant("authorization expiry", payload["expires_at"]):
        raise RegulatedFlowError("authorization evidence is already expired")
    event = _event(2, "authorize", event_at, payload, events[-1]["digest"])
    next_events = [*events, event]
    next_state = _replay(args.id, next_events)
    _publish(
        root,
        safe_io,
        root_fd,
        {state_path: _canonical(next_state), events_path: b"".join(_canonical(item) for item in next_events)},
        snapshots,
        read_preconditions=read_preconditions,
    )
    _result({"id": args.id, "status": next_state["status"], "authorization_digest": payload["authorization_digest"]})
    return 0


def command_verify(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    state_path, events_path, _ = _work_paths(root, args.id)
    state, events, snapshots, read_preconditions = _load(root, args.id, safe_io, root_fd)
    if state["status"] != "authorized" or len(events) != 2:
        raise RegulatedFlowError(f"cannot verify from status {state['status']}")
    payload = {
        "authorization_digest": state["authorization_digest"],
        "result": args.result,
        "summary": _bounded("summary", args.summary),
        "evidence_refs": _bounded_list("evidence references", args.evidence_ref, required=False),
        "observed_scope": _bounded("observed scope", args.observed_scope),
        "observed_result": _bounded("observed result", args.observed_result),
        "observed_effects": _bounded_list("observed effects", args.observed_effect),
    }
    event = _event(3, "verify", _now(), payload, events[-1]["digest"])
    next_events = [*events, event]
    next_state = _replay(args.id, next_events)
    _publish(
        root,
        safe_io,
        root_fd,
        {state_path: _canonical(next_state), events_path: b"".join(_canonical(item) for item in next_events)},
        snapshots,
        read_preconditions=read_preconditions,
    )
    _result({"id": args.id, "status": next_state["status"], "authorization_digest": state["authorization_digest"]})
    return 0 if args.result == "pass" else 1


def command_close(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    state_path, events_path, anchor_path = _work_paths(root, args.id)
    state, events, snapshots, read_preconditions = _load(root, args.id, safe_io, root_fd)
    if state["status"] != "verified" or len(events) != 3:
        raise RegulatedFlowError(f"cannot close from status {state['status']}")
    event = _event(4, "close", _now(), {"authorization_digest": state["authorization_digest"]}, events[-1]["digest"])
    next_events = [*events, event]
    next_state = _replay(args.id, next_events)
    anchor = _anchor(next_state)
    _publish(
        root,
        safe_io,
        root_fd,
        {
            state_path: _canonical(next_state),
            events_path: b"".join(_canonical(item) for item in next_events),
            anchor_path: _canonical(anchor),
        },
        snapshots,
        read_preconditions=read_preconditions,
    )
    handoff = None
    if next_state["external_anchor_required"]:
        handoff = {
            "digest": anchor["anchor_digest"],
            "record": f"work/{args.id}/regulated/anchor.json",
            "operation": "target-owned-authorized-append-only-process",
        }
    _result({"id": args.id, "status": "closed", "local_anchor": anchor, "external_anchor_handoff": handoff})
    return 0


def command_check(args: argparse.Namespace, root: Path, safe_io: types.ModuleType, root_fd: int) -> int:
    state, events, _, _ = _load(root, args.id, safe_io, root_fd)
    _result(
        {
            "id": args.id,
            "status": state["status"],
            "events": len(events),
            "authorization_digest": state["authorization_digest"],
            "final_event_digest": state["final_event_digest"],
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="trusted repository root")
    subparsers = parser.add_subparsers(dest="command", required=True)
    init = subparsers.add_parser("init")
    init.add_argument("--id", required=True)
    init.add_argument("--duty-kind", choices=sorted(DUTY_KINDS), required=True)
    init.add_argument("--duty-reference", required=True)
    init.add_argument("--obligation", required=True)
    init.add_argument("--authority", required=True)
    init.add_argument("--retention", required=True)
    init.add_argument("--external-anchor-required", action="store_true")
    authorize = subparsers.add_parser("authorize")
    authorize.add_argument("--id", required=True)
    authorize.add_argument(
        "--authority-evidence",
        required=True,
        help="pre-existing target-owned repository-confined authorization JSON",
    )
    verify = subparsers.add_parser("verify")
    verify.add_argument("--id", required=True)
    verify.add_argument("--result", choices=["pass", "fail"], required=True)
    verify.add_argument("--summary", required=True)
    verify.add_argument("--evidence-ref", action="append", default=[])
    verify.add_argument("--observed-scope", required=True)
    verify.add_argument("--observed-result", required=True)
    verify.add_argument("--observed-effect", action="append", required=True)
    close = subparsers.add_parser("close")
    close.add_argument("--id", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("--id", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).absolute()
    try:
        safe_io = _safe_io(root)
        with safe_io.trusted_root(root) as root_fd:
            identity = (os.fstat(root_fd).st_dev, os.fstat(root_fd).st_ino)
            if identity != safe_io._bootstrap_root_identity:
                raise RegulatedFlowError("repository root changed after runtime bootstrap")
            handlers = {
                "init": command_init,
                "authorize": command_authorize,
                "verify": command_verify,
                "close": command_close,
                "check": command_check,
            }
            return int(handlers[args.command](args, root, safe_io, root_fd))
    except Exception as exc:  # CLI boundary: dynamic safe-I/O errors are bounded rejections.
        print(json.dumps({"error": str(exc), "status": "rejected"}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
