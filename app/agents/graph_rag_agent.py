"""GraphRAGAgent — answers relationship/multi-hop queries against the synthetic CRM knowledge
graph (requirement.md GRAPHRAG section: "...GRAPH RETRIEVAL -> GRAPHRAG AGENT -> LLM").
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.graph_rag.context_formatter import GraphContextFormatter
from app.graph_rag.retriever import GraphRetriever
from app.llm.base import LLMMessage, LLMProvider
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, MessageRole

_INSTRUCTIONS = (
    "Answer the user's question using only the relationship facts provided as context. If the "
    "context doesn't contain the relevant relationship, say so plainly instead of guessing."
)

_NO_MATCH_RESPONSE = (
    "I couldn't find that person or relationship in the knowledge graph. "
    'Try including a full name (e.g. "John Doe").'
)


class GraphRAGAgent(BaseAgent):
    def __init__(
        self,
        retriever: GraphRetriever,
        config: AgentConfig | None = None,
        llm: LLMProvider | None = None,
    ) -> None:
        super().__init__(config=config, llm=llm)
        self._retriever = retriever
        self._formatter = GraphContextFormatter()

    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="graph_rag_agent",
            agent_type=AgentType.GRAPH_RAG,
            description="Answers relationship/multi-hop queries against the synthetic CRM knowledge graph.",
            instructions=_INSTRUCTIONS,
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        messages = state.get("messages", [])
        query = next((m.content for m in reversed(messages) if m.role == MessageRole.USER), "")

        paths = self._retriever.retrieve(query)
        if not paths:
            return {
                "response": _NO_MATCH_RESPONSE,
                "retrieved_context": [],
                "metadata": merge_metadata(state, graph_path_count=0),
            }

        context_text = self._formatter.format(paths)
        llm_messages = [
            LLMMessage(role=MessageRole.SYSTEM, content=self.instructions),
            LLMMessage(role=MessageRole.SYSTEM, content=f"CONTEXT: {context_text}"),
            LLMMessage(role=MessageRole.USER, content=query),
        ]
        answer = self.llm.generate(llm_messages)

        return {
            "response": answer.content,
            "retrieved_context": [context_text],
            "metadata": merge_metadata(state, graph_path_count=len(paths)),
        }
