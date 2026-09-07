---
metadata_schema: team-hub-skill/v1
summary: Guides scoped, maintainable implementation without authorizing broad refactors or replacing hard gates.
skill_id: code-quality
version: 1.1.0
lifecycle_status: active
family: grounding
capabilities: []
source_provenance:
  kind: original
  references: []
  note: null
authority_boundary: docs-only
activation_triggers:
- trigger_id: implementation-logic
  task_kinds:
  - implementation
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  description: new implementation logic is being written
- trigger_id: code-review
  task_kinds:
  - review
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - build-review
  - repository
  description: implementation code is under review
- trigger_id: test-writing
  task_kinds:
  - testing
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - build-review
  - repository
  description: tests are being written
- trigger_id: over-refactor-risk
  task_kinds:
  - refactor
  risk_flags:
  - high-risk-file
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  description: a scoped change risks broad cleanup or refactor
activation_exclusions: []
full_load_required_when:
- code-review
- implementation-logic
- over-refactor-risk
- test-writing
section_references: []
platforms:
- portable
- team-hub-runtime-advisory
surfaces:
- build-review
- documentation
- repository
required_roles: []
required_lanes: []
related_doctrine:
- docs/handoffs/ACTIVE-READ-ORDER.md
- docs/handoffs/DOCTRINE-WIRING-LAYER-LOCK.md
- docs/handoffs/SKILL-INVENTORY-LOCK.md
graph_edges:
- type: depends_on
  target: repo-grounding
  condition_trigger_ids: []
- type: related
  target: security
  condition_trigger_ids: []
- type: related
  target: store-readiness
  condition_trigger_ids: []
child_references: []
return_contributions:
- contribution_id: code-quality/quality-notes
  activation_trigger_ids:
  - implementation-logic
  - code-review
  - test-writing
  - over-refactor-risk
  requirement: optional
  order: 205
  fields:
  - field_id: quality-decisions
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record naming, responsibility, readability, and scoped-refactor decisions.
  - field_id: deferred-cleanup
    value_type: string-list
    required: true
    allowed_values: []
    prompt: List unrelated cleanup deliberately left untouched.
  - field_id: proportionality
    value_type: string
    required: true
    allowed_values: []
    prompt: Explain why the implementation is the simplest adequate route and identify any justified complexity.
supersedes: []
---

# code-quality/SKILL.md

**Status:** Active Team Hub OS skill. Active as documentation/skill guidance when loaded by the governed workflow. It is not runtime enforcement authority.

## Purpose

This skill provides soft heuristics for writing clean, readable, and maintainable code within Team Hub OS.

These are Soft Heuristics, not Hard Gates. They guide how new logic should be written. They do not authorize broad, unrequested refactoring of existing code.

Surgical implementation always takes precedence over stylistic perfection.

## Core Rule

Write new code defensively and clearly.

If existing code violates these heuristics, leave it alone unless:

1. the assigned task specifically requests a refactor,
2. the existing code prevents safe implementation, or
3. the existing code directly blocks verification of the assigned change.

Prefer the local file’s existing style over a new style preference, unless the existing style creates a safety or verification problem.

## Soft Heuristics for Builder Agents

### 1. Naming and Labeling

Use descriptive names that align with the repo’s existing naming conventions.

Avoid generic labels like `data`, `temp`, `obj`, `result`, or `item` unless the scope is tiny and obvious.

If a specific naming pattern already exists in the file, follow it. For example, camelCase names like `fetchUserData` should stay camelCase if that is the local convention.

Do not bulk-rename variables in existing files just to match a new preference.
Do not create extra categories, badges, labels, or status names when existing
language already communicates the needed distinction.

Do not create catch-all names like `utils`, `helpers`, or `misc` for new modules.
Group helpers near their domain until shared use is proven. Do not move code
across ownership boundaries to make a diff look smaller.

#### Domain language

Before implementation, check `operator-web/CONTEXT.md`.

If the task uses a term defined there, use the exact term. No synonyms, no
paraphrasing, no parallel name. Variable, function, and component names should
use that vocabulary where applicable.

If the task introduces or relies on a term that is not defined there, flag it
in the return rather than inventing one:

```text
Vocabulary gap: [term] is not in CONTEXT.md.
Suggested definition: [one sentence]
Authorization needed before adding to CONTEXT.md.
```

