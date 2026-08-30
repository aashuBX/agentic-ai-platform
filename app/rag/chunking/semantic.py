"""Semantic chunking: groups consecutive sentences while they stay embedding-similar, and starts a
new chunk when cosine similarity between consecutive sentence embeddings drops below a threshold.

Simplification note: this embeds one sentence at a time and compares only adjacent pairs, which is
a simpler (and cheaper) version of published semantic-chunking techniques that use a smoothed
similarity curve over a sentence window and an adaptive (e.g. percentile-based) breakpoint
threshold. It is a real, working use of embeddings, not a heuristic proxy for one.
"""

import re

from app.models.rag import Chunk, Document
from app.rag.chunking.base import ChunkingStrategy
from app.rag.embeddings.base import EmbeddingProvider

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class SemanticChunkingStrategy(ChunkingStrategy):
    name = "semantic"

    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        similarity_threshold: float = 0.5,
        max_chunk_chars: int = 1200,
    ) -> None:
        self._embedder = embedding_provider
        self._similarity_threshold = similarity_threshold
        self._max_chunk_chars = max_chunk_chars

    def chunk(self, document: Document) -> list[Chunk]:
        sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(document.content) if s.strip()]
        if not sentences:
            return []
        if len(sentences) == 1:
            return [self._make_chunk(document, 0, sentences[0])]

        embeddings = self._embedder.embed(sentences)
        chunks: list[Chunk] = []
        current_sentences = [sentences[0]]
        current_len = len(sentences[0])
        index = 0

        for i in range(1, len(sentences)):
            sentence = sentences[i]
            similarity = _cosine_similarity(embeddings[i - 1], embeddings[i])
            exceeds_size = current_len + len(sentence) > self._max_chunk_chars
            if similarity < self._similarity_threshold or exceeds_size:
                chunks.append(self._make_chunk(document, index, " ".join(current_sentences)))
                index += 1
                current_sentences = [sentence]
                current_len = len(sentence)
            else:
                current_sentences.append(sentence)
                current_len += len(sentence)

        if current_sentences:
            chunks.append(self._make_chunk(document, index, " ".join(current_sentences)))
        return chunks
