"""GraphRAG schemas: extracted entities/relationships, and relationship-aware query results."""

from typing import Any

from pydantic import BaseModel, Field


class GraphEntity(BaseModel):
    """A node in the knowledge graph."""

    id: str = Field(description='Normalized identifier, e.g. "customer:john-doe"')
    name: str
    entity_type: str = Field(
        description='e.g. "Customer", "Account", "Order", "Agent", "Appointment"'
    )
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphRelationship(BaseModel):
    """A directed edge in the knowledge graph."""

    source_id: str
    target_id: str
    relationship_type: str = Field(
        description='e.g. "OWNS", "CREATED", "ASSIGNED_TO", "BOOKED", "WITH"'
    )
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphExtractionResult(BaseModel):
    """What `GraphBuilder.build_from_text()` produces from one piece of text."""

    entities: list[GraphEntity] = Field(default_factory=list)
    relationships: list[GraphRelationship] = Field(default_factory=list)


class GraphPath(BaseModel):
    """One relationship-aware retrieval result: a start entity plus the hop(s) taken to reach it."""

    start_entity: GraphEntity
    hops: list[tuple[GraphRelationship, GraphEntity]] = Field(default_factory=list)

    def describe(self) -> str:
        """Human-readable one-liner, e.g. "John Doe --ASSIGNED_TO--> Sarah Lee"."""

        parts = [self.start_entity.name]
        for relationship, entity in self.hops:
            parts.append(f"--{relationship.relationship_type}--> {entity.name}")
        return " ".join(parts)
