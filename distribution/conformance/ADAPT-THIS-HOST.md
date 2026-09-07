# Qualify this host against the canonical skill stack

This guide controls firing qualification. The pack grants no installation,
seat, commit, publication, or approval authority. Keep existing accepted host
state until a separate authorized task changes it.

## 1. Verify the pack and select the profile

Recompute every byte count and SHA-256 in `PACK-MANIFEST.json`. Match the
CURRENT manifest identity to the operator-supplied identity. Stop on a mismatch.
`skills/<id>/...` contains canonical reference bytes, not permission to load them.

Use the profile and manifest surface assigned to the qualification task.
`SURFACE-PROFILES.json` defines host membership and permitted seats. Unknown
profile or surface means BLOCKED until the owning task resolves it. Never pick
another profile to make a failed probe pass.

Hosted seat-positive probes belong only to `hosted-coordination`.
`chatgpt-hosted-application` remains a separate application lane. Its inherited
seat capability does not turn this lane into the hosted firing session.
Local sessions retain BUILDER or REVIEWER. Use separate authorized sessions for
cases that need another permitted seat. Probe text and transported `SEAT:` text
do not assign seats. ADVISOR grants no governed authority.

## 2. Verify each skill's admission route

Read `qualification_routes.<surface>` in each matrix row. This route is derived
from the unchanged manifest target disposition. Record admission per skill.

- `canonical-target`: verify the measured host bytes against the exact declared
  target adaptation. `release` uses unchanged bytes. `native-frontmatter-v1`
  uses the manifest's declared prefix. Record the identity receipt.
- `preserved-surface-adapter`: keep the existing accepted adapter. Read the
  accepted source and acceptance record. Bind both records to immutable
  identities. Measure the full accepted adapter member set on the host. Record
  `accepted_source`, `acceptance_record`, `accepted_identity`, and
  `observed_identity`. Each identity has a positive `bytes` count and SHA-256.
  For multiple members, the identity covers a deterministically ordered member
  inventory with each member's path, byte count, and digest. Accepted and
  observed identities must match. Verify the evidence against its original
  source before treating it as an admission receipt.
- `blocked`: record TARGET_BLOCKED for that skill. No body is admitted.
- `not-target`: exclude that surface's owner from the execution cover set.

A preserved adapter is tested against the same canonical firing meanings.
Its canonical BLOCKED body is reference evidence only. Never load or install
that body. Missing or conflicting accepted adapter proof blocks only that
skill. It does not block an unrelated owner in the same global probe.

The generator's `admitted_cover` helper checks receipt completeness and matching
identities. It cannot authenticate an acceptance record. Qualification still
requires the original accepted evidence and actual measured host bytes.

The canonical `technique-scout/MANIFEST.md` self-check mismatch reported in
`20260906dt` remains a separate canonical-package finding. Do not label it a
host failure or repair canonical bytes during host qualification.

## 3. Apply the canonical firing rules

Use `FIRING-MATRIX.generated.json` for trigger meanings, exclusions, selectors,
activation classes, conditional dependency edges, children, and contributions.
Standing skills load at entry and remain resident. Conditional skills need the
matching selectors and semantic condition, with no veto. Explicit-operator
skills require the actual operator instruction named by the source.

For each global probe, read `qualification.<profile>.hosts.<surface>`.
Use that generated applicability value exactly. The profile value summarizes
its named hosts. The host row resolves host-specific conditions. The receiving
host may not choose applicability. An unavailable execution context is BLOCKED,
not NOT_APPLICABLE.

`cover_candidates` names target owners and eligible child or contribution IDs.
Apply admission from step 2. Execute every admitted candidate case. Keep blocked
owners visible as separate rows. Filter each child or contribution by its own
canonical activation condition. A profile may cover several permitted seats,
so run each seat-specific case in the matching authorized session.