Do not add terms to `CONTEXT.md` as a side effect of a bounded implementation
seam. Add a term only when the task explicitly includes vocabulary maintenance
or the operator has authorized the glossary update. `CONTEXT.md` is a quick
reference; root `AGENTS.md` and the canonical glossary lock are authoritative
on conflict. `skills/repo-grounding/SKILL.md` owns this check.

### 2. Shallow Control Flow

Prefer early returns and shallow control flow.

When writing new functions, avoid deeply nested `if/else`, `switch`, loop, or `try/catch` blocks when a clearer early return, guard clause, or helper extraction would make the code easier to verify.

Do not rewrite stable, functioning nested legacy code unless the assigned task requires it or the nesting prevents safe implementation.

### 3. Modular Logic

Prefer single-purpose functions.

When writing new logic, avoid combining unrelated responsibilities such as validation, fetching, transformation, UI mutation, logging, and persistence in one large block.

Extract helpers when doing so:

- reduces risk
- improves verification
- matches an existing repo pattern
- keeps the active seam easier to review

Do not over-abstract. Do not create helper files or shared utilities unless the current task needs them or the repo already has a clear pattern for them.

### 4. Complexity Awareness

Keep new logic easy to reason about.

If a new function has heavy branching, repeated conditionals, or multiple state transitions, consider simplifying it or extracting a helper inside the active seam.

Formal complexity scoring is not required for normal work.

Mention complexity risk in the Builder Return only when the implementation adds logic that may be hard to verify or maintain.

### 4A. Define Success Before Editing

Before touching implementation, translate the task into observable success criteria and name the verification for each step. If the criteria depend on an unresolved interpretation, surface that fork before coding instead of silently choosing one.

Strong criteria describe behavior a test, build, or real-surface check can prove. "Make it work" and "clean this up" are not sufficient acceptance criteria.

### 4B. Structural Simplification

A refactor should remove concepts, branches, duplication, or coupling rather than relocate the same complexity behind another layer.

When new behavior would bolt repeated conditionals onto an unrelated flow, prefer an explicit owning helper, state, or policy inside the active seam. Reuse an existing canonical helper instead of creating a near-duplicate, and make type boundaries explicit rather than hiding unclear invariants behind casts, optionals, or silent fallbacks.

Clean up functions and branches made semantically obsolete by the current change; where the repository's pinned analyzer runs, task-caused unused imports, locals, and parameters are already blocked mechanically at completion. Report unrelated pre-existing dead code instead of deleting it without authorization.

Extraction non-negotiables: no giant rewrites, no broad formatting churn, no
opportunistic cleanup outside the active seam, no behavior change hidden inside
"cleanup", and no new abstraction unless it removes real coupling or creates a
test seam.

A net line increase in the source file is acceptable during an extraction slice
when all of the following hold:

- the extracted seam has its own tests;
- the responsibility count of the source file decreases;
- the new file has a single clear module type and responsibility;
- the increase is caused only by import and adapter wiring, not new logic.

Do not abandon a correct extraction because the diff shows the source file
temporarily growing. The goal is responsibility reduction, not line reduction.

Stop and propose extraction before coding when the new code would extend a
giant handler, the target file already mixes UI, command routing, and
persistence, the change needs three or more distant state variables, the only
safe test would be a source-string assertion, or the change would add a
responsibility, command family, persistence path, or runtime/external-tool
authority path to a Critical file in
`docs/architecture/HIGH_RISK_FILE_REGISTRY.md` (the registry's allowed-work
list governs the exception).

### 4C. Proportionality Guard

Choose the simplest adequate implementation. Avoid unnecessary abstractions,
layers, controls, states, categories, badges, and labels.

Additional complexity is justified only by a verified requirement, a safety or
authority boundary, real reuse already exercised by the slice, or a measurable
reduction in total complexity. Familiar patterns, hypothetical reuse, visual
busyness, and a desire to make the work appear more governed are not sufficient
reasons.

If review identifies determinate excess, remove it inside the same open work
unit. That removal does not require another substantive review unless it
materially changes behavior or architecture. Preserve the largest safe slice
and its evidence; do not create microgates around simplification.

Before adding code, compare the real routes: current behavior, configuration,
reuse, deletion, documentation, and no-code. If the current acceptance evidence
already passes, make no change. Choose a route only when the fixed acceptance
evidence can prove it, then name the smallest ownership seam and the concepts
that route actually needs.

A reviewer applies the same test: new labels must communicate a real
distinction and must not restate existing status or governance vocabulary.

### 5. External Failure Strategy

External calls should not fail silently.

When adding or modifying an external API or service call, define the failure strategy.

