"""Shared enums used across schemas, agents, and the LangGraph state."""

from enum import StrEnum


class IntentCategory(StrEnum):
    """Initial intent taxonomy from requirement.md's INTENT DETECTION section."""

    FAQ = "FAQ"
    KNOWLEDGE_QUERY = "KNOWLEDGE_QUERY"
    GRAPH_QUERY = "GRAPH_QUERY"
    CRM_QUERY = "CRM_QUERY"
    CRM_UPDATE = "CRM_UPDATE"
    APPOINTMENT_QUERY = "APPOINTMENT_QUERY"
    FEEDBACK = "FEEDBACK"
    HANDOFF = "HANDOFF"
    VOICE_TASK = "VOICE_TASK"
    UNKNOWN = "UNKNOWN"


class AgentType(StrEnum):
    """Concrete agent kinds. Mirrors requirement.md's AGENT MODEL section."""

    INTENT = "intent"
    ROUTER = "router"
    FAQ = "faq"
    RAG = "rag"
    GRAPH_RAG = "graph_rag"
    CRM = "crm"
    FEEDBACK = "feedback"
    HANDOFF = "handoff"
    INPUT_GUARDRAIL = "input_guardrail"
    OUTPUT_GUARDRAIL = "output_guardrail"


class Channel(StrEnum):
    """Normalized channel identifier — see app/channels/ (Phase 10) for the adapter layer."""

    WEB = "web"
    SMS = "sms"
    WHATSAPP = "whatsapp"
    VOICE = "voice"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class GuardrailStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
