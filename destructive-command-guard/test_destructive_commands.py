#!/usr/bin/env python3
"""Regression tests for the destructive-command PreToolUse hook."""

import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import unittest


HOOK = Path(__file__).with_name("destructive_commands.py")

spec = importlib.util.spec_from_file_location("destructive_commands", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)

BLOCKED_COMMANDS = {
    "sentinel": "destructive-guard-self-test",
    "rm-short": "rm -rf /",
    "rm-reordered-short": "rm -fr /*",
    "rm-split-flags": "rm -r -f ~",
    "rm-reversed-split": "rm -f -r $HOME",
    "rm-long": "rm --recursive --force /Users",
    "rm-reordered-long": "rm --force --recursive /System",
    "rm-double-slash": "rm -rf //",
    "rm-traversal": "rm -rf /tmp/..",
    "rm-unset-absolute": "rm -rf /$GUARD_HOOK_DEFINITELY_UNSET",
    "rm-default-absolute": "rm -rf ${GUARD_HOOK_DEFINITELY_UNSET:-/Users}",
    "rm-empty-assignment": "EMPTY= rm -rf /$EMPTY",
    "rm-command-substitution": "rm -rf $(printf /)",
    "rm-users-glob": "rm -rf /U*sers",
    "rm-system-glob": "rm -rf /System/*",
    "rm-system-descendant": "rm -rf /System/Library",
    "rm-ansi-users": "rm -rf $'/Users'",
    "rm-ansi-concatenated-system": "rm -rf $'/Sys''tem'",
    "rm-ansi-hex-users": r"rm -rf $'\x2fUsers'",
    "rm-ansi-embedded-users": r"rm -rf /Use$'\x72's",
    "rm-ansi-adjacent-embedded-users": r"rm -rf /Use$'\x72'$'\x73'",
    "rm-ansi-embedded-system": r"rm -rf /Sys$'\x74'em",
    "rm-ansi-traversal-users": r"rm -rf /Users$'\x2f'..$'\x2f'Users",
    "rm-ansi-sudo-wrapper": r"sudo rm -fr /Use$'\x72's",
    "rm-ansi-reordered-long": r"rm --force --recursive /Sys$'\x74'em",
    "rm-ansi-bash-nested": r'''bash -c "rm -rf /Use$'\x72's"''',
    "rm-ansi-eval-nested": r'''eval "rm -rf /Use$'\x72's"''',
    "sudo": "sudo -u root rm -rf /System",
    "env": "env FOO=bar rm -rf /",
    "env-split": "env -S \"bash -c 'rm -rf /'\"",
    "env-long-split": "env --split-string=\"bash -c 'rm -rf /'\"",
    "assignment": "FOO=bar rm -rf /",
    "command-wrapper": "command rm -rf /",
    "command-path-wrapper": "command -p rm -rf /",
    "nohup-wrapper": "nohup rm -rf /",
    "nohup-separator-wrapper": "nohup -- rm -rf /",
    "exec-wrapper": "exec rm -rf /",
    "exec-argv-wrapper": "exec -a cleanup rm -rf /",
    "nice-wrapper": "nice -n 5 rm -rf /Users",
    "time-wrapper": "time -p rm -rf /System",
    "semicolon": "echo ok; rm -rf /",
    "and": "true && sudo rm -fr /",
    "or": "false || env X=1 rm --force --recursive /System",
    "pipe": "echo ok | rm -rf /",
    "newline": "echo ok\nrm -rf /",
    "bash": "bash -c 'rm -rf /'",
    "bash-options": "bash -O extglob -c 'rm -rf /'",
    "sh": "sh -c 'rm -rf /System'",
    "zsh": "zsh -fc 'rm -rf /Users'",
    "dash": "dash -c 'rm -rf /'",
    "ksh": "ksh -c 'rm -rf /'",
    "eval": "eval 'rm -rf /'",
    "assigned-bash": "CMD='rm -rf /' bash -c \"$CMD\"",
    "assigned-direct": "CMD='rm -rf /' $CMD",
    "persisted-assignment": "CMD='rm -rf /'; $CMD",
    "expanded-target-list": "TARGET='/ /tmp/build' rm -rf $TARGET",
    "diskutil-erase-disk": "diskutil eraseDisk APFS Empty disk4",
    "diskutil-erase-volume": "sudo diskutil eraseVolume APFS Empty disk4s1",
    "diskutil-partition": "diskutil partitionDisk disk4 1 GPT APFS Empty 100%",
    "mkfs": "mkfs /dev/disk4",
    "mkfs-variant": "env X=1 mkfs.ext4 /dev/disk4",
}

