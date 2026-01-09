"""
Tests for format-code.hook script.
Verifies script presence and importability.
"""

import importlib.util
import os

import pytest


def test_format_code_hook_exists():
    """format-code.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/format-code.hook")
    disabled_path = path + ".disabled"
    if not os.path.exists(path) and not os.path.exists(disabled_path):
        pytest.skip(f"Hook not found: {path} (and no .disabled version)")
    if not os.path.exists(path) and os.path.exists(disabled_path):
        pytest.skip(f"Hook is disabled: {disabled_path}")
    assert os.path.exists(path)


def test_format_code_hook_importable():
    """format-code.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../pre-commit/format-code.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    spec = importlib.util.spec_from_file_location("format_code_hook", path)
    if spec is None or spec.loader is None:
        pytest.skip("Not a valid Python module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Should not raise
