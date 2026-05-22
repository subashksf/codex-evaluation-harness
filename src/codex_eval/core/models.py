from typing import TypeAlias

from pydantic import BaseModel, ConfigDict, Field

from codex_eval.core.enums import EvaluationStatus, FindingSeverity

MetricValue: TypeAlias = bool | float | int | str


class Finding(BaseModel):
    """A concrete evaluation finding with supporting context."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    severity: FindingSeverity
    evidence: list[str] = Field(default_factory=list)
    remediation: str | None = None


class MetricResult(BaseModel):
    """A single metric produced by an evaluation."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    value: MetricValue
    threshold: MetricValue | None = None
    status: EvaluationStatus
    description: str | None = None
