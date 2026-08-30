"""LLM reranker: asks the configured LLM to score each candidate's relevance to the query.

Under the mock provider, scoring falls back to the same lexical-overlap heuristic CRAG uses for
its quality check, rather than silently returning meaningless placeholder scores from the mock's
generic text. With a real provider, each candidate gets one structured relevance-scoring call —
simple and clear, though it costs one LLM call per candidate (fine for the small candidate lists
this repo reranks; a production system might batch this).
"""

from pydantic import BaseModel, Field

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.rag import RetrievedChunk
from app.rag.reranking.base import Reranker
from app.rag.retrieval.crag import lexical_overlap_quality


class _RelevanceScore(BaseModel):
    relevance: float = Field(ge=0.0, le=1.0)


class LLMReranker(Reranker):
    name = "llm"

    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    def rerank(
        self, query: str, candidates: list[RetrievedChunk], top_k: int
    ) -> list[RetrievedChunk]:
        if not candidates:
            return []

        if isinstance(self._llm, MockLLMProvider):
            rescored = [
                RetrievedChunk(
                    chunk=c.chunk,
                    score=lexical_overlap_quality(query, [c]),
                    retrieval_method="reranked_llm",
                )
                for c in candidates
            ]
        else:
            rescored = [
                RetrievedChunk(
                    chunk=c.chunk,
                    score=self._score(query, c.chunk.content),
                    retrieval_method="reranked_llm",
                )
                for c in candidates
            ]

        rescored.sort(key=lambda r: r.score, reverse=True)
        return rescored[:top_k]

    def _score(self, query: str, passage: str) -> float:
        result = self._llm.generate_structured(
            [
                LLMMessage(
                    role=MessageRole.USER,
                    content=(
                        "On a scale of 0.0 (irrelevant) to 1.0 (highly relevant), how relevant is "
                        f"this passage to the query?\n\nQuery: {query}\n\nPassage: {passage}"
                    ),
                )
            ],
            _RelevanceScore,
        )
        return result.relevance
