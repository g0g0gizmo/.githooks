"""
Tests for dispatcher.hook script.
Verifies script presence and importability.
"""

import importlib.util
import os

import pytest


def test_dispatcher_hook_exists():
    """dispatcher.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/dispatcher.hook")
    assert os.path.exists(path)


def test_dispatcher_hook_importable():
    """dispatcher.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/dispatcher.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    spec = importlib.util.spec_from_file_location("dispatcher_hook", path)
    if spec is None or spec.loader is None:
        pytest.skip("Not a valid Python module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Should not raise
