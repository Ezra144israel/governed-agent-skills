# Instruction Layer source and adapter contract

Status: active.

## Public source home

This repository is the complete public source home for the six-skill
Instruction Layer. Each skill and its required reference files resolve inside
this repository. Release and verification commands use only files from this
repository.

Installed copies are releases or user-owned adapters. An adapter must declare
its change. An undeclared byte difference is drift.

The two Enforcement Layer guards have separate READMEs. They are outside the
skill distribution.

## Skill distribution

| Skill | Public files | Dependencies |
|---|---|---|
| `reasoning-doctrine` | `SKILL.md` and four files in `references/` | none |
| `governed-operator` | `SKILL.md` | `reasoning-doctrine` |
| `write-maintainable-code` | `SKILL.md` | none |
| `portable-adaptive-planning` | `SKILL.md` and `references/blueprint.md` | none |
| `test-verification` | `SKILL.md` and `reference/objective-integrity.md` | none |
| `ship-it-or-fix-it` | `SKILL.md` | `governed-operator`, `reasoning-doctrine`, and `test-verification` |

No skill absent from this table is part of the public package.

## Isolation boundary

The public package has no release or validation dependency on another source
checkout, an installed personal skill, a credential, a generated mirror, or an
external state manifest. A clean copy of this repository can run the public
package checks with Python and the runtimes required by each guard.

The plugin manifests install the six skill directories. They do not install,
wire, or activate either guard. Guard installation remains a separate manual
action described in each guard's README.

## Verification

Run these checks from the repository root:

```text
python3 -m unittest tools/test_check_public_package.py -v
python3 tools/check_public_package.py
python3 -m unittest tools/test_repository_security_check.py -v
python3 tools/repository_security_check.py
```

The public package checker verifies the exact skill file set, local reference
closure, plugin version and description agreement, documentation count
agreement, and the absence of release archives or external local dependencies.
