from app.agents.crm_agent import CRMAgent
from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def test_crm_skeleton_is_explicit_about_not_being_wired_to_mcp(mock_llm):
    agent = CRMAgent(llm=mock_llm)
    state = new_conversation_state(
        session_id="s1",
        message_text="Find John's lead and mark it as qualified.",
        trace_id=new_trace_id(),
    )

    update = agent.execute(state)

    assert "Phase 4" in update["response"]
    assert update["tool_results"] == []
    assert update["metadata"]["crm_tools_wired"] is False
