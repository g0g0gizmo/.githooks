"""
Tests for post-commit/autoversion-conventional-commit.hook.

Verifies importability of the autoversion-conventional-commit.hook Python script.
"""

import os

import pytest

from tests.conftest import load_hook_module

HOOK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../post-commit/autoversion-conventional-commit.hook")).replace("\\", "/")


def test_hook_exists():
    """Hook script should exist in post-commit directory."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    assert os.path.isfile(HOOK_PATH)


def test_hook_importable(load_hook_module):
    """Hook script should be importable as a Python module (if Python)."""
    disabled_path = HOOK_PATH + ".disabled"
    if not os.path.isfile(HOOK_PATH) and os.path.isfile(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    if not os.path.isfile(HOOK_PATH):
        pytest.skip(f"Hook not found: {HOOK_PATH}")

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
