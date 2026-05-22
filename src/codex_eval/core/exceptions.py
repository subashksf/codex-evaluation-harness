class CodexEvalError(Exception):
    """Base exception for Codex evaluation harness errors."""


class EvaluationConfigError(CodexEvalError):
    """Raised when evaluation configuration is invalid."""


class EvaluationExecutionError(CodexEvalError):
    """Raised when an evaluation cannot be executed."""


class EvaluationResultError(CodexEvalError):
    """Raised when an evaluation result cannot be produced or consumed."""
