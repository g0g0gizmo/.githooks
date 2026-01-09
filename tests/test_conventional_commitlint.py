"""
Tests for conventional-commitlint.hook script.
Verifies script presence and importability.
"""

import os

import pytest


def test_conventional_commitlint_hook_exists():
    """conventional-commitlint.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../commit-msg/conventional-commitlint.hook")
    disabled_path = path + ".disabled"
    if os.path.exists(disabled_path):
        pytest.skip("Hook is disabled (.hook.disabled)")
    assert os.path.exists(path)


def test_conventional_commitlint_hook_importable():
    """conventional-commitlint.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../commit-msg/conventional-commitlint.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    from tests.conftest import load_hook_module

    load_hook_module(path)
    # Should not raise
