from app.graph_rag.memory_repository import InMemoryGraphRepository
from app.models.graph_rag import GraphEntity, GraphRelationship

_JOHN = GraphEntity(id="customer:john-doe", name="John Doe", entity_type="Customer")
_ACCOUNT = GraphEntity(id="account:acct-1", name="ACCT-1", entity_type="Account")
_AGENT = GraphEntity(id="agent:sarah-lee", name="Sarah Lee", entity_type="Agent")


def test_upsert_and_get_entity():
    repo = InMemoryGraphRepository()
    repo.upsert_entity(_JOHN)
    assert repo.get_entity("customer:john-doe") == _JOHN
    assert repo.get_entity("does-not-exist") is None


def test_upsert_entity_overwrites_by_id():
    repo = InMemoryGraphRepository()
    repo.upsert_entity(_JOHN)
    updated = _JOHN.model_copy(update={"name": "Jonathan Doe"})
    repo.upsert_entity(updated)
    assert repo.get_entity("customer:john-doe").name == "Jonathan Doe"
    assert repo.counts()["entities"] == 1


def test_find_entities_by_name_is_case_insensitive():
    repo = InMemoryGraphRepository()
    repo.upsert_entity(_JOHN)
    assert repo.find_entities_by_name("john doe") == [_JOHN]
    assert repo.find_entities_by_name("Nobody") == []


def test_upsert_relationship_dedupes():
    repo = InMemoryGraphRepository()
    repo.upsert_entity(_JOHN)
    repo.upsert_entity(_ACCOUNT)
    relationship = GraphRelationship(
        source_id=_JOHN.id, target_id=_ACCOUNT.id, relationship_type="OWNS"
    )
    repo.upsert_relationship(relationship)
    repo.upsert_relationship(relationship)
    assert repo.counts()["relationships"] == 1


def test_outgoing_returns_relationship_and_target():
    repo = InMemoryGraphRepository()
    repo.upsert_entity(_JOHN)
    repo.upsert_entity(_ACCOUNT)
    repo.upsert_entity(_AGENT)
    repo.upsert_relationship(
        GraphRelationship(source_id=_JOHN.id, target_id=_ACCOUNT.id, relationship_type="OWNS")
    )
    repo.upsert_relationship(
        GraphRelationship(source_id=_JOHN.id, target_id=_AGENT.id, relationship_type="ASSIGNED_TO")
    )

    all_edges = repo.outgoing(_JOHN.id)
    assert len(all_edges) == 2

    filtered = repo.outgoing(_JOHN.id, relationship_type="OWNS")
    assert len(filtered) == 1
    assert filtered[0][1] == _ACCOUNT


def test_outgoing_from_unknown_entity_is_empty():
    repo = InMemoryGraphRepository()
    assert repo.outgoing("nobody") == []


def test_close_is_a_safe_no_op():
    InMemoryGraphRepository().close()
