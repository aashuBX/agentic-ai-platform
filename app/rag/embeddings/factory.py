"""Builds the configured `EmbeddingProvider`, always wrapped in a cache (RULE 4: adapters)."""

from app.config.settings import BASE_DIR, RAGSettings
from app.llm.exceptions import ProviderNotConfiguredError
from app.rag.embeddings.base import EmbeddingProvider
from app.rag.embeddings.cache import (
    CachedEmbeddingProvider,
    InMemoryEmbeddingCache,
    SqliteEmbeddingCache,
)

_SUPPORTED_PROVIDERS = ("sentence_transformers", "openai")


def build_embedding_provider(
    rag_settings: RAGSettings, openai_api_key: str | None = None
) -> EmbeddingProvider:
    provider_name = rag_settings.embedding_provider.strip().lower()

    if provider_name == "sentence_transformers":
        from app.rag.embeddings.sentence_transformers_provider import (
            SentenceTransformerEmbeddingProvider,
        )

        inner: EmbeddingProvider = SentenceTransformerEmbeddingProvider(
            model_name=rag_settings.embedding_model
        )
    elif provider_name == "openai":
        from app.rag.embeddings.openai_provider import OpenAIEmbeddingProvider

        inner = OpenAIEmbeddingProvider(api_key=openai_api_key, model=rag_settings.embedding_model)
    else:
        raise ProviderNotConfiguredError(
            f"Unknown RAG__EMBEDDING_PROVIDER={rag_settings.embedding_provider!r}. "
            f"Expected one of: {_SUPPORTED_PROVIDERS}."
        )

    cache = (
        SqliteEmbeddingCache(BASE_DIR / "data" / "embedding_cache.db")
        if rag_settings.embedding_cache_persistent
        else InMemoryEmbeddingCache()
    )
    return CachedEmbeddingProvider(inner=inner, cache=cache)
