# PLAN.md — Enterprise Conversational Agentic AI Platform

Status: living document, updated as phases complete.
Source spec: `requirement.md` (kept in repo root as the authoritative brief).

## 0. Repository inspection (Phase 0)

- Repo contained only `README.md` (aspirational architecture doc, no code), `LICENSE`, `.gitignore`
  (standard GitHub Python template, `.env`/`.venv` already excluded), and `requirement.md`.
- Two commits on `main`: `ac43c40` (license/gitignore), `bbbeaed` (README). No app code to collide with.
- System Python via pyenv defaults to 3.7.8 (too old). `pyenv` has 3.11.1, 3.11.7, 3.12.10 installed.
  → Project pinned to **3.11.7** via `.python-version`; venv created at `.venv/`.
- Docker 27.1.1 / Compose v2.29.1 available locally for Phase 11.
- No poetry/uv on PATH → using `pyproject.toml` + stdlib `venv` + `pip` (simplest, fewest moving parts,
  matches "keep the application runnable with minimal dependencies").

## 1. Guiding decisions

- **One package root**: `app/`, matching the spec's CODE ORGANIZATION section, installed editable
  (`pip install -e .`) so `python -m app...` and `uvicorn app.api.main:app` both work without path hacks.
- **Dependency layering**: base `dependencies` cover everything needed for the DEFAULT config to
  actually work end to end — FastAPI/Pydantic/LangGraph/LangChain-core, plus (as of Phase 2) the
  local RAG stack (Chroma, BM25, sentence-transformers) since "local vector store" is one of
  requirement.md's LOCAL DEFAULTS, not an opt-in extra, and there's no honest "mock" substitute for
  semantic search the way `LLM__PROVIDER=mock` substitutes for a real model. Everything that DOES
  have a real local/mock alternative and only helps if you opt in — OpenAI/Anthropic/Gemini/Groq
  SDKs, FAISS, Pinecone, and (from later phases) the Neo4j driver, Redis client, RabbitMQ/Celery,
  ElevenLabs — is an **optional extra** (`pip install -e ".[openai]"`, `.[faiss]"`, etc.), imported
  lazily inside the adapter that needs it. Missing an extra never breaks app startup for the default
  config — it only disables that specific adapter, with a clear error if selected via config.
  This directly implements RULE 1 / RULE 8 / the "LOCAL DEFAULTS" section: nothing *external*
  (a paid API, a running service) is ever required to boot the app, run the graph, or pass the test
  suite — only local, free, offline Python packages are, and only the ones the default config uses.
- **Mock-first providers**: every external integration (LLM, vector store, graph DB, cache, queue, voice)
  ships a working local/mock implementation selected by default via `.env` config, plus a real adapter
  behind the same interface. Switching is a config value, never a code change (Rule 4: interfaces/adapters).
- **Structured state**: LangGraph state is a `TypedDict` (`ConversationState`) — the field list matches the
  spec's LANGGRAPH section verbatim. Individual values inside it (messages, intent, guardrail results) are
  Pydantic models so validation still happens everywhere it matters, without fighting LangGraph's reducer
  model (which is built around TypedDict/dataclass state, not deeply-nested Pydantic mutation).
- **Honesty about phase boundaries**: where a routed intent points at an agent that doesn't exist yet in
  the current phase (GraphRAG, Feedback, Voice-from-chat), the router sends it to an explicit
  "not implemented yet" leaf node rather than silently mishandling it or faking a real answer. This node
  disappears/gets replaced as each phase lands — never a placeholder pretending to be real.
- **No empty scaffolding**: sub-packages listed in the spec's CODE ORGANIZATION (e.g. `app/mcp/`,
  `app/graph_rag/`, `app/voice/`, `app/channels/`, `app/memory/`) are created in the phase that actually
  implements them, not upfront as empty stubs. PLAN.md and the README track what's pending instead.

## 2. Phase roadmap (mirrors requirement.md's PHASE 0–12)

