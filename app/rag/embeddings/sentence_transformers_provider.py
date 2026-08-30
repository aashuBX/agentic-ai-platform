"""Local embedding provider using `sentence-transformers` — the default, no API key required.

The model is downloaded once from Hugging Face on first use and cached under `~/.cache/huggingface`
(standard `sentence-transformers` behavior). Verified against sentence-transformers==3.0.1 /
transformers==4.41.2 in this repo's dev environment — see the base `dependencies` comment in
pyproject.toml for why those exact versions are pinned.

Loading the model (even from local disk cache) is slow on CPU — tens of seconds on the machine
this was developed on — while running it is fast. `_MODEL_CACHE` keeps one loaded model per
process keyed by name, so constructing this provider more than once (the test suite does, and a
production process restarting workers might too) doesn't pay that cost again.
"""

from app.rag.embeddings.base import EmbeddingProvider

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_MODEL_CACHE: dict[str, object] = {}


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):
    name = "sentence_transformers"

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                '"sentence-transformers" is a base dependency — pip install -e . to reinstall it'
            ) from exc

        if model_name not in _MODEL_CACHE:
            _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
        self._model = _MODEL_CACHE[model_name]
        self.dimension = self._model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = self._model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return vectors.tolist()
