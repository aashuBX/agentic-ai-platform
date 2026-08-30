"""Single source of truth for "all agent instances in this process".

Used by both the LangGraph workflow builder (`app.graph.workflow.build_workflow`) and the
`/agents` API routes, so there is exactly one instance — and one config — per agent per process.
"""

from app.agents.base import BaseAgent
from app.agents.crm_agent import CRMAgent
from app.agents.faq_agent import FAQAgent
from app.agents.graph_rag_agent import GraphRAGAgent
from app.agents.handoff_agent import HandoffAgent
from app.agents.intent_agent import IntentAgent
from app.agents.rag_agent import RAGAgent
from app.agents.router_agent import RouterAgent
from app.graph_rag.retriever import GraphRetriever
from app.guardrails.input_guardrail_agent import InputGuardrailAgent
from app.guardrails.output_guardrail_agent import OutputGuardrailAgent
from app.llm.base import LLMProvider
from app.rag.pipeline import RAGPipeline


class AgentRegistry:
    """Constructs every agent with a shared LLM provider (and, for `RAGAgent`/`GraphRAGAgent`, a
    shared `RAGPipeline`/`GraphRetriever` — see `app.rag.factory` / `app.graph_rag.factory`)."""

    def __init__(
        self, llm: LLMProvider, rag_pipeline: RAGPipeline, graph_retriever: GraphRetriever
    ) -> None:
        self.input_guardrail = InputGuardrailAgent(llm=llm)
        self.intent = IntentAgent(llm=llm)
        self.router = RouterAgent(llm=llm)
        self.faq = FAQAgent(llm=llm)
        self.rag = RAGAgent(rag_pipeline=rag_pipeline, llm=llm)
        self.graph_rag = GraphRAGAgent(retriever=graph_retriever, llm=llm)
        self.crm = CRMAgent(llm=llm)
        self.handoff = HandoffAgent(llm=llm)
        self.output_guardrail = OutputGuardrailAgent(llm=llm)

    def all(self) -> list[BaseAgent]:
        return [
            self.input_guardrail,
            self.intent,
            self.router,
            self.faq,
            self.rag,
            self.graph_rag,
            self.crm,
            self.handoff,
            self.output_guardrail,
        ]

    def get(self, name: str) -> BaseAgent | None:
        return next((agent for agent in self.all() if agent.name == name), None)
