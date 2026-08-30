"""Document-aware chunking: splits on structural boundaries (markdown headers `#`..`######`, or
blank-line-separated paragraphs as a fallback for unstructured text) before falling back to
recursive splitting within any section that is still too large. A real, working implementation —
not a passthrough — though it only understands markdown-style structure, not arbitrary formats.
"""

import re

from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.recursive import RecursiveChunkingStrategy

_HEADER_RE = re.compile(r"^(#{1,6})\s+.*$", re.MULTILINE)


class DocumentAwareChunkingStrategy(ChunkingStrategy):
    name = "document_aware"

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100) -> None:
        self._chunk_size = chunk_size
        self._fallback = RecursiveChunkingStrategy(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk(self, document: Document) -> list[Chunk]:
        sections = self._split_into_sections(document.content)
        chunks: list[Chunk] = []
        index = 0
        for section_title, section_text in sections:
            if not section_text.strip():
                continue
            if len(section_text) <= self._chunk_size:
                chunks.append(
                    self._make_chunk(document, index, section_text, section=section_title)
                )
                index += 1
            else:
                sub_document = document.model_copy(update={"content": section_text})
                for sub_chunk in self._fallback.chunk(sub_document):
                    chunks.append(
                        self._make_chunk(document, index, sub_chunk.content, section=section_title)
                    )
                    index += 1
        return chunks

    def _split_into_sections(self, text: str) -> list[tuple[str, str]]:
        matches = list(_HEADER_RE.finditer(text))
        if not matches:
            paragraphs = [p for p in text.split("\n\n") if p.strip()]
            if not paragraphs:
                return [("document", text)]
            return [(f"paragraph-{i}", p) for i, p in enumerate(paragraphs)]

        sections: list[tuple[str, str]] = []
        for i, match in enumerate(matches):
            start = match.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            sections.append((match.group(0).strip(), text[start:end].strip()))
        return sections
