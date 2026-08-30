"""Builds a fully-wired `RAGPipeline` from settings — the single place that assembles the whole
RAG subsystem (embeddings -> vector store -> chunking -> retrieval -> reranking)."""

from app.config.settings import Settings
from app.llm.base import LLMProvider
from app.rag.embeddings.factory import build_embedding_provider
from app.rag.ingestion.repository import RagRepository
from app.rag.pipeline import RAGPipeline
from app.rag.reranking.factory import build_reranker
from app.rag.stores.factory import build_vector_store


def build_rag_pipeline(settings: Settings, llm: LLMProvider) -> RAGPipeline:
    embedding_provider = build_embedding_provider(
        settings.rag, openai_api_key=settings.llm.openai_api_key
    )
    repository = RagRepository(settings.database_url)
    vector_store = build_vector_store(settings, dimension=embedding_provider.dimension)
    reranker = build_reranker(settings.rag, llm)

    return RAGPipeline(
        repository=repository,
        embedding_provider=embedding_provider,
        vector_store=vector_store,
        llm=llm,
        chunk_size=settings.rag.chunk_size,
        chunk_overlap=settings.rag.chunk_overlap,
        chunking_strategy_name=settings.rag.chunking_strategy,
        candidate_k=settings.rag.candidate_k,
        top_k=settings.rag.top_k,
        rrf_k=settings.rag.rrf_k,
        hybrid_vector_weight=settings.rag.hybrid_vector_weight,
        query_rewriting_enabled=settings.rag.query_rewriting_enabled,
        reranker=reranker,
    )
