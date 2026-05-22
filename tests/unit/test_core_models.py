import pytest
from pydantic import ValidationError

from codex_eval.core.enums import CodexLayer, EvaluationStatus, FindingSeverity
from codex_eval.core.models import Finding, MetricResult
from codex_eval.core.results import LayerEvaluationResult


def test_finding_validates_required_fields() -> None:
    finding = Finding.model_validate(
        {
            "code": "missing-tests",
            "message": "Repository does not define a test command.",
            "severity": "high",
            "evidence": ["No test target found in Makefile."],
            "remediation": "Add a repeatable test command.",
        }
    )

    assert finding.severity is FindingSeverity.HIGH
    assert finding.evidence == ["No test target found in Makefile."]


def test_finding_rejects_empty_code() -> None:
    with pytest.raises(ValidationError):
        Finding(code="", message="Missing code.", severity=FindingSeverity.LOW)


def test_metric_result_accepts_status_and_values() -> None:
    metric = MetricResult(
        name="test_pass_rate",
        value=0.95,
        threshold=0.9,
        status=EvaluationStatus.PASS,
        description="Share of tests passing.",
    )

    assert metric.value == 0.95
    assert metric.status is EvaluationStatus.PASS


def test_layer_evaluation_result_validates_nested_models() -> None:
    result = LayerEvaluationResult.model_validate(
        {
            "repo": "example/service",
            "layer": CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS,
            "status": "warn",
            "score": 72.5,
            "max_allowed_layer": CodexLayer.LAYER_1_READ_ONLY_CODEBASE_QA,
            "metrics": [
                {
                    "name": "documentation_score",
                    "value": 0.7,
                    "threshold": 0.8,
                    "status": "warn",
                }
            ],
            "warnings": [
                {
                    "code": "missing-owner",
                    "message": "Repository ownership is not documented.",
                    "severity": "medium",
                    "evidence": ["CODEOWNERS not found."],
                }
            ],
            "required_actions": ["Document repository ownership."],
            "evidence": ["README reviewed."],
        }
    )

    assert result.status is EvaluationStatus.WARN
    assert result.metrics[0].status is EvaluationStatus.WARN
    assert result.warnings[0].severity is FindingSeverity.MEDIUM


def test_layer_evaluation_result_rejects_score_above_100() -> None:
    with pytest.raises(ValidationError):
        LayerEvaluationResult(
            repo="example/service",
            layer=CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS,
            status=EvaluationStatus.PASS,
            score=100.1,
            max_allowed_layer=CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS,
        )


def test_layer_evaluation_result_rejects_unknown_layer() -> None:
    with pytest.raises(ValidationError):
        LayerEvaluationResult.model_validate(
            {
                "repo": "example/service",
                "layer": "unknown",
                "status": EvaluationStatus.PASS,
                "score": 100.0,
                "max_allowed_layer": CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS,
            }
        )
