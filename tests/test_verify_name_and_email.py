"""
Tests for verify-name-and-email.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_verify_name_and_email_hook_exists():
    """verify-name-and-email.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/verify-name-and-email.hook")
    assert os.path.exists(path)


def test_verify_name_and_email_hook_executable():
    """verify-name-and-email.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/verify-name-and-email.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
