"""Shared pytest fixtures.

Tests must never depend on an external service, a real API key, or the project's real `data/`
directory. `_force_mock_provider` is `autouse` so every test — even ones that don't request it
explicitly — runs against `LLM__PROVIDER=mock` and an isolated SQLite DB / Chroma persist dir
under pytest's `tmp_path`, regardless of what a developer's local `.env` happens to set.

`rag_pipeline` uses the REAL `sentence-transformers` embedding model and a real (temp-dir) Chroma
store rather than a fake — the model is downloaded once by Hugging Face and cached afterward, so
only the very first run of the suite pays a real cost. This is what lets RAGAgent/API tests
exercise genuine hybrid retrieval instead of asserting against a stand-in.
"""

import pytest
from fastapi.testclient import TestClient

from app.agents.registry import AgentRegistry
from app.config.settings import get_settings
from app.graph.workflow import build_workflow
from app.llm.providers.mock import MockLLMProvider


@pytest.fixture(autouse=True)
def _force_mock_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("LLM__PROVIDER", "mock")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setenv("VECTOR_STORE__PERSIST_DIR", str(tmp_path / "chroma"))
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_llm() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture
def rag_pipeline(tmp_path, mock_llm: MockLLMProvider):
    from app.rag.embeddings.cache import CachedEmbeddingProvider, InMemoryEmbeddingCache
    from app.rag.embeddings.sentence_transformers_provider import (
        SentenceTransformerEmbeddingProvider,
    )
    from app.rag.ingestion.repository import RagRepository
    from app.rag.pipeline import RAGPipeline
    from app.rag.seed import seed_demo_knowledge
    from app.rag.stores.chroma_store import ChromaVectorStore

    embedder = CachedEmbeddingProvider(
        SentenceTransformerEmbeddingProvider(), InMemoryEmbeddingCache()
    )
    repository = RagRepository("sqlite:///:memory:")
    store = ChromaVectorStore(persist_dir=str(tmp_path / "rag-chroma"), collection_name="test")
    pipeline = RAGPipeline(
        repository=repository,
        embedding_provider=embedder,
        vector_store=store,
        llm=mock_llm,
        chunk_size=300,
        chunk_overlap=30,
        chunking_strategy_name="recursive",
        candidate_k=10,
        top_k=3,
    )
    seed_demo_knowledge(pipeline)
    return pipeline


@pytest.fixture
def graph_repository():
    from app.graph_rag.builder import GraphBuilder
    from app.graph_rag.entities import RegexEntityExtractor
    from app.graph_rag.memory_repository import InMemoryGraphRepository
    from app.graph_rag.relationships import RegexRelationshipExtractor
    from app.graph_rag.seed import seed_demo_graph

    repository = InMemoryGraphRepository()
    builder = GraphBuilder(RegexEntityExtractor(), RegexRelationshipExtractor(), repository)
    seed_demo_graph(builder)
    return repository


@pytest.fixture
def graph_retriever(graph_repository):
    from app.graph_rag.retriever import GraphRetriever

    return GraphRetriever(graph_repository)


@pytest.fixture
def agent_registry(mock_llm: MockLLMProvider, rag_pipeline, graph_retriever) -> AgentRegistry:
    return AgentRegistry(llm=mock_llm, rag_pipeline=rag_pipeline, graph_retriever=graph_retriever)


@pytest.fixture
def compiled_graph(agent_registry: AgentRegistry):
    return build_workflow(agent_registry)


@pytest.fixture
def api_client():
    from app.api.main import create_app

    with TestClient(create_app()) as client:
        yield client
