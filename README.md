
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

## 🎯 Project Overview

This repository is an **independent, public implementation of an enterprise-oriented Conversational Agentic AI platform**.

The platform demonstrates how modern Generative AI applications can combine:

- Multi-Agent orchestration
- LangGraph stateful workflows
- Intent detection and intelligent routing
- Chat-based AI agents
- Voice-based AI agents
- Advanced RAG
- Self-RAG
- Corrective RAG (CRAG)
- GraphRAG
- Hybrid retrieval
- Vector + BM25 + Knowledge Graph retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder / LLM reranking
- MCP client/server architecture
- AI tool calling
- CRM-style automation
- Conversation memory
- Cross-session context
- Input / output guardrails
- Hallucination detection
- Semantic grounding
- LLM-as-a-Judge
- Human-in-the-Loop workflows
- Intelligent document ingestion
- Multi-strategy document chunking
- Embedding pipelines
- Vector databases
- Knowledge graphs
- Voice AI pipelines
- Speech-to-Text / Text-to-Speech
- Voice provider abstraction
- Voice configuration
- Scenario-based agent testing
- RAGAS evaluation
- LangSmith / Langfuse observability
- Agent logs and execution traces
- Python backend services
- Redis, RabbitMQ and Celery
- Docker and cloud-ready deployment

The goal is to demonstrate an AI system that can:

