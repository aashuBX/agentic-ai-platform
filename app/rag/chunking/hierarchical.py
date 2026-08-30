"""Hierarchical chunking: large 'parent' sections subdivided into smaller 'child' chunks, with each
child linking back to its parent via `parent_chunk_id`. Both parent and child chunks are returned
and stored — parents give coarse context, children give precise retrieval granularity. A real,
working simplification of hierarchical node parsing (e.g. LlamaIndex's), not a fake passthrough.
"""

from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.recursive import RecursiveChunkingStrategy


class HierarchicalChunkingStrategy(ChunkingStrategy):
    name = "hierarchical"

    def __init__(
        self, parent_chunk_size: int = 2000, child_chunk_size: int = 400, chunk_overlap: int = 50
    ) -> None:
        self._parent_splitter = RecursiveChunkingStrategy(
            chunk_size=parent_chunk_size, chunk_overlap=0
        )
        self._child_splitter = RecursiveChunkingStrategy(
            chunk_size=child_chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, document: Document) -> list[Chunk]:
        parents = self._parent_splitter.chunk(document)
        result: list[Chunk] = []
        index = 0

        for parent_pos, parent in enumerate(parents):
            parent_id = f"{document.id}-parent-{parent_pos}"
            result.append(
                Chunk(
                    id=parent_id,
                    document_id=document.id,
                    content=parent.content,
                    chunk_index=index,
                    strategy=self.name,
                    metadata={"level": "parent"},
                )
            )
            index += 1

            child_document = document.model_copy(update={"content": parent.content})
            for child_pos, child in enumerate(self._child_splitter.chunk(child_document)):
                result.append(
                    Chunk(
                        id=f"{parent_id}-child-{child_pos}",
                        document_id=document.id,
                        content=child.content,
                        chunk_index=index,
                        strategy=self.name,
                        parent_chunk_id=parent_id,
                        metadata={"level": "child"},
                    )
                )
                index += 1
        return result
