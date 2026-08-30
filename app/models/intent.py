"""Structured output schema for intent classification.

Per requirement.md RULE 5: store only concise routing metadata (intent, confidence, a short
reason) — never raw chain-of-thought.
"""

from pydantic import BaseModel, Field

from app.models.enums import IntentCategory


class IntentClassification(BaseModel):
    """Matches requirement.md's INTENT DETECTION example exactly."""

    intent: IntentCategory
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str = Field(
        max_length=280,
        description="Concise routing rationale — never raw model chain-of-thought.",
    )
