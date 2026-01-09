"""
Error handling tests for post-commit/autoversion-conventional-commit.hook.

Verifies that the hook exits with error on invalid input.
"""

import os
import subprocess

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../post-commit/autoversion-conventional-commit.hook")).replace("\\", "/")


def test_hook_missing_git():
    """Should exit with error if git is not available (simulate by running in empty env)."""
    import sys

    import pytest

    if sys.platform.startswith("win"):
        pytest.skip("python3 not available on Windows; skipping test.")
    env = os.environ.copy()
    env["PATH"] = ""  # Remove all paths
    try:
        result = subprocess.run(["python3", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    except FileNotFoundError:
        pytest.skip("python3 not found; skipping test.")
    assert result.returncode != 0
    assert b"Error" in result.stdout or b"Error" in result.stderr
