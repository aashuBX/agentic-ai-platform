You are acting as a senior AI platform architect, senior Python engineer, Agentic AI engineer, RAG engineer, MCP engineer, voice AI engineer, and DevOps engineer.

You are working inside this repository:

agentic-ai-platform

This is a PUBLIC GitHub portfolio repository.

IMPORTANT CONTEXT
-----------------
This repository is an independent public implementation created to demonstrate AI engineering capabilities that I use professionally.

The original production system I work on is proprietary and MUST NOT be copied, reverse engineered, reconstructed from proprietary code, or exposed here.

DO NOT:
- copy proprietary company source code
- copy internal APIs
- copy confidential prompts
- copy production credentials
- copy customer data
- copy internal database schemas
- copy private URLs
- copy proprietary business logic
- use company screenshots/assets
- fabricate production metrics
- claim this repository is the actual employer system

Instead:
- build everything independently
- use generic/public-safe architecture
- use synthetic/mock data
- use open/public technologies
- use local development defaults wherever practical
- clearly distinguish implemented features from planned features
- document that this is an independent implementation

============================================================
PRIMARY OBJECTIVE
============================================================

Build a serious, production-oriented, public-safe:

"Enterprise Conversational Agentic AI Platform"

The project must demonstrate an end-to-end AI platform covering:

1. Conversational AI
2. Chat agents
3. Voice agents
4. Multi-agent orchestration
5. LangGraph
6. Intent detection
7. Agent routing
8. FAQ agent
9. RAG agent
10. GraphRAG agent
11. CRM agent
12. Feedback agent
13. Handoff agent
14. MCP client
15. MCP server
16. FastMCP
17. Tool calling
18. CRM-style tools
19. Appointment tools
20. Knowledge tools
21. Advanced RAG
22. Vector retrieval
23. BM25 retrieval
24. Hybrid retrieval
25. Reciprocal Rank Fusion
26. Cross-encoder reranking
27. LLM reranking abstraction
28. Query rewriting
29. Self-RAG
30. Corrective RAG / CRAG
31. GraphRAG
32. Neo4j
33. Entity extraction
34. Relationship extraction
35. Knowledge graph construction
36. Document ingestion
37. File hashing
38. Duplicate detection
39. Async processing
40. RabbitMQ
41. Celery
42. Multiple chunking strategies
43. Embeddings
44. Embedding cache
45. Vector databases
46. Conversation memory
47. Cross-session memory
48. Redis
49. LangGraph checkpointing
50. Conversation summaries
51. Input guardrails
52. Output guardrails
53. Semantic grounding
54. Hallucination detection
55. Claim decomposition
56. Claim validation
57. LLM-as-a-Judge
58. Pydantic structured output
59. Human-in-the-loop
60. Scenario-based agent testing
61. Scenario generation
62. Success criteria
63. Run-all-scenarios
64. Agent logs
65. LangSmith integration
66. Langfuse integration
67. RAGAS evaluation
68. Multi-provider LLM abstraction
69. Voice provider abstraction
70. Speech-to-text abstraction
71. Text-to-speech abstraction
72. Pronunciation rules
73. Silence handling
74. Voicemail detection
75. Human transfer
76. Recording disclosure
77. Voice live-test interface
78. Web chat channel
79. SMS-style channel abstraction
80. WhatsApp-style channel abstraction
81. FastAPI API layer
82. Docker
83. Docker Compose
84. Tests
85. CI/CD-ready structure
86. Documentation
87. Architecture diagrams
88. Demo-ready UI/API
89. Example datasets
90. Reproducible local setup

Do not attempt to make every component enterprise-scale on the first pass.

The architecture must be modular so components can be progressively improved.

============================================================
CORE DESIGN PRINCIPLE
============================================================

This repository must NOT become a huge collection of empty files.

Every major module must either:
- work,
- have a meaningful interface and implementation stub with clear status,
- or be explicitly marked as optional/pluggable and documented.

Prefer:
"small working vertical slice"
over:
"100 empty files"

Build the project progressively and keep it runnable after each major phase.

============================================================
TECHNOLOGY PREFERENCES
============================================================

Primary language:
- Python 3.11+

Backend:
- FastAPI
- Pydantic
- Uvicorn

