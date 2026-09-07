# continuity-handoff/reference/pressure-tester-session.md

**Status:** Active Team Hub OS optional addendum. Documentation/skill guidance loaded only by `pressure-tester-designation-addendum` for the `PRESSURE-TESTER` designation. It is not runtime enforcement authority or designation-membership authority.

## Scope

This reference adds `PRESSURE-TESTER`-specific close fields and resume behavior to the shared governed designation session contract in `skills/continuity-handoff/SKILL.md`. Read that contract first; the root map, location ledger, command-location contract, secret hygiene, starter pointer, blocked-close rule, and discovery rules are shared and are not repeated here. `PRESSURE-TESTER` uses this optional addendum; other valid designations close and resume through the shared body without it.

## Pressure-Tester close fields

A Pressure-Tester close writes the shared root map and location ledger, and additionally makes each of the following explicit and location-complete.

### Subject and return target

- Subject absolute path, repo-relative path, full SHA-256, and exact bytes.
- The exact verdict return path, with its existence state — `EXISTS`, or a `PENDING` row proved `ABSENT VERIFIED <timestamp>` with its exact absolute and repo-relative target.

### Grounding and authority chain

Give a location-ledger row, with the repository/commit surface each identity was taken from, to:

- every original source file used for grounding, not only the packet under review;
- every comparison input, prior verdict, amendment, operator-lock, or other authority-chain artifact; and
- the full base/head identity used to reject a wrong checkout.

### Role integrity

- Record the complete authored-artifact lineage used for role integrity: which actor authored each artifact versus which artifact that actor may review. The actor that produced an artifact never reviews it; designation history alone is not a conflict.
- Record the current role-integrity state and any authorship constraint that must survive the session change.

### Review progress and boundary

- Record the pressure-test checklist: completed checks, remaining checks, provisional findings, and any unverified load-bearing claim.
- Record the findings-only, do-not-rewrite, and do-not-build boundary.
- Record the next evidence check and the one after it.

## Pressure-Tester resume behavior

1. Re-run the handoff identity gate and the role-integrity/authorship gate **before** inspecting the subject; if the proposed reviewer authored the subject or another load-bearing artifact whose correctness the review would approve, refuse the review and flag the routing error.
2. Re-ground original sources; do not trust provisional findings or the handoff's conclusions without re-verification.
3. Continue findings-only review; never rewrite the packet under review and never defend a prior verdict to protect it.
4. Write the immutable verdict return only after full verification, at the exact return path recorded at close.
