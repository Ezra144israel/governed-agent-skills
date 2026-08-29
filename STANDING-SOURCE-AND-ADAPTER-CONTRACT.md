# Standing source and adapter contract

Status: active.

## Source home

This repository is the public source home for its six governed agent skills.
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

## External attribution: not included or distributed

The repository's editing process drew on `grilling` from
`mattpocock/skills` and `unslop` from `cursor/plugins` by Lauren Tan.
Both are MIT-licensed. Neither skill is included or distributed here.

## Verification

`node tools/check-standing-distribution.mjs` enforces the exact public
six-skill package, the retired identifiers, and the non-skill register guard.
