# continuity-handoff/reference/builder-session.md

**Status:** Active Team Hub OS optional addendum. Documentation/skill guidance loaded only by `builder-designation-addendum` for the `BUILDER` designation. It is not runtime enforcement authority or designation-membership authority.

## Scope

This reference adds `BUILDER`-specific close fields and resume behavior to the shared governed designation session contract in `skills/continuity-handoff/SKILL.md`. Read that contract first: the root map, location ledger, command-location contract, secret hygiene, starter pointer, blocked-close rule, and discovery rules are shared and are not repeated here. `BUILDER` uses this optional addendum; other valid designations close and resume through the shared body without it.

## Builder close fields

A Builder close writes the shared root map and location ledger, and additionally makes each of the following explicit and location-complete.

### Roots

Separately identify, in the root map, the:

- canonical device repository root (where the relay and authority artifacts live);
- isolated build worktree root (where code work occurs);
- package/application root from which repository commands run; and
- device relay root.

Never make the next Builder ask whether the relay lives in the isolated worktree or the device checkout. Both roots and their relationship are named explicitly.

### Governing and output artifacts

Give each a location-ledger row with full identity: the dispatch (path, full SHA-256, bytes, authorized scope); the design/convergence and operator-lock inputs; the builder-return target; and any audit or review-return target. A return path that does not yet exist is a `PENDING` row with its exact absolute and repo-relative target and the verified-absent result.

### Change and process state

Record:

- every authorized changed path with its close-time full SHA-256, exact bytes, and whether the change is complete;
- every protected or untouched path whose location is load-bearing;
- the worktree dirty/index census (`CLEAN`/`MODIFIED`/`UNTRACKED`/`STAGED`/`MIXED`) without modifying, staging, or cleaning it;
- the RED/GREEN progression and every verification already run; and
- any currently running process or its safe-termination state.

### Commands, resume point, and stops

- List every resume command and verification check in the shared command table with its `sequence`, `purpose`, `recorded_surface_id`, `recorded_surface_absolute_cwd`, `repository_identity`, `repo_relative_cwd`, the exact command or non-shell action, the expected safe result, and the stop condition — package-root commands and device-relay commands carry their different working directories, and `sequence` plus `purpose` keep a multi-command continuation deterministic.
- State where implementation resumes (the first incomplete vertical slice or verification gate) and where the immutable builder return is written.
- State the hard stops, the exact authorized tracked scope, and the original Lean Builder return contract the session must still satisfy.
- State the explicit no-stage / no-commit / no-push posture.

## Builder resume behavior

1. Enter the named repository/worktree before acting; on a different execution surface, re-root through repository identity per the shared command-location contract rather than using a stale absolute cwd.
2. Verify the dispatch identity and the exact base before reading changed code.
3. Preserve existing changes exactly — do not stash, revert, or re-stage them.
4. Resume at the first incomplete vertical slice or verification gate recorded at close.
5. Never convert the handoff into scope expansion or into approval to stage, commit, push, or merge.
6. Finish with the original Lean Builder return contract; the handoff does not replace it.
