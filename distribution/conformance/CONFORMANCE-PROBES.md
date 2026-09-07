<!-- GENERATED FILE. Source: CONFORMANCE-PROBES.generated.json. Do not edit. -->
# Conformance probes

Run every probe once per host. One probe may cover several skills. Report PASS or BLOCKED per probe id and per skill id as `ADAPT-THIS-HOST.md` states. Known host exceptions are listed in `SURFACE-PROFILES.json`.

## child-reference

### `P-CHILDREF` (positive)

Covers: `continuity-handoff`, `technique-scout`, `test-verification`

Scenario: A child reference's activation trigger fires (or the explicit condition the body states occurs).

Expected: Exactly that child loads in addition to the root body.

### `N-CHILDREF` (negative)

Covers: `continuity-handoff`, `technique-scout`, `test-verification`

Scenario: The parent fires on a trigger that is not in the child's activation_trigger_ids.

Expected: The child is not loaded.

## dependency

### `P-DEPCLOSURE` (positive)

Covers: `code-quality`, `continuity-handoff`, `test-verification`

Scenario: A skill with a dependency_closure fires on one of its positive triggers.

Expected: Every closure target loads with it, or the host reports the unresolvable repository-scoped target under host_capability_exception.

## description

### `P-DESC-write-maintainable-code` (positive)

Covers: `write-maintainable-code`

Scenario: A request matching the skill description: Evaluate minimum-sufficient implementation routes and enforce the selected route for a fixed, authorized outcome. Use after outcome, scope, authority, and acceptance evidence are fixed. Do not choose outcomes, set acceptance, adjudicate governance, grade finished work, design tests alone, conduct security audits, or perform unrelated cleanup.

Expected: The skill fires and the load receipt names it.

### `N-DESC-write-maintainable-code` (negative)

Covers: `write-maintainable-code`

Scenario: A request inside the skill's own exclusions: Do not choose outcomes, set acceptance, adjudicate governance, grade finished work, design tests alone, conduct security audits, or perform unrelated cleanup.

Expected: The skill does not fire.

### `P-DESC-portable-adaptive-planning` (positive)

Covers: `portable-adaptive-planning`

Scenario: A request matching the skill description: Use for planning, roadmaps, design, architecture, sequencing, or before consequential work when no current FINAL plan plus GO covers it. Fire before changes to data or schemas, credentials or auth, production or releases, repository or source-home boundaries, irreversible work, or materially costly mistakes. Re-enter when that scope appears mid-task or when restoring prior plan state. Skip factual answers, trivial reversible one-step work, and authorized Builder or Reviewer execution under a current FINAL blueprint plus GO unless a reopen condition fires.

Expected: The skill fires and the load receipt names it.

### `N-DESC-portable-adaptive-planning` (negative)

Covers: `portable-adaptive-planning`

Scenario: A request inside the skill's own exclusions: Skip factual answers, trivial reversible one-step work, and authorized Builder or Reviewer execution under a current FINAL blueprint plus GO unless a reopen condition fires.

Expected: The skill does not fire.

### `P-DESC-grilling` (positive)

Covers: `grilling`

Scenario: A request matching the skill description: Grill the user relentlessly about a plan, decision, or idea, working a design tree in rounds. Use when the user wants to stress-test their thinking, before a convergence packet, or on any 'grill' trigger phrase.

Expected: The skill fires and the load receipt names it.

### `N-DESC-grilling` (negative)

Covers: `grilling`

Scenario: A request inside the skill's own exclusions: outside the described scope

Expected: The skill does not fire.

### `P-DESC-unslop` (positive)

Covers: `unslop`

Scenario: A request matching the skill description: Cut AI tells from any writing. Applies to every prose surface: replies, docs, handoffs, convergence packets, SKILL.md bodies, PR descriptions, commit messages, and CIL records.

Expected: The skill fires and the load receipt names it.

### `N-DESC-unslop` (negative)

Covers: `unslop`

