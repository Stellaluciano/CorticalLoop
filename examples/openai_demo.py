"""Optional OpenAI demo (requires OPENAI_API_KEY + openai package)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from uuid import uuid4

from corticalloop import CorticalLoop
from corticalloop.evaluate import Evaluator
from corticalloop.generate import HypothesisGenerator
from corticalloop.llm.openai_client import OpenAIClient
from corticalloop.refine import Refiner
from corticalloop.types import Hypothesis


class LLMGenerator(HypothesisGenerator):
    def __init__(self, llm: OpenAIClient) -> None:
        self.llm = llm

    def generate(self, task: str, context: dict, num_hypotheses: int) -> list[Hypothesis]:
        prompt = f"Generate {num_hypotheses} concise hypotheses for task: {task}. Context: {context}"
        raw = self.llm.complete(prompt)
        lines = [line.strip("- ") for line in raw.splitlines() if line.strip()]
        return [Hypothesis(id=f"h-{uuid4().hex[:8]}", text=t) for t in lines[:num_hypotheses]]


class LLMEvaluator(Evaluator):
    def __init__(self, llm: OpenAIClient) -> None:
        self.llm = llm

    def evaluate(self, task: str, hypotheses: list[Hypothesis], context: dict) -> dict[str, float]:
        # fallback to simple score parsing heuristic
        scores: dict[str, float] = {}
        for i, hyp in enumerate(hypotheses):
            prompt = f"Score 0-1 for usefulness on task '{task}': {hyp.text}"
            out = self.llm.complete(prompt)
            try:
                val = float(out.strip().split()[0])
            except Exception:
                val = max(0.1, 1.0 - (i * 0.1))
            scores[hyp.id] = max(0.0, min(1.0, val))
        return scores


class LLMRefiner(Refiner):
    def __init__(self, llm: OpenAIClient) -> None:
        self.llm = llm

    def refine(self, task: str, top_hypotheses: list[Hypothesis], iteration: int) -> list[Hypothesis]:
        merged = "\n".join(h.text for h in top_hypotheses)
        refined = self.llm.complete(f"Refine these for task {task} (iteration {iteration}):\n{merged}")
        return [Hypothesis(id=f"h-{uuid4().hex[:8]}", text=refined, parent_ids=[h.id for h in top_hypotheses])]


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY missing. Run examples/quickstart.py for offline demo.")

    client = OpenAIClient()
    loop = CorticalLoop(generator=LLMGenerator(client), evaluator=LLMEvaluator(client), refiner=LLMRefiner(client))
    result = loop.solve("Create an onboarding plan for new AI engineers", context={"deadline": "2 weeks"})
    print(result.final_answer)
