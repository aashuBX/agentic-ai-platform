"""`build_graph_repository` must never crash app startup, whether Neo4j is deliberately disabled
or enabled-but-unreachable (requirement.md ERROR HANDLING: "Neo4j unavailable")."""

from app.config.settings import Neo4jSettings
from app.graph_rag.factory import build_graph_repository
from app.graph_rag.memory_repository import InMemoryGraphRepository


def test_disabled_neo4j_uses_in_memory_fallback():
    repository = build_graph_repository(Neo4jSettings(enabled=False))
    assert isinstance(repository, InMemoryGraphRepository)


def test_unreachable_neo4j_falls_back_gracefully():
    settings = Neo4jSettings(
        enabled=True, uri="bolt://localhost:1", user="neo4j", password="wrong-password"
    )
    repository = build_graph_repository(settings)
    assert isinstance(repository, InMemoryGraphRepository)
