"""
Tests for ensure_dependencies function.

Verifies that the dependency installation and validation mechanism works correctly
for both modules when dependencies are missing or present.
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the pre-push directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "pre-push"))


class TestEnsureDependencies:
    """Tests for automatic dependency installation."""

    def test_ensure_dependencies_with_all_installed(self):
        """Verify no installation occurs when all dependencies present."""
        # All required packages are already installed in test environment
        from githooks.hooks.jira_add_push_worklog import ensure_dependencies

        # Should not raise any exceptions
        try:
            ensure_dependencies()
        except SystemExit:
            pytest.fail("ensure_dependencies should not exit when dependencies present")

    def test_ensure_dependencies_imports_successfully(self):
        """Verify required modules can be imported after ensure_dependencies."""
        from githooks.hooks.jira_add_push_worklog import ensure_dependencies

        ensure_dependencies()

        # These imports should work after ensure_dependencies
        try:
            import jira
            import keyring
            import typer

            assert jira is not None
            assert keyring is not None
            assert typer is not None
        except ImportError as e:
            pytest.fail(f"Required dependency not available: {e}")

    def test_required_dependencies_structure(self):
        """Verify REQUIRED_DEPENDENCIES has correct structure."""
        from githooks.hooks.jira_add_push_worklog import REQUIRED_DEPENDENCIES

        assert isinstance(REQUIRED_DEPENDENCIES, dict)
        assert len(REQUIRED_DEPENDENCIES) == 3
        assert "jira" in REQUIRED_DEPENDENCIES
        assert "keyring" in REQUIRED_DEPENDENCIES
        assert "typer" in REQUIRED_DEPENDENCIES

        # Values should be package names
        assert REQUIRED_DEPENDENCIES["jira"] == "jira"
        assert REQUIRED_DEPENDENCIES["keyring"] == "keyring"
        assert REQUIRED_DEPENDENCIES["typer"] == "typer"


class TestServiceConfiguration:
    """Tests for service and configuration constants."""

    def test_service_name_defined(self):
        """Verify SERVICE_NAME constant is defined."""
        from githooks.core.constants import SERVICE_NAME

        assert isinstance(SERVICE_NAME, str)
        assert SERVICE_NAME == "gojira"

    def test_default_time_spent_format(self):
        """Verify WORKLOG_REVIEW_TIME is in valid Jira format."""
        from githooks.core.constants import WORKLOG_REVIEW_TIME

        assert isinstance(WORKLOG_REVIEW_TIME, str)
        # Should be number followed by time unit
        assert any(unit in WORKLOG_REVIEW_TIME for unit in ["m", "h", "d", "w"])

    def test_branch_regex_defined(self):
        """Verify BRANCH_REGEX constant is defined and valid."""
        import re

        from githooks.core.constants import BRANCH_REGEX

        assert isinstance(BRANCH_REGEX, str)
        # Should compile without errors
        try:
            re.compile(BRANCH_REGEX)
        except re.error as e:
            pytest.fail(f"BRANCH_REGEX is not valid regex: {e}")
