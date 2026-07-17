#!/usr/bin/env python3
"""Validate, update, and render the durable atomic requirements catalog."""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


class SpecError(RuntimeError):
    pass


ID_RE = re.compile(r"^[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+$")
ACTION_RE = re.compile(r"^[a-z][a-z0-9]*$")
STATUSES = {"active", "retired"}
TYPES = {"functional", "quality", "constraint", "interface", "data", "operational"}
TRACE_KEYS = {"design", "implementation", "tests", "standards"}
REQUIRED = {
    "id", "revision", "status", "type", "title", "subject", "action", "object",
    "rationale", "source_refs", "acceptance_criteria", "verification", "traces", "last_changed_by",
}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SpecError(f"cannot read JSON {path}: {exc}") from exc


def nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpecError(f"{label} must be a non-empty string")
    return value.strip()


def validate_requirement(item: Any, seen_ac: set[str]) -> None:
    if not isinstance(item, dict):
        raise SpecError("each requirement must be an object")
    missing = REQUIRED - set(item)
    extra = set(item) - REQUIRED - {"retirement_reason", "superseded_by"}
    if missing or extra:
        raise SpecError(f"requirement fields invalid: missing={sorted(missing)} extra={sorted(extra)}")
    rid = nonempty(item["id"], "id")
    if not ID_RE.fullmatch(rid):
        raise SpecError(f"invalid requirement ID: {rid}")
    if not isinstance(item["revision"], int) or item["revision"] < 1:
        raise SpecError(f"{rid}: revision must be a positive integer")
    if item["status"] not in STATUSES or item["type"] not in TYPES:
        raise SpecError(f"{rid}: invalid status or type")
    for key in ["title", "subject", "object", "rationale", "last_changed_by"]:
        value = nonempty(item[key], f"{rid}.{key}")
        if key in {"subject", "object"} and ("\n" in value or ";" in value or value.startswith(("-", "*"))):
            raise SpecError(f"{rid}.{key}: obligation must be one line and one clause")
    action = nonempty(item["action"], f"{rid}.action")
    if not ACTION_RE.fullmatch(action):
        raise SpecError(f"{rid}.action must be one normalized verb token")
    if not isinstance(item["source_refs"], list) or not item["source_refs"]:
        raise SpecError(f"{rid}: source_refs required")
    if any(not isinstance(value, str) or not value.strip() for value in item["source_refs"]):
        raise SpecError(f"{rid}: source_refs must contain non-empty strings")
    criteria = item["acceptance_criteria"]
    if not isinstance(criteria, list) or not criteria:
        raise SpecError(f"{rid}: acceptance_criteria required")
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != {"id", "given", "when", "then"}:
            raise SpecError(f"{rid}: each criterion needs id/given/when/then only")
        cid = nonempty(criterion["id"], f"{rid}.criterion.id")
        if cid in seen_ac:
            raise SpecError(f"duplicate acceptance criterion: {cid}")
        seen_ac.add(cid)
        for key in ["given", "when", "then"]:
            nonempty(criterion[key], f"{cid}.{key}")
    verification = item["verification"]
    if not isinstance(verification, dict) or set(verification) != {"method", "evidence"}:
        raise SpecError(f"{rid}: verification needs method/evidence")
    nonempty(verification["method"], f"{rid}.verification.method")
    nonempty(verification["evidence"], f"{rid}.verification.evidence")
    traces = item["traces"]
    if not isinstance(traces, dict) or set(traces) != TRACE_KEYS:
        raise SpecError(f"{rid}: traces must contain {sorted(TRACE_KEYS)}")
    if any(not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values) for values in traces.values()):
        raise SpecError(f"{rid}: trace values must be string lists")
    if item["status"] == "retired" and not str(item.get("retirement_reason") or "").strip():
        raise SpecError(f"{rid}: retired requirement needs retirement_reason")


def validate_catalog(catalog: Any) -> dict[str, Any]:
    if not isinstance(catalog, dict) or set(catalog) != {"schema_version", "catalog_revision", "product", "updated_at", "requirements"}:
        raise SpecError("catalog must contain schema_version/catalog_revision/product/updated_at/requirements only")
    if catalog["schema_version"] != 1 or not isinstance(catalog["catalog_revision"], int) or catalog["catalog_revision"] < 0:
        raise SpecError("invalid schema or catalog revision")
    nonempty(catalog["product"], "product")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", nonempty(catalog["updated_at"], "updated_at")):
        raise SpecError("updated_at must be YYYY-MM-DD")
    if not isinstance(catalog["requirements"], list):
        raise SpecError("requirements must be a list")
    seen: set[str] = set()
    seen_ac: set[str] = set()
    for item in catalog["requirements"]:
        validate_requirement(item, seen_ac)
        if item["id"] in seen:
            raise SpecError(f"duplicate requirement: {item['id']}")
        seen.add(item["id"])
    return catalog


