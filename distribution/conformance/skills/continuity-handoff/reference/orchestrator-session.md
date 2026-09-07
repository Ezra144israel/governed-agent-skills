# continuity-handoff/reference/orchestrator-session.md

**Status:** Active Team Hub OS optional addendum. Documentation/skill guidance loaded only by `orchestrator-designation-addendum` for the `ORCHESTRATOR` designation. It is not runtime enforcement authority or designation-membership authority.

## Scope

This reference adds `ORCHESTRATOR`-specific close fields and resume behavior to the shared governed designation session contract in `skills/continuity-handoff/SKILL.md`. Read that contract first; the root map, location ledger, command-location contract, secret hygiene, starter pointer, blocked-close rule, and discovery rules are shared and are not repeated here. `ORCHESTRATOR` uses this optional addendum; other valid designations close and resume through the shared body without it.

## Orchestrator close fields

An Orchestrator close writes the shared root map and location ledger, and additionally records one location-complete track ledger for every active track.

### Per-track gate ledger

Each active track lists the exact path and full identity, as applicable, for its:

- convergence packet and amendments;
- pressure-test return;
- operator lock record;
- builder dispatch and builder return;
- independent review dispatch and return;
- repair dispatch and superseding return;
- publication return, PR, merge, and deployment evidence;
- owner-walk / remediation records; and
- cleanup inventory and cleanup-authorization state.

Record which decisions were made within locked parameters versus which remain open operator decisions.

### Designations, next action, and waits

- Record current designation, executor, and artifact-specific authorship constraints for each track.
- For each active track, state the next executable step **and the one after it**, each naming its exact input and output paths and the exact working directory per the shared command-location contract.
- Identify each parallel wait by the precise expected return path — never merely `waiting for builder`.

### Authority boundaries

- Preserve separate authorization state for lock, build, commit, push/PR, merge, deploy, walk, and cleanup. Capability is not authorization; one approval does not generalize to the next act.
- Record the pending owner-walk and Done-bar state and the explicit canonical-mutation boundaries.

## Orchestrator resume behavior

1. Verify origin and relay independently before reconstructing state.
2. Reconstruct the gate ledger before issuing any dispatch or mutation command.
3. Continue all unblocked tracks without waiting for routine operator nudges.
   When `orchestrator-relay-queue` applies, load `continuity-handoff/relay-queue`
   and continue all unblocked tracks through that child; do not duplicate its
   protocol here.
4. Preserve separate authorization for lock, build, commit, push/PR, merge, deploy, walk, and cleanup — resume never merges these gates.
5. Do not change designation unless the operator authorizes it and the shared work-unit rotation barrier permits release.
