"""LLM routing gateway for TalentFlow-AI (LiteLLM with offline fallback)."""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

_LITELLM_AVAILABLE = False
try:
    import litellm  # noqa: F401

    _LITELLM_AVAILABLE = True
except ImportError:
    pass


def is_llm_available() -> bool:
    """Return True if an LLM API key is configured and litellm is importable."""
    if not _LITELLM_AVAILABLE:
        return False
    keys = [
        os.environ.get("OPENAI_API_KEY"),
        os.environ.get("ANTHROPIC_API_KEY"),
        os.environ.get("GEMINI_API_KEY"),
    ]
    return any(k for k in keys)


def complete(prompt: str, model: str = "gpt-4o-mini", max_tokens: int = 1024) -> str:
    """Call LLM completion; raises RuntimeError if unavailable."""
    if not is_llm_available():
        raise RuntimeError("No LLM API keys configured or litellm unavailable.")
    import litellm

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""
