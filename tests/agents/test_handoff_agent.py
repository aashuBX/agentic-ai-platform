from app.agents.handoff_agent import HandoffAgent
from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def test_handoff_sets_flag_and_a_human_response(mock_llm):
    agent = HandoffAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="I want to talk to a human.", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert update["metadata"]["handoff_requested"] is True
    assert "human" in update["response"].lower()
