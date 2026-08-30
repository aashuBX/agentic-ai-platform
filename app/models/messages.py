"""Chat message and API request/response schemas for the `/chat` contract."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.models.enums import Channel, MessageRole


class ChatMessage(BaseModel):
    """A single turn in a conversation, as stored in ConversationState."""

    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChatRequest(BaseModel):
    """POST /chat request body — matches requirement.md's CHAT section exactly."""

    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4000)
    channel: Channel = Channel.WEB
    user_id: str | None = None


class ChatResponse(BaseModel):
    """POST /chat response body — matches requirement.md's CHAT section exactly."""

    response: str
    intent: str | None = None
    agent: str | None = None
    tools_used: list[str] = Field(default_factory=list)
    trace_id: str
    guardrail_passed: bool = True
