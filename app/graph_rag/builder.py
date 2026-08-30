"""GraphBuilder: turns extracted entities + relationships into a stored graph.

requirement.md's GRAPHRAG pipeline: DOCUMENT -> ENTITY EXTRACTION -> RELATIONSHIP EXTRACTION ->
GRAPH BUILDER -> NEO4J. This class is the "GRAPH BUILDER" box — it owns nothing about extraction
or storage itself, just wires the two together against a `GraphRepository`.
"""

from app.graph_rag.entities import EntityExtractor
from app.graph_rag.relationships import RelationshipExtractor
from app.graph_rag.repository import GraphRepository
from app.models.graph_rag import GraphExtractionResult


class GraphBuilder:
    def __init__(
        self,
        entity_extractor: EntityExtractor,
        relationship_extractor: RelationshipExtractor,
        repository: GraphRepository,
    ) -> None:
        self._entity_extractor = entity_extractor
        self._relationship_extractor = relationship_extractor
        self._repository = repository

    def extract(self, text: str) -> GraphExtractionResult:
        entities = self._entity_extractor.extract(text)
        relationships = self._relationship_extractor.extract(text, entities)
        return GraphExtractionResult(entities=entities, relationships=relationships)

    def build_and_store(self, text: str) -> GraphExtractionResult:
        result = self.extract(text)
        for entity in result.entities:
            self._repository.upsert_entity(entity)
        for relationship in result.relationships:
            self._repository.upsert_relationship(relationship)
        return result
