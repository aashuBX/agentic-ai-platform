"""Guardrail result schemas, shared by the input and output guardrail agents."""

from pydantic import BaseModel, Field

from app.models.enums import GuardrailStatus


class GuardrailCheckResult(BaseModel):
    """Outcome of one individual check (e.g. "oversized_request", "grounding_check")."""

    check_name: str
    status: GuardrailStatus
    message: str = ""


class GuardrailReport(BaseModel):
    """Aggregate outcome of a guardrail stage (input or output), holding all its checks."""

    passed: bool
    status: GuardrailStatus
    checks: list[GuardrailCheckResult] = Field(default_factory=list)

    @classmethod
    def from_checks(cls, checks: list[GuardrailCheckResult]) -> "GuardrailReport":
        passed = all(c.status == GuardrailStatus.PASSED for c in checks)
        return cls(
            passed=passed,
            status=GuardrailStatus.PASSED if passed else GuardrailStatus.BLOCKED,
            checks=checks,
        )
