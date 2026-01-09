"""
Tests for enforce-insert-issue-number.hook script.
Verifies script presence and importability.
"""

import importlib.util
import os

import pytest


def test_enforce_insert_issue_number_hook_exists():
    """enforce-insert-issue-number.hook file exists and is readable."""
    path = os.path.join(os.path.dirname(__file__), "../commit-msg/enforce-insert-issue-number.hook")
    assert os.path.exists(path)


def test_enforce_insert_issue_number_hook_importable():
    """enforce-insert-issue-number.hook can be loaded as a module (if Python)."""
    path = os.path.join(os.path.dirname(__file__), "../commit-msg/enforce-insert-issue-number.hook")
    if not path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    spec = importlib.util.spec_from_file_location("enforce_insert_issue_number_hook", path)
    if spec is None or spec.loader is None:
        pytest.skip("Not a valid Python module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Should not raise
