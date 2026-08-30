from app.agents.graph_rag_agent import GraphRAGAgent
from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def test_answers_a_direct_relationship_query(mock_llm, graph_retriever):
    agent = GraphRAGAgent(retriever=graph_retriever, llm=mock_llm)
    state = new_conversation_state(
        session_id="s1",
        message_text="Who is the agent assigned to John Doe?",
        trace_id=new_trace_id(),
    )

    update = agent.execute(state)

    assert "Sarah Lee" in update["response"]
    assert update["metadata"]["graph_path_count"] > 0
    assert update["retrieved_context"]


def test_no_match_is_honest_instead_of_guessing(mock_llm, graph_retriever):
    agent = GraphRAGAgent(retriever=graph_retriever, llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="What is the weather today?", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert "couldn't find" in update["response"].lower()
    assert update["retrieved_context"] == []
    assert update["metadata"]["graph_path_count"] == 0
