"""Anthropic provider adapter.

Requires the `anthropic` extra (`pip install -e ".[anthropic]"`) and `LLM__ANTHROPIC_API_KEY`.
Verified against anthropic==1.2.0 in this repo's dev environment. Anthropic's API takes system
instructions as a separate top-level `system` parameter rather than a message with role "system",
so this adapter splits our provider-agnostic message list accordingly.
"""

import time

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.llm.exceptions import LLMError, ProviderNotConfiguredError
from app.models.enums import MessageRole


class AnthropicProvider(LLMProvider):
    name = "anthropic"

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
                "LLM__PROVIDER=anthropic requires LLM__ANTHROPIC_API_KEY to be set in your environment/.env."
            )
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                'The "anthropic" package is not installed. Run: pip install -e ".[anthropic]"'
            ) from exc

        self._client = Anthropic(api_key=api_key, timeout=timeout)
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
        system_text = "\n\n".join(m.content for m in messages if m.role == MessageRole.SYSTEM)
        turns = [
            {"role": m.role.value, "content": m.content}
            for m in messages
            if m.role in (MessageRole.USER, MessageRole.ASSISTANT)
        ]
        if not turns:
            raise LLMError("Anthropic request requires at least one user/assistant message.")

        start = time.perf_counter()
        try:
            message = self._client.messages.create(
                model=self._model,
                system=system_text or None,
                messages=turns,
                temperature=temperature if temperature is not None else self._default_temperature,
                max_tokens=max_tokens if max_tokens is not None else self._default_max_tokens,
            )
        except Exception as exc:  # noqa: BLE001 - normalize every SDK/network failure for callers
            raise LLMError(f"Anthropic request failed: {exc}") from exc
        latency_ms = (time.perf_counter() - start) * 1000

        text = "".join(
            block.text for block in message.content if getattr(block, "type", None) == "text"
        )
        usage = message.usage
        return LLMResponse(
            content=text,
            model=message.model,
            provider=self.name,
            latency_ms=latency_ms,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
        )
