"""Application configuration.

One `Settings` object, grouped into sub-models by integration category (LLM, RAG, VECTOR_STORE,
NEO4J, REDIS, RABBITMQ, MCP, VOICE, LANGSMITH, LANGFUSE, EVALUATION), as required by
requirement.md's PROJECT CONFIGURATION section.

Every category has a working local/mock default (`provider="mock"`, `enabled=False`, etc.) so the
application boots and the full LangGraph workflow runs with an empty `.env` file. Real integrations
are opt-in via environment variables — see `.env.example` for the full list and README
"Configuration" for which flags are required vs. optional vs. mock-by-default.

Env vars use `__` as the nested delimiter, e.g. `LLM__PROVIDER=openai` sets `settings.llm.provider`.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LLMSettings(BaseModel):
    """Multi-provider LLM abstraction settings. Default `provider="mock"` needs no API key."""

    provider: str = Field(default="mock", description="mock | openai | anthropic | gemini | groq")
    model: str = Field(
        default="gpt-4o-mini", description="Model name passed to the chosen provider"
    )
    temperature: float = 0.2
    max_tokens: int = 1024
    request_timeout_seconds: float = 30.0
    max_structured_output_retries: int = 2

    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    gemini_api_key: str | None = None
    groq_api_key: str | None = None


class RAGSettings(BaseModel):
    """Retrieval-augmented generation pipeline settings (chunking/embeddings/retrieval/reranking)."""

    chunking_strategy: str = Field(
        default="recursive",
        description="recursive | semantic | document_aware | proposition | late | hierarchical | agentic",
    )
    chunk_size: int = 800
    chunk_overlap: int = 100
    top_k: int = 5
    candidate_k: int = Field(
        default=20, description="How many candidates each retriever returns before RRF/rerank"
    )
    rrf_k: int = Field(
        default=60, description="RRF's rank-damping constant — 60 is the standard default"
    )
    hybrid_vector_weight: float = Field(
        default=0.5,
        description="Weight given to vector-search ranks vs. BM25 ranks in weighted RRF",
    )
    reranker: str = Field(default="none", description="none | cross_encoder | llm")
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    query_rewriting_enabled: bool = False
    embedding_provider: str = Field(
        default="sentence_transformers", description="sentence_transformers | openai"
    )
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_cache_persistent: bool = False
    self_rag_grounding_threshold: float = Field(
        default=0.3,
        description="Below this word-overlap ratio, Self-RAG treats an answer as ungrounded",
    )
    crag_quality_threshold: float = Field(
        default=0.35,
        description="Below this top-hit RRF score, CRAG treats retrieval as poor and corrects",
    )


class VectorStoreSettings(BaseModel):
    """Vector store adapter settings. Local persistence by default — no paid service required."""

    provider: str = Field(default="chroma", description="chroma | faiss | pinecone")
    persist_dir: str = str(BASE_DIR / "data" / "chroma")
    collection_name: str = "agentic_ai_platform"
    pinecone_api_key: str | None = None
    pinecone_environment: str | None = None
    pinecone_index: str | None = None


class Neo4jSettings(BaseModel):
    """GraphRAG store. Disabled by default; an in-memory graph fallback is used instead."""

    enabled: bool = False
    uri: str = "bolt://localhost:7687"
    user: str = "neo4j"
    password: str | None = None
    database: str = "neo4j"


class RedisSettings(BaseModel):
    """Cross-session memory / cache backend. Disabled by default; falls back to in-memory."""

    enabled: bool = False
    url: str = "redis://localhost:6379/0"
    key_prefix: str = "agentic-ai-platform"


class RabbitMQSettings(BaseModel):
    """Async document pipeline broker. Disabled by default; ingestion runs synchronously instead."""

    enabled: bool = False
    url: str = "amqp://guest:guest@localhost:5672/"
    ingestion_queue: str = "document-ingestion"


class MCPSettings(BaseModel):
    """MCP client/server settings for the CRM tool layer."""

    server_host: str = "127.0.0.1"
    server_port: int = 8765
    tool_timeout_seconds: float = 10.0


class VoiceSettings(BaseModel):
    """Voice provider abstraction. `provider="mock"` needs no telephony/voice API key."""

    provider: str = Field(default="mock", description="mock | elevenlabs | gemini")
    elevenlabs_api_key: str | None = None
    gemini_api_key: str | None = None
    default_language: str = "en-US"
    max_call_duration_seconds: int = 900
    silence_timeout_seconds: int = 10


class LangSmithSettings(BaseModel):
    """Optional LangSmith tracing. Off by default."""

    enabled: bool = False
    api_key: str | None = None
    project: str = "agentic-ai-platform"
    endpoint: str = "https://api.smith.langchain.com"


class LangfuseSettings(BaseModel):
    """Optional Langfuse tracing. Off by default."""

    enabled: bool = False
    public_key: str | None = None
    secret_key: str | None = None
    host: str = "https://cloud.langfuse.com"


class EvaluationSettings(BaseModel):
    """Scenario / RAGAS evaluation settings."""

    ragas_enabled: bool = False
    judge_model: str | None = None
    scenarios_dir: str = str(BASE_DIR / "demo" / "scenarios")


class Settings(BaseSettings):
    """Root settings object. Construct via `get_settings()`, not directly, outside of tests."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="local", description="local | test | staging | production")
    debug: bool = True
    log_level: str = "INFO"
    api_title: str = "Agentic AI Platform (Portfolio)"
    api_cors_origins: list[str] = ["*"]
    database_url: str = f"sqlite:///{BASE_DIR / 'data' / 'app.db'}"

    llm: LLMSettings = Field(default_factory=LLMSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
    neo4j: Neo4jSettings = Field(default_factory=Neo4jSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    voice: VoiceSettings = Field(default_factory=VoiceSettings)
    langsmith: LangSmithSettings = Field(default_factory=LangSmithSettings)
    langfuse: LangfuseSettings = Field(default_factory=LangfuseSettings)
    evaluation: EvaluationSettings = Field(default_factory=EvaluationSettings)


@lru_cache
def get_settings() -> Settings:
    """Process-wide cached settings singleton. Tests override via `get_settings.cache_clear()`."""

    return Settings()
