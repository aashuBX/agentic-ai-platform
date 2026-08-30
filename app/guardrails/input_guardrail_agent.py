"""InputGuardrailAgent — first node after START; validates the request before intent detection."""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.guardrails.input_checks import INPUT_CHECKS
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, GuardrailStatus
from app.models.guardrails import GuardrailReport


class InputGuardrailAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="input_guardrail_agent",
            agent_type=AgentType.INPUT_GUARDRAIL,
            description="Validates incoming requests before they reach the intent classifier.",
            instructions="Reject empty, oversized, or unsafe-pattern requests without calling an LLM.",
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        checks = [check.check(state) for check in INPUT_CHECKS]
        report = GuardrailReport.from_checks(checks)
        update: dict[str, Any] = {
            "guardrail_results": {**state.get("guardrail_results", {}), "input": report},
            "metadata": merge_metadata(state, input_guardrail_passed=report.passed),
        }
        if not report.passed:
            failed = next(c for c in checks if c.status == GuardrailStatus.FAILED)
            update["response"] = (
                f"Your request couldn't be processed ({failed.message}) Please rephrase and try again."
            )
        return update