Agent orchestration:
- LangGraph
- LangChain

LLM abstraction:
- OpenAI
- Anthropic
- Gemini
- Groq

MCP:
- FastMCP
- MCP client/server architecture

RAG:
- ChromaDB and/or FAISS as local default
- Pinecone as optional adapter
- BM25
- sentence-transformers where appropriate
- cross-encoder reranking

Graph:
- Neo4j
- local/mock fallback when Neo4j is unavailable

State/cache:
- Redis
- local in-memory fallback for development where appropriate

Async:
- RabbitMQ
- Celery

Database:
- SQLite as the simplest default for local/public demo
- SQLAlchemy if useful

Evaluation:
- RAGAS
- LangSmith
- Langfuse

Observability:
- Python structured logging
- trace IDs
- agent events
- tool execution events

Voice:
- provider abstraction
- STT abstraction
- TTS abstraction
- optional providers such as ElevenLabs / Gemini through adapters

Infrastructure:
- Docker
- Docker Compose

Testing:
- pytest
- unit tests
- integration tests
- workflow tests

Code quality:
- type hints
- clean architecture
- dependency injection where appropriate
- clear interfaces
- sensible error handling

============================================================
DEFAULT DEVELOPMENT PHILOSOPHY
============================================================

The project must run locally without requiring every external service.

Therefore:

LOCAL DEFAULTS
--------------
- SQLite
- in-memory fallback where appropriate
- local vector store
- mock CRM
- mock appointment service
- mock knowledge service
- configurable LLM provider
- optional Redis
- optional RabbitMQ
- optional Neo4j
- optional external voice providers

The README must clearly explain which integrations are:
- required
- optional
- mock/local
- provider-dependent

Never hard-code secrets.

Use:
.env.example

Never commit:
.env

============================================================
ARCHITECTURE
============================================================

Design the platform using these major layers:

1. Channel Layer
2. API Layer
3. Agent Runtime
4. RAG / Knowledge Layer
5. MCP / Tool Layer
6. Memory Layer
7. Guardrails Layer
8. Evaluation Layer
9. Observability Layer
10. Voice Layer
11. Async Processing Layer
12. Persistence Layer

High-level architecture:

USER
  |
  +--> Web Chat
  +--> SMS-style adapter
  +--> WhatsApp-style adapter
  +--> Voice
          |
          v
     Channel Adapter
          |
          v
     Input Guardrail
          |
          v
      Intent Agent
          |
          v
      Agent Router
          |
          +--> FAQ Agent
          |
          +--> RAG Agent
          |
          +--> GraphRAG Agent
          |
          +--> CRM Agent
          |
          +--> Feedback Agent
          |
          +--> Handoff Agent
          |
          v
     Tool / RAG / Memory
          |
          v
          LLM
          |
          v
    Output Guardrail
          |
          v
       Response

The system must preserve agent state and trace important execution steps.

============================================================
AGENT MODEL
============================================================

Create a reusable BaseAgent abstraction.

Each agent should have:
- name
- description
- type
- instructions
- tools
- knowledge sources
- configuration
- state
- execution method
- logging hooks

Agent types:

FAQAgent
RAGAgent
GraphRAGAgent
CRMAgent
FeedbackAgent
HandoffAgent

Also create:
IntentAgent
RouterAgent
InputGuardrailAgent
OutputGuardrailAgent

============================================================
AGENT CONFIGURATION
============================================================

Create a generic configuration model similar to:

Agent
 |
 +-- Identity
 +-- Description
 +-- Instructions
 +-- Connectors
 +-- Knowledge Base
 +-- Settings
 +-- Testing
 +-- Logs

Use Pydantic schemas.

Example AgentConfig:

{
    name,
    agent_type,
    description,
    language,
    conversation_style,
    instructions,
    connectors,
    knowledge_base,
    settings
}

Support configuration-driven behavior.

============================================================
LANGGRAPH
============================================================

Implement the first real workflow using LangGraph.

Create explicit state.

Example state:

ConversationState:
- session_id
- user_id
- channel
- messages
- intent
- selected_agent
- retrieved_context
- selected_tools
- tool_results
- response
- guardrail_results
- metadata

Workflow:

START
  |
  v
input_guardrail
  |
  v
intent_detection
  |
  v
