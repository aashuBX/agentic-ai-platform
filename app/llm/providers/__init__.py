"""Concrete LLMProvider implementations.

Only `mock` is imported eagerly (zero dependencies). The real providers (openai/anthropic/gemini/
groq) are imported lazily by `app.llm.factory` so a missing optional SDK never breaks app startup.
"""

from app.llm.providers.mock import MockLLMProvider

__all__ = ["MockLLMProvider"]
