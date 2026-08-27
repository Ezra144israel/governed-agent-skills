---
name: test-verification
description: Requires behavioral, failure-path, and durable-seam evidence for tests and review. Use when writing tests, reviewing test coverage, assessing behavioral test quality, or accepting high-risk behavior on test evidence.
---

# Test verification

## Core rule

Tests prove behavior through public seams, not implementation internals.

A test that breaks when you rename an internal variable without changing behavior
is testing the wrong thing. A test that passes when the behavior is broken is
worse than no test at all.

## Vertical slice discipline

Write one test. Implement to pass it. Repeat.

Do not write all tests before all implementation (horizontal slicing). Tests
written before the code exists verify imagined behavior, become insensitive to
real changes, and outrun understanding.

```text
WRONG (horizontal):
  RED:   write all tests
  GREEN: write all implementation

RIGHT (vertical):
  RED → GREEN: one test → its implementation → repeat
```

For existing code where implementation already exists:

```text
diagnose → implement narrow vertical behavior → add targeted verification
```

## Test quality checklist

Before accepting a test as complete:

```text
[ ] Test describes behavior, not implementation details
[ ] Test uses a public seam: route, server action, query helper, or pure helper interface
[ ] Test would survive an internal refactor without changing
[ ] Code written is the minimum to pass the current test
[ ] No test written speculatively for behavior not yet implemented
[ ] Test covers at least one failure or rejection case, not just the happy path
[ ] For high-risk seams: failure path, wrong input, unauthorized access are covered
```

## Seam-specific test expectations

| Seam type | Minimum test coverage |
|---|---|
| Pure helper or validation | valid input, invalid input, unsafe or malformed input, edge cases |
| Parser | correct parse, rejection, precedence between command types |
| Dispatcher or readback builder | safe input → expected output, authority markers, unsafe input fails closed |
| Server action | authorized path, wrong project or role → denial, invalid input → failure, idempotency where relevant |
| Route boundary | method validation, body validation, auth and authority, fail-closed response shape |
| DB query helper | correct project-scoped read, wrong-project exclusion, missing record handling |
| Presentational component | renders given props correctly; does not fetch, store, or dispatch |
| Hook | hydration and effect behavior, pure helper tests where possible |
| Natural-language matcher or routing seam | generated class matrix across frames and objects, including guard and veto vocabulary in object position; directive-veto cases; mention and question negatives; verbatim failing deployed inputs |
| Rendered answer or readback surface | whole-answer pins for each state branch plus structural assertions banning stale or forbidden wording |

The natural-language matcher and routing seam row is load-bearing:
test the direction class, not only the first known phrase. Include adversarial
object-position vocabulary so a veto or guard does not accidentally reject the
operator's intended noun phrase.

## Fixture-vs-deployed divergence

If correctness depends on fields or environment values supplied by the actual
caller, fixture-only proof is not enough.

Examples:

- a shell caller passes readiness fields into a rendered answer builder
- a server action reads runtime configuration from `process.env`
- a routing seam receives mode, project, and thread context from the live send path
- a grounded packet uses rows read by the live assembler

When the live caller matters, the test or captured evidence must exercise the
real call path. Hand-shaped fixtures may supplement that proof, but they do not
replace it.

## Exactly-once and concurrency expectations

For state-changing record-family seams, include tests for:

- replay of the same request
- double-submit from the same UI path
- concurrent attempts where only one winner is allowed
- zero partial records after a losing or failed attempt

If the repository claims exactly-once behavior through a DB transaction or
unique constraint, tests must prove that property at the durable record seam,
not just through an in-memory guard.

## Sad-path acceptance gate (governed crossings)

Every new or changed **governed crossing**, meaning a server action or route
that records a decision, transitions a status, consumes a grant, or creates
lineage, requires an explicit **sad-path matrix** in the builder return. A crossing
whose changed behavior has only happy-path tests is an incomplete return, not
a reviewable one.

The matrix has one row per failure condition, with these columns:

| Failure condition | Expected refusal or result | Mutation-boundary guarantee (what did NOT happen) | Operator-visible readback | Test file proving it |
|---|---|---|---|---|

The mutation-boundary column states, per row, which effects were prevented: no
execution, no application, no repo change, no canonical-truth change, no
duplicate transition, as applicable to the crossing.

Baseline row set (the starting matrix for any governed crossing):

- malformed input
- unauthorized actor
- missing target record
- stale, already-decided, or duplicate action
- partial persistence failure
- external service failure
- secret-bearing error (redacted before it reaches UI, log, or readback)
- conflicting sibling or state
- happy-path regression after hardening

A row may be marked **not-applicable** with one line of reasoning (for
example, "no external service on this crossing"). An unexplained empty row is a gap, not a
pass. This gate applies to new and changed crossings from adoption forward; it
is not a retroactive audit of existing code.

## Source-string tests are guardrails only

Source-string tests check whether a string, import, or pattern appears in source
code. They are guardrails, not behavioral proof.

Use source-string tests for:
- proving a forbidden import is absent
- proving a file does not call `fetch`, `insert`, or a route directly
- protecting inertness and non-authority boundaries on contract-only seams
- checking that a display-only surface did not gain a forbidden action keyword

Do not use source-string tests alone for:
- command parsing behavior
- dispatch decisions
- validation output
- readback text selection
- server action success and failure paths
- route authorization
- state transition logic

When source-string tests are the only coverage for complex behavior, flag the
gap in the builder return and the reviewer should request behavioral tests.

## Database assertions

For persistence seams, asserting durable database state is the correct proof.

