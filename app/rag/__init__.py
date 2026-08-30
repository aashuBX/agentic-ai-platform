"""RAG / Knowledge layer — the real pipeline (Phase 2).

    DOCUMENT -> PARSER -> HASH -> DEDUPLICATION -> CHUNKING -> EMBEDDING -> VECTOR STORE
    QUERY -> QUERY REWRITER -> {VECTOR SEARCH, BM25 SEARCH} -> RRF -> RERANKER -> CONTEXT

Subpackages: `ingestion/` (parse/hash/dedup + SQLite repository), `chunking/` (7 strategies +
factory), `embeddings/` (provider interface + cache + sentence-transformers/openai adapters),
`stores/` (Chroma default, FAISS/Pinecone optional), `retrieval/` (vector, BM25, hybrid+RRF, query
rewriting, Self-RAG, CRAG), `reranking/` (cross-encoder, LLM). `pipeline.py`/`factory.py` wire it
all together as `RAGPipeline`, used by `RAGAgent`.

`keyword_search.py` is intentionally kept, separately, for `FAQAgent`'s exact-match lookup over a
small curated FAQ list — a different, simpler problem than RAG over longer documents, not
something that needs the full pipeline.
"""
