"""FastAPI dependency-injection helpers — read the shared runtime objects off `app.state`."""

from fastapi import Request
from langgraph.graph.state import CompiledStateGraph

from app.agents.registry import AgentRegistry
from app.config.settings import Settings
from app.rag.pipeline import RAGPipeline


def get_settings_dep(request: Request) -> Settings:
    return request.app.state.settings


def get_agent_registry(request: Request) -> AgentRegistry:
    return request.app.state.agent_registry


def get_graph(request: Request) -> CompiledStateGraph:
    return request.app.state.graph


def get_rag_pipeline(request: Request) -> RAGPipeline:
    return request.app.state.rag_pipeline
