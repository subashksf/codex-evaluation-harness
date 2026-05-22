# Codex Evaluation Harness

This repository defines an evaluation framework for onboarding repositories to Codex. It is intended to help teams measure whether Codex improves engineering productivity while preserving correctness, security, maintainability, review quality, compliance, and operational safety.

The harness is organized around layered Codex rollout. Each layer should produce measurable signals, policy decisions, and workflow gates before a repository advances to more autonomous Codex usage.

## Rollout Layers

| Layer | Name | Evaluation Focus |
|---|---|---|
| 0 | Governance and repo readiness | Whether a repository is mature and safe enough for Codex usage. |
| 1 | Read-only codebase Q&A | Whether Codex can explain the codebase accurately for onboarding and discovery. |
| 2 | Human-guided code drafting | Whether Codex can draft snippets, tests, docs, and refactors before direct repo modification. |
| 3 | Assisted implementation | Whether Codex can make scoped code changes in a branch or worktree. |
| 4 | PR review assistance | Whether Codex can identify useful review findings without excessive noise. |
| 5 | Agentic PR creation | Whether Codex can complete tasks and open PRs for human review. |
| 6 | Scaled automation | Whether Codex can perform repeatable multi-repo automation with guardrails. |

## Operating Model

Every feature in this repository should support this loop:

```text
Observe engineering workflow
        |
Collect structured signals
        |
Evaluate against policy
        |
Produce score + decision
        |
Integrate into developer workflow
        |
Improve prompts, policies, and repo guidance
```

## What The Harness Should Evaluate

The framework should capture evidence across several dimensions:

- Productivity: task completion time, implementation effort, reviewer effort, and iteration count.
- Correctness: test outcomes, bug introduction rate, requirements coverage, and behavioral regressions.
- Security: unsafe code patterns, dependency risk, secret handling, and policy violations.
- Maintainability: code clarity, architectural fit, duplication, and long-term ownership risk.
- Review quality: useful findings, false positives, missed issues, and reviewer acceptance.
- Compliance: repository rules, enterprise policy, auditability, and approval gates.
- Operational safety: branch hygiene, rollback readiness, scoped permissions, and automation limits.

## Expected Outputs

For each rollout layer, the harness should produce:

- A scorecard with quantitative and qualitative signals.
- A pass, warn, or block decision.
- Evidence that supports the decision.
- Recommended next steps for repository owners.
- Prompt, policy, or repo guidance changes when gaps are found.

## Intended Workflow

1. Select a repository and target rollout layer.
2. Run the layer-specific evaluation scenario.
3. Collect structured observations from Codex output, repository checks, human review, and automation logs.
4. Evaluate results against the layer policy.
5. Produce a decision report.
6. Update prompts, policies, repository guidance, or onboarding status.

## Repository Status

This repository is currently in the framework-definition stage. The first source of project guidance is `AGENTS.md`.

The Python project skeleton is initialized, but harness business logic has not been implemented yet.

Implementation should start by defining:

- Evaluation scenario schemas.
- Layer-specific policies and gates.
- Scorecard formats.
- Evidence collection adapters.
- Report generation.
- Example evaluations for a small reference repository.

## Development Setup

This project targets Python 3.11.

The Makefile defaults to `python3.11`. If your Python 3.11+ interpreter has a different path, pass it explicitly:

```sh
make install PYTHON=/path/to/python3.11
```

Install the package and development tools:

```sh
make install
```

Run local checks:

```sh
make format
make lint
make typecheck
make test
```

Run the full local CI check:

```sh
make ci
```

## Project Layout

```text
src/codex_eval/       Python package
tests/unit/           Fast unit tests
tests/integration/    Integration tests
configs/policies/     Policy configuration files
docs/                 Project documentation
```

## Development Principles

- Prefer measurable evidence over subjective judgment.
- Keep each layer independently useful.
- Make policy decisions explainable and auditable.
- Treat human review as a core signal, not an afterthought.
- Avoid advancing a repository to a higher autonomy layer without passing lower-layer gates.
