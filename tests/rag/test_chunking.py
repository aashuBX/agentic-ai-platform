import pytest

from app.rag.chunking.factory import STRATEGY_NAMES, ChunkingFactory, UnknownChunkingStrategyError
from app.rag.ingestion.parser import DocumentParser

_SAMPLE_TEXT = (
    "# Getting Started\n\n"
    "This guide walks new administrators through initial setup. Creating a workspace is the "
    "first step. Inviting team members comes next.\n\n"
    "## Billing\n\n"
    "Billing happens monthly or annually. Upgrading a plan takes effect immediately."
)


@pytest.fixture
def sample_document():
    return DocumentParser().parse_text(_SAMPLE_TEXT, source="test", title="Sample")


class _FakeEmbeddingProvider:
    """Deterministic, dependency-free stand-in for semantic chunking's embedding needs."""

    name = "fake"
    dimension = 4

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(t) % 7), 0.0, 0.0, 1.0] for t in texts]


@pytest.mark.parametrize("strategy_name", STRATEGY_NAMES)
def test_every_strategy_produces_real_chunks_for_this_document(
    strategy_name, sample_document, mock_llm
):
    strategy = ChunkingFactory.create(
        strategy_name,
        chunk_size=200,
        chunk_overlap=20,
        llm=mock_llm,
        embedding_provider=_FakeEmbeddingProvider(),
    )
    chunks = strategy.chunk(sample_document)

    assert chunks, f"{strategy_name} produced no chunks"
    assert all(c.document_id == sample_document.id for c in chunks)
    assert all(c.strategy == strategy_name for c in chunks)
    assert all(c.content.strip() for c in chunks)
    # chunk_index must be unique per document regardless of strategy shape (flat or hierarchical)
    assert len({c.chunk_index for c in chunks}) == len(chunks)


def test_hierarchical_chunks_link_children_to_parents(sample_document, mock_llm):
    strategy = ChunkingFactory.create("hierarchical", chunk_size=50, llm=mock_llm)
    chunks = strategy.chunk(sample_document)

    parents = [c for c in chunks if c.metadata.get("level") == "parent"]
    children = [c for c in chunks if c.metadata.get("level") == "child"]
    assert parents
    assert children
    parent_ids = {p.id for p in parents}
    assert all(c.parent_chunk_id in parent_ids for c in children)


def test_late_chunking_keeps_clean_content_but_attaches_embedding_input(sample_document, mock_llm):
    strategy = ChunkingFactory.create("late", chunk_size=200, chunk_overlap=20)
    chunks = strategy.chunk(sample_document)

    assert all("embedding_input" in c.metadata for c in chunks)
    # The clean content must NOT be polluted with the injected context preview.
    assert "Sample" not in chunks[0].content
    assert "Sample" in chunks[0].metadata["embedding_input"]


def test_recursive_respects_chunk_size_bound():
    long_text = "word " * 1000
    document = DocumentParser().parse_text(long_text, source="s", title="t")
    strategy = ChunkingFactory.create("recursive", chunk_size=100, chunk_overlap=10)
    chunks = strategy.chunk(document)

    assert len(chunks) > 1
    assert all(len(c.content) <= 120 for c in chunks)  # some slack for overlap re-attachment


def test_recursive_rejects_overlap_not_smaller_than_chunk_size():
    from app.rag.chunking.recursive import RecursiveChunkingStrategy

    with pytest.raises(ValueError):
        RecursiveChunkingStrategy(chunk_size=100, chunk_overlap=100)


def test_factory_rejects_unknown_strategy():
    with pytest.raises(UnknownChunkingStrategyError):
        ChunkingFactory.create("not-a-real-strategy")


def test_factory_requires_llm_for_llm_based_strategies():
    with pytest.raises(ValueError):
        ChunkingFactory.create("proposition", llm=None)
    with pytest.raises(ValueError):
        ChunkingFactory.create("agentic", llm=None)


def test_factory_requires_embedder_for_semantic_strategy():
    with pytest.raises(ValueError):
        ChunkingFactory.create("semantic", embedding_provider=None)
