#!/usr/bin/env python3
"""Promote one authorized manifest through the existing canonical checker.

Default: read-only preparation. --write changes only current-skills.json.
--verify-published COMMIT checks the later publication without writing a pin.
The authorization digest is an externally supplied trust input, not an approval
created or authenticated by this tool. No command commits, pushes or installs.
"""
import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import types

OWNER = "Ezra144israel/governed-agent-skills"
AUTH_SCHEMA = "canonical-skill-release-authorization/v1"
MANIFEST = "current-skills.json"


class PromotionError(ValueError):
    pass


def load_checker(path, expected):
    # Execute the measured bytes, never an import cache or a neighboring module.
    path = Path(path).expanduser()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
        raise PromotionError("CHECKER_UNAVAILABLE")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise PromotionError("CHECKER_IDENTITY_MISMATCH")
    module = types.ModuleType("canonical_skillsync")
    module.__file__ = str(path)
    exec(compile(data, str(path), "exec"), module.__dict__)
    module.source_path_allowed(path)
    module.source_path_allowed(path.resolve())
    return module, module.identity(data)


def read_input(checker, path):
    path = Path(path).expanduser()
    checker.source_path_allowed(path)
    checker.source_path_allowed(path.resolve())
    return checker.regular_bytes(path.parent, path.name)


def authorization(checker, path, expected_sha, checker_identity):
    raw = read_input(checker, path)
    checker.require_identity(raw, {"bytes": len(raw), "sha256": expected_sha}, "authorization")
    auth = checker.parse_json(raw)
    if not isinstance(auth, dict) or auth.get("schema") != AUTH_SCHEMA or auth.get("repository") != OWNER:
        raise PromotionError("INVALID_AUTHORIZATION_SCHEMA")
    if not checker.HEX40.fullmatch(str(auth.get("base_commit", ""))):
        raise PromotionError("INVALID_AUTHORIZATION_BASE")
    candidate = auth.get("candidate", {})
    if (not isinstance(candidate, dict) or type(candidate.get("bytes")) is not int
            or not 0 < candidate["bytes"] <= checker.MAX_MEMBER
            or not checker.HEX64.fullmatch(str(candidate.get("sha256", "")))
            or not isinstance(candidate.get("revision"), str) or not candidate["revision"]):
        raise PromotionError("INVALID_AUTHORIZATION_CANDIDATE")
    if auth.get("checker") != checker_identity:
        raise PromotionError("AUTHORIZATION_CHECKER_MISMATCH")
    for name, state, prefix in (("accepted_review", "ACCEPTED", "relay/returns/"),
                                 ("release_authorization", "AUTHORIZED", "relay/")):
        record = auth.get(name)
        if (not isinstance(record, dict) or record.get("status") != state
                or record.get("repository") != "Ezra144israel/operator-agent-relay"
                or not str(record.get("path", "")).startswith(prefix)
                or not checker.HEX40.fullmatch(str(record.get("blob", "")))):
            raise PromotionError("MISSING_OR_INVALID_AUTHORIZATION " + name)
        checker.relative_path(record["path"])
        if "skill-versions" in record["path"].split("/"):
            raise PromotionError("HISTORICAL_AUTHORIZATION_PATH")
    if auth["release_authorization"].get("action") != "PROMOTE_FOR_PUBLICATION":
        raise PromotionError("MISSING_RELEASE_AUTHORIZATION")
    return auth, checker.identity(raw)


def git(checker, root, *args):
    return checker.git_output(root, *args).decode().strip()


def remote_matches(checker, root, owner, expected):
    checker.source_path_allowed(root)
    checker.source_path_allowed(Path(root).resolve())
    remote = git(checker, root, "remote", "get-url", "origin")
    if remote not in (f"https://github.com/{owner}", f"https://github.com/{owner}.git",
                      f"git@github.com:{owner}.git", f"ssh://git@github.com/{owner}.git"):
        raise PromotionError("SOURCE_OWNER_MISMATCH " + owner)
    observed = git(checker, root, "ls-remote", "--exit-code", "origin", "refs/heads/main")
    if observed != expected + "\trefs/heads/main":
        raise PromotionError(f"REMOTE_DRIFT {owner} expected={expected} observed={observed}")


def sources(checker, manifest, roots, own_commit):
    expected = {OWNER: own_commit}
    for row in manifest.skills.values():
        if row["lifecycle"] != "CURRENT":
            continue
        source = row["source"]
        owner, commit = source["repository"], source["commit"]
        if owner == OWNER:
            if commit != "MANIFEST":
                raise PromotionError("OWN_SOURCE_MUST_BIND_MANIFEST_COMMIT")
        elif not checker.HEX40.fullmatch(str(commit)):
            raise PromotionError("EXTERNAL_SOURCE_NOT_PUBLISHED " + owner)
        elif owner in expected and expected[owner] != commit:
            raise PromotionError("CONFLICTING_SOURCE_COMMITS " + owner)
        else:
            expected[owner] = commit
    if set(roots) != set(expected):
        raise PromotionError("SOURCE_ROOT_SET_MISMATCH")
    for owner, commit in expected.items():
        remote_matches(checker, roots[owner], owner, commit)
    # Resolve all current members, even if every hosted target is BLOCKED.
    for name, row in manifest.skills.items():
        if row["lifecycle"] != "CURRENT":
            continue
        members = checker.source_members(manifest, name, roots)
        for surface, target in row["targets"].items():
            if target["adaptation"] not in ("BLOCKED", "NOT_TARGET"):
                checker.adapt(row, surface, members)
    return expected


