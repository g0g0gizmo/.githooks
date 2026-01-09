"""
Tests for search-term.hook shell script.
Verifies file existence and basic execution.
"""

import os
import subprocess
import sys

import pytest


def test_search_term_hook_exists():
    """search-term.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/search-term.hook")
    assert os.path.exists(path)


def test_search_term_hook_executable():
    """search-term.hook is executable as a shell script (skipped on Windows)."""
    if sys.platform.startswith("win"):
        pytest.skip("Shell execution test skipped on Windows")
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/search-term.hook")
    path = os.path.normpath(path)
    result = subprocess.run(["bash", path], capture_output=True)
    assert result.returncode == 0
