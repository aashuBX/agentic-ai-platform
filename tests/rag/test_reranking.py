from app.models.rag import Chunk, RetrievedChunk
from app.rag.reranking.factory import build_reranker
from app.rag.reranking.llm_reranker import LLMReranker

_CANDIDATES = [
    RetrievedChunk(
        chunk=Chunk(
            id="c1",
            document_id="d1",
            content="Bananas are yellow and tasty.",
            chunk_index=0,
            strategy="recursive",
        ),
        score=0.05,
        retrieval_method="hybrid_rrf",
    ),
    RetrievedChunk(
        chunk=Chunk(
            id="c2",
            document_id="d1",
            content="Paris is the capital of France.",
            chunk_index=1,
            strategy="recursive",
        ),
        score=0.04,
        retrieval_method="hybrid_rrf",
    ),
]


def test_cross_encoder_reranker_reorders_by_relevance():
    from app.rag.reranking.cross_encoder import CrossEncoderReranker

    reranker = CrossEncoderReranker()
    results = reranker.rerank("What is the capital of France?", _CANDIDATES, top_k=2)

    assert results[0].chunk.id == "c2"
    assert all(r.retrieval_method == "reranked_cross_encoder" for r in results)


def test_llm_reranker_falls_back_to_lexical_overlap_under_mock_provider(mock_llm):
    reranker = LLMReranker(llm=mock_llm)
    results = reranker.rerank("capital of France", _CANDIDATES, top_k=2)

    assert results[0].chunk.id == "c2"
    assert all(r.retrieval_method == "reranked_llm" for r in results)


def test_llm_reranker_handles_empty_candidates(mock_llm):
    assert LLMReranker(llm=mock_llm).rerank("anything", [], top_k=5) == []


def test_reranker_factory_none_returns_none(mock_llm):
    from app.config.settings import RAGSettings

    assert build_reranker(RAGSettings(reranker="none"), mock_llm) is None


def test_reranker_factory_builds_llm_reranker(mock_llm):
    from app.config.settings import RAGSettings

    reranker = build_reranker(RAGSettings(reranker="llm"), mock_llm)
    assert isinstance(reranker, LLMReranker)


def test_reranker_factory_rejects_unknown_choice(mock_llm):
    import pytest

    from app.config.settings import RAGSettings

    with pytest.raises(ValueError):
        build_reranker(RAGSettings(reranker="not-a-real-reranker"), mock_llm)
