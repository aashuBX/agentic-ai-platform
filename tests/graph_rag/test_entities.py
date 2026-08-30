from app.graph_rag.entities import LLMEntityExtractor, RegexEntityExtractor, normalize_id

_TEXT = (
    "John Doe owns account ACCT-2001. John Doe created order ORD-3001. "
    "John Doe is assigned to agent Sarah Lee. "
    "John Doe booked appointment APT-4001 with Sarah Lee."
)


def test_normalize_id_is_stable_and_slugified():
    assert normalize_id("Customer", "John Doe") == "customer:john-doe"
    assert normalize_id("Customer", "John Doe") == normalize_id("customer", "john doe")


def test_regex_extractor_finds_every_entity_type():
    entities = RegexEntityExtractor().extract(_TEXT)
    by_type = {e.entity_type: e.name for e in entities}

    assert by_type["Customer"] == "John Doe"
    assert by_type["Account"] == "ACCT-2001"
    assert by_type["Order"] == "ORD-3001"
    assert by_type["Agent"] == "Sarah Lee"
    assert by_type["Appointment"] == "APT-4001"
    assert len(entities) == 5  # no duplicates despite "Sarah Lee" appearing twice


def test_regex_extractor_handles_unrelated_text():
    assert RegexEntityExtractor().extract("The weather is nice today.") == []


def test_llm_extractor_falls_back_to_regex_under_mock_provider(mock_llm):
    extractor = LLMEntityExtractor(llm=mock_llm)
    entities = extractor.extract(_TEXT)
    assert {e.entity_type for e in entities} == {
        "Customer",
        "Account",
        "Order",
        "Agent",
        "Appointment",
    }
