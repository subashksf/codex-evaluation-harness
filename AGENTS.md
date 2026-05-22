# AGENTS.md

## Project purpose

This repository implements an exhaustive evaluation framework for layered Codex usage and enterprise rollout.

The goal of this project is to measure whether Codex improves engineering productivity while preserving or improving correctness, security, maintainability, review quality, compliance, and operational safety.

The framework evaluates Codex across the following rollout layers. Treat the layer IDs as stable, canonical identifiers in docs, configs, scenarios, scorecards, reports, and future code.

| Layer | ID | Name | Description |
|---|---|---|---|
| 0 | `LAYER_0_GOVERNANCE_REPO_READINESS` | Governance and repo readiness | Determine whether a repo is safe and mature enough for Codex usage. |
| 1 | `LAYER_1_READ_ONLY_CODEBASE_QA` | Read-only codebase Q&A | Evaluate Codex as a codebase explanation and onboarding assistant. |
| 2 | `LAYER_2_HUMAN_GUIDED_CODE_DRAFTING` | Human-guided code drafting | Evaluate Codex-generated code snippets, tests, docs, and refactors before direct repo modification. |
| 3 | `LAYER_3_ASSISTED_IMPLEMENTATION` | Assisted implementation | Evaluate Codex making scoped code changes in a branch or worktree. |
| 4 | `LAYER_4_PR_REVIEW_ASSISTANCE` | PR review assistance | Evaluate Codex as a pull request reviewer. |
| 5 | `LAYER_5_AGENTIC_PR_CREATION` | Agentic PR creation | Evaluate Codex implementing tasks and opening PRs for human review. |
| 6 | `LAYER_6_SCALED_AUTOMATION` | Scaled automation | Evaluate Codex performing repeatable multi-repo automation with guardrails. |

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