Use retry/backoff only when it is safe, idempotent, and appropriate.

Do not blindly retry operations that could double-charge, double-create, double-dispatch, double-write, or corrupt state.

Refer to `security/SKILL.md` for security-sensitive failure behavior.

## Module types and authority

Every file needs one primary responsibility and one clear authority level. Do
not combine UI rendering, state ownership, routing, side effects, persistence,
runtime authority, external-tool authority, and command dispatch in one file
unless the task proves the combination is temporary, bounded, and already
covered by tests.

| Type | Owns | Must not own |
|---|---|---|
| UI component | Render structure and user-visible composition | Persistence, network calls, runtime authority, command routing |
| Presentational component | Props-only display, formatting, local display affordances | Fetching, storage, server actions, global orchestration |
| Hook | UI state, effects, hydration, subscriptions for one surface | Domain validation, DB writes, cross-lane orchestration |
| Pure helper | Deterministic parsing, validation, formatting, readback building | Fetch, storage, DB, `Date.now` unless injected, mutation |
| Server action | One server-side command/read boundary | UI rendering, large readback formatting, unrelated domain decisions |
| Route/API | Protocol boundary, auth/validation, adapter call | Tool registry sprawl, UI decisions, DB schema ownership |
| DB query helper | Scoped reads/writes through repo query patterns | UI labels, route parsing, runtime policy invention |
| Schema/migration | Durable data shape | Runtime decisions, UI states, command dispatch |
| Adapter | External service/tool translation | Product state ownership, canonical truth mutation outside approved boundary |
| Test | Behavioral proof or source-level guardrail | Production behavior, hidden runtime dependency |

Treat a file as higher risk when it owns more than one of these authorities:

- UI authority: what is rendered.
- State authority: component/global state and transitions.
- Side-effect authority: fetch, storage, timers, clipboard, browser APIs.
- Persistence authority: DB/query/storage writes or durable reads.
- Runtime authority: events, writebacks, approvals, orchestration, dispatch.
- External-tool authority: MCP, provider APIs, GitHub, bridge, SDK.

Mixed-authority files are high risk even when not huge. Warning signs that a
file has become one: UI rendering and command parsing together; local state,
browser storage, network calls, and runtime decisions in one component; large
handlers deciding unrelated workflows; protocol handling and tool dispatch in
one function; DB decisions mixed with operator-facing language; render trees so
large that behavior is hard to test; source-string tests as the main safety net.

Before creating a new file, state its module type and primary responsibility.

Good:

```text
Type: pure helper
Responsibility: parse Assistant Home command text into dispatch candidates.
Authority: no UI, no fetch, no storage, no runtime mutation.
```

Bad:

```text
Responsibility: handle assistant workflow.
```

Risk bands and file-size limits are not stated here. They are owned by
`docs/architecture/HIGH_RISK_FILE_REGISTRY.md` and enforced by
`operator-web/scripts/check-file-sizes.cjs`.

## Complexity thresholds

Warning triggers, not automatic failures. If a file crosses a threshold but is
cohesive, explain why it remains safe. File length is deliberately absent: the
registry policy owns it deterministically.

| Metric | Watch | High | Extraction required |
|---|---:|---:|---:|
| Component body | 300 lines | 1,000 lines | 2,000 lines |
| Function/handler body | 100 lines | 300 lines | 1,000 lines |
| Import count | 20 | 35 | 45 |
| Top-level functions | 25 | 75 | 125 |
| Responsibilities | 3 | 5 | 8 |
| Authority types | 2 | 3 | 4 |

"Extraction required" means an extraction plan is needed before adding new
responsibility. It does not change a file's registry band; band changes require
a separate registry update.

## Side-effect placement

- Keep fetch/API calls out of presentational components.
- Keep localStorage/sessionStorage hydration in hooks or small local adapters.
- Keep command parsing in pure helpers, not render bodies.
- Keep event/writeback/approval/runtime decisions outside UI rendering.
- Keep DB access inside query helpers or server boundaries.
- Keep external-tool calls behind adapters or governed actions.

## Extraction

Extract progressively and preserve behavior first. One slice extracts one pure
helper, hook, component, parser, or dispatcher seam. Do not combine extraction
with new feature behavior unless the operator explicitly approves that risk.

Recommended order:

1. Pure helpers.
2. Parsers.
3. Dispatch/readback builders.
4. Hooks for persistence/hydration/effects.
5. Presentational components.
6. Controller split only after tests exist.

