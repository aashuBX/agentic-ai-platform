"""Chroma vector store adapter — the local default, no paid service required.

Verified against chromadb==1.5.9's `PersistentClient` / `Collection.add/query/delete` API in this
repo's dev environment.
"""

import json

from app.models.rag import Chunk, RetrievedChunk
from app.rag.stores.base import VectorStore


class ChromaVectorStore(VectorStore):
    name = "chroma"

    def __init__(self, persist_dir: str, collection_name: str) -> None:
        try:
            import chromadb
        except ImportError as exc:
            raise ImportError(
                '"chromadb" is a base dependency — pip install -e . to reinstall it'
            ) from exc

        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection = self._client.get_or_create_collection(collection_name)

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self._collection.add(
            ids=[c.id for c in chunks],
            embeddings=embeddings,
            documents=[c.content for c in chunks],
            metadatas=[self._to_chroma_metadata(c) for c in chunks],
        )

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        total = self.count()
        if total == 0:
            return []
        result = self._collection.query(query_embeddings=[embedding], n_results=min(top_k, total))
        retrieved: list[RetrievedChunk] = []
        for chunk_id, content, metadata, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
            strict=True,
        ):
            chunk = self._from_chroma_metadata(chunk_id, content, metadata)
            # Chroma returns a distance (lower = more similar); negate so higher score = better,
            # matching this repo's convention (BM25/RRF/reranker scores are all "higher is better").
            retrieved.append(
                RetrievedChunk(chunk=chunk, score=-distance, retrieval_method="vector")
            )
        return retrieved

    def delete_by_document_id(self, document_id: str) -> None:
        self._collection.delete(where={"document_id": document_id})

    def count(self) -> int:
        return self._collection.count()

    @staticmethod
    def _to_chroma_metadata(chunk: Chunk) -> dict:
        return {
            "document_id": chunk.document_id,
            "chunk_index": chunk.chunk_index,
            "strategy": chunk.strategy,
            "parent_chunk_id": chunk.parent_chunk_id or "",
            "metadata_json": json.dumps(chunk.metadata),
        }

    @staticmethod
    def _from_chroma_metadata(chunk_id: str, content: str, metadata: dict) -> Chunk:
        return Chunk(
            id=chunk_id,
            document_id=metadata["document_id"],
            content=content,
            chunk_index=metadata["chunk_index"],
            strategy=metadata["strategy"],
            parent_chunk_id=metadata["parent_chunk_id"] or None,
            metadata=json.loads(metadata["metadata_json"]),
        )
