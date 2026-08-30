"""Recursive character/paragraph chunking — the default strategy.

Tries progressively finer separators (paragraph breaks, then lines, then sentence-ish breaks,
then words, then raw characters as a last resort) until every piece fits within `chunk_size`,
then greedily re-merges pieces up to `chunk_size` with `chunk_overlap` characters of overlap
between consecutive chunks. This mirrors the well-known "recursive character text splitter"
pattern (e.g. LangChain's `RecursiveCharacterTextSplitter`), implemented directly here rather than
importing it, to avoid a dependency for what is a small, self-contained amount of logic.
"""

from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy

DEFAULT_SEPARATORS: tuple[str, ...] = ("\n\n", "\n", ". ", " ", "")


class RecursiveChunkingStrategy(ChunkingStrategy):
    name = "recursive"

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        separators: tuple[str, ...] = DEFAULT_SEPARATORS,
    ) -> None:
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._separators = separators

    def chunk(self, document: Document) -> list[Chunk]:
        pieces = self._split(document.content, list(self._separators))
        merged = self._merge(pieces)
        return [
            self._make_chunk(document, i, text) for i, text in enumerate(merged) if text.strip()
        ]

    def _split(self, text: str, separators: list[str]) -> list[str]:
        if len(text) <= self._chunk_size:
            return [text] if text else []
        if not separators:
            return [text[i : i + self._chunk_size] for i in range(0, len(text), self._chunk_size)]

        separator, *rest = separators
        parts = text.split(separator) if separator else list(text)
        result: list[str] = []
        for i, part in enumerate(parts):
            piece = part + separator if separator and i < len(parts) - 1 else part
            if not piece:
                continue
            if len(piece) <= self._chunk_size:
                result.append(piece)
            else:
                result.extend(self._split(piece, rest))
        return result

    def _merge(self, pieces: list[str]) -> list[str]:
        chunks: list[str] = []
        current = ""
        for piece in pieces:
            if current and len(current) + len(piece) > self._chunk_size:
                chunks.append(current)
                tail = current[-self._chunk_overlap :] if self._chunk_overlap else ""
                current = tail + piece
            else:
                current += piece
        if current:
            chunks.append(current)
        return chunks
