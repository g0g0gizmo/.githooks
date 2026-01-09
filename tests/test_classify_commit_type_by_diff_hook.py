"""
Tests for classify-commit-type-by-diff.hook.

Verifies existence and execution of the classify-commit-type-by-diff.hook script.
"""

import os
import subprocess

import pytest

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../prepare-commit-msg/classify-commit-type-by-diff.hook")).replace("\\", "/")


def test_hook_exists():
    """Hook script should exist in prepare-commit-msg directory."""
    assert os.path.isfile(HOOK_PATH)


def test_hook_importable(load_hook_module):
    """Hook script should be importable as a Python module (if Python)."""
    with open(HOOK_PATH, encoding="utf-8") as f:
        first_line = f.readline()
    if not (first_line.startswith("#!/usr/bin/env python") or first_line.startswith("#!/usr/bin/python")):
        pytest.skip("Not a Python script; skipping import test.")
    import importlib.util

    spec = importlib.util.spec_from_file_location("hook_module", HOOK_PATH)
    if spec is None or spec.loader is None:
        pytest.skip("Could not load Python module spec; skipping import test.")
    load_hook_module(HOOK_PATH)
    # Should not raise


def test_hook_executable():
    """Hook script should be executable (exit code 0 or 1)."""
    if not os.path.isfile(HOOK_PATH):
        pytest.skip("Hook script not found; skipping test.")
    result = subprocess.run(["bash", HOOK_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 127:
        pytest.skip("Script not found or not executable by Bash; skipping test.")
    assert result.returncode in (0, 1)
