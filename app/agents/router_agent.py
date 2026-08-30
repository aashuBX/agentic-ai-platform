"""RouterAgent — deterministic table lookup from classified intent to target agent node.

Kept separate from `IntentAgent` to match requirement.md's workflow diagram, which shows
`agent_router` as its own box between intent detection and the specialized agents. The actual
LangGraph conditional-edge function (`route_by_selected_agent` in app/graph/nodes.py) simply reads
back the `selected_agent` this node writes.

Where an intent's real agent doesn't exist yet in the current phase, it's routed to the explicit
"not_implemented" node rather than silently mishandled or pointed at an unrelated agent.
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, IntentCategory

NOT_IMPLEMENTED_NODE = "not_implemented"

ROUTE_MAP: dict[IntentCategory, str] = {
    IntentCategory.FAQ: "faq_agent",
    IntentCategory.KNOWLEDGE_QUERY: "rag_agent",
    IntentCategory.GRAPH_QUERY: "graph_rag_agent",
    IntentCategory.CRM_QUERY: "crm_agent",
    IntentCategory.CRM_UPDATE: "crm_agent",
    IntentCategory.APPOINTMENT_QUERY: "crm_agent",
    IntentCategory.FEEDBACK: NOT_IMPLEMENTED_NODE,  # Feedback Agent not yet built
    IntentCategory.HANDOFF: "handoff_agent",
    IntentCategory.VOICE_TASK: NOT_IMPLEMENTED_NODE,  # Voice AI lands in Phase 9
    IntentCategory.UNKNOWN: "faq_agent",  # best-effort fallback rather than an immediate dead end
}


class RouterAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="router_agent",
            agent_type=AgentType.ROUTER,
            description="Maps a classified intent to the specialized agent that should handle it.",
            instructions="Deterministic table-based routing from intent to agent name (no LLM call).",
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        intent = state.get("intent")
        intent_category = intent.intent if intent else IntentCategory.UNKNOWN
        target = ROUTE_MAP.get(intent_category, NOT_IMPLEMENTED_NODE)
        return {
            "selected_agent": target,
            "metadata": merge_metadata(state, selected_agent=target),
        }
