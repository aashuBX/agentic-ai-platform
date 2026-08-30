"""BM25 lexical retriever using `rank_bm25`.

Rebuilds its in-memory index from the full chunk corpus via `index()` (`rank_bm25.BM25Okapi` has
no incremental-add API). Not persistent on its own — `RAGPipeline` rebuilds it from
`RagRepository.all_chunks()` after every ingest and on startup, so a process restart doesn't lose
lexical search.
"""

import re

from app.models.rag import Chunk, RetrievedChunk
from app.rag.retrieval.base import Retriever

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class BM25Retriever(Retriever):
    name = "bm25"

    def __init__(self) -> None:
        self._bm25 = None
        self._chunks: list[Chunk] = []

    def index(self, chunks: list[Chunk]) -> None:
        self._chunks = chunks
        if not chunks:
            self._bm25 = None
            return
        from rank_bm25 import BM25Okapi

        self._bm25 = BM25Okapi([_tokenize(c.content) for c in chunks])

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        if self._bm25 is None or not self._chunks:
            return []
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(
            zip(self._chunks, scores, strict=True), key=lambda pair: pair[1], reverse=True
        )
        return [
            RetrievedChunk(chunk=chunk, score=float(score), retrieval_method="bm25")
            for chunk, score in ranked[:top_k]
            if score > 0
        ]
