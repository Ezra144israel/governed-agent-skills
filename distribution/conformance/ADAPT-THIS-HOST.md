# Adapt this host to the canonical skill stack

You are a host, or the local agent for a host, that received this pack. The
pack tells you what the current skills are, when each fires and does not fire,
what must load with it, which roles your surface may hold, and how to prove it.
You implement loading and wiring for your host. You do not redefine any trigger.

## 1. Verify what you received

1. `PACK-MANIFEST.json` names every file in this pack with its byte count and
   SHA-256, the CURRENT manifest identity, and the source commits. Recompute
   the digests. Any mismatch means the pack is not this release. Stop.
2. `current-skills.json` is the exact published CURRENT manifest. Its identity
   in `PACK-MANIFEST.json` must equal the identity your operator supplied.
3. `skills/<id>/...` holds the exact canonical bytes of every CURRENT skill and
   every reference member it declares. Do not fetch bodies from anywhere else,
   and never from an installed replica, an old packet, or a download.

## 2. Load the bodies the way your host needs

Bodies are canonical bytes. If your native loader requires `name` and
`description` frontmatter, apply the adapter that `current-skills.json` declares
for your surface (`targets.<surface>.adaptation`); a `release` target means
bytes unchanged, `native-frontmatter-v1` means the declared frontmatter
prefix. Never change a body for any other reason. A surface whose target is
`BLOCKED` in the manifest does not receive that skill.

## 3. Wire firing exactly as the matrix states

`FIRING-MATRIX.generated.json` is the contract. For each skill row:

- `activation_class` `standing`: load once at session entry and keep resident;
  re-read only after compaction, a source-identity change, or an explicit
  operator refresh.
- `activation_class` `conditional`: load only when a positive trigger matches
  and no exclusion or veto applies. Where the row carries selectors
  (`task_kinds`, `surfaces`, `risk_flags`, `roles`, `lanes`), every non-empty
  selector list is a necessary condition; the trigger description is the
  semantic condition. Where the row carries only a description, match the
  description and honor its exclusion sentences.
- `activation_class` `explicit-operator`: load only on the operator's explicit
  instruction named in the row. Never self-fire on task class.
- `dependency_closure`: load each dependency when the skill fires. A
  dependency marked `repository-scoped` resolves only inside the named source
  repository; elsewhere report it under `host_capability_exception`.
- `child_references`: load a child only when one of its
  `activation_trigger_ids` fired, or on the explicit condition the row states.
- `return_contributions`: when the skill fires and owns a contribution, your
  return carries those fields.

You may organize this however your host works: a router injected at session
start, a hook, a rules file, or manual invocation. The meaning of a trigger is
fixed here and is the same on every host.

## 4. Apply your surface profile

`SURFACE-PROFILES.json` says which roles your surface may hold. A hosted
coordination surface may hold ORCHESTRATOR or PRESSURE-TESTER. A local
builder/reviewer surface holds BUILDER or REVIEWER, and receiving an
ORCHESTRATOR-authored dispatch never promotes it. ADVISOR grants no authority.
A transported `SEAT:` field never changes an already established seat.

## 5. Prove conformance and report

Run the probes in `CONFORMANCE-PROBES.generated.json` (the same set is shown
in `CONFORMANCE-PROBES.md`). One probe may cover several skills. For each
probe record `PASS` or `BLOCKED`.

Report format, one line per probe id, then one line per skill:

```text
PROBE <probe-id>: PASS | BLOCKED | <exact observation>
SKILL <skill-id>: PASS | BLOCKED | host_capability_exception=<NONE | exception text>
```

Rules for the report:

- A skill you cannot load is `BLOCKED` with a concrete capability exception.
  Never drop a required skill silently, and never mark it `PASS`.
- A known exception listed in `SURFACE-PROFILES.json` is reported by its
  exception id.
- Fix only real host-adapter failures. Do not reopen canonical skill
  semantics because one host cannot parse or load a body; report it.
- This pack grants no authority. Passing every probe proves firing conformance,
  not permission to commit, publish, approve, or delete.
