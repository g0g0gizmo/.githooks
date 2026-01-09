"""
Tests for classify-commit-type-by-diff.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_classify_commit_type_by_diff_hook_exists():
    """classify-commit-type-by-diff.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../prepare-commit-msg/classify-commit-type-by-diff.hook")
    assert os.path.exists(path)


def test_classify_commit_type_by_diff_hook_executable():
    """classify-commit-type-by-diff.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../prepare-commit-msg/classify-commit-type-by-diff.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
