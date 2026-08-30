"""OpenAI embeddings adapter — optional, needs the `openai` extra and `LLM__OPENAI_API_KEY`.

Verified against openai==3.5.0's `embeddings.create` interface in this repo's dev environment.
"""

from app.llm.exceptions import ProviderNotConfiguredError
from app.rag.embeddings.base import EmbeddingProvider

DEFAULT_MODEL = "text-embedding-3-small"
_DEFAULT_DIMENSION = 1536


class OpenAIEmbeddingProvider(EmbeddingProvider):
    name = "openai"

    def __init__(self, api_key: str | None, model: str = DEFAULT_MODEL) -> None:
        if not api_key:
            raise ProviderNotConfiguredError(
                "OpenAI embeddings require LLM__OPENAI_API_KEY to be set in your environment/.env."
            )
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ProviderNotConfiguredError(
                'The "openai" package is not installed. Run: pip install -e ".[openai]"'
            ) from exc
        self._client = OpenAI(api_key=api_key)
        self._model = model
        self.dimension = _DEFAULT_DIMENSION

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model=self._model, input=texts)
        return [item.embedding for item in response.data]
