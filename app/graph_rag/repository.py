"""GraphRepository interface (requirement.md GRAPHRAG section: "Neo4j repository")."""

from abc import ABC, abstractmethod

from app.models.graph_rag import GraphEntity, GraphRelationship


class GraphRepository(ABC):
    @abstractmethod
    def upsert_entity(self, entity: GraphEntity) -> None: ...

    @abstractmethod
    def upsert_relationship(self, relationship: GraphRelationship) -> None: ...

    @abstractmethod
    def get_entity(self, entity_id: str) -> GraphEntity | None: ...

    @abstractmethod
    def find_entities_by_name(self, name: str) -> list[GraphEntity]: ...

    @abstractmethod
    def outgoing(
        self, entity_id: str, relationship_type: str | None = None
    ) -> list[tuple[GraphRelationship, GraphEntity]]:
        """Relationships starting at `entity_id`, optionally filtered by type, paired with the
        target entity at the other end of each one."""

    @abstractmethod
    def counts(self) -> dict[str, int]: ...

    @abstractmethod
    def close(self) -> None: ...
