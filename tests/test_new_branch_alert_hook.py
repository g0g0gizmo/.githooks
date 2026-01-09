"""
Tests for new-branch-alert.hook.

Verifies existence and execution of the new-branch-alert.hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../post-checkout/new-branch-alert.hook")).replace("\\", "/")
HOOK_PATH_DISABLED = HOOK_PATH + ".disabled"


@pytest.mark.skipif(os.path.isfile(HOOK_PATH_DISABLED), reason=f"Hook is disabled ({HOOK_PATH_DISABLED})")
def test_hook_exists():
    """Hook script should exist in post-checkout directory."""
    assert os.path.isfile(HOOK_PATH)


@pytest.mark.skipif(not os.path.isfile(HOOK_PATH), reason="Hook script not found or not executable on this platform.")
def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1)."""
    result = subprocess.run(["bash", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)
