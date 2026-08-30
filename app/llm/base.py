"""Provider-agnostic LLM interface (RULE 4: prefer interfaces and adapters).

Every concrete provider (mock/OpenAI/Anthropic/Gemini/Groq) implements `generate()`. Structured
output (`generate_structured`) has one default, provider-agnostic implementation here: ask for
JSON matching the Pydantic schema, parse, validate, retry with a correction prompt on failure.
This is a deliberate simplification over each provider's native structured-output/tool-calling
API — it trades a little reliability for the same behavior across all four providers and the mock,
which matters more for a demo that must work regardless of which provider is configured. A
provider MAY override `generate_structured` later to use its native mechanism.
"""

import json
import re
from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.llm.exceptions import StructuredOutputError
from app.models.enums import MessageRole

T = TypeVar("T", bound=BaseModel)

_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


class LLMMessage(BaseModel):
    """One message in a provider-agnostic chat prompt."""

    role: MessageRole
    content: str


class LLMResponse(BaseModel):
    """Normalized result of a `generate()` call, regardless of provider."""

    content: str
    model: str
    provider: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None


def extract_json_object(text: str) -> dict:
    """Best-effort extraction of a JSON object from free-form model output.

    Handles the common cases: a bare JSON object, or one wrapped in ```json ... ``` fences.
    """

    stripped = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", stripped, re.DOTALL)
    candidate = fence_match.group(1) if fence_match else stripped
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        block_match = _JSON_BLOCK_RE.search(candidate)
        if block_match:
            return json.loads(block_match.group(0))
        raise


class LLMProvider(ABC):
    """Base class every LLM adapter implements."""

    name: str = "base"

    @abstractmethod
    def generate(
        self,
        messages: list[LLMMessage],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        """Produce a free-form text completion for the given chat messages."""

    def generate_structured(
        self,
        messages: list[LLMMessage],
        schema: type[T],
        *,
        max_retries: int = 2,
    ) -> T:
        """Ask the model for JSON matching `schema`, validating and retrying on failure."""

        schema_instruction = LLMMessage(
            role=MessageRole.SYSTEM,
            content=(
                "Respond with ONLY a single JSON object matching this JSON Schema. "
                "Do not include markdown fences or commentary.\n\n"
                f"{json.dumps(schema.model_json_schema())}"
            ),
        )
        working_messages = [schema_instruction, *messages]
        last_error: Exception | None = None

        for _ in range(max_retries + 1):
            response = self.generate(working_messages)
            try:
                data = extract_json_object(response.content)
                return schema.model_validate(data)
            except (json.JSONDecodeError, ValidationError) as exc:
                last_error = exc
                working_messages = [
                    *working_messages,
                    LLMMessage(role=MessageRole.ASSISTANT, content=response.content),
                    LLMMessage(
                        role=MessageRole.USER,
                        content=(
                            f"That response was not valid JSON matching the schema ({exc}). "
                            "Reply again with corrected JSON only."
                        ),
                    ),
                ]

        raise StructuredOutputError(
            f"{self.name}: failed to obtain schema-valid output for {schema.__name__} "
            f"after {max_retries + 1} attempt(s): {last_error}"
        )
