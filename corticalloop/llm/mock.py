"""Offline mock LLM client."""

from corticalloop.llm.base import LLMClient


class MockLLMClient(LLMClient):
    """Deterministic local completion for demos/tests."""

    def complete(self, prompt: str) -> str:
        return f"[MockLLM] {prompt[:180]}"
