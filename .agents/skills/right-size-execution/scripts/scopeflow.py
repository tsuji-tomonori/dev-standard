#!/usr/bin/env python3
"""Deterministic Estimate/Execute/Expand ledger for repository work."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = SKILL_ROOT / "assets" / "execution-policy.json"
BENCHMARK_PATH = SKILL_ROOT / "assets" / "benchmark-cases.json"

RISK_KEYWORDS = {
    "security": ["security", "セキュリティ", "脆弱性"],
    "authentication": ["authentication", "認証"],
    "authorization": ["authorization", "認可", "権限"],
    "data-loss": ["data deletion", "data loss", "データ削除", "データ損失"],
    "database-schema": ["database schema", "db schema", "DBスキーマ", "テーブル定義"],
    "migration": ["migration", "マイグレーション"],
    "public-api": ["public api", "公開API", "API contract"],
    "event-contract": ["event contract", "イベント契約"],
    "iac": ["iac", "cloudformation", "terraform", "cdk", "インフラ"],
    "network": ["network", "ネットワーク", "vpc"],
    "dependency": ["dependency", "依存ライブラリ", "依存関係"],
    "lockfile": ["lockfile", "lock file", "ロックファイル"],
    "durable-requirements": ["durable requirement", "永続要件", "正本要件"],
    "governance": ["governance", "ガバナンス", "実行基盤"],
    "checklist": ["checklist", "チェックリスト"],
    "generator": ["generator", "生成器"],
    "confidential": ["confidential", "機密"],
    "pii": ["pii", "個人情報", "個人データ"],
    "external-side-effect": ["external side effect", "外部副作用", "送信", "deploy", "デプロイ"],
    "irreversible": ["irreversible", "不可逆", "rollback困難", "ロールバック困難"],
}


class ScopeError(RuntimeError):
    pass


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    value = read_json(path)
    required = {"schema_version", "selector_version", "risk_floor_l3", "levels", "expansion_order"}
    missing = required - value.keys()
    if missing:
        raise ScopeError(f"policy missing: {', '.join(sorted(missing))}")
    return value


def csv_values(value: str | None) -> list[str]:
    return sorted({item.strip() for item in (value or "").split(",") if item.strip()})


def infer_risk_tags(request: str) -> list[str]:
    lowered = request.lower()
    return sorted(tag for tag, words in RISK_KEYWORDS.items() if any(word.lower() in lowered for word in words))


def estimate_scope(
    request: str,
    *,
    expected_files: int,
    domains: list[str],
    artifact_tags: list[str],
    risk_tags: list[str],
    metadata_probes: int = 0,
    confidence: float | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = policy or load_policy()
    if metadata_probes < 0 or metadata_probes > int(policy["max_metadata_probes"]):
        raise ScopeError("metadata-only probe exceeds policy maximum")
    tags = sorted(set(risk_tags) | set(infer_risk_tags(request)))
    high_risk = bool(set(tags) & set(policy["risk_floor_l3"]))
    contract_change = bool(set(artifact_tags) & {"public-api", "event-contract"})
    if high_risk or contract_change or len(set(domains)) > 1 or expected_files > 8:
        level = 3
    elif expected_files == 1 and len(set(domains)) == 1 and request.strip():
        level = 1
    else:
        level = 2
    difficulty = 3 if level == 3 else (2 if expected_files > 1 or len(domains) > 1 else 1)
    if confidence is None:
        confidence = 0.86 if expected_files > 0 and domains else (0.72 if request.strip() else 0.4)
    confidence = round(max(0.0, min(1.0, confidence)), 2)
    risk = "high" if high_risk else ("medium" if level == 2 or contract_change else "low")
    reasons = []
    if high_risk:
        reasons.append("L3 risk floor: " + ", ".join(tags))
    elif contract_change:
        reasons.append("public contract change")
    elif level == 1:
        reasons.append("one bounded file/domain and no contract change")
    elif level == 2:
        reasons.append("bounded multi-file or module impact")
    else:
        reasons.append("multiple domains or broad file impact")
    definition = deepcopy(policy["levels"][str(level)])
    now = utcnow()
    return {
        "schema_version": 1,
        "policy_version": int(policy["schema_version"]),
        "status": "estimated",
        "created_at": now,
        "updated_at": now,
        "estimate": {
            "scope_level": level,
            "scope_name": definition["name"],
            "difficulty": difficulty,
            "risk": risk,
            "confidence": confidence,
            "rationale": "; ".join(reasons),
            "expected_files": expected_files,
            "expected_domains": sorted(set(domains)),
            "artifact_tags": sorted(set(artifact_tags)),
            "risk_tags": tags,
            "model_tier": definition["model_tier"],
            "reasoning_level": definition["reasoning_level"],
            "context_budget": definition["context_budget"],
            "tool_budget": definition["tool_budget"],
            "verification": definition["verification"],
            "metadata_probes": metadata_probes,
        },
        "expansions": [],
        "actual": {
            "input_tokens": None,
            "output_tokens": None,
            "wall_clock_seconds": 0.0,
            "tool_calls": 0,
            "searches": 0,
            "unique_files": [],
            "read_bytes": 0,
            "read_ranges": 0,
            "duplicate_read_bytes": 0,
            "capability_escalations": 0,
            "subagents": 0,
            "expansion_count": 0,
            "time_to_first_valid_patch_seconds": None,
            "success": False,
        },
        "observations": [],
        "selection": {},
        "success_at": None,
    }


def validate_scope(state: dict[str, Any], policy: dict[str, Any] | None = None) -> list[str]:
    policy = policy or load_policy()
    errors: list[str] = []
    if state.get("schema_version") != 1:
        errors.append("unsupported schema_version")
    estimate = state.get("estimate")
    if not isinstance(estimate, dict):
        return errors + ["estimate must be an object"]
    level = estimate.get("scope_level")
    if level not in {1, 2, 3}:
        errors.append("scope_level must be 1..3")
    confidence = estimate.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("confidence must be 0..1")
    if int(estimate.get("metadata_probes", -1)) > int(policy["max_metadata_probes"]):
        errors.append("metadata probe limit exceeded")
    risk_tags = set(estimate.get("risk_tags") or [])
    if risk_tags & set(policy["risk_floor_l3"]) and level != 3:
        errors.append("high-risk task is below L3")
    if not isinstance(state.get("expansions"), list) or not isinstance(state.get("observations"), list):
        errors.append("expansions and observations must be arrays")
    if not isinstance(state.get("actual"), dict):
        errors.append("actual must be an object")
    return errors


def budget_overruns(state: dict[str, Any]) -> dict[str, dict[str, float]]:
    estimate = state["estimate"]
    actual = state["actual"]
    mapping = {
        "unique_files": (len(actual.get("unique_files") or []), estimate["context_budget"]["unique_files"]),
        "read_bytes": (actual.get("read_bytes", 0), estimate["context_budget"]["read_bytes"]),
        "read_ranges": (actual.get("read_ranges", 0), estimate["context_budget"]["read_ranges"]),
        "searches": (actual.get("searches", 0), estimate["tool_budget"]["searches"]),
        "tool_calls": (actual.get("tool_calls", 0), estimate["tool_budget"]["tool_calls"]),
        "subagents": (actual.get("subagents", 0), estimate["tool_budget"]["subagents"]),
    }
    return {key: {"actual": float(a), "budget": float(b)} for key, (a, b) in mapping.items() if a > b}


def record_observation(state: dict[str, Any], metrics: dict[str, Any], *, kind: str, evidence: str) -> None:
    errors = validate_scope(state)
    if errors:
        raise ScopeError("; ".join(errors))
    actual = state["actual"]
    positive_activity = False
    for key in ["wall_clock_seconds", "tool_calls", "searches", "read_bytes", "read_ranges", "duplicate_read_bytes", "subagents"]:
        value = metrics.get(key)
        if value is not None:
            if value < 0:
                raise ScopeError(f"{key} must be non-negative")
            actual[key] = round(float(actual.get(key, 0)) + float(value), 3)
            positive_activity = positive_activity or value > 0
    for key in ["input_tokens", "output_tokens", "time_to_first_valid_patch_seconds"]:
        if metrics.get(key) is not None:
            actual[key] = metrics[key]
    files = sorted(set(actual.get("unique_files") or []) | set(metrics.get("unique_files") or []))
    positive_activity = positive_activity or len(files) > len(actual.get("unique_files") or [])
    actual["unique_files"] = files
    observation = {"timestamp": utcnow(), "kind": kind, "evidence": evidence, "metrics": metrics}
    if state.get("status") == "success" and positive_activity:
        observation["post_success_activity"] = True
    state["observations"].append(observation)
    if state["status"] == "estimated":
        state["status"] = "executing"
    state["updated_at"] = utcnow()


def expand_scope(state: dict[str, Any], *, axis: str, reason_code: str, evidence: str, actor: str) -> None:
    policy = load_policy()
    errors = validate_scope(state, policy)
    if errors:
        raise ScopeError("; ".join(errors))
    if state["status"] == "success":
        raise ScopeError("cannot expand after decisive success")
    if axis not in policy["expansion_order"]:
        raise ScopeError(f"unknown expansion axis: {axis}")
    allowed_reasons = {
        "verification-failed", "estimate-exceeded", "dependency-discovered",
        "contract-impact-discovered", "artifact-impact-discovered",
        "requirements-conflict", "low-confidence-high-risk", "capability-insufficient",
    }
    if reason_code not in allowed_reasons or not evidence.strip():
        raise ScopeError("expansion requires an allowed reason and concrete evidence")
    if len(state["expansions"]) >= int(policy["max_expansions"]):
        raise ScopeError("maximum expansion count reached")
    if axis == "capability" and reason_code != "capability-insufficient":
        raise ScopeError("capability expansion requires capability-insufficient evidence")
    before = deepcopy(state["estimate"])
    estimate = state["estimate"]
    if axis == "scope":
        level = min(3, int(estimate["scope_level"]) + 1)
        definition = deepcopy(policy["levels"][str(level)])
        estimate.update({
            "scope_level": level,
            "scope_name": definition["name"],
            "model_tier": definition["model_tier"],
            "reasoning_level": definition["reasoning_level"],
            "context_budget": definition["context_budget"],
            "tool_budget": definition["tool_budget"],
            "verification": definition["verification"],
        })
    elif axis == "dependencies":
        estimate["context_budget"] = {key: max(value + 1, int(value * 1.5)) for key, value in estimate["context_budget"].items()}
    elif axis == "verification":
        for check in policy["levels"]["3"]["verification"]:
            if check not in estimate["verification"]:
                estimate["verification"].append(check)
                break
    elif axis == "review":
        estimate["tool_budget"]["subagents"] = max(1, estimate["tool_budget"]["subagents"])
    elif axis == "capability":
        estimate["model_tier"] = "capable"
        estimate["reasoning_level"] = "high"
        state["actual"]["capability_escalations"] += 1
    event = {
        "sequence": len(state["expansions"]) + 1,
        "timestamp": utcnow(),
        "axis": axis,
        "reason_code": reason_code,
        "evidence": evidence,
        "actor": actor,
        "before_digest": digest(before),
        "after_digest": digest(estimate),
    }
    state["expansions"].append(event)
    state["actual"]["expansion_count"] = len(state["expansions"])
    state["status"] = "executing"
    state["updated_at"] = utcnow()


def mark_verification(state: dict[str, Any], *, result: str, evidence: str, summary: str) -> None:
    if result not in {"pass", "fail"} or not evidence.strip() or not summary.strip():
        raise ScopeError("verification needs pass/fail, evidence, and summary")
    state["observations"].append({
        "timestamp": utcnow(), "kind": "verification", "result": result,
        "evidence": evidence, "summary": summary,
    })
    if result == "pass":
        state["status"] = "success"
        state["success_at"] = utcnow()
        state["actual"]["success"] = True
    else:
        state["status"] = "verification-failed"
        state["actual"]["success"] = False
    state["updated_at"] = utcnow()


def audit_scope(state: dict[str, Any]) -> dict[str, Any]:
    policy = load_policy()
    errors = validate_scope(state, policy)
    warnings: list[str] = []
    overruns = budget_overruns(state)
    expanded_reasons = {event.get("reason_code") for event in state.get("expansions", [])}
    if overruns and not ({"estimate-exceeded", "dependency-discovered", "artifact-impact-discovered"} & expanded_reasons):
        warnings.append("budget overrun has no corresponding Expand evidence")
    if any(event.get("axis") == "capability" and event.get("reason_code") != "capability-insufficient" for event in state.get("expansions", [])):
        warnings.append("capability escalation lacks capability-insufficient evidence")
    if any(item.get("post_success_activity") for item in state.get("observations", [])):
        warnings.append("exploration continued after decisive success")
    if state["estimate"]["risk"] == "high" and state["estimate"]["confidence"] < float(policy["high_risk_confidence_floor"]):
        if "low-confidence-high-risk" not in expanded_reasons:
            warnings.append("high-risk low-confidence estimate was not expanded")
    return {"schema_version": 1, "scope_digest": digest(state), "errors": errors, "warnings": warnings, "overruns": overruns}


def item_matches(item: dict[str, Any], state: dict[str, Any], profiles: set[str], phases: set[str]) -> bool:
    estimate = state["estimate"]
    if profiles and item.get("profile") not in profiles:
        return False
    if phases and item.get("phase") not in phases:
        return False
    if estimate["scope_level"] not in item.get("scope_levels", [1, 2, 3]):
        return False
    artifact = set(estimate.get("artifact_tags") or [])
    risks = set(estimate.get("risk_tags") or [])
    return bool(item.get("always_on") or artifact.intersection(item.get("artifact_tags") or []) or risks.intersection(item.get("risk_tags") or []))


def select_catalog_items(catalog: dict[str, Any], state: dict[str, Any], *, profiles: list[str], phases: list[str]) -> dict[str, Any]:
    policy = load_policy()
    selected = sorted(item["id"] for item in catalog["items"] if item_matches(item, state, set(profiles), set(phases)))
    inputs = {
        "scope_level": state["estimate"]["scope_level"],
        "artifact_tags": state["estimate"].get("artifact_tags") or [],
        "risk_tags": state["estimate"].get("risk_tags") or [],
        "profiles": sorted(set(profiles)),
        "phases": sorted(set(phases)),
        "catalog_sha256": digest(catalog),
    }
    selection = {
        "selector_version": policy["selector_version"],
        "inputs": inputs,
        "selected_item_ids": selected,
        "selected_count": len(selected),
        "candidate_count": len(catalog["items"]),
    }
    selection["selection_sha256"] = digest(selection)
    return selection


def efficiency_report(state: dict[str, Any]) -> dict[str, Any]:
    audit = audit_scope(state)
    ratios: dict[str, float] = {}
    for key, values in audit["overruns"].items():
        budget = values["budget"]
        ratios[key] = round((values["actual"] - budget) / budget, 4) if budget else 1.0
    return {
        "schema_version": 1,
        "generated_at": utcnow(),
        "status": state["status"],
        "success": state["actual"]["success"],
        "estimate": state["estimate"],
        "actual": state["actual"],
        "expansions": state["expansions"],
        "execution_overrun_ratio": ratios,
        "audit": audit,
        "acrr": None,
        "acrr_note": "C_min oracleがない実案件ではACRRを算出しない",
    }


def run_benchmark(path: Path = BENCHMARK_PATH) -> dict[str, Any]:
    suite = read_json(path)
    results = []
    for case in suite["cases"]:
        state = estimate_scope(
            case["request"], expected_files=case["expected_files"], domains=case["domains"],
            artifact_tags=case["artifact_tags"], risk_tags=case["risk_tags"],
        )
        actual = state["estimate"]["scope_level"]
        results.append({"id": case["id"], "expected_level": case["expected_level"], "actual_level": actual, "passed": actual == case["expected_level"]})
    return {
        "schema_version": 1,
        "suite": str(path),
        "variants": suite.get("variants", []),
        "passed": all(item["passed"] for item in results),
        "case_count": len(results),
        "results": results,
        "claim_boundary": "論文の削減率をdev-standardの目標値として使用しない",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="適正規模実行の推定・台帳・監査")
    sub = parser.add_subparsers(dest="command", required=True)
    estimate = sub.add_parser("estimate")
    estimate.add_argument("--request", required=True)
    estimate.add_argument("--out", required=True)
    estimate.add_argument("--expected-files", type=int, default=0)
    estimate.add_argument("--domains", default="")
    estimate.add_argument("--artifact-tags", default="")
    estimate.add_argument("--risk-tags", default="")
    estimate.add_argument("--metadata-probes", type=int, default=0)
    estimate.add_argument("--confidence", type=float)
    expand = sub.add_parser("expand")
    expand.add_argument("--scope", required=True)
    expand.add_argument("--axis", required=True)
    expand.add_argument("--reason-code", required=True)
    expand.add_argument("--evidence", required=True)
    expand.add_argument("--actor", required=True)
    observe = sub.add_parser("observe")
    observe.add_argument("--scope", required=True)
    observe.add_argument("--kind", default="execute")
    observe.add_argument("--evidence", required=True)
    for name in ["tool-calls", "searches", "read-bytes", "read-ranges", "duplicate-read-bytes", "subagents"]:
        observe.add_argument(f"--{name}", type=int, default=0)
    observe.add_argument("--wall-clock-seconds", type=float, default=0)
    observe.add_argument("--input-tokens", type=int)
    observe.add_argument("--output-tokens", type=int)
    observe.add_argument("--time-to-first-valid-patch-seconds", type=float)
    observe.add_argument("--unique-file", action="append", default=[])
    verify = sub.add_parser("verification")
    verify.add_argument("--scope", required=True)
    verify.add_argument("--result", choices=["pass", "fail"], required=True)
    verify.add_argument("--evidence", required=True)
    verify.add_argument("--summary", required=True)
    finalize = sub.add_parser("finalize")
    finalize.add_argument("--scope", required=True)
    finalize.add_argument("--out", required=True)
    audit = sub.add_parser("audit")
    audit.add_argument("--scope", required=True)
    audit.add_argument("--mode", choices=["soft", "strict"], default="soft")
    select = sub.add_parser("select-checks")
    select.add_argument("--scope", required=True)
    select.add_argument("--catalog", required=True)
    select.add_argument("--profiles", default="")
    select.add_argument("--phases", default="")
    select.add_argument("--out", required=True)
    benchmark = sub.add_parser("benchmark")
    benchmark.add_argument("--suite", default=str(BENCHMARK_PATH))
    benchmark.add_argument("--out")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "estimate":
            state = estimate_scope(args.request, expected_files=args.expected_files, domains=csv_values(args.domains), artifact_tags=csv_values(args.artifact_tags), risk_tags=csv_values(args.risk_tags), metadata_probes=args.metadata_probes, confidence=args.confidence)
            write_json(Path(args.out), state)
            print(f"L{state['estimate']['scope_level']} {state['estimate']['scope_name']} -> {args.out}")
        elif args.command == "expand":
            path = Path(args.scope)
            state = read_json(path)
            expand_scope(state, axis=args.axis, reason_code=args.reason_code, evidence=args.evidence, actor=args.actor)
            write_json(path, state)
            print(f"expanded {args.axis}: {len(state['expansions'])}")
        elif args.command == "observe":
            path = Path(args.scope)
            state = read_json(path)
            metrics = {key.replace("_", "-"): value for key, value in vars(args).items()}
            normalized = {
                "tool_calls": args.tool_calls, "searches": args.searches, "read_bytes": args.read_bytes,
                "read_ranges": args.read_ranges, "duplicate_read_bytes": args.duplicate_read_bytes,
                "subagents": args.subagents, "wall_clock_seconds": args.wall_clock_seconds,
                "input_tokens": args.input_tokens, "output_tokens": args.output_tokens,
                "time_to_first_valid_patch_seconds": args.time_to_first_valid_patch_seconds,
                "unique_files": args.unique_file,
            }
            record_observation(state, normalized, kind=args.kind, evidence=args.evidence)
            write_json(path, state)
            print(f"observed: {digest(metrics)[:12]}")
        elif args.command == "verification":
            path = Path(args.scope)
            state = read_json(path)
            mark_verification(state, result=args.result, evidence=args.evidence, summary=args.summary)
            write_json(path, state)
            print(state["status"])
        elif args.command == "finalize":
            state = read_json(Path(args.scope))
            report = efficiency_report(state)
            write_json(Path(args.out), report)
            print(args.out)
        elif args.command == "audit":
            report = audit_scope(read_json(Path(args.scope)))
            print(json.dumps(report, ensure_ascii=False, indent=2))
            if report["errors"] or (args.mode == "strict" and report["warnings"]):
                return 1
        elif args.command == "select-checks":
            path = Path(args.scope)
            state = read_json(path)
            selection = select_catalog_items(read_json(Path(args.catalog)), state, profiles=csv_values(args.profiles), phases=csv_values(args.phases))
            state["selection"] = selection
            state["updated_at"] = utcnow()
            write_json(path, state)
            write_json(Path(args.out), selection)
            print(f"selected {selection['selected_count']}")
        elif args.command == "benchmark":
            report = run_benchmark(Path(args.suite))
            if args.out:
                write_json(Path(args.out), report)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0 if report["passed"] else 1
        return 0
    except (ScopeError, OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"scopeflow error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
