"""Optional OpenAI-backed LLM client."""

from __future__ import annotations

import os

from corticalloop.llm.base import LLMClient


class OpenAIClient(LLMClient):
    """Thin wrapper around OpenAI Chat Completions."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError("Install optional dependency: pip install openai") from exc
        self._client = OpenAI(api_key=api_key)

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
