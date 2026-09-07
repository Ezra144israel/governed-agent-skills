---
name: cil-mode-switch
description: Portable CIL Mode Switch source candidate. Enter, hold, and automatically restore a CIL-conditioned operating posture across a session, without storing or restoring authority. Pre-wiring source only — it installs nothing and grants nothing.
---

# CIL Mode Switch (portable source candidate)

Mode Switch is a CIL-owned agent operating capability. It belongs to no consuming
project. An agent may run it while working on any project; that never makes the
project its owner.

This package is **pre-wiring source**. It performs no installation, changes no
account, and carries no authority. Installation, account changes, publication,
and behavioural qualification stay with the operator.

## Package layout

```text
SKILL.md                                this file
lib/mode-switch.mjs                     restore and evidence evaluator
lib/mode-switch.test.mjs                focused verification
lib/fixtures/restore-vectors.json       golden vectors
lib/fixtures/evidence/                  synthetic test evidence, UNPROVEN boundary
lib/fixtures/evidence-install-bound/    the same records, modelled INSTALL_BOUND
lib/fixtures/*/artifacts/               the evidence artifacts those records cite
schema/mode-baseline.schema.json        what a baseline may hold
schema/restore-trace.schema.json        what every restore event records
schema/capability-record.schema.json    per-surface capability MODEL
schema/install-pin.schema.json          install-time binding of records to digests
schema/install-authority.schema.json    the install's claim that the home is out of reach
schema/rollback-requirements.schema.json portable rollback requirements
schema/source-set-measurement.schema.json full-switch source-set receipt
acceptance/frozen-prompts.json          staged acceptance cases, incomplete for Q5
template/rollback-requirements.template.json placeholder-only rollback template
```

The evaluator resolves every resource from this package. It never walks up to a
host repository root, and it runs on Node built-ins with no dependencies.

## Full switch

Run a full switch on an explicit `Mode Switch`, on a proven fresh-session entry
signal, or when restore cannot establish a trustworthy same-session baseline.

Resolve the current seat and Governance Dial from their live authority sources
before CIL work. Load the standing stack, the current CIL ref and capability
state, the five bootstrap slots, your own calibration, and the five named branch
notes while the source-set hypothesis is under measurement. Read the current
behavioural spine and every record that fires. Record one Application Gate result
and one concrete changed action.

Write a Mode Baseline holding CIL and posture identities only. It may hold
*locators* for the authority sources. It may never hold a seat, a designation, or
a Governance Dial value. Use `schema/mode-baseline.schema.json`.

## ChatGPT hosted CIL route adapter

On supported ChatGPT web and mobile text conversations that load the hosted
global instruction field and Personal Skill, complete this adapter before live
CIL grounding.

Use the CIL connector.

Discover the connector named exactly `CIL` through the current connector
discovery mechanics. An initially filtered or incomplete tool list does not prove
that the connector is absent. Attempt at least one required CIL call before
declaring the connector unavailable. Use a returned live CIL commit or blob
identity as route evidence.

Do not use the `Substrate_8` connector for CIL grounding. Do not use the GitHub
connector for CIL grounding. Do not use web search or another repository
connector as a substitute. An old probe or generic repository search is
historical support, not current CIL or account-state authority.

If the CIL connector is unavailable, report the exact failure and do not claim
that Mode Switch is active. Fresh Mode Switch entry does not require an active
handoff. Load `continuity-handoff` only for an actual close, resume, designation
rotation, handoff, or Relay-continuity operation.

These restrictions apply only to CIL grounding and current CIL authority. After
grounding, `Substrate_8`, GitHub, web search, and other connectors remain lawful
for their own non-CIL source homes.

This adapter makes no claim for voice-first, empty or system-generated first
turns, attachment-only first turns, or other runtimes. Hosted invocation is a
prompt-level request, not a deterministic platform hook. Q4 proves installation.
Q5 proves observed instances, not universal deterministic firing.

## Restore

On a supported same-session re-entry signal, resolve seat and Governance Dial
from their live authority sources again — on every path, including a healthy one.
Verify the standing stack, the CIL ref, posture identities, recall state, and
trigger attachment where the surface exposes it.

