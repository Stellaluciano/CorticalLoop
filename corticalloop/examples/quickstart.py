"""Offline quickstart demo."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from corticalloop import CorticalLoop, LoopConfig


if __name__ == "__main__":
    loop = CorticalLoop(config=LoopConfig(max_iters=3, num_hypotheses=4, top_k=2))
    result = loop.solve(
        task="Design a plan for reducing support ticket response times",
        context={"constraints": ["small team", "no new hires", "within 30 days"]},
    )
    print("Final answer:\n", result.final_answer)
    print("\nIterations:", len(result.record.iterations))
    print("\nRunRecord JSON:\n", result.record.to_json())
