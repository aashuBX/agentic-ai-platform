"""FastAPI application factory.

Builds one `LLMProvider`, one `AgentRegistry`, and one compiled LangGraph workflow at startup and
shares them across requests via `app.state` — see `app/api/deps.py` for how routes access them.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents.registry import AgentRegistry
from app.config import get_settings
from app.graph.workflow import build_workflow
from app.graph_rag.builder import GraphBuilder
from app.graph_rag.entities import RegexEntityExtractor
from app.graph_rag.factory import build_graph_repository
from app.graph_rag.relationships import RegexRelationshipExtractor
from app.graph_rag.retriever import GraphRetriever
from app.graph_rag.seed import seed_demo_graph
from app.llm.factory import build_llm_provider
from app.observability import configure_logging, get_logger
from app.rag.factory import build_rag_pipeline
from app.rag.seed import seed_demo_knowledge

logger = get_logger("agentic_ai_platform.api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)

    llm = build_llm_provider(settings.llm)

    rag_pipeline = build_rag_pipeline(settings, llm)
    seed_demo_knowledge(rag_pipeline)

    graph_repository = build_graph_repository(settings.neo4j)
    graph_builder = GraphBuilder(
        RegexEntityExtractor(), RegexRelationshipExtractor(), graph_repository
    )
    graph_seed_counts = seed_demo_graph(graph_builder)
    graph_retriever = GraphRetriever(graph_repository)

    registry = AgentRegistry(llm=llm, rag_pipeline=rag_pipeline, graph_retriever=graph_retriever)

    app.state.settings = settings
    app.state.llm = llm
    app.state.rag_pipeline = rag_pipeline
    app.state.graph_repository = graph_repository
    app.state.agent_registry = registry
    app.state.graph = build_workflow(registry)

    logger.info(
        "startup_complete",
        extra={
            "event_data": {
                "llm_provider": llm.name,
                "app_env": settings.app_env,
                "rag_stats": rag_pipeline.stats(),
                "graph_repository": graph_repository.__class__.__name__,
                "graph_stats": graph_repository.counts(),
                "graph_seed_counts": graph_seed_counts,
            }
        },
    )
    yield
    graph_repository.close()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.api_title,
        description=(
            "Independent, public-safe portfolio implementation of an enterprise conversational "
            "agentic AI platform. See README.md for the public-safe disclaimer and implementation status."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes import agents, chat, documents, health, knowledge

    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(agents.router)
    app.include_router(documents.router)
    app.include_router(knowledge.router)
    return app


app = create_app()
