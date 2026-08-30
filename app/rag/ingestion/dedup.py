"""Duplicate detection: SHA-256 content-hash lookup against already-ingested documents.

Kept as its own explicit component (rather than folded into the repository) because
requirement.md's ADVANCED RAG pipeline diagram calls out `HASH -> DEDUPLICATION` as its own stage.
"""

from dataclasses import dataclass

from app.models.rag import Document
from app.rag.ingestion.repository import RagRepository


@dataclass(frozen=True)
class DedupResult:
    is_duplicate: bool
    existing_document: Document | None


class Deduplicator:
    def __init__(self, repository: RagRepository) -> None:
        self._repository = repository

    def check(self, document: Document) -> DedupResult:
        existing = self._repository.find_document_by_hash(document.content_hash)
        return DedupResult(is_duplicate=existing is not None, existing_document=existing)
