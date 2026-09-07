<!-- GENERATED FILE. Source: CONFORMANCE-PROBES.generated.json. Do not edit. -->
# Conformance probes

Account for every global ID. Execute only its generated profile and host applicability. Use the required execution modes and admission route in ADAPT-THIS-HOST.md.

## child-reference

### `P-CHILDREF` (positive)

Covers: `continuity-handoff`, `technique-scout`, `test-verification`

Scenario: A child reference's activation trigger fires (or the explicit condition the body states occurs).

Expected: Exactly that child loads in addition to the root body.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | technique-scout:canonical-target, test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | technique-scout:canonical-target, test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | technique-scout:blocked, test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-CHILDREF` (negative)

Covers: `continuity-handoff`, `technique-scout`, `test-verification`

Scenario: The parent fires on a trigger that is not in the child's activation_trigger_ids.

Expected: The child is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | technique-scout:canonical-target, test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | technique-scout:canonical-target, test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | technique-scout:blocked, test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter, technique-scout:canonical-target, test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

## dependency

### `P-DEPCLOSURE` (positive)

Covers: `code-quality`, `continuity-handoff`, `test-verification`

Scenario: A skill with a dependency_closure fires on one of its positive triggers.

Expected: Test each admitted owner and each applicable dependency edge in its required context. Resolve repo-grounding in Substrate 8 repository context; outside it, record REPOSITORY_CONTEXT_REQUIRED for that edge without failing unrelated firing probes.

Execution modes: repository-context

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked, continuity-handoff:blocked, test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

## description

### `P-DESC-write-maintainable-code` (positive)

Covers: `write-maintainable-code`

Scenario: A request matching the skill description: Evaluate minimum-sufficient implementation routes and enforce the selected route for a fixed, authorized outcome. Use after outcome, scope, authority, and acceptance evidence are fixed. Do not choose outcomes, set acceptance, adjudicate governance, grade finished work, design tests alone, conduct security audits, or perform unrelated cleanup.

Expected: The skill fires and the load receipt names it.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | write-maintainable-code:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | write-maintainable-code:canonical-target |
| external-host-adapter | grok | APPLICABLE | write-maintainable-code:blocked |
| hosted-coordination | chatgpt | APPLICABLE | write-maintainable-code:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | write-maintainable-code:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-DESC-write-maintainable-code` (negative)

Covers: `write-maintainable-code`

Scenario: A request inside the skill's own exclusions: Do not choose outcomes, set acceptance, adjudicate governance, grade finished work, design tests alone, conduct security audits, or perform unrelated cleanup.

Expected: The skill does not fire.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | write-maintainable-code:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | write-maintainable-code:canonical-target |
| external-host-adapter | grok | APPLICABLE | write-maintainable-code:blocked |
| hosted-coordination | chatgpt | APPLICABLE | write-maintainable-code:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | write-maintainable-code:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | write-maintainable-code:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-DESC-portable-adaptive-planning` (positive)

Covers: `portable-adaptive-planning`

Scenario: A request matching the skill description: Use for planning, roadmaps, design, architecture, sequencing, or before consequential work when no current FINAL plan plus GO covers it. Fire before changes to data or schemas, credentials or auth, production or releases, repository or source-home boundaries, irreversible work, or materially costly mistakes. Re-enter when that scope appears mid-task or when restoring prior plan state. Skip factual answers, trivial reversible one-step work, and authorized Builder or Reviewer execution under a current FINAL blueprint plus GO unless a reopen condition fires.

Expected: The skill fires and the load receipt names it.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | portable-adaptive-planning:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | portable-adaptive-planning:canonical-target |
| external-host-adapter | grok | APPLICABLE | portable-adaptive-planning:blocked |
| hosted-coordination | chatgpt | APPLICABLE | portable-adaptive-planning:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | portable-adaptive-planning:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-DESC-portable-adaptive-planning` (negative)

Covers: `portable-adaptive-planning`

Scenario: A request inside the skill's own exclusions: Skip factual answers, trivial reversible one-step work, and authorized Builder or Reviewer execution under a current FINAL blueprint plus GO unless a reopen condition fires.