```text
Understand
    ↓
Reason
    ↓
Retrieve Knowledge
    ↓
Select Agent
    ↓
Select Tools
    ↓
Execute Actions
    ↓
Validate
    ↓
Evaluate
    ↓
Respond


🏗️ End-to-End Architecture

                                      ┌──────────────────────┐
                                      │       USER           │
                                      │                      │
                                      │ Web / SMS / WhatsApp │
                                      │        / Voice       │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  CHANNEL ADAPTERS    │
                                      │ Chat / Messaging     │
                                      │ Voice / WebSocket    │
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
             │                    │             │             │               ┌──────────────┐
             │                    ▼             ▼             ▼               │  MCP SERVER  │
             │                 Vector         BM25          Graph             └──────┬───────┘
             │                 Search        Search       Retrieval                   │
             │                    │             │             │                         │
             │                    └─────────────┼─────────────┘                         │
             │                                  ▼                                       │
             │                                 RRF                                      │
             │                                  │                                       │
             │                             Reranking                                    │
             │                                  │                                       │
             └──────────────────────────────────┼───────────────────────────────────────┘
                                                │
                                                ▼
                                         ┌──────────────┐
                                         │     LLM      │
                                         └──────┬───────┘
                                                │
                                                ▼
                                      ┌──────────────────────┐
                                      │  OUTPUT GUARDRAIL    │
                                      └──────────┬───────────┘
                                                 │
                                                 ▼
                                          FINAL RESPONSE


🤖 Agentic AI Layer

The platform uses specialized agents rather than relying on a single monolithic agent.

Core orchestration concepts:

LangGraph
LangChain
Multi-Agent Orchestration
Intent Detection
Agent Routing
ReAct
Plan-and-Execute
Hierarchical Agent Graphs
Stateful Agent Workflows
Inter-Agent Delegation
A2A-style task delegation
Human-in-the-Loop
Checkpointed execution
Specialized Agents

Input Guardrail Agent
        ↓
Validate / filter incoming request

Intent Agent
        ↓
Understand and classify the request

Agent Router
        ↓
Select specialized agent

FAQ Agent
        ↓
Handle knowledge-oriented questions

RAG Agent
        ↓
Retrieve grounded information

GraphRAG Agent
        ↓
Handle relationship / multi-hop queries

CRM Agent
        ↓
Interact with business tools

Feedback Agent
        ↓
Process feedback workflows

Handoff Agent
        ↓
Transfer to human assistance

Output Guardrail
        ↓
Validate final response


🔀 Intent Detection & Agent Routing

                    USER REQUEST
                          │
                          ▼
                   Intent Detection
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
    Knowledge            CRM              Support
       │                  │                  │
       ▼                  ▼                  ▼
    RAG Agent          CRM Agent       Handoff Agent


🔎 Advanced RAG

The RAG subsystem is designed beyond simple vector similarity search.

Supported retrieval approaches:

Vector Retrieval
Semantic Search
BM25
Hybrid Retrieval
Self-RAG
Corrective RAG (CRAG)
GraphRAG
Query Rewriting
Reciprocal Rank Fusion
Cross-Encoder Reranking
LLM Reranking
Semantic Caching
Hybrid Retrieval


                         USER QUERY
                              │
                              ▼
                       Query Rewriter
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
          Vector Search     BM25         Graph Search
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                             RRF
                              │
                              ▼
                         Candidate Set
                              │
                              ▼
                     Cross-Encoder Reranker
                              │
                              ▼
                         Top Context
                              │
                              ▼
                             LLM
                              │
                              ▼
                     Grounded Response


🕸️ GraphRAG & Knowledge Graph

Documents
    │
    ▼
Entity Extraction
    │
    ▼
Relationship Extraction
    │
    ▼
Knowledge Graph
    │
    ▼
Neo4j
    │
    ▼
Graph Retrieval
    │
    ▼
GraphRAG Agent
    │
    ▼
LLM


GraphRAG is intended for:

Entity-centric questions
Relationship queries
Multi-hop retrieval
Connected knowledge
Knowledge graph reasoning

📚 Vector Databases & Search

Supported technologies include:

Pinecone
ChromaDB
FAISS
Qdrant
Elasticsearch
Neo4j
Sentence Transformers
📄 Intelligent Document Processing

The ingestion pipeline transforms raw documents into searchable AI knowledge.

Document Upload
      │
      ▼
   File Hash
      │
      ▼
Duplicate Detection
      │
      ▼
   Event / Queue
      │
      ▼
RabbitMQ
      │
      ▼
Celery Worker
      │
      ▼
Document Parser
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Embedding Cache
      │
      ▼
Vector / Graph Store
      │
      ▼
Knowledge Layer


Multi-Strategy Chunking

Recursive
Semantic
Document-Aware
Proposition
Late
Hierarchical
Agentic

🔌 MCP — Model Context Protocol

MCP acts as the tool integration layer between agents and external capabilities.

                     AI AGENT
                         │
                         ▼
                    MCP CLIENT
                         │
                         ▼
                    MCP SERVER
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        CRM Tools    Search Tools   Data Tools
            │            │            │
            ▼            ▼            ▼
          CRM/API     Knowledge     Services
                         System


Example MCP Tools

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
get_document()

MCP Execution Flow

User Request
     ↓
Intent Detection
     ↓
CRM Agent
     ↓
Tool Selection
     ↓
MCP Client
     ↓
MCP Server
     ↓
Tool Execution
     ↓
Tool Result
     ↓
Agent
     ↓
LLM
     ↓
Final Response

🧠 Multi-Model LLM Layer

The platform uses an abstraction layer so agents can work with different model providers.

Supported providers:

OpenAI
Anthropic
Google Gemini

                    Agent
                      │
                      ▼
                LLM Provider
                   Factory
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
    OpenAI        Anthropic       Gemini


💬 Conversational AI

The platform is designed for multiple conversational channels.

                 Conversational AI
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Web Chat         SMS         WhatsApp
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  Agent Runtime

The same orchestration layer can be reused across communication channels.

📞 Voice AI

Voice agents are treated as first-class AI agents.

User Speech
     │
     ▼
Speech-to-Text
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
     ├──────────► RAG
     │
     ├──────────► GraphRAG
     │
     └──────────► MCP / Tools
                    │
                    ▼
                   LLM
                    │
                    ▼
              Output Guardrail
                    │
                    ▼
              Text-to-Speech
                    │
                    ▼
               User Voice


Voice capabilities
  Speech-to-Text
  Text-to-Speech
  Voice provider abstraction
  Voice selection
  Pronunciation rules
  Silence timeout
  Maximum call duration
  Thinking sound
  Ambient sound
  Human transfer
  Voicemail detection
  Recording disclosure
  Live call testing

🔊 Voice Provider Architecture

                      Voice Agent
                           │
                           ▼
                    Voice Provider
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
           ElevenLabs               Gemini

Providers are accessed through a common abstraction.

⚙️ Voice Configuration

Example:
voice:
  provider: gemini
  language: en-US
  max_call_duration: 900
  silence_timeout: 10
  thinking_sound: true
  ambient_sound: true
  transfer_to_human: true
  voicemail_detection: true
  recording_disclosure: true

🗣️ Pronunciation Management

Domain-specific pronunciation rules can be applied before text is sent to the TTS engine.

Term
 ↓
Pronunciation Rule
 ↓
Voice Provider
 ↓
Natural Speech


📵 Silence & Voicemail Handling

Active Call
    │
    ▼
Silence Detection
    │
    ├── User Responds
    │       ↓
    │   Continue Call
    │
    └── Silence Threshold
            ↓
       Handle Silence

Voicemail:
Call
 ↓
Voicemail Detection
 ↓
Configured Action
 ├── End Call
 ├── Leave Message
 └── Transfer / Escalate

📝 Conversation Management

Conversation history can be summarized into structured information.

Conversation
     ↓
Message History
     ↓
Summary Model
     ↓
Key Discussion Points
     ↓
Structured Summary
     ↓
Conversation State


💾 Memory & Stateful Agents

Conversation
      │
      ▼
   Agent State
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
Redis Vector      Checkpoint
     Memory          │
       │             │
       └──────┬──────┘
              ▼
        Context Retrieval


Memory concepts:

Short-term conversation state
Cross-session memory
Retrieval-based memory
Redis-backed context
FAISS
Qdrant


LangGraph checkpointing
🛡️ AI Guardrails
Input Guardrail


Input Guardrail
User Input
    ↓
Validation
    ↓
Safety / Policy Check
    ↓
Approved Request
Output Guardrail
LLM Response
    ↓
Validation
    ↓
Grounding Check
    ↓
Safe Response
🚨 Hallucination Detection
                        LLM RESPONSE
                             │
                             ▼
                    Semantic Grounding
                             │
                             ▼
                      LLM-as-a-Judge
                             │
                             ▼
                     Claim Decomposition
                             │
                             ▼
                       Claim Validation
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
               PASS                    FAIL
                 │                       │
                 ▼                       ▼
             Response              Regenerate /
                                    Correct
🧱 Structured Outputs
LLM
 ↓
Structured Output
 ↓
Pydantic Model
 ↓
Validation
 ↓
Accepted / Rejected

This provides predictable contracts for downstream processing and tool execution.

👨‍💼 Human-in-the-Loop

Sensitive workflows can pause for human approval.

Agent
  ↓
Decision
  ↓
Approval Required?
  │
 ┌┴──────────────┐
 ▼               ▼
No              Yes
 │                │
 ▼                ▼
Continue       Human Review
                 │
            ┌────┴────┐
            ▼         ▼
         Approve     Reject
            │
            ▼
          Resume



🔗 Connector Architecture

Enterprise capabilities are exposed through reusable connectors/tools.

                      AI AGENT
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Lead Mgmt      Customer Data   Appointment
         Tools           Tools          Tools
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Enterprise APIs

Example capabilities:

Lead Management
Customer / Account Records
Appointment Management
Guided Scheduling
Knowledge Search
🧪 Agent Testing & Scenario Framework

AI agents are tested using reproducible scenarios.

                    AGENT
                      │
                      ▼
                Test Scenario
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Happy Path   Edge Case   Failure Case
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Run Scenario
                      │
                      ▼
                Success Criteria
                      │
                      ▼
                  Evaluation
Scenario Definition
name: CRM Lead Qualification

description: >
  Verify that the agent can identify a lead,
  collect required information and update CRM state.

success_criteria:
  - Correct intent detected
  - Correct agent selected
  - Required fields collected
  - Correct MCP tool selected
  - Tool execution succeeds
  - Final response is grounded
▶️ Scenario Execution
Scenario Suite
      ↓
Run All Scenarios
      ↓
Agent Execution
      ↓
Tool / RAG / Guardrail Checks
      ↓
Success Criteria
      ↓
Evaluation Report
📊 LLMOps & Observability

The platform is designed to make AI execution observable.

Tracing
LangSmith
Langfuse
Evaluation
RAGAS
Example trace information
Trace ID
Agent
Intent
Model
Prompt Version
Retrieved Documents
Selected Tool
Tool Result
Latency
Token Usage
Guardrail Result
Evaluation Result
Final Response
📈 AI Evaluation

Evaluation dimensions include:

RAG
Faithfulness
Answer Relevancy
Context Precision
Context Recall
Retrieval Quality
Agents
Intent classification
Routing accuracy
Agent behavior
Workflow completion
Tools
Tool selection
Argument validity
Tool execution success
Reliability
Grounding
Hallucination detection
Guardrail behavior
Performance
Latency
Token usage
🧠 Prompt Engineering

The platform supports:

Chain-of-Thought
Self-Consistency
Tree-of-Thought
Context-aware prompts
Agent system instructions
Response guidelines
Inbound guidelines
Outbound guidelines
Prompt versioning
Structured output
Pydantic schemas
📱 Agent Configuration

Agents can be represented through configuration rather than being completely hard-coded.

Agent
 │
 ├── Identity
 │
 ├── Description
 │
 ├── Instructions
 │
 ├── Connectors
 │
 ├── Knowledge Base
 │
 ├── Settings
 │
 ├── Testing
 │
 └── Logs
⚙️ Backend Architecture

FastAPI exposes APIs for the platform.

FastAPI
   │
   ├── Agent APIs
   ├── Conversation APIs
   ├── Knowledge APIs
   ├── RAG APIs
   ├── MCP APIs
   ├── Voice APIs
   └── Evaluation APIs

Supporting services:

Python
FastAPI
Redis
RabbitMQ
Celery
Elasticsearch
WebSockets
Docker
🔄 Asynchronous Processing
API Request
    │
    ▼
Message / Task Queue
    │
    ▼
RabbitMQ
    │
    ▼
Celery Worker
    │
    ├── Document Processing
    ├── Embeddings
    ├── Summaries
    ├── Evaluation
    └── Background Tasks
⚡ Redis Usage

Redis can support:

Conversation state
Semantic caching
Embedding caching
Temporary workflow state
Frequently accessed data
Request
  ↓
Cache Lookup
  ├── HIT  → Return / Continue
  │
  └── MISS → Compute → Store
🔎 Search & Analytics

Elasticsearch-based search and analytics can be integrated for operational visibility.

Application
    ↓
Logs / Events
    ↓
Elasticsearch
    ↓
Logstash
    ↓
Kibana
    ↓
Dashboards / Analysis
🐳 Containerized Deployment
                    Docker
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   API Service    Worker Service   MCP Server
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
                Infrastructure
☁️ Production Cloud Architecture
CloudFront
    ↓
Application / API
    ↓
ECS / EC2
    ↓
┌─────────────┬───────────────┬───────────────┐
│             │               │
Redis       RabbitMQ       Databases
│             │               │
│          Workers            │
│             │               │
└─────────────┼───────────────┘
              │
              ▼
          S3 / Storage
