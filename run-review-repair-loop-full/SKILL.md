---
name: run-review-repair-loop
description: Conduct a bounded, repository-grounded code self-review and repair loop with objective 1-5 scoring, exact scope preservation, targeted fixes, and focused and full verification. In repositories with owned doctrine, dynamically apply current engineering, security, testing, maintainability, build-gate, and return-contract standards through progressive activation. Use when the user asks you to review your own recent code, grade the work, repeatedly fix actionable findings until it earns an evidence-backed 5/5 or reaches an iteration limit, or prepare a change for independent review without publishing or deploying it.
---

# Run Review Repair Loop

Review the real repository state, score the change honestly, repair concrete findings, and repeat. Treat the final score as a self-assessment supported by evidence, never as independent approval.

## Establish The Contract

Before reviewing or editing:

1. Read all applicable system, developer, `AGENTS.md`, repository, and user instructions.
2. Identify the repository, branch, base or comparison range, dirty state, staged state, authorized files, protected paths, required gates, prohibited actions, and iteration limit.
3. Use an explicit user-supplied base or range when provided. Otherwise, prefer the current branch's upstream merge base and include relevant working-tree changes. If the intended range cannot be determined safely, ask one concise question before editing.
4. Default to at most five review-repair iterations unless the user specifies another bound.
5. Preserve pre-existing user changes. Never revert, stage, commit, push, open a pull request, deploy, access production, or mutate external systems unless the current request explicitly authorizes that action.
6. Stop and report if a required fix needs a file outside the authorized scope. Name the exact file and reason instead of silently broadening scope.

If the request is review-only, report findings and scores without editing. If repair is requested or clearly implied, perform the repairs within the established contract.

## Load Repository Doctrine

Treat repository-owned instructions and doctrine as part of the scoring contract, not optional background.

For every repository:

- Read applicable repository instruction files and use current canonical sources rather than memory or pasted summaries.
- Discover repository-native quality, security, testing, architecture, and verification standards before inventing a generic checklist.
- Load detailed doctrine progressively. Do not force unrelated domain guidance into the task.

When the repository has owned doctrine, read its doctrine-router file and follow it. Re-evaluate its trigger matrix whenever the changed-file set or behavior changes during the loop.

## Inspect The Change

Review more than the patch in isolation:

- Inspect the complete target diff and current status.
- Read affected production code, tests, types, schemas, configuration, callers, and downstream consumers needed to understand behavior.
- Check correctness, failure behavior, security boundaries, data integrity, compatibility, concurrency and idempotency where relevant, test quality, and scope containment.
- Search for duplicated contracts or call sites that could make the change incomplete.
- Distinguish defects introduced by the target change from unrelated pre-existing issues. Do not edit unrelated issues unless the user expands scope.

## Score Objectively

Score each category from 1 to 5:

| Category | What to evaluate |
| --- | --- |
| Correctness | Required behavior, edge cases, error paths, and regressions |
| Security and integrity | Trust boundaries, validation, leakage, authorization, and fail-closed behavior |
| Tests and verification | Meaningful coverage, negative cases, realistic seams, and passing gates |
| Scope and compatibility | Authorized-file containment, API compatibility, migration impact, and unrelated churn |
| Maintainability and operations | Clarity, duplication, observability, deterministic behavior, and operational safety |
| Doctrine and governance | Compliance with every activated repository-owned hard gate, authority boundary, and return contract |

Use this scale:

- `5`: No actionable finding remains in this category and all relevant evidence passes.
- `4`: Sound overall, but a concrete low-risk finding or verification gap remains.
- `3`: A meaningful defect, incomplete behavior, or material coverage gap remains.
- `2`: A major correctness, security, compatibility, or verification problem remains.
- `1`: The change is unsafe, broken, unreviewable, or violates the governing contract.

The overall score is the **lowest category score**, not an average. A serious weakness cannot be offset by strengths elsewhere.

Do not award 5/5 based on appearance, compilation alone, or tests that do not exercise the changed behavior. A 5/5 requires:

- no actionable findings after a fresh review of the final diff;
- all required focused checks passing;
- all required repository-wide gates passing when available and authorized;
- exact scope and clean-diff checks passing;
- every activated doctrine gate passing or explicitly marked not applicable with evidence;
- remaining risks limited to explicitly stated external or untestable conditions.

## Run The Bounded Loop

For each iteration:

1. Resolve the current doctrine activation set from the actual changed files, behavior, risk bands, and task authority.
2. Review the current implementation and produce findings first, ordered by severity. Include file and line references, impact, violated doctrine where applicable, and the smallest defensible repair.
3. Record the category scores and overall score.
4. If the score is 5/5, run or confirm the full required gates, then re-inspect the final diff and doctrine activation set before finishing.
5. If actionable findings remain and edits are authorized, implement only the necessary fixes within scope.
6. Add or strengthen tests proportional to the defect and blast radius. Do not weaken assertions, remove coverage, broadly mock away production behavior, suppress errors, or change expected behavior merely to obtain a passing score.
7. Run the narrowest relevant checks after each repair, including syntax, type, focused tests, and diff checks as applicable.
8. Start a new review iteration against the updated code. Do not reuse the prior score or activation set without re-evaluation.

Do not make cosmetic churn solely to raise the grade. Do not invent findings to force additional iterations. If the first review genuinely earns 5/5, make no unnecessary edit.

## Verify The Final Candidate

Use the repository's native verification commands and established test hierarchy. For a provisional 5/5:

1. Run focused tests for the changed behavior.
2. Run the repository's required full battery, type checks, builds, linters, security or manifest checks, and file-size or generated-artifact checks when applicable.
3. Run diff hygiene and exact-scope checks.
4. Inspect the final status and confirm nothing was staged or published unless explicitly authorized.
5. If a command fails, inspect the complete raw output before diagnosing or editing. When a test runner or build tool produces structured logs, read its full raw output for every failing result.
6. Confirm the final doctrine activation report contains no unresolved hard gate, missing required source, or falsely claimed independent review.

A failed required gate caps the overall score below 5 until it passes. If a gate cannot run, state the reason and do not represent the result as a fully verified 5/5 unless the user explicitly accepts that limitation.

## Stop Honestly

Stop before 5/5 when:

- the iteration limit is reached;
- a fix requires unauthorized scope;
- the base, branch, or repository state violates a locked condition;
- required user input or external access is unavailable;
- a safe fix would require a prohibited migration, API change, deployment, or production mutation;
- required verification cannot be completed.

Report the blocker, current score, remaining findings, and the exact next authorization or action needed. Never hide a blocker, lower the rubric, or declare success because time or context is limited.

## Return The Evidence

At completion, report:

1. Review range, branch, and base.
2. Iterations completed and the score progression.
3. Final category scores and overall score.
4. Findings repaired, with concise file references.
5. Remaining findings or risks.
6. Exact changed-file scope.
7. Focused and full verification commands and results.
8. Doctrine activation report: always loaded, triggered, not triggered with reasons, pre-wiring, missing, and downstream-only.
9. Final repository status, including staged, committed, pushed, or deployed state.
10. A clear statement that the score is the builder agent's evidence-backed self-review, that it does not replace independent review, and which independent review contract should run next.

Keep the final report concise, but never omit a failed gate, unresolved finding, scope deviation, or prohibited action.
