"""HandoffAgent — transfers the conversation to a human.

Deterministic, fixed-copy response by design: handoff scripts are typically fixed copy in real
systems (consistency, legal/tone review), not model-generated, so this reliably works even under
the mock provider and needs no LLM call.
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType

_RESPONSE = (
    "I'm connecting you with a human team member who can help further. "
    "They'll follow up on this conversation shortly."
)


class HandoffAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="handoff_agent",
            agent_type=AgentType.HANDOFF,
            description="Transfers the conversation to a human agent.",
            instructions="Acknowledge the request and hand off to a human; never fabricate a resolution.",
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        return {
            "response": _RESPONSE,
            "metadata": merge_metadata(state, handoff_requested=True),
        }
