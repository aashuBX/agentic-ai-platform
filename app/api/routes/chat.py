"""POST /chat — the primary conversational entry point, matching requirement.md's CHAT section."""

from fastapi import APIRouter, Depends
from langgraph.graph.state import CompiledStateGraph

from app.api.deps import get_graph
from app.graph.state import new_conversation_state
from app.models.messages import ChatRequest, ChatResponse
from app.observability import new_trace_id

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, graph: CompiledStateGraph = Depends(get_graph)) -> ChatResponse:
    trace_id = new_trace_id()
    turn_input = new_conversation_state(
        session_id=request.session_id,
        message_text=request.message,
        trace_id=trace_id,
        channel=request.channel.value,
        user_id=request.user_id,
    )
    result = graph.invoke(turn_input, config={"configurable": {"thread_id": request.session_id}})

    intent = result.get("intent")
    guardrails = result.get("guardrail_results", {})
    input_report = guardrails.get("input")
    output_report = guardrails.get("output")
    guardrail_passed = (input_report is None or input_report.passed) and (
        output_report is None or output_report.passed
    )
    tools_used = [str(tool_result.get("tool")) for tool_result in result.get("tool_results", [])]

    return ChatResponse(
        response=result.get("response") or "",
        intent=intent.intent.value if intent else None,
        agent=result.get("selected_agent"),
        tools_used=tools_used,
        trace_id=trace_id,
        guardrail_passed=guardrail_passed,
    )
