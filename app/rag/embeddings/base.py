"""EmbeddingProvider interface (requirement.md EMBEDDINGS section)."""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Turns text into vectors. `dimension` must be set by `__init__` before first use."""

    name: str
    dimension: int

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts. Returns one vector per input text, in the same order."""

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