Expected: The skill does not fire.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | portable-adaptive-planning:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | portable-adaptive-planning:canonical-target |
| external-host-adapter | grok | APPLICABLE | portable-adaptive-planning:blocked |
| hosted-coordination | chatgpt | APPLICABLE | portable-adaptive-planning:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | portable-adaptive-planning:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | portable-adaptive-planning:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-DESC-grilling` (positive)

Covers: `grilling`

Scenario: A request matching the skill description: Grill the user relentlessly about a plan, decision, or idea, working a design tree in rounds. Use when the user wants to stress-test their thinking, before a convergence packet, or on any 'grill' trigger phrase.

Expected: The skill fires and the load receipt names it.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | grilling:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | grilling:canonical-target |
| external-host-adapter | grok | APPLICABLE | grilling:blocked |
| hosted-coordination | chatgpt | APPLICABLE | grilling:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | grilling:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-DESC-grilling` (negative)

Covers: `grilling`

Scenario: A request inside the skill's own exclusions: outside the described scope

Expected: The skill does not fire.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | grilling:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | grilling:canonical-target |
| external-host-adapter | grok | APPLICABLE | grilling:blocked |
| hosted-coordination | chatgpt | APPLICABLE | grilling:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | grilling:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | grilling:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-DESC-unslop` (positive)

Covers: `unslop`

Scenario: A request matching the skill description: Cut AI tells from any writing. Applies to every prose surface: replies, docs, handoffs, convergence packets, SKILL.md bodies, PR descriptions, commit messages, and CIL records.

Expected: The skill fires and the load receipt names it.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | unslop:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | unslop:canonical-target |
| external-host-adapter | grok | APPLICABLE | unslop:blocked |
| hosted-coordination | chatgpt | APPLICABLE | unslop:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | unslop:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-DESC-unslop` (negative)

Covers: `unslop`

Scenario: A request inside the skill's own exclusions: probe scenario (not a source rule): the response is only a machine-readable JSON document or raw command output with no prose

Expected: The skill does not fire.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | unslop:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | unslop:canonical-target |
| external-host-adapter | grok | APPLICABLE | unslop:blocked |
| hosted-coordination | chatgpt | APPLICABLE | unslop:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | unslop:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | unslop:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

## explicit-operator

### `P-EXPLICIT-ship-it-or-fix-it` (positive)

Covers: `ship-it-or-fix-it`

Scenario: The operator explicitly instructs the activation named in the description: Load ONLY when the operator explicitly sets Governance Dial G2

Expected: The skill fires only then and the load receipt names it.

Execution modes: operator-authorized

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| external-host-adapter | grok | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:blocked |
| hosted-coordination | chatgpt | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| hosted-coordination | claude-web | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | agents | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | claude-code | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | codex | OPERATOR_ACTION_REQUIRED | ship-it-or-fix-it:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-EXPLICIT-ship-it-or-fix-it` (negative)

Covers: `ship-it-or-fix-it`

Scenario: A task whose class alone might suggest the skill, with no explicit operator instruction: Never auto-activate on task class, such as security, auth, or payments. Not for ordinary governed implementation, analysis, review-only, or documentation work.

Expected: The skill does not self-fire; at most it asks once.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | ship-it-or-fix-it:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | ship-it-or-fix-it:canonical-target |
| external-host-adapter | grok | APPLICABLE | ship-it-or-fix-it:blocked |
| hosted-coordination | chatgpt | APPLICABLE | ship-it-or-fix-it:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | ship-it-or-fix-it:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | ship-it-or-fix-it:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

## host-capability

### `P-HOSTEXC-BLOCKED` (positive)

Covers: (all skills / host)

Scenario: An isolated Antigravity parser fixture rejects canonical unslop frontmatter under KNOWN-ANTIGRAVITY-UNSLOP-YAML. No live skill root is modified.

Expected: The host reports BLOCKED for that skill with a concrete host_capability_exception; it never drops the skill silently or alters its bytes.

Execution modes: host-parser-fixture

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | NOT_APPLICABLE | none |
| local-builder-reviewer | claude-code | NOT_APPLICABLE | none |
| local-builder-reviewer | codex | NOT_APPLICABLE | none |

Use the machine row for exact reasons and child/contribution case IDs.

## retired

### `N-RETIRED` (negative)

Covers: (all skills / host)

Scenario: Any task; an isolated inventory fixture contains a replica named builder-return, orchestrator-seat, pending-convergence, reviewer-validation, run-review-repair-loop, scouted-rules.

Expected: No retired name becomes active or appears in the load receipt; a present replica is reported BLOCKED (RETIRED_REPLICA_PRESENT).

Execution modes: isolated-inventory-fixture

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | none |
| external-host-adapter | grok | APPLICABLE | none |
| hosted-coordination | chatgpt | APPLICABLE | none |
| hosted-coordination | claude-web | APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | none |
| local-builder-reviewer | claude-code | APPLICABLE | none |
| local-builder-reviewer | codex | APPLICABLE | none |

Use the machine row for exact reasons and child/contribution case IDs.

## return-contribution

### `P-RETURN-CONTRIB` (positive)

Covers: `code-quality`, `continuity-handoff`, `test-verification`

Scenario: A skill that owns a return contribution fires on one of that contribution's activation triggers.

Expected: The return carries the contribution's fields.

Execution modes: alternate-seat-session

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked, continuity-handoff:blocked, test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target, continuity-handoff:preserved-surface-adapter, test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

## seat

### `P-SEAT-HOSTED` (positive)

Covers: (all skills / host)

Scenario: A hosted-coordination surface (profile hosted-coordination) is assigned ORCHESTRATOR or PRESSURE-TESTER.

Expected: Role-specific material for that governed role is applied; ADVISOR assignment applies no governed authority.

Execution modes: alternate-seat-session

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | NOT_APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | APPLICABLE | none |
| hosted-coordination | claude-web | APPLICABLE | none |
| local-builder-reviewer | agents | NOT_APPLICABLE | none |
| local-builder-reviewer | claude-code | NOT_APPLICABLE | none |
| local-builder-reviewer | codex | NOT_APPLICABLE | none |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEAT-LOCAL-PROMOTION` (negative)

