"""
Tests for delete-pyc-files.hook.

Verifies existence and execution of the delete-pyc-files.hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../post-checkout/delete-pyc-files.hook")).replace("\\", "/")
HOOK_PATH_DISABLED = HOOK_PATH + ".disabled"


def test_hook_exists():
    """Hook script should exist in post-checkout directory."""
    if os.path.isfile(HOOK_PATH_DISABLED):
        pytest.skip(f"Hook is disabled ({HOOK_PATH_DISABLED})")
    assert os.path.isfile(HOOK_PATH)


def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1)."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    result = subprocess.run(["bash", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)
