# Instruction Layer source and adapter contract

Status: active.

## Source home

This document governs the eight-skill Instruction Layer. The two Enforcement
Layer guards have their own READMEs and are outside this distribution table.

This repository is the public source home for its eight governed agent skills.
Installed copies are releases or declared adapters. A byte difference with no
adapter declaration is drift.

## Distribution table

| Skill | Distribution | Target surfaces | Adapter permitted |
|---|---|---|---|
| `reasoning-doctrine` (+ 4 references) | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `governed-operator` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `write-maintainable-code` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `portable-adaptive-planning` (+ 1 reference) | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `test-verification` (+ 1 reference) | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `grilling` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |
| `unslop` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |

No skill absent from this table is published by this repository.

## Retired: must not regrow

These retired workflow wrappers must not return as package skills:

| Identifier | Status |
|---|---|
| `run-review-repair-loop` | retired |
| `scouted-rules` | retired |
| `orchestrator-seat` | retired |
| `builder-return` | retired |
| `reviewer-validation` | retired |

## Register owner: `pending-convergence` has no skill source home

`pending-convergence` is a non-skill Relay convergence register. Its owner is
`relay/convergence/`. It must never be installed, routed, synced, or packaged
as a `SKILL.md` file.

## Accepted adaptations and upstream provenance

This repository owns the accepted adapted `grilling` and `unslop` skills.
Their upstream authors remain provenance. Later upstream changes do not replace
these accepted adaptations. The exact bytes follow the ownership decision
`skill-version-hygiene--ORCHESTRATOR--ownership-resolution-test-verification-grilling-unslop-v1--20260906co`.

`grilling` originates from `mattpocock/skills`. `unslop` originates from
`cursor/plugins` by Lauren Tan. Both are MIT-licensed.

## Current identity and distribution

`current-skills.json` is the sole current shared-skill identity manifest.
It also identifies external-owned skills without making this repository their
source owner. Its accepted release pin supplies the manifest SHA-256 and bytes.
A `MANIFEST` source commit resolves to that pin's repository commit. This avoids
embedding a file's own future commit identity inside itself.

The manifest remains `CANDIDATE` until authorized promotion after independent
review. A local `CURRENT` result remains unpublished until its release identity
is bound to a verified publication commit.
A candidate packet is preparation only. It cannot establish installed currentness.

The tracked `substrate8-hooks/hand-managed/skillsync` checker in
`Substrate-8/team-hub-operator-web` owns current resolution and packet generation.
It reads only manifest rows. The former installed `.sync-manifest` list is a
legacy replica and cannot select source bytes. Generated packets live only in
`distribution/current/` and carry the manifest identity, surface adaptation,
complete member identities, and a detached packet SHA-256.

The portable conformance pack lives only in `distribution/conformance/`.
`tools/build-conformance-pack.py` generates it from the CURRENT manifest and
each canonical SKILL.md frontmatter, resolving member bytes through the same
`skillsync` checker. It carries the exact manifest, one firing matrix, one probe
set, the operator-owned surface profiles, and the canonical bodies. It is a
derived distribution snapshot for hosts; it is never a source owner, and its
`--check` mode must reproduce the committed pack byte for byte.

`test-verification` has one consolidated behavior body here. The Team Hub
repository keeps a generated routing pointer controlled by this manifest.
Its pointer contains no second test policy. The objective-integrity reference
stays conditional under the consolidated root.

## Verification

`node tools/check-standing-distribution.mjs` enforces the exact public
eight-skill package, the retired identifiers, and the non-skill register guard.

## Candidate-to-release transition

`tools/promote-current-manifest.py` is the sole promotion entry point. It uses
`Manifest`, `source_members`, and adaptation checks from the existing S8
`skillsync` owner. Supply that source file explicitly with its accepted SHA-256.
Do not substitute an installed copy. The tool needs Python 3, Git, Node.js, and
read access to each source owner's `origin/main`.

The release authority supplies a JSON authorization file and its SHA-256 through
the governed release instruction. Its schema is:

