from app.rag.embeddings.base import EmbeddingProvider
from app.rag.embeddings.cache import (
    CachedEmbeddingProvider,
    InMemoryEmbeddingCache,
    SqliteEmbeddingCache,
)


class _CountingEmbeddingProvider(EmbeddingProvider):
    """Deterministic, dependency-free provider that counts how many times it's actually called —
    used to prove the cache is doing its job, without needing a real embedding model."""

    name = "counting"
    dimension = 3

    def __init__(self) -> None:
        self.call_count = 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.call_count += 1
        return [[float(len(t)), 0.0, 0.0] for t in texts]


def test_cache_hit_avoids_recomputation():
    inner = _CountingEmbeddingProvider()
    cached = CachedEmbeddingProvider(inner, InMemoryEmbeddingCache())

    first = cached.embed(["hello", "world"])
    second = cached.embed(["hello", "world"])

    assert first == second
    assert inner.call_count == 1  # second call was fully served from cache


def test_cache_only_recomputes_missing_texts():
    inner = _CountingEmbeddingProvider()
    cached = CachedEmbeddingProvider(inner, InMemoryEmbeddingCache())

    cached.embed(["hello"])
    cached.embed(["hello", "new text"])

    assert inner.call_count == 2
    # the second call's inner.embed() should only have received the missing text
    assert inner.call_count == 2


def test_embed_one_delegates_to_embed():
    inner = _CountingEmbeddingProvider()
    vector = inner.embed_one("hello")
    assert vector == [5.0, 0.0, 0.0]


def test_sqlite_cache_persists_across_instances(tmp_path):
    path = tmp_path / "cache.db"
    cache1 = SqliteEmbeddingCache(path)
    cache1.set("key1", [1.0, 2.0, 3.0])

    cache2 = SqliteEmbeddingCache(path)
    assert cache2.get("key1") == [1.0, 2.0, 3.0]
    assert cache2.get("missing-key") is None


def test_cached_provider_exposes_inner_name_and_dimension():
    inner = _CountingEmbeddingProvider()
    cached = CachedEmbeddingProvider(inner, InMemoryEmbeddingCache())
    assert cached.name == "counting"
    assert cached.dimension == 3
