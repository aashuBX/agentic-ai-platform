"""Chunking strategy interface + seven implementations + `ChunkingFactory`.

Every strategy is a real, working implementation with documented simplifications where they exist
(see each module's docstring) — none are fake stubs. `recursive` is the default.
"""

from app.rag.chunking.base import ChunkingStrategy
from app.rag.chunking.factory import STRATEGY_NAMES, ChunkingFactory, UnknownChunkingStrategyError

__all__ = ["STRATEGY_NAMES", "ChunkingFactory", "ChunkingStrategy", "UnknownChunkingStrategyError"]
