#!/usr/bin/env python3
"""Deny a small set of catastrophic Bash commands before your agent executes them."""

# SCOPE (accepted limitations — this is a targeted denylist, NOT a shell sandbox):
#   Guards only: recursive+force `rm` of / , /System(+descendants), all of
#   /Users(+globs), and the current $HOME; `diskutil erase*/partition*`; `mkfs*`;
#   and the self-test sentinel. Every other destructive operation is out of scope
#   by design and intentionally allowed — e.g. dd to a device, `find … -delete`,
#   newfs_*, `chmod/chown -R` on system roots, `> /dev/disk*`, and deletion of
#   /Library, /Applications, /usr, /etc.
#   Because matching is static (shlex/posix, not a faithful Bash parser), Bash
#   ANSI-C quoting ($'…') that reaches `rm` from OUTSIDE the checked segment is a
#   known, accepted residual — e.g. outer-quote concatenation
#   (`bash -c 'rm -rf /Use'$'\x72''s'`) or variable-carried indirection
#   (`X=$'\x72'; rm -rf /Use${X}s`). In-segment $'…' IS caught (fail-closed).
#   Malformed/unparseable hook payloads fail OPEN by contract.

import fnmatch
import json
import os
import posixpath
import re
import shlex
import sys


SEGMENT_SEPARATOR = re.compile(r"&&|\|\||[;|\r\n]")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=.*$", re.DOTALL)
BRACED_PARAMETER = re.compile(r"\$\{[^{}]+\}")
BRACED_DEFAULT = re.compile(
    r"\$\{[A-Za-z_][A-Za-z0-9_]*(?::?[-=])([^{}]*)\}"
)
SIMPLE_PARAMETER = re.compile(
    r"\$(?:([A-Za-z_][A-Za-z0-9_]*)|\{([A-Za-z_][A-Za-z0-9_]*)\})"
)
GLOB_MAGIC = re.compile(r"[*?\[]")

RM_REASON = (
    "Never recursively force-delete the root filesystem, the current home "
    "directory, all user directories, or /System paths."
)
DISKUTIL_REASON = "Never erase or repartition a disk."
MKFS_REASON = "Never format a filesystem."
SELF_TEST_REASON = "Destructive-command guard self-test denied before Bash execution."
INSPECTION_LIMIT_REASON = (
    "Nested shell command exceeds the destructive-command inspection limit."
)
DYNAMIC_COMMAND_REASON = "Dynamic nested shell command cannot be safely inspected."

SHELL_EXECUTABLES = {"bash", "dash", "ksh", "sh", "zsh"}
SHELL_OPTIONS_WITH_VALUE = {"-O", "-o", "--init-file", "--rcfile"}
MAX_NESTED_COMMAND_DEPTH = 8
TIME_OPTIONS_WITH_VALUE = {"-f", "-o", "--format", "--output"}
NICE_OPTIONS_WITH_VALUE = {"-n", "--adjustment"}
EXEC_OPTIONS_WITH_VALUE = {"-a"}

SUDO_OPTIONS_WITH_VALUE = {
    "-C",
    "-D",
    "-g",
    "-h",
    "-p",
    "-R",
    "-T",
    "-t",
    "-u",
    "--chdir",
    "--close-from",
    "--group",
    "--host",
    "--other-user",
    "--prompt",
    "--role",
    "--type",
    "--user",
}
ENV_OPTIONS_WITH_VALUE = {"-C", "-u", "--chdir", "--unset"}


def command_strings(payload):
    if not isinstance(payload, dict):
        return []
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return []
    command = tool_input.get("command")
    if isinstance(command, str):
        return [command]
    if isinstance(command, list):
        return [item for item in command if isinstance(item, str)]
    return []


def split_segments(command):
    for raw_segment in SEGMENT_SEPARATOR.split(command):
        normalized = re.sub(r"\s+", " ", raw_segment).strip()
        if normalized:
            yield normalized


def consume_wrapper_options(tokens, options_with_value):
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return tokens[index + 1 :]
        if not token.startswith("-") or token == "-":
            break

        option_name = token.split("=", 1)[0]
        if option_name in options_with_value and "=" not in token:
            index += 2
        else:
            index += 1
    return tokens[index:]


