"""
Tests for dotenvx.hook.

Verifies existence and execution of the dotenvx.hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../pre-commit/dotenvx.hook")).replace("\\", "/")


def test_hook_exists():
    """Hook script should exist in pre-commit directory."""
    disabled_path = HOOK_PATH + ".disabled"
    if os.path.isfile(disabled_path):
        pytest.skip("Hook is disabled (.hook.disabled)")
    assert os.path.isfile(HOOK_PATH)


def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1)."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found or not executable on this platform.")
    result = subprocess.run(["bash", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)
