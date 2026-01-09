"""
Issue tracker detection and parsing utilities.

This module provides unified utilities for detecting and parsing issue references
from Git branch names. It supports both JIRA and GitHub Issues, automatically
detecting which system is being used based on branch naming patterns.

Architecture:
    - Pattern-based detection (JIRA: PROJ-123, GitHub: issue-123, gh-123, #123)
    - Returns issue type, number, and tracker system
    - Used by hooks and CLI commands to work with either system

Branch Naming Patterns:
    JIRA: JT_PTEAE-2930_description, PROJ-123_description
    GitHub: issue-123-description, gh-123-description, 123-description, #123
"""

import re
from typing import Literal, Optional, Tuple

from githooks.core.constants import BRANCH_REGEX, GITHUB_ISSUE_REGEX, ISSUE_TRACKER_GITHUB, ISSUE_TRACKER_JIRA, ISSUE_TRACKER_UNKNOWN

IssueTracker = Literal["jira", "github", "unknown"]


def detect_issue_tracker(branch_name: str) -> IssueTracker:
    """Detect which issue tracking system is used based on branch name.

    Args:
        branch_name: Git branch name to analyze

    Returns:
        'jira', 'github', or 'unknown'
    """
    # Check for JIRA pattern first (more specific: PROJECT-123)
    if re.search(BRANCH_REGEX, branch_name):
        return ISSUE_TRACKER_JIRA  # type: ignore[return-value]

    # Check for GitHub issue patterns (issue-123, gh-123, #123, or just 123-description)
    # Look for common GitHub issue prefixes or numeric patterns
    if re.search(r"(?:issue|gh|#)-?\d+", branch_name, re.IGNORECASE):
        return ISSUE_TRACKER_GITHUB  # type: ignore[return-value]

    # Check if branch name starts with a number (common pattern: 123-fix-bug)
    if re.match(r"^\d+-", branch_name):
        return ISSUE_TRACKER_GITHUB  # type: ignore[return-value]

    return ISSUE_TRACKER_UNKNOWN  # type: ignore[return-value]


def parse_jira_ticket(branch_name: str) -> Optional[str]:
    """Parse JIRA ticket from branch name.

    Args:
        branch_name: Git branch name

    Returns:
        JIRA ticket key (e.g., 'PROJ-123') or None
    """
    match = re.search(BRANCH_REGEX, branch_name)
    return match.group(1) if match else None


def parse_github_issue(branch_name: str) -> Optional[int]:
    """Parse GitHub issue number from branch name.

    Supports patterns:
    - issue-123
    - gh-123
    - #123
    - 123-description (number at start)

    Args:
        branch_name: Git branch name

    Returns:
        GitHub issue number or None
    """
    # Try explicit patterns first (issue-123, gh-123, #123)
    match = re.search(r"(?:issue|gh|#)-?(\d+)", branch_name, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try number at start of branch name (123-description)
    match = re.match(r"^(\d+)-", branch_name)
    if match:
        return int(match.group(1))

    return None


def parse_issue_from_branch(branch_name: str) -> Tuple[IssueTracker, Optional[str], Optional[int]]:
    """Parse issue reference from branch name, detecting tracker type.

    Args:
        branch_name: Git branch name

    Returns:
        Tuple of (tracker_type, jira_key, github_issue_number)
        - tracker_type: 'jira', 'github', or 'unknown'
        - jira_key: JIRA ticket key if JIRA, else None
        - github_issue_number: GitHub issue number if GitHub, else None
    """
    tracker = detect_issue_tracker(branch_name)

    if tracker == ISSUE_TRACKER_JIRA:
        jira_key = parse_jira_ticket(branch_name)
        return (tracker, jira_key, None)

    if tracker == ISSUE_TRACKER_GITHUB:
        github_issue = parse_github_issue(branch_name)
        return (tracker, None, github_issue)

    return (ISSUE_TRACKER_UNKNOWN, None, None)  # type: ignore[return-value]


def format_issue_reference(tracker: IssueTracker, jira_key: Optional[str] = None, github_issue: Optional[int] = None) -> str:
    """Format issue reference for display or URLs.

    Args:
        tracker: Issue tracker type ('jira', 'github', or 'unknown')
        jira_key: JIRA ticket key (e.g., 'PROJ-123')
        github_issue: GitHub issue number (e.g., 123)

    Returns:
        Formatted issue reference (e.g., 'PROJ-123', '#123', 'No issue')
    """
    if tracker == ISSUE_TRACKER_JIRA and jira_key:
        return jira_key
    if tracker == ISSUE_TRACKER_GITHUB and github_issue is not None:
        return f"#{github_issue}"
    return "No issue"
