"""Proposition chunking: decomposes text into atomic, self-contained factual statements.

Simplification note: true proposition-based chunking (Chen et al., "Dense X Retrieval") uses a
fine-tuned "propositionizer" model. This implementation prompts the configured LLM to decompose
each paragraph into propositions instead — a practical approximation, not the original technique.
Under the mock provider (no real language understanding), it falls back to one proposition per
sentence rather than feeding the mock's generic placeholder text through as a fake "proposition" —
that fallback is documented here, not silently pretended to be LLM-quality decomposition.
"""

import re

from app.llm.base import LLMMessage, LLMProvider
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

_PROMPT = (
    "Break the following passage into a list of short, atomic, self-contained factual statements "
    "(propositions). Reply with one proposition per line, no numbering, no commentary.\n\n"
    "Passage:\n{text}"
)


class PropositionChunkingStrategy(ChunkingStrategy):
    name = "proposition"

    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    def chunk(self, document: Document) -> list[Chunk]:
        paragraphs = [p.strip() for p in document.content.split("\n\n") if p.strip()]
        chunks: list[Chunk] = []
        index = 0
        for paragraph in paragraphs:
            for proposition in self._propositions_for(paragraph):
                chunks.append(self._make_chunk(document, index, proposition))
                index += 1
        return chunks

    def _propositions_for(self, paragraph: str) -> list[str]:
        if isinstance(self._llm, MockLLMProvider):
            return [s.strip() for s in _SENTENCE_SPLIT_RE.split(paragraph) if s.strip()]
        response = self._llm.generate(
            [LLMMessage(role=MessageRole.USER, content=_PROMPT.format(text=paragraph))]
        )
        lines = [line.strip("-• \t") for line in response.content.splitlines() if line.strip()]
        return lines or [paragraph]
