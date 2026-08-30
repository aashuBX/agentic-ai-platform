from app.graph_rag.entities import RegexEntityExtractor
from app.graph_rag.relationships import LLMRelationshipExtractor, RegexRelationshipExtractor

_TEXT = (
    "John Doe owns account ACCT-2001. John Doe created order ORD-3001. "
    "John Doe is assigned to agent Sarah Lee. "
    "John Doe booked appointment APT-4001 with Sarah Lee."
)


def test_regex_extractor_finds_every_relationship():
    entities = RegexEntityExtractor().extract(_TEXT)
    relationships = RegexRelationshipExtractor().extract(_TEXT, entities)
    by_type = {r.relationship_type: (r.source_id, r.target_id) for r in relationships}

    assert by_type["OWNS"] == ("customer:john-doe", "account:acct-2001")
    assert by_type["CREATED"] == ("customer:john-doe", "order:ord-3001")
    assert by_type["ASSIGNED_TO"] == ("customer:john-doe", "agent:sarah-lee")
    assert by_type["BOOKED"] == ("customer:john-doe", "appointment:apt-4001")
    assert by_type["WITH"] == ("appointment:apt-4001", "agent:sarah-lee")
    assert len(relationships) == 5


def test_regex_extractor_handles_unrelated_text():
    assert RegexRelationshipExtractor().extract("The weather is nice today.", []) == []


def test_llm_extractor_falls_back_to_regex_under_mock_provider(mock_llm):
    entities = RegexEntityExtractor().extract(_TEXT)
    extractor = LLMRelationshipExtractor(llm=mock_llm)
    relationships = extractor.extract(_TEXT, entities)
    assert {r.relationship_type for r in relationships} == {
        "OWNS",
        "CREATED",
        "ASSIGNED_TO",
        "BOOKED",
        "WITH",
    }
