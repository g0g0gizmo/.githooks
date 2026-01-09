"""Tests for issue tracker detection and parsing.

This module tests the issue_tracker.py module which detects and parses
issue references from Git branch names for both JIRA and GitHub Issues.
"""

import pytest

from githooks.core.constants import ISSUE_TRACKER_GITHUB, ISSUE_TRACKER_JIRA, ISSUE_TRACKER_UNKNOWN
from githooks.core.issue_tracker import detect_issue_tracker, format_issue_reference, parse_github_issue, parse_issue_from_branch, parse_jira_ticket


class TestDetectIssueTracker:
    """Tests for detect_issue_tracker function."""

    def test_detects_jira_pattern(self):
        """detect_issue_tracker returns 'jira' for JIRA branch patterns."""
        assert detect_issue_tracker("JT_PTEAE-2930_feature-description") == ISSUE_TRACKER_JIRA
        assert detect_issue_tracker("PROJ-123_fix-bug") == ISSUE_TRACKER_JIRA
        assert detect_issue_tracker("feature/ABC-456") == ISSUE_TRACKER_JIRA

    def test_detects_github_issue_pattern(self):
        """detect_issue_tracker returns 'github' for GitHub issue patterns."""
        assert detect_issue_tracker("issue-123-description") == ISSUE_TRACKER_GITHUB
        assert detect_issue_tracker("gh-456-fix-bug") == ISSUE_TRACKER_GITHUB
        assert detect_issue_tracker("#789-feature") == ISSUE_TRACKER_GITHUB
        assert detect_issue_tracker("123-simple-fix") == ISSUE_TRACKER_GITHUB

    def test_detects_unknown_pattern(self):
        """detect_issue_tracker returns 'unknown' for unrecognized patterns."""
        assert detect_issue_tracker("main") == ISSUE_TRACKER_UNKNOWN
        assert detect_issue_tracker("develop") == ISSUE_TRACKER_UNKNOWN
        assert detect_issue_tracker("feature-branch") == ISSUE_TRACKER_UNKNOWN


class TestParseJiraTicket:
    """Tests for parse_jira_ticket function."""

    def test_parses_jira_ticket_from_branch(self):
        """parse_jira_ticket extracts JIRA ticket key from branch names."""
        assert parse_jira_ticket("JT_PTEAE-2930_feature") == "PTEAE-2930"
        assert parse_jira_ticket("PROJ-123_fix") == "PROJ-123"
        assert parse_jira_ticket("feature/ABC-456") == "ABC-456"

    def test_returns_none_for_non_jira_branches(self):
        """parse_jira_ticket returns None when no JIRA ticket found."""
        assert parse_jira_ticket("issue-123-description") is None
        assert parse_jira_ticket("main") is None
        assert parse_jira_ticket("gh-456-fix") is None


class TestParseGithubIssue:
    """Tests for parse_github_issue function."""

    def test_parses_issue_prefix_pattern(self):
        """parse_github_issue extracts issue number from 'issue-123' pattern."""
        assert parse_github_issue("issue-123-description") == 123
        assert parse_github_issue("issue-456") == 456

    def test_parses_gh_prefix_pattern(self):
        """parse_github_issue extracts issue number from 'gh-123' pattern."""
        assert parse_github_issue("gh-123-description") == 123
        assert parse_github_issue("gh-789") == 789

    def test_parses_hash_prefix_pattern(self):
        """parse_github_issue extracts issue number from '#123' pattern."""
        assert parse_github_issue("#123-description") == 123
        assert parse_github_issue("#456") == 456

    def test_parses_number_at_start_pattern(self):
        """parse_github_issue extracts issue number when branch starts with number."""
        assert parse_github_issue("123-simple-fix") == 123
        assert parse_github_issue("456-add-feature") == 456

    def test_returns_none_for_non_github_branches(self):
        """parse_github_issue returns None when no GitHub issue found."""
        assert parse_github_issue("JT_PTEAE-2930_feature") is None
        assert parse_github_issue("main") is None
        assert parse_github_issue("develop") is None


class TestParseIssueFromBranch:
    """Tests for parse_issue_from_branch function."""

    def test_parses_jira_branch(self):
        """parse_issue_from_branch returns ('jira', key, None) for JIRA branches."""
        tracker, jira_key, github_issue = parse_issue_from_branch("JT_PTEAE-2930_feature")
        assert tracker == ISSUE_TRACKER_JIRA
        assert jira_key == "PTEAE-2930"
        assert github_issue is None

    def test_parses_github_issue_branch(self):
        """parse_issue_from_branch returns ('github', None, number) for GitHub branches."""
        tracker, jira_key, github_issue = parse_issue_from_branch("issue-123-description")
        assert tracker == ISSUE_TRACKER_GITHUB
        assert jira_key is None
        assert github_issue == 123

    def test_parses_unknown_branch(self):
        """parse_issue_from_branch returns ('unknown', None, None) for unrecognized branches."""
        tracker, jira_key, github_issue = parse_issue_from_branch("main")
        assert tracker == ISSUE_TRACKER_UNKNOWN
        assert jira_key is None
        assert github_issue is None


class TestFormatIssueReference:
    """Tests for format_issue_reference function."""

    def test_formats_jira_reference(self):
        """format_issue_reference returns JIRA key format."""
        assert format_issue_reference(ISSUE_TRACKER_JIRA, jira_key="PROJ-123") == "PROJ-123"  # type: ignore[arg-type]

    def test_formats_github_reference(self):
        """format_issue_reference returns '#123' format for GitHub."""
        assert format_issue_reference(ISSUE_TRACKER_GITHUB, github_issue=123) == "#123"  # type: ignore[arg-type]

    def test_formats_unknown_reference(self):
        """format_issue_reference returns 'No issue' for unknown tracker."""
        assert format_issue_reference(ISSUE_TRACKER_UNKNOWN) == "No issue"  # type: ignore[arg-type]


class TestRealWorldBranchNames:
    """Tests with real-world branch name patterns."""

    def test_jira_standard_pattern(self):
        """Handles standard JIRA branch: JT_PTEAE-2930_automatic-sw-versioning."""
        tracker, jira_key, github_issue = parse_issue_from_branch("JT_PTEAE-2930_automatic-sw-versioning")
        assert tracker == ISSUE_TRACKER_JIRA
        assert jira_key == "PTEAE-2930"
        assert github_issue is None

    def test_github_issue_standard_pattern(self):
        """Handles GitHub issue branch: issue-123-fix-login-bug."""
        tracker, jira_key, github_issue = parse_issue_from_branch("issue-123-fix-login-bug")
        assert tracker == ISSUE_TRACKER_GITHUB
        assert jira_key is None
        assert github_issue == 123

    def test_github_short_pattern(self):
        """Handles short GitHub pattern: 42-quick-fix."""
        tracker, jira_key, github_issue = parse_issue_from_branch("42-quick-fix")
        assert tracker == ISSUE_TRACKER_GITHUB
        assert jira_key is None
        assert github_issue == 42

    def test_protected_branches(self):
        """Protected branches (main, develop) return unknown."""
        for branch in ["main", "develop", "master"]:
            tracker, jira_key, github_issue = parse_issue_from_branch(branch)
            assert tracker == ISSUE_TRACKER_UNKNOWN
            assert jira_key is None
            assert github_issue is None
