"""
Test for cyclic import edge cases after refactoring to githooks/.
Ensures importing githooks modules and dependent modules does not cause ImportError or recursion errors.
"""

import importlib
import sys

import pytest


def test_utils_import_no_cyclic_error():
    """Importing githooks.core.utils should not cause ImportError or RecursionError."""
    try:
        importlib.import_module("githooks.core.utils")
    except (ImportError, RecursionError) as e:
        pytest.fail(f"Cyclic import or recursion error: {e}")


def test_finish_import_no_cyclic_error():
    """Importing githooks.cli.finish should not cause ImportError or RecursionError."""
    try:
        importlib.import_module("githooks.cli.finish")
    except (ImportError, RecursionError) as e:
        pytest.fail(f"Cyclic import or recursion error: {e}")


def test_github_utils_import_no_cyclic_error():
    """Importing githooks.core.github_utils should not cause ImportError or RecursionError."""
    try:
        importlib.import_module("githooks.core.github_utils")
    except (ImportError, RecursionError) as e:
        pytest.fail(f"Cyclic import or recursion error: {e}")


def test_jira_helpers_import_no_cyclic_error():
    """Importing githooks.core.jira_helpers should not cause ImportError or RecursionError."""
    try:
        importlib.import_module("githooks.core.jira_helpers")
    except (ImportError, RecursionError) as e:
        pytest.fail(f"Cyclic import or recursion error: {e}")


def test_repo_helpers_import_no_cyclic_error():
    """Importing githooks.core.repo_helpers should not cause ImportError or RecursionError."""
    try:
        importlib.import_module("githooks.core.repo_helpers")
    except (ImportError, RecursionError) as e:
        pytest.fail(f"Cyclic import or recursion error: {e}")
