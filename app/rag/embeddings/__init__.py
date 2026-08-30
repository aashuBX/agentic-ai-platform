"""Embedding provider interface, cache, concrete adapters, and the settings-driven factory."""

from app.rag.embeddings.base import EmbeddingProvider
from app.rag.embeddings.cache import (
    CachedEmbeddingProvider,
    EmbeddingCache,
    InMemoryEmbeddingCache,
    SqliteEmbeddingCache,
)
from app.rag.embeddings.factory import build_embedding_provider

__all__ = [
    "CachedEmbeddingProvider",
    "EmbeddingCache",
    "EmbeddingProvider",
    "InMemoryEmbeddingCache",
    "SqliteEmbeddingCache",
    "build_embedding_provider",
]
