"""Document/chunk/retrieval schemas shared across the RAG ingestion and query paths."""

from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A single ingested source document, before chunking."""

    id: str
    source: str = Field(description="File path or logical identifier the content came from")
    title: str
    content: str
    content_hash: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    """One chunk produced by a `ChunkingStrategy`."""

    id: str
    document_id: str
    content: str
    chunk_index: int
    strategy: str = Field(description="Name of the ChunkingStrategy that produced this chunk")
    parent_chunk_id: str | None = Field(
        default=None, description="Set by hierarchical chunking to link a child chunk to its parent"
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    """A chunk plus the score/method that surfaced it — the unit retrievers/rerankers operate on."""

    chunk: Chunk
    score: float
    retrieval_method: str = Field(
        description='e.g. "vector", "bm25", "hybrid_rrf", "reranked_cross_encoder"'
    )


class IngestResult(BaseModel):
    """Outcome of ingesting one document."""

    document_id: str
    chunk_count: int
    was_duplicate: bool
    strategy: str


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    top_k: int | None = Field(default=None, ge=1, le=50)


class RetrievedChunkView(BaseModel):
    """API-facing view of a `RetrievedChunk` — omits internal fields not useful to a client."""

    chunk_id: str
    document_id: str
    content: str
    score: float
    retrieval_method: str

    @classmethod
    def from_retrieved_chunk(cls, retrieved: RetrievedChunk) -> "RetrievedChunkView":
        return cls(
            chunk_id=retrieved.chunk.id,
            document_id=retrieved.chunk.document_id,
            content=retrieved.chunk.content,
            score=retrieved.score,
            retrieval_method=retrieved.retrieval_method,
        )


class KnowledgeSearchResponse(BaseModel):
    query: str
    results: list[RetrievedChunkView]
