"""Guardrail check interface — one reusable shape for both input and output checks."""

from abc import ABC, abstractmethod

from app.graph.state import ConversationState
from app.models.guardrails import GuardrailCheckResult


class GuardrailCheck(ABC):
    """A single, independently-testable rule. `InputGuardrailAgent`/`OutputGuardrailAgent`
    run a list of these and aggregate the results into one `GuardrailReport`."""

    name: str

    @abstractmethod
    def check(self, state: ConversationState) -> GuardrailCheckResult: ...
