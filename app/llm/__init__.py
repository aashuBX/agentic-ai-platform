"""Multi-provider LLM abstraction (RULE 4: interfaces and adapters).

`LLM__PROVIDER=mock` (the default) needs no API key or extra dependency. Real providers are
lazy-imported by `build_llm_provider` and require their SDK extra plus an API key.
"""

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.llm.exceptions import (
    LLMError,
    LLMTimeoutError,
    ProviderNotConfiguredError,
    StructuredOutputError,
)
from app.llm.factory import build_llm_provider

__all__ = [
    "LLMError",
    "LLMMessage",
    "LLMProvider",
    "LLMResponse",
    "LLMTimeoutError",
    "ProviderNotConfiguredError",
    "StructuredOutputError",
    "build_llm_provider",
]