| Phase | Scope | Status |
|---|---|---|
| 0 | Repo inspection, environment, this PLAN.md | ✅ done |
| 1 | Config, schemas, BaseAgent, ConversationState, input/output guardrails, Intent Agent, Router, FAQ Agent, RAG Agent skeleton, CRM Agent skeleton, Handoff Agent, LangGraph workflow, FastAPI health/chat, tests | ✅ done — 50 tests passing, ruff clean |
| 2 | Real RAG: parser/hash/dedup, all 7 chunking strategies, embeddings+cache, Chroma+FAISS+Pinecone stores, BM25, hybrid+RRF, cross-encoder+LLM reranking, query rewriting, Self-RAG, CRAG, RAG Agent upgraded, `/documents/upload` + `/knowledge/search` | ✅ done — 119 tests passing, ruff clean |
| 3 | GraphRAG: entity/relationship extraction, graph builder, Neo4j adapter (+ in-memory fallback), graph retriever, context formatter, GraphRAG Agent, synthetic CRM graph domain | ✅ done — 148 passed / 5 skipped (Neo4j-optional), ruff clean |
| 4 | MCP: FastMCP server + client, customer/lead/appointment/knowledge tools, mock CRM store, CRM Agent wired to MCP, tool-call error handling | ⬜ planned |
| 5 | Memory: Redis adapter + local fallback, LangGraph checkpointer swap, conversation summaries | ⬜ planned |
| 6 | Guardrails+reliability: semantic grounding, claim decomposition/validation, LLM-judge, regeneration loop | ⬜ planned |
| 7 | Evaluation: scenario schema/generator/runner/run-all, RAGAS integration | ⬜ planned |
| 8 | Observability: structured events, trace IDs end-to-end, LangSmith adapter, Langfuse adapter | ⬜ planned |
| 9 | Voice AI: STT/TTS/Voice provider abstractions, settings, pronunciation, silence FSM, voicemail, translator/sales agents, demo mode | ⬜ planned |
| 10 | Multi-channel: message envelope, Web/SMS/WhatsApp/Voice channel adapters | ⬜ planned |
| 11 | Docker/Compose, worker process, CI-ready structure | ⬜ planned |
| 12 | Docs/demo: demo data, scripts, Mermaid diagrams, README pass, troubleshooting | ⬜ planned |

This is a multi-session build. Each row's status is updated in place only after that phase's code is
written, tested, and passing — never in advance. See README "Implementation Status" for the feature-level
`[x]`/`[ ]` breakdown, which is the source of truth over this table.

## 3. Phase 1 detail (this pass)

Directory additions:

```
app/
  config/settings.py            pydantic-settings, nested by category (LLM/RAG/VECTOR_STORE/NEO4J/
                                 REDIS/RABBITMQ/MCP/VOICE/LANGSMITH/LANGFUSE/EVALUATION)
  models/                       enums, ChatMessage/ChatRequest/ChatResponse, IntentClassification,
                                 GuardrailCheckResult, AgentConfig
  observability/                logging setup, AgentEvent + EventSink interface (LoggingEventSink only
                                 for now; LangSmith/Langfuse sinks land in Phase 8)
  llm/                          LLMProvider interface, generate()/generate_structured(), MockLLMProvider
                                 (heuristic, zero-dependency, deterministic — used as the default so the
                                 whole graph runs offline), OpenAI/Anthropic/Gemini/Groq adapters (lazy
                                 import, need extras + API key)
  agents/                       BaseAgent, IntentAgent, RouterAgent, FAQAgent, RAGAgent (skeleton —
                                 naive keyword retriever over demo/data/faqs.json), CRMAgent (skeleton —
                                 explicit "not wired to MCP yet" response), HandoffAgent
  guardrails/                   GuardrailCheck interface, input checks (empty/oversized/unsafe-pattern),
                                 output checks (non-empty/schema/prohibited-pattern), InputGuardrailAgent,
                                 OutputGuardrailAgent
  graph/                        ConversationState TypedDict, node functions, StateGraph wiring with
                                 conditional routing + MemorySaver checkpointer (thread_id = session_id)
  api/                          FastAPI app factory, GET /health, POST /chat, GET /agents, POST /agents/run
demo/data/faqs.json              synthetic FAQ knowledge base for the FAQ/RAG skeleton agents
tests/                           unit tests per module + one full-graph integration test
```

Explicitly deferred past Phase 1 (tracked, not hidden): real vector/BM25/hybrid retrieval, GraphRAG,
MCP tools, Redis-backed memory, semantic grounding/hallucination pipeline, scenario framework, LangSmith/
Langfuse, voice, multi-channel adapters, Docker. Each has its own phase above.

## 3b. Phase 2 detail

Directory additions: `app/rag/{ingestion,chunking,embeddings,stores,retrieval,reranking}/`,
`app/rag/pipeline.py` + `factory.py` + `seed.py`, `app/api/routes/{documents,knowledge}.py`,
`tests/rag/` (8 files), `tests/api/{test_documents,test_knowledge}.py`.

Notable decisions and problems hit (kept here since they're exactly the kind of thing "inspect the
environment, resolve conflicts" in requirement.md is asking for, and future-me will want the reasoning):

- **faiss-cpu wouldn't build from source** on this Intel Mac (missing SWIG headers for 1.12.0's
  bindings). Fix: `pip install --only-binary=:all: faiss-cpu` resolves to 1.10.0, which has a wheel.
  FAISS is still a fully-implemented adapter — just not the default (Chroma is), matching the
  spec's "ChromaDB and/or FAISS."
- **transformers 4.5x+ requires torch>=2.5, but PyPI has no torch wheel newer than 2.2.2 for this
  platform** (Intel macOS) — pinned `transformers==4.41.2` / `sentence-transformers==3.0.1` /
  `tokenizers==0.19.1` (versions contemporaneous with torch 2.2.x) in the `rag` extra instead of
  trying to force a torch upgrade that doesn't exist for this platform.
