"""Builds the configured `LLMProvider` from settings.

RULE 1: an unconfigured/unavailable provider raises `ProviderNotConfiguredError` immediately with
actionable instructions — it never silently falls back to another provider or pretends to work.
"""

from app.config.settings import LLMSettings
from app.llm.base import LLMProvider
from app.llm.exceptions import ProviderNotConfiguredError
from app.llm.providers.mock import MockLLMProvider

_SUPPORTED_PROVIDERS = ("mock", "openai", "anthropic", "gemini", "groq")


def build_llm_provider(settings: LLMSettings) -> LLMProvider:
    provider = settings.provider.strip().lower()

    if provider == "mock":
        return MockLLMProvider(model=settings.model)

    if provider == "openai":
        from app.llm.providers.openai_provider import OpenAIProvider

        return OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.model,
            default_temperature=settings.temperature,
            default_max_tokens=settings.max_tokens,
            timeout=settings.request_timeout_seconds,
        )

    if provider == "anthropic":
        from app.llm.providers.anthropic_provider import AnthropicProvider

        return AnthropicProvider(
            api_key=settings.anthropic_api_key,
            model=settings.model,
            default_temperature=settings.temperature,
            default_max_tokens=settings.max_tokens,
            timeout=settings.request_timeout_seconds,
        )

    if provider == "gemini":
        from app.llm.providers.gemini_provider import GeminiProvider

        return GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.model,
            default_temperature=settings.temperature,
            default_max_tokens=settings.max_tokens,
            timeout=settings.request_timeout_seconds,
        )

    if provider == "groq":
        from app.llm.providers.groq_provider import GroqProvider

        return GroqProvider(
            api_key=settings.groq_api_key,
            model=settings.model,
            default_temperature=settings.temperature,
            default_max_tokens=settings.max_tokens,
            timeout=settings.request_timeout_seconds,
        )

    raise ProviderNotConfiguredError(
        f"Unknown LLM__PROVIDER={settings.provider!r}. Expected one of: {', '.join(_SUPPORTED_PROVIDERS)}."
    )
