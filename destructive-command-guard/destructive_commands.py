#!/usr/bin/env python3
"""Deny a small set of catastrophic Bash commands before your agent executes them.

This file is the surface adapter: it reads whatever payload shape the calling
agent sends, asks guard_core for a verdict, and writes that verdict back in the
shape that agent understands. The matching logic lives in guard_core.py and is
identical on every surface.

Supported envelopes are detected automatically from the payload:

  claude       Claude Code and Codex   tool_input.command            exit 0
  kimi         Kimi CLI                tool_input.command            exit 2
  cursor       Cursor                  command                       exit 0
  antigravity  Antigravity             toolCall.args.CommandLine     exit 0

Kimi shares Claude's payload and deny shape but identifies its shell tool as
"Shell" rather than "Bash", and blocks on exit code 2 rather than on the JSON
alone — so the exit code travels with the envelope.

Set DESTRUCTIVE_GUARD_ENVELOPE to one of those names to skip detection.

Adding a surface means adding one entry to ENVELOPES below. Nothing in
guard_core.py should need to change.
"""

import importlib.util
import json
import os
import sys
from pathlib import Path


# Loaded by path so the hook works regardless of cwd or sys.path. A missing
# guard_core.py raises loudly and on purpose: a guard that silently degrades to
# a no-op is worse than one that visibly fails, because you would go on
# believing you were protected.
_CORE_PATH = Path(__file__).with_name("guard_core.py")
_spec = importlib.util.spec_from_file_location("guard_core", _CORE_PATH)
guard_core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard_core)


def _as_command_list(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return None


def _claude_extract(payload):
    """Claude Code and Codex: {"tool_input": {"command": ...}}"""
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    return _as_command_list(tool_input.get("command"))


def _claude_render(reason):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def _kimi_extract(payload):
    """Kimi CLI: same payload as Claude Code, but the tool is named "Shell".

    Distinguishing the two matters because Kimi requires exit code 2 to block.
    A Kimi payload that fell through to the claude envelope would print a
    perfectly correct denial and exit 0 — the command would run anyway.
    """
    if payload.get("tool_name") != "Shell":
        return None
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    return _as_command_list(tool_input.get("command"))


def _cursor_extract(payload):
    """Cursor beforeShellExecution: {"command": "...", "cwd": ...}"""
    return _as_command_list(payload.get("command"))


def _cursor_render(reason):
    return {
        "permission": "deny",
        "user_message": reason,
        "agent_message": reason,
    }


def _antigravity_extract(payload):
    """Antigravity PreToolUse: {"toolCall": {"args": {"CommandLine": ...}}}"""
    tool_call = payload.get("toolCall")
    if not isinstance(tool_call, dict):
        return None
    args = tool_call.get("args")
    if not isinstance(args, dict):
        return None
    return _as_command_list(args.get("CommandLine"))


def _antigravity_render(reason):
    return {"decision": "deny", "reason": reason}


# (name, extract, render, deny_exit_code)
#
# Order matters. Kimi must precede claude because its payload also carries
# tool_input.command and would otherwise be handled with the wrong exit code.
# Cursor's flat "command" key is the loosest match, so it is tried last.
#
# The exit code is part of the surface contract, not an implementation detail:
# Kimi blocks on exit 2, while the others honour the JSON alone and are left at
# 0 because that is the behaviour verified against them.
ENVELOPES = (
    ("antigravity", _antigravity_extract, _antigravity_render, 0),
    ("kimi", _kimi_extract, _claude_render, 2),
    ("claude", _claude_extract, _claude_render, 0),
    ("cursor", _cursor_extract, _cursor_render, 0),
)


def detect_envelope(payload):
    """Return (name, commands, render, deny_exit_code) for the first match."""
    forced = os.environ.get("DESTRUCTIVE_GUARD_ENVELOPE")
    candidates = ENVELOPES
    if forced:
        candidates = tuple(item for item in ENVELOPES if item[0] == forced)

    for name, extract, render, deny_exit_code in candidates:
        commands = extract(payload)
        if commands is not None:
            return name, commands, render, deny_exit_code
    return None, [], None, 0


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError, UnicodeError):
        return 0
    if not isinstance(payload, dict):
        return 0

    _name, commands, render, deny_exit_code = detect_envelope(payload)
    if render is None:
        return 0

    for command in commands:
        reason = guard_core.denial_reason(command)
        if reason:
            json.dump(render(reason), sys.stdout)
            sys.stdout.write("\n")
            return deny_exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
