"""GraphRAG layer (Phase 3) — a genuine knowledge-graph pipeline over a synthetic CRM domain:

    DOCUMENT -> ENTITY EXTRACTION -> RELATIONSHIP EXTRACTION -> GRAPH BUILDER -> NEO4J
        -> GRAPH RETRIEVAL -> GRAPHRAG AGENT -> LLM

`entities.py`/`relationships.py` extract from text (regex-based for this repo's fixed synthetic
sentence templates, LLM-based for arbitrary text with a real provider configured). `builder.py`
wires extraction to storage. `repository.py` is the storage interface, with `Neo4jGraphRepository`
(real, needs `NEO4J__ENABLED=true` + a reachable server) and `InMemoryGraphRepository` (default
fallback) behind it. `retriever.py` + `context_formatter.py` turn a natural-language query into
graph-traversal results and back into text. `seed.py` loads `demo/data/relationships.json`.
"""