Covers: `continuity-handoff`

Scenario: A local-builder-reviewer surface receives a dispatch authored by an ORCHESTRATOR (transport `SEAT:` field present).

Expected: The surface stays BUILDER or REVIEWER; orchestrator-role triggers do not fire; no seat promotion.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | NOT_APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

## selector

### `P-SEL-01` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=high-risk-file; roles=*; surfaces=build-review,repository; task_kinds=review,testing,verification. Scenarios: test-verification/high-risk-acceptance: high-risk behavior needs test evidence

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-02` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=high-risk-file; roles=*; surfaces=repository; task_kinds=refactor. Scenarios: code-quality/over-refactor-risk: a scoped change risks broad cleanup or refactor

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-03` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=builder; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/builder-designation-addendum: load the optional BUILDER close/resume addendum as a known optimization, not as designation authority

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: alternate-seat-session

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | NOT_APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-04` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=orchestrator; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/orchestrator-designation-addendum: load the optional ORCHESTRATOR close/resume addendum as a known optimization, not as designation authority | continuity-handoff/orchestrator-relay-queue: Orchestrator continuity or handoff work resumes or explicitly operates the local relay-queue surface

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: alternate-seat-session

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | NOT_APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | NOT_APPLICABLE | none |
| local-builder-reviewer | claude-code | NOT_APPLICABLE | none |
| local-builder-reviewer | codex | NOT_APPLICABLE | none |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-05` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=pressure-test; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/pressure-tester-designation-addendum: load the optional PRESSURE-TESTER close/resume addendum as a known optimization, not as designation authority

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: alternate-seat-session

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | NOT_APPLICABLE | none |
| external-host-adapter | grok | NOT_APPLICABLE | none |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | NOT_APPLICABLE | none |
| local-builder-reviewer | claude-code | NOT_APPLICABLE | none |
| local-builder-reviewer | codex | NOT_APPLICABLE | none |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-06` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review,testing. Scenarios: test-verification/coverage-review: test coverage is reviewed

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-07` (positive)

Covers: `blast-radius`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review,verification. Scenarios: blast-radius/change-risk-review: a change's cross-module breakage risk is assessed before it ships

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | blast-radius:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | blast-radius:canonical-target |
| external-host-adapter | grok | APPLICABLE | blast-radius:blocked |
| hosted-coordination | chatgpt | APPLICABLE | blast-radius:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | blast-radius:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-08` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=review. Scenarios: code-quality/code-review: implementation code is under review

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-09` (positive)

Covers: `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=testing,verification. Scenarios: test-verification/behavioral-quality: behavioral test quality is assessed

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-10` (positive)

Covers: `code-quality`, `test-verification`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=build-review,repository; task_kinds=testing. Scenarios: test-verification/test-writing: tests are being written | code-quality/test-writing: tests are being written

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target, test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked, test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target, test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target, test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-11` (positive)

Covers: `encode-lessons-in-structure`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,repository; task_kinds=implementation,refactor,review. Scenarios: encode-lessons-in-structure/recurring-correction: the same instruction or correction recurs and should become structure

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | encode-lessons-in-structure:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | encode-lessons-in-structure:canonical-target |
| external-host-adapter | grok | APPLICABLE | encode-lessons-in-structure:blocked |
| hosted-coordination | chatgpt | APPLICABLE | encode-lessons-in-structure:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | encode-lessons-in-structure:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-12` (positive)

