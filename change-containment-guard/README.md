# Enforcement Layer: Change-containment guard

The Instruction Layer tells agents how to work. `write-maintainable-code` helps
an agent choose the smallest useful change. This Enforcement Layer guard checks
the part that should not depend on judgment. It verifies that the final
repository state stayed inside an exact, sealed change contract.

The skill owns maintainability. The guard owns containment.

## What it proves

The Rust core binds a contract to one repository, branch, HEAD, and possibly
dirty baseline. It compares the final index and working tree with that baseline,
then classifies every added, deleted, or modified path as implementation, test,
evaluator, dependency, generated, or unclassified.

It handles tracked, staged, unstaged, untracked non-ignored files, symlinks, and
submodule pointers. A rename is reported as a deletion plus an addition.
Wherever they appear, `.gitignore`, `.gitattributes`, and `.gitmodules` need
exact full-path rules. Symlink and submodule changes need their entry kinds
named. Dependency and generated paths need their matching classes. Test
suppression is checked in the named Rust, Python, JavaScript/TypeScript, Go,
Java/JUnit, and Ruby/RSpec ecosystems from the contract. A changed test-looking
path outside those declarations stops for human classification.

Ignored files are outside the state identity by design. Git decides whether a
file is ignored. A change to any `.gitignore` path remains protected.

## Files

| File | Purpose |
|---|---|
| `src/lib.rs` | Repository identity, contract, classification, receipt, and envelope core |
| `src/main.rs` | The single command-line and hook entry point |
| `contract.example.json` | Unsealed contract example. Copy it outside the candidate write scope before editing. |
| `COMPONENT-DECISIONS.md` | Benefit-based language and dependency decisions |
| `PACKAGING.md` | Source-only packaging boundary, planned targets, and measurement plan |
| `tests/` | Public-seam tests using disposable real Git repositories |

## Contract lifecycle

Keep the contract and receipt outside the agent's permitted repository write
scope. Start from `contract.example.json`, reduce it to the actual task, then
seal the baseline once:

```text
change-containment-guard seal --contract /evidence/contract.json --repository /work/repo
```

The seal writes repository identity, baseline state, suppression counts, and a
SHA-256 contract hash into the contract. A second seal is rejected.

Check containment without running tests:

```text
change-containment-guard check --contract /evidence/contract.json --repository /work/repo
```

Exit `0` means contained. Exit `10` means the JSON result contains violations.
Parse, file, Git, and contract failures exit `2`.

Run one command already sealed in `verification_commands` and write a receipt:

```text
change-containment-guard verify --contract /evidence/contract.json --receipt /evidence/receipt.json --repository /work/repo -- cargo test --all-targets
```

The guard checks containment before and after the command. The receipt binds the
repository, branch, contract hash, final state hash, exact command, exit status,
and exact stdout/stderr digest. Raw command output is not copied into the
receipt. Combined captured output is limited to 16 MiB. Larger output fails
instead of creating an unbounded receipt. Consumers recompute current state:

```text
change-containment-guard check-receipt --contract /evidence/contract.json --receipt /evidence/receipt.json --repository /work/repo
```

A replaced contract, changed branch, different repository, later edit, reused
receipt, or nonzero verification result is rejected. The receipt records command
output identity but does not authenticate or independently reproduce the output.
A changed receipt is rejected when its integrity hash no longer matches. A
writer who can replace both `output_digest` and the unkeyed `receipt_hash` is
outside this integrity claim.

## Agent envelopes

`envelope` reads one JSON object on standard input. It accepts the public
Claude Code/Codex shape with `tool_input` and `cwd`, and the public Antigravity
shape with `toolCall.args` and `toolCall.args.Cwd`. The same Rust policy runs for
all three surfaces. A violation is returned in each existing public guard's deny
shape and in `changeContainmentGuard` details.

```text
change-containment-guard envelope --contract /evidence/contract.json
```

These adapters are tested offline. This candidate does not claim that every
product invokes a post-change hook at the needed time. Live dispatch must be
proved in a disposable profile before a surface is called supported.

## Honest limits

The guard does not decide whether code is readable, whether an abstraction was
necessary, whether a test is useful, or whether the contract expresses the
right outcome. A broad contract can faithfully prove a weak boundary. The
author of the contract, an independent reviewer, and the operator still own
those decisions.

The guard does not observe repository-external Git exclude sources such as
`.git/info/exclude`, `core.excludesFile`, or global exclude files.

The contract and receipt hashes are integrity identities, not signatures. If an
agent can rewrite the contract, receipt, and acceptance process, this tool does
not create an independent authority boundary. Store evidence outside its write
scope.

The guard observes state when invoked. It is not a daemon and does not watch
future edits. A valid receipt becomes stale after any bound state changes.

## Install boundary

Version 4 is source-only. It contains no published binaries. The plugin does not
install this guard. Cloning, building, or testing this directory activates
nothing. The binary does not edit Claude Code, Codex, Antigravity, shell, Git,
or account settings. Build instructions are in `PACKAGING.md`. Copying a
reviewed binary and wiring an agent hook are separate manual actions.
