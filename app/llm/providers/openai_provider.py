"""OpenAI provider adapter.

Requires the `openai` extra (`pip install -e ".[openai]"`) and `LLM__OPENAI_API_KEY`. Implemented
against openai-python's `chat.completions.create` interface, verified against openai==3.5.0 in this
repo's dev environment — if a materially different SDK version changes that surface, this is the
one place to update.
"""

import time

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.llm.exceptions import LLMError, ProviderNotConfiguredError


class OpenAIProvider(LLMProvider):
    name = "openai"

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
                "LLM__PROVIDER=openai requires LLM__OPENAI_API_KEY to be set in your environment/.env."
            )
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                'The "openai" package is not installed. Run: pip install -e ".[openai]"'
            ) from exc

        self._client = OpenAI(api_key=api_key, timeout=timeout)
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
            raise LLMError(f"OpenAI request failed: {exc}") from exc
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
