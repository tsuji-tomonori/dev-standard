from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

from .io import BenchmarkError, digest_value, safe_path

SECRET_MARKERS = ("TOKEN", "SECRET", "PASSWORD", "KEY", "CREDENTIAL")


@dataclass(frozen=True)
class SandboxPlan:
    argv: tuple[str, ...]
    workspace: Path
    audit_path: Path
    executor: str
    network_policy: str


def validate_argv(argv: Sequence[str]) -> tuple[str, ...]:
    if isinstance(argv, (str, bytes)) or not argv or not all(isinstance(item, str) and item for item in argv):
        raise BenchmarkError("adapter command must be a non-empty argv sequence, never shell text")
    return tuple(argv)


def redact_environment(environment: Mapping[str, str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in environment.items():
        result[key] = "<redacted>" if any(marker in key.upper() for marker in SECRET_MARKERS) else value
    return result


def write_tool_audit(path: Path, *, workspace: Path, argv: Sequence[str], environment: Mapping[str, str], status: str) -> None:
    workspace = workspace.resolve()
    path = path.resolve(strict=False)
    if path == workspace or workspace in path.parents:
        raise BenchmarkError("tool audit must be outside the agent workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "argv_digest": digest_value(list(validate_argv(argv))),
        "environment": redact_environment(environment),
        "status": status,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def build_plan(workspace: Path, argv: Sequence[str], audit_path: Path) -> SandboxPlan:
    workspace = workspace.resolve()
    safe_path(workspace.parent, workspace.name, require_exists=True)
    audit = audit_path.resolve(strict=False)
    if audit == workspace or workspace in audit.parents:
        raise BenchmarkError("audit path must not be inside agent workspace")
    command = validate_argv(argv)
    unshare = shutil.which("unshare")
    sudo = shutil.which("sudo")
    if not unshare:
        raise BenchmarkError("unshare is required to enforce network isolation")
    prefix = (sudo, "-n") if sudo else ()
    sandboxed = tuple(item for item in prefix if item) + (unshare, "--net", "--mount", "--pid", "--fork", "--mount-proc", "--") + command
    return SandboxPlan(sandboxed, workspace, audit, "linux-unshare-net-mount-pid", "deny-agent-workspace-egress")


def network_namespace_probe(runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run) -> bool:
    unshare = shutil.which("unshare") or "unshare"
    sudo = shutil.which("sudo")
    prefix = [sudo, "-n"] if sudo else []
    script = (
        "import socket,sys; "
        "s=socket.socket(); s.settimeout(0.5); "
        "\ntry: s.connect(('1.1.1.1',53)); sys.exit(7)"
        "\nexcept OSError: sys.exit(0)"
    )
    command = [*prefix, unshare, "--net", "--", sys.executable, "-c", script]
    result = runner(command, text=True, capture_output=True, check=False, timeout=10)
    return result.returncode == 0


def execute(plan: SandboxPlan, *, environment: Mapping[str, str], timeout: int) -> subprocess.CompletedProcess[str]:
    if plan.network_policy != "deny-agent-workspace-egress":
        raise BenchmarkError("sandbox network policy is not enforced")
    return subprocess.run(
        list(plan.argv),
        cwd=plan.workspace,
        env=dict(environment),
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe-network", action="store_true")
    args = parser.parse_args(argv)
    if args.probe_network:
        if not network_namespace_probe():
            print("ERROR: network namespace is unavailable or egress was not denied")
            return 2
        print("network namespace isolation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
