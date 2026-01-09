"""
Tests for autoversion-conventional-commit.hook script.
Verifies script presence and importability.
"""

import os

import pytest


def test_autoversion_hook_exists():
    """autoversion-conventional-commit.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../post-commit/autoversion-conventional-commit.hook")
    disabled_path = path + ".disabled"
    if not os.path.exists(path) and os.path.exists(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    assert os.path.exists(path)


def test_autoversion_hook_importable():
    """autoversion-conventional-commit.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../post-commit/autoversion-conventional-commit.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    load_hook_module = pytest.fixture()(lambda: __import__("tests.conftest").load_hook_module)

    module = load_hook_module(path)
    # Should not raise
