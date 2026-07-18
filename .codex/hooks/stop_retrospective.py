#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def has_active_regulated_work(root: Path) -> bool:
    for state_path in (root / "work").glob("*/state.json"):
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if state.get("status") == "active":
            return True
    return False


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}

    root = Path(__file__).resolve().parents[2]
    if not has_active_regulated_work(root):
        print(json.dumps({
            "continue": True,
            "systemMessage": "No active regulated work item; retrospective skipped.",
        }, ensure_ascii=False))
        return 0

    session_id = str(event.get("session_id") or "unknown-session")
    cwd = str(event.get("cwd") or root)
    command = [
        sys.executable,
        str(root / "tools" / "devflow.py"),
        "session-retrospective",
        "--session-id",
        session_id,
        "--cwd",
        cwd,
    ]
    try:
        result = subprocess.run(
            command,
            cwd=root,
            text=True,
            capture_output=True,
            timeout=75,
            check=False,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        prefix = "regulated retrospective" if result.returncode == 0 else "regulated retrospective warning"
        message = f"{prefix}: {output or f'exit {result.returncode}'}"
    except (OSError, subprocess.SubprocessError) as exc:
        message = f"regulated retrospective hook warning: {exc}"

    print(json.dumps({
        "continue": True,
        "systemMessage": message,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
