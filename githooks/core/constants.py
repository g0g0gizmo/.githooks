"""
Centralized constants for Git hooks project.

This module contains all configuration constants used across the git-go workflow,
including JIRA work logging durations, transition names, and service defaults.
"""

# Git Configuration
BRANCH_REGEX = r"([A-Z]+-\d+)"  # JIRA ticket pattern (e.g., PROJ-123)
GITHUB_ISSUE_REGEX = r"(?:issue|gh|#)?-?(\d+)"  # GitHub issue pattern (e.g., issue-123, gh-123, #123)
DEFAULT_ROOT_BRANCH = "develop"

# JIRA Integration
DEFAULT_JIRA_SERVER = "https://jira.viasat.com"
SERVICE_NAME = "gojira"

# Work Logging Durations
WORKLOG_START_TIME = "1m"  # Time logged when starting work (git-go start)
WORKLOG_REVIEW_TIME = "1m"  # Time logged when creating PR (git-go finish)
WORKLOG_DONE_TIME = "1m"  # Time logged when completing work (git-go publish)

# Hook-specific default time values
WORKLOG_TRANSITION_TIME = "5m"  # Time logged when transitioning to In Progress (post-checkout hook)
WORKLOG_PUSH_TIME = "2m"  # Time logged when pushing code for review (pre-push hook)

# JIRA Transition Keywords (searched in order)
TRANSITION_IN_PROGRESS = ["in progress", "development"]
TRANSITION_REVIEW = ["under review", "code review", "peer review", "in review", "review"]
TRANSITION_DONE = ["done", "completed", "closed", "resolve"]

# Test Repository Configuration
TEST_REPO_URL = "https://git.viasat.com/jtuttle/test-repo"
TEST_JIRA_SERVER = "https://git.viasat.com/jtuttle/test-repo/issues"

# Alias map for repositories used by git-go commands
ALIAS_MAP: dict[str, str] = {
    "test": TEST_REPO_URL,
}

# GitHub Integration
GITHUB_PR_BODY_TEMPLATE = """# [{ticket}]({jira_url}/browse/{ticket})

## Description

{summary}

## Commits

{commits}

## Test Steps

1. Review code changes
2. Run automated tests
3. Verify functionality
"""

# Issue Tracking Types
ISSUE_TRACKER_JIRA = "jira"
ISSUE_TRACKER_GITHUB = "github"
ISSUE_TRACKER_UNKNOWN = "unknown"

# Dependencies
REQUIRED_DEPENDENCIES = {"jira": "jira", "keyring": "keyring", "PyGithub": "PyGithub"}
