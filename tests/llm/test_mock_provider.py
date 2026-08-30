from pydantic import BaseModel

from app.llm.base import LLMMessage
from app.llm.providers.mock import MockLLMProvider
from app.models.enums import MessageRole
from app.models.intent import IntentClassification


def test_generate_passes_through_grounding_context_verbatim():
    provider = MockLLMProvider()
    response = provider.generate(
        [
            LLMMessage(role=MessageRole.SYSTEM, content="CONTEXT: The sky is blue."),
            LLMMessage(role=MessageRole.USER, content="What color is the sky?"),
        ]
    )
    assert response.content == "The sky is blue."
    assert response.provider == "mock"


def test_generate_labels_itself_as_a_mock_without_context():
    provider = MockLLMProvider()
    response = provider.generate([LLMMessage(role=MessageRole.USER, content="hello")])
    assert "mock-llm" in response.content


def test_structured_output_uses_the_registered_intent_heuristic():
    provider = MockLLMProvider()
    result = provider.generate_structured(
        [LLMMessage(role=MessageRole.USER, content="I'd like to book an appointment for Tuesday.")],
        IntentClassification,
    )
    assert isinstance(result, IntentClassification)
    assert result.intent.value == "APPOINTMENT_QUERY"


def test_structured_output_falls_back_to_a_minimal_valid_instance_for_unregistered_schemas():
    class Scratch(BaseModel):
        flag: bool
        label: str
        score: float

    provider = MockLLMProvider()
    result = provider.generate_structured(
        [LLMMessage(role=MessageRole.USER, content="irrelevant")], Scratch
    )

    assert result == Scratch(flag=False, label="", score=0.0)
