from pathlib import Path

from codex_eval.core.enums import CodexLayer, EvaluationStatus, FindingSeverity
from codex_eval.core.models import Finding, MetricResult
from codex_eval.core.results import LayerEvaluationResult
from codex_eval.scanners.local_repo_scanner import LocalRepoScanner, LocalRepoScanResult


class Layer0RepoReadinessEvaluator:
    """Evaluate Layer 0 repository readiness from local filesystem signals."""

    def __init__(self, scanner: LocalRepoScanner | None = None) -> None:
        self.scanner = scanner or LocalRepoScanner()

    def evaluate(self, repo_path: str | Path) -> LayerEvaluationResult:
        scan = self.scanner.scan(repo_path)
        blocking_findings = self._blocking_findings(scan)
        warnings = self._warnings(scan)
        max_allowed_layer = self._max_allowed_layer(scan)

        return LayerEvaluationResult(
            repo=str(scan.repo_path),
            layer=CodexLayer.LAYER_0_GOVERNANCE_REPO_READINESS,
            status=self._status(max_allowed_layer, warnings),
            score=self._score(scan),
            max_allowed_layer=max_allowed_layer,
            metrics=self._metrics(scan),
            blocking_findings=blocking_findings,
            warnings=warnings,
            required_actions=self._required_actions(blocking_findings, warnings),
            evidence=self._evidence(scan),
        )

    def _max_allowed_layer(self, scan: LocalRepoScanResult) -> CodexLayer:
        if not scan.readme_exists or not scan.agents_exists:
            return CodexLayer.LAYER_1_READ_ONLY_CODEBASE_QA
        if not scan.ci_config_exists or not scan.test_directory_exists:
            return CodexLayer.LAYER_2_HUMAN_GUIDED_CODE_DRAFTING
        if not scan.codeowners_exists:
            return CodexLayer.LAYER_3_ASSISTED_IMPLEMENTATION
        return CodexLayer.LAYER_4_PR_REVIEW_ASSISTANCE

    def _status(self, max_allowed_layer: CodexLayer, warnings: list[Finding]) -> EvaluationStatus:
        if max_allowed_layer is CodexLayer.LAYER_1_READ_ONLY_CODEBASE_QA:
            return EvaluationStatus.FAIL
        if max_allowed_layer is not CodexLayer.LAYER_4_PR_REVIEW_ASSISTANCE:
            return EvaluationStatus.WARN
        if warnings:
            return EvaluationStatus.WARN
        return EvaluationStatus.PASS

    def _score(self, scan: LocalRepoScanResult) -> float:
        checks = (
            scan.readme_exists,
            scan.agents_exists,
            scan.ci_config_exists,
            scan.build_config_exists,
            scan.test_directory_exists,
            scan.codeowners_exists,
        )
        return round((sum(checks) / len(checks)) * 100, 2)

    def _metrics(self, scan: LocalRepoScanResult) -> list[MetricResult]:
        return [
            self._boolean_metric("readme_exists", scan.readme_exists, "README.md exists."),
            self._boolean_metric("agents_exists", scan.agents_exists, "AGENTS.md exists."),
            self._boolean_metric(
                "ci_config_exists",
                scan.ci_config_exists,
                "CI/CD configuration exists.",
            ),
            self._boolean_metric(
                "build_config_exists",
                scan.build_config_exists,
                "A supported build configuration file exists.",
            ),
            self._boolean_metric(
                "test_directory_exists",
                scan.test_directory_exists,
                "A test directory exists.",
            ),
            self._boolean_metric(
                "codeowners_exists",
                scan.codeowners_exists,
                "CODEOWNERS exists in a supported location.",
            ),
            MetricResult(
                name="sensitive_paths_present",
                value=bool(scan.sensitive_paths),
                threshold=False,
                status=EvaluationStatus.WARN if scan.sensitive_paths else EvaluationStatus.PASS,
                description="Sensitive path patterns were found.",
            ),
        ]

    def _blocking_findings(self, scan: LocalRepoScanResult) -> list[Finding]:
        findings: list[Finding] = []

        if not scan.readme_exists:
            findings.append(
                Finding(
                    code="missing-readme",
                    message="README.md is required for repository onboarding.",
                    severity=FindingSeverity.BLOCKER,
                    evidence=["README.md was not found at the repository root."],
                    remediation="Add README.md with repository purpose, setup, and workflows.",
                )
            )

        if not scan.agents_exists:
            findings.append(
                Finding(
                    code="missing-agents",
                    message="AGENTS.md is required before Codex usage can be evaluated.",
                    severity=FindingSeverity.BLOCKER,
                    evidence=["AGENTS.md was not found at the repository root."],
                    remediation="Add AGENTS.md with Codex operating guidance for this repository.",
                )
            )

        if scan.readme_exists and scan.agents_exists and not scan.ci_config_exists:
            findings.append(
                Finding(
                    code="missing-ci-config",
                    message="CI/CD configuration is required before implementation workflows.",
                    severity=FindingSeverity.HIGH,
                    evidence=["No supported CI/CD configuration was found."],
                    remediation="Add a CI/CD configuration for the repository's build system.",
                )
            )

        if (
            scan.readme_exists
            and scan.agents_exists
            and scan.ci_config_exists
            and not scan.test_directory_exists
        ):
            findings.append(
                Finding(
                    code="missing-test-directory",
                    message="A test directory is required before assisted implementation.",
                    severity=FindingSeverity.HIGH,
                    evidence=["No test or tests directory was found."],
                    remediation="Add a test directory with repository tests.",
                )
            )

        if (
            scan.readme_exists
            and scan.agents_exists
            and scan.ci_config_exists
            and scan.test_directory_exists
            and not scan.codeowners_exists
        ):
            findings.append(
                Finding(
                    code="missing-codeowners",
                    message="CODEOWNERS is required before PR review assistance.",
                    severity=FindingSeverity.MEDIUM,
                    evidence=[
                        "No CODEOWNERS file was found in CODEOWNERS, "
                        ".github/CODEOWNERS, or docs/CODEOWNERS."
                    ],
                    remediation="Add CODEOWNERS in a supported location.",
                )
            )

        return findings

    def _warnings(self, scan: LocalRepoScanResult) -> list[Finding]:
        warnings: list[Finding] = []

        if not scan.build_config_exists:
            warnings.append(
                Finding(
                    code="missing-build-config",
                    message="No supported build configuration file was found.",
                    severity=FindingSeverity.LOW,
                    evidence=[
                        "Expected one of pyproject.toml, package.json, pom.xml, or build.gradle."
                    ],
                    remediation="Add or document the repository build configuration.",
                )
            )

        if scan.sensitive_paths:
            warnings.append(
                Finding(
                    code="sensitive-paths-present",
                    message=(
                        "Sensitive path patterns were found and may need stricter Codex controls."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    evidence=scan.sensitive_paths,
                    remediation="Review sensitive areas and define explicit Codex guardrails.",
                )
            )

        return warnings

    def _required_actions(
        self, blocking_findings: list[Finding], warnings: list[Finding]
    ) -> list[str]:
        return [
            finding.remediation
            for finding in [*blocking_findings, *warnings]
            if finding.remediation is not None
        ]

    def _evidence(self, scan: LocalRepoScanResult) -> list[str]:
        evidence = [
            f"README.md exists: {scan.readme_exists}",
            f"AGENTS.md exists: {scan.agents_exists}",
            f"CODEOWNERS paths: {', '.join(scan.codeowners_paths) or 'none'}",
            f"CI/CD config paths: {', '.join(scan.ci_config_paths) or 'none'}",
            f"Build config paths: {', '.join(scan.build_config_paths) or 'none'}",
            f"Test directories: {', '.join(scan.test_directory_paths) or 'none'}",
        ]
        if scan.sensitive_paths:
            evidence.append(f"Sensitive paths: {', '.join(scan.sensitive_paths)}")
        return evidence

    @staticmethod
    def _boolean_metric(name: str, value: bool, description: str) -> MetricResult:
        return MetricResult(
            name=name,
            value=value,
            threshold=True,
            status=EvaluationStatus.PASS if value else EvaluationStatus.FAIL,
            description=description,
        )


def evaluate_layer0_repo_readiness(repo_path: str | Path) -> LayerEvaluationResult:
    return Layer0RepoReadinessEvaluator().evaluate(repo_path)
