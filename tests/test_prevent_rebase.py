"""
Tests for prevent-rebase.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_prevent_rebase_hook_exists():
    """prevent-rebase.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-rebase/prevent-rebase.hook")
    assert os.path.exists(path)


def test_prevent_rebase_hook_executable():
    """prevent-rebase.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-rebase/prevent-rebase.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
