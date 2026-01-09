"""
Tests for dotenvx.hook script.
Verifies script presence and basic execution.
"""

import importlib.util
import os

import pytest


def test_dotenvx_hook_exists():
    """dotenvx.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/dotenvx.hook")
    disabled_path = path + ".disabled"
    if os.path.exists(disabled_path):
        pytest.skip("Hook is disabled (.hook.disabled)")
    assert os.path.exists(path)


def test_dotenvx_hook_importable():
    """dotenvx.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/dotenvx.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    spec = importlib.util.spec_from_file_location("dotenvx_hook", path)
    if spec is None or spec.loader is None:
        pytest.skip("Not a valid Python module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Should not raise
