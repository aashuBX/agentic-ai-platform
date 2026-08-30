"""Hybrid retrieval: fuses vector + BM25 rankings via Reciprocal Rank Fusion (RRF)."""

from app.models.rag import RetrievedChunk
from app.rag.retrieval.base import Retriever
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.vector_retriever import VectorRetriever


def reciprocal_rank_fusion(
    rankings: list[list[RetrievedChunk]], weights: list[float] | None = None, k: int = 60
) -> list[RetrievedChunk]:
    """Standard RRF: score(chunk) = sum_i weight_i / (k + rank_i(chunk)), 1-indexed ranks.

    `weights` lets one ranker count more than another (e.g. trust vector search over BM25);
    defaults to equal weighting, which is the textbook RRF formula. `k=60` is the standard
    rank-damping constant from the original RRF paper (Cormack et al., 2009).
    """

    if weights is None:
        weights = [1.0] * len(rankings)
    if len(weights) != len(rankings):
        raise ValueError("weights must have the same length as rankings")

    scores: dict[str, float] = {}
    chunk_lookup: dict[str, RetrievedChunk] = {}
    for ranking, weight in zip(rankings, weights, strict=True):
        for rank, retrieved in enumerate(ranking, start=1):
            chunk_id = retrieved.chunk.id
            scores[chunk_id] = scores.get(chunk_id, 0.0) + weight / (k + rank)
            chunk_lookup[chunk_id] = retrieved

    fused = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return [
        RetrievedChunk(
            chunk=chunk_lookup[chunk_id].chunk, score=score, retrieval_method="hybrid_rrf"
        )
        for chunk_id, score in fused
    ]


class HybridRetriever(Retriever):
    name = "hybrid"

    def __init__(
        self,
        vector_retriever: VectorRetriever,
        bm25_retriever: BM25Retriever,
        vector_weight: float = 0.5,
        rrf_k: int = 60,
        candidate_k: int = 20,
    ) -> None:
        self._vector = vector_retriever
        self._bm25 = bm25_retriever
        self._vector_weight = vector_weight
        self._rrf_k = rrf_k
        self._candidate_k = candidate_k

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        vector_results = self._vector.search(query, top_k=self._candidate_k)
        bm25_results = self._bm25.search(query, top_k=self._candidate_k)
        fused = reciprocal_rank_fusion(
            [vector_results, bm25_results],
            weights=[self._vector_weight, 1.0 - self._vector_weight],
            k=self._rrf_k,
        )
        return fused[:top_k]
