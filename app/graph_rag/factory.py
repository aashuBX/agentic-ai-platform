"""Builds the configured `GraphRepository`: Neo4j if enabled and reachable, otherwise the
in-memory fallback — requirement.md's TECHNOLOGY PREFERENCES: "local/mock fallback when Neo4j is
unavailable," and the ERROR HANDLING section's "Neo4j unavailable" case. A misconfigured or
unreachable Neo4j must degrade gracefully, never crash app startup.
"""

from app.config.settings import Neo4jSettings
from app.graph_rag.memory_repository import InMemoryGraphRepository
from app.graph_rag.repository import GraphRepository
from app.observability import get_logger

_logger = get_logger("agentic_ai_platform.graph_rag")


def build_graph_repository(settings: Neo4jSettings) -> GraphRepository:
    if not settings.enabled:
        _logger.info(
            "graph_repository_using_in_memory_fallback",
            extra={"event_data": {"reason": "neo4j_disabled"}},
        )
        return InMemoryGraphRepository()

    try:
        from app.graph_rag.neo4j_repository import Neo4jGraphRepository

        repository = Neo4jGraphRepository(
            uri=settings.uri,
            user=settings.user,
            password=settings.password,
            database=settings.database,
        )
        _logger.info("graph_repository_using_neo4j", extra={"event_data": {"uri": settings.uri}})
        return repository
    except Exception as exc:  # noqa: BLE001 - any Neo4j failure must fall back, never crash startup
        _logger.warning(
            "graph_repository_falling_back_to_in_memory", extra={"event_data": {"reason": str(exc)}}
        )
        return InMemoryGraphRepository()