agent_router
  |
  +--> faq_agent
  |
  +--> rag_agent
  |
  +--> graph_rag_agent
  |
  +--> crm_agent
  |
  +--> feedback_agent
  |
  +--> handoff_agent
  |
  v
output_guardrail
  |
  v
END

Use conditional routing in LangGraph.

Design the workflow so it can later support:
- ReAct-style execution
- Plan-and-Execute
- Hierarchical orchestration
- Human approval
- retries
- checkpointing

Do not fake these as completed if not actually implemented.

============================================================
INTENT DETECTION
============================================================

Implement an intent classifier abstraction.

Initial intent categories:

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

Use structured output.

Example:

{
    "intent": "CRM_QUERY",
    "confidence": 0.93,
    "reason": "User requested customer information"
}

Do not expose hidden chain-of-thought.

Store only concise routing metadata.

============================================================
FAQ AGENT
============================================================

Build a working FAQ agent.

It must:
- receive user query
- search configured knowledge
- produce an answer
- pass output through guardrails

============================================================
ADVANCED RAG
============================================================

Build a real modular RAG subsystem.

Pipeline:

DOCUMENT
  |
  v
PARSER
  |
  v
HASH
  |
  v
DEDUPLICATION
  |
  v
CHUNKING
  |
  v
EMBEDDING
  |
  v
VECTOR STORE


QUERY
  |
  v
QUERY REWRITER
  |
  +-------------------+
  |                   |
  v                   v
VECTOR SEARCH       BM25 SEARCH
  |                   |
  +--------+----------+
           |
           v
      RRF FUSION
           |
           v
       RERANKER
           |
           v
        CONTEXT
           |
           v
          LLM
           |
           v
       GROUNDED ANSWER

Implement:
- vector retriever
- BM25 retriever
- hybrid retriever
- RRF
- reranker interface
- cross-encoder implementation where practical
- LLM reranker interface
- query rewriting

============================================================
SELF-RAG / CRAG
============================================================

Design separate strategy modules.

Self-RAG:
- determine whether retrieval is needed
- retrieve when necessary
- inspect answer grounding

CRAG:
- retrieve
- evaluate retrieval quality
- if poor, perform corrective retrieval/rewrite
- regenerate

Do not claim full research-grade Self-RAG if only a simplified implementation exists.

Document exactly what is implemented.

============================================================
CHUNKING
============================================================

Implement a chunking strategy interface.

Strategies:

- Recursive
- Semantic
- Document-Aware
- Proposition
- Late
- Hierarchical
- Agentic

Each strategy must share a common interface.

Example:

ChunkingStrategy.chunk(document)

Create:
ChunkingFactory

Allow configuration:

chunking_strategy=recursive

Do not create fake implementations.

If a strategy is simplified for portfolio purposes, document the simplification.

============================================================
EMBEDDINGS
============================================================

Implement:
EmbeddingProvider interface

Support configurable providers.

Add embedding cache abstraction.

Example:

get_embedding(text)
cache lookup
generate if missing
store result

============================================================
VECTOR STORES
============================================================

Create VectorStore interface.

Adapters:
- Chroma
- FAISS
- Pinecone optional

Use local storage as default.

Do not require paid infrastructure for basic demo.

============================================================
GRAPHRAG
============================================================

Build a genuine GraphRAG module.

Pipeline:

DOCUMENT
   |
   v
ENTITY EXTRACTION
   |
   v
RELATIONSHIP EXTRACTION
   |
   v
GRAPH BUILDER
   |
   v
NEO4J
   |
   v
GRAPH RETRIEVAL
   |
   v
GRAPHRAG AGENT
   |
   v
LLM

Implement:
- entity extraction interface
- relationship extraction interface
- graph builder
- Neo4j repository
- graph retriever
- graph context formatter

Use a simple synthetic domain.

Example:

Customer
 -> owns -> Account
 -> created -> Order
 -> assigned_to -> Agent
 -> booked -> Appointment

GraphRAG queries must demonstrate relationship-aware retrieval.

============================================================
MCP
============================================================

This is a major component.

Build BOTH:

1. MCP client
2. MCP server

Use FastMCP.

The MCP server must expose meaningful tools.

Create tools such as:

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