def render(catalog: dict[str, Any]) -> str:
    lines = [
        "<!-- AUTO-GENERATED by specflow.py; edit spec/requirements/requirements.json instead. -->",
        f"# {catalog['product']} requirements",
        "",
        f"- Catalog revision: {catalog['catalog_revision']}",
        f"- Updated: {catalog['updated_at']}",
        "- Authoritative source: `spec/requirements/requirements.json`",
        "",
        "| ID | Rev | Status | Type | Atomic obligation | Verification |",
        "|---|---:|---|---|---|---|",
    ]
    for item in catalog["requirements"]:
        obligation = f"{item['subject']} **{item['action']}** {item['object']}"
        lines.append(f"| `{item['id']}` | {item['revision']} | {item['status']} | {item['type']} | {obligation} | {item['verification']['method']} |")
    for item in catalog["requirements"]:
        lines += ["", f"## {item['id']}: {item['title']}", "", f"{item['subject']} **{item['action']}** {item['object']}.", "", f"Rationale: {item['rationale']}", "", "Acceptance criteria:"]
        for criterion in item["acceptance_criteria"]:
            lines.append(f"- `{criterion['id']}` Given {criterion['given']}; when {criterion['when']}; then {criterion['then']}.")
        lines += ["", f"Source: {', '.join(item['source_refs'])}", f"Verification evidence: {item['verification']['evidence']}"]
        trace_values = [f"{key}={','.join(values) or '-'}" for key, values in item["traces"].items()]
        lines.append("Trace: " + "; ".join(trace_values))
        if item["status"] == "retired":
            lines.append(f"Retirement: {item['retirement_reason']}")
    return "\n".join(lines) + "\n"


def atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def apply_change(catalog: dict[str, Any], change: Any) -> dict[str, Any]:
    if not isinstance(change, dict) or set(change) != {"base_catalog_revision", "changed_at", "work_item", "operations"}:
        raise SpecError("change needs base_catalog_revision/changed_at/work_item/operations")
    if change["base_catalog_revision"] != catalog["catalog_revision"]:
        raise SpecError("stale catalog revision; no changes written")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", nonempty(change["changed_at"], "changed_at")):
        raise SpecError("changed_at must be YYYY-MM-DD")
    work_item = nonempty(change["work_item"], "work_item")
    if not isinstance(change["operations"], list) or not change["operations"]:
        raise SpecError("operations must be a non-empty list")
    candidate = copy.deepcopy(catalog)
    by_id = {item["id"]: item for item in candidate["requirements"]}
    for operation in change["operations"]:
        op = operation.get("op") if isinstance(operation, dict) else None
        if op == "add":
            if set(operation) != {"op", "requirement"}:
                raise SpecError("add operation needs op/requirement only")
            item = copy.deepcopy(operation.get("requirement"))
            if not isinstance(item, dict) or item.get("id") in by_id:
                raise SpecError("add requires a new requirement")
            item["last_changed_by"] = work_item
            by_id[item["id"]] = item
            candidate["requirements"].append(item)
        elif op == "update":
            if set(operation) != {"op", "id", "expected_revision", "changes"}:
                raise SpecError("update operation needs op/id/expected_revision/changes only")
            rid = operation.get("id")
            item = by_id.get(rid)
            if item is None or operation.get("expected_revision") != item["revision"]:
                raise SpecError(f"{rid}: stale or missing requirement")
            changes = operation.get("changes")
            if not isinstance(changes, dict) or {"id", "revision"}.intersection(changes):
                raise SpecError(f"{rid}: invalid update fields")
            item.update(copy.deepcopy(changes))
            item["revision"] += 1
            item["last_changed_by"] = work_item
        elif op == "retire":
            if set(operation) != {"op", "id", "expected_revision", "reason"}:
                raise SpecError("retire operation needs op/id/expected_revision/reason only")
            rid = operation.get("id")
            item = by_id.get(rid)
            if item is None or operation.get("expected_revision") != item["revision"]:
                raise SpecError(f"{rid}: stale or missing requirement")
            item.update({"status": "retired", "retirement_reason": nonempty(operation.get("reason"), f"{rid}.reason"), "revision": item["revision"] + 1, "last_changed_by": work_item})
        else:
            raise SpecError(f"unsupported operation: {op}")
    candidate["requirements"] = sorted(candidate["requirements"], key=lambda item: item["id"])
    candidate["catalog_revision"] += 1
    candidate["updated_at"] = change["changed_at"]
    return validate_catalog(candidate)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    for name in ["validate", "generate", "check"]:
        cmd = sub.add_parser(name)
        cmd.add_argument("--spec", type=Path, default=Path("spec/requirements/requirements.json"))
        if name != "validate":
            cmd.add_argument("--out", type=Path, default=Path("docs/requirements/REQUIREMENTS.md"))
    apply = sub.add_parser("apply")
    apply.add_argument("--spec", type=Path, default=Path("spec/requirements/requirements.json"))
    apply.add_argument("--change", required=True, type=Path)
    apply.add_argument("--out", type=Path, default=Path("docs/requirements/REQUIREMENTS.md"))
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        catalog = validate_catalog(read_json(args.spec))
        if args.command == "validate":
            print(f"requirements valid: {len(catalog['requirements'])} items / revision {catalog['catalog_revision']}")
        elif args.command == "generate":
            atomic_text(args.out, render(catalog))
            print(f"generated {args.out}")
        elif args.command == "check":
            if not args.out.is_file() or args.out.read_text(encoding="utf-8") != render(catalog):
                raise SpecError(f"generated requirements drift: {args.out}")
            print(f"requirements docs current: {args.out}")
        else:
            candidate = apply_change(catalog, read_json(args.change))
            atomic_text(args.spec, canonical_json(candidate))
            atomic_text(args.out, render(candidate))
            print(f"applied revision {candidate['catalog_revision']} and generated {args.out}")
        return 0
    except SpecError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
