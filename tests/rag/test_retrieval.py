from app.models.rag import Chunk, RetrievedChunk
from app.rag.retrieval.bm25_retriever import BM25Retriever
from app.rag.retrieval.hybrid_retriever import HybridRetriever, reciprocal_rank_fusion
from app.rag.retrieval.query_rewriter import QueryRewriter
from app.rag.retrieval.vector_retriever import VectorRetriever

_CHUNKS = [
    Chunk(
        id="c1",
        document_id="d1",
        content="Paris is the capital of France.",
        chunk_index=0,
        strategy="recursive",
    ),
    Chunk(
        id="c2",
        document_id="d1",
        content="Bananas are yellow and tasty fruit.",
        chunk_index=1,
        strategy="recursive",
    ),
    Chunk(
        id="c3",
        document_id="d2",
        content="The Eiffel Tower is a famous landmark in Paris.",
        chunk_index=0,
        strategy="recursive",
    ),
]


def _retrieved(chunk_id: str, score: float, method: str = "vector") -> RetrievedChunk:
    chunk = next(c for c in _CHUNKS if c.id == chunk_id)
    return RetrievedChunk(chunk=chunk, score=score, retrieval_method=method)


class TestBM25Retriever:
    def test_finds_lexically_matching_chunks(self):
        retriever = BM25Retriever()
        retriever.index(_CHUNKS)

        results = retriever.search("capital of France", top_k=5)

        assert results
        assert results[0].chunk.id == "c1"
        assert all(r.retrieval_method == "bm25" for r in results)

    def test_returns_nothing_for_a_query_with_no_lexical_overlap(self):
        retriever = BM25Retriever()
        retriever.index(_CHUNKS)

        assert retriever.search("nonexistent gibberish zzz", top_k=5) == []

    def test_empty_index_returns_nothing(self):
        retriever = BM25Retriever()
        assert retriever.search("anything", top_k=5) == []

    def test_reindexing_replaces_the_corpus(self):
        retriever = BM25Retriever()
        retriever.index(_CHUNKS)
        retriever.index([])
        assert retriever.search("Paris", top_k=5) == []


class TestReciprocalRankFusion:
    def test_agreement_across_rankers_boosts_score(self):
        ranking_a = [_retrieved("c1", 0.9), _retrieved("c3", 0.5)]
        ranking_b = [_retrieved("c1", 5.0, "bm25"), _retrieved("c2", 3.0, "bm25")]

        fused = reciprocal_rank_fusion([ranking_a, ranking_b])

        assert fused[0].chunk.id == "c1"  # ranked #1 in both lists
        assert fused[0].retrieval_method == "hybrid_rrf"
        assert {r.chunk.id for r in fused} == {"c1", "c2", "c3"}

    def test_weights_change_which_ranker_dominates(self):
        ranking_a = [_retrieved("c1", 0.9)]
        ranking_b = [_retrieved("c2", 5.0, "bm25")]

        vector_favored = reciprocal_rank_fusion([ranking_a, ranking_b], weights=[0.9, 0.1])
        bm25_favored = reciprocal_rank_fusion([ranking_a, ranking_b], weights=[0.1, 0.9])

        assert vector_favored[0].chunk.id == "c1"
        assert bm25_favored[0].chunk.id == "c2"

    def test_rejects_mismatched_weight_count(self):
        import pytest

        with pytest.raises(ValueError):
            reciprocal_rank_fusion([[_retrieved("c1", 1.0)]], weights=[0.5, 0.5])


class _LiteralVectorStore:
    """Deterministic stand-in for a real VectorStore — returns a fixed ranking regardless of the
    query embedding, so HybridRetriever's wiring can be tested without a real embedder."""

    def __init__(self, results: list[RetrievedChunk]) -> None:
        self._results = results

    def query(self, embedding, top_k):
        return self._results[:top_k]


class _LiteralEmbeddingProvider:
    name = "literal"
    dimension = 3

    def embed_one(self, text: str) -> list[float]:
        return [0.0, 0.0, 0.0]


class TestHybridRetriever:
    def test_fuses_vector_and_bm25_results(self):
        vector_store = _LiteralVectorStore([_retrieved("c1", 0.9), _retrieved("c2", 0.3)])
        vector_retriever = VectorRetriever(_LiteralEmbeddingProvider(), vector_store)
        bm25 = BM25Retriever()
        bm25.index(_CHUNKS)

        hybrid = HybridRetriever(vector_retriever, bm25, candidate_k=5)
        results = hybrid.search("capital of France", top_k=3)

        assert results
        assert all(r.retrieval_method == "hybrid_rrf" for r in results)


def test_query_rewriter_is_a_documented_no_op_under_the_mock_provider(mock_llm):
    rewriter = QueryRewriter(mock_llm)
    assert rewriter.rewrite("what r ur biz hours") == "what r ur biz hours"
