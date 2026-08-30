"""Deterministic, zero-dependency mock LLM provider.

This is the default provider (`LLM__PROVIDER=mock`) so the entire platform — graph, agents, API,
tests — runs offline with no API key. It is a heuristic stand-in, **not** a language model:

- `generate()` passthrough-quotes any retrieved grounding context it is given (agents mark context
  with a leading system message `"CONTEXT: ..."`), or otherwise returns a clearly-labelled
  placeholder string. It never invents facts.
- `generate_structured()` dispatches on the requested schema's class name to a small registry of
  hand-written heuristics — currently just keyword-based intent classification, which is all
  Phase 1 needs. Anything else falls back to a generic, schema-driven "minimal valid instance"
  so the workflow keeps running; that fallback is intentionally dumb and is not a substitute for
  a real model.

Configure a real provider (`LLM__PROVIDER=openai|anthropic|gemini|groq` + matching API key) for
actual language understanding and generation.
"""

import time
from collections.abc import Callable
from enum import Enum
from types import UnionType
from typing import Any, TypeVar, Union, get_args, get_origin

from pydantic import BaseModel

from app.llm.base import LLMMessage, LLMProvider, LLMResponse
from app.models.enums import IntentCategory, MessageRole

T = TypeVar("T", bound=BaseModel)

CONTEXT_PREFIX = "CONTEXT:"

# Ordered: first match wins. Deliberately simple substring rules, not real NLU.
_INTENT_KEYWORDS: dict[IntentCategory, tuple[str, ...]] = {
    IntentCategory.HANDOFF: (
        "human",
        "representative",
        "talk to someone",
        "speak to a person",
        "real person",
        "agent please",
    ),
    IntentCategory.FEEDBACK: (
        "feedback",
        "complaint",
        "unhappy with",
        "leave a review",
        "suggestion box",
    ),
    IntentCategory.CRM_UPDATE: (
        "mark it",
        "mark lead",
        "update the lead",
        "change status",
        "qualify",
        "close the deal",
    ),
    IntentCategory.APPOINTMENT_QUERY: (
        "appointment",
        "schedule a",
        "book a",
        "reschedule",
        "cancel my meeting",
    ),
    IntentCategory.CRM_QUERY: (
        "lead",
        "customer record",
        " account ",
        "crm",
        "pipeline",
        "find the customer",
    ),
    IntentCategory.GRAPH_QUERY: (
        "relationship",
        "connected to",
        "who owns",
        "assigned to",
        "related to",
        "which agent",
    ),
    IntentCategory.FAQ: (
        "what is",
        "how do i",
        "how does",
        "pricing",
        "faq",
        "business hours",
        "policy",
        "refund",
    ),
}


def _keyword_intent(text: str) -> tuple[IntentCategory, float, str]:
    lowered = f" {text.lower()} "
    for intent, keywords in _INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                return intent, 0.72, f"heuristic keyword match: '{kw.strip()}'"
    if "?" in lowered:
        return IntentCategory.KNOWLEDGE_QUERY, 0.55, "question phrasing, no stronger keyword match"
    return IntentCategory.UNKNOWN, 0.3, "no heuristic rule matched"


def _last_user_message(messages: list[LLMMessage]) -> str:
    for message in reversed(messages):
        if message.role == MessageRole.USER:
            return message.content
    return ""


def _context_block(messages: list[LLMMessage]) -> str | None:
    for message in messages:
        if message.role == MessageRole.SYSTEM and message.content.startswith(CONTEXT_PREFIX):
            return message.content.removeprefix(CONTEXT_PREFIX).strip()
    return None


def _default_value_for_annotation(annotation: Any) -> Any:
    """Type-directed placeholder value, used only when no mock heuristic is registered."""

    origin = get_origin(annotation)
    if origin in (Union, UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        annotation = args[0] if args else str
        origin = get_origin(annotation)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation))
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return _default_instance(annotation)
    if annotation in (int, float):
        return 0
    if annotation is bool:
        return False
    if annotation is str:
        return ""
    if origin is list:
        return []
    if origin is dict:
        return {}
    return None


def _default_instance(schema: type[T]) -> T:
    """Best-effort minimal valid instance for a schema with no registered mock heuristic."""

    kwargs: dict[str, Any] = {}
    for field_name, field in schema.model_fields.items():
        if not field.is_required():
            kwargs[field_name] = field.get_default(call_default_factory=True)
        else:
            kwargs[field_name] = _default_value_for_annotation(field.annotation)
    return schema.model_validate(kwargs)


def _mock_intent_classification(messages: list[LLMMessage]) -> dict:
    # Local import keeps this module dependency-light.
    from app.models.intent import IntentClassification

    intent, confidence, reason = _keyword_intent(_last_user_message(messages))
    return IntentClassification(intent=intent, confidence=confidence, reason=reason).model_dump(
        mode="json"
    )


_STRUCTURED_HEURISTICS: dict[str, Callable[[list[LLMMessage]], dict]] = {
    "IntentClassification": _mock_intent_classification,
}


class MockLLMProvider(LLMProvider):
    """Heuristic, offline stand-in for a real LLM. See module docstring for exact behavior."""

    name = "mock"

    def __init__(self, model: str = "mock-heuristic-v1") -> None:
        self._model = model

    def generate(
        self,
        messages: list[LLMMessage],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        start = time.perf_counter()
        context = _context_block(messages)
        user_text = _last_user_message(messages)

        if context:
            content = context
        elif user_text:
            content = (
                "[mock-llm] No real language model is configured, so this is a deterministic "
                f'placeholder response for: "{user_text[:200]}". Set LLM__PROVIDER to openai, '
                "anthropic, gemini, or groq (with the matching API key) for a genuine generated answer."
            )
        else:
            content = "[mock-llm] (received an empty prompt)"

        latency_ms = (time.perf_counter() - start) * 1000
        return LLMResponse(
            content=content,
            model=self._model,
            provider=self.name,
            latency_ms=latency_ms,
            input_tokens=None,
            output_tokens=None,
        )

    def generate_structured(
        self,
        messages: list[LLMMessage],
        schema: type[T],
        *,
        max_retries: int = 2,
    ) -> T:
        heuristic = _STRUCTURED_HEURISTICS.get(schema.__name__)
        data = heuristic(messages) if heuristic is not None else None
        if data is None:
            return _default_instance(schema)
        return schema.model_validate(data)
