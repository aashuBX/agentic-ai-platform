"""Schemas for POST /agents/run — invoking one named agent directly, outside the full graph."""

from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    agent_name: str
    message: str = Field(min_length=1, max_length=4000)
    session_id: str = "agent-run-session"


class AgentRunResponse(BaseModel):
    agent: str
    response: str | None
    metadata: dict[str, Any] = Field(default_factory=dict)
