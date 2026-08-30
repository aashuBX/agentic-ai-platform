"""Deterministic input checks. All rule-based on purpose — no LLM call needed, so these can never
be jailbroken by the very input they are inspecting.

`UnsafePatternCheck` is a documented simplification: a small regex denylist for obvious cases, not
a general-purpose prompt-injection/jailbreak defense. requirement.md is explicit that limitations
must be stated rather than implied to be more than they are.
"""

import re

from app.graph.state import ConversationState
from app.guardrails.base import GuardrailCheck
from app.models.enums import GuardrailStatus, MessageRole
from app.models.guardrails import GuardrailCheckResult

MAX_MESSAGE_LENGTH = 4000

_UNSAFE_PATTERNS = (
    re.compile(r"ignore\b.{0,30}\binstructions\b", re.IGNORECASE),
    re.compile(r"reveal (your|the) (system prompt|instructions)", re.IGNORECASE),
    re.compile(r"<script[^>]*>", re.IGNORECASE),
)


def _latest_user_text(state: ConversationState) -> str:
    for message in reversed(state.get("messages", [])):
        if message.role == MessageRole.USER:
            return message.content
    return ""


class NotEmptyCheck(GuardrailCheck):
    name = "not_empty"

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        if not _latest_user_text(state).strip():
            return GuardrailCheckResult(
                check_name=self.name, status=GuardrailStatus.FAILED, message="Message is empty."
            )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


class OversizedRequestCheck(GuardrailCheck):
    name = "oversized_request"

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        length = len(_latest_user_text(state))
        if length > MAX_MESSAGE_LENGTH:
            return GuardrailCheckResult(
                check_name=self.name,
                status=GuardrailStatus.FAILED,
                message=f"Message is {length} characters, exceeding the {MAX_MESSAGE_LENGTH} limit.",
            )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


class UnsafePatternCheck(GuardrailCheck):
    name = "unsafe_pattern"

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        text = _latest_user_text(state)
        for pattern in _UNSAFE_PATTERNS:
            if pattern.search(text):
                return GuardrailCheckResult(
                    check_name=self.name,
                    status=GuardrailStatus.FAILED,
                    message="Message matched a disallowed pattern.",
                )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


INPUT_CHECKS: list[GuardrailCheck] = [
    NotEmptyCheck(),
    OversizedRequestCheck(),
    UnsafePatternCheck(),
]