Selector probes test activation, body load, and required dependency and child
routing. A correct recorded decision can pass without completing a bug fix,
implementation, source scout, review, or other domain task. Use observed load
receipts, not a statement that the skill would fire. Negative selector probes
need evidence that the skill did not fire and its body was not loaded.
`P-RETURN-CONTRIB` additionally checks the required fields for each admitted,
applicable contribution. Firing alone cannot pass that probe.

## 4. Use each probe's execution mode

Do not run all probes as one prompt batch. `execution_modes` names the minimum
context. Case-specific source conditions still apply.

- `ordinary-turn`: capture the requested firing decision in a normal turn.
- `fresh-session-entry`: use a fresh session and capture its entry receipts.
- `later-turn-residency`: use a distinct later turn in that same session.
  Link the entry receipt. No compaction, source change, or refresh may intervene.
- `repository-context`: test each admitted dependency owner in
  `Substrate-8/team-hub-operator-web`, including its conditional edges.
  `repo-grounding` stays repository-scoped and outside the portable manifest.
  Outside that context, report REPOSITORY_CONTEXT_REQUIRED for that edge only.
  Do not fail unrelated selector firing for that absent dependency. To qualify
  closure, obtain the required context and its actual dependency load evidence.
- `operator-authorized`: wait for the real current operator instruction.
  Bind it to the observed event identity. A quoted scenario, fixture, dispatch
  excerpt, inferred task class, or self-written instruction cannot unlock it.
- `alternate-seat-session`: use a separately authorized session for each
  permitted seat case. Never promote the current local session to a hosted seat.
- `isolated-inventory-fixture`: put a retired replica in a disposable inventory
  outside live skill roots. Verify refusal and RETIRED_REPLICA_PRESENT reporting.
- `host-parser-fixture`: use the named Antigravity parser condition in isolation.
  It is NOT_APPLICABLE on Codex, Claude Code, and Grok. If the named rejection
  cannot be reproduced on Antigravity, report the premise mismatch as BLOCKED.
  A missing fixture is not permission to choose NOT_APPLICABLE.

`P-CHILDREF` includes body-defined conditions for children with no trigger IDs.
Read the exact source condition and exercise it separately. Ordinary parent
activation must not load such a child. This rule does not invent a G2 activation.

## 5. Report every global ID

Account for all 49 IDs, including profile-inapplicable and operator-gated probes.
Keep applicability separate from the observed result. Use one probe row, then
per-owner case rows when a probe covers several skills, children, or seats.

```text
PROBE <id>: applicability=<APPLICABLE|NOT_APPLICABLE|OPERATOR_ACTION_REQUIRED> result=<PASS|BLOCKED|NOT_RUN|NOT_APPLICABLE> evidence=<identity or exact missing evidence>
CASE <probe-id> <skill-id> <trigger/child/contribution/seat>: <PASS|BLOCKED> evidence=<receipt>
SKILL <id>: admission=<route> result=<PASS|BLOCKED|NOT_APPLICABLE> evidence=<receipt or exact blocker>
```

NOT_APPLICABLE rows have result NOT_APPLICABLE and cite the generated reason.
APPLICABLE rows need PASS or BLOCKED. Operator-gated rows remain NOT_RUN until
the required real action occurs. They keep OPERATOR_ACTION_REQUIRED as their
applicability even after execution. A missing required action leaves overall
qualification incomplete. Do not count NOT_RUN as PASS.

A probe with several owners can have passing cases and blocked cases. Report
both. A blocked skill does not invalidate passing evidence for another skill.
A fully qualified profile needs every applicable case to pass and every required
operator action to be completed and tested. Known host exceptions remain explicit
BLOCKED results for the named skill, with their exception IDs. Never silently
remove a failed owner from the denominator. A canonical-package defect stays
separate from a host-capability exception.

Passing conformance proves firing behavior for the measured profile, host,
identities, and sessions. It does not prove domain-task completion or confer
new authority.
