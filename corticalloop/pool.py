"""Hypothesis pool operations."""

from __future__ import annotations

from corticalloop.types import Hypothesis


class HypothesisPool:
    """Stores and ranks hypotheses across loop iterations."""

    def __init__(self) -> None:
        self._items: dict[str, Hypothesis] = {}

    def add(self, hypotheses: list[Hypothesis]) -> None:
        for hypothesis in hypotheses:
            self._items[hypothesis.id] = hypothesis

    def all(self) -> list[Hypothesis]:
        return list(self._items.values())

    def topk(self, k: int) -> list[Hypothesis]:
        return sorted(self._items.values(), key=lambda h: h.score, reverse=True)[:k]

    def prune_below(self, threshold: float) -> None:
        self._items = {hid: hyp for hid, hyp in self._items.items() if hyp.score >= threshold}

    def clear(self) -> None:
        self._items = {}
