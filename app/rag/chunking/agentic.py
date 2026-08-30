"""'Agentic' chunking: an LLM iteratively decides chunk boundaries rather than using fixed rules —
for each new sentence, it is asked whether the sentence continues the current chunk's topic or
should start a new chunk.

Simplification note: this is a lightweight approximation — one small structured decision per
sentence boundary — not a full planning/reasoning agent. Under the mock provider it falls back to
the recursive strategy, since a keyword-heuristic model has no real basis for a topic-continuation
judgment; that fallback is documented here rather than silently faked.
"""

import re

from pydantic import BaseModel

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.recursive import RecursiveChunkingStrategy

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


class _BoundaryDecision(BaseModel):
    continues_current_chunk: bool


class AgenticChunkingStrategy(ChunkingStrategy):
    name = "agentic"

    def __init__(self, llm: LLMProvider, max_chunk_chars: int = 1200) -> None:
        self._llm = llm
        self._max_chunk_chars = max_chunk_chars
        self._fallback = RecursiveChunkingStrategy(chunk_size=max_chunk_chars, chunk_overlap=100)

    def chunk(self, document: Document) -> list[Chunk]:
        if isinstance(self._llm, MockLLMProvider):
            return [
                self._make_chunk(document, c.chunk_index, c.content)
                for c in self._fallback.chunk(document)
            ]

        sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(document.content) if s.strip()]
        if not sentences:
            return []

        chunks: list[Chunk] = []
        current = sentences[0]
        index = 0
        for sentence in sentences[1:]:
            exceeds_size = len(current) + len(sentence) > self._max_chunk_chars
            if exceeds_size or not self._continues(current, sentence):
                chunks.append(self._make_chunk(document, index, current))
                index += 1
                current = sentence
            else:
                current = f"{current} {sentence}"
        chunks.append(self._make_chunk(document, index, current))
        return chunks

    def _continues(self, current_chunk: str, next_sentence: str) -> bool:
        decision = self._llm.generate_structured(
            [
                LLMMessage(
                    role=MessageRole.USER,
                    content=(
                        f"Current chunk:\n{current_chunk}\n\n"
                        f"Next sentence: {next_sentence}\n\n"
                        "Does the next sentence continue the same topic as the current chunk?"
                    ),
                )
            ],
            _BoundaryDecision,
        )
        return decision.continues_current_chunk
