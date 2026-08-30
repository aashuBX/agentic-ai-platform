"""Cross-encoder reranker using `sentence-transformers.CrossEncoder` — local, no API key.

Verified against sentence-transformers==3.0.1's `CrossEncoder.predict` in this repo's dev
environment. Cross-encoders score a (query, passage) pair jointly (unlike the bi-encoder used for
embeddings), which is typically far more accurate for reranking a short candidate list — the
standard reason to have a separate reranking stage at all.

`_MODEL_CACHE` avoids reloading the model (slow on CPU) if this class is constructed more than
once per process — see the same pattern/rationale in `sentence_transformers_provider.py`.
"""

from app.models.rag import RetrievedChunk
from app.rag.reranking.base import Reranker

DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_MODEL_CACHE: dict[str, object] = {}


class CrossEncoderReranker(Reranker):
    name = "cross_encoder"

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as exc:
            raise ImportError(
                '"sentence-transformers" is a base dependency — pip install -e . to reinstall it'
            ) from exc

        if model_name not in _MODEL_CACHE:
            _MODEL_CACHE[model_name] = CrossEncoder(model_name)
        self._model = _MODEL_CACHE[model_name]

    def rerank(
        self, query: str, candidates: list[RetrievedChunk], top_k: int
    ) -> list[RetrievedChunk]:
        if not candidates:
            return []
        pairs = [(query, c.chunk.content) for c in candidates]
        scores = self._model.predict(pairs)
        rescored = [
            RetrievedChunk(
                chunk=c.chunk, score=float(score), retrieval_method="reranked_cross_encoder"
            )
            for c, score in zip(candidates, scores, strict=True)
        ]
        rescored.sort(key=lambda r: r.score, reverse=True)
        return rescored[:top_k]
