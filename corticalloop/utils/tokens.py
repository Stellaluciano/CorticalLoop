"""Simple token estimation helper."""


def estimate_tokens(text: str) -> int:
    """Estimate token count by rough words-to-tokens mapping."""
    words = len(text.split())
    return max(1, int(words * 1.3))
