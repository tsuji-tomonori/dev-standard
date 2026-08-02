from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any, Iterable

from .io import BenchmarkError


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total <= 0 or not 0 <= successes <= total:
        raise BenchmarkError("Wilson interval requires 0 <= successes <= total and total > 0")
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / denominator
    return max(0.0, centre - radius), min(1.0, centre + radius)


def exact_mcnemar(b: int, c: int) -> float:
    if b < 0 or c < 0:
        raise BenchmarkError("discordant pair counts cannot be negative")
    total = b + c
    if total == 0:
        return 1.0
    tail = sum(math.comb(total, index) for index in range(0, min(b, c) + 1)) / (2**total)
    return min(1.0, 2 * tail)


def paired_bootstrap_interval(differences: list[float], *, samples: int = 2000, seed: int = 0) -> tuple[float, float]:
    if not differences:
        raise BenchmarkError("paired bootstrap requires observations")
    randomizer = random.Random(seed)
    means = []
    for _ in range(samples):
        means.append(sum(randomizer.choice(differences) for _ in differences) / len(differences))
    means.sort()
    low = means[int(0.025 * (samples - 1))]
    high = means[int(0.975 * (samples - 1))]
    return max(-1.0, low), min(1.0, high)


def _index_results(results: Iterable[dict[str, Any]]) -> dict[tuple[str, int, str], dict[str, Any]]:
    indexed: dict[tuple[str, int, str], dict[str, Any]] = {}
    for result in results:
        key = (result["task_id"], result["seed"], result["condition"])
        if key in indexed:
            raise BenchmarkError(f"duplicate task/seed/condition result: {key}")
        indexed[key] = result
    return indexed


def paired_report(results: list[dict[str, Any]], protocol: dict[str, Any]) -> dict[str, Any]:
    if any(result.get("run_type") != "utility" for result in results):
        raise BenchmarkError("smoke, flake and release results cannot be used for utility inference")
    indexed = _index_results(results)
    grouped: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for (task_id, seed, condition), result in indexed.items():
        grouped[(task_id, seed)][condition] = result
    primary = tuple(protocol["statistics"]["primary_contrast"])
    secondary = tuple(protocol["statistics"]["secondary_contrast"])

    def contrast(arms: tuple[str, str]) -> dict[str, Any]:
        complete: list[tuple[bool, bool]] = []
        incomplete = 0
        for values in grouped.values():
            if not all(arm in values for arm in arms):
                incomplete += 1
                continue
            left, right = values[arms[0]], values[arms[1]]
            if left["status"] != "completed" or right["status"] != "completed":
                incomplete += 1
                continue
            complete.append((bool(left["strict_e2e_pass"]), bool(right["strict_e2e_pass"])))
        if not complete:
            return {"arms": list(arms), "complete_pairs": 0, "incomplete_pairs": incomplete, "inconclusive": True}
        b = sum(left and not right for left, right in complete)
        c = sum((not left) and right for left, right in complete)
        differences = [float(left) - float(right) for left, right in complete]
        left_success = sum(left for left, _ in complete)
        right_success = sum(right for _, right in complete)
        minimum = protocol["statistics"]["minimum_paired_observations_per_task"]
        tasks = {task_id for task_id, _ in grouped}
        fixed_plan_met = all(sum(1 for (candidate, _), values in grouped.items() if candidate == task_id and all(arm in values for arm in arms)) >= minimum for task_id in tasks)
        return {
            "arms": list(arms),
            "complete_pairs": len(complete),
            "incomplete_pairs": incomplete,
            "inconclusive": incomplete > 0 or not fixed_plan_met,
            "fixed_plan_met": fixed_plan_met,
            "optional_stopping": False,
            "delta": sum(differences) / len(differences),
            "delta_interval": list(paired_bootstrap_interval(differences)),
            "mcnemar_p": exact_mcnemar(b, c),
            "discordant": {"left_only": b, "right_only": c},
            "left_rate_interval": list(wilson_interval(left_success, len(complete))),
            "right_rate_interval": list(wilson_interval(right_success, len(complete))),
        }

    return {
        "schema_version": 1,
        "claim_boundary": protocol["claim_boundary"],
        "primary": contrast(primary),
        "length_matched_control": contrast(secondary),
    }


def flake_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    _index_results(results)
    total = len(results)
    completed = sum(result.get("status") == "completed" for result in results)
    return {
        "schema_version": 1,
        "mode": "flake-health",
        "total": total,
        "completed": completed,
        "failure_rate": 0.0 if total == 0 else (total - completed) / total,
        "utility_inference": False,
    }
