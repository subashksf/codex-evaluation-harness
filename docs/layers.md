# Rollout Layers

The Codex evaluation harness uses stable layer IDs to describe a repository's current Codex rollout maturity and the next gate it must pass. These IDs should be used consistently across scenario definitions, policy configs, scorecards, reports, and future Python types.

| Layer | ID | Name | Evaluation Focus |
|---|---|---|---|
| 0 | `LAYER_0_GOVERNANCE_REPO_READINESS` | Governance and repo readiness | Determine whether a repository is safe and mature enough for Codex usage. |
| 1 | `LAYER_1_READ_ONLY_CODEBASE_QA` | Read-only codebase Q&A | Evaluate Codex as a codebase explanation and onboarding assistant. |
| 2 | `LAYER_2_HUMAN_GUIDED_CODE_DRAFTING` | Human-guided code drafting | Evaluate Codex-generated snippets, tests, docs, and refactors before direct repo modification. |
| 3 | `LAYER_3_ASSISTED_IMPLEMENTATION` | Assisted implementation | Evaluate Codex making scoped code changes in a branch or worktree. |
| 4 | `LAYER_4_PR_REVIEW_ASSISTANCE` | PR review assistance | Evaluate Codex as a pull request reviewer. |
| 5 | `LAYER_5_AGENTIC_PR_CREATION` | Agentic PR creation | Evaluate Codex implementing tasks and opening pull requests for human review. |
| 6 | `LAYER_6_SCALED_AUTOMATION` | Scaled automation | Evaluate Codex performing repeatable multi-repo automation with guardrails. |

## Layer 0: Governance And Repo Readiness

ID: `LAYER_0_GOVERNANCE_REPO_READINESS`

This layer determines whether a repository has the governance, structure, documentation, tests, ownership, and safety controls needed before Codex is introduced into developer workflows.

## Layer 1: Read-Only Codebase Q&A

ID: `LAYER_1_READ_ONLY_CODEBASE_QA`

This layer evaluates whether Codex can answer onboarding, architecture, debugging, and code-navigation questions accurately without modifying the repository.

## Layer 2: Human-Guided Code Drafting

ID: `LAYER_2_HUMAN_GUIDED_CODE_DRAFTING`

This layer evaluates Codex output that is reviewed and applied by a human, including code snippets, tests, documentation, refactoring suggestions, and implementation plans.

## Layer 3: Assisted Implementation

ID: `LAYER_3_ASSISTED_IMPLEMENTATION`

This layer evaluates Codex making scoped repository changes in a controlled branch or worktree, with human review and normal repository checks before merge.

## Layer 4: PR Review Assistance

ID: `LAYER_4_PR_REVIEW_ASSISTANCE`

This layer evaluates Codex as a pull request reviewer, including the usefulness, severity, precision, and completeness of review findings.

## Layer 5: Agentic PR Creation

ID: `LAYER_5_AGENTIC_PR_CREATION`

This layer evaluates Codex taking a task from issue or prompt to a complete pull request that is ready for human review.

## Layer 6: Scaled Automation

ID: `LAYER_6_SCALED_AUTOMATION`

This layer evaluates Codex performing repeatable automation across repositories with explicit guardrails, auditability, approval controls, and rollback paths.
