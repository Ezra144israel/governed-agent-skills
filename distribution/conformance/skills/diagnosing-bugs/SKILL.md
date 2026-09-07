---
metadata_schema: team-hub-skill/v1
summary: Diagnosis loop for hard bugs and performance regressions, anchored on a red-capable feedback loop.
skill_id: diagnosing-bugs
version: 1.0.0
lifecycle_status: active
family: verification
capabilities: []
source_provenance:
  kind: adapted
  references:
  - https://github.com/mattpocock/skills
  note: skills/engineering/diagnosing-bugs/SKILL.md @ 1bb95954, MIT, scouted 2026-08-19; project-specific grounding generalized for global eligibility.
authority_boundary: docs-only
eligibility: global
activation_triggers:
- trigger_id: bug-diagnosis
  task_kinds:
  - implementation
  - testing
  - verification
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  - runtime
  description: something is broken, throwing, failing, or intermittently wrong and needs a diagnosis loop
- trigger_id: performance-regression
  task_kinds:
  - testing
  - verification
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  - runtime
  description: a performance regression needs baseline measurement and bisection
activation_exclusions: []
full_load_required_when:
- bug-diagnosis
- performance-regression
section_references: []
platforms:
- portable
surfaces:
- repository
- runtime
required_roles: []
required_lanes: []
related_doctrine: []
graph_edges: []
child_references: []
return_contributions: []
supersedes: []
---

# Diagnosing bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

When exploring a codebase, read its domain-vocabulary document (a glossary or
CONTEXT file) if one exists, and check ADRs and any locked contract in the area you
are touching.

## Redact

This skill has you show commands, outputs, and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask.

## Phase 1: Build a feedback loop

**This is the skill. Everything else is mechanical.** If you have a **tight** pass/fail signal for the bug, one that goes red on *this* bug, you will find the cause. Bisection, hypothesis-testing, and instrumentation all just consume it. If you do not have one, no amount of staring at code will save you.

Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

Ways to construct one, in roughly this order:

1. **Failing test** at whatever test seam reaches the bug.
2. **Curl or HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** driving the UI, asserting on DOM, console, or network.
5. **Replay a captured trace.** Save a real payload or event log to disk, replay it through the code path in isolation.
6. **Throwaway harness.** A minimal subset of the system that exercises the bug path in one function call.
7. **Property or fuzz loop.** For "sometimes wrong output", run many random inputs and look for the failure mode.
8. **Bisection harness.** If it appeared between two known states, automate "boot at state X, check, repeat".
9. **Differential loop.** Same input through old versus new, diff the outputs.
10. **Human-in-the-loop script.** Last resort, and structured: if a human must click, drive them with a script so the loop still has a shape.

### Tighten the loop

Treat the loop as a product. Once you have *a* loop, tighten it:

- Faster: cache setup, skip unrelated init, narrow scope.
- Sharper: assert the specific symptom, not "did not crash".
- More deterministic: pin time, seed RNG, isolate filesystem, freeze network.

A 30-second flaky loop is barely better than no loop. A 2-second deterministic one is a superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop the trigger, parallelise, add stress, narrow timing windows. A 50 percent flake is debuggable. One percent is not. Keep raising the rate.

### When you genuinely cannot build a loop

Stop and say so. List what you tried. Ask for access to an environment that reproduces it, a redacted captured artifact, or authorization for temporary instrumentation. Do **not** proceed to hypothesise without a loop.

### Completion criterion

Phase 1 is done when you can name **one command** you have **already run at least once**, showing the invocation and its redacted output, that is:

- **Red-capable**: drives the actual bug path and asserts the user's exact symptom. Not "runs without erroring".
- **Deterministic**: same verdict every run, or a pinned high reproduction rate.
- **Fast**: seconds, not minutes.
- **Agent-runnable**: runnable unattended.

If you catch yourself reading code to build a theory before this command exists, **stop. Jumping to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2: Reproduce and minimise

Run the loop. Watch it go red.