def consume_env_options(tokens):
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return tokens[index + 1 :]
        if token in {"-S", "--split-string"}:
            if index + 1 >= len(tokens):
                return []
            try:
                split_tokens = shlex.split(tokens[index + 1], posix=True)
            except ValueError:
                return []
            return split_tokens + tokens[index + 2 :]
        if token.startswith("--split-string="):
            try:
                split_tokens = shlex.split(token.split("=", 1)[1], posix=True)
            except ValueError:
                return []
            return split_tokens + tokens[index + 1 :]
        if token.startswith("-S") and token != "-S":
            try:
                split_tokens = shlex.split(token[2:], posix=True)
            except ValueError:
                return []
            return split_tokens + tokens[index + 1 :]
        if not token.startswith("-") or token == "-":
            break

        option_name = token.split("=", 1)[0]
        if option_name in ENV_OPTIONS_WITH_VALUE and "=" not in token:
            index += 2
        else:
            index += 1
    return tokens[index:]


def consume_command_options(tokens):
    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return tokens[index + 1 :]
        if not token.startswith("-") or token == "-":
            break
        flags = token[1:]
        if "v" in flags or "V" in flags:
            return []
        if any(flag != "p" for flag in flags):
            return []
        index += 1
    return tokens[index:]


def strip_wrappers(tokens, inherited_assignments=None):
    remaining = list(tokens)
    assignments = dict(inherited_assignments or {})
    while remaining:
        if ASSIGNMENT.match(remaining[0]):
            name, value = remaining[0].split("=", 1)
            assignments[name] = value
            remaining = remaining[1:]
            continue

        executable = posixpath.basename(remaining[0]).lower()
        if executable == "sudo":
            remaining = consume_wrapper_options(remaining, SUDO_OPTIONS_WITH_VALUE)
            continue

        if executable == "env":
            remaining = consume_env_options(remaining)
            continue

        if executable == "command":
            remaining = consume_command_options(remaining)
            continue

        if executable == "exec":
            remaining = consume_wrapper_options(remaining, EXEC_OPTIONS_WITH_VALUE)
            continue

        if executable == "nohup":
            remaining = consume_wrapper_options(remaining, set())
            continue

        # To trust additional wrapper commands of your own (loggers,
        # launchers), add clauses here following the pattern above.

        if executable == "time":
            remaining = consume_wrapper_options(remaining, TIME_OPTIONS_WITH_VALUE)
            continue

        if executable == "nice":
            remaining = consume_wrapper_options(remaining, NICE_OPTIONS_WITH_VALUE)
            continue

        break
    return remaining, assignments


def expand_known_parameters(value, assignments):
    def replacement(match):
        name = match.group(1) or match.group(2)
        if name in assignments:
            return assignments[name]
        return os.environ.get(name, match.group(0))

    return SIMPLE_PARAMETER.sub(replacement, value)


def split_expanded_token(token, assignments):
    expanded = expand_known_parameters(token, assignments)
    if expanded == token or not re.search(r"\s", expanded):
        return [expanded]
    try:
        words = shlex.split(expanded, posix=True)
    except ValueError:
        return [expanded]
    return words or [""]


def prepare_tokens(tokens, inherited_assignments=None):
    remaining, assignments = strip_wrappers(tokens, inherited_assignments)
    if not remaining:
        return [], assignments

    command_words = split_expanded_token(remaining[0], assignments)
    remaining = command_words + remaining[1:]
    remaining, assignments = strip_wrappers(remaining, assignments)
    if not remaining:
        return [], assignments

    executable = posixpath.basename(remaining[0]).lower()
    preserve_argument_words = executable in SHELL_EXECUTABLES or executable == "eval"
    expanded = [remaining[0]]
    for token in remaining[1:]:
        if preserve_argument_words:
            expanded.append(expand_known_parameters(token, assignments))
        else:
            expanded.extend(split_expanded_token(token, assignments))
    return expanded, assignments


def normalized_target(target):
    expanded = os.path.expandvars(os.path.expanduser(target))
    normalized = posixpath.normpath(expanded)
    if normalized.startswith("//"):
        return "/" + normalized.lstrip("/")
    return normalized


def target_candidates(target):
    candidates = {target}
    without_parameters = BRACED_PARAMETER.sub("", target)
    candidates.add(SIMPLE_PARAMETER.sub("", without_parameters))

    for match in BRACED_DEFAULT.finditer(target):
        with_default = target[: match.start()] + match.group(1) + target[match.end() :]
        without_braces = BRACED_PARAMETER.sub("", with_default)
        candidates.add(SIMPLE_PARAMETER.sub("", without_braces))

    return candidates


