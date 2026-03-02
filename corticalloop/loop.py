"""Core recurrent loop controller."""

from __future__ import annotations

from typing import Any
import copy

from corticalloop.config import LoopConfig
from corticalloop.evaluate import Evaluator
from corticalloop.generate import HypothesisGenerator
from corticalloop.pool import HypothesisPool
from corticalloop.refine import Refiner
from corticalloop.types import IterationRecord, RunRecord


class LoopController:
    """Runs iterative generation-evaluation-refinement cycles."""

    def __init__(
        self,
        generator: HypothesisGenerator,
        evaluator: Evaluator,
        refiner: Refiner,
        config: LoopConfig,
    ) -> None:
        self.generator = generator
        self.evaluator = evaluator
        self.refiner = refiner
        self.config = config

    def run(self, task: str, context: dict[str, Any] | None = None) -> RunRecord:
        context = context or {}
        pool = HypothesisPool()
        record = RunRecord(task=task, context=context)
        prev_best = 0.0

        hypotheses = self.generator.generate(task, context, self.config.num_hypotheses)
        pool.add(hypotheses)

        for i in range(1, self.config.max_iters + 1):
            current = pool.all()
            feedback = self.evaluator.evaluate(task, current, context)
            for hyp in current:
                hyp.score = feedback.get(hyp.id, 0.0)

            top = pool.topk(self.config.top_k)
            best_score = top[0].score if top else 0.0
            stop_reason = None

            if self.config.inhibitory_gate:
                gate_threshold = max(0.0, best_score - 0.25)
                pool.prune_below(gate_threshold)

            if best_score >= self.config.score_threshold:
                stop_reason = "score_threshold"
            elif abs(best_score - prev_best) <= self.config.convergence_delta and i > 1:
                stop_reason = "convergence"
            elif i == self.config.max_iters:
                stop_reason = "max_iters"

            selected_ids = [h.id for h in top]
            record.iterations.append(
                IterationRecord(
                    iteration=i,
                    cortical_state={"pool_size": len(pool.all()), "best_score": best_score},
                    hypotheses=[copy.deepcopy(h) for h in pool.all()],
                    selected_ids=selected_ids,
                    feedback_signal=feedback,
                    stopped=stop_reason is not None,
                    stop_reason=stop_reason,
                )
            )

            if stop_reason:
                record.selected_path.extend(selected_ids)
                break

            refined = self.refiner.refine(task, top, i)
            pool.add(refined)
            prev_best = best_score

        winner = pool.topk(1)
        record.final_answer = winner[0].text if winner else "No hypothesis generated."
        if winner and winner[0].id not in record.selected_path:
            record.selected_path.append(winner[0].id)
        return record
