from __future__ import annotations

import argparse
from pathlib import Path

from .fixture import load_fixture
from .io import write_json
from .schema import load_and_validate
from .scoring import score_observed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--condition", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--phase", choices=["clarify", "execute"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    task = load_and_validate(args.root, "task", args.root / "benchmarks" / "tasks" / args.task / "task.json")
    oracle = load_and_validate(args.root, "oracle", args.root / "benchmarks" / "oracles" / args.task / "oracle.json")
    fixture_root, observed = load_fixture(args.root, args.task, "gold")
    result = score_observed(args.root, task, oracle, observed, state_root=fixture_root, condition=args.condition, run_type="smoke", seed=args.seed)
    write_json(args.output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
