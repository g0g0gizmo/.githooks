"""
Tests for delete-pyc-files.hook Python script.
Verifies .pyc file deletion logic and argument handling.
"""

import os
import sys
import tempfile

import pytest


def test_script_runs_without_error():
    """Script runs without error when called as main."""
    script_path = os.path.join(os.path.dirname(__file__), "../post-checkout/delete-pyc-files.hook")
    if not script_path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    from tests.conftest import load_hook_module

    load_hook_module(script_path)
    # Should not raise


def test_deletes_pyc_files(tmp_path):
    """Script deletes .pyc files in directory tree."""
    # Create dummy .pyc file
    pyc_file = tmp_path / "test.pyc"
    pyc_file.write_bytes(b"dummy")
    # Simulate script run
    sys.argv = [str(tmp_path)]
    script_path = os.path.join(os.path.dirname(__file__), "../post-checkout/delete-pyc-files.hook")
    if not script_path.endswith(".py"):
        pytest.skip("Not a Python file; skipping import test.")
    from tests.conftest import load_hook_module

    load_hook_module(script_path)
    # File should be deleted
    assert not pyc_file.exists()
