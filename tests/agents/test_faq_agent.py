from app.agents.faq_agent import FAQAgent
from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def test_answers_a_known_faq_grounded_in_context(mock_llm):
    agent = FAQAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="What are your business hours?", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert "9am-6pm" in update["response"]
    assert update["retrieved_context"]
    assert update["metadata"]["faq_match"] == "faq-003"


def test_no_match_is_honest_instead_of_guessing(mock_llm):
    agent = FAQAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="zzz qqq xyzabc", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert "couldn't find" in update["response"].lower()
    assert update["retrieved_context"] == []
    assert update["metadata"]["faq_match"] is None
