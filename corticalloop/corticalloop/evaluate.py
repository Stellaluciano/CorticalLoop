"""Evaluation interfaces and implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from corticalloop.types import Hypothesis


class Evaluator(ABC):
    """Scores hypotheses and returns feedback signals."""

    @abstractmethod
    def evaluate(self, task: str, hypotheses: list[Hypothesis], context: dict[str, Any]) -> dict[str, float]:
        raise NotImplementedError


class HeuristicEvaluator(Evaluator):
    """Keyword-coverage + brevity heuristic evaluator."""

    def evaluate(self, task: str, hypotheses: list[Hypothesis], context: dict[str, Any]) -> dict[str, float]:
        task_words = {w.lower() for w in task.split() if len(w) > 3}
        constraints = [str(c).lower() for c in context.get("constraints", [])]
        scores: dict[str, float] = {}
        for hyp in hypotheses:
            text = hyp.text.lower()
            coverage_hits = sum(1 for w in task_words if w in text)
            coverage = coverage_hits / max(len(task_words), 1)
            length_penalty = min(len(hyp.text) / 350, 1.0) * 0.25
            constraint_bonus = 0.0
            if constraints:
                satisfied = sum(1 for c in constraints if c in text)
                constraint_bonus = 0.3 * (satisfied / max(len(constraints), 1))
            score = max(0.0, min(1.0, 0.7 * coverage + constraint_bonus + 0.3 - length_penalty))
            scores[hyp.id] = score
        return scores
