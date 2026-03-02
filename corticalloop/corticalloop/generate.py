"""Hypothesis generation interfaces and implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import uuid4

from corticalloop.types import Hypothesis


class HypothesisGenerator(ABC):
    """Creates candidate hypotheses from a task and context."""

    @abstractmethod
    def generate(self, task: str, context: dict[str, Any], num_hypotheses: int) -> list[Hypothesis]:
        raise NotImplementedError


class SimpleGenerator(HypothesisGenerator):
    """Offline template-driven generator."""

    templates = [
        "Direct answer: {task}. Use context: {ctx}",
        "Stepwise plan for {task}: 1) analyze 2) solve 3) verify. Context: {ctx}",
        "Constraint-aware approach to {task}. Given context: {ctx}",
        "Alternative strategy for {task}: compare options then pick best. Context: {ctx}",
    ]

    def generate(self, task: str, context: dict[str, Any], num_hypotheses: int) -> list[Hypothesis]:
        ctx = ", ".join(f"{k}={v}" for k, v in context.items()) if context else "none"
        hypotheses: list[Hypothesis] = []
        for i in range(num_hypotheses):
            template = self.templates[i % len(self.templates)]
            text = template.format(task=task, ctx=ctx)
            hypotheses.append(Hypothesis(id=f"h-{uuid4().hex[:8]}", text=text))
        return hypotheses
