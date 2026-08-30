"""Optional, real integration test for `Neo4jGraphRepository` — skipped automatically unless a
Neo4j server is actually reachable at `NEO4J_TEST_URI` (default `bolt://localhost:7687`) with
`NEO4J_TEST_PASSWORD` (default `testpassword`).

This is deliberately NOT part of the required test suite (requirement.md: the app and its tests
must run without every external service) — but it does exist and does pass against a real server,
which is how the Neo4j adapter was actually verified during development (see PLAN.md §3c). Run it
locally with, e.g.:

    docker run -d --rm --name neo4j-test -p 7687:7687 \\
        -e NEO4J_AUTH=neo4j/testpassword -e NEO4J_PLUGINS='[]' neo4j:5
    pytest tests/graph_rag/test_neo4j_repository.py -v
"""

import os

import pytest

_URI = os.environ.get("NEO4J_TEST_URI", "bolt://localhost:7687")
_PASSWORD = os.environ.get("NEO4J_TEST_PASSWORD", "testpassword")


def _neo4j_reachable() -> bool:
    try:
        from neo4j import GraphDatabase

        driver = GraphDatabase.driver(_URI, auth=("neo4j", _PASSWORD))
        driver.verify_connectivity()
        driver.close()
        return True
    except Exception:  # noqa: BLE001 - any failure means "not reachable", not a test error
        return False


pytestmark = pytest.mark.skipif(not _neo4j_reachable(), reason=f"No Neo4j reachable at {_URI}")


@pytest.fixture
def neo4j_repository():
    from app.graph_rag.neo4j_repository import Neo4jGraphRepository

    repository = Neo4jGraphRepository(uri=_URI, user="neo4j", password=_PASSWORD)
    yield repository
    # Clean up this test's data so repeated runs stay idempotent.
    repository._driver.execute_query(
        "MATCH (n:Entity) DETACH DELETE n", database_=repository._database
    )
    repository.close()


def test_upsert_and_get_entity(neo4j_repository):
    from app.models.graph_rag import GraphEntity

    entity = GraphEntity(id="customer:test-user", name="Test User", entity_type="Customer")
    neo4j_repository.upsert_entity(entity)

    fetched = neo4j_repository.get_entity("customer:test-user")
    assert fetched == entity


def test_upsert_relationship_and_traverse(neo4j_repository):
    from app.models.graph_rag import GraphEntity, GraphRelationship

    customer = GraphEntity(id="customer:test-user", name="Test User", entity_type="Customer")
    agent = GraphEntity(id="agent:test-agent", name="Test Agent", entity_type="Agent")
    neo4j_repository.upsert_entity(customer)
    neo4j_repository.upsert_entity(agent)
    neo4j_repository.upsert_relationship(
        GraphRelationship(
            source_id=customer.id, target_id=agent.id, relationship_type="ASSIGNED_TO"
        )
    )

    edges = neo4j_repository.outgoing(customer.id)
    assert len(edges) == 1
    relationship, target = edges[0]
    assert relationship.relationship_type == "ASSIGNED_TO"
    assert target == agent


def test_find_entities_by_name_case_insensitive(neo4j_repository):
    from app.models.graph_rag import GraphEntity

    neo4j_repository.upsert_entity(
        GraphEntity(id="customer:abc", name="Abc De", entity_type="Customer")
    )
    matches = neo4j_repository.find_entities_by_name("abc de")
    assert len(matches) == 1


def test_counts_reflect_stored_graph(neo4j_repository):
    from app.models.graph_rag import GraphEntity, GraphRelationship

    a = GraphEntity(id="customer:a", name="A", entity_type="Customer")
    b = GraphEntity(id="agent:b", name="B", entity_type="Agent")
    neo4j_repository.upsert_entity(a)
    neo4j_repository.upsert_entity(b)
    neo4j_repository.upsert_relationship(
        GraphRelationship(source_id=a.id, target_id=b.id, relationship_type="OWNS")
    )

    counts = neo4j_repository.counts()
    assert counts["entities"] == 2
    assert counts["relationships"] == 1


def test_rejects_unsafe_relationship_type(neo4j_repository):
    from app.models.graph_rag import GraphEntity, GraphRelationship

    a = GraphEntity(id="customer:a", name="A", entity_type="Customer")
    b = GraphEntity(id="agent:b", name="B", entity_type="Agent")
    neo4j_repository.upsert_entity(a)
    neo4j_repository.upsert_entity(b)

    with pytest.raises(ValueError):
        neo4j_repository.upsert_relationship(
            GraphRelationship(
                source_id=a.id, target_id=b.id, relationship_type="OWNS} DETACH DELETE (a"
            )
        )
