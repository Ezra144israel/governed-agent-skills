# Pattern: Destructive-Command Guard

The skills in this repo are instructions — they lower the frequency of bad
actions, but they cannot technically prevent one. This pattern is the
enforcement layer they tell you to pair with: a pre-execution hook that
intercepts every shell command before your agent runs it and denies a small set
of catastrophic operations outright.

Instructions lower the frequency; this caps the damage.

## Files

| File | What it is |
|---|---|
| [`guard_core.py`](guard_core.py) | The matching logic. Knows nothing about any agent. |
| [`destructive_commands.py`](destructive_commands.py) | The hook you wire up. Reads your agent's payload shape, answers in its deny shape. |
| [`test_guard_core.py`](test_guard_core.py) | 90 command cases against the core. Surface-free. |
| [`test_adapters.py`](test_adapters.py) | Envelope tests — one per supported surface. |

The split is the point. Every agent wraps the command in a different envelope
and expects a different deny response, but the question *"is this command
catastrophic?"* has the same answer everywhere. `guard_core.py` answers it;
`destructive_commands.py` translates. Porting to a new agent means adding one
entry to `ENVELOPES` — never touching the core.

## Supported surfaces

| Surface | Hook event | Config file | Command at | Deny response | Deny exit |
|---|---|---|---|---|---|
| Claude Code | `PreToolUse` | `~/.claude/settings.json` | `tool_input.command` | `hookSpecificOutput.permissionDecision` | 0 |
| Codex | `PreToolUse` | `~/.codex/hooks.json` | `tool_input.command` | same as Claude Code | 0 |
| Antigravity | `PreToolUse` | `.agents/hooks.json` or `~/.gemini/config/` | `toolCall.args.CommandLine` | `decision` | 0 |

The hook detects which envelope it is being called with and replies in kind. No
per-surface build, no configuration flag. Set `DESTRUCTIVE_GUARD_ENVELOPE` to
`claude` or `antigravity` if you ever need to force one.

**Every surface listed here has been confirmed working in a live session.**
Other agents expose pre-execution hooks and are straightforward to add — the
work is an envelope adapter, not a change to the guard — but nothing goes in
this table on documentation alone. A surface that passes every offline test can
still fail to call the hook at all, and a guard you believe in but that never
runs is worse than no guard.

## What it blocks — and what it deliberately doesn't

**Blocked:** recursive+force `rm` aimed at the root filesystem, `/Users` (and
globs under it), `/System` (and every descendant), or the current home
directory — including attempts routed through `sudo`, `env`, `nohup`, `exec`,
`nice`, `time`, chained commands (`&&`, `;`, `|`), variable indirection, nested
`bash -c` (eight levels deep; anything dynamic it cannot inspect is denied), and
ANSI-C quoting tricks. Also blocked: `diskutil erase*/partition*` and any
`mkfs`.

**Deliberately out of scope** — this is a targeted denylist, NOT a sandbox:
`dd` to a device, `find ... -delete`, `xargs rm`, deletions of specific project
folders (`rm -rf ~/my-project` is allowed — that's what backups are for), and
quoting tricks assembled outside the inspected segment. `guard_core.py`'s header
documents these accepted residuals.

Pair the guard with real backups or snapshots. It is a tripwire against
catastrophe, not a substitute for recovery.

## Install

Requires `python3` and nothing else — no packages, no virtualenv. Standard
library only, and it runs on the system Python that ships with macOS (verified
on 3.9). If `python3` resolves for you, the guard runs.

Copy both Python files into your agent's hooks directory — the hook loads the
core from its own directory, so they must sit together:

```
mkdir -p ~/.claude/hooks
cp guard_core.py destructive_commands.py ~/.claude/hooks/
```

Substitute `~/.codex/hooks/` or `~/.gemini/config/hooks/` as appropriate. A
missing `guard_core.py` makes the hook fail loudly rather than silently pass
every command — see Design notes.

### Wiring — Claude Code

`~/.claude/settings.json`, merging into your existing `hooks` block:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/hooks/destructive_commands.py\"",
            "timeout": 30,
            "statusMessage": "Checking destructive command policy"
          }
        ]
      }
    ]
  }
}
```

### Wiring — Codex

`~/.codex/hooks.json`. Same shape, but note the anchored matcher:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.codex/hooks/destructive_commands.py\"",
            "timeout": 30,
            "statusMessage": "Checking destructive command policy"
          }
        ]
      }
    ]
  }
}
```

### Wiring — Antigravity

`hooks.json` in `.agents/` in your workspace, or `~/.gemini/config/` for all
projects. Antigravity's schema differs from the others in two ways worth
reading carefully: the top level is a map of **named hook groups**, not a
`hooks` key, and the `matcher` selects a **tool name** (`run_command`), not a
command pattern.

