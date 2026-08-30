"""GET /agents, POST /agents/run"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.agents.registry import AgentRegistry
from app.api.deps import get_agent_registry
from app.graph.state import new_conversation_state
from app.models.agent_run import AgentRunRequest, AgentRunResponse
from app.observability import new_trace_id

router = APIRouter(tags=["agents"])


@router.get("/agents")
def list_agents(registry: AgentRegistry = Depends(get_agent_registry)) -> list[dict[str, Any]]:
    return [
        {
            "name": agent.name,
            "agent_type": agent.agent_type.value,
            "description": agent.description,
            "tools": agent.tools,
            "knowledge_sources": agent.knowledge_sources,
        }
        for agent in registry.all()
    ]


@router.post("/agents/run", response_model=AgentRunResponse)
def run_agent(
    request: AgentRunRequest, registry: AgentRegistry = Depends(get_agent_registry)
) -> AgentRunResponse:
    """Runs a single named agent directly against an ad-hoc message — bypasses intent detection
    and routing. Useful for testing/demoing one agent in isolation (see requirement.md API DESIGN)."""

    agent = registry.get(request.agent_name)
    if agent is None:
        available = ", ".join(a.name for a in registry.all())
        raise HTTPException(
            status_code=404,
            detail=f"Unknown agent {request.agent_name!r}. Available: {available}.",
        )

    state = new_conversation_state(
        session_id=request.session_id,
        message_text=request.message,
        trace_id=new_trace_id(),
    )
    update = agent.execute(state)
    return AgentRunResponse(
        agent=agent.name,
        response=update.get("response"),
        metadata=update.get("metadata", {}),
    )
