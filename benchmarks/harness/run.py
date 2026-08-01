from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .io import BenchmarkError, digest_value, load_json, safe_path
from .isolation import CONDITIONS, prepare_workspace
from .schema import validate_value

SAFE_ENVIRONMENT = ("PATH", "HOME", "LANG", "LC_ALL", "TZ", "TMPDIR", "PYTHONPATH")
PHASE_STATUSES = {"completed", "provider_error", "timeout", "tool_crash", "skipped"}


def counterbalanced_order(seed: int) -> list[str]:
    conditions = list(CONDITIONS)
    shift = seed % len(conditions)
    rotated = conditions[shift:] + conditions[:shift]
    if (seed // len(conditions)) % 2:
        rotated[1:] = reversed(rotated[1:])
    return rotated


def validate_conditions(conditions: Sequence[str]) -> tuple[str, ...]:
    if len(conditions) != 3 or len(set(conditions)) != 3 or set(conditions) != set(CONDITIONS):
        raise BenchmarkError("paired run requires all three conditions exactly once")
    return tuple(conditions)


def parse_adapter_command(value: str | Sequence[str]) -> tuple[str, ...]:
    parsed: Any = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise BenchmarkError("adapter command must be a JSON argv array") from exc
    if isinstance(parsed, (str, bytes)) or not isinstance(parsed, list) or not parsed or not all(isinstance(item, str) and item for item in parsed):
        raise BenchmarkError("adapter command must be a non-empty JSON argv array")
    return tuple(parsed)


def build_environment(source: Mapping[str, str] | None = None) -> dict[str, str]:
    source = source or os.environ
    result: dict[str, str] = {}
    for key in SAFE_ENVIRONMENT:
        if key.startswith("BENCHMARK_"):
            raise BenchmarkError("benchmark variables must be explicit command arguments, not imported environment")
        if key in source:
            result[key] = source[key]
    return result


def run_identity(fixed_inputs: Mapping[str, Any]) -> str:
    ignored = {"started_at", "finished_at", "clock", "wall_ms"}
    return digest_value({key: value for key, value in fixed_inputs.items() if key not in ignored})


def create_manifest(
    root: Path,
    task_id: str,
    condition: str,
    seed: int,
    *,
    model_id: str,
    model_revision: str,
    repository_commit: str,
    arm_order: list[str],
    started_at: str | None = None,
) -> dict[str, Any]:
    task = load_json(safe_path(root, f"benchmarks/tasks/{task_id}/task.json", require_exists=True))
    oracle = load_json(safe_path(root, f"benchmarks/oracles/{task_id}/oracle.json", require_exists=True))
    skill_digests = {}
    for skill_id in task["agent_visible"]["selected_skill_ids"]:
        skill_digests[skill_id] = digest_value((root / ".agents" / "skills" / skill_id / "SKILL.md").read_text(encoding="utf-8"))
    fixed = {
        "harness_version": "1.0.0",
        "model": {"id": model_id, "revision": model_revision, "settings_digest": digest_value({"temperature": 0})},
        "system_prompt_digest": digest_value("benchmark-system-v1"),
        "developer_prompt_digest": digest_value("benchmark-developer-v1"),
        "tool_schema_digest": digest_value({"adapter": "argv-json-v1"}),
        "skill_digests": skill_digests,
        "repository_commit": repository_commit,
        "task_digest": digest_value(task),
        "oracle_digest": digest_value(oracle),
        "condition": condition,
        "seed": seed,
        "arm_order": arm_order,
        "timeout_seconds": 300,
        "max_retries": 1,
        "failure_policy": load_json(root / "benchmarks" / "protocol.json")["failure_policy"],
        "environment": {
            "allowed_variables": list(SAFE_ENVIRONMENT),
            "network_policy": "deny-agent-workspace-egress",
            "control_plane_allowed": ["model-provider", "github-actions-artifact"],
        },
    }
    manifest = {"schema_version": 1, "run_id": run_identity(fixed), **fixed, "started_at": started_at or dt.datetime.now(dt.UTC).isoformat()}
    validate_value(root, "run-manifest", manifest, "run manifest")
    return manifest


def _phase(name: str, status: str, attempts: int, command: Sequence[str], duration_ms: int = 0) -> dict[str, Any]:
    if status not in PHASE_STATUSES:
        raise BenchmarkError(f"invalid phase status: {status}")
    return {"name": name, "status": status, "attempts": attempts, "command_digest": digest_value(list(command)), "duration_ms": duration_ms}


def run_phase(
    name: str,
    command: Sequence[str],
    *,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: int = 300,
    max_provider_retries: int = 1,
) -> dict[str, Any]:
    attempts = 0
    start = time.monotonic()
    while True:
        attempts += 1
        try:
            result = runner(list(command), text=True, capture_output=True, check=False, timeout=timeout)
        except subprocess.TimeoutExpired:
            return _phase(name, "timeout", attempts, command, int((time.monotonic() - start) * 1000))
        except OSError:
            return _phase(name, "tool_crash", attempts, command, int((time.monotonic() - start) * 1000))
        status = "completed" if result.returncode == 0 else ("provider_error" if result.returncode == 75 else "tool_crash")
        if status == "provider_error" and attempts <= max_provider_retries:
            continue
        return _phase(name, status, attempts, command, int((time.monotonic() - start) * 1000))


def adapter_command(base: Sequence[str], *, root: Path, workspace: Path, task_id: str, condition: str, seed: int, phase: str, output: Path) -> list[str]:
    return [
        *base,
        "--root", str(root),
        "--workspace", str(workspace),
        "--task", task_id,
        "--condition", condition,
        "--seed", str(seed),
        "--phase", phase,
        "--output", str(output),
    ]


def paired_plan(task: dict[str, Any], seed: int) -> list[str]:
    validate_conditions(task["conditions"])
    order = counterbalanced_order(seed)
    if set(order) != set(task["conditions"]):
        raise BenchmarkError("counterbalanced order is incomplete")
    return order


def run_paired(root: Path, task_id: str, seed: int, adapter: Sequence[str], output_root: Path, run_type: str = "smoke") -> list[dict[str, Any]]:
    root = root.resolve()
    task = load_json(safe_path(root, f"benchmarks/tasks/{task_id}/task.json", require_exists=True))
    order = paired_plan(task, seed)
    results: list[dict[str, Any]] = []
    for condition in order:
        workspace = output_root / "workspace" / task_id / str(seed) / condition
        prepare_workspace(root, task_id, condition, workspace)
        result_path = output_root / "results" / f"{task_id}-{seed}-{condition}.json"
        command = adapter_command(adapter, root=root, workspace=workspace, task_id=task_id, condition=condition, seed=seed, phase="execute", output=result_path)
        phase = run_phase("execute", command)
        if result_path.is_file():
            result = load_json(result_path)
        else:
            result = {
                "schema_version": 1,
                "task_id": task_id,
                "condition": condition,
                "run_type": run_type,
                "seed": seed,
                "status": phase["status"] if phase["status"] != "skipped" else "missing",
                "execution": {"phases": [phase], "sandbox": {"network_enforced": False, "tool_audit_valid": False, "executor": "external-adapter"}},
                "gates": {name: False for name in ("interaction", "requirements", "implementation", "generated_design", "governance", "safety_authority")},
                "strict_e2e_pass": False,
                "sub_scores": {name: 0.0 for name in ("interaction", "requirements", "implementation", "generated_design", "governance", "safety_authority")},
                "cost": {"user_turns": 0, "tool_calls": 0, "failed_commands": 1, "tokens": 0, "wall_ms": phase["duration_ms"]},
                "evidence": [],
                "llm_judge": {"used": False, "advisory_only": True},
            }
        validate_value(root, "result", result, result_path.as_posix())
        results.append(result)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    paired = sub.add_parser("paired")
    paired.add_argument("--root", type=Path, default=Path.cwd())
    paired.add_argument("--task", required=True)
    paired.add_argument("--seed", type=int, default=0)
    paired.add_argument("--run-type", default="smoke", choices=["smoke", "flake", "utility", "release"])
    paired.add_argument("--adapter", required=True, help="JSON argv array")
    paired.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        adapter = parse_adapter_command(args.adapter)
        results = run_paired(args.root, args.task, args.seed, adapter, args.output, args.run_type)
    except BenchmarkError as exc:
        print(f"ERROR: {exc}")
        return 2
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
