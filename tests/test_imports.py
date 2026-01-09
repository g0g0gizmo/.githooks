#!/usr/bin/env python
"""Quick test to verify module imports work correctly."""

import sys


def test_jira_add_push_worklog():
    """Test jira_add_push_worklog exports."""
    from githooks.hooks import jira_add_push_worklog

    expected = [
        "BRANCH_REGEX",
        "SERVICE_NAME",
        "DEFAULT_SERVER",
        "DEFAULT_TIME_SPENT",
        "REQUIRED_DEPENDENCIES",
        "ensure_dependencies",
        "parse_ticket_from_branch",
        "get_current_branch",
        "get_jira_client",
        "transition_to_review",
    ]

    for attr in expected:
        if not hasattr(jira_add_push_worklog, attr):
            print(f"❌ Missing: {attr}")
            return False
        print(f"✅ Found: {attr}")

    # Test constants have correct values
    assert jira_add_push_worklog.SERVICE_NAME == "gojira"
    assert jira_add_push_worklog.DEFAULT_SERVER == "https://jira.viasat.com"
    assert jira_add_push_worklog.DEFAULT_TIME_SPENT == "2m"
    assert len(jira_add_push_worklog.REQUIRED_DEPENDENCIES) == 3

    return True


def test_jira_transition_worklog():
    """Test jira_transition_worklog exports."""
    from githooks.hooks import jira_transition_worklog

    expected = [
        "BRANCH_REGEX",
        "SERVICE_NAME",
        "DEFAULT_SERVER",
        "DEFAULT_TIME_SPENT",
        "REQUIRED_DEPENDENCIES",
        "ensure_dependencies",
        "parse_ticket_from_branch",
        "get_jira_client",
        "transition_and_log_work",
    ]

    for attr in expected:
        if not hasattr(jira_transition_worklog, attr):
            print(f"❌ Missing: {attr}")
            return False
        print(f"✅ Found: {attr}")

    # Test constants have correct values
    assert jira_transition_worklog.SERVICE_NAME == "gojira"
    assert jira_transition_worklog.DEFAULT_SERVER == "https://jira.viasat.com"
    assert jira_transition_worklog.DEFAULT_TIME_SPENT == "5m"
    assert len(jira_transition_worklog.REQUIRED_DEPENDENCIES) == 3

    return True


if __name__ == "__main__":
    print("Testing jira_add_push_worklog...")
    if not test_jira_add_push_worklog():
        sys.exit(1)

    print("\nTesting jira_transition_worklog...")
    if not test_jira_transition_worklog():
        sys.exit(1)

    print("\n✅ All imports successful!")
