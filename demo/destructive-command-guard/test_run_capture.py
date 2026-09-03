#!/usr/bin/env python3
"""Harmless process-group lifecycle tests for the sterile capture harness."""

import importlib.util
import os
from pathlib import Path
import signal
import subprocess
import sys
import unittest


HARNESS = Path(__file__).with_name("run_capture.py")
spec = importlib.util.spec_from_file_location("run_capture", HARNESS)
run_capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_capture)


@unittest.skipUnless(hasattr(os, "killpg"), "process groups require POSIX")
class ProcessGroupCleanupTests(unittest.TestCase):
    def test_stop_process_group_stops_owned_descendant(self):
        child_program = "import time; time.sleep(60)"
        leader_program = (
            "import subprocess, sys; "
            "child = subprocess.Popen([sys.executable, '-c', sys.argv[1]], "
            "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, "
            "stderr=subprocess.DEVNULL); "
            "print(child.pid, flush=True)"
        )
        leader = subprocess.Popen(
            [sys.executable, "-c", leader_program, child_program],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        child_pid = None
        try:
            stdout, stderr = leader.communicate(timeout=5)
            self.assertEqual(leader.returncode, 0, stderr)
            child_pid = int(stdout.strip())
            self.assertEqual(os.getpgid(child_pid), leader.pid)
            self.assertNotEqual(leader.pid, os.getpgrp())

            run_capture.stop_process_group(leader.pid)

            with self.assertRaises(ProcessLookupError):
                os.killpg(leader.pid, 0)
        finally:
            if leader.poll() is None:
                leader.kill()
                leader.wait(timeout=5)
            if child_pid is not None:
                try:
                    group_id = os.getpgid(child_pid)
                except ProcessLookupError:
                    pass
                else:
                    if group_id == leader.pid and group_id != os.getpgrp():
                        os.killpg(group_id, signal.SIGKILL)


if __name__ == "__main__":
    unittest.main()
