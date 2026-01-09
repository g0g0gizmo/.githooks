"""
Tests for prevent-bad-push.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_prevent_bad_push_hook_exists():
    """prevent-bad-push.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-push/prevent-bad-push.hook")
    assert os.path.exists(path)


def test_prevent_bad_push_hook_executable():
    """prevent-bad-push.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-push/prevent-bad-push.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
