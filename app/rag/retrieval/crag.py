"""Corrective RAG (CRAG) strategy: retrieve, evaluate retrieval quality, and if it's poor, rewrite
the query and retrieve again before generating.

Simplification note: the CRAG paper (Yan et al., 2024) trains a dedicated lightweight retrieval
evaluator model. This implementation scores retrieval quality by lexical overlap between the
query and the top-retrieved chunk (scale-independent: 0..1 regardless of whether the underlying
retriever is vector/BM25/hybrid-RRF, whose raw scores live on very different, incomparable
scales) — a cheap, explainable heuristic, not a trained classifier. Documented as a simplification.
"""

import re
from collections.abc import Callable

from pydantic import BaseModel

from app.models.rag import RetrievedChunk
from app.rag.retrieval.query_rewriter import QueryRewriter

_WORD_RE = re.compile(r"[a-z0-9]+")


def lexical_overlap_quality(query: str, results: list[RetrievedChunk]) -> float:
    """Fraction of the query's non-trivial words found in the top-retrieved chunk's text."""

    if not results:
        return 0.0
    query_words = {w for w in _WORD_RE.findall(query.lower()) if len(w) > 2}
    if not query_words:
        return 1.0
    top_words = set(_WORD_RE.findall(results[0].chunk.content.lower()))
    return len(query_words & top_words) / len(query_words)


class CRAGResult(BaseModel):
    initial_quality_score: float
    correction_applied: bool
    rewritten_query: str | None
    retrieved_context: list[str]
    answer: str


class CRAGStrategy:
    def __init__(
        self,
        query_rewriter: QueryRewriter,
        retrieve_fn: Callable[[str], list[RetrievedChunk]],
        generate_fn: Callable[[str, list[str]], str],
        quality_threshold: float = 0.35,
    ) -> None:
        self._rewriter = query_rewriter
        self._retrieve_fn = retrieve_fn
        self._generate_fn = generate_fn
        self._quality_threshold = quality_threshold

    def run(self, query: str) -> CRAGResult:
        results = self._retrieve_fn(query)
        quality = lexical_overlap_quality(query, results)
        correction_applied = False
        rewritten_query = None

        if quality < self._quality_threshold:
            rewritten_query = self._rewriter.rewrite(query)
            if rewritten_query != query:
                corrected_results = self._retrieve_fn(rewritten_query)
                corrected_quality = lexical_overlap_quality(rewritten_query, corrected_results)
                if corrected_results and corrected_quality > quality:
                    results = corrected_results
                    correction_applied = True

        context_texts = [r.chunk.content for r in results]
        answer = self._generate_fn(query, context_texts)
        return CRAGResult(
            initial_quality_score=quality,
            correction_applied=correction_applied,
            rewritten_query=rewritten_query,
            retrieved_context=context_texts,
            answer=answer,
        )
