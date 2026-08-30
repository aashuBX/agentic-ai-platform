"""Full `RAGPipeline` integration tests — real sentence-transformers embeddings, real Chroma
store, real BM25 index, exercising genuine hybrid retrieval end to end (the `rag_pipeline` fixture
is pre-seeded with demo/data/knowledge_documents.json — see tests/conftest.py).
"""


def test_pipeline_is_seeded_with_demo_knowledge(rag_pipeline):
    stats = rag_pipeline.stats()
    assert stats["documents"] == 5
    assert stats["chunks"] > 0


def test_retrieve_finds_the_right_document_for_a_specific_query(rag_pipeline):
    results = rag_pipeline.retrieve("What are the API rate limits?")
    assert results
    assert "60 requests per minute" in results[0].chunk.content


def test_retrieve_finds_a_different_document_for_a_different_query(rag_pipeline):
    results = rag_pipeline.retrieve("How long is customer data retained?")
    assert results
    assert "24 months" in results[0].chunk.content


def test_ingest_text_is_idempotent_via_dedup(rag_pipeline):
    stats_before = rag_pipeline.stats()
    result = rag_pipeline.ingest_text(
        "The NimbusDesk API enforces a default limit of 60 requests per minute per API key, "
        "with burst tolerance up to 120 requests. Enterprise plans can request a higher quota. "
        "Exceeding the limit returns an HTTP 429 response with a Retry-After header indicating "
        "when to resume.",
        source="doc-004",
        title="NimbusDesk API Rate Limits & Quotas",
    )
    assert result.was_duplicate is True
    assert rag_pipeline.stats() == stats_before


def test_ingest_new_document_is_immediately_retrievable(rag_pipeline):
    result = rag_pipeline.ingest_text(
        "NimbusDesk supports single sign-on (SSO) via SAML 2.0 for Enterprise customers. "
        "Configure your identity provider under Settings > Security > SSO.",
        source="doc-sso",
        title="Single Sign-On",
    )
    assert result.was_duplicate is False
    assert result.chunk_count > 0

    results = rag_pipeline.retrieve("How do I configure SSO?")
    assert results
    assert "SAML" in results[0].chunk.content