Prefer testing through public seams, such as routes, server actions, and
query helpers, rather than querying DB internals directly.

When persistence is the behavior being proven, assert the durable record exists
with the correct fields through the same query layer the app uses.

## What makes a bad test

- Tests a private function or internal helper directly
- Breaks when you rename an internal variable but behavior is unchanged
- Was written before the implementation existed and tests imagined structure
- Mocks internal collaborators instead of testing through the interface
- Passes when the actual behavior is broken
- Only tests the happy path when the seam has real failure modes
- Source-string assertion for complex behavior treated as full coverage

## Evaluator-side change handling

An evaluator-side change alters what declares pass: a test, fixture, threshold,
expected value, sample set, judge prompt, validation route, or evidence path.
An implementation-side change alters the behavior being measured.

**Evaluator-side and implementation-side changes must stay separately
inspectable**, so review can determine which one produced the green result. This
is a separability requirement on the record, not a limit on diff width; scope
rules govern how wide a change may be, not whether the two halves can be told
apart. Separate commits, separate sections of the return, or an explicit
before-and-after statement of the evaluator all satisfy it. A single undifferentiated
change that moves both halves at once does not.

Classify every evaluator-side change:

| Class | Meaning | Routing |
|---|---|---|
| `EVALUATOR_REPAIR` | the evaluator was wrong about the objective | fix it; state the objective or invariant it contradicted |
| `REQUIREMENT_CHANGE` | the definition of success itself changed | route through reconvergence, not through a quiet edit |
| `TESTABILITY_SUPPORT` | the seam was made testable without changing behavior | state the extraction (for example, a pure helper) and show behavior is unchanged |
| `COVERAGE_CHANGE` | which cases are measured or discovered changed | state what stopped being measured |
| `OBSERVABILITY_CHANGE` | logs, telemetry, reporting, or what reviewers see changed | state what became less visible |
| `UNRESOLVED` | the conflict was not settled | flag it in the return; the reviewing seat classifies the gap |

When the evaluator appears wrong: preserve the original failure and the
evaluator's identity, cite the objective or invariant it contradicts, classify
the change, route a changed success definition through reconvergence, **compare
old and new evaluator behavior on positive and negative controls**, and rerun the
original case plus one non-equivalent check. A positive control must still pass
and a negative control must still fail under the new evaluator; an evaluator
change that silences the negative control is a defect, not a repair.

## Non-equivalent discriminating evidence

Where the visible signal is controlled by the same change that is being
accepted, at least one check must be **non-equivalent** to that signal. Re-running
a second command over the same manipulated signal is not independent evidence.

Already owned elsewhere and referenced here rather than restated: re-running the
original failure, real-caller-path evidence (Fixture-vs-Deployed Divergence
above), a clean-baseline rerun, negative and denied-path proof for high-risk seams,
independent review, and owner verification on the real surface.

Options for the non-equivalent check:

- **held-out** inputs the change did not target;
- **counterfactual**: break the behavior on purpose and confirm the check fails;
- **metamorphic**: a transformation of the input whose expected effect on the
  output is known independently of the implementation;
- **property-based**: an invariant asserted over generated inputs rather than
  chosen ones; and
- **proxy perturbation**: perturb or hide the visible proxy and confirm the
  intended behavior still holds.

**Model-graded evaluators.** Where an LLM judge or model-scored rubric is
load-bearing and the executor can influence its input through text, the rubric
must be assembled or sanitized independently of executor-controlled text.
Candidate-supplied text must not reach the rubric, the grading instructions, or
the judge's notion of success unfiltered.

## Objective integrity, Level A

When a test, metric, rubric, benchmark, judge, or other proxy is load-bearing
for accepting a change, record three lines in the return before claiming
success:

```text
TRUE OBJECTIVE:
STRONGEST APPARENT-SUCCESS SHORTCUT:
DISCRIMINATING CHECK:
```

Passing a proxy is evidence about the objective, not proof the objective was
achieved. Name the strongest route by which the change could pass while
leaving the objective unmet, and the check that would catch it.

Stop at Level A when the discriminating check is already mandatory,
independent of this change, and capable of failing the strongest shortcut
named above.

**Materiality gate.** Technical editability alone never escalates routine
work. Being able to edit an in-tree test is not by itself a reason to
escalate, or every implementation would escalate. Repeated failure or budget
pressure raises scrutiny only when paired with a load-bearing evaluator this
change can modify. Pressure is a risk signal, never a diagnosis, and never a
claim about intent.

Escalate beyond Level A only when the Level A check is inadequate **and** a
material condition holds:

1. acceptance materially relies on an evaluator, environment, or evidence
   surface this change may modify under current scope;
2. the strongest plausible shortcut is not already defeated by a mandatory
   independent check;
3. the change touches a load-bearing evaluator, fixture, threshold, expected
   value, sample set, judge prompt, validation route, or evidence path;
4. the objective and the acceptance conditions appear mutually unsatisfiable;
5. observable evidence suggests evaluator gaming, environment tampering, or
   evidence shaping; or
6. a reviewer or pressure-tester requests it.

When escalation applies, load `reference/objective-integrity.md` for the
Level B decision model, escalation handling, and non-claim boundary. Do not
reconstruct those rules here.

## Return requirement

Include in the unified return block when this skill fires:

```text
Test verification:
- Seam type tested:
- Behavioral tests added: yes or no, with the list
- Failure or rejection path covered: yes or no
- Source-string tests used: yes or no; if used for complex behavior, flag the gap
- Test gaps remaining:
```
