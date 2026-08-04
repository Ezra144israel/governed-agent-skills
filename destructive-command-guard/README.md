# Pattern: Destructive-Command Guard

The skills in this repo are instructions — they lower the frequency of bad
actions, but they cannot technically prevent one. This pattern is the
enforcement layer they tell you to pair with: a PreToolUse hook that intercepts
every Bash command before your agent executes it and denies a small set of
catastrophic operations outright.

Instructions lower the frequency; this caps the damage.

## Files

| File | What it is |
|---|---|
| [`destructive_commands.py`](destructive_commands.py) | The hook. Copy into your hooks directory. |
| [`test_destructive_commands.py`](test_destructive_commands.py) | Regression suite. Run it before you rely on the guard. |

## What it blocks — and what it deliberately doesn't

**Blocked:** recursive+force `rm` aimed at the root filesystem, `/Users` (and
globs under it), `/System` (and descendants), or the current home directory —
including attempts routed through `sudo`, `env`, `nohup`, `exec`, `nice`,
`time`, chained commands (`&&`, `;`, `|`), variable indirection, nested
`bash -c` (eight levels deep; anything dynamic it cannot inspect is denied),
and ANSI-C quoting tricks. Also blocked: `diskutil erase*/partition*` and any
`mkfs`.

**Deliberately out of scope** — this is a targeted denylist, NOT a sandbox:
`dd` to a device, `find ... -delete`, `xargs rm`, deletions of specific project
folders (`rm -rf ~/my-project` is allowed — that's what backups are for), and
quoting tricks assembled outside the inspected segment. The script's own header
documents these accepted residuals.

Pair the guard with real backups or snapshots. It is a tripwire against
catastrophe, not a substitute for recovery.

The protected-path set is macOS-flavored (`/Users`, `/System`). On Linux, extend
the `protected` set in `is_protected_rm_target` with `/home`, `/etc`, `/usr`,
and whatever else you consider unsurvivable.

## Install

Copy the hook into your agent's hooks directory:

```
# Claude Code
mkdir -p ~/.claude/hooks
cp destructive_commands.py test_destructive_commands.py ~/.claude/hooks/

# Codex
mkdir -p ~/.codex/hooks
cp destructive_commands.py test_destructive_commands.py ~/.codex/hooks/
```

### Wiring — Claude Code

Add to `~/.claude/settings.json`, merging into your existing `hooks` block if
you have one:

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

Add to `~/.codex/hooks.json`:

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

Note the matcher differs between surfaces: Claude Code uses `Bash`, Codex uses
the anchored `^Bash$`.

## Verify it's live

The guard has a built-in sentinel. In a **fresh** agent session, ask the agent
to run:

```
destructive-guard-self-test
```

Expected: the command is DENIED before execution, with the reason
`Destructive-command guard self-test denied before Bash execution.`

If it runs instead — harmlessly failing as command-not-found — the hook is not
wired. Fix the wiring before trusting it. This is the hook equivalent of a load
receipt: activation proven, not assumed.

The sentinel is safe by design. If the guard is dead, nothing happens; if it is
live, nothing executes. Never test a guard with a command that would do real
damage if the guard failed.

## Tests

```
python3 test_destructive_commands.py
```

All tests should pass before you rely on the guard, and you should rerun them
after any modification — especially after editing the protected-path set or
adding a wrapper clause.

## Extending it

**Trusting your own wrapper commands.** If you route commands through a logger
or launcher of your own, the guard will see your wrapper as the executable and
stop looking. `strip_wrappers` carries a marked comment showing where to add a
clause so the guard sees through it to the real command.

**Adding protected paths.** Extend the `protected` set in
`is_protected_rm_target`, then add matching cases to `BLOCKED_COMMANDS` in the
test file and rerun.

## Design notes

Fail-open on malformed payloads is a deliberate contract: a broken hook should
not brick every Bash call, because a guard that gets disabled in frustration
protects nothing.

Fail-closed applies where it matters — a nested command too deep or too dynamic
to inspect is denied, and an ANSI-C-quoted segment that resolves to destructive
`rm` is denied without resolving the quoting.

Denials return the documented PreToolUse deny shape, so the agent receives the
reason and can adapt instead of retrying blindly.
