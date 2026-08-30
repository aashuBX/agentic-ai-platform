"""Naive keyword-matching retriever — the Phase 1 RAG skeleton.

No chunking, embeddings, or vector index: score = fraction of query terms found in the item's
title/content/tags. This is intentionally simple (documented per requirement.md's instruction to
flag simplifications rather than pretend a skeleton is the real pipeline) and is replaced by the
hybrid vector+BM25+RRF+reranking pipeline in Phase 2.
"""

import json
from dataclasses import dataclass
from pathlib import Path

_STOPWORDS = frozenset(
    "the a an is are was were do does did how what when where why who which "
    "i you he she it we they my your our their this that to of in on for and or".split()
)


@dataclass(frozen=True)
class KnowledgeItem:
    id: str
    title: str
    content: str
    tags: tuple[str, ...] = ()


def load_knowledge_items(path: str | Path) -> list[KnowledgeItem]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return [
        KnowledgeItem(
            id=entry["id"],
            title=entry["title"],
            content=entry["content"],
            tags=tuple(entry.get("tags", [])),
        )
        for entry in raw
    ]


def keyword_search(
    query: str, items: list[KnowledgeItem], top_k: int = 1
) -> list[tuple[KnowledgeItem, float]]:
    """Score each item by the fraction of (non-stopword) query terms it contains."""

    query_terms = {t for t in query.lower().split() if len(t) > 2 and t not in _STOPWORDS}
    if not query_terms:
        return []

    scored: list[tuple[KnowledgeItem, float]] = []
    for item in items:
        haystack = f"{item.title} {item.content} {' '.join(item.tags)}".lower()
        hits = sum(1 for term in query_terms if term in haystack)
        if hits:
            scored.append((item, hits / len(query_terms)))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]
