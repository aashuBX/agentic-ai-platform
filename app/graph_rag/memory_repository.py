"""In-memory graph repository — the fallback when Neo4j is disabled or unreachable.

A real (if simple) adjacency-list graph store: entities and relationships genuinely round-trip and
support traversal via `outgoing()`. It just doesn't persist across process restarts or scale past
what fits in memory — acceptable at this repo's demo scale, and exactly the "local/mock fallback
when Neo4j is unavailable" requirement.md's TECHNOLOGY PREFERENCES section asks for.
"""

from app.graph_rag.repository import GraphRepository
from app.models.graph_rag import GraphEntity, GraphRelationship


class InMemoryGraphRepository(GraphRepository):
    def __init__(self) -> None:
        self._entities: dict[str, GraphEntity] = {}
        self._relationships: list[GraphRelationship] = []

    def upsert_entity(self, entity: GraphEntity) -> None:
        self._entities[entity.id] = entity

    def upsert_relationship(self, relationship: GraphRelationship) -> None:
        is_duplicate = any(
            r.source_id == relationship.source_id
            and r.target_id == relationship.target_id
            and r.relationship_type == relationship.relationship_type
            for r in self._relationships
        )
        if not is_duplicate:
            self._relationships.append(relationship)

    def get_entity(self, entity_id: str) -> GraphEntity | None:
        return self._entities.get(entity_id)

    def find_entities_by_name(self, name: str) -> list[GraphEntity]:
        lowered = name.strip().lower()
        return [entity for entity in self._entities.values() if entity.name.lower() == lowered]

    def outgoing(
        self, entity_id: str, relationship_type: str | None = None
    ) -> list[tuple[GraphRelationship, GraphEntity]]:
        results: list[tuple[GraphRelationship, GraphEntity]] = []
        for relationship in self._relationships:
            if relationship.source_id != entity_id:
                continue
            if relationship_type and relationship.relationship_type != relationship_type:
                continue
            target = self._entities.get(relationship.target_id)
            if target is not None:
                results.append((relationship, target))
        return results

    def counts(self) -> dict[str, int]:
        return {"entities": len(self._entities), "relationships": len(self._relationships)}

    def close(self) -> None:
        pass