```json
{
  "destructive-command-guard": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.gemini/config/hooks/destructive_commands.py\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

> **Watch the `enabled` key.** Antigravity hook groups accept
> `"enabled": false`, and the safety-gate example in their own documentation
> ships with it set. Copy that example as a starting point and you get a guard
> that is wired, syntactically valid, and doing nothing. Omit the key (it
> defaults to enabled) or set it to `true` — then prove it with the sentinel
> below rather than trusting the file.

Scripts are run as shell commands, and the doc's examples use relative paths
(`./scripts/lint.sh`) without stating what they are relative to. Use an absolute
`$HOME`-anchored path as above and the ambiguity disappears.

## Verify it's live

The guard has a built-in sentinel. In a **fresh** agent session, ask the agent
to run:

```
destructive-guard-self-test
```

Expected: DENIED before execution, reason
`Destructive-command guard self-test denied before Bash execution.`

If it runs instead — harmlessly failing as command-not-found — the hook is not
wired. Fix the wiring before trusting it. This is the hook equivalent of a load
receipt: activation proven, not assumed.

The sentinel is safe by design. If the guard is dead, nothing happens; if it is
live, nothing executes. **Never test a guard with a command that would do real
damage if the guard failed.**

Each surface wraps the denial in its own error format. On Antigravity it
surfaces as an invalid-tool-call error carrying the reason through:

```
Error invalid tool call: model output error: invalid tool call error
(invalid_args) tool call denied with reason: Destructive-command guard
self-test denied before Bash execution.
```

Recognize the wrapper for your surface so you can tell a real denial from a
command that merely failed.

### Getting an answer you can trust

Ask the agent to run the compound form instead of the bare sentinel:

```
echo GUARD_INACTIVE_PROOF && destructive-guard-self-test
```

The whole command is denied as one unit, so `GUARD_INACTIVE_PROOF` can only
appear in the output if the guard failed to fire. A bare sentinel proves the
guard is live only if you trust the agent's report of being blocked — and an
agent that has just read the expected reason string can reproduce it whether or
not it was actually stopped. Here the passing result is *no output at all*,
which is the one thing a plausible reconstruction cannot produce.

## Tests

```
python3 test_guard_core.py
python3 test_adapters.py
```

Both must pass before you rely on the guard, and after any modification. The
core suite runs in-process and finishes in well under a second, so there is no
excuse for skipping it.

## Extending it

**A new agent surface.** Add an extract/render pair and one `ENVELOPES` entry in
`destructive_commands.py`, then add the surface to `ENVELOPES` in
`test_adapters.py`. The core is untouched, and the core suite still proves the
matching logic.

**Your own wrapper commands.** If you route commands through a logger or
launcher, the guard sees your wrapper as the executable and stops looking.
`strip_wrappers` in `guard_core.py` carries a marked comment showing where to add
a clause so it sees through to the real command.

**More protected paths.** `guard_core.py` has two sets, and they are
deliberately not symmetric:

- `PROTECTED_ROOTS` — the root itself and any glob under it are denied, but a
  named descendant is allowed. `rm -rf /Users` and `rm -rf /Users/*` are denied;
  `rm -rf /Users/you/project` is your own project and is allowed.
- `SEALED_ROOTS` — every descendant is denied, named or not. `rm -rf
  /System/Library` is denied.

On Linux you would likely add `/home` to `PROTECTED_ROOTS` and `/etc`, `/usr`,
`/boot` to `SEALED_ROOTS`. `test_guard_core.py` asserts the asymmetry
generically, so it will cover your additions — but add explicit cases too, and
rerun both suites.

## Design notes

**Fail open on malformed payloads** is a deliberate contract: a broken hook
should not brick every shell call, because a guard that gets disabled in
frustration protects nothing. An unrecognized envelope is treated the same way —
the hook stays silent rather than guessing at a deny format the agent might not
understand.

**Fail closed where it matters.** A nested command too deep or too dynamic to
inspect is denied. An ANSI-C-quoted segment that resolves to destructive `rm` is
denied without resolving the quoting.

**Fail loudly on a broken install.** A missing `guard_core.py` raises rather than
degrading to a no-op, because the dangerous failure is not a crash — it is
believing you are protected when you are not.

Denials return each surface's documented deny shape, so the agent receives the
reason and can adapt instead of retrying blindly.

## Verification status

| Surface | Envelope tested | Run in a live session |
|---|---|---|
| Claude Code | yes | yes |
| Codex | yes | yes |
| Antigravity | yes | yes |

"Envelope tested" and "run in a live session" are deliberately separate columns,
and nothing ships here on the first alone. The first says the hook reads and
writes that surface's wire format correctly, which a test can establish offline.
The second says the surface actually calls the hook and honours the denial,
which only a real session can establish.

A guard that passes the first and fails the second is the dangerous case: it
looks installed, its config reads correctly, its tests are green, and it
protects nothing. That is not hypothetical — it is why this table is shorter
than the set of agents whose hook APIs are documented.
