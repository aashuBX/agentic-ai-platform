from app.agents.rag_agent import RAGAgent
from app.graph.state import new_conversation_state
from app.observability import new_trace_id


def test_answers_from_knowledge_documents_via_the_real_pipeline(mock_llm, rag_pipeline):
    agent = RAGAgent(rag_pipeline=rag_pipeline, llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="What are the API rate limits?", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert "60 requests per minute" in update["response"]
    assert update["metadata"]["rag_pipeline_phase"] == "phase2_full_pipeline"
    assert update["metadata"]["rag_match_count"] > 0
    assert update["retrieved_context"]


def test_no_match_is_honest_instead_of_guessing(mock_llm, rag_pipeline):
    agent = RAGAgent(rag_pipeline=rag_pipeline, llm=mock_llm)
    state = new_conversation_state(
        session_id="s1", message_text="zzz qqq xyzabc nonsense gibberish", trace_id=new_trace_id()
    )

    update = agent.execute(state)

    assert "couldn't find" in update["response"].lower()
    assert update["retrieved_context"] == []
    assert update["metadata"]["rag_match_count"] == 0
