from pydantic import BaseModel, ConfigDict, Field

from codex_eval.core.enums import CodexLayer, EvaluationStatus
from codex_eval.core.models import Finding, MetricResult


class LayerEvaluationResult(BaseModel):
    """Evaluation result for a repository at a specific Codex rollout layer."""

    model_config = ConfigDict(extra="forbid")

    repo: str = Field(min_length=1)
    layer: CodexLayer
    status: EvaluationStatus
    score: float = Field(ge=0.0, le=100.0)
    max_allowed_layer: CodexLayer
    metrics: list[MetricResult] = Field(default_factory=list)
    blocking_findings: list[Finding] = Field(default_factory=list)
    warnings: list[Finding] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
