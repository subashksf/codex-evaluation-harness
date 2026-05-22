from pathlib import Path

from codex_eval.core.enums import CodexLayer, EvaluationStatus
from codex_eval.evaluators.layer0_repo_readiness import (
    evaluate_layer0_repo_readiness,
)
from codex_eval.scanners.local_repo_scanner import LocalRepoScanner

FIXTURE_REPOS = Path(__file__).parents[1] / "fixtures" / "repos"


def finding_codes(result_codes: list[str]) -> set[str]:
    return set(result_codes)


def test_minimal_repo_is_limited_to_layer_1() -> None:
    result = evaluate_layer0_repo_readiness(FIXTURE_REPOS / "minimal")

    assert result.layer is CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS
    assert result.max_allowed_layer is CodexLayer.LAYER_1_READ_ONLY_CODEBASE_QA
    assert result.status is EvaluationStatus.FAIL
    assert finding_codes([finding.code for finding in result.blocking_findings]) >= {
        "missing-readme",
        "missing-agents",
    }


def test_repo_with_readme_and_agents_is_limited_to_layer_2_without_ci() -> None:
    result = evaluate_layer0_repo_readiness(FIXTURE_REPOS / "readme_agents")

    assert result.max_allowed_layer is CodexLayer.LAYER_2_HUMAN_GUIDED_CODE_DRAFTING
    assert result.status is EvaluationStatus.WARN
    assert "missing-ci-config" in {finding.code for finding in result.blocking_findings}


def test_repo_with_ci_and_tests_is_limited_to_layer_3_without_codeowners() -> None:
    result = evaluate_layer0_repo_readiness(FIXTURE_REPOS / "ci_tests")

    assert result.max_allowed_layer is CodexLayer.LAYER_3_ASSISTED_IMPLEMENTATION
    assert result.status is EvaluationStatus.WARN
    assert "missing-codeowners" in {finding.code for finding in result.blocking_findings}


def test_repo_with_codeowners_is_limited_to_layer_4_from_local_checks() -> None:
    result = evaluate_layer0_repo_readiness(FIXTURE_REPOS / "codeowners")

    assert result.max_allowed_layer is CodexLayer.LAYER_4_PR_REVIEW_ASSISTANCE
    assert result.status is EvaluationStatus.PASS
    assert result.blocking_findings == []
    assert result.warnings == []


def test_repo_with_sensitive_paths_reports_warning_without_advancing_past_layer_4() -> None:
    result = evaluate_layer0_repo_readiness(FIXTURE_REPOS / "sensitive")

    assert result.max_allowed_layer is CodexLayer.LAYER_4_PR_REVIEW_ASSISTANCE
    assert result.status is EvaluationStatus.WARN
    assert "sensitive-paths-present" in {finding.code for finding in result.warnings}
    assert any("config/prod" in evidence for evidence in result.evidence)


def test_scanner_finds_sensitive_paths() -> None:
    scan = LocalRepoScanner().scan(FIXTURE_REPOS / "sensitive")

    assert "infra" in scan.sensitive_paths
    assert "customer-data" in scan.sensitive_paths
    assert any(path.startswith("config/prod") for path in scan.sensitive_paths)
