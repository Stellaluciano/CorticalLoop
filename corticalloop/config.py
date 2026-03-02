"""Configuration objects for CorticalLoop."""

from dataclasses import dataclass


@dataclass
class LoopConfig:
    """Runtime configuration for the recurrent reasoning loop."""

    num_hypotheses: int = 4
    top_k: int = 2
    max_iters: int = 4
    score_threshold: float = 0.8
    convergence_delta: float = 0.01
    max_hypothesis_chars: int = 320
    inhibitory_gate: bool = True
