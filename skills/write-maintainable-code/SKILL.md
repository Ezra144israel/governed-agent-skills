---
name: write-maintainable-code
description: "Evaluate minimum-sufficient implementation routes and enforce the selected route for a fixed, authorized outcome: decide whether code is needed, compare existing behavior, configuration, reuse, deletion, documentation, and no-code routes, locate the smallest code ownership seam, control speculative concepts, and keep a nontrivial implementation or refactor proportionate and testable. Use only after outcome, acceptance evidence, scope, and authority are fixed. Do not use to select or reframe outcomes, set acceptance evidence, adjudicate governance authority, seat responsibility, scope, or publication, discover a repository without an authorized implementation decision, grade completed work, design tests only, conduct a security audit, write documentation-only copy with no implementation decision, or perform unrelated style cleanup."
---

# Write Maintainable Code

Use the fewest concepts that satisfy the already-approved result and its
acceptance evidence. Minimize current maintenance burden, not raw line count.

## Keep the ownership boundary

This skill is a subordinate implementation lens inside the public method:

- During CONVERGE, generate code/no-code route alternatives and possible code
  ownership seams. Let `reasoning-doctrine` own the stage, recommendation,
  rejected alternatives, hard stops, safe outcome slice, and transition to
  execution.
- During EXECUTE, apply this lens to the selected route. Do not redefine the
  selected outcome, acceptance evidence, safe slice, or mutation method.
- During an authorized repair, apply only this execution lens.
  `run-review-repair-loop` continues to own review, scoring, and repair
  iteration.
- When governance is active, let `governed-operator` own authority, seats,
  scope, the formal contract, verdicts, publication boundaries, and Done.

If the outcome or acceptance evidence is unresolved, return to
`reasoning-doctrine`. If authority, seat responsibility, scope, or publication
authority is unresolved, return to `governed-operator`. If a finished change
needs review-only grading, use `run-review-repair-loop` and keep its Builder
self-review separate from the independent-review and Done boundaries owned by
`governed-operator`; do not score or approve under this lens. Re-enter this
skill only for an authorized repair.

## Compare routes before adding code

1. Echo the fixed outcome and acceptance evidence without reopening them.
2. Inspect the current behavior and evidence. If they already satisfy the
   acceptance check, choose no change and stop.
3. Compare existing behavior, configuration, reuse, deletion, documentation,
   and no-code routes before proposing new code. A route is sufficient only
   when the fixed acceptance evidence can prove it.
4. Under CONVERGE, return the route and ownership-seam alternatives to the
   public method for selection. Once a route is selected, execute only that
   route.

When different routes would satisfy different acceptance checks and the
current evidence does not identify which check applies, do not invent one.
Return that gap to `reasoning-doctrine`. Otherwise, let the public method select
only the route proved necessary by the fixed check.

Do not turn this comparison into a second implementation brief or a competing
return schema.

## Bound the implementation

Before changing code, name:

- the smallest code ownership seam that can own the current behavior;
- the concepts required by the selected result; and
- the tempting concepts declined because the current result does not need
  them.

Decline a dependency, layer, abstraction, state or status flag, endpoint,
migration, generic helper, or compatibility path when its only justification
is hypothetical reuse or an unselected future. Prefer readable, explicit,
testable code over dense code golf. A slightly longer implementation can be
more minimal when it carries fewer concepts or less maintenance risk.

Treat file size as a signal, not a diagnosis. Extract a bounded seam only when
the extraction lowers verified current risk; do not split a file merely to
make it shorter.

Apply this lens inside the already-selected safe outcome slice. Remove only
code made obsolete by the current change. Report unrelated cleanup instead of
performing it.

## Respect operator priorities

Absent a contrary approved predicate, interpret minimum as minimizing concepts
and maintenance burden. If the operator explicitly prioritizes raw line count,
surface the readability and testability tradeoff. Follow that preference only
when it remains compatible with correctness, safety, repository rules, and
authority.

If a line-count preference or new evidence changes the fixed acceptance
predicate, selected result, route, seam, scope, or authority, stop this lens
and return to the appropriate public reconvergence owner before acting.

## Stop and return evidence

Stop as soon as the selected acceptance evidence passes. Do not add cleanup or
future-proofing after that point.

Without governed mode, return only a short minimum-sufficiency rationale and a
residual-risk note. With `governed-operator` active, map the route, seam,
declined concepts, verification, and residual risk into its existing Builder
judgment record. Do not define another brief, score, verdict, approval rule, or
Done condition.
