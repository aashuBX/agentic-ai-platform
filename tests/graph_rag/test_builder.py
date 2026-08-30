from app.graph_rag.builder import GraphBuilder
from app.graph_rag.entities import RegexEntityExtractor
from app.graph_rag.memory_repository import InMemoryGraphRepository
from app.graph_rag.relationships import RegexRelationshipExtractor

_TEXT = "John Doe owns account ACCT-2001. John Doe is assigned to agent Sarah Lee."


def test_extract_does_not_touch_the_repository():
    repository = InMemoryGraphRepository()
    builder = GraphBuilder(RegexEntityExtractor(), RegexRelationshipExtractor(), repository)

    result = builder.extract(_TEXT)

    assert len(result.entities) == 3
    assert len(result.relationships) == 2
    assert repository.counts() == {"entities": 0, "relationships": 0}


def test_build_and_store_persists_to_the_repository():
    repository = InMemoryGraphRepository()
    builder = GraphBuilder(RegexEntityExtractor(), RegexRelationshipExtractor(), repository)

    builder.build_and_store(_TEXT)

    assert repository.counts() == {"entities": 3, "relationships": 2}
    john = repository.find_entities_by_name("John Doe")[0]
    assigned = repository.outgoing(john.id, relationship_type="ASSIGNED_TO")
    assert assigned[0][1].name == "Sarah Lee"


def test_build_and_store_is_idempotent():
    repository = InMemoryGraphRepository()
    builder = GraphBuilder(RegexEntityExtractor(), RegexRelationshipExtractor(), repository)

    builder.build_and_store(_TEXT)
    builder.build_and_store(_TEXT)

    assert repository.counts() == {"entities": 3, "relationships": 2}
