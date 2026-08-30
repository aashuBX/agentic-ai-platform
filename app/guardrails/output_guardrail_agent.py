"""OutputGuardrailAgent — last node before END; validates the generated response.

Also appends the final response as an assistant `ChatMessage` to `messages` — this is the one
place in the graph that knows the *final* text (original or guardrail-replaced), so it is the
right place to close out the turn's transcript. Combined with `messages`' `operator.add` reducer
and the checkpointer keyed by session_id (see app/graph/workflow.py), this is what makes
`ConversationState.messages` an actually-accumulating cross-turn transcript rather than a
Phase 1 pretend feature.
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.guardrails.output_checks import OUTPUT_CHECKS
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, MessageRole
from app.models.guardrails import GuardrailReport
from app.models.messages import ChatMessage


class OutputGuardrailAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="output_guardrail_agent",
            agent_type=AgentType.OUTPUT_GUARDRAIL,
            description="Validates the generated response before it is returned to the user.",
            instructions="Ensure the response is a non-empty, well-formed string free of prohibited patterns.",
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        checks = [check.check(state) for check in OUTPUT_CHECKS]
        report = GuardrailReport.from_checks(checks)
        final_response = state.get("response") or ""

        if not report.passed:
            final_response = (
                "I generated a response but it didn't pass output safety checks, so I can't show it. "
                "Please try rephrasing your question."
            )

        return {
            "response": final_response,
            "messages": [ChatMessage(role=MessageRole.ASSISTANT, content=final_response)],
            "guardrail_results": {**state.get("guardrail_results", {}), "output": report},
            "metadata": merge_metadata(state, output_guardrail_passed=report.passed),
        }
