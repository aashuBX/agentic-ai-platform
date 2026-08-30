"""Vector store adapter tests — literal, tiny vectors throughout, so these run fast with no
embedding model involved. Each store implementation is exercised through the same behavior via
parametrization, which also documents that they satisfy the same `VectorStore` interface.
"""

import pytest

from app.models.rag import Chunk

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
        content="Bananas are yellow and tasty.",
        chunk_index=1,
        strategy="recursive",
    ),
    Chunk(
        id="c3",
        document_id="d2",
        content="The Eiffel Tower is in Paris.",
        chunk_index=0,
        strategy="recursive",
    ),
]
_EMBEDDINGS = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.9, 0.1, 0.0]]


def _chroma_store(tmp_path):
    from app.rag.stores.chroma_store import ChromaVectorStore

    return ChromaVectorStore(persist_dir=str(tmp_path / "chroma"), collection_name="test")


def _faiss_store(tmp_path):
    from app.rag.stores.faiss_store import FAISSVectorStore

    return FAISSVectorStore(
        persist_dir=str(tmp_path / "faiss"), collection_name="test", dimension=3
    )


@pytest.fixture(params=[_chroma_store, _faiss_store], ids=["chroma", "faiss"])
def store(request, tmp_path):
    return request.param(tmp_path)


def test_add_and_count(store):
    assert store.count() == 0
    store.add(_CHUNKS, _EMBEDDINGS)
    assert store.count() == 3


def test_add_with_no_chunks_is_a_safe_no_op(store):
    store.add([], [])
    assert store.count() == 0


def test_query_ranks_the_closest_vector_first(store):
    store.add(_CHUNKS, _EMBEDDINGS)
    results = store.query([0.95, 0.05, 0.0], top_k=2)
    assert len(results) == 2
    assert results[0].chunk.id == "c1"  # nearly identical to the query vector
    assert all(r.retrieval_method == "vector" for r in results)


def test_delete_by_document_id_removes_only_that_documents_chunks(store):
    store.add(_CHUNKS, _EMBEDDINGS)
    store.delete_by_document_id("d1")
    assert store.count() == 1

    remaining = store.query([0.9, 0.1, 0.0], top_k=5)
    assert {r.chunk.id for r in remaining} == {"c3"}


def test_faiss_persists_across_instances(tmp_path):
    from app.rag.stores.faiss_store import FAISSVectorStore

    store1 = FAISSVectorStore(
        persist_dir=str(tmp_path / "faiss"), collection_name="persist", dimension=3
    )
    store1.add(_CHUNKS, _EMBEDDINGS)

    store2 = FAISSVectorStore(
        persist_dir=str(tmp_path / "faiss"), collection_name="persist", dimension=3
    )
    assert store2.count() == 3
    results = store2.query([1.0, 0.0, 0.0], top_k=1)
    assert results[0].chunk.id == "c1"


def test_chroma_persists_across_instances(tmp_path):
    from app.rag.stores.chroma_store import ChromaVectorStore

    store1 = ChromaVectorStore(persist_dir=str(tmp_path / "chroma"), collection_name="persist")
    store1.add(_CHUNKS, _EMBEDDINGS)

    store2 = ChromaVectorStore(persist_dir=str(tmp_path / "chroma"), collection_name="persist")
    assert store2.count() == 3
