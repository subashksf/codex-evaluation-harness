from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

DEFAULT_SENSITIVE_PATH_PATTERNS = (
    "auth",
    "security",
    "payments",
    "infra",
    "terraform",
    "k8s",
    "secrets",
    "config/prod",
    "migrations",
    "customer-data",
    "pii",
)

CODEOWNERS_CANDIDATES = (
    "CODEOWNERS",
    ".github/CODEOWNERS",
    "docs/CODEOWNERS",
)

BUILD_CONFIG_CANDIDATES = (
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
)

TEST_DIRECTORY_CANDIDATES = (
    "test",
    "tests",
)

CI_CONFIG_CANDIDATES = (
    ".github/workflows",
    "Jenkinsfile",
    "jenkinsfile",
    ".jenkins/Jenkinsfile",
    ".sfci.yml",
    ".sfci.yaml",
    "sfci.yml",
    "sfci.yaml",
    ".sfci",
    "sfci",
    ".gitlab-ci.yml",
    ".gitlab-ci.yaml",
    ".circleci/config.yml",
    ".circleci/config.yaml",
    ".buildkite/pipeline.yml",
    ".buildkite/pipeline.yaml",
    "azure-pipelines.yml",
    "azure-pipelines.yaml",
    ".azure-pipelines.yml",
    ".azure-pipelines.yaml",
    ".azure/pipelines.yml",
    ".azure/pipelines.yaml",
    "ci.yml",
    "ci.yaml",
    ".ci.yml",
    ".ci.yaml",
    "pipeline.yml",
    "pipeline.yaml",
    ".pipeline.yml",
    ".pipeline.yaml",
)


class LocalRepoScanResult(BaseModel):
    """Filesystem readiness signals collected from a local repository."""

    model_config = ConfigDict(extra="forbid")

    repo_path: Path
    readme_exists: bool
    agents_exists: bool
    codeowners_paths: list[str] = Field(default_factory=list)
    ci_config_paths: list[str] = Field(default_factory=list)
    build_config_paths: list[str] = Field(default_factory=list)
    test_directory_paths: list[str] = Field(default_factory=list)
    sensitive_paths: list[str] = Field(default_factory=list)

    @property
    def codeowners_exists(self) -> bool:
        return len(self.codeowners_paths) > 0

    @property
    def ci_config_exists(self) -> bool:
        return len(self.ci_config_paths) > 0

    @property
    def build_config_exists(self) -> bool:
        return len(self.build_config_paths) > 0

    @property
    def test_directory_exists(self) -> bool:
        return len(self.test_directory_paths) > 0


class LocalRepoScanner:
    """Collect local filesystem signals for a repository."""

    def __init__(self, sensitive_path_patterns: Sequence[str] | None = None) -> None:
        self.sensitive_path_patterns = tuple(
            sensitive_path_patterns or DEFAULT_SENSITIVE_PATH_PATTERNS
        )

    def scan(self, repo_path: str | Path) -> LocalRepoScanResult:
        root = Path(repo_path).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"Repository path does not exist: {root}")
        if not root.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {root}")

        return LocalRepoScanResult(
            repo_path=root,
            readme_exists=(root / "README.md").is_file(),
            agents_exists=(root / "AGENTS.md").is_file(),
            codeowners_paths=self._existing_relative_paths(root, CODEOWNERS_CANDIDATES),
            ci_config_paths=self._existing_ci_paths(root),
            build_config_paths=self._existing_relative_paths(root, BUILD_CONFIG_CANDIDATES),
            test_directory_paths=self._existing_relative_directories(
                root, TEST_DIRECTORY_CANDIDATES
            ),
            sensitive_paths=self._find_sensitive_paths(root),
        )

    def _existing_relative_paths(self, root: Path, relative_candidates: Sequence[str]) -> list[str]:
        return sorted(
            self._to_posix_relative(path, root)
            for candidate in relative_candidates
            if (path := root / candidate).exists()
        )

    def _existing_relative_directories(
        self, root: Path, relative_candidates: Sequence[str]
    ) -> list[str]:
        return sorted(
            self._to_posix_relative(path, root)
            for candidate in relative_candidates
            if (path := root / candidate).is_dir()
        )

    def _existing_ci_paths(self, root: Path) -> list[str]:
        existing_paths = self._existing_relative_paths(root, CI_CONFIG_CANDIDATES)
        workflows_dir = root / ".github" / "workflows"
        if workflows_dir.is_dir() and any(workflows_dir.glob("*.yml")):
            existing_paths.append(".github/workflows")
        if workflows_dir.is_dir() and any(workflows_dir.glob("*.yaml")):
            existing_paths.append(".github/workflows")
        return sorted(set(existing_paths))

    def _find_sensitive_paths(self, root: Path) -> list[str]:
        matches = {
            self._to_posix_relative(path, root)
            for path in root.rglob("*")
            if self._is_scannable_path(path, root) and self._matches_sensitive_pattern(path, root)
        }
        return sorted(matches)

    def _matches_sensitive_pattern(self, path: Path, root: Path) -> bool:
        relative_path = self._to_posix_relative(path, root)
        components = tuple(part.lower() for part in Path(relative_path).parts)

        for pattern in self.sensitive_path_patterns:
            normalized_pattern = pattern.lower().strip("/")
            if "/" in normalized_pattern:
                if relative_path == normalized_pattern or relative_path.startswith(
                    f"{normalized_pattern}/"
                ):
                    return True
                continue

            if any(
                self._component_matches_pattern(component, normalized_pattern)
                for component in components
            ):
                return True

        return False

    @staticmethod
    def _component_matches_pattern(component: str, pattern: str) -> bool:
        return component in {
            pattern,
            f"{pattern}.yml",
            f"{pattern}.yaml",
            f"{pattern}.json",
            f"{pattern}.toml",
        } or component.startswith((f"{pattern}-", f"{pattern}_", f"{pattern}."))

    @staticmethod
    def _is_scannable_path(path: Path, root: Path) -> bool:
        relative_parts = path.relative_to(root).parts
        ignored_parts = {
            ".git",
            ".venv",
            "__pycache__",
            ".mypy_cache",
            ".pytest_cache",
            ".ruff_cache",
        }
        return not any(part in ignored_parts for part in relative_parts)

    @staticmethod
    def _to_posix_relative(path: Path, root: Path) -> str:
        return path.relative_to(root).as_posix()