- **NumPy 2.x breaks torch 2.2.2's compiled C-extension ABI** (`RuntimeError: Numpy is not
  available` on the very first `.encode()` call — not just a warning). Pinned `numpy<2` in the
  `rag` extra to match what torch 2.2.2 was built against.
- **faiss + torch/sentence-transformers in the same process deadlocks** on this machine (each
  bundles its own OpenMP runtime). Fixed at `app/__init__.py` (before any submodule can import
  either library) with `KMP_DUPLICATE_LIB_OK=TRUE` / `OMP_NUM_THREADS=1` — a standard, documented
  workaround for this exact class of conflict, not a code bug on either side.
- **Model loads are slow on CPU** (~20s for the MiniLM embedding model on this hardware) even from
  local disk cache. Added a process-wide model cache (keyed by model name) inside
  `SentenceTransformerEmbeddingProvider`/`CrossEncoderReranker` so constructing either more than
  once per process — which the test suite does routinely — only pays that cost once.
- **Vector search always returns its nearest neighbors, even for an off-topic query** — there's no
  natural "no results" the way BM25-only or Phase 1's keyword matcher had. `RAGAgent` gates on a
  lexical-overlap relevance score (same heuristic CRAG uses for its quality check) before trusting
  retrieved context, rather than presenting a confidently-irrelevant top-1 hit as an answer.
- **RRF scores are tiny and scale-dependent** (~0.01–0.03 for two equally-weighted rankers at
  k=60) — CRAG's "is retrieval poor?" check deliberately does NOT compare a raw retrieval score to
  an absolute threshold (it would either never fire or always fire depending on which retriever
  backs it). It uses the same scale-independent lexical-overlap heuristic instead.

## 3c. Phase 3 detail

Directory additions: `app/graph_rag/{entities,relationships,builder,repository,memory_repository,
neo4j_repository,retriever,context_formatter,factory,seed}.py`, `app/agents/graph_rag_agent.py`,
`demo/data/relationships.json`, `tests/graph_rag/` (6 files), `tests/agents/test_graph_rag_agent.py`.

- **Synthetic domain**: 5 fictional customers (John Doe, Jane Smith, Priya Patel, Carlos Mendes,
  Aisha Khan), each with an Account, Order, assigned Agent (2 agents total, shared across
  customers), and a booked Appointment — matches requirement.md's `Customer -> owns -> Account
  -> created -> Order -> assigned_to -> Agent -> booked -> Appointment` example. Structured as
  `demo/data/relationships.json`; `seed.py` converts each record into narrative sentences and runs
  them through the real extraction pipeline (not hand-built graph nodes) so extraction is actually
  exercised, not bypassed.
- **Extraction is regex-based by default, LLM-based with a real provider**: `RegexEntityExtractor`/
  `RegexRelationshipExtractor` are correct for this repo's fixed sentence templates (verified: 5
  entities + 5 relationships extracted per customer record, zero false positives on unrelated
  text) but explicitly NOT general-purpose NER/RE — documented in both modules' docstrings.
  `LLMEntityExtractor`/`LLMRelationshipExtractor` use `generate_structured` against a real
  provider; under the mock provider they fall back to the regex extractors rather than trusting
  the mock's generic placeholder text as if it were real extraction.
- **Neo4j adapter verified live**, not just implemented-against-the-SDK-docs like Pinecone: ran a
  temporary `neo4j:5` Docker container (`docker run -d --rm --name neo4j-test -p 7687:7687 -e
  NEO4J_AUTH=neo4j/testpassword neo4j:5`) and executed `tests/graph_rag/test_neo4j_repository.py`
  against it — upsert/get/find-by-name/traversal/counts and the unsafe-relationship-type rejection
  all passed for real. That test file auto-skips when no Neo4j is reachable (checked via
  `driver.verify_connectivity()`), so it's not part of the required suite, but it's a real,
  passing integration test, not just aspirational code.
- **Dynamic Cypher relationship types**: Cypher has no parameter syntax for relationship *types*
  (only property values), so `Neo4jGraphRepository` interpolates the type name into the query
  string — validated against a strict `^[A-Z_]+$` allowlist first (`_require_safe_relationship_type`),
  since these values, while always internally-generated today, are exactly the kind of thing that
  becomes a Cypher-injection vector if that ever changes.
- **Router change**: `GRAPH_QUERY` now maps to `graph_rag_agent` instead of `not_implemented` in
  `ROUTE_MAP` — the first `not_implemented` mapping to actually get replaced, exactly the "seam"
  PLAN.md §1 described. `FEEDBACK`/`VOICE_TASK` still route there, honestly, until their phases land.

## 4. Working agreement for this session

- Never invent that an unconfigured provider is live; default config always resolves to a working
  local/mock path.
- Run tests + lint after every phase; fix failures before moving on; do not mark a checkbox `[x]` in the
  README until the code behind it actually runs.
- No commits/pushes unless explicitly requested.