```json
{
  "schema": "canonical-skill-release-authorization/v1",
  "repository": "Ezra144israel/governed-agent-skills",
  "base_commit": "<40 lowercase hexadecimal characters>",
  "candidate": {
    "bytes": 62020,
    "sha256": "<accepted candidate SHA-256>",
    "revision": "<accepted candidate revision>"
  },
  "checker": {"bytes": 0, "sha256": "<accepted checker SHA-256>"},
  "accepted_review": {
    "status": "ACCEPTED",
    "repository": "Ezra144israel/operator-agent-relay",
    "path": "relay/returns/<accepted review>.md",
    "blob": "<review Git blob>"
  },
  "release_authorization": {
    "status": "AUTHORIZED",
    "action": "PROMOTE_FOR_PUBLICATION",
    "repository": "Ezra144israel/operator-agent-relay",
    "path": "relay/dispatches/<release instruction>.md",
    "blob": "<release instruction Git blob>"
  }
}
```

Replace the example values with exact accepted identities, including checker
bytes. The supplied authorization digest is a trust input. The tool verifies
its bytes and required fields. It does not authenticate the author or fetch the
cited Relay records. The governing release instruction must verify those records
and supply the digest. A Builder-generated file does not grant release authority.

The default command prepares the release without writing it:

```sh
python3 tools/promote-current-manifest.py \
  --checker "$RELEASE_CHECKER" --checker-sha256 "$RELEASE_CHECKER_SHA256" \
  --authorization "$RELEASE_AUTHORIZATION" \
  --authorization-sha256 "$RELEASE_AUTHORIZATION_SHA256" \
  --source-root "Ezra144israel/governed-agent-skills=$RELEASE_GAS_ROOT" \
  --source-root "Substrate-8/team-hub-operator-web=$RELEASE_S8_ROOT" \
  --source-root "Ezra144israel/collective-intelligence-layer=$RELEASE_CIL_ROOT"
```

Supply exactly the source owners in the candidate. Each root must identify its
owner through `origin`. Local HEAD must equal the authorized base. The tool
checks each owner's live remote head against the manifest's source commit, or
the authorized base for this repository. Missing access or drift blocks the run.
Current member bytes and declared adaptations must match the canonical checker.
Forbidden source locations are rejected by that same checker.

Success returns `PREPARED_READ_ONLY` and the deterministic release SHA-256 and
byte count. With explicit release authority, add `--write` to replace only
`current-skills.json`. This returns `PROMOTED_UNPUBLISHED`. The output changes
only `status` to `CURRENT`. Canonical JSON encoding is required before promotion.
Ownership, lifecycle, targets, source members, and skill bytes stay unchanged.
A second write refuses with `ALREADY_PROMOTED`.

After separately authorized publication, use the same inputs with
`--verify-published <publication-commit>`. This read-only check requires the
publication commit's sole parent to equal the authorized base, the live remote
head to equal that commit, and all committed source members to match. Success
returns `PUBLISHED_CURRENT` with commit, manifest SHA-256, and bytes. These are
the identity fields for the existing accepted release pin. `MANIFEST` resolves
to that commit through the pin. The manifest never contains its own future hash.

These commands do not commit, push, create a release pin, generate packets, or
install skills. Existing candidate packets must be regenerated through the
canonical checker for the accepted release identity before distribution.
`BLOCKED` target dispositions remain blocked after source publication.

`node tools/check-standing-distribution.mjs --require-current` checks the
standing distribution and requires `CURRENT`. Its success alone is not a
publication receipt or an accepted install pin. The default check still permits
candidate development.

Run the focused regression suite with an explicit source dependency:

```sh
SKILLSYNC_TEST_CHECKER="$RELEASE_CHECKER" python3 tools/test_promote_current_manifest.py
```

The suite pins the tested checker to SHA-256
`e7c5d0cc74a167b917279394841e7e573ab672a17de3c7a528ecadb3e82c480c`.
It uses disposable Git repositories and substitutes only remote transport.
It does not promote the real candidate or publish test commits.
