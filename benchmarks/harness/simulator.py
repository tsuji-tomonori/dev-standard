from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .io import BenchmarkError, load_json, safe_path


@dataclass(frozen=True)
class SimulatedAnswer:
    task_id: str
    variant: str
    answer: str
    expected_outcome: str


class UserSimulator:
    """Controller-only answer source. It must never be copied into an agent workspace."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def answer(self, task_id: str, variant: str, question_concepts: list[str]) -> SimulatedAnswer:
        oracle_path = safe_path(self.root, f"benchmarks/oracles/{task_id}/oracle.json", require_exists=True)
        oracle = load_json(oracle_path)
        interaction = oracle["interaction"]
        forbidden = set(interaction["forbidden_question_concepts"])
        asked = set(question_concepts)
        if asked & forbidden:
            raise BenchmarkError(f"question contains forbidden reversible concept: {sorted(asked & forbidden)}")
        if not set(interaction["key_question_concepts"]).issubset(asked):
            raise BenchmarkError("question does not cover the annotated key concept")
        values = interaction["answer_variants"]
        if variant not in values:
            raise BenchmarkError(f"unknown answer variant: {variant}")
        selected = values[variant]
        return SimulatedAnswer(task_id, variant, selected["answer"], selected["expected_outcome"])
