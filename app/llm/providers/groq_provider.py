"""Groq provider adapter.

Requires the `groq` extra (`pip install -e ".[groq]"`) and `LLM__GROQ_API_KEY`. Groq's Python SDK
mirrors the OpenAI chat-completions shape, verified against groq==1.7.0 in this repo's dev
environment.
"""

import time

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.llm.exceptions import LLMError, ProviderNotConfiguredError


class GroqProvider(LLMProvider):
    name = "groq"

    def __init__(
        self,
        api_key: str | None,
        model: str,
        default_temperature: float,
        default_max_tokens: int,
        timeout: float,
    ) -> None:
        if not api_key:
            raise ProviderNotConfiguredError(
                "LLM__PROVIDER=groq requires LLM__GROQ_API_KEY to be set in your environment/.env."
            )
        try:
            from groq import Groq
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                'The "groq" package is not installed. Run: pip install -e ".[groq]"'
            ) from exc

        self._client = Groq(api_key=api_key, timeout=timeout)
        self._model = model
        self._default_temperature = default_temperature
        self._default_max_tokens = default_max_tokens

    def generate(
        self,
        messages: list[LLMMessage],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        payload = [{"role": m.role.value, "content": m.content} for m in messages]
        start = time.perf_counter()
        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=payload,
                temperature=temperature if temperature is not None else self._default_temperature,
                max_tokens=max_tokens if max_tokens is not None else self._default_max_tokens,
            )
        except Exception as exc:  # noqa: BLE001 - normalize every SDK/network failure for callers
            raise LLMError(f"Groq request failed: {exc}") from exc
        latency_ms = (time.perf_counter() - start) * 1000

        choice = completion.choices[0]
        usage = completion.usage
        return LLMResponse(
            content=choice.message.content or "",
            model=completion.model,
            provider=self.name,
            latency_ms=latency_ms,
            input_tokens=usage.prompt_tokens if usage else None,
            output_tokens=usage.completion_tokens if usage else None,
        )
