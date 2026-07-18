#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    root = Path(__file__).resolve().parents[2]
    active: list[str] = []
    for state_path in sorted((root / "work").glob("*/state.json")):
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if state.get("status") == "active":
            active.append(f"{state.get('id')}:{state.get('current_phase')}")

    context = [
        "Use the repository's direct / assured / regulated profile selection.",
        "Do not create a permanent work item for direct or assured changes.",
        "Use structured Commit Comments, repository review YAML, and external CI results.",
    ]
    if active:
        context.extend([
            "Active regulated work items: " + ", ".join(active),
            "Resume their recorded authority boundary and regulated gate state before acting.",
        ])

    print(json.dumps({
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(context),
        },
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
