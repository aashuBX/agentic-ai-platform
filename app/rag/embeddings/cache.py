"""Embedding cache abstraction + a caching `EmbeddingProvider` decorator.

Implements requirement.md's EMBEDDINGS flow directly: `get_embedding(text)` -> cache lookup ->
generate if missing -> store result. Implemented as a decorator (`CachedEmbeddingProvider`) so any
`EmbeddingProvider` gets caching without changing its own code.
"""

import hashlib
import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path

from app.rag.embeddings.base import EmbeddingProvider


def _cache_key(provider_name: str, text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{provider_name}:{digest}"


class EmbeddingCache(ABC):
    @abstractmethod
    def get(self, key: str) -> list[float] | None: ...

    @abstractmethod
    def set(self, key: str, value: list[float]) -> None: ...


class InMemoryEmbeddingCache(EmbeddingCache):
    """Process-lifetime cache. Default — no setup required."""

    def __init__(self) -> None:
        self._store: dict[str, list[float]] = {}

    def get(self, key: str) -> list[float] | None:
        return self._store.get(key)

    def set(self, key: str, value: list[float]) -> None:
        self._store[key] = value


class SqliteEmbeddingCache(EmbeddingCache):
    """Persists across process restarts, avoiding re-embedding unchanged text after a redeploy."""

    def __init__(self, path: str | Path) -> None:
        resolved = Path(path)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(resolved), check_same_thread=False)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS embedding_cache (key TEXT PRIMARY KEY, vector TEXT NOT NULL)"
        )
        self._conn.commit()

    def get(self, key: str) -> list[float] | None:
        row = self._conn.execute(
            "SELECT vector FROM embedding_cache WHERE key = ?", (key,)
        ).fetchone()
        return json.loads(row[0]) if row else None

    def set(self, key: str, value: list[float]) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO embedding_cache (key, vector) VALUES (?, ?)",
            (key, json.dumps(value)),
        )
        self._conn.commit()


class CachedEmbeddingProvider(EmbeddingProvider):
    """Wraps another `EmbeddingProvider`, adding cache-lookup-or-generate-and-store per text."""

    def __init__(self, inner: EmbeddingProvider, cache: EmbeddingCache | None = None) -> None:
        self._inner = inner
        self._cache = cache or InMemoryEmbeddingCache()
        self.name = inner.name
        self.dimension = inner.dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        results: list[list[float] | None] = []
        missing_indices: list[int] = []
        missing_texts: list[str] = []

        for i, text in enumerate(texts):
            cached = self._cache.get(_cache_key(self._inner.name, text))
            results.append(cached)
            if cached is None:
                missing_indices.append(i)
                missing_texts.append(text)

        if missing_texts:
            generated = self._inner.embed(missing_texts)
            for i, text, vector in zip(missing_indices, missing_texts, generated, strict=True):
                self._cache.set(_cache_key(self._inner.name, text), vector)
                results[i] = vector

        return results  # type: ignore[return-value]  # every slot filled: cached or just generated