SAFE_COMMANDS = {
    "ls": "ls",
    "git-status": "git status",
    "bare-star": "rm -rf *",
    "dot-star": "rm -rf ./*",
    "log-glob": "rm -rf *.log",
    "node-modules": "rm -rf ./node_modules",
    "tmp-build": "rm -rf /tmp/build",
    "home-project": "rm -rf ~/project",
    "specific-other-user-project": "rm -rf /Users/example/project",
    "recursive-only": "rm -r /",
    "force-only": "rm -f /",
    "diskutil-list": "diskutil list",
    "echo-mkfs": "echo mkfs /dev/disk4",
    "bash-safe": "bash -c 'git status'",
    "bash-safe-home": "bash -c 'echo $HOME'",
    "nested-safe-rm": "bash -c 'rm -rf ./node_modules'",
    "bash-option-safe": "bash -O extglob -c 'echo ok'",
    "env-split-safe": "env -S \"bash -c 'echo ok'\"",
    "eval-safe": "eval 'echo ok'",
    "command-query-safe": "command -v rm",
    "nice-safe": "nice -n 5 git status",
    "time-safe": "time -p git status",
    "safe-variable-target": "rm -rf $BUILD_DIR",
    "safe-assigned-targets": "TARGET='/tmp/a /tmp/b' rm -rf $TARGET",
    "nonpersistent-assignment": "CMD='rm -rf /' echo ok; $CMD",
    "unparseable-segment": "rm -rf 'unterminated",
    "ansi-echo": r"echo $'\n'",
    "ansi-rm-recursive-only": r"rm -r /Use$'\x72's",
    "ansi-rm-force-only": r"rm -f /Use$'\x72's",
}


def payload(command):
    return json.dumps(
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": command},
        }
    )


def invoke(raw_input):
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=raw_input,
        text=True,
        capture_output=True,
        check=False,
    )


class DestructiveCommandHookTests(unittest.TestCase):
    def test_blocked_commands_return_documented_deny_shape(self):
        for name, command in BLOCKED_COMMANDS.items():
            with self.subTest(name=name):
                result = invoke(payload(command))
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stderr, "")
                output = json.loads(result.stdout)
                hook_output = output["hookSpecificOutput"]
                self.assertEqual(hook_output["hookEventName"], "PreToolUse")
                self.assertEqual(hook_output["permissionDecision"], "deny")
                self.assertTrue(hook_output["permissionDecisionReason"])

    def test_safe_commands_produce_no_decision(self):
        for name, command in SAFE_COMMANDS.items():
            with self.subTest(name=name):
                result = invoke(payload(command))
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_malformed_payloads_fail_open(self):
        malformed = {
            "invalid-json": "not-json",
            "null": "null",
            "missing-tool-input": "{}",
            "missing-command": '{"tool_input": {}}',
            "wrong-command-type": '{"tool_input": {"command": 42}}',
        }
        for name, raw_input in malformed.items():
            with self.subTest(name=name):
                result = invoke(raw_input)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")

    def test_list_payload_denies_when_any_command_is_blocked(self):
        result = invoke(payload(["git status", "sudo rm -rf /System"]))
        self.assertEqual(result.returncode, 0)
        output = json.loads(result.stdout)
        self.assertEqual(
            output["hookSpecificOutput"]["permissionDecision"],
            "deny",
        )

    def test_nested_command_depth_is_bounded(self):
        nested = "rm -rf /"
        for _ in range(hook.MAX_NESTED_COMMAND_DEPTH + 2):
            nested = "bash -c " + shlex.quote(nested)
        self.assertEqual(hook.denial_reason(nested), hook.INSPECTION_LIMIT_REASON)

    def test_rm_reason_matches_declared_coverage(self):
        self.assertEqual(
            hook.denial_reason("rm -rf /System/Library"),
            hook.RM_REASON,
        )
        self.assertNotIn("macOS system files", hook.RM_REASON)


if __name__ == "__main__":
    unittest.main()
