"""'Late chunking' — simplified approximation.

The real technique (Günther et al., 2024) embeds a document with a long-context transformer
*before* splitting, then mean-pools token-level embeddings per chunk boundary, so each chunk's
embedding carries context from the whole document. That requires token-level embedding access,
which this repo's `EmbeddingProvider` interface (sentence-level `embed(texts) -> vectors`) does not
expose, and a genuine implementation needs a long-context embedding model this repo does not ship.

Approximation implemented here: split first (recursive strategy), then attach a short
whole-document context preview (title + first ~200 characters) as `metadata["embedding_input"]` on
each chunk. `RAGPipeline` embeds that field instead of the raw chunk text when present (see
`app/rag/pipeline.py`), approximating "the chunk's embedding is aware of surrounding document
context" — the chunk's stored/displayed `content` stays the clean original text. This is
documented as an approximation, not the original late-chunking algorithm.
"""

from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.recursive import RecursiveChunkingStrategy

_CONTEXT_PREVIEW_CHARS = 200


class LateChunkingStrategy(ChunkingStrategy):
    name = "late"

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100) -> None:
        self._splitter = RecursiveChunkingStrategy(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, document: Document) -> list[Chunk]:
        context_preview = document.content[:_CONTEXT_PREVIEW_CHARS].strip()
        base_chunks = self._splitter.chunk(document)
        result: list[Chunk] = []
        for base in base_chunks:
            embedding_input = f"[{document.title}] {context_preview}\n\n{base.content}"
            result.append(
                self._make_chunk(
                    document, base.chunk_index, base.content, embedding_input=embedding_input
                )
            )
        return result
