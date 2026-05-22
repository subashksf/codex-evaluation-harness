# AGENTS.md

## Project purpose

This repository implements an exhaustive evaluation framework for layered Codex usage and enterprise rollout.

The goal of this project is to measure whether Codex improves engineering productivity while preserving or improving correctness, security, maintainability, review quality, compliance, and operational safety.

The framework evaluates Codex across the following rollout layers:

| Layer | Name | Description |
|---|---|---|
| 0 | Governance and repo readiness | Determine whether a repo is safe and mature enough for Codex usage. |
| 1 | Read-only codebase Q&A | Evaluate Codex as a codebase explanation and onboarding assistant. |
| 2 | Human-guided code drafting | Evaluate Codex-generated code snippets, tests, docs, and refactors before direct repo modification. |
| 3 | Assisted implementation | Evaluate Codex making scoped code changes in a branch or worktree. |
| 4 | PR review assistance | Evaluate Codex as a pull request reviewer. |
| 5 | Agentic PR creation | Evaluate Codex implementing tasks and opening PRs for human review. |
| 6 | Scaled automation | Evaluate Codex performing repeatable multi-repo automation with guardrails. |

The framework should produce measurable signals, policy decisions, and workflow gates for each layer.

---

## Core design principle

Every feature in this repo must support this operating model:

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
