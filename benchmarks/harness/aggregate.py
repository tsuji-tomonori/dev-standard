from __future__ import annotations

import argparse
import json
from pathlib import Path

from .io import BenchmarkError, load_json, write_json
from .statistics import flake_report, paired_report


def load_results(paths: list[Path]) -> list[dict]:
    results: list[dict] = []
    for path in paths:
        value = load_json(path)
        if isinstance(value, list):
            results.extend(value)
        elif isinstance(value, dict):
            results.append(value)
        else:
            raise BenchmarkError(f"{path}: result input must be object or array")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=["utility", "status"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("inputs", type=Path, nargs="+")
    args = parser.parse_args(argv)
    try:
        results = load_results(args.inputs)
        report = paired_report(results, load_json(args.root / "benchmarks" / "protocol.json")) if args.mode == "utility" else flake_report(results)
        write_json(args.output, report)
    except BenchmarkError as exc:
        print(f"ERROR: {exc}")
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
