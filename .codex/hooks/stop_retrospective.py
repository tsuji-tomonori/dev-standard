#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(command: list[str], root: Path) -> tuple[int, str]:
    result = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=75, check=False)
    output = (result.stdout + "\n" + result.stderr).strip()
    return result.returncode, output


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}
    root = Path(__file__).resolve().parents[2]
    session_id = str(event.get("session_id") or "unknown-session")
    cwd = str(event.get("cwd") or root)
    devflow = str(root / "tools" / "devflow.py")
    messages = []
    try:
        code, output = run([sys.executable, devflow, "session-retrospective", "--session-id", session_id, "--cwd", cwd], root)
        messages.append(("retrospective" if code == 0 else "retrospective warning") + ": " + (output or f"exit {code}"))
        code, output = run([sys.executable, devflow, "improvement-apply"], root)
        messages.append(("skill update" if code == 0 else "skill update warning") + ": " + (output or f"exit {code}"))
    except (OSError, subprocess.SubprocessError) as exc:
        messages.append(f"retrospective hook warning: {exc}")
    print(json.dumps({
        "continue": True,
        "systemMessage": "\n".join(messages),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