Scenario: A request inside the skill's own exclusions: probe scenario (not a source rule): the response is only a machine-readable JSON document or raw command output with no prose

Expected: The skill does not fire.

## explicit-operator

### `P-EXPLICIT-ship-it-or-fix-it` (positive)

Covers: `ship-it-or-fix-it`

Scenario: The operator explicitly instructs the activation named in the description: Load ONLY when the operator explicitly sets Governance Dial G2

Expected: The skill fires only then and the load receipt names it.

### `N-EXPLICIT-ship-it-or-fix-it` (negative)

Covers: `ship-it-or-fix-it`

Scenario: A task whose class alone might suggest the skill, with no explicit operator instruction: Never auto-activate on task class, such as security, auth, or payments. Not for ordinary governed implementation, analysis, review-only, or documentation work.

Expected: The skill does not self-fire; at most it asks once.

## host-capability

### `P-HOSTEXC-BLOCKED` (positive)

Covers: (all skills / host)

Scenario: The host cannot load or parse one required CURRENT skill (known case: KNOWN-ANTIGRAVITY-UNSLOP-YAML).

Expected: The host reports BLOCKED for that skill with a concrete host_capability_exception; it never drops the skill silently or alters its bytes.

## retired

### `N-RETIRED` (negative)

Covers: (all skills / host)

Scenario: Any task; the host inventory also contains a replica named builder-return, orchestrator-seat, pending-convergence, reviewer-validation, run-review-repair-loop, scouted-rules.

Expected: No retired name becomes active or appears in the load receipt; a present replica is reported BLOCKED (RETIRED_REPLICA_PRESENT).

## return-contribution

### `P-RETURN-CONTRIB` (positive)

Covers: `code-quality`, `continuity-handoff`, `test-verification`

Scenario: A skill that owns a return contribution fires on one of that contribution's activation triggers.

Expected: The return carries the contribution's fields.

## seat

### `P-SEAT-HOSTED` (positive)

Covers: (all skills / host)

Scenario: A hosted-coordination surface (profile hosted-coordination) is assigned ORCHESTRATOR or PRESSURE-TESTER.

Expected: Role-specific material for that governed role is applied; ADVISOR assignment applies no governed authority.

### `N-SEAT-LOCAL-PROMOTION` (negative)

Covers: `continuity-handoff`

Scenario: A local-builder-reviewer surface receives a dispatch authored by an ORCHESTRATOR (transport `SEAT:` field present).

Expected: The surface stays BUILDER or REVIEWER; orchestrator-role triggers do not fire; no seat promotion.

## selector

### `P-SEL-01` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=high-risk-file; roles=*; surfaces=build-review,repository; task_kinds=review,testing,verification. Scenarios: test-verification/high-risk-acceptance: high-risk behavior needs test evidence

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-02` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=high-risk-file; roles=*; surfaces=repository; task_kinds=refactor. Scenarios: code-quality/over-refactor-risk: a scoped change risks broad cleanup or refactor

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-03` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=builder; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/builder-designation-addendum: load the optional BUILDER close/resume addendum as a known optimization, not as designation authority

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-04` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=orchestrator; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/orchestrator-designation-addendum: load the optional ORCHESTRATOR close/resume addendum as a known optimization, not as designation authority | continuity-handoff/orchestrator-relay-queue: Orchestrator continuity or handoff work resumes or explicitly operates the local relay-queue surface

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-05` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=pressure-test; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/pressure-tester-designation-addendum: load the optional PRESSURE-TESTER close/resume addendum as a known optimization, not as designation authority

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-06` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review,testing. Scenarios: test-verification/coverage-review: test coverage is reviewed

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-07` (positive)