Any missing or unverifiable item in that minimum set forbids `CURRENT`. A missing
baseline produces `RECONSTRUCTED`. A changed posture source produces `UPDATED`. A
measured component change escalates to a full switch.

Every restore event emits a mechanical trace under
`schema/restore-trace.schema.json`, including healthy ones. A healthy `CURRENT`
may stay operator-silent; its trace must still exist for audit. The evaluator
proves plumbing only. It never proves behavioural residency, and self-report is
never evidence.

## Surface capability evidence

The package ships the capability **model**. It does not ship any surface's
capability state.

A per-surface capability record is written at install time into the evidence
home — `evidence/capability/<surface>.json` beside this package, or the directory
named by `CIL_MODE_SWITCH_EVIDENCE_HOME` — together with
`evidence/capability/INSTALL-PIN.json`, which binds each record to its digest.

The evaluator loads and verifies that record itself. The caller supplies only a
surface identifier and its live claim. **There is no call argument through which a
caller can supply capability evidence**, and every record is verified against its
install pin, so post-install tampering is detected. An absent, unpinned, tampered,
malformed, or non-durable record returns `SURFACE_CAPABILITY_UNVERIFIABLE` and
forces a full switch.

### Proof-bearing states must cite bytes, not strings

`PROVEN` and `NOT_APPLICABLE` are the two states that make a positive claim about
the surface. Both are held to the same evidence contract, and **every** such
capability in a record is checked, not the first one:

- `directEvidence` is present;
- `evidencePath` names an artifact that is relative to the evidence home, cannot
  escape it, is not an absolute or drive-letter local path, and resolves to real
  bytes;
- `evidenceIdentity` is `sha256:<64 lowercase hex>` and is compared against the
  digest of those bytes;
- `evidenceBasis` classifies the **surface** — `SURFACE_INSPECTED` or
  `SURFACE_DOCUMENTED`.

A missing artifact, a path escape, an absolute or local-only citation, a
malformed identity, or an identity that does not match its artifact fails the
whole record. The record then returns `SURFACE_CAPABILITY_UNVERIFIABLE` and
cannot authorize any restore state.

This closes the citation form that produced the historical R3 defect: a `PROVEN`
grade whose entire evidence was prose naming an uncommitted local working-tree
file, with an identity that was only a label. Presence of plausible strings is
not proof.

### Unknown is not "not applicable"

`NOT_APPLICABLE` means the surface has no such capability. "The evaluating seat
had no read path" is a different claim about a different subject, and it is
`UNKNOWN`.

`evidenceBasis: "EVALUATOR_NO_READ_PATH"` is admissible only on `UNKNOWN`. On any
proof-bearing state it is rejected, naming `UNKNOWN` as the state that fits. So a
surface nobody could inspect starts at `UNKNOWN`, and an unsupported
`NOT_APPLICABLE` record fails closed instead of reaching `CURRENT`.

The package ships **no** ChatGPT or Claude capability truth, and hardcodes no
account-surface exception. Those surfaces begin at `UNKNOWN` and stay there until
an install obtains qualifying surface evidence.

### What the pin proves, and what it does not

The pin proves **integrity**: the record has not changed since it was pinned. It
does not prove **authenticity**: nothing in it binds the record to an authority
distinct from the evaluating caller. A party that can write the evidence home, or
set `CIL_MODE_SWITCH_EVIDENCE_HOME` for its own evaluation, can author a
self-consistent record and pin. Closing the call parameter alone therefore does
**not** mean a caller cannot authorize its own `NOT_APPLICABLE`.

**R1-b independence is an install-time (Q4) precondition, not a property of these
bytes.** It requires the evidence home to sit where the ordinary evaluating actor
cannot write or redirect it. `CIL_MODE_SWITCH_EVIDENCE_HOME` is install and
runtime configuration: the installer or host fixes it, never the evaluated
process at evaluation time.

### The boundary is represented, not assumed

An install that meets that precondition writes
`evidence/capability/INSTALL-AUTHORITY.json`, bound to the install pin, stating
who established the home and that the evaluating actor can neither write nor
redirect it. The evaluator reports the result on every trace as
`capabilityEvidence.authorityBoundary`:

- `INSTALL_BOUND` — a receipt is present and binds this install.
- `UNPROVEN` — no receipt, or one that is malformed or bound elsewhere.