The tools must operate against a safe mock/local data source.

Architecture:

CRM Agent
   |
   v
MCP Client
   |
   v
MCP Server
   |
   +--> Customer tools
   +--> Lead tools
   +--> Appointment tools
   +--> Knowledge tools
   |
   v
Mock CRM / Local DB

Do not connect to any real employer system.

============================================================
TOOL CALLING
============================================================

Implement structured tool selection.

Example:

User:
"Find John's lead and mark it as qualified."

Flow:

Intent Detection
  |
  v
CRM Agent
  |
  v
Tool Selection
  |
  v
MCP Client
  |
  v
MCP Server
  |
  +--> get_lead
  |
  +--> update_lead
  |
  v
Tool result
  |
  v
LLM
  |
  v
Output Guardrail

Handle:
- invalid arguments
- tool not found
- tool timeout
- tool failure
- malformed tool output

============================================================
CRM DOMAIN
============================================================

Create a safe synthetic CRM model.

Entities:
Customer
Lead
Appointment
Conversation
Agent

Use fake records.

Example:

John Doe
john@example.com
Lead ID: LEAD-1001

No real personal data.

============================================================
MEMORY
============================================================

Implement memory abstraction.

Short-term conversation state:
- current messages
- current workflow state

Long-term:
- conversation summaries
- optional vector memory

Use:
- Redis adapter
- local fallback

Implement conversation summary generation.

Store:
- summary
- key points
- important entities
- latest state

============================================================
HUMAN-IN-THE-LOOP
============================================================

Implement approval points for sensitive actions.

Example:

Agent
 |
 v
Sensitive Action?
 |
 +--> No --> Continue
 |
 +--> Yes
       |
       v
    Pending Approval
       |
       v
 Human Approve / Reject
       |
       v
    Resume Workflow

Use LangGraph-compatible checkpoint/state design.

============================================================
GUARDRAILS
============================================================

Implement:

Input Guardrail
Output Guardrail

Guardrails should have reusable interfaces.

Input checks can include:
- malformed input
- unsafe patterns
- oversized requests

Output checks can include:
- schema validation
- grounding checks
- prohibited output patterns
- missing required information

============================================================
HALLUCINATION DETECTION
============================================================

Implement a practical portfolio-safe hallucination validation pipeline.

Response
   |
   v
Semantic Grounding
   |
   v
Claim Extraction / Decomposition
   |
   v
Claim Validation
   |
   v
LLM-as-a-Judge
   |
   +--> PASS
   |
   +--> FAIL
          |
          v
       Regenerate / Correct

Do not pretend this is mathematically perfect hallucination detection.

Document limitations.

============================================================
STRUCTURED OUTPUTS
============================================================

Use Pydantic for:
- intent
- agent selection
- tool inputs
- tool outputs
- evaluations
- scenario definitions
- voice settings
- guardrail results

============================================================
VOICE AI
============================================================

Voice AI must be a first-class subsystem.

Architecture:

USER SPEECH
   |
   v
STT
   |
   v
Input Guardrail
   |
   v
Intent Agent
   |
   v
Agent Router
   |
   +--> RAG
   +--> GraphRAG
   +--> MCP
   |
   v
LLM
   |
   v
Output Guardrail
   |
   v
TTS
   |
   v
USER AUDIO

Create interfaces:

SpeechToTextProvider
TextToSpeechProvider
VoiceProvider

Support optional adapters for providers such as:
- ElevenLabs
- Gemini

Do not require live paid credentials to run the repository.

============================================================
VOICE FEATURES
============================================================

Implement configuration models for:

- provider
- voice
- language
- conversation style
- maximum call duration
- silence timeout
- thinking sound
- ambient sound
- human transfer
- voicemail detection
- recording disclosure
- pronunciation rules

Create:
voice/settings.py
voice/pronunciation.py
voice/voicemail.py
voice/handoff.py
voice/runtime.py

============================================================
VOICE AGENTS
============================================================

Support several generic agent configurations:

1. Voice Assistant
2. Language Translator
3. Sales Assistant

They can share infrastructure but use different instructions/configuration.

============================================================
VOICE TRANSLATOR
============================================================

Implement a translator flow:

Speech
 |
 v
STT
 |
 v
Language Detection
 |
 v
