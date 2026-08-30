"""Google Gemini provider adapter.

Requires the `gemini` extra (`pip install -e ".[gemini]"`) and `LLM__GEMINI_API_KEY`. Uses the
`google-genai` SDK (verified against google-genai==2.20.0 in this repo's dev environment), which
uses role "model" instead of "assistant" and takes system instructions via `GenerateContentConfig`
rather than as a message — this adapter translates our provider-agnostic message list accordingly.
"""

import time

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.llm.exceptions import LLMError, ProviderNotConfiguredError
from app.models.enums import MessageRole


class GeminiProvider(LLMProvider):
    name = "gemini"

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
                "LLM__PROVIDER=gemini requires LLM__GEMINI_API_KEY to be set in your environment/.env."
            )
        try:
            from google import genai
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                'The "google-genai" package is not installed. Run: pip install -e ".[gemini]"'
            ) from exc

        self._genai = genai
        self._client = genai.Client(api_key=api_key)
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
        from google.genai import types

        system_text = "\n\n".join(m.content for m in messages if m.role == MessageRole.SYSTEM)
        contents = [
            types.Content(
                role="model" if m.role == MessageRole.ASSISTANT else "user",
                parts=[types.Part(text=m.content)],
            )
            for m in messages
            if m.role in (MessageRole.USER, MessageRole.ASSISTANT)
        ]
        if not contents:
            raise LLMError("Gemini request requires at least one user/assistant message.")

        config = types.GenerateContentConfig(
            system_instruction=system_text or None,
            temperature=temperature if temperature is not None else self._default_temperature,
            max_output_tokens=max_tokens if max_tokens is not None else self._default_max_tokens,
        )

        start = time.perf_counter()
        try:
            response = self._client.models.generate_content(
                model=self._model, contents=contents, config=config
            )
        except Exception as exc:  # noqa: BLE001 - normalize every SDK/network failure for callers
            raise LLMError(f"Gemini request failed: {exc}") from exc
        latency_ms = (time.perf_counter() - start) * 1000

        usage = response.usage_metadata
        return LLMResponse(
            content=response.text or "",
            model=self._model,
            provider=self.name,
            latency_ms=latency_ms,
            input_tokens=usage.prompt_token_count if usage else None,
            output_tokens=usage.candidates_token_count if usage else None,
        )
