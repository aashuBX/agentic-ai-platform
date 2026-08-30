"""Generic, configuration-driven agent definition.

Matches requirement.md's AGENT CONFIGURATION section: Identity + Description + Instructions +
Connectors + Knowledge Base + Settings (+ Testing/Logs, which live in the scenarios and
observability layers rather than on the config object itself).
"""

from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import AgentType


class AgentConfig(BaseModel):
    """Declarative configuration for a `BaseAgent`. See each agent's `default_config()`."""

    name: str
    agent_type: AgentType
    description: str
    language: str = "en"
    conversation_style: str = "professional"
    instructions: str
    connectors: list[str] = Field(default_factory=list)
    knowledge_base: list[str] = Field(default_factory=list)
    settings: dict[str, Any] = Field(default_factory=dict)
