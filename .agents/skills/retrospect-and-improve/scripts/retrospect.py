#!/usr/bin/env python3
"""Validate one evidenced, bounded, non-applied improvement candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import types
from datetime import date
from pathlib import Path
from typing import Any

TRIGGERS = {"escaped-defect", "incident", "rollback", "recurring-cost"}
NON_TRIGGERS = {
    "regulated-close",
    "periodic-audit",
    "ordinary-session",
    "transient-check-failure",
    "repeated-ci-repair",
    "template-gap",
}
REPEATED_TRIGGERS = {"recurring-cost"}
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
MAX_TEXT = 2_000
MAX_EVIDENCE = 16
MAX_ALTERNATIVES = 8
SKILL_NAMES = {
    "adversarial-review",
    "author-lifecycle-docs",
    "authorize-autonomous-execution",
    "calibrated-collaborative-listening",
    "chat-first-development",
    "design-frontend-experience",
    "elicit-frontend-requirements",
    "generate-implementation-design",
    "govern-development-request",
    "implement-frontend-experience",
    "inspect-quality-gates",
    "japanese-git-commit-gitmoji",
    "maintain-canonical-requirements",
    "maintain-reference-repository",
    "retrospect-and-improve",
    "right-size-execution",
    "test-frontend-experience",
    "verify-against-engineering-standards",
}
OPERATIONS = {
    "narrow-trigger",
    "add-bounded-diagnostic",
    "clarify-contract",
    "add-focused-test",
    "remove-redundant-instruction",
}
FORBIDDEN_CHANGE_PATTERNS = {
    "disable check",
    "disable test",
    "remove check",
    "remove test",
    "bypass",
    "skip authorization",
    "allow all",
    "expand authority",
    "grant authority",
    "create ci",
    "add ci workflow",
    "merge rule",
    "branch protection",
    "required check",
}


class RetrospectError(RuntimeError):
    """An improvement input was unsafe, unbounded, or insufficiently evidenced."""


def _bootstrap_module(path: Path, *, root: Path) -> types.ModuleType:
    root = root.absolute()
    path = path.absolute()
    try:
        parts = path.relative_to(root).parts
    except ValueError as exc:
        raise RetrospectError(f"runtime escapes repository root: {path}") from exc
    portable = sys.modules.get("_dev_standard_portable_imports")
    if portable is not None:
        return portable.load_relative(
            "/".join(parts),
            "dev_standard_retrospect_safe_io",
        )
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
                raise RetrospectError(f"runtime is not a regular file: {path}")
            chunks: list[bytes] = []
            while chunk := os.read(source_descriptor, 1024 * 1024):
                chunks.append(chunk)
        finally:
            os.close(source_descriptor)
    finally:
        os.close(descriptor)
    module = types.ModuleType("dev_standard_retrospect_safe_io")
    module.__file__ = str(path)
    module._bootstrap_root_identity = root_identity
    sys.modules[module.__name__] = module
    exec(compile(b"".join(chunks), str(path), "exec"), module.__dict__)
    return module


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _bounded(label: str, value: Any, *, maximum: int = MAX_TEXT) -> str:
    if not isinstance(value, str):
        raise RetrospectError(f"{label} must be text")
    value = value.strip()
    if not value or len(value) > maximum:
        raise RetrospectError(f"{label} must contain 1..{maximum} characters")
    return value


def _text_object(label: str, value: Any, fields: set[str]) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != fields:
        raise RetrospectError(f"{label} fields must be exact: {sorted(fields)}")
    return {field: _bounded(f"{label}.{field}", value[field]) for field in sorted(fields)}


def _evidence(value: Any) -> list[str]:
    if not isinstance(value, list) or len(value) > MAX_EVIDENCE:
        raise RetrospectError(f"consequence.evidence_refs must contain 0..{MAX_EVIDENCE} entries")
    evidence = [_bounded("evidence reference", item, maximum=512) for item in value]
    if len(set(evidence)) != len(evidence):
        raise RetrospectError("evidence references must be unique")
    return evidence


def _alternatives(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_ALTERNATIVES:
        raise RetrospectError(f"alternatives must contain 1..{MAX_ALTERNATIVES} entries")
    alternatives = [_text_object("alternative", item, {"option", "why_insufficient"}) for item in value]
    if len({item["option"] for item in alternatives}) != len(alternatives):
        raise RetrospectError("alternative options must be unique")
    return alternatives


def _repo_path(root: Path, raw: str, *, output: bool = False) -> Path:
    candidate = Path(raw)
    if candidate.is_absolute() or any(part in {"", ".", ".."} for part in candidate.parts):
        raise RetrospectError("paths must be relative without dot segments")
    if output and (len(candidate.parts) <= 2 or candidate.parts[:2] != (".devflow", "run")):
        raise RetrospectError("output must be below .devflow/run")
    return root.absolute() / candidate


def _load_input(path: Path, *, root: Path, safe_io: types.ModuleType, root_fd: int) -> tuple[dict[str, Any], Any]:
    before = safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd)
    if not before.exists:
        raise RetrospectError("input does not exist")
    try:
        value = json.loads(safe_io.read_bytes_nofollow_pinned(path, root=root, root_fd=root_fd))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RetrospectError("input must be valid UTF-8 JSON") from exc
    if safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd) != before:
        raise RetrospectError("input changed while reading")
    fields = {
        "schema_version",
        "trigger",
        "consequence",
        "target",
        "problem",
        "alternatives",
        "proposal",
        "safety_claims",
        "expected",
        "evaluation",
        "rollback",
        "sunset",
    }
    if not isinstance(value, dict) or set(value) != fields or value.get("schema_version") != 2:
        raise RetrospectError("input must match the exact schema_version=2 candidate shape")
    trigger = value["trigger"]
    if trigger not in TRIGGERS | NON_TRIGGERS:
        raise RetrospectError("trigger is not recognized")
    consequence = value["consequence"]
    consequence_fields = {"kind", "description", "materiality", "evidence_refs"}
    if not isinstance(consequence, dict) or set(consequence) != consequence_fields:
        raise RetrospectError("consequence fields must be exact")
    if consequence["kind"] not in {"user-impact", "security-impact", "operational-impact", "material-cost"}:
        raise RetrospectError("consequence.kind is not consequential")
    if consequence["materiality"] not in {"material", "major", "critical"}:
        raise RetrospectError("consequence.materiality must be material, major, or critical")
    normalized_consequence = {
        "kind": consequence["kind"],
        "description": _bounded("consequence.description", consequence["description"]),
        "materiality": consequence["materiality"],
        "evidence_refs": _evidence(consequence["evidence_refs"]),
    }
    target = _text_object("target", value["target"], {"skill", "behavior"})
    if not ID_PATTERN.fullmatch(target["skill"]) or target["skill"] not in SKILL_NAMES:
        raise RetrospectError("target.skill must name exactly one existing Skill")
    problem = _text_object("problem", value["problem"], {"observed", "root_cause_hypothesis"})
    alternatives = _alternatives(value["alternatives"])
    proposal_value = value["proposal"]
    proposal_fields = {"operation", "change", "activation_trigger", "scope", "control_effect", "authority_effect", "affected_controls", "authority_delta"}
    if not isinstance(proposal_value, dict) or set(proposal_value) != proposal_fields:
        raise RetrospectError("proposal fields must be exact")
    proposal = {
        field: _bounded(f"proposal.{field}", proposal_value[field])
        for field in ["operation", "change", "activation_trigger", "scope", "control_effect", "authority_effect"]
    }
    if proposal["operation"] not in OPERATIONS:
        raise RetrospectError("proposal.operation is not an allowed bounded operation")
    lowered_change = proposal["change"].lower()
    if any(pattern in lowered_change for pattern in FORBIDDEN_CHANGE_PATTERNS):
        raise RetrospectError("proposal.change attempts control weakening, authority expansion, or repository policy creation")
    controls = value["proposal"]["affected_controls"]
    if not isinstance(controls, list) or not 1 <= len(controls) <= 16:
        raise RetrospectError("proposal.affected_controls must contain 1..16 identifiers")
    proposal["affected_controls"] = [_bounded("affected control", control, maximum=128) for control in controls]
    if len(set(proposal["affected_controls"])) != len(proposal["affected_controls"]):
        raise RetrospectError("affected controls must be unique")
    delta = _text_object("proposal.authority_delta", proposal_value["authority_delta"], {"kind", "before", "after"})
    if delta["kind"] not in {"none", "narrower"}:
        raise RetrospectError("authority delta must be none or narrower")
    if (delta["kind"] == "none" and delta["before"] != delta["after"]) or (delta["kind"] == "narrower" and delta["before"] == delta["after"]):
        raise RetrospectError("authority delta is internally inconsistent")
    proposal["authority_delta"] = delta
    if proposal["scope"] != "one-skill-one-behavior":
        raise RetrospectError("proposal scope must remain one-skill-one-behavior")
    if proposal["control_effect"] != "preserve-or-strengthen":
        raise RetrospectError("proposal may not weaken checks or controls")
    if proposal["authority_effect"] != "unchanged-or-narrower":
        raise RetrospectError("proposal may not expand authority")
    safety = value["safety_claims"]
    safety_fields = {"weakens_checks", "expands_authority", "creates_ci_or_merge_policy", "auto_apply"}
    if not isinstance(safety, dict) or set(safety) != safety_fields or any(safety.get(field) is not False for field in safety_fields):
        raise RetrospectError("all safety claims must be explicit false booleans")
    expected = _text_object("expected", value["expected"], {"benefit", "cost"})
    evaluation_value = value["evaluation"]
    evaluation_fields = {"metric", "unit", "baseline", "target", "direction", "evidence_source", "shadow_period_days", "max_observations"}
    if not isinstance(evaluation_value, dict) or set(evaluation_value) != evaluation_fields:
        raise RetrospectError("evaluation fields must be exact and measurable")
    for numeric in ["baseline", "target"]:
        if isinstance(evaluation_value[numeric], bool) or not isinstance(evaluation_value[numeric], (int, float)):
            raise RetrospectError(f"evaluation.{numeric} must be numeric")
    for numeric, upper in [("shadow_period_days", 365), ("max_observations", 10_000)]:
        if isinstance(evaluation_value[numeric], bool) or not isinstance(evaluation_value[numeric], int) or not 1 <= evaluation_value[numeric] <= upper:
            raise RetrospectError(f"evaluation.{numeric} is outside its bounded range")
    direction = evaluation_value["direction"]
    if direction not in {"increase", "decrease", "zero"}:
        raise RetrospectError("evaluation.direction is invalid")
    baseline, target_value = float(evaluation_value["baseline"]), float(evaluation_value["target"])
    if (
        (direction == "increase" and target_value <= baseline)
        or (direction == "decrease" and target_value >= baseline)
        or (direction == "zero" and target_value != 0)
    ):
        raise RetrospectError("evaluation target does not match its direction")
    evaluation = {
        "metric": _bounded("evaluation.metric", evaluation_value["metric"], maximum=256),
        "unit": _bounded("evaluation.unit", evaluation_value["unit"], maximum=64),
        "baseline": evaluation_value["baseline"],
        "target": evaluation_value["target"],
        "direction": direction,
        "evidence_source": _bounded("evaluation.evidence_source", evaluation_value["evidence_source"], maximum=512),
        "shadow_period_days": evaluation_value["shadow_period_days"],
        "max_observations": evaluation_value["max_observations"],
    }
    rollback = _text_object("rollback", value["rollback"], {"trigger", "action"})
    if rollback["action"].lower() in {"never", "none", "n/a", "not applicable"}:
        raise RetrospectError("rollback.action must be executable")
    sunset = _text_object("sunset", value["sunset"], {"review_at", "remove_if"})
    try:
        date.fromisoformat(sunset["review_at"])
    except ValueError as exc:
        raise RetrospectError("sunset.review_at must be an ISO date") from exc
    return (
        {
            "schema_version": 2,
            "trigger": trigger,
            "consequence": normalized_consequence,
            "target": target,
            "problem": problem,
            "alternatives": alternatives,
            "proposal": proposal,
            "safety_claims": {field: False for field in sorted(safety_fields)},
            "expected": expected,
            "evaluation": evaluation,
            "rollback": rollback,
            "sunset": sunset,
        },
        before,
    )


def _evaluate(value: dict[str, Any]) -> dict[str, Any]:
    trigger = value["trigger"]
    evidence = value["consequence"]["evidence_refs"]
    if trigger in NON_TRIGGERS:
        return {
            "schema_version": 2,
            "status": "not_triggered",
            "trigger": trigger,
            "reason": "no consequential defect, incident, rollback, or recurring cost trigger",
        }
    if not evidence:
        return {"schema_version": 2, "status": "not_triggered", "trigger": trigger, "reason": "direct consequence evidence is missing"}
    if trigger in REPEATED_TRIGGERS and len(set(evidence)) < 2:
        return {
            "schema_version": 2,
            "status": "not_triggered",
            "trigger": trigger,
            "reason": "recurring cost needs at least two distinct observations",
        }
    candidate = {key: value[key] for key in value if key != "schema_version"}
    return {
        "schema_version": 2,
        "status": "candidate",
        "candidate_id": hashlib.sha256(_canonical(candidate)).hexdigest()[:16],
        "auto_apply": False,
        "candidate": candidate,
    }


def _write(
    path: Path,
    value: dict[str, Any],
    *,
    root: Path,
    safe_io: types.ModuleType,
    root_fd: int,
    read_preconditions: dict[Path, Any],
) -> None:
    before = safe_io.snapshot_file_pinned(path, root=root, root_fd=root_fd)
    if before.exists:
        raise RetrospectError("output already exists")
    safe_io.atomic_batch_write_cas(
        {path: json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode() + b"\n"},
        {path: before},
        root=root,
        lock_name=".devflow/run/retrospect.lock",
        pinned_root_fd=root_fd,
        read_preconditions=read_preconditions,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--input", required=True, help="repository-confined candidate input JSON")
    parser.add_argument("--json-out", help="optional .devflow/run result JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.root).absolute()
    try:
        safe_io = _bootstrap_module(root / "tools" / "safe_io.py", root=root)
        with safe_io.trusted_root(root) as root_fd:
            identity = (os.fstat(root_fd).st_dev, os.fstat(root_fd).st_ino)
            if identity != safe_io._bootstrap_root_identity:
                raise RetrospectError("repository root changed after runtime bootstrap")
            input_path = _repo_path(root, args.input)
            candidate, input_snapshot = _load_input(input_path, root=root, safe_io=safe_io, root_fd=root_fd)
            result = _evaluate(candidate)
            if safe_io.snapshot_file_pinned(input_path, root=root, root_fd=root_fd) != input_snapshot:
                raise RetrospectError("input changed after evaluation")
            if args.json_out:
                _write(
                    _repo_path(root, args.json_out, output=True),
                    result,
                    root=root,
                    safe_io=safe_io,
                    root_fd=root_fd,
                    read_preconditions={input_path: input_snapshot},
                )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
    except Exception as exc:  # CLI boundary: dynamic safe-I/O errors become bounded rejections.
        print(json.dumps({"error": str(exc), "status": "rejected"}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
