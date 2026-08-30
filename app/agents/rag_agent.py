"""RAGAgent — Phase 2: backed by the real `RAGPipeline` (chunking -> embeddings -> Chroma/FAISS ->
hybrid vector+BM25 retrieval -> RRF -> optional reranking), not the Phase 1 keyword skeleton.

The agent's own shape didn't need to change from Phase 1 (retrieve, ground, generate) — only what
backs retrieval did, which is exactly the point of keeping `RAGPipeline` behind a small interface.

One thing that DOES need explicit handling here: vector search always returns its nearest
neighbors, even when nothing in the store is actually relevant (there is no "no results" case for
cosine similarity the way there was for Phase 1's keyword matcher, or the way BM25 alone would
naturally score an unrelated query as 0). Left unchecked, that means the agent would confidently
"answer" from irrelevant chunks for an off-topic query. `_MIN_RELEVANCE` gates on the same
scale-independent lexical-overlap heuristic CRAG uses, to catch that case honestly.
"""

from typing import Any

from app.agents.base import BaseAgent
from app.graph.state import ConversationState, merge_metadata
from app.llm.base import LLMMessage, LLMProvider
from app.models.agent_config import AgentConfig
from app.models.enums import AgentType, MessageRole
from app.rag.pipeline import RAGPipeline
from app.rag.retrieval.crag import lexical_overlap_quality

_INSTRUCTIONS = (
    "Answer the user's question using only the retrieved document context. Cite the source when "
    "it's clear from the context. If the context doesn't answer the question, say so plainly."
)

_NO_MATCH_RESPONSE = (
    "I couldn't find relevant documentation for that. Try rephrasing, or ask to speak with a human."
)

_MIN_RELEVANCE = 0.15


class RAGAgent(BaseAgent):
    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        config: AgentConfig | None = None,
        llm: LLMProvider | None = None,
    ) -> None:
        super().__init__(config=config, llm=llm)
        self._pipeline = rag_pipeline

    @classmethod
    def default_config(cls) -> AgentConfig:
        return AgentConfig(
            name="rag_agent",
            agent_type=AgentType.RAG,
            description="Retrieves grounded answers via hybrid (vector+BM25) retrieval with RRF and reranking.",
            instructions=_INSTRUCTIONS,
            settings={"pipeline_phase": "phase2_full_pipeline"},
        )

    def _run(self, state: ConversationState) -> dict[str, Any]:
        messages = state.get("messages", [])
        query = next((m.content for m in reversed(messages) if m.role == MessageRole.USER), "")

        retrieved = self._pipeline.retrieve(query)
        relevance = lexical_overlap_quality(query, retrieved) if retrieved else 0.0
        if not retrieved or relevance < _MIN_RELEVANCE:
            return {
                "response": _NO_MATCH_RESPONSE,
                "retrieved_context": [],
                "metadata": merge_metadata(
                    state, rag_match_count=0, rag_relevance=round(relevance, 3)
                ),
            }

        context_texts = [r.chunk.content for r in retrieved]
        context_block = "\n\n---\n\n".join(context_texts)
        llm_messages = [
            LLMMessage(role=MessageRole.SYSTEM, content=self.instructions),
            LLMMessage(role=MessageRole.SYSTEM, content=f"CONTEXT: {context_block}"),
            LLMMessage(role=MessageRole.USER, content=query),
        ]
        answer = self.llm.generate(llm_messages)

        return {
            "response": answer.content,
            "retrieved_context": context_texts,
            "metadata": merge_metadata(
                state,
                rag_match_count=len(retrieved),
                rag_top_chunk_id=retrieved[0].chunk.id,
                rag_top_score=round(retrieved[0].score, 4),
                rag_retrieval_method=retrieved[0].retrieval_method,
                rag_pipeline_phase="phase2_full_pipeline",
            ),
        }
