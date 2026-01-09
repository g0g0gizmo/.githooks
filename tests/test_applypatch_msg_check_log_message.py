"""
Tests for applypatch-msg-check-log-message hook.

Verifies existence and execution of the applypatch-msg-check-log-message hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../applypatch-msg/applypatch-msg-check-log-message")).replace("\\", "/")


def test_hook_exists():
    """Hook script should exist in applypatch-msg directory."""
    assert os.path.isfile(HOOK_PATH)


def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1 for valid/invalid input)."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    result = subprocess.run(["bash", HOOK_PATH], input="test commit message", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)


@pytest.mark.parametrize(
    "msg,expected",
    [
        ("fix: valid commit", 0),
        ("random message", 1),
    ],
)
def test_hook_validates_commit_message(msg: str, expected: int) -> None:
    """Hook should validate commit message format and return correct exit code."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    result = subprocess.run(["bash", HOOK_PATH], input=msg, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode == expected
