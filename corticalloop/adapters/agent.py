"""Reasoning agent adapter."""

from __future__ import annotations

from typing import Any

from corticalloop.config import LoopConfig
from corticalloop.evaluate import Evaluator, HeuristicEvaluator
from corticalloop.generate import HypothesisGenerator, SimpleGenerator
from corticalloop.loop import LoopController
from corticalloop.refine import Refiner, SimpleRefiner
from corticalloop.types import SolveResult


class CorticalLoop:
    """High-level API for iterative reasoning over a task."""

    def __init__(
        self,
        generator: HypothesisGenerator | None = None,
        evaluator: Evaluator | None = None,
        refiner: Refiner | None = None,
        config: LoopConfig | None = None,
    ) -> None:
        self.config = config or LoopConfig()
        self.controller = LoopController(
            generator=generator or SimpleGenerator(),
            evaluator=evaluator or HeuristicEvaluator(),
            refiner=refiner or SimpleRefiner(),
            config=self.config,
        )

    def solve(self, task: str, context: dict[str, Any] | None = None) -> SolveResult:
        if not task.strip():
            raise ValueError("task must be a non-empty string")
        record = self.controller.run(task=task, context=context or {})
        return SolveResult(final_answer=record.final_answer, record=record)