Covers: `technique-scout`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,repository; task_kinds=review. Scenarios: technique-scout/external-source-scout: an external source is shared for a read-only scout of what is worth keeping | technique-scout/source-capability-question: the operator asks what an external repository or source actually does | technique-scout/source-roundup-triage: a top-N roundup of external sources is triaged against what this estate already has

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | technique-scout:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | technique-scout:canonical-target |
| external-host-adapter | grok | APPLICABLE | technique-scout:blocked |
| hosted-coordination | chatgpt | APPLICABLE | technique-scout:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | technique-scout:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-13` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,team-hub-doctrine; task_kinds=continuity,handoff. Scenarios: continuity-handoff/designation-session-close: the operator closes the current working chat for any designation (for example, we're closing the session) and carries the designation as a parameter in the handoff | continuity-handoff/designation-session-resume: a fresh session resumes any designation (for example, starting a new session) from a verified handoff pointer or the safe bare-phrase rule | continuity-handoff/designation-rotation-request: record a requested designation change and apply the work-unit closure barrier

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| external-host-adapter | grok | APPLICABLE | continuity-handoff:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-14` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation,team-hub-doctrine; task_kinds=continuity. Scenarios: continuity-handoff/roadmap-truth-change: approved roadmap truth changes | continuity-handoff/phase-status-change: phase status changes

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| external-host-adapter | grok | APPLICABLE | continuity-handoff:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-15` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=continuity,handoff. Scenarios: continuity-handoff/phase-boundary: work reaches a phase boundary

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| external-host-adapter | grok | APPLICABLE | continuity-handoff:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-16` (positive)

Covers: `writing-for-agents`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=copy,design. Scenarios: writing-for-agents/agent-document-design: a skill, doctrine file, or pointer-reached document is created or edited

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | writing-for-agents:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | writing-for-agents:canonical-target |
| external-host-adapter | grok | APPLICABLE | writing-for-agents:blocked |
| hosted-coordination | chatgpt | APPLICABLE | writing-for-agents:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | writing-for-agents:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-17` (positive)

Covers: `continuity-handoff`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=documentation; task_kinds=handoff. Scenarios: continuity-handoff/long-context-transfer: long-running context must be transferred | continuity-handoff/session-agent-switch: work switches session or agent

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| external-host-adapter | grok | APPLICABLE | continuity-handoff:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-18` (positive)

Covers: `diagnosing-bugs`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository,runtime; task_kinds=implementation,testing,verification. Scenarios: diagnosing-bugs/bug-diagnosis: something is broken, throwing, failing, or intermittently wrong and needs a diagnosis loop

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | diagnosing-bugs:canonical-target |
| external-host-adapter | grok | APPLICABLE | diagnosing-bugs:blocked |
| hosted-coordination | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | diagnosing-bugs:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-19` (positive)

Covers: `diagnosing-bugs`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository,runtime; task_kinds=testing,verification. Scenarios: diagnosing-bugs/performance-regression: a performance regression needs baseline measurement and bisection

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | diagnosing-bugs:canonical-target |
| external-host-adapter | grok | APPLICABLE | diagnosing-bugs:blocked |
| hosted-coordination | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | diagnosing-bugs:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-20` (positive)

Covers: `code-quality`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository; task_kinds=implementation. Scenarios: code-quality/implementation-logic: new implementation logic is being written

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `P-SEL-21` (positive)

Covers: `blast-radius`

Scenario: Task selectors: lanes=*; risk_flags=*; roles=*; surfaces=repository; task_kinds=review. Scenarios: blast-radius/small-diff-distrust: a small diff is reviewed without trust in its stated safety

Expected: Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. Activation evidence is sufficient; domain-task completion is not required.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | blast-radius:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | blast-radius:canonical-target |
| external-host-adapter | grok | APPLICABLE | blast-radius:blocked |
| hosted-coordination | chatgpt | APPLICABLE | blast-radius:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | blast-radius:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-test-verification` (negative)

Covers: `test-verification`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | test-verification:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | test-verification:canonical-target |
| external-host-adapter | grok | APPLICABLE | test-verification:blocked |
| hosted-coordination | chatgpt | APPLICABLE | test-verification:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | test-verification:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | test-verification:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-blast-radius` (negative)

