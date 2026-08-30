"""Document ingestion: parse -> hash -> dedup, before chunking/embedding/storage.

Real Phase 2 implementation — `.txt`/`.md` natively, `.pdf` via the lazily-imported `pypdf`
package (the `rag` extra). SQLite-backed (`RagRepository`) for document/chunk persistence, dedup
lookups, and rebuilding the BM25 corpus across process restarts.
"""
