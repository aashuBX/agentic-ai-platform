"""ChunkingFactory: builds a configured `ChunkingStrategy` by name (`RAG__CHUNKING_STRATEGY`).

`recursive` is the default and needs neither an LLM nor an embedding provider. `proposition` and
`agentic` need an LLM; `semantic` needs an embedding provider — both are passed in explicitly
rather than the factory reaching for a global, keeping this easy to unit test.
"""

from app.llm.base import LLMProvider
from app.rag.chunking.agentic import AgenticChunkingStrategy
from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.document_aware import DocumentAwareChunkingStrategy
from app.rag.chunking.hierarchical import HierarchicalChunkingStrategy
from app.rag.chunking.late import LateChunkingStrategy
from app.rag.chunking.proposition import PropositionChunkingStrategy
from app.rag.chunking.recursive import RecursiveChunkingStrategy
from app.rag.chunking.semantic import SemanticChunkingStrategy
from app.rag.embeddings.base import EmbeddingProvider

STRATEGY_NAMES: tuple[str, ...] = (
    "recursive",
    "semantic",
    "document_aware",
    "proposition",
    "late",
    "hierarchical",
    "agentic",
)


class UnknownChunkingStrategyError(ValueError):
    pass


class ChunkingFactory:
    @classmethod
    def create(
        cls,
        strategy_name: str,
        *,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        llm: LLMProvider | None = None,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> ChunkingStrategy:
        name = strategy_name.strip().lower()

        if name == "recursive":
            return RecursiveChunkingStrategy(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if name == "document_aware":
            return DocumentAwareChunkingStrategy(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if name == "late":
            return LateChunkingStrategy(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if name == "hierarchical":
            # The child splitter's overlap must stay smaller than its own chunk size — cap it
            # relative to `chunk_size` rather than passing `chunk_overlap` through unchecked,
            # since a small `chunk_size` (as child_chunk_size) with the default 100-char overlap
            # would otherwise violate RecursiveChunkingStrategy's own invariant.
            safe_child_overlap = min(chunk_overlap, max(chunk_size // 4, 1))
            return HierarchicalChunkingStrategy(
                parent_chunk_size=max(chunk_size * 2, chunk_size + 1),
                child_chunk_size=chunk_size,
                chunk_overlap=safe_child_overlap,
            )
        if name == "proposition":
            if llm is None:
                raise ValueError("proposition chunking requires an llm provider")
            return PropositionChunkingStrategy(llm=llm)
        if name == "agentic":
            if llm is None:
                raise ValueError("agentic chunking requires an llm provider")
            return AgenticChunkingStrategy(llm=llm, max_chunk_chars=chunk_size)
        if name == "semantic":
            if embedding_provider is None:
                raise ValueError("semantic chunking requires an embedding provider")
            return SemanticChunkingStrategy(
                embedding_provider=embedding_provider, max_chunk_chars=chunk_size
            )

        raise UnknownChunkingStrategyError(
            f"Unknown chunking_strategy={strategy_name!r}. Expected one of: {STRATEGY_NAMES}"
        )
