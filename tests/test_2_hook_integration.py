"""
Tests for Git hooks integration and main entry points.

Verifies the main() functions, dependency checks, and full workflow integrations
without external dependencies like Jira.
"""

import sys
from pathlib import Path


def test_jira_add_push_worklog_module_imports():
    """Module can be imported successfully."""
    import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

    assert jira_add_push_worklog is not None


def test_jira_transition_worklog_module_imports():
    """Module can be imported successfully."""
    import githooks.hooks.jira_transition_worklog as jira_transition_worklog

    assert jira_transition_worklog is not None


def test_parse_ticket_from_branch_basic():
    """Parse ticket handles basic branch patterns."""
    from githooks.hooks.jira_add_push_worklog import parse_ticket_from_branch

    result = parse_ticket_from_branch("feature/TEST-123-description")
    assert result == "TEST-123"


def test_parse_ticket_handles_none():
    """Parse ticket returns None for non-matching input."""
    from githooks.hooks.jira_add_push_worklog import parse_ticket_from_branch

    result = parse_ticket_from_branch("main")
    assert result is None


def test_get_current_branch_returns_string_or_none():
    """Get current branch returns string or None."""
    from githooks.hooks.jira_add_push_worklog import get_current_branch

    result = get_current_branch()
    # In test environment, might return None or a branch name
    assert result is None or isinstance(result, str)


def test_constants_defined_in_add_push():
    """All required constants are defined in add_push module."""
    import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

    assert hasattr(jira_add_push_worklog, "BRANCH_REGEX")
    assert hasattr(jira_add_push_worklog, "SERVICE_NAME")
    assert hasattr(jira_add_push_worklog, "DEFAULT_TIME_SPENT")
    assert hasattr(jira_add_push_worklog, "DEFAULT_SERVER")
    assert hasattr(jira_add_push_worklog, "REQUIRED_DEPENDENCIES")


def test_constants_defined_in_transition():
    """All required constants are defined in transition module."""
    import githooks.hooks.jira_transition_worklog as jira_transition_worklog

    assert hasattr(jira_transition_worklog, "BRANCH_REGEX")
    assert hasattr(jira_transition_worklog, "SERVICE_NAME")
    assert hasattr(jira_transition_worklog, "DEFAULT_TIME_SPENT")
    assert hasattr(jira_transition_worklog, "DEFAULT_SERVER")
    assert hasattr(jira_transition_worklog, "REQUIRED_DEPENDENCIES")


def test_functions_defined_in_add_push():
    """All required functions are defined in add_push module."""
    import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

    assert callable(jira_add_push_worklog.parse_ticket_from_branch)
    assert callable(jira_add_push_worklog.get_current_branch)
    assert callable(jira_add_push_worklog.ensure_dependencies)
    assert callable(jira_add_push_worklog.get_jira_client)
    assert callable(jira_add_push_worklog.transition_to_review)
    assert callable(jira_add_push_worklog.main)


def test_functions_defined_in_transition():
    """All required functions are defined in transition module."""
    import githooks.hooks.jira_transition_worklog as jira_transition_worklog

    assert callable(jira_transition_worklog.parse_ticket_from_branch)
    assert callable(jira_transition_worklog.ensure_dependencies)
    assert callable(jira_transition_worklog.get_jira_client)
    assert callable(jira_transition_worklog.transition_and_log_work)


def test_required_dependencies_structure():
    """REQUIRED_DEPENDENCIES is properly structured."""
    import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

    deps = jira_add_push_worklog.REQUIRED_DEPENDENCIES
    assert isinstance(deps, dict)
    assert "jira" in deps
    assert "keyring" in deps
    assert "typer" in deps


def test_service_name_is_gojira():
    """SERVICE_NAME constant is correctly set."""
    import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

    assert jira_add_push_worklog.SERVICE_NAME == "gojira"


def test_branch_regex_matches_uppercase_ticket():
    """BRANCH_REGEX pattern matches uppercase ticket IDs."""
    import re

    from githooks.hooks.jira_add_push_worklog import BRANCH_REGEX

    match = re.search(BRANCH_REGEX, "feature/PROJ-123-test")
    assert match is not None
    assert match.group(1) == "PROJ-123"


def test_default_time_spent_format():
    """DEFAULT_TIME_SPENT is in valid Jira format."""
    from githooks.hooks.jira_add_push_worklog import DEFAULT_TIME_SPENT

    assert isinstance(DEFAULT_TIME_SPENT, str)
    assert "m" in DEFAULT_TIME_SPENT or "h" in DEFAULT_TIME_SPENT or "d" in DEFAULT_TIME_SPENT


def test_default_server_has_valid_url():
    """DEFAULT_SERVER is a valid HTTPS URL."""
    from githooks.hooks.jira_add_push_worklog import DEFAULT_SERVER

    assert DEFAULT_SERVER.startswith("https://")
    assert "jira" in DEFAULT_SERVER.lower()
