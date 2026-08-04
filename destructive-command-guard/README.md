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

| Surface | Hook event | Config file | Command at | Deny response |
|---|---|---|---|---|
| Claude Code | `PreToolUse` | `~/.claude/settings.json` | `tool_input.command` | `hookSpecificOutput.permissionDecision` |
| Codex | `PreToolUse` | `~/.codex/hooks.json` | `tool_input.command` | same as Claude Code |
| Cursor | `beforeShellExecution` | `~/.cursor/hooks.json` | `command` | `permission` |
| Antigravity | `PreToolUse` | `.agents/hooks.json` or `~/.gemini/config/` | `toolCall.args.CommandLine` | `decision` |

The hook detects which envelope it is being called with and replies in kind. No
per-surface build, no configuration flag. Set `DESTRUCTIVE_GUARD_ENVELOPE` to
`claude`, `cursor`, or `antigravity` if you ever need to force one.

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

Copy both Python files into your agent's hooks directory — the hook loads the
core from its own directory, so they must sit together:

```
mkdir -p ~/.claude/hooks
cp guard_core.py destructive_commands.py ~/.claude/hooks/
```

Substitute `~/.codex/hooks/` or `~/.cursor/hooks/` as appropriate. A missing
`guard_core.py` makes the hook fail loudly rather than silently pass every
command — see Design notes.

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

### Wiring — Cursor

`~/.cursor/hooks.json` for all projects, or `.cursor/hooks.json` in one repo.
The `matcher` is a regex over the command; `.*` is deliberate here, because a
guard that only inspects some commands is not a guard:

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "python3 \"$HOME/.cursor/hooks/destructive_commands.py\"",
        "matcher": ".*"
      }
    ]
  }
}
```

### Wiring — Antigravity

Antigravity fires `PreToolUse` before `run_command` and honours
`{"decision": "deny"}`, with `hooks.json` living in `.agents/` in the workspace
or `~/.gemini/config/`. Check Antigravity's own hooks documentation for the
exact entry syntax — the payload and response shapes are handled for you, but
the surrounding config schema is theirs and it is not reproduced here from
memory.

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

Claude Code and Codex wiring have been run in practice. The Cursor and
Antigravity envelopes are implemented from those products' published hook
documentation and are covered by `test_adapters.py`, but have not been executed
inside a live session on either product. If you are the first to run one, the
sentinel above is how you find out.