Translation
 |
 v
TTS
 |
 v
Audio

Allow configurable source/target languages.

============================================================
VOICE SETTINGS
============================================================

Implement runtime settings:

max_call_duration
silence_timeout
thinking_sound
ambient_sound
transfer_to_human
voicemail_detection
recording_disclosure

Enforce settings in the voice runtime where practical.

============================================================
PRONUNCIATION
============================================================

Implement a pronunciation dictionary.

Example:

{
  "Neo4j": "...",
  "OpenAI": "...",
  "domain-specific-term": "..."
}

Apply normalization before TTS.

============================================================
SILENCE HANDLING
============================================================

Implement state transitions for:

ACTIVE
USER_SPEAKING
USER_SILENT
RETRY_PROMPT
TRANSFER
END

============================================================
VOICEMAIL
============================================================

Implement a provider-independent voicemail detection abstraction.

Actions:
- end call
- leave message
- transfer
- flag event

Document that real-world detection depends on telephony/provider integration.

============================================================
LIVE VOICE TESTING
============================================================

Create a simple browser/demo-friendly testing interface if practical.

For local demo:
- microphone input where feasible
- or a simulated audio/text conversation mode
- show conversation transcript
- show call status
- show selected agent
- show tool calls

Do not make this depend on a telecom provider.

============================================================
CHAT
============================================================

Create a simple chat interface or API demonstration.

Minimum:

POST /chat

Input:
{
  "session_id": "...",
  "message": "...",
  "channel": "web"
}

Response:
{
  "response": "...",
  "intent": "...",
  "agent": "...",
  "tools_used": [],
  "trace_id": "..."
}

============================================================
MULTI-CHANNEL
============================================================

Create channel abstractions:

WebChatChannel
SMSChannel
WhatsAppChannel
VoiceChannel

These should normalize messages into a common internal representation.

Do not integrate real telecom systems unless a safe public adapter is available.

============================================================
CONVERSATION SUMMARY
============================================================

Implement:

summarize_conversation()

Output:
- summary
- key points
- entities
- actions
- unresolved items

============================================================
SCENARIO TESTING
============================================================

Build a scenario framework.

Scenario fields:

name
description
input
expected_behavior
success_criteria
tags

Example:

CRM Lead Qualification

Success criteria:
- correct intent
- correct agent
- correct tool
- tool succeeds
- correct state update
- grounded response

============================================================
SCENARIO GENERATION
============================================================

Create a scenario generator abstraction.

It may use an LLM to generate scenarios from:
- agent description
- tools
- instructions
- knowledge base

Generated scenarios must still be validated.

============================================================
RUN ALL SCENARIOS
============================================================

Create a scenario runner:

Scenario Suite
  |
  v
Run All
  |
  v
Execute Agents
  |
  v
Collect Results
  |
  v
Evaluate
  |
  v
Report

Report:
- total
- passed
- failed
- pass rate
- average latency where measured
- tool failures
- guardrail failures

Only report measured values.

============================================================
LLM AS A JUDGE
============================================================

Create evaluation interfaces for:
- response quality
- faithfulness
- relevance
- tool correctness
- workflow completion

Keep judge prompts versioned.

============================================================
RAGAS
============================================================

Integrate RAGAS where practical.

Do not fake metrics.

Provide evaluation scripts and sample datasets.

============================================================
LANGSMITH
============================================================

Add optional LangSmith integration.

Trace:
- workflow
- agents
- retriever
- tool calls
- final response

Make it optional through environment configuration.

============================================================
LANGFUSE
============================================================

Add optional Langfuse integration with equivalent observability concepts.

============================================================
OBSERVABILITY
============================================================

Every important operation should have structured events.

Example:

{
  "trace_id": "...",
  "session_id": "...",
  "agent": "CRM Agent",
  "action": "update_lead",
  "tool": "mcp.update_lead",
  "status": "success"
}

Create reusable event/logging interfaces.

============================================================
ERROR HANDLING
============================================================

Design explicit handling for:

- LLM errors
- invalid model output
- tool errors
- retrieval errors
- vector store errors
- MCP errors
- Neo4j unavailable
- Redis unavailable
- RabbitMQ unavailable
- voice provider unavailable
- timeout
- retryable failure

