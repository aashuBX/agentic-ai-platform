"""Vector similarity retriever: embeds the query, searches the configured `VectorStore`."""

from app.models.rag import RetrievedChunk
from app.rag.embeddings.base import EmbeddingProvider
from app.rag.retrieval.base import Retriever
from app.rag.stores.base import VectorStore


class VectorRetriever(Retriever):
    name = "vector"

    def __init__(self, embedding_provider: EmbeddingProvider, vector_store: VectorStore) -> None:
        self._embedder = embedding_provider
        self._store = vector_store

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        embedding = self._embedder.embed_one(query)
        return self._store.query(embedding, top_k=top_k)
