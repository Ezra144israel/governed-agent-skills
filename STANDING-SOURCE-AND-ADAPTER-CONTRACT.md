# Standing source and adapter contract

Status: active — durable source ownership for the standing environment skill family.

## Why this file exists

Installed copies of these skills drifted for weeks across five surfaces while no
file said which body was the source. `.sync-manifest` covered part of the estate
and nothing covered the rest, so a byte difference could not be classified as
either a lawful adapter or drift. This file makes that classification possible
before any resync runs.

It is the standing-family counterpart to
`docs/architecture/SKILL-SOURCE-DISTRIBUTION-CONTRACT.md` in
`Substrate-8/team-hub-operator-web`, which deliberately governs only that
repository's own skills.

## Source home

This repository is the canonical source for the skills under `skills/`.

Basis, not assertion:

- operator-locked decision `builder-quality-system--ORCHESTRATOR--decision-v1--14958640.md`
  ("one lean universal Builder core owned by `Ezra144israel/governed-agent-skills`");
- the same decision's rule that "installed agent copies are adapters or
  releases, not independent canonical owners";
- this repository's own published plugin and marketplace manifests, which name
  it as the plugin's repository, and its tagged releases.

`Ezra144israel/governed-agent-core` is **not** a source home. It states in its
own `AGENTS.md` that it is "a private, unpublished Q1/Q2 source candidate" that
"is not installed, published, deployed, or product Done".

Copies under `Ezra144israel/operator-agent-relay` in `relay/archive/`,
`relay/packages/`, and `relay/skill-versions/` are provenance and frozen package
payloads. They are evidence, never source.

## Rules

1. Every skill under `skills/` in this repository is the source for that skill.
2. An installed copy on any surface is a **release** (byte-identical to source)
   or a **declared adapter** (different bytes, stating its source and its target
   surface inside its own body). There is no third kind.
3. A byte difference with no such declaration is drift, not an adapter.
4. A plugin cache, account upload, or project attachment is never a second
   source owner, whatever its bytes say.
5. A skill absent from the table below is not published by this repository.

## Distribution table

| Skill | Distribution | Target surfaces | Adapter permitted |
|---|---|---|---|
| `reasoning-doctrine` (+ 4 references) | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `governed-operator` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `grilling` | release | Claude Code, Codex, Agents, Claude shared | no |
| `unslop` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |

## Retired: must not regrow

These were retired by
`substrate8-lean-governance-pruning--ORCHESTRATOR--closed-pruning-manifest-v2--20260828.md`
and are removed from this package so a normal install or update cannot
reintroduce them:

| Skill | Where its value went |
|---|---|
| `portable-adaptive-planning` | restore protocol → published `continuity-handoff`; `FINAL` + `GO` → `governed-operator` Gate 2 |
| `write-maintainable-code` | no-code route comparison → published `code-quality` §4C; ownership split → `governed-operator` precedence |
| `run-review-repair-loop` | retired by `builder-quality-system--ORCHESTRATOR--decision-v2--14958640.md`; already absent here |
| `scouted-rules` | distributed to named owners; never published from this repository |
| `test-verification` | not retired — owned solely by `Substrate-8/team-hub-operator-web`. Removed from this package so it cannot regrow here as a generic standing duplicate |
| `pending-convergence` | not a skill — preserved as a non-skill Relay convergence register snapshot. Guarded here so no sync, install, or packaging step can recreate it as `SKILL.md` |

## Ownership boundary with `Substrate-8/team-hub-operator-web`

Resolved by
`relay/decisions/substrate8-lean-governance-pruning--ORCHESTRATOR--standing-source-ownership-v1--20260828.md`.

The split is an ownership boundary, not a duplication licence. A skill has one
source home only.

| Family | Home |
|---|---|
| generic cross-environment method skills | this repository |
| Substrate-specific skill specialists | `Substrate-8/team-hub-operator-web` |

Both families hold skills and nothing else. A register is not a skill and has no
place in either row; see the separate register-owner statement below.

