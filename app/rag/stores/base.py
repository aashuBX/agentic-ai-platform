"""VectorStore interface (requirement.md VECTOR STORES section)."""

from abc import ABC, abstractmethod

from app.models.rag import Chunk, RetrievedChunk


class VectorStore(ABC):
    name: str

    @abstractmethod
    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """Upsert `chunks` with their pre-computed `embeddings` (same order, same length)."""

    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        """Return the `top_k` nearest chunks to `embedding`, best match first."""

    @abstractmethod
    def delete_by_document_id(self, document_id: str) -> None: ...

    @abstractmethod
    def count(self) -> int: ...
