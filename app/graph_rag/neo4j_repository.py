"""Neo4j graph repository — the real adapter.

Verified against neo4j==6.2.0's driver API (`Driver.execute_query`, `EagerResult.records`) in this
repo's dev environment, including a live round-trip against a temporary local Neo4j container (see
PLAN.md) — this is not just implemented-but-unverified the way the Pinecone adapter is.

Cypher doesn't support parameterized relationship *types* (only property values), so relationship
type names are interpolated into the query string directly — safe here because
`_SAFE_RELATIONSHIP_TYPE` validates them against a strict allowlist pattern before interpolation;
they never come from raw user input, only from this repo's own extractors.
"""

import re

from app.graph_rag.repository import GraphRepository
from app.models.graph_rag import GraphEntity, GraphRelationship

_SAFE_RELATIONSHIP_TYPE = re.compile(r"^[A-Z_]+$")


def _require_safe_relationship_type(relationship_type: str) -> str:
    if not _SAFE_RELATIONSHIP_TYPE.match(relationship_type):
        raise ValueError(
            f"Unsafe relationship_type for Cypher interpolation: {relationship_type!r} "
            "(expected upper-snake-case, e.g. 'ASSIGNED_TO')"
        )
    return relationship_type


class Neo4jGraphRepository(GraphRepository):
    def __init__(self, uri: str, user: str, password: str | None, database: str = "neo4j") -> None:
        try:
            from neo4j import GraphDatabase
        except ImportError as exc:
            raise ImportError(
                'Neo4j support requires the "neo4j" package: pip install neo4j'
            ) from exc

        self._driver = GraphDatabase.driver(uri, auth=(user, password or ""))
        self._driver.verify_connectivity()
        self._database = database
        self._driver.execute_query(
            "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE",
            database_=self._database,
        )

    def upsert_entity(self, entity: GraphEntity) -> None:
        self._driver.execute_query(
            "MERGE (n:Entity {id: $id}) SET n.name = $name, n.entity_type = $entity_type",
            id=entity.id,
            name=entity.name,
            entity_type=entity.entity_type,
            database_=self._database,
        )

    def upsert_relationship(self, relationship: GraphRelationship) -> None:
        relationship_type = _require_safe_relationship_type(relationship.relationship_type)
        query = (
            "MATCH (a:Entity {id: $source_id}), (b:Entity {id: $target_id}) "
            f"MERGE (a)-[:{relationship_type}]->(b)"
        )
        self._driver.execute_query(
            query,
            source_id=relationship.source_id,
            target_id=relationship.target_id,
            database_=self._database,
        )

    def get_entity(self, entity_id: str) -> GraphEntity | None:
        result = self._driver.execute_query(
            "MATCH (n:Entity {id: $id}) RETURN n.id AS id, n.name AS name, n.entity_type AS entity_type",
            id=entity_id,
            database_=self._database,
        )
        if not result.records:
            return None
        record = result.records[0]
        return GraphEntity(id=record["id"], name=record["name"], entity_type=record["entity_type"])

    def find_entities_by_name(self, name: str) -> list[GraphEntity]:
        result = self._driver.execute_query(
            "MATCH (n:Entity) WHERE toLower(n.name) = toLower($name) "
            "RETURN n.id AS id, n.name AS name, n.entity_type AS entity_type",
            name=name,
            database_=self._database,
        )
        return [
            GraphEntity(id=r["id"], name=r["name"], entity_type=r["entity_type"])
            for r in result.records
        ]

    def outgoing(
        self, entity_id: str, relationship_type: str | None = None
    ) -> list[tuple[GraphRelationship, GraphEntity]]:
        if relationship_type:
            relationship_type = _require_safe_relationship_type(relationship_type)
            query = (
                f"MATCH (a:Entity {{id: $id}})-[r:{relationship_type}]->(b:Entity) "
                "RETURN type(r) AS rel_type, b.id AS id, b.name AS name, b.entity_type AS entity_type"
            )
        else:
            query = (
                "MATCH (a:Entity {id: $id})-[r]->(b:Entity) "
                "RETURN type(r) AS rel_type, b.id AS id, b.name AS name, b.entity_type AS entity_type"
            )
        result = self._driver.execute_query(query, id=entity_id, database_=self._database)

        results: list[tuple[GraphRelationship, GraphEntity]] = []
        for record in result.records:
            target = GraphEntity(
                id=record["id"], name=record["name"], entity_type=record["entity_type"]
            )
            relationship = GraphRelationship(
                source_id=entity_id, target_id=target.id, relationship_type=record["rel_type"]
            )
            results.append((relationship, target))
        return results

    def counts(self) -> dict[str, int]:
        entity_result = self._driver.execute_query(
            "MATCH (n:Entity) RETURN count(n) AS c", database_=self._database
        )
        relationship_result = self._driver.execute_query(
            "MATCH ()-[r]->() RETURN count(r) AS c", database_=self._database
        )
        return {
            "entities": entity_result.records[0]["c"],
            "relationships": relationship_result.records[0]["c"],
        }

    def close(self) -> None:
        self._driver.close()
