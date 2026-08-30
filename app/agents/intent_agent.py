"""IntentAgent — classifies the latest user message into a routing intent.

Uses structured output (`IntentClassification`) so only concise routing metadata is stored —
never raw chain-of-thought (RULE 5).
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.llm.base import LLMMessage
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, MessageRole
from app.models.intent import IntentClassification

_INSTRUCTIONS = (
    "Classify the user's most recent message into exactly one intent category from the provided "
    "schema. Respond only with the requested structured JSON — do not explain your reasoning in prose."
)


class IntentAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="intent_agent",
            agent_type=AgentType.INTENT,
            description="Classifies user requests into a routing intent with a confidence score.",
            instructions=_INSTRUCTIONS,
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        messages = state.get("messages", [])
        latest_user_text = next(
            (m.content for m in reversed(messages) if m.role == MessageRole.USER), ""
        )
        llm_messages = [
            LLMMessage(role=MessageRole.SYSTEM, content=self.instructions),
            LLMMessage(role=MessageRole.USER, content=latest_user_text),
        ]
        classification = self.llm.generate_structured(llm_messages, IntentClassification)
        return {
            "intent": classification,
            "metadata": merge_metadata(
                state,
                intent=classification.intent.value,
                intent_confidence=classification.confidence,
                intent_reason=classification.reason,
            ),
        }
