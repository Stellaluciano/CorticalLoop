"""LLM client interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Minimal chat completion interface."""

    @abstractmethod
    def complete(self, prompt: str) -> str:
        raise NotImplementedError
