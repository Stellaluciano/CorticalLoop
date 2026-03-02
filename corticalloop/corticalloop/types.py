"""Data models for reasoning records."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Hypothesis:
    """A candidate answer/plan within the Hypothesis Pool."""

    id: str
    text: str
    score: float = 0.0
    parent_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class IterationRecord:
    """Information captured for one recurrent-loop iteration."""

    iteration: int
    cortical_state: dict[str, Any] = field(default_factory=dict)
    hypotheses: list[Hypothesis] = field(default_factory=list)
    selected_ids: list[str] = field(default_factory=list)
    feedback_signal: dict[str, float] = field(default_factory=dict)
    stopped: bool = False
    stop_reason: str | None = None


@dataclass
class RunRecord:
    """Full execution log represented as a hypothesis graph over iterations."""

    task: str
    context: dict[str, Any] = field(default_factory=dict)
    iterations: list[IterationRecord] = field(default_factory=list)
    selected_path: list[str] = field(default_factory=list)
    final_answer: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_json(self) -> str:
        payload = asdict(self)
        payload["created_at"] = self.created_at.isoformat()
        return json.dumps(payload, indent=2)


@dataclass
class SolveResult:
    """Return object for agent solve() API."""

    final_answer: str
    record: RunRecord