**An `UNPROVEN` install is not R1-b-qualified.** The `NOT_APPLICABLE` exemption is
refused with `TRIGGER_NOT_APPLICABLE_EVIDENCE_UNBOUND`, the minimum read set is
`INCOMPLETE`, and a trace claiming `CURRENT` on an unbound `NOT_APPLICABLE` fails
`verifyRestoreTrace`. A directly measured `VERIFIED` trigger never rested on the
record and is unaffected.

The receipt is a **representation** of the install boundary, not a proof of it.
A same-process actor can write a receipt for itself, and this package cannot tell
that apart from a real install — doing so in-process requires an install-time
signing key, which this slice deliberately does not add. What the receipt buys is
that a package which has not been through Q4 says `UNPROVEN` and is refused,
instead of presenting integrity as independence.

**Stage A and Stage B publish this model. They do not assert that any Q4 install
boundary exists yet.** The shipped fixture home under `lib/fixtures/evidence`
carries no receipt and is `UNPROVEN` by design;
`lib/fixtures/evidence-install-bound` models a qualified install so the positive
path stays testable, and says so in its own receipt.

Q4 must therefore establish and check, alongside its other preconditions:

1. an evidence home the evaluating actor cannot write;
2. `CIL_MODE_SWITCH_EVIDENCE_HOME` set by the installer or host, not settable by
   the evaluated process;
3. an `INSTALL-AUTHORITY.json` written by that installer and bound to the install
   pin, whose `evidenceHomeControl` names how 1 and 2 actually hold on that
   surface.

## Growth

Deliver the CIL deposit test only at a detectable structural work boundary. The
agent judges the answer. An advisory self-reminder is not a boundary and is not
enforcement. Where a surface exposes no structural boundary, record
`AUTOMATIC_GROWTH_TRIGGER: UNPROVEN` rather than claiming ambient capture. The
candidate never promotes a lesson, playbook, or decision.

## Authority boundary

Structural machinery may wake the mode, fetch and verify sources, deliver
records, detect drift, rehydrate instructions, and record evidence.

It may not decide whether a record applies, resolve a CIL-versus-project conflict,
choose a seat, choose or change a Governance Dial, approve its own work, or
promote anything. The Mode Baseline is evidence and cache. It is never authority.

## Acceptance and rollback

`acceptance/frozen-prompts.json` carries the staged acceptance cases and declares
itself **incomplete**: nineteen of the terminal thirty-two numbered cases are
staged. The remaining thirteen must be written and reverified before the claims
they cover are run. Paired behavioural scoring requires an independent scorer who
is neither the agent under test nor the seat that produced the work.

`template/rollback-requirements.template.json` carries portable rollback
requirements with placeholder locations only, no install binding, and no
identities. Resolved per-surface payload and rollback identities are install-time
state, produced when a surface is actually installed — never package truth.

### What Q4 must capture, and when

A `RESOLVED` rollback document is accepted only when it is authoritative for one
named install and every surface entry carries a **durable identity for both
sides of the rollback**:

- `priorIdentity` — the prior known-good payload or state that rollback restores.
  **Capture it before the first install mutation on that surface.** A capture
  taken after the write is not a known-good identity. Where the surface genuinely
  held no prior payload, record `absent:<REASON>` and make removal the rollback
  action; never leave it null.
- `candidateIdentity` — the payload the install writes. Capture it as part of
  that surface's install receipt.

The two sides do not share one grammar. `candidateIdentity` is `sha256:<64 hex>`
or `git:<40 hex>` and nothing else: a resolved install always writes a payload,
so there is always something positive to identify, and `absent:` has nothing to
mean there. `priorIdentity` accepts those two forms **and** `absent:<REASON>`,
because "there was nothing on this surface" is a real prior state.

A filesystem path, a prose label, or a placeholder is not an identity on either
side: a path can be rewritten, and a path to an uncommitted local file cannot be
restored from.
That was the A2 defect — a resolved plan that pinned paths, left identity null,
and named the same uncommitted file that produced R3 as its known-good payload.

**A surface with no resolved rollback identity is not installable.**

## Verification

```bash
node --test lib/mode-switch.test.mjs
```

The suite runs from a clean copy of this package in an empty directory, with no
host repository present.