Confirm the loop produces the failure the **user** described, not a different one nearby. Wrong bug means wrong fix. Confirm it reproduces across runs. Capture the exact symptom so later phases can verify the fix addresses it.

Then shrink to the **smallest scenario that still goes red**. Cut inputs, callers, config, data, and steps one at a time, re-running after each cut. Done when every remaining element is load-bearing: removing any one makes it go green.

A minimal repro shrinks the hypothesis space and becomes the clean regression test.

## Phase 3: Hypothesise

Generate **three to five ranked hypotheses** before testing any. Single-hypothesis generation anchors on the first plausible idea.

Each must be **falsifiable**: state the prediction. *"If X is the cause, then changing Y makes the bug disappear."* If you cannot state the prediction, it is a vibe. Discard or sharpen it.

Show the ranked list to the operator before testing. They often re-rank instantly. Cheap checkpoint. Proceed with your ranking if they are away; this is a read-only step and carries no mutation authority either way.

## Phase 4: Instrument

Each probe maps to a specific prediction. **Change one variable at a time.**

1. Debugger or REPL inspection where the environment supports it. One breakpoint beats ten logs.
2. Targeted logs at the boundaries that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix such as `[DEBUG-a4f2]`, so cleanup is a single grep. Untagged logs survive. Tagged logs die.

For performance regressions, logs are usually wrong. Establish a baseline measurement, then bisect. Measure first, fix second.

## Phase 5: Fix and regression test

Write the regression test **before the fix**, but only if a correct test seam exists.

**Test seam** means a route, server action, query helper, or pure helper interface, exercised the way the bug actually occurs at the call site. Always write `test seam`, never bare `seam`: in governed repositories the bare word may be reserved as an authorization term (the exact files, routes, components, or subsystem an agent is authorized to modify), and that definition wins where it exists.

If the only available test seam is too shallow to replicate the chain that triggered the bug, a test there gives false confidence. **If no correct test seam exists, that itself is the finding.** Note it. The architecture is preventing the bug from being locked down.

If a correct test seam exists: turn the minimised repro into a failing test, watch it fail, apply the fix, watch it pass, then re-run the Phase 1 loop against the original un-minimised scenario.

## Phase 6: Cleanup

Required before declaring done:

- Original repro no longer reproduces, re-run the Phase 1 loop.
- Regression test passes, or the absence of a test seam is documented.
- Task-added `[DEBUG-...]` instrumentation is blocked mechanically at completion (residue scan); the tag convention exists so the scan and one grep both see every probe.
- Throwaway harnesses deleted or moved to a clearly marked location.
- The hypothesis that turned out correct is stated in the commit or return, so the next debugger learns.

---

## Scouted investigation rules

_Salvaged from the retired `scouted-rules` holding pen; sources cited in parentheses._

- No shortcut by code-reading. The code tells you what it does; it rarely tells
  you why it exists. Resist inferring intent from code shape. (`why`)
- Null results from searched sources are first-class evidence. Report them
  beside the positive findings. (`why`)
- Assess complexity before fanning out. A narrow question gets one pass; a
  cross-cutting one gets parallel explorers. When in doubt, lean simple — you
  can always fan out if the single pass hits a wall. (`how`)
- Tag every thread with its state: `[merged #N]`, `[open PR #N]`,
  `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`,
  `[planned, not started]`. A thread with no tag is not done yet. (`recall`)

## Boundary: this skill versus `blast-radius`

Two evidence formalisms, two directions. Do not mix them.

- **`diagnosing-bugs` is backward-looking.** Something is already broken. The artifact is a red-capable loop, and its completion criterion is the four-part check in Phase 1.
- **`blast-radius` is forward-looking.** Nothing is broken yet, and you want to know what a change could break. The artifact is the one fact the change is safe because of, and its formalism is the five-rung ladder where you say which rung you stopped at.

A bug fix uses both, in order: diagnose to find and fix the cause, then blast-radius the fix before it ships.
