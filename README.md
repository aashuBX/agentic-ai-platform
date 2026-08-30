
# 🤖 Enterprise Conversational Agentic AI Platform

<p align="center">

### Production-Oriented GenAI • Agentic AI • Multi-Agent Systems • RAG • GraphRAG • MCP • Voice AI • LLMOps

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20Framework-1C3C3C?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-6B4FBB?style=for-the-badge)
![RAG](https://img.shields.io/badge/Advanced-RAG-0A7AFF?style=for-the-badge)
![Neo4j](https://img.shields.io/badge/Neo4j-GraphRAG-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Memory%20%26%20Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</p>

---

## ⚠️ Independent Portfolio Project — Public-Safe Disclaimer

This repository is an **independent, personal implementation** built to demonstrate AI/agentic-engineering
practices publicly. It is **not** my employer's product, is not affiliated with or endorsed by any employer,
and contains **no proprietary source code, internal APIs, confidential prompts, production credentials,
customer data, internal database schemas, private URLs, proprietary business logic, or company assets**.

Everything here is built independently, from scratch, against **open/public technologies**, using
**synthetic/mock data** (a fictional product called "NimbusDesk" and fictional people like "John Doe") and
**local development defaults**. No real metrics are fabricated — every number in this README is either a
measured result from this repository's own test suite, or explicitly marked as not-yet-measured.

## ✅ Implementation Status

This is a large spec (~90 capabilities across 12 build phases — see [`PLAN.md`](PLAN.md) for the phase
roadmap and [`requirement.md`](requirement.md) for the original brief). It is being built **progressively,
as a sequence of small working vertical slices**, not as 100 empty files. `[x]` below means the code exists,
runs, and is covered by a passing test — not "stubbed" or "planned." Everything else is `[ ]`.

**Phase 1 — Core Agent Runtime: complete.** See [Test Results](#-testing) for the current pass count.

<details open>
<summary><strong>Conversational core & orchestration</strong></summary>

- [x] Conversational AI (`POST /chat`, web channel)
- [x] Chat agents (FAQ, RAG skeleton, CRM skeleton, Handoff)
- [x] Multi-agent orchestration (`BaseAgent` + `AgentRegistry`)
- [x] LangGraph (compiled `StateGraph`, conditional routing, checkpointing)
- [x] Intent detection (structured output, keyword-heuristic under the mock provider)
- [x] Agent routing (deterministic intent → agent table, `RouterAgent`)
- [x] FAQ agent
- [x] RAG agent *(Phase 2: real hybrid retrieval pipeline — see [RAG](#-rag))*
- [x] GraphRAG agent *(Phase 3: real relationship-aware retrieval — see [GraphRAG](#-graphrag--knowledge-graph))*
- [x] CRM agent *(Phase 1 skeleton: not yet wired to MCP — see [MCP](#-mcp))*
- [ ] Feedback agent
- [x] Handoff agent
- [x] Agent Configuration (`AgentConfig` Pydantic model, per-agent `default_config()`)
- [x] Structured outputs (Pydantic everywhere; `IntentClassification` is the live Phase 1 example)
- [ ] Human-in-the-loop approval points

</details>

<details>
<summary><strong>MCP & tool calling</strong></summary>

- [ ] MCP client *(Phase 4)*
- [ ] MCP server / FastMCP *(Phase 4)*
- [ ] Tool calling / structured tool selection *(Phase 4)*
- [ ] Customer / Lead / Appointment / Knowledge tools *(Phase 4)*

</details>

<details>
<summary><strong>RAG & knowledge</strong></summary>

- [x] Document ingestion: parser (.txt/.md/.pdf), SHA-256 hashing, dedup, SQLite repository
- [x] All 7 chunking strategies (recursive, semantic, document-aware, proposition, late,
      hierarchical, agentic) behind one `ChunkingStrategy` interface + `ChunkingFactory`
- [x] Embeddings (`sentence-transformers` local default, OpenAI optional) + embedding cache
      (in-memory default, SQLite-persistent option)
- [x] Vector store: Chroma (default), FAISS (optional extra), Pinecone (optional, unverified live)
- [x] BM25 retrieval, hybrid retrieval, Reciprocal Rank Fusion (weighted, standard k=60 formula)
- [x] Cross-encoder reranking (local model), LLM reranking abstraction
- [x] Query rewriting *(documented no-op under the mock provider)*
- [x] Self-RAG, Corrective RAG / CRAG *(both simplified — see [RAG](#-rag) for exactly what)*
- [x] `POST /documents/upload`, `POST /knowledge/search`
- [x] Example datasets (`demo/data/faqs.json`, `demo/data/knowledge_documents.json`)

</details>

<details>
<summary><strong>GraphRAG</strong></summary>

- [x] Entity extraction, relationship extraction (regex-based for this repo's synthetic domain,
      LLM-based for arbitrary text with a real provider configured)
- [x] Graph builder, graph repository interface
- [x] Neo4j adapter — verified against a real, temporary Neo4j container during development (not
      just implemented-against-the-docs), with an in-memory fallback when disabled/unreachable
- [x] Graph retriever + context formatter (relationship-aware, multi-hop retrieval)
- [x] Synthetic CRM graph domain (`demo/data/relationships.json`): Customer → owns → Account,
      → created → Order, → assigned_to → Agent, → booked → Appointment → with → Agent

</details>

<details>
<summary><strong>Memory</strong></summary>

- [x] Short-term conversation memory *(LangGraph `MemorySaver` checkpointer, keyed by session — messages
      genuinely accumulate turn-to-turn; see `tests/graph/test_workflow.py`)*
- [ ] Cross-session memory, Redis-backed persistence, conversation summaries *(Phase 5)*

</details>

<details>
<summary><strong>Guardrails & reliability</strong></summary>

- [x] Input guardrail (empty / oversized / unsafe-pattern checks)
- [x] Output guardrail (schema / non-empty / prohibited-pattern checks)
- [ ] Semantic grounding, claim decomposition/validation, LLM-as-a-Judge, hallucination regeneration loop
      *(Phase 6)*

</details>

<details>
<summary><strong>Evaluation</strong></summary>

- [x] Tests (pytest: unit + integration — see [Testing](#-testing))
- [ ] Scenario framework (schema, generator, runner, run-all, success criteria) *(Phase 7)*
- [ ] RAGAS evaluation *(Phase 7)*

</details>

<details>
<summary><strong>Observability</strong></summary>

- [x] Structured JSON logging, trace IDs, agent execution events (`EventBus`)
- [ ] LangSmith integration, Langfuse integration *(Phase 8)*

</details>

<details>
<summary><strong>LLM abstraction</strong></summary>

- [x] Multi-provider `LLMProvider` interface (`generate` + `generate_structured`)
- [x] Mock provider (heuristic, zero-dependency, default — powers every test and the default local run)
- [x] OpenAI / Anthropic / Gemini / Groq adapters implemented *(need their SDK extra + a real API key to
      actually call out — see [Configuration](#-configuration))*

</details>

<details>
<summary><strong>Voice AI</strong></summary>

- [ ] STT/TTS/Voice provider abstractions, settings, pronunciation, silence handling, voicemail, human
      transfer (voice), recording disclosure, live-test interface, translator/sales agents *(Phase 9)*
- [x] Human transfer *(chat channel only, via `HandoffAgent`; voice-specific transfer is Phase 9)*

</details>

<details>
<summary><strong>Multi-channel</strong></summary>

- [x] Web chat channel (`channel: "web"` on `POST /chat`)
- [ ] SMS-style / WhatsApp-style channel adapters, common message envelope *(Phase 10)*

</details>

<details>
<summary><strong>Infrastructure & docs</strong></summary>

- [x] FastAPI API layer (`/health`, `/chat`, `/agents`, `/agents/run`)
- [x] pyproject.toml dependency management, `.env.example`, reproducible local setup
- [ ] Docker / Docker Compose *(Phase 11)*
- [ ] CI/CD pipeline config *(not started — project structure is CI-friendly, but no workflow file exists yet)*
- [x] `PLAN.md` phase roadmap
- [ ] Mermaid architecture diagrams under `docs/architecture/` *(Phase 12)*
- [ ] Dedicated demo UI / screenshots *(Swagger UI at `/docs` is the current demo surface)*

</details>

## 🚀 Quick Start

Requires **Python 3.11+**. No external services, Docker, or API keys are required for this to run —
but the base install does pull in a local embeddings/reranking stack (torch + transformers +
sentence-transformers + chromadb, ~1-2GB) since real local semantic search is one of this repo's
"local defaults," not an opt-in extra. See [RAG](#-rag) and [Limitations](#-limitations) for why.

```bash
git clone <this-repo-url>
cd agentic-ai-platform

python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
cp .env.example .env               # defaults are all mock/local — no editing required to run

# Run the API
uvicorn app.api.main:app --reload
# -> http://127.0.0.1:8000/docs for interactive Swagger UI
# First startup downloads two small local models from Hugging Face (~100MB, one-time, cached
# under ~/.cache/huggingface): the embedding model always, the reranker only if RAG__RERANKER=cross_encoder.
```

Try it:

```bash
curl -s http://127.0.0.1:8000/health | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo-1", "message": "What are your business hours?", "channel": "web"}' \
  | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo-1", "message": "Find John'"'"'s lead and mark it as qualified."}' \
  | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo-1", "message": "What are the API rate limits?"}' \
  | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8000/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "data retention policy", "top_k": 3}' \
  | python3 -m json.tool

curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "demo-1", "message": "Who is the agent assigned to John Doe?"}' \
  | python3 -m json.tool

echo "NimbusDesk supports two-factor authentication via TOTP apps or SMS codes." > /tmp/2fa-note.txt
curl -s -X POST http://127.0.0.1:8000/documents/upload -F "file=@/tmp/2fa-note.txt" | python3 -m json.tool

curl -s http://127.0.0.1:8000/agents | python3 -m json.tool
```

Run the tests:

```bash
pytest                # 148 passed + 5 optional-Neo4j skips, see Testing below
ruff check app tests  # lint
ruff format app tests # format
```

## 🎯 Project Overview

This repository is an **independent, public implementation of an enterprise-oriented Conversational Agentic AI platform**.

The platform demonstrates how modern Generative AI applications can combine:

- Multi-Agent orchestration
- LangGraph stateful workflows
- Intent detection and intelligent routing
- Chat-based AI agents
- Voice-based AI agents
- Advanced RAG, Self-RAG, Corrective RAG (CRAG)
- GraphRAG, hybrid retrieval (Vector + BM25 + Knowledge Graph)
- Reciprocal Rank Fusion (RRF), Cross-Encoder / LLM reranking
- MCP client/server architecture, AI tool calling, CRM-style automation
- Conversation memory, cross-session context
- Input / output guardrails, hallucination detection, semantic grounding, LLM-as-a-Judge
- Human-in-the-Loop workflows
- Intelligent document ingestion, multi-strategy chunking, embedding pipelines
- Vector databases, knowledge graphs
- Voice AI pipelines, Speech-to-Text / Text-to-Speech, voice provider abstraction & configuration
- Scenario-based agent testing, RAGAS evaluation, LangSmith / Langfuse observability
- Agent logs and execution traces
- Python backend services, Redis, RabbitMQ and Celery
- Docker and cloud-ready deployment

The goal is to demonstrate an AI system that can:

```text
Understand → Reason → Retrieve Knowledge → Select Agent → Select Tools
    → Execute Actions → Validate → Evaluate → Respond
```

## 🏗️ End-to-End Architecture

**Status:** the `Channel Adapter → Input Guardrail → Intent Agent → Agent Router → {FAQ, RAG, CRM,
Handoff} → Output Guardrail → Response` spine below is implemented and tested today for the web-chat
channel. GraphRAG/Feedback routes exist but currently return an explicit "not implemented yet" response
(see [Implementation Status](#-implementation-status)); SMS/WhatsApp/Voice channels are not implemented yet.

```text
                                      ┌──────────────────────┐
                                      │       USER            │
                                      │                        │
                                      │ Web / SMS / WhatsApp   │
                                      │        / Voice         │
                                      └──────────┬─────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  CHANNEL ADAPTERS     │
                                      │ Chat / Messaging      │
                                      │ Voice / WebSocket     │
                                      └──────────┬─────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │   INPUT GUARDRAIL     │
                                      └──────────┬─────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │    INTENT AGENT       │
                                      └──────────┬─────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │     AGENT ROUTER      │
                                      └──────────┬─────────────┘
                                                 │
             ┌───────────────────────────────────┼───────────────────────────────────┐
             │                                   │                                   │
             ▼                                   ▼                                   ▼
      ┌──────────────┐                    ┌──────────────┐                    ┌──────────────┐
      │   FAQ AGENT  │                    │   RAG AGENT  │                    │   CRM AGENT  │
      └──────┬───────┘                    └──────┬───────┘                    └──────┬───────┘
             │                                   │                                   │
             │                                   ▼                                   ▼
             │                           ┌──────────────┐                      ┌──────────────┐
             │                           │ RAG PIPELINE │                      │  MCP CLIENT  │
             │                           └──────┬───────┘                      └──────┬───────┘
             │                                  │                                     │
             │                    ┌─────────────┼─────────────┐                       ▼
             │                    ▼             ▼             ▼               ┌──────────────┐
             │                 Vector         BM25          Graph             │  MCP SERVER  │
             │                 Search        Search       Retrieval           └──────┬───────┘
             │                    │             │             │                       │
             │                    └─────────────┼─────────────┘                       │
             │                                  ▼                                     │
             │                                 RRF                                    │
             │                                  │                                     │
             │                             Reranking                                  │
             │                                  │                                     │
             └──────────────────────────────────┼─────────────────────────────────────┘
                                                 │
                                                 ▼
                                         ┌──────────────┐
                                         │     LLM      │
                                         └──────┬───────┘
                                                │
                                                ▼
                                      ┌──────────────────────┐
                                      │  OUTPUT GUARDRAIL     │
                                      └──────────┬─────────────┘
                                                 │
                                                 ▼
                                          FINAL RESPONSE
```

## 🤖 Agentic AI Layer

**Status:** `BaseAgent`, the LangGraph workflow, and the agents marked `[x]` above are implemented. ReAct,
Plan-and-Execute, hierarchical graphs, and inter-agent delegation beyond the current router are **design
targets documented in `app/graph/workflow.py`'s docstring, not implemented** — the graph is deliberately
built so those can be added as new nodes/edges later without a rewrite.

The platform uses specialized agents rather than relying on a single monolithic agent:

```text
Input Guardrail Agent  →  Validate / filter incoming request
Intent Agent            →  Understand and classify the request
Agent Router            →  Select specialized agent
FAQ Agent                →  Handle knowledge-oriented questions
RAG Agent                →  Retrieve grounded information
GraphRAG Agent           →  Handle relationship / multi-hop queries        [planned]
CRM Agent                →  Interact with business tools                  [skeleton]
Feedback Agent           →  Process feedback workflows                    [planned]
Handoff Agent            →  Transfer to human assistance
Output Guardrail         →  Validate final response
```

Core orchestration concepts covered by the brief: LangGraph, LangChain, multi-agent orchestration, intent
detection, agent routing, ReAct, Plan-and-Execute, hierarchical agent graphs, stateful agent workflows,
inter-agent delegation, human-in-the-loop, checkpointed execution. See
[Implementation Status](#-implementation-status) for exactly which of these exist today.

## 🔀 Intent Detection & Agent Routing

**Status: implemented.** Structured output (`IntentClassification`: `intent`, `confidence`, `reason`) via
`IntentAgent`, deterministic table-based routing via `RouterAgent`. Under the default mock LLM provider,
classification is a documented keyword heuristic (see `app/llm/providers/mock.py`); a real provider gets
genuine model-based classification through the same code path.

```text
USER REQUEST → Intent Detection → { FAQ | KNOWLEDGE_QUERY | GRAPH_QUERY | CRM_QUERY | CRM_UPDATE |
                                     APPOINTMENT_QUERY | FEEDBACK | HANDOFF | VOICE_TASK | UNKNOWN }
                                            │
                     ┌──────────────────────┼──────────────────────┬─────────────┐
                     ▼                      ▼                      ▼             ▼
                 FAQ Agent              RAG Agent              CRM Agent   Handoff Agent
```

## 🔎 RAG

**Status: implemented (Phase 2).** Real pipeline, not a keyword skeleton:

```text
DOCUMENT → PARSER (.txt/.md/.pdf) → SHA-256 HASH → DEDUP (SQLite) → CHUNKING → EMBEDDING → VECTOR STORE

                         USER QUERY
                              │
                              ▼
                       Query Rewriter (no-op under mock provider)
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
          Vector Search (Chroma)         BM25 Search (rank_bm25)
               │                             │
               └──────────────┬──────────────┘
                              ▼
                     Weighted Reciprocal Rank Fusion (k=60)
                              │
                              ▼
                Reranker (none by default | cross-encoder | LLM)
                              │
                              ▼
                         Top Context → LLM → Grounded Response
```

- **Chunking** (`app/rag/chunking/`): all 7 strategies from requirement.md share one
  `ChunkingStrategy.chunk(document)` interface via `ChunkingFactory` — `recursive` (the default,
  hand-rolled paragraph/sentence/word splitter with overlap), `document_aware` (splits on markdown
  headers), `hierarchical` (parent sections + linked child chunks), `semantic` (embedding-based
  breakpoint detection between sentences), `proposition` and `agentic` (LLM-driven — fall back to
  sentence-splitting/recursive under the mock provider, since asking a heuristic mock for semantic
  judgment would just be noise), and `late` (an approximation — see the module docstring for
  exactly how it differs from the published "late chunking" technique; token-level late interaction
  isn't achievable through this repo's sentence-level `EmbeddingProvider` interface).
- **Embeddings** (`app/rag/embeddings/`): `sentence-transformers/all-MiniLM-L6-v2` local default
  (no API key), OpenAI adapter optional. `CachedEmbeddingProvider` wraps either one with an
  in-memory or SQLite-persistent cache.
- **Vector stores** (`app/rag/stores/`): Chroma (default, local persistent), FAISS (optional
  extra), Pinecone (optional, implemented but not exercised against a live index — no key to test
  with).
- **Retrieval** (`app/rag/retrieval/`): vector + BM25 fused via weighted Reciprocal Rank Fusion
  (standard `1/(k+rank)` formula, `k=60`). `QueryRewriter` is a documented no-op under the mock
  provider. `SelfRAGStrategy` and `CRAGStrategy` are separate, explicitly-simplified strategy
  modules (not wired into the default `RAGAgent` flow) — see their docstrings for exactly what's
  approximated relative to the published techniques they're named after.
- **Reranking** (`app/rag/reranking/`): off by default (`RAG__RERANKER=none`); `cross_encoder`
  (local `cross-encoder/ms-marco-MiniLM-L-6-v2`) or `llm` (one relevance-scoring call per
  candidate; falls back to lexical overlap under the mock provider) are opt-in via config.
- **Relevance gating**: vector search always returns its nearest neighbors, even for an
  off-topic query — `RAGAgent` checks lexical overlap between the query and top hit before
  trusting it, rather than confidently answering from irrelevant context.

## 🕸️ GraphRAG & Knowledge Graph

**Status: implemented (Phase 3).** Real pipeline, real synthetic domain:

```text
DOCUMENT → ENTITY EXTRACTION → RELATIONSHIP EXTRACTION → GRAPH BUILDER → NEO4J (or in-memory fallback)
    → GRAPH RETRIEVAL → GRAPHRAG AGENT → LLM

Customer --OWNS--> Account          Customer --CREATED--> Order
Customer --ASSIGNED_TO--> Agent     Customer --BOOKED--> Appointment --WITH--> Agent
```

- **Extraction** (`app/graph_rag/entities.py` / `relationships.py`): regex-based by default —
  tailored to (and verified correct for) this repo's fixed synthetic sentence templates, honestly
  documented as not a general-purpose NER/RE system. With a real LLM provider configured,
  `LLMEntityExtractor`/`LLMRelationshipExtractor` extract from arbitrary text via structured
  output instead.
- **Storage**: `Neo4jGraphRepository` is optional (`NEO4J__ENABLED=true` + a reachable server) and
  was verified against a real, temporary Neo4j container during development — not just written
  against the driver docs. `InMemoryGraphRepository` (a real, working adjacency-list graph, not a
  stub) is the default, matching this repo's "local defaults" philosophy — GraphRAG does not
  require a running Neo4j instance to demo. A misconfigured/unreachable Neo4j falls back
  automatically and logs why, never crashing startup.
- **Retrieval** (`app/graph_rag/retriever.py`): finds entities named in the query and traverses up
  to 2 outgoing hops, genuinely demonstrating relationship-aware, multi-hop retrieval — e.g. "Who
  is the agent assigned to John Doe?" resolves via a direct `ASSIGNED_TO` edge *and* independently
  via `BOOKED → Appointment → WITH → Agent`, which a text-similarity search has no structural way
  to do.
- **Synthetic domain** (`demo/data/relationships.json`): 5 fictional customers, each with an
  Account, Order, assigned Agent, and booked Appointment — matches requirement.md's CRM DOMAIN and
  GraphRAG examples exactly, with zero real personal data.

## 🔌 MCP

**Status: not implemented — Phase 4.** MCP (Model Context Protocol) will be the tool-integration layer
between the CRM Agent and a safe, synthetic/mock CRM data source — never a real employer system.

```text
CRM Agent → MCP Client → MCP Server → { Customer tools | Lead tools | Appointment tools | Knowledge tools }
                                              │
                                              ▼
                                      Mock CRM / Local DB
```

Planned tools: `get_customer`, `search_customer`, `create_customer`, `update_customer`, `get_lead`,
`search_lead`, `create_lead`, `update_lead`, `get_appointment`, `search_appointment`,
`create_appointment`, `update_appointment`, `cancel_appointment`, `search_knowledge`,
`get_customer_history` — built with FastMCP, covering invalid-argument/tool-not-found/timeout/failure/
malformed-output error handling per requirement.md.

Today, `CRMAgent` (see [Agents](#-implementation-status)) already recognizes CRM/lead/appointment intents
and responds honestly that tool execution isn't wired up yet — it does not read or write any CRM data.

## 🧠 Multi-Model LLM Layer

**Status: implemented.** One `LLMProvider` interface (`app/llm/base.py`) with `generate()` and a
cross-provider `generate_structured()` (schema-in-prompt, parse, validate, retry-on-failure). Concrete
adapters:

```text
                    Agent → LLMProvider (interface) → { Mock | OpenAI | Anthropic | Gemini | Groq }
```

- **Mock** (default, `LLM__PROVIDER=mock`): zero dependencies, zero API key, fully deterministic — powers
  every test in this repo and the default local run. It is a heuristic stand-in, not a real model; see its
  docstring in `app/llm/providers/mock.py` for exactly what it does and doesn't do.
- **OpenAI / Anthropic / Gemini / Groq**: real adapters, implemented against each SDK's current chat/
  message-creation API (verified interactively against the installed SDK versions during development —
  see each adapter's docstring for the exact version checked against). They raise a clear
  `ProviderNotConfiguredError` (naming the missing extra or env var) rather than silently falling back to
  the mock if selected without their API key/package installed.

## 💬 Conversational AI

**Status:** web chat is implemented (`POST /chat`). SMS-style and WhatsApp-style channel abstractions are
Phase 10 and not implemented yet.

```text
Conversational AI → { Web Chat [implemented] | SMS [planned] | WhatsApp [planned] } → Agent Runtime
```

## 📞 Voice AI

**Status: not implemented — Phase 9.** Planned architecture (STT → guardrail → intent → router → RAG/
GraphRAG/MCP → LLM → guardrail → TTS), voice capabilities (provider abstraction, voice selection,
pronunciation rules, silence timeout, max call duration, thinking/ambient sound, human transfer, voicemail
detection, recording disclosure, live call testing), and generic voice agent configs (Voice Assistant,
Language Translator, Sales Assistant) are all documented in `requirement.md` and will be built as
`voice/settings.py`, `voice/pronunciation.py`, `voice/voicemail.py`, `voice/handoff.py`, `voice/runtime.py`
with `SpeechToTextProvider`/`TextToSpeechProvider`/`VoiceProvider` interfaces and optional ElevenLabs/
Gemini adapters — no live paid credentials will ever be required to run this repository.

## 🛡️ AI Guardrails

**Status: implemented (Phase 1 scope).** Two agents, `InputGuardrailAgent` and `OutputGuardrailAgent`,
each running a list of independent, deterministic `GuardrailCheck` rules (no LLM call, so they can't be
talked around by the very input they inspect):

- **Input:** not-empty, oversized-request (>4000 chars), a small unsafe-pattern denylist (documented as a
  naive first line of defense, not a general jailbreak/prompt-injection solution).
- **Output:** schema-valid (response is a string), non-empty, a prohibited-pattern denylist (stack traces,
  unrendered template markers).

**Not yet implemented (Phase 6):** semantic grounding, claim decomposition/validation, and LLM-as-a-Judge
hallucination detection — see the next section.

## 🚨 Hallucination Detection

**Status: not implemented — Phase 6.** Planned pipeline: `Response → Semantic Grounding → Claim
Extraction/Decomposition → Claim Validation → LLM-as-a-Judge → PASS | FAIL → Regenerate/Correct`. This
will explicitly not be presented as mathematically perfect hallucination detection — limitations will be
documented alongside the implementation.

## 🧱 Structured Outputs

**Status: implemented as a cross-cutting pattern.** Every agent-to-agent contract in this codebase is a
Pydantic model — `IntentClassification`, `GuardrailCheckResult`/`GuardrailReport`, `AgentConfig`,
`ChatRequest`/`ChatResponse`, `LLMMessage`/`LLMResponse` — validated at construction, not just at the API
boundary. `LLMProvider.generate_structured()` is the mechanism that gets a Pydantic instance back from any
configured provider (including the mock).

## 👨‍💼 Human-in-the-Loop

**Status: not implemented yet.** Planned: an approval gate for sensitive actions (`Sensitive Action? → No
→ Continue`, `→ Yes → Pending Approval → Human Approve/Reject → Resume Workflow`) built on LangGraph's
`interrupt_before` / checkpoint-resume mechanism, which the Phase 1 graph is already compiled with a
checkpointer to support.

## 🧪 Scenario Testing & Evaluation (planned)

**Status:** this repo's own `pytest` suite is implemented today (see [Testing](#-testing) below). The separate
**scenario framework** described in `requirement.md` (declarative `Scenario` definitions with
`success_criteria`, an LLM-assisted scenario *generator*, a `run-all` suite runner, and pass/fail/latency
reporting) is **Phase 7, not implemented yet** — don't confuse the two. RAGAS evaluation and LLM-as-a-Judge
interfaces (response quality, faithfulness, relevance, tool correctness, workflow completion) are also
Phase 7.

## 📊 Observability

**Status: implemented (Phase 1 scope).** Every `BaseAgent.execute()` call emits a structured `AgentEvent`
(`trace_id`, `session_id`, `agent`, `action`, `status`, `latency_ms`) through an `EventBus` to a
`LoggingEventSink` (stdout, JSON-formatted). `POST /chat` returns a `trace_id` on every response.

**Not yet implemented (Phase 8):** optional `LangSmithEventSink` / `LangfuseEventSink` adapters behind the
same `EventSink` interface, tool-execution-specific events (there are no tools yet — that's Phase 4), and
retriever-specific events (no real retriever yet — that's Phase 2).

## 📱 Agent Configuration

**Status: implemented.** Every agent is configuration-driven via a Pydantic `AgentConfig`
(`name, agent_type, description, language, conversation_style, instructions, connectors, knowledge_base,
settings`), with a `default_config()` classmethod per agent and the option to override it entirely at
construction time — no subclassing required to change an agent's identity/instructions/knowledge sources.

## ⚙️ Backend Architecture

**Status: partial.** Implemented: `GET /health`, `POST /chat`, `GET /agents`, `POST /agents/run`,
`POST /documents/upload`, `POST /knowledge/search` (see [API Reference](#api-reference) below). Not
yet implemented: `/conversations/summarize`, `/scenarios/run(-all)`, `/conversations/{id}`,
`/mcp/test-tool`, and the `/voice/*` endpoints — each lands with the phase that implements its
backing capability.

<a id="api-reference"></a>

| Method | Path | Status |
|---|---|---|
| GET | `/health` | ✅ implemented |
| POST | `/chat` | ✅ implemented |
| GET | `/agents` | ✅ implemented |
| POST | `/agents/run` | ✅ implemented |
| POST | `/documents/upload` | ✅ implemented |
| POST | `/knowledge/search` | ✅ implemented |
| POST | `/conversations/summarize` | ⬜ planned (Phase 5) |
| GET | `/conversations/{id}` | ⬜ planned (Phase 5) |
| POST | `/mcp/test-tool` | ⬜ planned (Phase 4) |
| POST | `/scenarios/run` | ⬜ planned (Phase 7) |
| POST | `/scenarios/run-all` | ⬜ planned (Phase 7) |
| POST | `/voice/session`, `/voice/turn`, `/voice/end` | ⬜ planned (Phase 9) |

## 🔄 Asynchronous Processing

**Status: not implemented — Phases 2 & 11.** Planned: `upload → hash → deduplicate → queue → RabbitMQ →
Celery → parse → chunk → embed → store`, with a synchronous local fallback so document ingestion doesn't
require RabbitMQ/Celery to demo.

## ⚡ Redis Usage

**Status: not implemented — Phase 5.** `REDIS__ENABLED` is already a config flag (default `false`, local
in-memory fallback used instead) — see `app/config/settings.py`. Planned uses: conversation state,
semantic/embedding caching, temporary workflow state.

## 🐳 Containerized Deployment

**Status: not implemented — Phase 11.** Planned: a `Dockerfile` and `docker-compose.yml` with the API and
worker as required services and Redis/RabbitMQ/Neo4j as optional services (`docker compose up` should work
with none of them running), per requirement.md Rule 7 (no Kubernetes — Compose is sufficient).

## ☁️ Production Cloud Architecture (illustrative only)

The diagram below describes how a system like this *could* be deployed in a real cloud environment. It is
**conceptual/illustrative, not a build target of this repository** — this project targets local Docker
Compose, not CloudFront/ECS/S3.

```text
CloudFront → Application/API → ECS/EC2 → { Redis | RabbitMQ + Workers | Databases } → S3/Storage
```

## 📂 Project Structure

Reflects what actually exists today (see `PLAN.md` for what each future phase adds):

```text
agentic-ai-platform/
├── app/
│   ├── api/                 FastAPI app factory, deps, routes (health, chat, agents, documents, knowledge)
│   ├── agents/               BaseAgent, IntentAgent, RouterAgent, FAQAgent, RAGAgent, CRMAgent,
│   │                         HandoffAgent, AgentRegistry
│   ├── guardrails/           GuardrailCheck interface, input/output checks, guardrail agents
│   ├── graph/                ConversationState, LangGraph node functions, compiled workflow
│   ├── llm/                  LLMProvider interface + mock/openai/anthropic/gemini/groq adapters
│   ├── rag/                  Real pipeline: ingestion, chunking (7 strategies), embeddings, stores
│   │                         (Chroma/FAISS/Pinecone), retrieval (BM25/hybrid/RRF/Self-RAG/CRAG),
│   │                         reranking (cross-encoder/LLM), pipeline.py orchestrator
│   ├── graph_rag/             Entity/relationship extraction, graph builder, Neo4j + in-memory
│   │                         repositories, graph retriever, context formatter
│   ├── models/                Pydantic schemas (enums, messages, intent, guardrails, agent config, rag,
│   │                         graph_rag)
│   ├── config/                Settings (one category per integration)
│   └── observability/        Structured logging, trace IDs, AgentEvent/EventBus
├── tests/
│   ├── agents/, guardrails/, graph/, llm/, rag/, graph_rag/, api/    153 tests, see Testing below
│   └── test_settings.py
├── demo/data/                 faqs.json, knowledge_documents.json, relationships.json (synthetic, safe)
├── PLAN.md                    Phase-by-phase roadmap and architectural decisions
├── requirement.md             The original build brief this repo implements progressively
├── pyproject.toml
├── .env.example
└── README.md
```

Not created yet (by design — see "Core design principle" in `requirement.md`: no empty scaffolding ahead
of the phase that implements it): `app/mcp/`, `app/voice/`, `app/channels/`, `app/memory/`,
`app/connectors/`, `app/evaluation/`, `app/scenarios/`, `docs/`, `scripts/`, `Dockerfile`,
`docker-compose.yml`.

## 🧪 Testing

```bash
pytest -q
```

**Last measured result: 148 passed, 5 skipped, 0 failed** (`pytest -q`, mock LLM provider, no external
services — the 5 skips are the optional live-Neo4j integration tests, which auto-skip unless a Neo4j
server is actually reachable; see [GraphRAG](#-graphrag--knowledge-graph)). Ruff lint (`ruff check app
tests`) and format (`ruff format --check app tests`) are both clean. First run downloads two small local
models from Hugging Face (embedding + cross-encoder, ~100MB combined, cached afterward under
`~/.cache/huggingface`) and takes ~50-60s; subsequent runs are model-load-bound (~15-25s) rather than
network-bound, since both models are cached process-wide, not just on disk. Coverage: intent
classification heuristics, table-based routing for every intent category, the full RAG pipeline
(ingestion/dedup, all 7 chunking strategies, embedding cache hit/miss, Chroma+FAISS add/query/delete,
BM25, RRF with weighting, cross-encoder + LLM reranking, Self-RAG/CRAG strategy logic, and an end-to-end
pipeline integration test with real embeddings), the full GraphRAG pipeline (entity/relationship
extraction, graph builder, in-memory repository CRUD/traversal, multi-hop retrieval, context formatting,
and — when a Neo4j server is reachable — a real live-database integration suite), FAQ/RAG/GraphRAG
grounded-answer and no-match/low-relevance paths, the CRM skeleton's honesty about not being wired to
MCP, the handoff agent, every input/output guardrail check, a full-graph integration test per demo
scenario (FAQ query, RAG query, GraphRAG relationship query, CRM update, human handoff, guardrail
rejection), cross-turn memory accumulation via the LangGraph checkpointer, document upload + knowledge
search API routes. External providers (OpenAI/Anthropic/Gemini/Groq, Pinecone) are not exercised by the
test suite — they need a real API key by nature.

## ⚙️ Configuration

Copy `.env.example` to `.env`. Every category below has a working default that requires **no external
service and no API key** — see the file for the full list of variables.

| Category | Required? | Default | Notes |
|---|---|---|---|
| `LLM__*` | Required (but defaults to mock) | `provider=mock` | Set to `openai`/`anthropic`/`gemini`/`groq` + the matching API key + install that extra (`pip install -e ".[openai]"` etc.) for a real model. |
| `RAG__*` | Optional | `chunking_strategy=recursive`, `reranker=none` | See [RAG](#-rag) for every strategy/reranker option. |
| `VECTOR_STORE__*` | Optional | `provider=chroma`, local dir | FAISS (`pip install -e ".[faiss]"`) and Pinecone (`.[pinecone]"`) are drop-in alternatives. |
| `NEO4J__*` | Optional | `enabled=false` | In-memory graph fallback when disabled or unreachable — see [GraphRAG](#-graphrag--knowledge-graph). |
| `REDIS__*` | Optional | `enabled=false` | In-memory fallback when disabled (Phase 5). |
| `RABBITMQ__*` | Optional | `enabled=false` | Synchronous ingestion fallback when disabled (Phase 2/11). |
| `MCP__*` | Optional | local host/port | Not wired up until Phase 4. |
| `VOICE__*` | Optional | `provider=mock` | Real voice provider adapters land in Phase 9. |
| `LANGSMITH__*` | Optional | `enabled=false` | Phase 8. |
| `LANGFUSE__*` | Optional | `enabled=false` | Phase 8. |
| `EVALUATION__*` | Optional | `ragas_enabled=false` | Phase 7. |

Never commit `.env`. Secrets are only ever read from the environment (`pydantic-settings`) — nothing is
hard-coded.

## 🚧 Limitations

- The `MockLLMProvider` is a deterministic keyword heuristic, not a language model — it demonstrates the
  architecture end-to-end offline, but response *quality* with it is intentionally limited. Configure a
  real provider for genuine generation/classification quality.
- `FAQAgent` still uses simple keyword lookup over a small curated FAQ list (a deliberately
  different, simpler problem than RAG over longer documents) — `RAGAgent` uses the real Phase 2
  pipeline. See [RAG](#-rag) for exactly what's real vs. approximated within that pipeline
  (`proposition`/`agentic`/`late` chunking, Self-RAG, and CRAG are all documented simplifications
  of published techniques, not full reproductions of them).
- `CRMAgent` does not call any tool yet — it recognizes CRM-shaped intents and says so honestly.
- Conversation memory is short-term and in-process only (LangGraph's `MemorySaver`) — it is lost on
  process restart and does not survive across multiple API instances. Redis-backed persistence is Phase 5.
- Guardrails are rule-based pattern checks, not a general-purpose safety/jailbreak solution, and there is
  no grounding/hallucination check yet (Phase 6) beyond `RAGAgent`'s lexical-overlap relevance gate.
- FAISS and PyTorch/sentence-transformers each bundle their own OpenMP runtime, which can deadlock
  if both are loaded in one process on some platforms — worked around in `app/__init__.py`
  (`KMP_DUPLICATE_LIB_OK=TRUE`); see `PLAN.md` §3b if you hit a similar hang with a different
  native-dependency combination.
- GraphRAG's entity/relationship extractors are regex-based, correct for this repo's fixed
  synthetic sentence templates but explicitly not general-purpose NER/RE — see
  [GraphRAG](#-graphrag--knowledge-graph). The knowledge graph itself is small (5 customers, 2
  agents) and intended to demonstrate the pattern, not graph scale.
- No MCP, voice, multi-channel, async pipeline, evaluation, or observability-export functionality
  exists yet — see [Implementation Status](#-implementation-status).
- No CI workflow file exists yet.

## 🗺️ Roadmap

See [`PLAN.md`](PLAN.md) for the full phase-by-phase plan (Phases 2–12: Real RAG, GraphRAG, MCP, Memory,
Guardrails+Reliability, Evaluation, Observability, Voice AI, Multi-Channel, Docker, Documentation/Demo).

## License

See [`LICENSE`](LICENSE).