def is_protected_rm_target(target):
    home = posixpath.normpath(os.path.expanduser("~"))
    protected = {"/", "/Users", "/System", home}

    # shlex preserves the leading dollar but not Bash ANSI-C quote markers.
    if target.startswith(("$/", "$\\")):
        return True
    if "$(" in target or "`" in target:
        return True

    for candidate in target_candidates(target):
        normalized = normalized_target(candidate)
        if normalized == "/*" or normalized in protected:
            return True
        if normalized.startswith("/") and any(
            fnmatch.fnmatchcase(path, normalized) for path in protected
        ):
            return True
        if normalized.startswith("/System/"):
            return True
        if any(
            normalized.startswith(root + "/")
            and GLOB_MAGIC.search(normalized[len(root) + 1 :])
            for root in ("/Users", "/System")
        ):
            return True
    return False


def self_test_denial(tokens):
    if tokens == ["destructive-guard-self-test"]:
        return SELF_TEST_REASON
    return None


def rm_denial(tokens, raw_segment=""):
    if not tokens or posixpath.basename(tokens[0]).lower() != "rm":
        return None

    recursive = False
    force = False
    targets = []
    parsing_options = True

    for token in tokens[1:]:
        if parsing_options and token == "--":
            parsing_options = False
            continue

        if parsing_options and token.startswith("--"):
            option = token.split("=", 1)[0]
            recursive = recursive or option == "--recursive"
            force = force or option == "--force"
            continue

        if parsing_options and token.startswith("-") and token != "-":
            flags = token[1:]
            recursive = recursive or "r" in flags or "R" in flags
            force = force or "f" in flags
            continue

        targets.append(token)

    if recursive and force:
        # Bash ANSI-C quoting is not decoded by shlex. Fail closed for the
        # entire quoting class only after this segment resolves to destructive rm.
        if "$'" in raw_segment:
            return RM_REASON
        if any(is_protected_rm_target(target) for target in targets):
            return RM_REASON
    return None


def diskutil_denial(tokens):
    if not tokens or posixpath.basename(tokens[0]).lower() != "diskutil":
        return None
    if len(tokens) > 1 and tokens[1].lower() in {
        "erasedisk",
        "erasevolume",
        "partitiondisk",
    }:
        return DISKUTIL_REASON
    return None


def mkfs_denial(tokens):
    if not tokens:
        return None
    executable = posixpath.basename(tokens[0]).lower()
    if executable == "mkfs" or executable.startswith("mkfs."):
        return MKFS_REASON
    return None


def nested_command(tokens):
    if not tokens:
        return None

    executable = posixpath.basename(tokens[0]).lower()
    if executable == "eval" and len(tokens) > 1:
        return " ".join(tokens[1:])
    if executable not in SHELL_EXECUTABLES:
        return None

    index = 1
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return None
        if token in SHELL_OPTIONS_WITH_VALUE:
            index += 2
            continue
        if any(token.startswith(option + "=") for option in SHELL_OPTIONS_WITH_VALUE):
            index += 1
            continue
        if not token.startswith("-") or token == "-":
            return None
        if not token.startswith("--") and "c" in token[1:]:
            return tokens[index + 1] if index + 1 < len(tokens) else None
        index += 1
    return None


def denial_reason(command, depth=0, inherited_assignments=None):
    active_assignments = dict(inherited_assignments or {})
    for segment in split_segments(command):
        try:
            tokens = shlex.split(segment, posix=True)
        except ValueError:
            continue

        tokens, segment_assignments = prepare_tokens(tokens, active_assignments)
        if not tokens:
            active_assignments = segment_assignments
            continue
        reason = rm_denial(tokens, segment)
        if reason:
            return reason
        for matcher in (self_test_denial, diskutil_denial, mkfs_denial):
            reason = matcher(tokens)
            if reason:
                return reason

        nested = nested_command(tokens)
        if nested is not None:
            if depth >= MAX_NESTED_COMMAND_DEPTH:
                return INSPECTION_LIMIT_REASON
            if SIMPLE_PARAMETER.search(nested) or "$(" in nested or "`" in nested:
                return DYNAMIC_COMMAND_REASON
            reason = denial_reason(nested, depth + 1, segment_assignments)
            if reason:
                return reason
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError, UnicodeError):
        return 0

    for command in command_strings(payload):
        reason = denial_reason(command)
        if reason:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
            json.dump(output, sys.stdout)
            sys.stdout.write("\n")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