`test-verification` and `technique-scout` are Substrate-specific skill
specialists and are sourced there, distributed through that repository's own
`SKILL-SOURCE-DISTRIBUTION-CONTRACT.md`. This repository publishes neither.
`test-verification` was shipped here through v2.0.0 and is removed in v3.0.0.
Removing a skill a published package shipped is a breaking distribution
change, so this release takes a major version, not a minor one.

## Register owner: `pending-convergence` has no skill source home

`pending-convergence` is owned only by the Relay convergence record family at
`relay/convergence/`. It has no skill source home in this repository, in
`Substrate-8/team-hub-operator-web`, or in any other skill repository.

`relay/decisions/substrate8-lean-governance-pruning--ORCHESTRATOR--pending-convergence-is-register-not-skill-v1--20260828.md`
(FILE_SHA `c3905965318f8316f843ee17e650878aa6e074a8`) rules that
`pending-convergence` was never a behavioral skill. It is a register of
unresolved subjects; its own body states *"This file holds. It does not
decide."* Packaging it as a skill created a false active capability and an
unnecessary standing read cost.

Its accepted contents live as a versioned non-skill governed record in the Relay
`relay/convergence/` family:
`substrate8-lean-governance-pruning--ORCHESTRATOR--pending-convergence-register-v1--c5088675d20c.md`.
That record is the durable register. The Builder snapshots
`…--BUILDER--pending-convergence-register-snapshot-v1--c5088675d20c.md` and
`…-v2--c5088675d20c.md` remain immutable worker evidence and provenance; they
are not the governed register, because only the ORCHESTRATOR produces governed
artifacts. Cite the ORCHESTRATOR record, not the snapshots.

Future updates supersede that record at the next version under Relay record
lineage. They never reinstall a skill and never add a router, index, manifest,
or package row. The guard in `tools/check-standing-distribution.mjs` fails the
build if `skills/pending-convergence/SKILL.md` ever reappears.

This decision supersedes only the `pending-convergence` portion of the standing
source ownership decision. Every other ownership assignment in that decision is
unchanged.

## Provenance of newly sourced bodies

`grilling` and `unslop` had no repository source before this candidate. Their
bodies were recovered from the current accepted operative copies, each verified
against two independent chains: the accepted managed set in
`~/.claude/skills/.sync-manifest`, and the Relay provenance snapshot named by
the body's own digest.

| Skill | SHA-256 | Bytes at import | `.sync-manifest` | Relay snapshot |
|---|---|---:|---|---|
| `grilling` | `ec7718062b7dce9650a9608339ce405c171407f6ab58529c98daae70530f7fce` | 4774 | match | `relay/skill-versions/grilling/ec7718062b7d.md` |
| `unslop` | `8e6472835009def01137d6c3fb241d6d3dbbc59ce4f5bd613dd34636b8d83bd1` | 9940 | match | `relay/skill-versions/unslop/8e6472835009.md` |

No `.pre-*`, `.bak`, stale snapshot, account-transformed, or duplicate local
variant was imported. `grilling` was then repaired at source; see below.

## `grilling` source repair

`pending-convergence` entry 9 identified an agent-authored bridge in
`grilling` § *Boundary: the confirm gate*: *"Execution proceeds only when both
tests pass: the specific act is already authorized under the per-act model
above, and it is reversible. Neither alone is enough."*

No current authority establishes that conjunction. In `governed-operator`,
reversibility decides whether an in-scope method choice is `EXECUTOR_OWNED`,
whether an unpredicted obstacle may be adapted around rather than escalated, and
whether an action needs a `METHOD_LOCKED` basis — and that skill states plainly
that reversible continuation is *not* an operator gate. Reversibility there
removes gates; it never adds a second permission test to an already-authorized
act.

The unsupported conjunction is removed. The two real rules are stated separately
with their real owner, and `grilling`'s own job — refusing to commit to a design
the user has not agreed — is unchanged, as is its trigger.

## Verification

`node tools/check-standing-distribution.mjs` proves this table covers exactly
the skills this repository publishes, and that no retired skill has regrown.
