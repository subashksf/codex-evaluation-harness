from enum import StrEnum


class CodexLayer(StrEnum):
    """Canonical Codex rollout layer identifiers."""

    LAYER_0_GOVERNANCE_REPO_READINESS = "LAYER_0_GOVERNANCE_REPO_READINESS"
    LAYER_1_READ_ONLY_CODEBASE_QA = "LAYER_1_READ_ONLY_CODEBASE_QA"
    LAYER_2_HUMAN_GUIDED_CODE_DRAFTING = "LAYER_2_HUMAN_GUIDED_CODE_DRAFTING"
    LAYER_3_ASSISTED_IMPLEMENTATION = "LAYER_3_ASSISTED_IMPLEMENTATION"
    LAYER_4_PR_REVIEW_ASSISTANCE = "LAYER_4_PR_REVIEW_ASSISTANCE"
    LAYER_5_AGENTIC_PR_CREATION = "LAYER_5_AGENTIC_PR_CREATION"
    LAYER_6_SCALED_AUTOMATION = "LAYER_6_SCALED_AUTOMATION"


class EvaluationStatus(StrEnum):
    """Possible evaluation outcomes."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    BLOCKED = "blocked"
    NOT_APPLICABLE = "not_applicable"


class FindingSeverity(StrEnum):
    """Severity levels for evaluation findings."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKER = "blocker"
