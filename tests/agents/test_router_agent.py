import pytest

from app.agents.router_agent import ROUTE_MAP, RouterAgent
from app.graph.state import new_conversation_state
from app.models.enums import IntentCategory
from app.models.intent import IntentClassification
from app.observability import new_trace_id


@pytest.mark.parametrize("intent_category,expected_node", list(ROUTE_MAP.items()))
def test_routes_every_known_intent_to_a_real_node(mock_llm, intent_category, expected_node):
    agent = RouterAgent(llm=mock_llm)
    state = new_conversation_state(session_id="s1", message_text="hello", trace_id=new_trace_id())
    state["intent"] = IntentClassification(intent=intent_category, confidence=0.9, reason="test")

    update = agent.execute(state)

    assert update["selected_agent"] == expected_node


def test_missing_intent_defaults_to_the_unknown_route(mock_llm):
    agent = RouterAgent(llm=mock_llm)
    state = new_conversation_state(session_id="s1", message_text="hello", trace_id=new_trace_id())
    state["intent"] = None

    update = agent.execute(state)

    assert update["selected_agent"] == ROUTE_MAP[IntentCategory.UNKNOWN]
