"""End-to-end tests of the compiled LangGraph workflow — one per requirement.md DEMO SCENARIOS
entry (FAQ, RAG, GraphRAG relationship query, CRM update, handoff, guardrail rejection)."""

from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def _invoke(graph, session_id: str, text: str) -> dict:
    state = new_conversation_state(
        session_id=session_id, message_text=text, trace_id=new_trace_id()
    )
    return graph.invoke(state, config={"configurable": {"thread_id": session_id}})


def test_faq_scenario(compiled_graph):
    result = _invoke(compiled_graph, "t-faq", "What are your business hours?")
    assert result["selected_agent"] == "faq_agent"
    assert "9am-6pm" in result["response"]
    assert result["guardrail_results"]["input"].passed is True
    assert result["guardrail_results"]["output"].passed is True


def test_rag_scenario(compiled_graph):
    result = _invoke(compiled_graph, "t-rag", "What are the API rate limits?")
    assert result["selected_agent"] == "rag_agent"
    assert result["response"]


def test_graph_query_scenario_demonstrates_relationship_aware_retrieval(compiled_graph):
    result = _invoke(compiled_graph, "t-graph", "Who is the agent assigned to John Doe?")
    assert result["selected_agent"] == "graph_rag_agent"
    assert "Sarah Lee" in result["response"]


def test_feedback_intent_still_reports_not_implemented_honestly(compiled_graph):
    result = _invoke(compiled_graph, "t-feedback", "I have some feedback about your service.")
    assert result["selected_agent"] == "not_implemented"
    assert "Feedback" in result["response"]


def test_crm_update_scenario_matches_requirement_example(compiled_graph):
    result = _invoke(compiled_graph, "t-crm", "Find John's lead and mark it as qualified.")
    assert result["intent"].intent.value == "CRM_UPDATE"
    assert result["selected_agent"] == "crm_agent"
    assert "Phase 4" in result["response"]


def test_handoff_scenario(compiled_graph):
    result = _invoke(
        compiled_graph, "t-handoff", "I want to talk to a human representative please."
    )
    assert result["selected_agent"] == "handoff_agent"


def test_guardrail_rejection_scenario_never_reaches_the_router(compiled_graph):
    result = _invoke(compiled_graph, "t-blocked", "")
    assert result["guardrail_results"]["input"].passed is False
    assert result["selected_agent"] is None
    assert result["intent"] is None


def test_cross_turn_memory_genuinely_accumulates(compiled_graph):
    _invoke(compiled_graph, "t-memory", "What are your business hours?")
    _invoke(compiled_graph, "t-memory", "And what about WhatsApp integration?")

    snapshot = compiled_graph.get_state({"configurable": {"thread_id": "t-memory"}})

    assert len(snapshot.values["messages"]) == 4  # user, assistant, user, assistant


def test_separate_sessions_do_not_share_history(compiled_graph):
    _invoke(compiled_graph, "t-iso-a", "What are your business hours?")
    _invoke(compiled_graph, "t-iso-b", "What is your refund policy?")

    snapshot_a = compiled_graph.get_state({"configurable": {"thread_id": "t-iso-a"}})
    snapshot_b = compiled_graph.get_state({"configurable": {"thread_id": "t-iso-b"}})

    assert len(snapshot_a.values["messages"]) == 2
    assert len(snapshot_b.values["messages"]) == 2
