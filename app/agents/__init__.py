"""Specialized agents. Every concrete agent subclasses `BaseAgent` (see base.py).

Phase 1: IntentAgent, RouterAgent, FAQAgent, RAGAgent (skeleton), CRMAgent (skeleton),
HandoffAgent. InputGuardrailAgent/OutputGuardrailAgent live in `app.guardrails` since they are
guardrail orchestrators first. GraphRAGAgent (Phase 3) and FeedbackAgent are not implemented yet.
"""

from app.agents.base import BaseAgent
from app.agents.crm_agent import CRMAgent
from app.agents.faq_agent import FAQAgent
from app.agents.handoff_agent import HandoffAgent
from app.agents.intent_agent import IntentAgent
from app.agents.rag_agent import RAGAgent
from app.agents.registry import AgentRegistry
from app.agents.router_agent import RouterAgent

__all__ = [
    "AgentRegistry",
    "BaseAgent",
    "CRMAgent",
    "FAQAgent",
    "HandoffAgent",
    "IntentAgent",
    "RAGAgent",
    "RouterAgent",
]
