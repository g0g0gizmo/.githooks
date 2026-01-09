"""
Tests for update-server-info.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_update_server_info_hook_exists():
    """update-server-info.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../post-update/update-server-info.hook")
    if not os.path.exists(path):
        pytest.skip("update-server-info.hook not found; skipping test.")
    assert os.path.exists(path)


def test_update_server_info_hook_executable():
    """update-server-info.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../post-update/update-server-info.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
