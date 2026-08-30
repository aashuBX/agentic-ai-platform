"""CRMAgent — Phase 1 skeleton.

Not yet wired to MCP tools (that integration is Phase 4). Returns an explicit, honest placeholder
so the routing/graph architecture is fully demonstrable end-to-end without pretending a tool call
happened. No LLM call is made here on purpose — there is nothing to ground yet.
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType

_PLANNED_CONNECTORS = [
    "mcp.get_customer",
    "mcp.search_customer",
    "mcp.get_lead",
    "mcp.search_lead",
    "mcp.update_lead",
    "mcp.get_appointment",
    "mcp.create_appointment",
]

_RESPONSE = (
    "This looks like a CRM, lead, or appointment request. Tool execution via MCP is implemented in "
    "Phase 4 of this build and isn't wired up yet in this skeleton, so no CRM data has been read or "
    "changed. See PLAN.md for status."
)


class CRMAgent(BaseAgent):
    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="crm_agent",
            agent_type=AgentType.CRM,
            description="Handles CRM, lead, and appointment requests via MCP tools.",
            instructions="Select and call the appropriate MCP CRM tool for the user's request.",
            connectors=_PLANNED_CONNECTORS,
            settings={"mcp_wired": False},
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        return {
            "response": _RESPONSE,
            "tool_results": [],
            "metadata": merge_metadata(state, crm_tools_wired=False),
        }
