"""SQLite-backed persistence for ingested documents and chunks.

Deliberately plain `sqlite3` rather than SQLAlchemy: the schema is two simple tables with one
foreign key, and stdlib `sqlite3` keeps this dependency-free (Rule 8: minimal dependencies).
SQLAlchemy would be a reasonable choice if this schema grows more relational.

Two responsibilities: (1) dedup lookups by content hash, (2) the durable copy of every chunk's
text/metadata, which is what lets the BM25 index (in-memory, not persistent on its own) be rebuilt
after a process restart — see `app.rag.retrieval.bm25.BM25Retriever.index`.
"""

import json
import sqlite3
from pathlib import Path

from app.models.rag import Chunk, Document

_MEMORY_URL = "sqlite:///:memory:"


def _sqlite_target(database_url: str) -> str:
    prefix = "sqlite:///"
    if not database_url.startswith(prefix):
        raise ValueError(f"Only sqlite:/// URLs are supported here, got: {database_url!r}")
    if database_url == _MEMORY_URL:
        return ":memory:"
    path = Path(database_url[len(prefix) :])
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


class RagRepository:
    """Owns the `documents` and `chunks` tables used by the ingestion/retrieval pipeline."""

    def __init__(self, database_url: str) -> None:
        self._conn = sqlite3.connect(_sqlite_target(database_url), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL UNIQUE,
                metadata TEXT NOT NULL
            )
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL REFERENCES documents(id),
                content TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                strategy TEXT NOT NULL,
                parent_chunk_id TEXT,
                metadata TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def find_document_by_hash(self, content_hash: str) -> Document | None:
        row = self._conn.execute(
            "SELECT * FROM documents WHERE content_hash = ?", (content_hash,)
        ).fetchone()
        return self._row_to_document(row) if row else None

    def save_document(self, document: Document) -> None:
        self._conn.execute(
            "INSERT INTO documents (id, source, title, content, content_hash, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                document.id,
                document.source,
                document.title,
                document.content,
                document.content_hash,
                json.dumps(document.metadata),
            ),
        )
        self._conn.commit()

    def save_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        self._conn.executemany(
            "INSERT INTO chunks "
            "(id, document_id, content, chunk_index, strategy, parent_chunk_id, metadata) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    c.id,
                    c.document_id,
                    c.content,
                    c.chunk_index,
                    c.strategy,
                    c.parent_chunk_id,
                    json.dumps(c.metadata),
                )
                for c in chunks
            ],
        )
        self._conn.commit()

    def all_chunks(self) -> list[Chunk]:
        rows = self._conn.execute(
            "SELECT * FROM chunks ORDER BY document_id, chunk_index"
        ).fetchall()
        return [self._row_to_chunk(row) for row in rows]

    def chunks_for_document(self, document_id: str) -> list[Chunk]:
        rows = self._conn.execute(
            "SELECT * FROM chunks WHERE document_id = ? ORDER BY chunk_index", (document_id,)
        ).fetchall()
        return [self._row_to_chunk(row) for row in rows]

    def get_chunk(self, chunk_id: str) -> Chunk | None:
        row = self._conn.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,)).fetchone()
        return self._row_to_chunk(row) if row else None

    def document_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]

    def chunk_count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _row_to_document(row: sqlite3.Row) -> Document:
        return Document(
            id=row["id"],
            source=row["source"],
            title=row["title"],
            content=row["content"],
            content_hash=row["content_hash"],
            metadata=json.loads(row["metadata"]),
        )

    @staticmethod
    def _row_to_chunk(row: sqlite3.Row) -> Chunk:
        return Chunk(
            id=row["id"],
            document_id=row["document_id"],
            content=row["content"],
            chunk_index=row["chunk_index"],
            strategy=row["strategy"],
            parent_chunk_id=row["parent_chunk_id"],
            metadata=json.loads(row["metadata"]),
        )