Covers: `blast-radius`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | blast-radius:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | blast-radius:canonical-target |
| external-host-adapter | grok | APPLICABLE | blast-radius:blocked |
| hosted-coordination | chatgpt | APPLICABLE | blast-radius:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | blast-radius:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | blast-radius:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-diagnosing-bugs` (negative)

Covers: `diagnosing-bugs`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | diagnosing-bugs:canonical-target |
| external-host-adapter | grok | APPLICABLE | diagnosing-bugs:blocked |
| hosted-coordination | chatgpt | APPLICABLE | diagnosing-bugs:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | diagnosing-bugs:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | diagnosing-bugs:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-encode-lessons-in-structure` (negative)

Covers: `encode-lessons-in-structure`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | encode-lessons-in-structure:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | encode-lessons-in-structure:canonical-target |
| external-host-adapter | grok | APPLICABLE | encode-lessons-in-structure:blocked |
| hosted-coordination | chatgpt | APPLICABLE | encode-lessons-in-structure:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | encode-lessons-in-structure:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | encode-lessons-in-structure:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-writing-for-agents` (negative)

Covers: `writing-for-agents`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | writing-for-agents:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | writing-for-agents:canonical-target |
| external-host-adapter | grok | APPLICABLE | writing-for-agents:blocked |
| hosted-coordination | chatgpt | APPLICABLE | writing-for-agents:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | writing-for-agents:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | writing-for-agents:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-technique-scout` (negative)

Covers: `technique-scout`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | technique-scout:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | technique-scout:canonical-target |
| external-host-adapter | grok | APPLICABLE | technique-scout:blocked |
| hosted-coordination | chatgpt | APPLICABLE | technique-scout:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | technique-scout:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | technique-scout:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-code-quality` (negative)

Covers: `code-quality`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | NOT_APPLICABLE | none |
| chatgpt-hosted-application | chatgpt-project | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | antigravity | APPLICABLE | code-quality:canonical-target |
| external-host-adapter | grok | APPLICABLE | code-quality:blocked |
| hosted-coordination | chatgpt | NOT_APPLICABLE | none |
| hosted-coordination | claude-web | NOT_APPLICABLE | none |
| local-builder-reviewer | agents | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | code-quality:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | code-quality:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-SEL-continuity-handoff` (negative)

Covers: `continuity-handoff`

Scenario: A task classified task_kind=architecture on surface=api with no risk flags, no role, no lane.

Expected: The skill does not fire; its body is not loaded.

Execution modes: ordinary-turn

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| external-host-adapter | grok | APPLICABLE | continuity-handoff:blocked |
| hosted-coordination | chatgpt | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| hosted-coordination | claude-web | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | agents | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | claude-code | APPLICABLE | continuity-handoff:preserved-surface-adapter |
| local-builder-reviewer | codex | APPLICABLE | continuity-handoff:preserved-surface-adapter |

Use the machine row for exact reasons and child/contribution case IDs.

## standing

### `P-STANDING-ENTRY` (positive)

Covers: `cil-grounding`, `cil-mode-switch`, `governed-operator`, `reasoning-doctrine`

Scenario: A fresh session starts with any nontrivial task and no explicit skill request.

Expected: The first substantive response carries a load receipt naming every standing skill; each is applied.

Execution modes: fresh-session-entry

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| external-host-adapter | grok | APPLICABLE | cil-grounding:blocked, cil-mode-switch:blocked, governed-operator:blocked, reasoning-doctrine:blocked |
| hosted-coordination | chatgpt | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.

### `N-STANDING-RESIDENCY` (negative)

Covers: `cil-grounding`, `cil-mode-switch`, `governed-operator`, `reasoning-doctrine`

Scenario: After entry, a later turn asks a trivial factual question; no compaction, source-identity change, or operator refresh occurred.

Expected: No standing skill is re-read or re-announced; residency holds.

Execution modes: later-turn-residency

| Profile | Host | Applicability | Candidate owners |
|---|---|---|---|
| chatgpt-hosted-application | chatgpt | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| chatgpt-hosted-application | chatgpt-project | NOT_APPLICABLE | none |
| external-host-adapter | antigravity | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| external-host-adapter | grok | APPLICABLE | cil-grounding:blocked, cil-mode-switch:blocked, governed-operator:blocked, reasoning-doctrine:blocked |
| hosted-coordination | chatgpt | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| hosted-coordination | claude-web | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | agents | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | claude-code | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |
| local-builder-reviewer | codex | APPLICABLE | cil-grounding:canonical-target, cil-mode-switch:canonical-target, governed-operator:canonical-target, reasoning-doctrine:canonical-target |

Use the machine row for exact reasons and child/contribution case IDs.