Use graceful degradation where appropriate.

============================================================
ASYNC DOCUMENT PIPELINE
============================================================

Create:

upload
 ->
hash
 ->
deduplicate
 ->
queue
 ->
RabbitMQ
 ->
Celery
 ->
parse
 ->
chunk
 ->
embed
 ->
store

For basic local development, make it possible to run ingestion synchronously or with local fallback.

============================================================
SEARCH
============================================================

Create a search abstraction supporting:

Vector
BM25
Hybrid
Graph

Do not couple the agent directly to a specific database.

============================================================
API DESIGN
============================================================

Create FastAPI routes.

At minimum:

GET  /health
POST /chat
POST /agents/run
POST /documents/upload
POST /knowledge/search
POST /conversations/summarize
POST /scenarios/run
POST /scenarios/run-all
GET  /agents
GET  /conversations/{id}
POST /mcp/test-tool

Voice APIs:
POST /voice/session
POST /voice/turn
POST /voice/end

These can remain demo-friendly rather than production-public.

============================================================
SECURITY
============================================================

Implement:
- environment-based secrets
- input validation
- Pydantic validation
- no hardcoded secrets
- safe logging
- no customer data
- no credential exposure

Add .env.example.

============================================================
PROJECT CONFIGURATION
============================================================

Create a clean configuration layer.

Example categories:

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

Use sensible defaults.

============================================================
CODE ORGANIZATION
============================================================

Use this approximate structure, but adjust where architecturally appropriate:

app/
  api/
  agents/
  graph/
  llm/
  channels/
  conversations/
  memory/
  rag/
    ingestion/
    chunking/
    embeddings/
    retrieval/
    reranking/
    stores/
  graph_rag/
  mcp/
    client/
    server/
    tools/
  voice/
    stt/
    tts/
    providers/
    runtime/
  guardrails/
  evaluation/
  scenarios/
  observability/
  connectors/
  models/
  config/

tests/
  agents/
  graph/
  rag/
  graph_rag/
  mcp/
  voice/
  guardrails/
  evaluation/
  api/

docs/
  architecture/
  workflows/
  decisions/
  examples/

scripts/
demo/

============================================================
ARCHITECTURE DOCUMENTATION
============================================================

Create diagrams that match the implementation.

Planned:

docs/architecture/
  system-architecture.png
  agent-architecture.png
  rag-pipeline.png
  graph-rag.png
  mcp-architecture.png
  voice-architecture.png
  guardrail-pipeline.png
  evaluation-pipeline.png

For now, create Mermaid source files if image generation is inconvenient:

.mmd files

But never document an architecture that the implementation does not support.

============================================================
README
============================================================

The existing README is already comprehensive.

Update it as implementation progresses.

IMPORTANT:
- do not claim planned features are implemented
- mark completed features with [x]
- mark incomplete features with [ ]
- add actual setup commands
- add screenshots after the application exists
- add real measured evaluation results only
- document limitations
- document optional integrations
- maintain the public-safe disclaimer

Add sections as needed:

- Architecture
- Quick Start
- Demo
- Project Structure
- Agents
- RAG
- GraphRAG
- MCP
- Voice
- Memory
- Guardrails
- Evaluation
- Observability
- Testing
- Docker
- Configuration
- Limitations
- Roadmap

============================================================
DEMO DATA
============================================================

Create synthetic demo data.

Examples:
- customers
- leads
- appointments
- FAQs
- support documents
- relationships

Put safe example data under:

demo/data/

============================================================
DEMO SCENARIOS
============================================================

Create at least these scenarios:

1. FAQ query
2. RAG query
3. GraphRAG relationship query
4. CRM lookup
5. CRM update
6. Appointment lookup
7. Human handoff
8. Guardrail rejection
9. Voice assistant simulation
10. Translation workflow

============================================================
TESTS
============================================================

Write actual tests.

Minimum:
- intent classification schema
- routing
- FAQ agent
- RAG retrieval
- RRF
- reranking interface
- GraphRAG graph lookup
- MCP tools
- CRM tools
- guardrails
- memory
- scenario runner
- API health
- chat endpoint

Mock external dependencies where necessary.

============================================================
DOCKER
============================================================

Create:

Dockerfile
docker-compose.yml

