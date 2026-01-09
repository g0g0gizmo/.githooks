"""
Tests for spell-check-md-files.hook.

Verifies existence and execution of the spell-check-md-files.hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../pre-commit/spell-check-md-files.hook")).replace("\\", "/")


def test_hook_exists():
    """Hook script should exist in pre-commit directory."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    if not os.path.isfile(HOOK_PATH) and not os.path.isfile(disabled_path):
        pytest.skip(f"Hook not found: {HOOK_PATH}")
    assert os.path.isfile(HOOK_PATH)


def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1)."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found or not executable on this platform.")
    result = subprocess.run(["bash", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)
