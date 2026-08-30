"""Pinecone vector store adapter — optional, needs `VECTOR_STORE__PINECONE_API_KEY`/`_INDEX` and
the `pinecone` extra.

Implemented against pinecone-client==9.1.0's documented API (`upsert`/`query`/`delete`/
`describe_index_stats`, verified via introspection in this repo's dev environment) but **not**
exercised end-to-end against a live index here — Pinecone is a paid cloud service and this repo
does not have a key to test against. If you enable this and hit an API mismatch, this is the one
file to check against your installed `pinecone` version.
"""

from app.models.rag import Chunk, RetrievedChunk
from app.rag.stores.base import VectorStore


class PineconeVectorStore(VectorStore):
    name = "pinecone"

    def __init__(
        self, api_key: str | None, environment: str | None, index_name: str | None, dimension: int
    ) -> None:
        if not api_key or not index_name:
            raise ValueError(
                "Pinecone requires VECTOR_STORE__PINECONE_API_KEY and VECTOR_STORE__PINECONE_INDEX."
            )
        try:
            from pinecone import Pinecone, ServerlessSpec
        except ImportError as exc:
            raise ImportError(
                'Pinecone requires the "pinecone" extra: pip install -e ".[pinecone]"'
            ) from exc

        client = Pinecone(api_key=api_key)
        existing_names = {index.name for index in client.list_indexes()}
        if index_name not in existing_names:
            client.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=environment or "us-east-1"),
            )
        self._index = client.Index(index_name)

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        vectors = [
            {
                "id": chunk.id,
                "values": embedding,
                "metadata": {
                    "document_id": chunk.document_id,
                    "content": chunk.content,
                    "chunk_index": chunk.chunk_index,
                    "strategy": chunk.strategy,
                },
            }
            for chunk, embedding in zip(chunks, embeddings, strict=True)
        ]
        self._index.upsert(vectors=vectors)

    def query(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        response = self._index.query(vector=embedding, top_k=top_k, include_metadata=True)
        results: list[RetrievedChunk] = []
        for match in response.matches:
            metadata = match.metadata
            chunk = Chunk(
                id=match.id,
                document_id=metadata["document_id"],
                content=metadata["content"],
                chunk_index=metadata["chunk_index"],
                strategy=metadata["strategy"],
            )
            results.append(
                RetrievedChunk(chunk=chunk, score=match.score, retrieval_method="vector")
            )
        return results

    def delete_by_document_id(self, document_id: str) -> None:
        self._index.delete(filter={"document_id": {"$eq": document_id}})

    def count(self) -> int:
        stats = self._index.describe_index_stats()
        return stats.total_vector_count
