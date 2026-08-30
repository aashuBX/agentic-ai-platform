"""Self-RAG / CRAG strategy tests, using fake retrieve/generate functions so these stay fast and
independent of the real vector store or embedding model — they test the *strategy logic*, not the
retrieval pipeline underneath it (that's covered in test_pipeline.py and test_retrieval.py).
"""

from app.models.rag import Chunk, RetrievedChunk
from app.rag.retrieval.crag import CRAGStrategy, lexical_overlap_quality
from app.rag.retrieval.query_rewriter import QueryRewriter
from app.rag.retrieval.self_rag import SelfRAGStrategy, word_overlap_ratio

_RELEVANT_CHUNK = RetrievedChunk(
    chunk=Chunk(
        id="c1",
        document_id="d1",
        content="Support hours are 9am-6pm IST.",
        chunk_index=0,
        strategy="recursive",
    ),
    score=0.05,
    retrieval_method="hybrid_rrf",
)


class TestSelfRAG:
    def test_skips_retrieval_for_chit_chat(self, mock_llm):
        strategy = SelfRAGStrategy(
            llm=mock_llm,
            retrieve_fn=lambda q: [_RELEVANT_CHUNK],
            generate_fn=lambda q, ctx: "Thanks, bye!",
        )
        result = strategy.run("thanks for your help, bye!")
        assert result.retrieval_used is False
        assert result.retrieved_context == []

    def test_retrieves_for_a_factual_question(self, mock_llm):
        strategy = SelfRAGStrategy(
            llm=mock_llm,
            retrieve_fn=lambda q: [_RELEVANT_CHUNK],
            generate_fn=lambda q, ctx: ctx[0] if ctx else "no context",
        )
        result = strategy.run("What are your business hours?")
        assert result.retrieval_used is True
        assert result.is_grounded is True
        assert result.grounding_score == 1.0

    def test_detects_ungrounded_answers(self, mock_llm):
        strategy = SelfRAGStrategy(
            llm=mock_llm,
            retrieve_fn=lambda q: [_RELEVANT_CHUNK],
            generate_fn=lambda q, ctx: "The moon is made of green cheese and unicorns exist.",
            grounding_threshold=0.3,
        )
        result = strategy.run("What are your business hours?")
        assert result.is_grounded is False


def test_word_overlap_ratio_handles_empty_inputs():
    assert word_overlap_ratio("", ["some context"]) == 1.0
    assert word_overlap_ratio("some answer words", []) == 0.0


class TestCRAG:
    def test_good_retrieval_is_not_corrected(self, mock_llm):
        strategy = CRAGStrategy(
            query_rewriter=QueryRewriter(mock_llm),
            retrieve_fn=lambda q: [_RELEVANT_CHUNK],
            generate_fn=lambda q, ctx: "answer",
            quality_threshold=0.1,
        )
        result = strategy.run("business hours support")
        assert result.correction_applied is False
        assert result.initial_quality_score > 0.1

    def test_poor_retrieval_attempts_correction(self, mock_llm):
        strategy = CRAGStrategy(
            query_rewriter=QueryRewriter(mock_llm),
            retrieve_fn=lambda q: [_RELEVANT_CHUNK],
            generate_fn=lambda q, ctx: "answer",
            quality_threshold=0.9,  # unreachable, forces the low-quality branch
        )
        result = strategy.run("business hours support")
        # Under the mock provider, QueryRewriter is a documented no-op, so correction can be
        # attempted but cannot actually change the outcome — this is the honest, expected result.
        assert result.rewritten_query == "business hours support"
        assert result.correction_applied is False

    def test_no_results_scores_zero_quality(self, mock_llm):
        strategy = CRAGStrategy(
            query_rewriter=QueryRewriter(mock_llm),
            retrieve_fn=lambda q: [],
            generate_fn=lambda q, ctx: "no context",
        )
        result = strategy.run("anything")
        assert result.initial_quality_score == 0.0


def test_lexical_overlap_quality_handles_no_results():
    assert lexical_overlap_quality("query", []) == 0.0
