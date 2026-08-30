from app.graph.state import new_conversation_state
from app.guardrails.output_guardrail_agent import OutputGuardrailAgent
from app.models.enums import MessageRole
from app.observability import new_trace_id


def test_passes_a_normal_response_and_appends_it_to_messages(mock_llm):
    agent = OutputGuardrailAgent(llm=mock_llm)
    state = new_conversation_state(session_id="s1", message_text="hi", trace_id=new_trace_id())
    state["response"] = "Here is a helpful answer."

    update = agent.execute(state)

    assert update["guardrail_results"]["output"].passed is True
    assert update["response"] == "Here is a helpful answer."
    assert len(update["messages"]) == 1
    assert update["messages"][0].role == MessageRole.ASSISTANT
    assert update["messages"][0].content == "Here is a helpful answer."


def test_blocks_an_empty_response_with_a_safe_fallback(mock_llm):
    agent = OutputGuardrailAgent(llm=mock_llm)
    state = new_conversation_state(session_id="s1", message_text="hi", trace_id=new_trace_id())
    state["response"] = ""

    update = agent.execute(state)

    assert update["guardrail_results"]["output"].passed is False
    assert update["response"] != ""


def test_blocks_a_leaked_stack_trace(mock_llm):
    agent = OutputGuardrailAgent(llm=mock_llm)
    state = new_conversation_state(session_id="s1", message_text="hi", trace_id=new_trace_id())
    state["response"] = "Traceback (most recent call last):\n  File x, line 1"

    update = agent.execute(state)

    assert update["guardrail_results"]["output"].passed is False