Optional services:
- API
- worker
- Redis
- RabbitMQ
- Neo4j

Do not force every service for basic startup.

Provide:
docker compose up

and also:
local Python startup instructions.

============================================================
DEPENDENCY MANAGEMENT
============================================================

Prefer pyproject.toml over a minimal requirements.txt if appropriate.

Pin compatible versions.

Before adding dependencies:
- inspect the environment
- avoid obsolete packages
- avoid unnecessary dependencies
- verify imports

If a dependency version conflicts:
- resolve it
- do not randomly downgrade unrelated dependencies

============================================================
QUALITY BAR
============================================================

The result must look like code written by a senior AI engineer.

Requirements:
- no giant monolithic file
- no duplicated code
- no fake implementations
- no unexplained magic constants
- no hardcoded credentials
- no TODO-only core functionality
- useful type hints
- meaningful docstrings
- sensible exception handling
- clear module boundaries
- deterministic tests where possible
- reproducible setup

============================================================
GIT WORKFLOW
============================================================

DO NOT push to GitHub automatically.

DO NOT rewrite existing Git history.

DO NOT delete the existing README.

Work locally.

At the end of each major phase:
- run tests
- run lint/type checks where configured
- summarize changes
- show git diff summary
- tell me which files were created
- tell me what is fully implemented vs optional

============================================================
IMPLEMENTATION STRATEGY
============================================================

Do not try to write the entire system blindly in one pass.

Implement in these phases.

PHASE 0 — REPOSITORY INSPECTION
--------------------------------
1. Inspect current repository.
2. Inspect README.
3. Inspect .gitignore.
4. Detect Python version.
5. Detect existing environment.
6. Create a short PLAN.md describing implementation.
7. Check for existing code before creating duplicates.

PHASE 1 — CORE AGENT RUNTIME
----------------------------
Implement:
- config
- schemas
- BaseAgent
- state
- Input Guardrail
- Intent Agent
- Router
- FAQ Agent
- RAG Agent skeleton
- CRM Agent skeleton
- Handoff Agent
- Output Guardrail
- LangGraph workflow
- FastAPI health/chat endpoints
- tests

At the end:
the basic workflow must run locally.

PHASE 2 — REAL RAG
------------------
Implement:
- document model
- parser
- hash
- dedup
- chunking interface
- recursive chunking
- embeddings
- Chroma/FAISS
- vector retrieval
- BM25
- hybrid retrieval
- RRF
- reranking
- query rewriting
- RAG Agent
- tests

At the end:
a document can be indexed and queried.

PHASE 3 — GRAPH RAG
-------------------
Implement:
- entity extraction
- relationship extraction
- graph builder
- Neo4j adapter
- graph retriever
- GraphRAG Agent
- tests

At the end:
a relationship-heavy query can execute against a synthetic graph.

PHASE 4 — MCP
--------------
Implement:
- FastMCP server
- MCP client
- tool schemas
- customer tools
- lead tools
- appointment tools
- knowledge tools
- CRM agent integration
- error handling
- tests

At the end:
a user request can cause an actual MCP tool execution.

PHASE 5 — MEMORY + CONVERSATIONS
---------------------------------
Implement:
- conversation state
- Redis adapter
- local fallback
- checkpoints
- summary generation
- persistent context
- tests

PHASE 6 — GUARDRAILS + RELIABILITY
----------------------------------
Implement:
- semantic grounding
- claim decomposition
- claim validation
- LLM judge
- regeneration logic
- structured outputs
- tests

PHASE 7 — EVALUATION
--------------------
Implement:
- scenario schema
- scenario generator
- runner
- run-all
- success criteria
- evaluation reports
- RAGAS integration
- regression tests

PHASE 8 — OBSERVABILITY
-----------------------
Implement:
- structured events
- trace IDs
- LangSmith adapter
- Langfuse adapter
- agent logs
- tool logs
- retrieval logs

PHASE 9 — VOICE AI
------------------
Implement:
- voice agent schema
- STT abstraction
- TTS abstraction
- provider factory
- voice configuration
- pronunciation
- silence handling
- voicemail handling
- transfer/handoff
- recording disclosure
- live test/demo mode
- translator agent
- sales assistant agent

