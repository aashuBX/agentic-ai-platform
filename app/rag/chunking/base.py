"""Chunking strategy interface (requirement.md CHUNKING section): `ChunkingStrategy.chunk(document)`."""

from abc import ABC, abstractmethod
from typing import Any

from app.models.rag import Chunk, Document


class ChunkingStrategy(ABC):
    name: str

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """Split `document` into one or more `Chunk`s."""

    def _make_chunk(self, document: Document, index: int, content: str, **metadata: Any) -> Chunk:
        return Chunk(
            id=f"{document.id}-chunk-{index}",
            document_id=document.id,
            content=content,
            chunk_index=index,
            strategy=self.name,
            metadata=metadata,
        )
