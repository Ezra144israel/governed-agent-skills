---
metadata_schema: team-hub-skill/v1
summary: Preserves approved truth, detects drift, and runs governed designation session close, resume, and rotation handoffs across sessions and agents.
skill_id: continuity-handoff
version: 1.5.0
lifecycle_status: active
family: continuity
capabilities: []
source_provenance:
  kind: original
  references: []
  note: null
authority_boundary: docs-only
activation_triggers:
- trigger_id: roadmap-truth-change
  task_kinds:
  - continuity
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: approved roadmap truth changes
- trigger_id: phase-status-change
  task_kinds:
  - continuity
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: phase status changes
- trigger_id: long-context-transfer
  task_kinds:
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  description: long-running context must be transferred
- trigger_id: session-agent-switch
  task_kinds:
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  description: work switches session or agent
- trigger_id: phase-boundary
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  description: work reaches a phase boundary
- trigger_id: designation-session-close
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: the operator closes the current working chat for any designation (for example, we're closing the session) and carries the designation as a parameter in the handoff
- trigger_id: designation-session-resume
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: a fresh session resumes any designation (for example, starting a new session) from a verified handoff pointer or the safe bare-phrase rule
- trigger_id: designation-rotation-request
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: record a requested designation change and apply the work-unit closure barrier
- trigger_id: builder-designation-addendum
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles:
  - builder
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: load the optional BUILDER close/resume addendum as a known optimization, not as designation authority
- trigger_id: orchestrator-designation-addendum
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles:
  - orchestrator
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: load the optional ORCHESTRATOR close/resume addendum as a known optimization, not as designation authority
- trigger_id: orchestrator-relay-queue
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles:
  - orchestrator
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: Orchestrator continuity or handoff work resumes or explicitly operates the local relay-queue surface
- trigger_id: pressure-tester-designation-addendum
  task_kinds:
  - continuity
  - handoff
  risk_flags: []
  path_globs: []
  roles:
  - pressure-test
  lanes: []
  surfaces:
  - documentation
  - team-hub-doctrine
  description: load the optional PRESSURE-TESTER close/resume addendum as a known optimization, not as designation authority
activation_exclusions: []
full_load_required_when:
- designation-rotation-request
- designation-session-close
- designation-session-resume
- long-context-transfer
- phase-boundary
- phase-status-change
- roadmap-truth-change
- session-agent-switch
section_references: []
platforms:
- portable
- team-hub-runtime-advisory
surfaces:
- documentation
- team-hub-doctrine
required_roles: []
required_lanes: []
related_doctrine:
- docs/handoffs/ACTIVE-READ-ORDER.md
- docs/handoffs/NEXT-CHAT-ENTRYPOINT-AND-ACTIVE-DIRECTION.md
graph_edges:
- type: depends_on
  target: repo-grounding
  condition_trigger_ids: []
child_references:
- child_id: continuity-handoff/builder-session
  path: skills/continuity-handoff/reference/builder-session.md
  lifecycle_status: active
  platforms:
  - portable
  - team-hub-runtime-advisory
  surfaces:
  - documentation
  - team-hub-doctrine
  activation_trigger_ids:
  - builder-designation-addendum
  full_load_trigger_ids:
  - builder-designation-addendum
  contributes_return_ids:
  - continuity-handoff/session-handoff
  independently_invocable: false
  content_origin: authored
- child_id: continuity-handoff/orchestrator-session
  path: skills/continuity-handoff/reference/orchestrator-session.md
  lifecycle_status: active
  platforms:
  - portable
  - team-hub-runtime-advisory
  surfaces:
  - documentation
  - team-hub-doctrine
  activation_trigger_ids:
  - orchestrator-designation-addendum
  full_load_trigger_ids:
  - orchestrator-designation-addendum
  contributes_return_ids:
  - continuity-handoff/session-handoff
  independently_invocable: false
  content_origin: authored
- child_id: continuity-handoff/relay-queue
  path: skills/continuity-handoff/reference/relay-queue.md
  lifecycle_status: active
  platforms:
  - portable
  - team-hub-runtime-advisory
  surfaces:
  - documentation
  - team-hub-doctrine
  activation_trigger_ids:
  - orchestrator-relay-queue
  full_load_trigger_ids:
  - orchestrator-relay-queue
  contributes_return_ids:
  - continuity-handoff/session-handoff
  independently_invocable: false
  content_origin: authored
- child_id: continuity-handoff/pressure-tester-session
  path: skills/continuity-handoff/reference/pressure-tester-session.md
  lifecycle_status: active
  platforms:
  - portable
  - team-hub-runtime-advisory
  surfaces:
  - documentation
  - team-hub-doctrine
  activation_trigger_ids:
  - pressure-tester-designation-addendum
  full_load_trigger_ids:
  - pressure-tester-designation-addendum
  contributes_return_ids:
  - continuity-handoff/session-handoff
  independently_invocable: false
  content_origin: authored
return_contributions:
- contribution_id: continuity-handoff/continuity
  activation_trigger_ids:
  - roadmap-truth-change
  - phase-status-change
  - long-context-transfer
  - session-agent-switch
  - phase-boundary
  requirement: required
  order: 600
  fields:
  - field_id: truth-state
    value_type: string
    required: true
    allowed_values: []
    prompt: State current approved truth, phase, and outstanding divergence.
  - field_id: handoff-artifact
    value_type: path-list
    required: true
    allowed_values: []
    prompt: List the durable handoff or continuity artifacts.
  - field_id: resume-boundary
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record completed, blocked, next, and explicit do-not items.
- contribution_id: continuity-handoff/session-handoff
  activation_trigger_ids:
  - designation-session-close
  - designation-session-resume
  requirement: required
  order: 650
  fields:
  - field_id: starter-pointer
    value_type: string
    required: true
    allowed_values: []
    prompt: State the immutable starter pointer line, appending the blocked status marker when the close is blocked.
  - field_id: handoff-identity
    value_type: string
    required: true
    allowed_values: []
    prompt: State the handoff Relay path, full Git blob FILE_SHA, full SHA-256, and exact byte count, plus any load-bearing local path.
  - field_id: root-map
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Confirm the ROOT MAP records every locked root, surface, path-kind, and identity field.
  - field_id: location-ledger
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Confirm every load-bearing item has a complete nine-column location-ledger row.
  - field_id: continuity-state
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record completed, current, blocked, next action, the one after, and explicit do-not items.
  - field_id: cil-grounding-gate
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record that live CIL Mode Reset, five-slot bootstrap, role onboarding, and activation must precede substantive resume work.
- contribution_id: continuity-handoff/seat-rotation
  activation_trigger_ids:
  - designation-session-close
  - designation-session-resume
  - designation-rotation-request
  - session-agent-switch
  requirement: required
  order: 700
  fields:
  - field_id: work-unit-id
    value_type: string
    required: true
    allowed_values: []
    prompt: Record the stable identity of the current governed work unit.
  - field_id: work-unit-state
    value_type: enum
    required: true
    allowed_values:
    - active
    - complete
    - blocked
    - failed
    - reconvergence-required
    prompt: Record the current work-unit disposition.
  - field_id: rotation-state
    value_type: enum
    required: true
    allowed_values:
    - none
    - pending
    - released
    prompt: Record whether designation rotation is absent, requested, or released.
  - field_id: current-executor
    value_type: string
    required: true
    allowed_values: []
    prompt: Record the actor currently executing the unit without treating identity as a standing designation.
  - field_id: current-designation
    value_type: string
    required: true
    allowed_values: []
    prompt: Record the current uppercase per-slice designation.
  - field_id: authorship-ledger
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record artifact-specific authorship and review-disqualification lineage.
  - field_id: next-step
    value_type: string
    required: true
    allowed_values: []
    prompt: Record the next executable action under the current work unit and authority.
  - field_id: recovery-boundary
    value_type: checklist
    required: true
    allowed_values: []
    prompt: Record the exact resume point, pending authority, and do-not boundaries.
supersedes: []
---

# continuity-handoff/SKILL.md

**Status:** Active Team Hub OS skill. Active as documentation/skill guidance when loaded by the governed workflow. It is not runtime enforcement authority.

## Purpose

This skill defines how continuity work preserves stable truth across chat sessions, agent interactions, and development days.

Status note: the dedicated Continuity Agent role is pre-wiring unless a current
slice proves live wiring. The role exists in doctrine; the practices in this
skill remain binding on whoever performs continuity work.

It prevents session amnesia, specification drift, lost architectural decisions, and handoffs that force the next agent to work from stale or incomplete context.

Continuity work is not implementation work. It is truth preservation, handoff preparation, and drift detection.

This skill also defines the **governed designation session close, resume, and rotation contract**: the operator's short close phrase produces one immutable, location-complete handoff pointer, and the short resume phrase safely grounds and continues any valid designation from that pointer. See [Governed Seat Session Close and Resume](#governed-seat-session-close-and-resume) below; the `seat` label remains for compatibility, while the three child references are optional known-designation addenda.

## Core Rule

The continuity role does not write implementation code.

Its role is to:

1. Preserve approved decisions.
2. Detect documentation drift.
3. Update stable docs when approved truth changes.
4. Generate or update the active handoff/read-order artifact required by the repo workflow.
5. Ensure the next agent has a grounded, actionable starting point.

The Continuity Agent must separate:

- approved decisions
- observed implementation facts
- open questions
- unresolved conflicts
- recommendations

Only approved decisions become stable truth.

## When This Skill Applies

Use this skill:

- at the end of a significant coding session
- at the end of a significant architectural discussion
- when a task is marked complete and accepted
- when a task is blocked and needs operator decision
- when transferring work between agent classes, such as Architect → Builder or Builder → Reviewer
- when stable docs conflict with current accepted implementation
- when the active read order or handoff would otherwise become stale

## Continuity Responsibilities

### 1. Preserve Approved Decisions

If an architectural choice, security protocol, release rule, agent role rule, or workflow rule is approved during a session, the Continuity Agent must ensure it is captured in the appropriate stable doc or handoff artifact.

Do not leave approved decisions only in chat context.

If it is stable truth, it must live in a stable file.

## Architecture Decision Records

When a significant architectural choice is made during a session, evaluate whether it warrants an ADR.

Builders flag ADR candidates in builder returns. Continuity agents create the actual ADRs.

### Three-criteria filter

Only create an ADR when ALL THREE are true:

1. **Hard to reverse** - changing this later has real cost
2. **Surprising without context** - future agents will wonder why
3. **Real trade-off** - genuine alternatives existed and were weighed

If any is missing, record the decision in the active handoff only.
Do not create an ADR for implementation details, temporary choices, or decisions already fully captured by existing contracts or specs.

### ADR creation process

When all three criteria are met:

1. Check `docs/adr/` for existing ADRs on this topic.
   If one exists and the context has changed, supersede it.
   If one exists and context has not changed, point to it.

2. Create `docs/adr/[NNNN]-[slug].md` using the ADR template.

3. Link the new ADR from the active handoff document.

4. Update the related docs field with any governing contracts or specs.

### What ADRs do not replace

ADRs do not replace:
- Phase handoff documents
- Contract specs (Runtime Foundation, Bridge, etc.)
- Phase lock documents
- The canonical spec index

ADRs are lightweight single-decision records that make specific choices discoverable. The governing authority for a decision area remains in the relevant spec or lock document.


### 2. Detect and Repair Specification Drift

Continuity must compare:

- current accepted code
- builder return packet
- reviewer validation result
- stable docs
- active handoff/read-order
- operator-approved decisions

If pushed code contradicts documentation, do not automatically normalize the docs to the code.

Use this rule:

```text
Verified repo truth beats memory.
Approved product truth beats accidental implementation.
```

If the code passed Reviewer Validation and reflects approved product truth, update the relevant documentation.

If the code conflicts with approved product truth, flag the drift and do not rewrite stable docs to match the bad implementation.

If the source of truth is unclear, mark the issue as a conflict and escalate.

### 3. Maintain the Active Handoff / Read Order

Before a work transfer or session close, the Continuity Agent should generate or update the active handoff/read-order artifact used by the repo workflow.

The handoff must tell the next agent:

- current project state
- last accepted action
- next immediate task
- required read order
- active seam
- known constraints
- protected paths
- unresolved blockers
- latest pushed branch/commit when available

### 4. Preserve Role Boundaries

Continuity may document, clarify, and route.

Continuity may not:

- implement code
- silently revise product direction
- invent new roadmap phases
- approve work that the reviewer blocked
- turn observations into stable truth
- bypass store/privacy/security gates
- rewrite law docs unless the change reflects approved truth

## Handoff Generation Format

Use this structure when creating or updating the active handoff/read-order artifact:

```md
# Active Handoff

## Current State

<One-sentence summary of where the project stands right now.>

## Last Accepted Action

<What was finished, accepted, and by whom: Builder, Reviewer, Architect, or Operator.>

## Next Immediate Task

<Clear, actionable description of what the next agent needs to do.>

## Active Seam

<Exact files, routes, components, docs, or subsystem expected to be touched.>

## Required Read Order

To execute the next task, the agent must read these files in this exact order:

1. `path/to/relevant/skill.md`
2. `path/to/governing/doc.md`
3. `path/to/specific/code_or_doc_file`

## Known Constraints & Warnings

- <Active blocker, risk, or protected path.>
- <Specific file or subsystem the next agent should not touch.>

## Store / Privacy / Security Notes

- Store Impact: Yes / No / Needs review
- Security-sensitive path: Yes / No / Needs review
- Required artifacts to read or update:
  - `<path>`

## Unresolved Questions

- <Question requiring operator, architect, or reviewer decision.>

## Latest Pushed State

Branch: `<branch-name>`
Commit: `<commit-hash or pushed state>`
```

## Hard Gates for Continuity

The Continuity Agent must block or flag the handoff if:

- previous work was marked complete but Reviewer Validation returned Needs Revision or Blocked
- Store Impact is unresolved
- security impact is unresolved
- stable docs conflict and source of truth is unclear
- the required read order omits files needed for the next task
- the next task touches store/privacy artifacts but the read order omits those artifacts
- the next task touches security-sensitive paths but the read order omits `security/SKILL.md`
- the active seam is unclear
- the latest pushed repo state is unknown for implementation handoff
- the handoff would cause the next agent to work from chat context alone

If blocked, return:

```text
Status: Blocked

Reason:
<clear reason>

Needed to proceed:
<operator decision, reviewer result, repo state, file path, or artifact update required>
```

## Conflict Handling

If two stable docs disagree, do not guess.

Return:

```text
Continuity Conflict:
- File A says: <claim>
- File B says: <claim>
- Current repo/code says: <claim, if verified>
- Reviewer/Operator decision found: Yes / No
- Recommended resolution: <specific recommendation or “operator decision required”>
```

Do not silently choose one source unless the governing hierarchy is explicit.

## Non-Goals

The Continuity Agent must not:

- write implementation code
- fix bugs discovered during handoff
- create unapproved roadmap items
- expand scope
- summarize casual brainstorming as stable truth
- convert unreviewed implementation into doctrine
- treat memory as more authoritative than verified repo files
- bypass Reviewer Validation
- bypass Store Impact, security, or grounding requirements

## Governed Seat Session Close and Resume

This contract lets the operator close a working chat with one short phrase, receive one immutable location-complete handoff pointer, paste that pointer into a fresh session of any valid designation, and resume without restating the task or answering avoidable file-path questions.

The rules in this section are the **shared invariants** for every designation. The first three references below are optional known-designation addenda loaded progressively; they are not the complete designation set. The fourth is the progressive relay-queue protocol:

- `continuity-handoff/builder-session` — `skills/continuity-handoff/reference/builder-session.md`
- `continuity-handoff/pressure-tester-session` — `skills/continuity-handoff/reference/pressure-tester-session.md`
- `continuity-handoff/orchestrator-session` — `skills/continuity-handoff/reference/orchestrator-session.md`
- `continuity-handoff/relay-queue` — `skills/continuity-handoff/reference/relay-queue.md`; load only for Orchestrator resume when relay-queue work is active or for explicit local relay-queue work.

The compatibility field and pointer label remain `seat`, but the value is the current per-slice designation, not a permanent actor class. A valid designation uses uppercase kebab case matching `[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*`; membership is open. Schema `ROLES` values are optional known-addendum selectors, never designation-membership authority. The generic close/resume trigger loads this full shared body for every valid designation. `BUILDER`, `PRESSURE-TESTER`, and `ORCHESTRATOR` additionally select exactly their matching addendum; an unknown valid designation such as `REVIEWER` or `AUDITOR-2` selects no child, proceeds normally, and records `designation addendum: NONE`. An invalid token fails without guessing, inventing a role mapping, or loading every child.

### Universal CIL grounding gate

Every continuity handoff and every resumed designation is fail-closed on live CIL
activation. This rule applies equally to ChatGPT, Claude, Claude Code, Codex,
Gemini, web, desktop, CLI, terminal, and any future or unknown agent.

Before reading substantive handoff content or taking any project-facing action, the
resumed agent must use the live CIL connector and:

1. perform the Mode Reset from `STARTUP.md` — enter CIL to be changed by it,
   not merely to understand or summarize it;
2. complete the five-slot bootstrap: `STATUS.md`,
   `session-handoff/current.md`, exactly one designation/role-matched onboarding
   file, the operator-priority slot, and the latest meaningful activity entries;
3. load a matching branch note only when the agent is a named branch or the
   resolved delta requires it;
4. resolve the behavior delta — what the agent will do differently because of
   the active CIL records;
5. complete one relevant activation action before its first operator-facing
   response; and
6. carry the Application Gate throughout the resumed session: when a CIL record
   fires, apply it, rule it out with reason, or challenge/qualify it.

Only the minimum actions needed to parse the starter pointer, locate and verify the
handoff identity without substantive access, and reach the live CIL connector may
precede this gate. If CIL or a load-bearing bootstrap slot is unavailable, stale
beyond safe use, or contradictory, the agent must stop substantive continuation and
return the exact blocker and recovery needed. It must not proceed from memory,
narration, a prior summary, or the project handoff alone.

Every newly generated handoff must contain a `CIL GROUNDING GATE` section before
its `ROOT MAP`. That section records:

- `state_at_close: REQUIRED_ON_RESUME`;
- the live CIL connector name and the CIL repository identity;
- the mandatory bootstrap sources and matching onboarding selection rule;
- `first_response_shape: activation action completed + current delta + preserved boundary`;
- `failure_behavior: BLOCK SUBSTANTIVE RESUME`; and
- the explicit statement that CIL activation is not project authority and does
  not replace independent grounding from project origin.

A readiness statement, CIL summary, handoff summary, or claim that CIL was read is
not satisfaction evidence. Work produced before this gate completes is ungrounded
and cannot authorize downstream implementation, review acceptance, commit,
publication, deployment, or production action.

### Intent triggers are not authority

The close, resume, and rotation phrases are working-chat intent triggers only. No such phrase authorizes a builder return, review verdict, operator lock, staging, commit, push, PR, approval, merge, deployment, relay cleanup, external message, or CIL write. A handoff is a continuity pointer, never repository or canonical truth. A resumed session must not treat `latest` as `accepted`, a builder self-review as independent approval, a prior `proceed` as a later mutation authorization, or a new chat as erasing authorship restrictions. Role integrity is artifact-specific: designation history or prior advisory participation alone is not a conflict; a conflict exists when the proposed reviewer authored the implementation candidate or another load-bearing artifact whose correctness that review would approve.

### Activation phrases and product-session disambiguation

Close behavior activates on working-chat close intent such as `we're closing the session`, `close this session`, `write the session handoff`, and `handoff to a new session`. Resume behavior activates on `starting a new session`, `resume this session`, and `continue from handoff`.

These phrases refer to the current working agent/chat session. If the conversation is discussing, quoting, testing, or operating a product feature whose domain language includes `session`, `close this session`, `new session`, or `closed sessions`, confirm that the operator means the working agent/chat before activating a handoff close. Quoted test copy or product UI instructions must not trigger handoff creation, and a product-surface action is never inferred from a handoff phrase. An unambiguous first-person working-chat statement such as `we're closing this chat; write the handoff` may proceed directly without a redundant question.

### Immutable handoff location and naming

For Relay-mediated session continuity, immutable handoffs live in:

`relay/handoffs/` inside `Ezra144israel/operator-agent-relay`

Deposits there follow the governed Relay standards: create-once, never
overwritten, superseded only by a new version file. A duplicate operator-local
handoff file is not required and is never a universal prerequisite; a local
project continuity artifact may still exist for a separate current purpose, but
it is not a mandatory mirror of the Relay handoff. Historical local handoffs
and Relay mirrors remain immutable provenance, and the absence of a retired
local duplicate is not drift and never reopens completed work.

Each handoff is immutable and named:

`<task-key>--<seat>--handoff-v<integer>--<head8>.md`

For a new handoff, `<seat>` carries the uppercase designation token verbatim; the body and starter pointer use that same token. Thus `BUILDER`, `PRESSURE-TESTER`, `REVIEWER`, and `AUDITOR-2` remain uppercase in their filename component. Existing lowercase filenames are historical and remain tolerated and untouched. A later handoff supersedes an earlier one through the `supersedes` field; it never overwrites it. `<head8>` is a **filename locator only**. It is never accepted as artifact, commit, base, or head identity. The handoff body, starter pointer, root map, and location ledger must retain the full 64-character SHA-256 and full Git object identities everywhere they are load-bearing.

Every handoff body must record the complete header field set: `handoff_id`, `task_key`, `seat`, `version`, `created_at`, `repo` (identity), `branch`, `base`, `head`, `status`, and `supersedes`, with `repo`, `branch`, `base`, and `head` carrying project identity whenever project work is in scope. `repo_root_hint` and `worktree` are device facts: record them when a later safe action genuinely depends on that device location, and otherwise record `NONE` or `NOT VISIBLE ON THIS SURFACE` without treating that as a gap. These fields are in addition to — never a substitute for — the `ROOT MAP` and `LOCATION LEDGER` below. A blocked close carries the same header set with its `status` set to the blocked value.

### Root map

Every handoff must contain a `ROOT MAP` before its location ledger. The map must distinguish a canonical device checkout from an isolated builder worktree, a package/application root, a relay root, and any external attachment or additional repository root. It may not label two different roots merely `repo`.

Assign every recorded root a `surface_id` and a `path_kind`, one of `DEVICE_ABSOLUTE`, `SURFACE_ABSOLUTE`, `REPO_RELATIVE`, `ATTACHMENT_ABSOLUTE`, or `EXTERNAL_REFERENCE`. For each repository used, record:

- `surface_id` — stable label such as `operator-device`, `builder-worktree`, or `claude-bridge-shell`;
- `repository_identity` — exact `owner/repository` plus origin URL when Git-owned;
- `device_absolute_root` — literal device path, or `NOT VISIBLE ON THIS SURFACE`;
- `surface_absolute_root` — literal root usable by the current shell, or `NO SHELL ACCESS`;
- `repo_relative_anchor` — `.` after repository identity is verified;
- `expected_ref_or_object` — full base/head identity used to reject the wrong checkout;
- `valid_for` — the tools/surfaces for which each literal root was verified.

The `ROOT MAP` must additionally record, in the map itself and not only elsewhere in the body, the exact identities needed to re-ground: the project repository identity and its current ref where project work is in scope; the Relay repository identity and the handoff's Relay path and identity; every load-bearing artifact identity; pending return paths when they are part of the resumed work; and this handoff's `branch`, `base`, `head`, and expected remote reference. Distributing these into the starter pointer or ledger alone does not satisfy the requirement.

A device absolute root — a device repository root, isolated-worktree root, package/application root, or local relay root — is required only when a later safe action genuinely depends on that device location. A hosted or connector-only session records `NOT VISIBLE ON THIS SURFACE` for a device path it cannot see, and that entry is never by itself a blocker when the next safe action does not use it.

`NONE` is allowed when a surface genuinely does not exist; `NOT VISIBLE ON THIS SURFACE` is allowed when the current surface cannot see a device path. `UNKNOWN`, a blank field, or an unresolved genuinely load-bearing root is a close blocker (see [Blocked close](#blocked-close-preserves-continuity)).

### Location ledger

Every load-bearing or mentioned input, output, governing artifact, working file, dispatch, return, review, lock, publication record, deployment record, walk record, attachment, and pending return path must have one row in a `LOCATION LEDGER`. Each row records:

| Field | Required meaning |
| --- | --- |
| Purpose | What the next session needs the item for |
| Authority/status | `LOCKED`, `INPUT`, `OUTPUT`, `WORKING`, `SOURCE`, `PENDING`, or `HISTORICAL` |
| Absolute path | Full path from the filesystem root |
| Repo-relative path | Exact path from the identified repository root, or `EXTERNAL` |
| Source surface | `origin/main@<full-sha>`, working tree, index, relay, attachment, or named external source |
| SHA-256 | Full 64-character digest for existing load-bearing files; `PENDING` only for a return path proved absent |
| Bytes | Exact byte count for existing files; `PENDING` only for a return path proved absent |
| Existence | `EXISTS` or `ABSENT VERIFIED <timestamp>` |
| Repo state | `CLEAN`, `MODIFIED`, `UNTRACKED`, `STAGED`, `MIXED`, or `NOT REPO-OWNED` |

For a mutable working file, hash the exact close-time bytes and label the state honestly. For an `origin/main` source, take identity from the named commit, not from dirty working-tree bytes. A pending immutable output needs its exact absolute and repo-relative target path plus the verified-absent result.

The ledger may not use basenames without directories, ellipses or abbreviated paths, digest prefixes in place of full digests, `same as above`/`usual relay`/`current repo`-style inference, paths that require concatenating undocumented roots, or a file named only in prose and omitted from the ledger.

A `HISTORICAL` row may avoid re-hashing an unchanged historical artifact only when it cites the artifact's exact absolute and repo-relative paths, its full SHA-256 and exact bytes, the exact immutable authority/return record that previously pinned that identity (itself named by path, full SHA-256, and bytes), and a read-only existence check at close time. Any path drift, missing file, inconsistent pin, mutable source, or use in the next executable action promotes the row to `INPUT` and requires close-time identity verification.

### Command and check location contract

Every resume command or evidence check must be listed in a table carrying, in order: `sequence` (the ordinal that fixes execution order), `purpose` (why the row exists), `recorded_surface_id`, `recorded_surface_absolute_cwd`, `repository_identity`, `repo_relative_cwd`, the exact command or non-shell action, the expected safe result, and the stop condition. The `sequence` and `purpose` columns are mandatory: without them a resumed session cannot reproduce a multi-command continuation deterministically or know why a row exists. No command may depend on the reader remembering which root a prior paragraph called `the repo`; device-relay commands and isolated-worktree commands carry their different working directories. Listing a command preserves an already authorized next action and its gate — it never converts a pending commit, push, merge, deployment, cleanup, external message, or CIL mutation into authority.

On the same execution surface, use the verified surface-absolute path. On a different surface — a Claude bridge, container, cloud workspace, or new isolated worktree — do not execute the stale literal path. Instead discover a root with the recorded `repository_identity` through bounded read-only discovery, verify the `expected_ref_or_object` and reject a mismatched repository, re-root the `repo_relative_cwd` onto that surface's verified repository root, verify the resulting directory exists, and execute only after all original authority gates still pass. File-transfer tools may use a device or attachment path the shell cannot use; name that tool/surface validity in `valid_for` instead of pretending one namespace serves both. If no matching repository is visible on the resumed surface, do not improvise with a similarly named directory — apply the blocked behavior below and ask one consolidated location question only after discovery fails.

### Secret hygiene

A filesystem account component inside an exact local path (for example `/Users/<account>/...`) is accepted non-secret routing context for this operator's local relay workflow; record only the minimum full path required for deterministic navigation. This narrow exception never permits emails, account profiles, author/userinfo fields, tokens, credentials, session values, browser state, environment dumps, credential-store locations, or unrelated home-directory contents. When an artifact is intentionally destined for a public or unrelated external channel, a home-anchored display form may be added, but repository identity, repo-relative paths, and a valid surface-root mapping must be retained. Do not record a secret merely to eliminate a question; record the safe retrieval authority or a sanitized source description instead.

### Transport seat and continuity designation

Relay transport `SEAT` and continuity `current-designation` are different concepts. Pointer `SEAT` is transport routing only: it names the Relay receiving seat and is never the authority for, or a mutation of, the handoff's `current-designation`. Pointer `SEAT` is strictly one of the four Relay receiving seats defined by current `relay/standards/POINTERS.md`: `BUILDER`, `REVIEWER`, `PRESSURE-TESTER`, or `ORCHESTRATOR`. The verified handoff body carries the continuity designation using the open designation grammar `[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*`.

- If the recorded continuity designation is one of the four Relay seats and that seat is the intended receiver, use the same token in pointer `SEAT`.
- If the recorded continuity designation is a valid open designation outside the four Relay seats, use `SEAT: ORCHESTRATOR` and put the exact recorded designation in `TASK`. ORCHESTRATOR then verifies the handoff and the target surface's designation eligibility before continuing or routing. It must not treat the transport seat as a designation change.
- A starter pointer cannot change a sticky session seat, release a designation rotation, or grant implementation/review/mutation authority. Existing surface eligibility and role-integrity rules still control.

### Starter pointer

A normal successful close deposits exactly one immutable handoff, reads back the deposited bytes, computes the full Git blob FILE_SHA, full SHA-256, and exact byte count from that read-back, and returns:

```text
STARTING A NEW SESSION | SEAT: <relay-receiving-seat> | TASK: <resume instruction carrying the exact designation> | RELAY_REPOSITORY: Ezra144israel/operator-agent-relay | RELAY_PATH: relay/handoffs/<handoff-filename> | FILE_SHA: <full-git-blob-sha> | SHA-256: <full-64-char-digest> | BYTES: <exact-count>
```

These keys, in this order, and no others; the pointer conforms to current Relay `relay/standards/POINTERS.md`. It is pasteable across Codex, ChatGPT, Claude, and any agent that can reach the Relay.

Four-seat example:

```text
STARTING A NEW SESSION | SEAT: REVIEWER | TASK: resume designation REVIEWER from the verified continuity handoff | RELAY_REPOSITORY: Ezra144israel/operator-agent-relay | RELAY_PATH: relay/handoffs/example--REVIEWER--handoff-v2--abc12345.md | FILE_SHA: <full-blob-sha> | SHA-256: <full-sha256> | BYTES: <n>
```

Open-designation example:

```text
STARTING A NEW SESSION | SEAT: ORCHESTRATOR | TASK: resume designation AUDITOR-2 from the verified continuity handoff; transport seat is routing only | RELAY_REPOSITORY: Ezra144israel/operator-agent-relay | RELAY_PATH: relay/handoffs/example--AUDITOR-2--handoff-v2--abc12345.md | FILE_SHA: <full-blob-sha> | SHA-256: <full-sha256> | BYTES: <n>
```

### Shared close workflow

On a working-chat close, the current executor under the current designation must:

1. stop starting new work but finish or safely terminate the current atomic operation;
2. verify repo/worktree/branch/base/head/status and index when a repository is in scope;
3. re-verify every load-bearing relay artifact by full SHA-256 and exact bytes;
4. write the mandatory `CIL GROUNDING GATE` section before the `ROOT MAP`, with
   `state_at_close: REQUIRED_ON_RESUME` and every field required by the universal
   gate above;
5. separate verified facts, operator decisions, inferences, and unknowns;
6. record completed work, current work, blocked work, the next executable action and the one after it, exact do-nots, and pending authority gates;
7. record all changed/untracked files owned by the session without modifying, stashing, staging, committing, cleaning, or deleting them;
8. record skill/doctrine names that must load at resume without duplicating their prose;
9. record the artifact-specific authorship ledger needed for role-integrity checks;
10. apply the one matching optional designation addendum, or explicitly record `designation addendum: NONE` when no addendum exists;
11. deposit one immutable handoff, read back the deposited bytes, and compute its full Git blob FILE_SHA, full SHA-256, and exact bytes from that read-back; and
12. return the starter line plus any genuine unsafe-close blocker.

### Designation rotation barrier

Before changing designation, record the required `continuity-handoff/seat-rotation` fields and apply all of these rules:

- `rotation-state: released` is valid only when `work-unit-state` is `complete`, `blocked`, `failed`, or `reconvergence-required`;
- `work-unit-state: active` permits only `rotation-state: none` or `pending`;
- a pending rotation never changes the active designation;
- executor replacement inherits the same work-unit ID, designation, authorship restrictions, and recovery boundary; it is not a released rotation; and
- a new designation begins only after the prior work unit has a recorded terminal disposition and its required handback/review boundary is stable.

An unavailable executor may be replaced inside the same work unit without releasing a designation rotation. These are governing documentation rules in Slice A, not runtime enforcement; the separately locked Slice B owns actual return-envelope cross-field enforcement.

### Blocked close preserves continuity

`UNRESOLVED HANDOFF LOCATION` applies only when a genuinely load-bearing location or identity required for the next safe action cannot be resolved after bounded read-only discovery. The following alone are NOT blockers:

- no duplicate local handoff;
- no device path on a web-only surface when the next action does not use it;
- no local relay root when Relay is available through its governed connector.

A web-only or connector-only session is never blocked merely because it cannot see a non-load-bearing device filesystem path or local relay root.

If a genuinely load-bearing location or identity remains unresolved after bounded read-only discovery, still deposit, read back, hash, and byte-count one immutable Relay handoff. That handoff must carry `STATUS: BLOCKED — UNRESOLVED HANDOFF LOCATION`, preserve every resolved root, ledger row, decision, gate, changed-file record, completed action, pending action, and do-not boundary, and list each unresolved item, why it could not be resolved, every location already checked, the minimum operator input needed, and the exact first safe resume action after resolution. It keeps the normal immutable filename, version, and supersession rules. Never discard verified continuity because one row is missing.

A blocked close returns the normal starter line with the blocked status appended, so the operator and the resumed session see the state at paste time before reading the handoff:

```text
STARTING A NEW SESSION | SEAT: <relay-receiving-seat> | TASK: <resume instruction carrying the exact designation> | RELAY_REPOSITORY: Ezra144israel/operator-agent-relay | RELAY_PATH: relay/handoffs/<handoff-filename> | FILE_SHA: <full-git-blob-sha> | SHA-256: <full-64-char-digest> | BYTES: <exact-count> | STATUS: BLOCKED
```

A BLOCKED handoff is excluded from bare-phrase auto-selection. It may be resumed only through its exact starter pointer, and the resumed session must surface the unresolved-location blocker before further task work. The operator may supply or acknowledge the missing location; acknowledgment does not waive later path, identity, role-integrity, or authority checks.

### Discovery and bare-phrase auto-selection

When the operator supplies the starter pointer, use it: fetch the exact `RELAY_PATH` from the named `RELAY_REPOSITORY`, require the exact `BYTES`, and require the computed SHA-256 (and, where available, the Git blob `FILE_SHA`) to match before reading. An identity mismatch is a stop, never a prompt to search for a substitute file. Where a recorded local root is load-bearing for the resumed work, verify it against the recorded repository identity; on a different surface, perform bounded read-only discovery — locate a repository whose origin matches the recorded origin URL or `owner/repository`, verify the expected base/head object or remote reference, join the recorded repo-relative paths to that verified root, and verify recorded file identities before reading. Only after both the pointer identities and deterministic discovery fail may the session ask the operator for a location, and it must report what it checked in that one consolidated question.

The exact starter pointer is the normal resume route. A bare `starting a new session` with no pointer may auto-select a handoff **only** when all of these hold: the repository identity is known; the designation is known; the task key or exact supersession chain is known; the available Relay discovery source proves the candidate set is complete and non-truncated; exactly one unsuperseded non-BLOCKED handoff matches; and its file identity verifies. A capped directory listing, stale generated index, degraded search, or incomplete candidate set cannot prove uniqueness — in that case do not guess `latest`; ask for the exact starter pointer or another deterministic selector. Never select by newest timestamp alone and never scan unrelated repositories.

Otherwise report precisely, without guessing:

- **Zero non-blocked matches, but one or more BLOCKED handoffs exist for the designation/repo:** report that a blocked handoff exists and that exact-pointer resume is required. Do not report that no handoff exists.
- **Zero matches of any kind:** report that no resumable handoff was found.
- **More than one non-blocked match:** present one consolidated choice list using task key, created time, and status; do not auto-select.

### Shared resume workflow

On resume, the new session must:

1. parse only enough of the starter pointer to recover the claimed designation and
   locate the exact handoff through the supplied pointer or safe bare-phrase rule;
2. verify the handoff's full SHA-256, exact bytes, and, where supplied, Git blob
   `FILE_SHA` against the pointer without substantively reading its task content;
3. complete the universal CIL grounding gate above through the live CIL connector;
4. recover the current designation from the verified handoff and require it to match `[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*` without treating known addenda as a membership list;
5. run the artifact-specific role-integrity/authorship check **before** inspecting any subject the current executor may be forbidden to review;
6. ground independently from the current repo, relay, and original authorities rather than trusting the handoff;
7. compare current state with handoff state and classify drift — the absence of a
   retired local duplicate is not drift and never reopens completed work;
8. refuse unsafe continuation when CIL activation, base, scope, authorship, lock, return-path, or worktree identity has changed incompatibly;
9. read the root map and location ledger before asking the operator where anything lives, and directly inspect any item whose exact location is present and verifiable;
10. preserve every separate mutation gate; update the working plan; and continue automatically to the next safe action; and
11. stop only for unavailable or unsafe CIL grounding, a genuine authority gate, ambiguous handoff selection, artifact-authorship conflict, or incompatible state drift.

The acceptance target is zero operator path questions for information the handoff could have captured at close time. Then load the matching optional designation addendum when one exists; when none exists, continue through the shared contract and record `designation addendum: NONE`.

### Restored plan and execution state

Salvaged from the retired `portable-adaptive-planning` source. This is a resume
safety rule, not a second plan schema: continuity owns it because the risk is a
session boundary, and the risk is that a restored plan looks complete when it
is not.

Before continuing restored planning or execution work:

1. reproduce the latest complete restored state from current source, not memory;
2. verify that it covers the current operator instruction, not an earlier one;
3. show the readback before any mutation or execution.

If the restored state is complete, exact, and current, continue after that
readback. Do not ask for another confirmation only because a session boundary
occurred.

If the state is incomplete, stale, conflicting, uncertain, or cannot be
reproduced exactly from current source, mark it:

```text
RESTORED: UNVERIFIED
```

show the reconstruction, and hold for explicit operator confirmation before
executing. An accepted plan plus a prior GO is not an exact restore when the
complete state cannot be reproduced.

### Post-publication installed-surface resync inventory

After independent review and canonical publication, and only under separate later authorization, resync must inventory the four local Claude snapshots under `/Users/ezraisrael/.claude/skills/continuity-handoff/`, the `claude.ai` account skill, the Codex install if present, and any other exact-name installed snapshot. Publication does not authorize or prove resync. This Builder slice must not inspect, mutate, install, upload, or resync any external surface.

## Relationship to Other Skills

Continuity handoff depends on:

- `repo-grounding/SKILL.md`
- the Lean Loop Reviewer overlay (`relay/packages/human-grade-engineering-loop-v1.1/seat-reviewer.md`)
- the Lean Loop Builder return contract (`relay/packages/human-grade-engineering-loop-v1.1/seat-builder.md`)
- `security/SKILL.md`
- `store-readiness/SKILL.md`

Continuity output feeds:

- the next agent’s grounding read
- the next builder prompt
- reviewer validation
- future stable documentation updates