PHASE 10 — MULTI-CHANNEL
------------------------
Implement:
- common message envelope
- Web Chat adapter
- SMS-style adapter
- WhatsApp-style adapter
- Voice adapter

PHASE 11 — DOCKER / PRODUCTION STRUCTURE
----------------------------------------
Implement:
- Dockerfile
- docker-compose
- worker
- Redis
- RabbitMQ
- Neo4j optional
- environment configuration
- CI-ready project

PHASE 12 — DOCUMENTATION / DEMO
-------------------------------
Implement:
- example data
- demo scripts
- architecture Mermaid diagrams
- screenshots if a demo UI exists
- updated README
- setup instructions
- troubleshooting
- architecture decisions

============================================================
IMPORTANT IMPLEMENTATION RULES
============================================================

RULE 1
------
Never invent that an external provider is working.

If API credentials are missing:
- implement the adapter
- create a mock/local implementation
- document how to enable the real provider

RULE 2
------
Never invent metrics.

Only report:
- measured latency
- measured token usage
- measured retrieval metrics
- measured evaluation results

RULE 3
------
Never hide failures.

If a service is optional, report that clearly.

RULE 4
------
Prefer interfaces and adapters.

For example:

LLMProvider
EmbeddingProvider
VectorStore
VoiceProvider
STTProvider
TTSProvider
MCPTool
MemoryStore
Evaluator

RULE 5
------
Do not expose chain-of-thought.

Store only concise reasoning metadata such as:
- intent
- confidence
- selected agent
- selected tool
- retrieval strategy
- validation result

RULE 6
------
Do not make one giant "agent.py".

Separate agent responsibilities.

RULE 7
------
Do not overengineer with Kubernetes unless there is a real reason.

Docker Compose is sufficient initially.

RULE 8
------
Keep the application runnable with minimal dependencies.

RULE 9
------
Every major implementation must have tests.

RULE 10
-------
Update README status only after functionality actually exists.

============================================================
SUCCESS CRITERIA
============================================================

The project is considered successful when a new developer can:

1. clone the repository
2. create a virtual environment
3. install dependencies
4. configure .env
5. run the application
6. send a chat request
7. observe intent detection
8. observe agent routing
9. execute an RAG query
10. execute a GraphRAG query
11. execute an MCP CRM tool
12. inspect the result
13. run scenario tests
14. view evaluation output
15. optionally run voice simulation
16. understand the architecture from README/docs

============================================================
FINAL DELIVERABLES
============================================================

At completion, the repository should contain:

1. Working Agentic AI runtime
2. Working LangGraph workflow
3. Working specialized agents
4. Working RAG pipeline
5. Working hybrid retrieval
6. Working RRF
7. Working reranking abstraction
8. Working GraphRAG
9. Working Neo4j adapter
10. Working MCP server
11. Working MCP client
12. Working mock CRM tools
13. Working memory
14. Working guardrails
15. Working hallucination validation pipeline
16. Working scenario framework
17. Working evaluation pipeline
18. Optional LangSmith
19. Optional Langfuse
20. RAGAS evaluation
21. Voice abstractions
22. Voice configuration
23. Voice test/simulation
24. Conversation summaries
25. FastAPI API
26. Docker setup
27. Unit tests
28. Integration tests
29. Synthetic demo data
30. Architecture documentation
31. Public-safe README

============================================================
HOW TO WORK
============================================================

Start now.

First inspect the existing repository.

Then create PLAN.md.

Then implement Phase 1 completely.

Do not stop after creating PLAN.md.

Continue implementing phases sequentially.

After each phase:
1. run tests
2. fix failures
3. verify imports
4. check formatting
5. summarize what works
6. continue to the next phase

Do not push to GitHub.

Do not create commits unless I explicitly ask.

At the end of the session provide:

A. Final repository tree
B. Implemented features
C. Optional integrations
D. Remaining limitations
E. Test results
F. How to run locally
G. Environment variables
H. Recommended next manual actions
I. Git diff summary

Most importantly:

Build a REAL, RUNNABLE, PUBLIC-SAFE portfolio project.

Do not optimize for number of files.

Optimize for:
- architecture quality
- correctness
- modularity
- demonstrability
- reproducibility
- interview explainability
- clean code
- realistic AI engineering practices

