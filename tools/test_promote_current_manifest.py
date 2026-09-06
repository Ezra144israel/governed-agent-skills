"""Promotion at the real CLI/file/Git seam; remote transport is fixture-local."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = Path(os.environ.get("SKILLSYNC_TEST_CHECKER", ""))
CHECKER_SHA256 = "e7c5d0cc74a167b917279394841e7e573ab672a17de3c7a528ecadb3e82c480c"
OWNER = "Ezra144israel/governed-agent-skills"


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


class PromotionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CHECKER.is_file():
            raise RuntimeError("Set SKILLSYNC_TEST_CHECKER to the accepted S8 skillsync source file")
        if identity(CHECKER.read_bytes())["sha256"] != CHECKER_SHA256:
            raise RuntimeError("SKILLSYNC_TEST_CHECKER identity differs from the tested dependency")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cv-release-test-")
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.repo = self.home / "source"
        self.repo.mkdir()
        self.git = shutil.which("git")
        self.env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                    "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        self.run_git("init", "-q")
        self.run_git("remote", "add", "origin", f"https://github.com/{OWNER}.git")
        self.run_git("-c", "core.hooksPath=/dev/null", "commit", "--allow-empty", "-qm", "fixture base")
        self.base = self.run_git("rev-parse", "HEAD").strip()
        self.remote = self.home / "remote-main"
        self.remote.write_text(self.base)
        # Only ls-remote is substituted. All local Git commands run real Git.
        bin_dir = self.home / "bin"
        bin_dir.mkdir()
        shim = bin_dir / "git"
        shim.write_text("#!" + sys.executable + "\nimport os,sys\nfrom pathlib import Path\n"
                        "if 'ls-remote' in sys.argv:\n"
                        " print(Path(os.environ['FIXTURE_REMOTE']).read_text().strip() + '\\trefs/heads/main')\n"
                        "else: os.execv(os.environ['FIXTURE_GIT'], [os.environ['FIXTURE_GIT'], *sys.argv[1:]])\n")
        shim.chmod(0o755)
        self.env.update({"PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", ""),
                         "FIXTURE_REMOTE": str(self.remote), "FIXTURE_GIT": self.git})
        (self.repo / "tools").mkdir()
        shutil.copy2(ROOT / "tools/check-standing-distribution.mjs", self.repo / "tools/check-standing-distribution.mjs")
        (self.repo / "STANDING-SOURCE-AND-ADAPTER-CONTRACT.md").write_text(
            "## Distribution table\n| `example` | release | codex | no |\n"
            "## Retired: must not regrow\n"
            "## Register owner: `pending-convergence` has no skill source home\nrelay/convergence/\n")
        self.skill = self.repo / "skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_bytes(b"---\nname: example\ndescription: fixture\n---\n\n# Example\nAccepted behavior.\n")
        self.ref = self.skill.parent / "reference.md"
        self.ref.write_bytes(b"Accepted reference.\n")
        self.document = {"schema": "canonical-current-skills/v1", "repository": OWNER,
            "revision": "fixture-v1", "status": "CANDIDATE", "surfaces": ["codex"],
            "skills": [{"name": "example", "lifecycle": "CURRENT", "source": {
                "repository": OWNER, "path": "skills/example", "commit": "MANIFEST",
                "members": [{"path": p.name, **identity(p.read_bytes())} for p in (self.skill, self.ref)]},
                "targets": {"codex": {"adaptation": "release"}}}]}
        self.manifest = self.repo / "current-skills.json"
        self.manifest.write_bytes(encode(self.document))
        self.auth = self.home / "authorization.json"
        self.authorization = {"schema": "canonical-skill-release-authorization/v1", "repository": OWNER,
            "base_commit": self.base, "candidate": {**identity(self.manifest.read_bytes()), "revision": "fixture-v1"},
            "checker": identity(CHECKER.read_bytes()),
            "accepted_review": {"status": "ACCEPTED", "repository": "Ezra144israel/operator-agent-relay",
                                "path": "relay/returns/fixture-review.md", "blob": "a" * 40},
            "release_authorization": {"status": "AUTHORIZED", "action": "PROMOTE_FOR_PUBLICATION",
                "repository": "Ezra144israel/operator-agent-relay", "path": "relay/dispatches/fixture-release.md", "blob": "b" * 40}}
        self.write_auth()

    def run_git(self, *args):
        return subprocess.check_output([self.git, "-C", str(self.repo), *args], env=self.env, text=True)

    def write_auth(self):
        self.auth.write_bytes(encode(self.authorization))

    def accept_manifest(self):
        self.manifest.write_bytes(encode(self.document))
        self.authorization["candidate"].update(identity(self.manifest.read_bytes()))
        self.write_auth()

    def invoke(self, *args, authorization=True):
        command = [sys.executable, str(ROOT / "tools/promote-current-manifest.py"),
                   "--root", str(self.repo), "--checker", str(CHECKER),
                   "--checker-sha256", identity(CHECKER.read_bytes())["sha256"],
                   "--source-root", OWNER + "=" + str(self.repo)]
        if authorization:
            command += ["--authorization", str(self.auth), "--authorization-sha256", identity(self.auth.read_bytes())["sha256"]]
        return subprocess.run(command + list(args), env=self.env, capture_output=True, text=True)

    def assert_refused(self, fragment, *args):
        before = self.manifest.read_bytes()
        result = self.invoke("--write", *args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(fragment, result.stderr)
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_reviewed_candidate_promotes_only_status_and_preserves_skill_bytes(self):
        skills = {p: p.read_bytes() for p in (self.skill, self.ref)}
        result = self.invoke("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        released = json.loads(self.manifest.read_bytes())
        self.assertEqual(released, {**self.document, "status": "CURRENT"})
        self.assertEqual({p: p.read_bytes() for p in skills}, skills)
        self.assertEqual(json.loads(result.stdout)["status"], "PROMOTED_UNPUBLISHED")
        checked = subprocess.run(["node", "tools/check-standing-distribution.mjs", "--require-current"],
                                 cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_dry_run_is_deterministic_and_writes_nothing(self):
        before = self.manifest.read_bytes()
        one, two = self.invoke(), self.invoke()
        self.assertEqual(one.returncode, 0, one.stderr)
        self.assertEqual(one.stdout, two.stdout)
        self.assertEqual(json.loads(one.stdout)["status"], "PREPARED_READ_ONLY")
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_unreviewed_or_unauthorized_subject_cannot_promote(self):
        self.assertNotEqual(self.invoke("--write", authorization=False).returncode, 0)
        for section, value in (("accepted_review", "NEEDS_REVISION"), ("release_authorization", "CANDIDATE")):
            with self.subTest(section=section):
                saved = self.authorization[section]["status"]
                self.authorization[section]["status"] = value
                self.write_auth()
                self.assert_refused("AUTHORIZATION")
                self.authorization[section]["status"] = saved
        self.write_auth()

    def test_changed_root_or_reference_is_refused(self):
        for path in (self.skill, self.ref):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before + b"Drift.\n")
                self.assert_refused("IDENTITY_MISMATCH")
                path.write_bytes(before)

    def test_changed_candidate_identity_is_refused(self):
        self.document["revision"] = "unreviewed"
        self.manifest.write_bytes(encode(self.document))
        self.assert_refused("IDENTITY_MISMATCH")

    def test_duplicate_owner_and_forbidden_source_fail_existing_checker(self):
        self.document["skills"].append(self.document["skills"][0])
        self.accept_manifest()
        self.assert_refused("DUPLICATE_CURRENT_IDENTITY")
        self.document["skills"].pop()
        self.document["skills"][0]["source"]["path"] = "Downloads/example"
        self.accept_manifest()
        self.assert_refused("FORBIDDEN_SOURCE_LOCATION")

    def test_remote_and_local_base_drift_are_refused(self):
        self.remote.write_text("f" * 40)
        self.assert_refused("REMOTE_DRIFT")
        self.remote.write_text(self.base)
        self.authorization["base_commit"] = "f" * 40
        self.write_auth()
        self.assert_refused("BASE_DRIFT")

    def test_stale_authorization_and_checker_pins_are_refused(self):
        self.assert_refused("IDENTITY_MISMATCH", "--authorization-sha256", "0" * 64)
        self.assert_refused("CHECKER_IDENTITY_MISMATCH", "--checker-sha256", "0" * 64)

    def test_source_root_owner_mismatch_is_refused(self):
        self.run_git("remote", "set-url", "origin", "https://github.com/fixture/wrong.git")
        self.assert_refused("SOURCE_OWNER_MISMATCH")

    def test_malformed_json_is_refused_without_write(self):
        self.manifest.write_bytes(b'{"status":')
        self.authorization["candidate"].update(identity(self.manifest.read_bytes()))
        self.write_auth()
        self.assert_refused("INVALID_JSON")

    def test_repeated_write_refuses_cleanly(self):
        result = self.invoke("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_refused("ALREADY_PROMOTED")

    def test_candidate_fails_current_distribution_gate(self):
        result = subprocess.run(["node", "tools/check-standing-distribution.mjs", "--require-current"],
                                cwd=self.repo, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a current release", result.stderr)

    def test_release_binds_eventual_commit_and_remote_without_self_reference(self):
        result = self.invoke("--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        release = self.manifest.read_bytes()
        self.run_git("add", "current-skills.json", "skills", "tools", "STANDING-SOURCE-AND-ADAPTER-CONTRACT.md")
        self.run_git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "fixture publication")
        commit = self.run_git("rev-parse", "HEAD").strip()
        self.remote.write_text(commit)
        result = self.invoke("--verify-published", commit)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "PUBLISHED_CURRENT")
        self.assertEqual(receipt["commit"], commit)
        self.assertEqual(receipt["release"], identity(release))
        self.assertEqual(self.manifest.read_bytes(), release)
        self.assertNotIn(commit.encode(), release)
        self.remote.write_text(self.base)
        result = self.invoke("--verify-published", commit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REMOTE_DRIFT", result.stderr)


if __name__ == "__main__":
    unittest.main()
