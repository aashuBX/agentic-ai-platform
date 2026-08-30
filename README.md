# 🤖 Enterprise Conversational Agentic AI Platform

<p align="center">

### Production-Oriented GenAI • Agentic AI • Multi-Agent Systems • Advanced RAG • GraphRAG • MCP • Voice AI • LLMOps

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-1C3C3C?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20Framework-1C3C3C?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-6B4FBB?style=for-the-badge)
![RAG](https://img.shields.io/badge/Advanced-RAG-0A7AFF?style=for-the-badge)
![GraphRAG](https://img.shields.io/badge/GraphRAG-Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Memory%20%26%20Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</p>

---

## 🎯 Overview

This repository is an **independent public implementation of a production-oriented Conversational Agentic AI platform**, created to demonstrate modern AI engineering architecture and implementation patterns.

The platform brings together:

- Multi-Agent orchestration
- LangGraph stateful workflows
- LangChain
- Intent detection and intelligent routing
- Chat-based AI agents
- Advanced RAG
- Self-RAG
- Corrective RAG (CRAG)
- Hybrid retrieval
- BM25
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder reranking
- LLM-based reranking abstraction
- GraphRAG
- Neo4j
- Entity and relationship extraction
- MCP / FastMCP architecture
- Tool calling and enterprise-style tools
- Conversation memory
- Checkpointed state
- Input / output guardrails
- Semantic grounding and hallucination controls
- LLM-as-a-Judge
- Human-in-the-loop workflows
- Voice AI
- Speech-to-Text / Text-to-Speech
- Scenario-based agent evaluation
- RAGAS
- LangSmith / Langfuse
- Redis
- RabbitMQ / Celery
- FastAPI
- Docker
- Cloud-ready architecture

The implementation is intentionally modular so individual capabilities can evolve independently.

---

# ⭐ Core AI Capabilities

| Capability | Focus |
|---|---|
| 🤖 Agentic AI | Multi-Agent orchestration, specialized agents, routing |
| 🧠 LangGraph | Stateful workflows, conditional routing, checkpointing |
| 🔀 Intent Routing | Structured intent classification and deterministic routing |
| 🔎 Advanced RAG | Vector + BM25 + hybrid retrieval + reranking |
| 🕸️ GraphRAG | Relationship-aware and multi-hop knowledge retrieval |
| 🔌 MCP | MCP Client / Server architecture and tool integration |
| 🧠 Memory | Conversation state and checkpoint-based context |
| 🛡️ Guardrails | Input/output validation and response controls |
| 📊 LLMOps | Tracing, structured events, evaluation architecture |
| 🧪 Evaluation | Scenario testing, RAGAS, LLM-as-a-Judge |
| 📞 Voice AI | STT/TTS, voice configuration and conversational workflows |
| ⚙️ Backend | Python, FastAPI, asynchronous processing |
| ☁️ Infrastructure | Redis, RabbitMQ, Celery, Docker, AWS-oriented architecture |

---

# 🏗️ End-to-End Architecture

```text
                                      ┌──────────────────────┐
                                      │         USER         │
                                      │                      │
                                      │ Web / SMS / WhatsApp │
                                      │        / Voice       │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │   CHANNEL LAYER      │
                                      │ Chat / Messaging /   │
                                      │ Voice Adapters       │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │   INPUT GUARDRAIL    │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │    INTENT AGENT      │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │     AGENT ROUTER     │
                                      └──────────┬───────────┘
                                                 │
             ┌───────────────────────────────────┼──────────────────────────────────┐
             │                                   │                                  │
             ▼                                   ▼                                  ▼
      ┌──────────────┐                    ┌──────────────┐                   ┌──────────────┐
      │   FAQ AGENT  │                    │   RAG AGENT  │                   │   CRM AGENT  │
      └──────────────┘                    └──────┬───────┘                   └──────┬───────┘
                                                 │                                  │
                                                 ▼                                  ▼
                                        ┌─────────────────┐                  ┌───────────────┐
                                        │  RAG PIPELINE   │                  │  MCP CLIENT   │
                                        └────────┬────────┘                  └───────┬───────┘
                                                 │                                   │
                             ┌───────────────────┼───────────────────┐               ▼
                             ▼                   ▼                   ▼        ┌───────────────┐
                         Vector Search        BM25              GraphRAG      │  MCP SERVER   │
                             │                   │                   │        └───────┬───────┘
                             └───────────────────┼───────────────────┘                │
                                                 ▼                                    │
                                            RRF Fusion                                │
                                                 │                                    │
                                                 ▼                                    │
                                            Reranking                                 │
                                                 │                                    │
                                                 └───────────────────┬────────────────┘
                                                                     ▼
                                                               ┌──────────┐
                                                               │   LLM    │
                                                               └────┬─────┘
                                                                    │
                                                                    ▼
                                                          ┌──────────────────┐
                                                          │ OUTPUT GUARDRAIL  │
                                                          └─────────┬────────┘
                                                                    │
                                                                    ▼
                                                               RESPONSE

                         ┌──────────────────────────────────────────────────┐
                         │ Memory • Observability • Evaluation • Logging   │
                         └──────────────────────────────────────────────────┘
```

> The repository currently contains a working web-chat/core orchestration path, with additional platform capabilities represented as extensible modules and implementation roadmap items.

---

# 🤖 Agentic AI Architecture

The platform uses specialized agents rather than putting all behavior into one monolithic agent.

```text
User Request
     │
     ▼
Input Guardrail
     │
     ▼
Intent Detection
     │
     ▼
Agent Router
     │
     ├──────────────► FAQ Agent
     │
     ├──────────────► RAG Agent
     │
     ├──────────────► GraphRAG Agent
     │
     ├──────────────► CRM Agent
     │
     ├──────────────► Feedback Agent
     │
     └──────────────► Handoff Agent
                          │
                          ▼
                    Human Assistance

Selected Agent
     │
     ▼
Knowledge / Tools / Memory
     │
     ▼
LLM
     │
     ▼
Output Guardrail
     │
     ▼
Response
```

## Specialized Agents

### FAQ Agent
Handles straightforward knowledge and FAQ-oriented requests.

### RAG Agent
Uses retrieval-based generation for document and knowledge-intensive questions.

### GraphRAG Agent
Supports relationship-aware and multi-hop retrieval using graph data.

### CRM Agent
Designed to interact with enterprise-style CRM capabilities through a tool abstraction.

### Feedback Agent
Designed for feedback-oriented workflows.

### Handoff Agent
Provides escalation from autonomous AI to human assistance.

---

# 🔀 Intent Detection & Agent Routing

The routing layer converts user requests into structured intent and selects the appropriate agent.

Supported intent categories include:

```text
FAQ
KNOWLEDGE_QUERY
GRAPH_QUERY
CRM_QUERY
CRM_UPDATE
APPOINTMENT_QUERY
FEEDBACK
HANDOFF
VOICE_TASK
UNKNOWN
```

Example:

```text
User Request
      ↓
IntentClassification
      ↓
Intent + Confidence + Routing Metadata
      ↓
Agent Router
      ↓
Specialized Agent
```

The implementation uses structured Pydantic outputs and a provider abstraction so the same routing path can work with the repository's deterministic mock provider or a configured real LLM provider.

---

# 🧠 LangGraph Orchestration

The core workflow is built around a stateful LangGraph graph.

```text
START
  ↓
Input Guardrail
  ↓
Intent Detection
  ↓
Agent Router
  ↓
Specialized Agent
  ↓
Output Guardrail
  ↓
END
```

Conversation state includes concepts such as:

```text
session_id
user_id
channel
messages
intent
selected_agent
retrieved_context
selected_tools
tool_results
response
guardrail_results
metadata
```

The architecture is designed for future extensions such as:

- ReAct
- Plan-and-Execute
- hierarchical agent graphs
- inter-agent delegation
- human approval
- retries
- checkpoint-based resumption

---

# 🔎 Advanced RAG

The RAG layer goes beyond basic vector similarity.

## End-to-End Retrieval Pipeline

```text
DOCUMENT
   ↓
PARSER
   ↓
SHA-256 HASH
   ↓
DUPLICATE DETECTION
   ↓
CHUNKING
   ↓
EMBEDDINGS
   ↓
VECTOR STORE


USER QUERY
   ↓
QUERY REWRITING
   ↓
┌───────────────────────┐
│                       │
▼                       ▼
VECTOR SEARCH          BM25
│                       │
└──────────┬────────────┘
           ▼
      HYBRID RETRIEVAL
           ↓
          RRF
           ↓
       RERANKING
           ↓
    TOP RELEVANT CONTEXT
           ↓
           LLM
           ↓
      GROUNDED ANSWER
```

## Retrieval Techniques

- Vector Search
- Semantic Search
- BM25
- Hybrid Retrieval
- Reciprocal Rank Fusion
- Cross-Encoder Reranking
- LLM Reranking
- Query Rewriting
- Relevance Gating
- Semantic Caching architecture
- Self-RAG strategy
- Corrective RAG / CRAG strategy

---

# ✂️ Document Chunking

A common `ChunkingStrategy` interface allows multiple chunking approaches to be selected through a factory.

Supported strategies:

```text
Recursive
Semantic
Document-Aware
Proposition
Late
Hierarchical
Agentic
```

Example:

```text
Document
   ↓
ChunkingFactory
   ↓
Selected ChunkingStrategy
   ↓
Chunks
```

The repository distinguishes between full implementations and deliberately simplified approximations where the underlying technique requires richer model infrastructure.

---

# 🧠 Embedding Pipeline

```text
Document
   ↓
Chunk
   ↓
Embedding Provider
   ↓
Vector Representation
   ↓
Embedding Cache
   ↓
Vector Store
```

Supported concepts include:

- Sentence Transformers
- OpenAI embeddings
- embedding cache
- in-memory caching
- SQLite-persistent cache

---

# 🗄️ Vector & Search Stores

The architecture supports adapters for:

- Chroma
- FAISS
- Pinecone
- Elasticsearch-oriented search workflows
- Neo4j for graph storage/retrieval

Local-first defaults keep the project practical for portfolio demonstrations.

---

# 🕸️ GraphRAG & Knowledge Graph

GraphRAG is used for relationship-aware and multi-hop retrieval.

```text
DOCUMENT
   ↓
ENTITY EXTRACTION
   ↓
RELATIONSHIP EXTRACTION
   ↓
GRAPH BUILDER
   ↓
NEO4J / IN-MEMORY GRAPH
   ↓
GRAPH RETRIEVAL
   ↓
GRAPHRAG AGENT
   ↓
LLM
```

Example knowledge graph:

```text
Customer ──OWNS──────► Account
Customer ──CREATED───► Order
Customer ──ASSIGNED──► Agent
Customer ──BOOKED────► Appointment
Appointment ──WITH───► Agent
```

This enables questions where plain vector similarity is insufficient and relationships themselves carry the important information.

---

# 🔌 MCP — Model Context Protocol

The platform is designed with MCP as the integration boundary between agents and enterprise capabilities.

```text
                    CRM / Business Agent
                            │
                            ▼
                       MCP Client
                            │
                            ▼
                       MCP Server
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
          Customer       Lead        Appointment
            Tools        Tools          Tools
               │            │            │
               └────────────┼────────────┘
                            ▼
                     Mock / Local Data
```

Planned MCP tool categories include:

```text
Customer Tools
Lead Tools
Appointment Tools
Knowledge Tools
Conversation / History Tools
```

Example tool concepts:

```text
get_customer()
search_customer()
create_customer()
update_customer()

get_lead()
search_lead()
create_lead()
update_lead()

get_appointment()
search_appointment()
create_appointment()
update_appointment()
cancel_appointment()

search_knowledge()
get_customer_history()
```

The repository keeps this integration public-safe by using synthetic/local data rather than any real enterprise system.

---

# 🧠 Multi-Model LLM Architecture

The application uses a provider abstraction rather than coupling agents to a single LLM vendor.

```text
                       Agent
                         │
                         ▼
                  LLMProvider
                    Interface
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      Mock             OpenAI        Anthropic
        │
        ├──────────────► Gemini
        │
        └──────────────► Groq
```

Providers represented by the project include:

- Mock provider
- OpenAI
- Anthropic
- Google Gemini
- Groq

Structured generation is represented through a common provider interface and Pydantic schemas.

---

# 💬 Conversational AI

The platform provides a channel-independent conversational architecture.

```text
                  Conversational AI
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Web Chat          SMS         WhatsApp
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    Agent Runtime
```

The repository currently exposes a web-chat API while keeping the channel layer extensible for additional adapters.

---

# 📞 Voice AI

Voice AI is designed as a first-class extension of the conversational agent runtime.

```text
User Speech
     ↓
Speech-to-Text
     ↓
Input Guardrail
     ↓
Intent Detection
     ↓
Agent Router
     ↓
RAG / GraphRAG / MCP
     ↓
LLM
     ↓
Output Guardrail
     ↓
Text-to-Speech
     ↓
User Voice
```

The voice architecture covers:

- STT abstraction
- TTS abstraction
- voice provider abstraction
- voice selection
- voice configuration
- pronunciation rules
- silence timeout
- maximum call duration
- thinking sound
- ambient sound
- human transfer
- voicemail detection
- recording disclosure
- live voice testing
- translator agent
- sales assistant agent

The repository keeps these capabilities modular so real voice providers can be integrated without coupling the entire platform to a single provider.

---

# 🎙️ Voice Configuration

Example configuration:

```yaml
voice:
  provider: mock
  language: en-US
  max_call_duration: 900
  silence_timeout: 10
  thinking_sound: true
  ambient_sound: true
  transfer_to_human: true
  voicemail_detection: true
  recording_disclosure: true
```

---

# 🗣️ Pronunciation & Voice Controls

Voice workflows are designed to support:

```text
Term
 ↓
Pronunciation Rule
 ↓
TTS Provider
 ↓
Natural Speech
```

Additional runtime controls include:

- Silence handling
- Maximum call duration
- Thinking sound
- Ambient sound
- Voicemail handling
- Human transfer
- Recording disclosure

---

# 🧠 Memory & Stateful Conversations

The project treats memory as a separate architectural concern.

```text
Conversation
      ↓
Agent State
      │
      ├── Short-Term Messages
      ├── Checkpointed Workflow State
      ├── Conversation Summary
      └── Long-Term Memory Adapter
```

The current runtime demonstrates short-term stateful conversation through LangGraph checkpointing.

The architecture is prepared for:

- Redis-backed persistence
- cross-session memory
- vector memory
- conversation summaries

---

# 🛡️ AI Guardrails

The platform validates both incoming user input and generated model output.

## Input Guardrails

```text
User Input
    ↓
Validation
    ↓
Policy / Pattern Checks
    ↓
Approved Request
```

## Output Guardrails

```text
LLM Response
    ↓
Schema Validation
    ↓
Output Checks
    ↓
Validated Response
```

Current guardrail concepts include:

- empty input validation
- oversized request protection
- unsafe pattern checks
- non-empty output validation
- prohibited-pattern checks
- structured output validation

The architecture is designed to extend into:

- semantic grounding
- claim decomposition
- claim validation
- hallucination detection
- LLM-as-a-Judge
- regeneration / correction

---

# 🚨 Hallucination & Reliability Layer

The reliability pipeline is designed as:

```text
LLM Response
     ↓
Semantic Grounding
     ↓
Claim Extraction
     ↓
Claim Validation
     ↓
LLM-as-a-Judge
     ↓
PASS / FAIL
     ↓
Regenerate / Correct
```

This layer is deliberately designed as a modular validation pipeline rather than treating model output as automatically trustworthy.

---

# 🧱 Structured Outputs

Pydantic models are used to make AI and API contracts explicit.

Examples include:

```text
IntentClassification
GuardrailCheckResult
GuardrailReport
AgentConfig
ChatRequest
ChatResponse
LLMMessage
LLMResponse
RAG schemas
GraphRAG schemas
```

This makes agent-to-agent and API interactions predictable and easier to validate.

---

# 👨‍💼 Human-in-the-Loop

The architecture supports controlled human intervention for sensitive actions.

```text
Agent
  ↓
Decision
  ↓
Sensitive Action?
  │
 ┌┴──────────────┐
 ▼               ▼
No              Yes
 │                │
 ▼                ▼
Continue      Pending Approval
                  │
             ┌────┴────┐
             ▼         ▼
          Approve     Reject
             │
             ▼
           Resume
```

LangGraph checkpointing provides the foundation for future interrupt/resume workflows.

---

# 🧪 Scenario Testing & Evaluation

The platform is designed for scenario-based agent evaluation.

Example scenario:

```yaml
name: CRM Lead Qualification

description: >
  Verify that the agent can identify a lead,
  collect required information and perform
  the expected workflow.

success_criteria:
  - Correct intent detected
  - Correct agent selected
  - Correct tool selected
  - Workflow completes successfully
  - Final response is valid
```

The evaluation architecture supports:

- Scenario definitions
- Scenario generation
- Scenario execution
- Run-all workflows
- Success criteria
- Pass/fail reporting
- Latency measurement
- Agent evaluation
- Tool evaluation
- Retrieval evaluation

---

# 📊 RAG & Agent Evaluation

Evaluation concepts include:

### RAG

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

### Agent

- Routing accuracy
- Agent selection
- Workflow completion
- Response quality

### Tools

- Tool selection
- Argument correctness
- Execution success

### Reliability

- Guardrail behavior
- Grounding
- Hallucination detection

---

# 🔍 LLMOps & Observability

The platform is structured for traceable AI execution.

```text
Request
  ↓
Agent
  ↓
Retrieval / Tool
  ↓
LLM
  ↓
Guardrail
  ↓
Response
```

Structured events can capture:

```text
trace_id
session_id
agent
action
status
latency_ms
```

The architecture also supports:

- LangSmith
- Langfuse
- structured JSON logs
- agent execution events
- tool execution traces
- retrieval traces
- evaluation traces

---

# ⚡ Distributed Processing & Infrastructure

The platform is designed to separate interactive AI workloads from background processing.

```text
API
 ↓
Message Queue
 ↓
RabbitMQ
 ↓
Celery Worker
 ↓
Background Processing
```

Potential workloads include:

- document ingestion
- chunking
- embeddings
- evaluation
- summaries
- asynchronous processing

---

# 🔴 Redis

Redis is part of the state and caching architecture.

Potential uses include:

- conversation state
- semantic caching
- embedding caching
- temporary workflow state
- frequently accessed data

---

# 📦 Document Processing Pipeline

```text
Upload
  ↓
Hash
  ↓
Deduplication
  ↓
Parse
  ↓
Chunk
  ↓
Embed
  ↓
Store
```

Supported document-oriented concepts include:

- TXT
- Markdown
- PDF
- SHA-256 hashing
- duplicate detection
- chunking
- embeddings
- vector storage
- knowledge search

---

# ☁️ Cloud & Production Architecture

The project is designed with cloud-oriented architecture in mind.

Illustrative deployment:

```text
Cloud / CDN
    ↓
Application / API
    ↓
Compute
    ↓
┌────────────┬──────────────┬──────────────┐
│            │              │
Redis     RabbitMQ       Databases
│            │              │
│         Celery          │
│         Workers         │
└────────────┼──────────────┘
             ↓
         Object Storage
```

Relevant infrastructure concepts include:

- AWS
- S3
- CloudFront
- EC2 / ECS
- Lambda
- Redis
- RabbitMQ
- Celery
- Docker
- CI/CD

---

# 🐳 Containerization

The architecture is designed for containerized deployment.

```text
                 Docker
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
      API        Worker      MCP
                               │
                               ▼
                         External Tools
```

The target production model is modular rather than a single monolithic container.

---

# 📂 Project Structure

```text
agentic-ai-platform/
│
├── app/
│   ├── api/
│   ├── agents/
│   ├── config/
│   ├── graph/
│   ├── graph_rag/
│   ├── guardrails/
│   ├── llm/
│   ├── models/
│   ├── observability/
│   │
│   └── rag/
│       ├── ingestion/
│       ├── chunking/
│       ├── embeddings/
│       ├── retrieval/
│       ├── reranking/
│       └── stores/
│
├── demo/
│   └── data/
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── PLAN.md
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# 🛠️ Technology Stack

## Generative AI / LLM

- OpenAI
- Anthropic
- Google Gemini
- Groq
- LangChain
- LangGraph

## Agentic AI

- Multi-Agent orchestration
- Intent Detection
- Agent Routing
- ReAct architecture
- Plan-and-Execute architecture
- Hierarchical Agent Graphs
- Stateful Workflows
- Inter-Agent Delegation
- Human-in-the-Loop
- Checkpointed execution
- MCP
- FastMCP
- Tool Calling

## RAG / Knowledge

- Advanced RAG
- Self-RAG
- Corrective RAG / CRAG
- Hybrid Retrieval
- Vector Search
- BM25
- Reciprocal Rank Fusion
- Cross-Encoder Reranking
- LLM Reranking
- Query Rewriting
- Semantic Search
- Semantic Caching

## GraphRAG

- Neo4j
- Knowledge Graphs
- Entity Extraction
- Relationship Extraction
- Multi-Hop Retrieval
- Graph Retrieval

## Vector / Search

- Chroma
- FAISS
- Pinecone
- Elasticsearch
- Sentence Transformers

## Document AI

- Recursive Chunking
- Semantic Chunking
- Document-Aware Chunking
- Proposition Chunking
- Late Chunking
- Hierarchical Chunking
- Agentic Chunking
- Embedding Pipelines
- Embedding Cache

## Conversational AI

- Web Chat
- SMS-style channel architecture
- WhatsApp-style channel architecture
- Channel abstraction
- Conversation state

## Voice AI

- Speech-to-Text
- Text-to-Speech
- Voice Provider Abstraction
- Voice Configuration
- Pronunciation
- Silence Handling
- Voicemail Detection
- Human Transfer
- Recording Disclosure
- Live Voice Testing
- Translator Agent
- Sales Assistant Agent

## Reliability / Guardrails

- Input Guardrails
- Output Guardrails
- Semantic Grounding
- Claim Decomposition
- Claim Validation
- Hallucination Detection
- LLM-as-a-Judge
- Structured Outputs
- Pydantic

## Evaluation / LLMOps

- RAGAS
- Scenario Testing
- Success Criteria
- LangSmith
- Langfuse
- Structured Logging
- Tracing
- Agent Execution Events

## Backend / Infrastructure

- Python
- FastAPI
- Flask
- Redis
- RabbitMQ
- Celery
- WebSockets
- Docker
- AWS
- S3
- CloudFront
- EC2
- ECS
- Lambda
- CI/CD

---

# 🚀 Quick Start

Requires Python 3.11+.

```bash
git clone https://github.com/aashuBX/agentic-ai-platform.git
cd agentic-ai-platform

python3.11 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"

cp .env.example .env
```

Start the API:

```bash
uvicorn app.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

for the interactive FastAPI / Swagger interface.

---

# 🔌 Example API Usage

Health:

```bash
curl -s http://127.0.0.1:8000/health
```

Chat:

```bash
curl -s -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "demo-1",
    "message": "What are your business hours?",
    "channel": "web"
  }'
```

Knowledge search:

```bash
curl -s -X POST http://127.0.0.1:8000/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "data retention policy",
    "top_k": 3
  }'
```

Agent listing:

```bash
curl -s http://127.0.0.1:8000/agents
```

---

# 🧪 Testing

The repository includes automated tests covering the implemented areas of the platform.

Example:

```bash
pytest -q
```

Additional checks:

```bash
ruff check app tests
ruff format --check app tests
```

Tests cover areas such as:

- intent classification
- agent routing
- graph workflow behavior
- FAQ / RAG behavior
- document ingestion
- chunking strategies
- embeddings
- vector stores
- BM25
- RRF
- reranking
- GraphRAG
- guardrails
- checkpointed conversation state
- API routes

External providers such as OpenAI, Anthropic, Gemini, Groq and Pinecone require their own credentials and are therefore provider-dependent.

---

# ⚙️ Configuration

Configuration is environment-driven.

Representative categories:

```text
LLM
RAG
VECTOR_STORE
NEO4J
REDIS
RABBITMQ
MCP
VOICE
LANGSMITH
LANGFUSE
EVALUATION
```

Example:

```text
LLM__PROVIDER=mock
RAG__RERANKER=none
VECTOR_STORE__PROVIDER=chroma
NEO4J__ENABLED=false
REDIS__ENABLED=false
RABBITMQ__ENABLED=false
```

Secrets must be supplied through environment variables.

Never commit `.env`.

---

# 🧭 Engineering Principles

### 1. Modular AI Architecture

Agents, retrieval, tools, memory, guardrails and evaluation are separate concerns.

### 2. Provider Abstraction

LLM, embedding, vector, voice and evaluation providers are accessed through interfaces.

### 3. Local-First Development

The repository supports local or mock implementations wherever practical.

### 4. Public-Safe by Design

The project uses synthetic data and does not depend on private enterprise systems.

### 5. Explainable Workflows

Important AI decisions are represented as explicit state transitions, routing decisions and execution events.

### 6. Evaluation-Aware Engineering

AI behavior should be measured and tested rather than assumed to be correct.

---

# 📌 Current Implementation Focus

The repository demonstrates a working foundation around:

```text
FastAPI
   ↓
Input Guardrail
   ↓
Intent Detection
   ↓
LangGraph Workflow
   ↓
Agent Router
   ↓
FAQ / RAG / GraphRAG / CRM pathways
   ↓
Output Guardrail
   ↓
Response
```

Implemented areas are expanded incrementally while additional capabilities remain modular and documented in the project roadmap.

---

# 🗺️ Roadmap

The roadmap covers:

- Core Agent Runtime
- Advanced RAG
- GraphRAG
- MCP
- Memory
- Guardrails & Reliability
- Evaluation
- LLMOps
- Voice AI
- Multi-Channel
- Docker / Production Infrastructure
- Documentation & Demo

See `PLAN.md` for implementation details and architectural decisions.

---

# 🔐 Independent Portfolio Project

This repository is an **independent public implementation created for technical portfolio and demonstration purposes**.

It is:

- not an employer product
- not affiliated with or endorsed by an employer
- not based on proprietary source code
- not connected to internal enterprise APIs
- not using production credentials
- not using customer data
- not exposing confidential prompts or schemas

The implementation uses public technologies and synthetic/mock data.

---

# 🎓 What This Project Demonstrates

This repository demonstrates how an AI engineer can combine:

```text
LLMs
  ↓
Prompt Engineering
  ↓
Structured Outputs
  ↓
Agentic Workflows
  ↓
Multi-Agent Orchestration
  ↓
RAG
  ↓
GraphRAG
  ↓
MCP / Tool Calling
  ↓
Memory
  ↓
Guardrails
  ↓
Evaluation
  ↓
LLMOps
  ↓
Production-Oriented Infrastructure
```

The engineering goal is:

```text
Understand
    ↓
Reason
    ↓
Retrieve
    ↓
Select Tools
    ↓
Execute
    ↓
Validate
    ↓
Evaluate
    ↓
Improve
```

---

# 👨‍💻 About

**Aashu Kumar Jha**

AI / GenAI / Agentic AI Engineer

Focus areas:

```text
Agentic AI
Generative AI
LLM Engineering
LangGraph
LangChain
MCP
Advanced RAG
GraphRAG
AI Guardrails
LLMOps
Voice AI
Python
FastAPI
AWS
Distributed Systems
```

GitHub:

https://github.com/aashuBX

---

<div align="center">

# 🤖 Understand → Reason → Retrieve → Act → Validate → Evaluate

### Build Intelligent Systems. Engineer for Reliability. Ship to Production.

</div>
