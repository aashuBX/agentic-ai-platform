from app.agents.intent_agent import IntentAgent
from app.graph.state import new_conversation_state
from app.models.enums import IntentCategory
from app.observability import new_trace_id


def test_classifies_crm_update(mock_llm):
    agent = IntentAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1",
        message_text="Find John's lead and mark it as qualified.",
        trace_id=new_trace_id(),
    )
    update = agent.execute(state)
    assert update["intent"].intent == IntentCategory.CRM_UPDATE
    assert 0.0 <= update["intent"].confidence <= 1.0
    assert update["metadata"]["intent"] == "CRM_UPDATE"


def test_classifies_faq_question(mock_llm):
    agent = IntentAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="What is your refund policy?", trace_id=new_trace_id()
    )
    update = agent.execute(state)
    assert update["intent"].intent == IntentCategory.FAQ


def test_unrecognized_text_falls_back_to_unknown(mock_llm):
    agent = IntentAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="asdkjhasdkjh", trace_id=new_trace_id()
    )
    update = agent.execute(state)
    assert update["intent"].intent == IntentCategory.UNKNOWN


def test_never_leaks_chain_of_thought_only_concise_reason(mock_llm):
    agent = IntentAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="I'd like to book an appointment.", trace_id=new_trace_id()
    )
    update = agent.execute(state)
    assert len(update["intent"].reason) <= 280
