"""Formats `GraphPath` retrieval results into LLM-consumable context text (the "GRAPH CONTEXT
FORMATTER" requirement.md's GraphRAG implementation list asks for)."""

from app.models.graph_rag import GraphPath


class GraphContextFormatter:
    def format(self, paths: list[GraphPath]) -> str:
        if not paths:
            return ""
        # Longer paths carry more specific, multi-hop information — surface those first, and
        # de-duplicate identical descriptions (a single-hop path is often a prefix of a longer one).
        descriptions = sorted({path.describe() for path in paths}, key=len, reverse=True)
        return "\n".join(descriptions)
