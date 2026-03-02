"""Refinement interfaces and implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import uuid4

from corticalloop.types import Hypothesis


class Refiner(ABC):
    """Refines top hypotheses into updated candidates."""

    @abstractmethod
    def refine(self, task: str, top_hypotheses: list[Hypothesis], iteration: int) -> list[Hypothesis]:
        raise NotImplementedError


class SimpleRefiner(Refiner):
    """String-based refiner that merges top candidate fragments."""

    def refine(self, task: str, top_hypotheses: list[Hypothesis], iteration: int) -> list[Hypothesis]:
        if not top_hypotheses:
            return []
        joined = " | ".join(h.text[:140] for h in top_hypotheses)
        refined_text = f"Refined iteration {iteration} for {task}: {joined}"
        return [
            Hypothesis(
                id=f"h-{uuid4().hex[:8]}",
                text=refined_text,
                parent_ids=[h.id for h in top_hypotheses],
            )
        ]
