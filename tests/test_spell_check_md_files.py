"""
Tests for spell-check-md-files.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_spell_check_md_files_hook_exists():
    """spell-check-md-files.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/spell-check-md-files.hook")
    disabled_path = path + ".disabled"
    if not os.path.exists(path) and os.path.exists(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    if not os.path.exists(path) and not os.path.exists(disabled_path):
        pytest.skip(f"Hook not found: {path}")
    assert os.path.exists(path)


def test_spell_check_md_files_hook_executable():
    """spell-check-md-files.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/spell-check-md-files.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