def standing(root, require_current=False):
    command = ["node", "tools/check-standing-distribution.mjs"]
    if require_current:
        command.append("--require-current")
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise PromotionError("STANDING_CHECK_FAILED " + (result.stderr or result.stdout).strip())


def prepare(checker, root, roots, auth, raw, published=None):
    document = checker.parse_json(raw)
    if not isinstance(document, dict):
        raise PromotionError("INVALID_MANIFEST")
    if not published and document.get("status") == "CURRENT":
        raise PromotionError("ALREADY_PROMOTED")
    if document.get("status") != ("CURRENT" if published else "CANDIDATE"):
        raise PromotionError("WRONG_MANIFEST_STATE")
    candidate = copy.deepcopy(document)
    candidate["status"] = "CANDIDATE"
    candidate_bytes = checker.json_bytes(candidate) if published else raw
    checker.require_identity(candidate_bytes, auth["candidate"], "accepted candidate")
    if checker.json_bytes(candidate) != candidate_bytes:
        raise PromotionError("NON_CANONICAL_CANDIDATE_ENCODING")
    manifest = checker.Manifest(candidate_bytes, auth["candidate"], candidate=True)
    if manifest.repository != OWNER or manifest.revision != auth["candidate"]["revision"]:
        raise PromotionError("AUTHORIZATION_SUBJECT_MISMATCH")
    released = copy.deepcopy(candidate)
    released["status"] = "CURRENT"
    release_bytes = checker.json_bytes(released)
    commit = published or auth["base_commit"]
    release = checker.Manifest(release_bytes, {**checker.identity(release_bytes), "commit": commit})
    if published:
        checker.require_identity(raw, checker.identity(release_bytes), "published release")
        parents = git(checker, root, "rev-list", "--parents", "-n", "1", published).split()
        if parents != [published, auth["base_commit"]]:
            raise PromotionError("PUBLICATION_PARENT_MISMATCH")
    elif git(checker, root, "rev-parse", "HEAD") != auth["base_commit"]:
        raise PromotionError("BASE_DRIFT")
    roots_used = sources(checker, release if published else manifest, roots, commit)
    standing(root, require_current=bool(published))
    return release_bytes, roots_used


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--checker", required=True, help="Explicit accepted S8 skillsync source file")
    parser.add_argument("--checker-sha256", required=True)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--authorization-sha256", required=True)
    parser.add_argument("--source-root", action="append", default=[], metavar="OWNER=PATH")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify-published", metavar="COMMIT")
    args = parser.parse_args(argv)
    try:
        checker, checker_id = load_checker(args.checker, args.checker_sha256)
        auth, auth_id = authorization(checker, args.authorization, args.authorization_sha256, checker_id)
        root = Path(args.root).expanduser()
        checker.source_path_allowed(root)
        checker.source_path_allowed(root.resolve())
        roots = {}
        for option in args.source_root:
            owner, separator, path = option.partition("=")
            if not separator or not path or owner in roots:
                raise PromotionError("INVALID_OR_DUPLICATE_SOURCE_ROOT")
            roots[owner] = str(Path(path).expanduser())
        if OWNER not in roots or Path(roots[OWNER]).resolve() != root.resolve():
            raise PromotionError("OWN_SOURCE_ROOT_MISMATCH")
        if args.verify_published:
            if not checker.HEX40.fullmatch(args.verify_published):
                raise PromotionError("INVALID_PUBLICATION_COMMIT")
            raw = checker.git_output(root, "show", args.verify_published + ":" + MANIFEST)
            release, source_heads = prepare(checker, root, roots, auth, raw, args.verify_published)
            state = "PUBLISHED_CURRENT"
        else:
            path = root / MANIFEST
            raw = read_input(checker, path)
            release, source_heads = prepare(checker, root, roots, auth, raw)
            state = "PREPARED_READ_ONLY"
            if args.write:
                # Lock the original inode, then recheck every gate before replacement.
                with path.open("rb") as lock:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    if read_input(checker, path) != raw:
                        raise PromotionError("CANDIDATE_CHANGED_BEFORE_WRITE")
                    prepare(checker, root, roots, auth, raw)
                    fd, temporary = tempfile.mkstemp(prefix=".current-skills-", dir=root)
                    try:
                        with os.fdopen(fd, "wb") as stream:
                            os.fchmod(stream.fileno(), stat.S_IMODE(path.stat().st_mode))
                            stream.write(release)
                            stream.flush()
                            os.fsync(stream.fileno())
                        if read_input(checker, path) != raw:
                            raise PromotionError("CANDIDATE_CHANGED_BEFORE_WRITE")
                        os.replace(temporary, path)
                    finally:
                        if os.path.exists(temporary):
                            os.unlink(temporary)
                    checker.require_identity(read_input(checker, path), checker.identity(release), "release readback")
                state = "PROMOTED_UNPUBLISHED"
        receipt = {"status": state, "candidate": auth["candidate"], "release": checker.identity(release),
                   "authorization": auth_id, "checker": checker_id, "base_commit": auth["base_commit"],
                   "source_heads": source_heads, "revision": auth["candidate"]["revision"],
                   "commit_binding": "MANIFEST resolves to the verified publication commit supplied by the release pin"}
        if args.verify_published:
            receipt["commit"] = args.verify_published
        print(checker.json_bytes(receipt).decode(), end="")
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, subprocess.TimeoutExpired) as exc:
        print("PUBLICATION_BLOCKED | " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
