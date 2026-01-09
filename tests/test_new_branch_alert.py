"""
Tests for new-branch-alert.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_new_branch_alert_hook_exists():
    """new-branch-alert.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../post-checkout/new-branch-alert.hook")
    path_disabled = path + ".disabled"
    if os.path.exists(path_disabled):
        pytest.skip(f"Hook is disabled ({path_disabled})")
    assert os.path.exists(path)


def test_new_branch_alert_hook_executable():
    """new-branch-alert.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../post-checkout/new-branch-alert.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
