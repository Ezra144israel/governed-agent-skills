# continuity-handoff/reference/relay-queue.md

**Status:** Active Team Hub OS progressive child. This is documentation guidance only, not runtime enforcement.

## Scope

Q1A is a local working-chat coordination ledger under
`operator-web/scratchpad/relay/queue/`. Only the active Orchestrator writes
events. Other designations may read a routed subject but never mutate queue
state. An event is routing/index evidence, never authority, a lock, approval,
designation change, product queue record, or canonical truth.

## Event contract

Each transition creates one immutable Markdown file:

`<task-key>--q<sequence>--<STATE>--v<integer>--<subject8>.md`

`subject8` is only a locator. The event cannot contain its own final digest;
after writing it, report its path, full SHA-256, and bytes out of band. Each
event carries:

- `queue_schema`: `teamhub-relay-queue/v1`
- `queue_event_id`, `task_key`, strictly increasing `sequence`, and UTC
  `created_at`
- `state` and `next_action`; lifecycle stage belongs in `next_action`
- `required_designation`
- `subject_path`, `subject_sha256`, `subject_bytes`
- `expected_return_path`
- `authority_status`: `GRANTED`, `AWAITING_OPERATOR`, or `NOT_REQUIRED`
- `authority_basis`: exact path + SHA-256 + bytes, or `NONE`
- `authorship_ledger_ref`: exact path + SHA-256 + bytes
- `review_disqualifications`, or `NONE`
- `blocked_question`, or `NONE`
- `reopen_condition`, or `NONE`
- `supersedes_events`: `NONE`, one predecessor identity, or every conflicting
  leaf identity, where each identity is `{path, sha256, bytes}`
- `priority_override_basis`: `NONE`, an exact quoted current operator
  instruction, or that instruction's immutable path + SHA-256 + bytes
- bounded `notes`, or `NONE`

## States and BLOCKED validation

Exactly five states exist:

- `READY`: the exact subject exists; its next action is authorized or
  read-only; designation, authorship, and free return path verify.
- `IN_FLIGHT`: the Orchestrator issued the exact routing pointer. This does
  not claim receipt or execution.
- `AWAITING_OPERATOR`: one explicit operator gate is needed; exclude it from
  ready selection.
- `BLOCKED`: one observable `reopen_condition` is required; exclude it without
  blocking other tracks.
- `TERMINAL`: the unit completed, failed, was canceled, or was replaced; record
  the final outcome identity and exclude it.

The `BLOCKED` matrix is exact:

- operator decision blocker: one concrete `blocked_question`; the
  `reopen_condition` names the required recorded operator answer or authority
  evidence.
- dependency blocker: `blocked_question: NONE`; the `reopen_condition` names
  the exact task/event identity and required terminal state.
- external-state blocker: `blocked_question: NONE`; the `reopen_condition`
  names the exact observable external-state predicate.
- missing both question and condition: invalid and quarantined.
- operator decision with `blocked_question: NONE`: invalid and quarantined.
- dependency or external blocker with an invented operator question: invalid
  and quarantined.

Reopening `BLOCKED` requires a new event citing the recorded operator answer or
observed dependency/external-state change.

## Chain, quarantine, and reconciliation

Current state is the unique unsuperseded leaf of one identity-linked,
strictly increasing chain per `task_key`. The first event has
`supersedes_events: NONE`; an ordinary transition names exactly one predecessor.
A missing or wrong predecessor identity, wrong sequence, or multiple leaves
causes task-local quarantine. Exclude only that task like `BLOCKED`; never
silently repair it or stop valid tracks from flowing.

Reconciliation requires a separately authorized immutable event. It:

1. retains the same `task_key`;
2. sets `sequence = max(conflicting leaf sequences) + 1`;
3. lists every conflicting unsuperseded leaf exactly once in
   `supersedes_events`;
4. records exact operator reconciliation authorization in `authority_basis`;
5. records the selected recovered state and reason in bounded `notes`;
6. never edits or deletes a conflicting event; and
7. is invalid if any leaf, identity, sequence, or operator authority is
   missing.

A valid reconciliation becomes that task's unique leaf and changes no other
track.

## Selection and duplicate backstop

After a returned artifact, the Orchestrator verifies it before reading, writes
the affected task's next event, validates every current leaf independently,
excludes non-`READY` and quarantined tasks, and selects oldest `created_at`, then lexical `task_key`.
It then verifies subject identity, authority, required
designation, and role integrity, writes `IN_FLIGHT`, and returns only the
operator's established plain label plus PATH/SHA-256/BYTES pointer.

Default selection uses `priority_override_basis: NONE`. Only explicit current
operator reprioritization may select otherwise, and only the acting
`IN_FLIGHT` event records the non-`NONE` basis. Orchestrator preference,
severity, vendor, model, and artifact type are invalid priority bases.

Before a routed session executes an `IN_FLIGHT` subject, it verifies the exact
`expected_return_path` is absent. If occupied, stop
`BLOCKED — RETURN PATH COLLISION`, report the existing path identity, and do
not inspect further, execute, overwrite, invent a v2 return, or choose another
path. Only the Orchestrator reconciles whether the first route completed, is
active, or is stale. Legitimate repair/resume work requires a new immutable
dispatch or resume artifact with its own predeclared free return path.

## Invariants and deferrals

- `READY` is invalid unless its exact subject carries the required authority;
  queue presence never grants or broadens it.
- Registration is not a review pass, build grant, commit, publication, merge,
  deployment, cleanup, designation change, designation rotation release, or
  CIL grant.
- `required_designation` never names a vendor or agent. Queue state cannot
  promote an executor, change designation, or release the shared rotation
  barrier.
- Review and pressure-test subjects still require artifact-specific authorship screening before inspection.
- A session starts no new work unit until its prior unit has a terminal
  disposition and stable handback boundary.
- Queue events never supersede the governed artifacts they reference.
- Q1A does not pull work or claim cross-chat transport; the operator still
  pastes the pointer.
- Q1B self-pull remains deferred until evidence justifies it and an atomic
  claim/duplicate-prevention contract is converged.
- Layer 2 product planner-queue semantics, schema, runtime, routes, and UI are
  separate and deferred to an explicitly opened lane.