Controller split rule: do not split a large controller, route handler, or
component body first. Extract deterministic helpers and tests around dispatch
decisions before the split, because controller splits can silently alter
behavior, ordering, or authority boundaries.

Pure helper pattern: identify the input shape; add or move tests for current
behavior; create a named helper in the nearest domain folder; move only
deterministic logic; import it back; verify no rendered or side-effect
behavior changed.

Hook pattern: extract one state/effect family; keep props and return values
explicit; do not hide runtime authority inside the hook; test the pure pieces;
smoke-test the component path where tooling exists.

Presentational pattern: pass data and callbacks as props; do not move fetch,
storage, server actions, or command parsing into the component; keep labels and
accessibility behavior unchanged.

Good helper shapes:

```ts
buildReadback(input): Readback
parseCommand(text): ParsedCommand | null
deriveDispatchDecision(input): DispatchDecision
validateBoundaryPayload(payload): ValidationResult
```

Bad helper shapes:

```ts
handleEverything(...)
processAssistantWorkflow(...)
doRuntimeStuff(...)
renderAndFetch(...)
```

Stop before implementation when no behavioral seam can be identified, the only
proposed proof is a source-string assertion for complex behavior, the helper
needs hidden global state, or the helper would import React, DB clients,
routes, or browser storage without necessity.

## Test writing

`skills/test-verification/SKILL.md` is the authority for test design, ordering,
seam expectations, failure-path coverage, and what a source-string test may not
prove. Load it whenever a testing seam matters. This skill states no separate
test rules.

## Scouted design rules

_Salvaged from the retired `scouted-rules` holding pen; sources cited in parentheses._

- A lying type guard is worse than a cast, because the bug hides behind a name
  that says it is safe. (`typescript-best-practices`)
- Strengthen a type only where partiality appears. Extra precision costs reuse
  and ceremony and buys no safety. (`principle-type-system-discipline`)
- The 30-second test: can a new reader answer "where does X come from?" and
  "what can change X?" in under 30 seconds? If not, cut layers or cut state.
  (`principle-minimize-reader-load`)
- If a human developer would find the code exhausting to maintain, it is a bad
  solution. (`principle-laziness-protocol`)
- The tell that you skipped domain modeling is a new feature that grows an
  existing if/else chain by one more branch, or a second boolean that must stay
  in sync with the first. (`principle-model-the-domain`)
- Restart bugs: suspect state before code. Code does not change between runs;
  state does. If clearing a state file restores behavior, the fix is state
  validation. (`principle-fix-root-causes`)
- If any answer is "it depends what state was left behind," the operation needs
  a reconciliation step. (`principle-make-operations-idempotent`)
- Treat "we need a lock" as a design smell to check, not the default answer.
  Eliminate the sharing first.
  (`principle-separate-before-serializing-shared-state`)
- Is this data crossing a system boundary right now? If not, the validation is
  redundant. (`principle-boundary-discipline`)
- Scrap on a pattern, not on single instances. The signal that a design is
  wrong is the same shape of workaround recurring: types needing escape
  hatches, callers having to know internal rules, repeated special-case
  branches. A few hard cases do not condemn a design. (`architect`)

Local qualification, carried with the rules: the source skill's
reversible-versus-irreversible split is weaker than the per-act authority gates
in `governed-operator`, where lock, build, commit, push, merge, deploy, walk,
and cleanup are held separately and none inherits from another. Keep that line;
do not import the binary.

## Over-Refactor Guardrail

The most common AI builder failure is rewriting an entire file to make it “cleaner.”

Code quality improvements must stay inside the active seam defined by `repo-grounding/SKILL.md`.

If a 2-line bug fix causes a 50-line rewrite, the agent must justify why that broader change was required.

Aesthetic cleanup is not a valid reason to widen scope.

## Reviewer Interaction

When a Reviewer Agent evaluates code against this skill:

- They may issue Needs Revision if newly added logic is unnecessarily convoluted, poorly named, unsafe, or hard to verify.
- They should not block work solely because existing legacy code outside the active seam violates these heuristics.
- They should not turn these soft heuristics into hard gates unless the issue creates safety, verification, or maintainability risk for the assigned task.

## Relationship to Other Skills

This skill is subordinate to:

- `repo-grounding/SKILL.md` for domain vocabulary
- `security/SKILL.md`
- `store-readiness/SKILL.md`
- the Lean Loop Builder return contract (`relay/packages/human-grade-engineering-loop-v1.1/seat-builder.md`)

If a code-quality preference conflicts with a hard gate, the hard gate wins.