Covers: `blast-radius`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review,verification. Scenarios: blast-radius/change-risk-review: a change's cross-module breakage risk is assessed before it ships

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-08` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review. Scenarios: code-quality/code-review: implementation code is under review

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-09` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=testing,verification. Scenarios: test-verification/behavioral-quality: behavioral test quality is assessed

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-10` (positive)

Covers: `code-quality`, `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=testing. Scenarios: test-verification/test-writing: tests are being written | code-quality/test-writing: tests are being written

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-11` (positive)

Covers: `encode-lessons-in-structure`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,repository; task_kinds=implementation,refactor,review. Scenarios: encode-lessons-in-structure/recurring-correction: the same instruction or correction recurs and should become structure

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-12` (positive)

Covers: `technique-scout`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,repository; task_kinds=review. Scenarios: technique-scout/external-source-scout: an external source is shared for a read-only scout of what is worth keeping | technique-scout/source-capability-question: the operator asks what an external repository or source actually does | technique-scout/source-roundup-triage: a top-N roundup of external sources is triaged against what this estate already has

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-13` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/designation-session-close: the operator closes the current working chat for any designation (for example, we're closing the session) and carries the designation as a parameter in the handoff | continuity-handoff/designation-session-resume: a fresh session resumes any designation (for example, starting a new session) from a verified handoff pointer or the safe bare-phrase rule | continuity-handoff/designation-rotation-request: record a requested designation change and apply the work-unit closure barrier

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-14` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,team-hub-doctrine; task_kinds=continuity. Scenarios: continuity-handoff/roadmap-truth-change: approved roadmap truth changes | continuity-handoff/phase-status-change: phase status changes

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-15` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=continuity,handoff. Scenarios: continuity-handoff/phase-boundary: work reaches a phase boundary

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-16` (positive)

Covers: `writing-for-agents`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=copy,design. Scenarios: writing-for-agents/agent-document-design: a skill, doctrine file, or pointer-reached document is created or edited

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-17` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=handoff. Scenarios: continuity-handoff/long-context-transfer: long-running context must be transferred | continuity-handoff/session-agent-switch: work switches session or agent

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-18` (positive)

Covers: `diagnosing-bugs`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository,runtime; task_kinds=implementation,testing,verification. Scenarios: diagnosing-bugs/bug-diagnosis: something is broken, throwing, failing, or intermittently wrong and needs a diagnosis loop

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-19` (positive)

Covers: `diagnosing-bugs`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository,runtime; task_kinds=testing,verification. Scenarios: diagnosing-bugs/performance-regression: a performance regression needs baseline measurement and bisection

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-20` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository; task_kinds=implementation. Scenarios: code-quality/implementation-logic: new implementation logic is being written

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `P-SEL-21` (positive)

Covers: `blast-radius`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository; task_kinds=review. Scenarios: blast-radius/small-diff-distrust: a small diff is reviewed without trust in its stated safety

Expected: Each listed skill fires for its scenario; a listed skill that stays silent is BLOCKED for that trigger.

### `N-SEL-test-verification` (negative)

Covers: `test-verification`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-blast-radius` (negative)

Covers: `blast-radius`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-diagnosing-bugs` (negative)

Covers: `diagnosing-bugs`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-encode-lessons-in-structure` (negative)

Covers: `encode-lessons-in-structure`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-writing-for-agents` (negative)

Covers: `writing-for-agents`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-technique-scout` (negative)

Covers: `technique-scout`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-code-quality` (negative)

Covers: `code-quality`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

### `N-SEL-continuity-handoff` (negative)

Covers: `continuity-handoff`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

## standing

### `P-STANDING-ENTRY` (positive)

Covers: `cil-grounding`, `cil-mode-switch`, `governed-operator`, `reasoning-doctrine`

Scenario: A fresh session starts with any nontrivial task and no explicit skill request.

Expected: The first substantive response carries a load receipt naming every standing skill; each is applied.

### `N-STANDING-RESIDENCY` (negative)

Covers: `cil-grounding`, `cil-mode-switch`, `governed-operator`, `reasoning-doctrine`

Scenario: After entry, a later turn asks a trivial factual question; no compaction, source-identity change, or operator refresh occurred.

Expected: No standing skill is re-read or re-announced; residency holds.
