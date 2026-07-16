#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        event = {}
    root = Path(__file__).resolve().parents[2]
    active = []
    for state_path in sorted((root / "work").glob("*/state.json")):
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if state.get("status") == "active":
            active.append(f"{state.get('id')}:{state.get('current_phase')}")
    pending = []
    proposals = root / "governance" / "improvements" / "proposals.json"
    if proposals.exists():
        try:
            pending = [item["id"] for item in json.loads(proposals.read_text(encoding="utf-8")) if item.get("status") == "pending"]
        except (OSError, json.JSONDecodeError, KeyError):
            pending = []
    context = [
        "This repository requires the governed lifecycle in AGENTS.md.",
        "Use $govern-development-request before implementation and never self-approve a gate.",
        "Active work items: " + (", ".join(active) if active else "none"),
        "Pending skill improvements requiring governance-owner review: " + (", ".join(pending) if pending else "none"),
    ]
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
