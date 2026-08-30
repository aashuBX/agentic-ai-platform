"""Reranker interface (requirement.md ADVANCED RAG section)."""

from abc import ABC, abstractmethod

from app.models.rag import RetrievedChunk


class Reranker(ABC):
    name: str

    @abstractmethod
    def rerank(
        self, query: str, candidates: list[RetrievedChunk], top_k: int
    ) -> list[RetrievedChunk]:
        """Re-score and re-order `candidates` for `query`, returning the best `top_k`."""
