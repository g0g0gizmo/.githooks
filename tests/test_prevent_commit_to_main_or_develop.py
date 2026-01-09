"""
Tests for prevent-commit-to-main-or-develop.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_prevent_commit_to_main_or_develop_hook_exists():
    """prevent-commit-to-main-or-develop.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/prevent-commit-to-main-or-develop.hook")
    assert os.path.exists(path)


def test_prevent_commit_to_main_or_develop_hook_executable():
    """prevent-commit-to-main-or-develop.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/prevent-commit-to-main-or-develop.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
