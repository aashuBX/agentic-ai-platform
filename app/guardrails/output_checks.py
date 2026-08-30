"""Deterministic output checks.

Phase 1 scope only: schema/shape validity, non-empty, and an obvious-leakage denylist (stack
traces, unrendered template markers). Semantic grounding and hallucination detection are a
separate, LLM-assisted pipeline built in Phase 6 — see requirement.md's HALLUCINATION DETECTION
section — and are deliberately not attempted here.
"""

from app.graph.state import ConversationState
from app.guardrails.base import GuardrailCheck
from app.models.enums import GuardrailStatus
from app.models.guardrails import GuardrailCheckResult


class SchemaValidCheck(GuardrailCheck):
    """Confirms the response is a plain string — catches an agent bug returning None/a dict."""

    name = "schema_valid"

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        response = state.get("response")
        if not isinstance(response, str):
            return GuardrailCheckResult(
                check_name=self.name,
                status=GuardrailStatus.FAILED,
                message=f"Response must be a string, got {type(response).__name__}.",
            )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


class NonEmptyResponseCheck(GuardrailCheck):
    name = "non_empty_response"

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        if not (state.get("response") or "").strip():
            return GuardrailCheckResult(
                check_name=self.name, status=GuardrailStatus.FAILED, message="Response is empty."
            )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


class ProhibitedPatternCheck(GuardrailCheck):
    """Blocks obvious internal-detail leakage: stack traces or unrendered template markers."""

    name = "prohibited_pattern"
    _PATTERNS = ("Traceback (most recent call last)", "{{", "}}", "<script")

    def check(self, state: ConversationState) -> GuardrailCheckResult:
        response = state.get("response") or ""
        for pattern in self._PATTERNS:
            if pattern in response:
                return GuardrailCheckResult(
                    check_name=self.name,
                    status=GuardrailStatus.FAILED,
                    message=f"Response contains a prohibited pattern: {pattern!r}.",
                )
        return GuardrailCheckResult(check_name=self.name, status=GuardrailStatus.PASSED)


OUTPUT_CHECKS: list[GuardrailCheck] = [
    SchemaValidCheck(),
    NonEmptyResponseCheck(),
    ProhibitedPatternCheck(),
]
