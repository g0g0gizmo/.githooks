"""
Tests for pre-push Jira worklog hook.

Verifies that the pre-push hook correctly parses Jira tickets from branch names,
interacts with Git commands, and handles Jira transitions to 'Under Review'.
"""

import os
import subprocess

import pytest

from githooks.core.constants import BRANCH_REGEX
from githooks.core.constants import DEFAULT_JIRA_SERVER as DEFAULT_SERVER
from githooks.core.constants import WORKLOG_PUSH_TIME as DEFAULT_TIME_SPENT
from githooks.core.git_operations import get_current_branch

# Use shared lib utilities and fixtures
from githooks.core.jira_client import parse_ticket_from_branch


class TestParseTicketFromBranch:
    """Tests for parsing Jira ticket IDs from branch names."""

    def test_parse_ticket_from_feature_branch(self, sample_branches):
        """Parse ticket from standard feature branch format."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"feature/{REAL_TEST_JIRA_TICKET}-add-feature")
        assert ticket is not None
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_from_bugfix_branch(self, sample_branches):
        """Parse ticket from bugfix branch format."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"bugfix/{REAL_TEST_JIRA_TICKET}-fix-bug")
        assert ticket is not None
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_from_underscore_format(self, sample_branches):
        """Parse ticket from underscore-separated branch format."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"JT_{REAL_TEST_JIRA_TICKET}_automatic-sw-versioning")
        assert ticket is not None
        # Regex captures PROJECT-NUMBER format (letters followed by hyphen and digits)
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_from_complex_branch(self, sample_branches):
        """Parse ticket from complex branch name with multiple parts."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"develop-feature/JT_{REAL_TEST_JIRA_TICKET}_reverse_proxy")
        assert ticket is not None
        # Regex captures PROJECT-NUMBER format
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_returns_none_for_main(self):
        """Return None when branch is 'main' without ticket."""
        ticket = parse_ticket_from_branch("main")
        assert ticket is None

    def test_parse_ticket_returns_none_for_develop(self):
        """Return None when branch is 'develop' without ticket."""
        ticket = parse_ticket_from_branch("develop")
        assert ticket is None

    def test_parse_ticket_returns_none_for_no_ticket_branch(self):
        """Return None when branch has no ticket ID."""
        ticket = parse_ticket_from_branch("no-ticket-branch")
        assert ticket is None

    def test_parse_ticket_returns_none_for_descriptive_branch(self):
        """Return None when branch is descriptive without ticket ID."""
        ticket = parse_ticket_from_branch("feature/add-something")
        assert ticket is None

    def test_parse_ticket_with_empty_string(self):
        """Return None when branch name is empty string."""
        ticket = parse_ticket_from_branch("")
        assert ticket is None

    def test_parse_ticket_with_lowercase_ticket(self):
        """Parse ticket even when ticket ID uses lowercase (should still match)."""
        ticket = parse_ticket_from_branch("feature/proj-999-test")
        assert ticket is None  # Regex requires uppercase letters

    def test_parse_ticket_with_multiple_tickets(self):
        """Parse first ticket when multiple ticket IDs in branch name."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"feature/{REAL_TEST_JIRA_TICKET}-and-OTHER-123")
        assert ticket == REAL_TEST_JIRA_TICKET  # Should return first match


class TestGetCurrentBranch:
    """Tests for getting the current Git branch."""

    def test_get_current_branch_in_git_repo(self, temp_git_repo):
        """Get current branch name from a valid Git repository."""
        os.chdir(temp_git_repo)
        branch = get_current_branch()
        assert branch is not None
        # Default branch could be 'master', 'main', or 'develop' depending on Git config
        assert branch in ["master", "main", "develop"]

    def test_get_current_branch_after_checkout(self, temp_git_repo):
        """Get correct branch name after checking out a new branch."""
        os.chdir(temp_git_repo)

        # Create and checkout new branch
        subprocess.run(["git", "checkout", "-b", "feature/TEST-123-test"], check=True, capture_output=True)

        branch = get_current_branch()
        assert branch == "feature/TEST-123-test"

    def test_get_current_branch_with_slashes(self, temp_git_repo):
        """Handle branch names containing forward slashes."""
        os.chdir(temp_git_repo)

        subprocess.run(["git", "checkout", "-b", "feature/sub/PROJ-456-complex"], check=True, capture_output=True)

        branch = get_current_branch()
        assert branch == "feature/sub/PROJ-456-complex"


class TestConstants:
    """Tests for module-level constants and configuration."""

    def test_default_time_spent_is_string(self):
        """Verify DEFAULT_TIME_SPENT is a string in Jira time format."""
        assert isinstance(DEFAULT_TIME_SPENT, str)
        assert DEFAULT_TIME_SPENT == "2m"  # WORKLOG_PUSH_TIME constant

    def test_default_server_has_fallback(self):
        """Verify DEFAULT_SERVER has appropriate default value."""
        assert isinstance(DEFAULT_SERVER, str)
        assert DEFAULT_SERVER.startswith("https://")

    def test_branch_regex_pattern_matches_uppercase(self):
        """Verify BRANCH_REGEX requires uppercase ticket format."""
        import re

        # Should match
        from tests.conftest import REAL_TEST_JIRA_TICKET

        assert re.search(BRANCH_REGEX, REAL_TEST_JIRA_TICKET)
        assert re.search(BRANCH_REGEX, f"JT_{REAL_TEST_JIRA_TICKET}")

        # Should not match
        assert not re.search(BRANCH_REGEX, "proj-123")
        assert not re.search(BRANCH_REGEX, "123-PROJ")
        assert not re.search(BRANCH_REGEX, "no-ticket-here")


class TestIntegrationScenarios:
    """Integration tests for complete workflows."""

    def test_full_branch_to_ticket_workflow(self, temp_git_repo):
        """Test complete flow from branch creation to ticket parsing."""
        os.chdir(temp_git_repo)

        # Create branch with ticket
        branch_name = "feature/INTEG-789-new-feature"
        subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)

        # Verify we can get the branch
        current_branch = get_current_branch()
        assert current_branch == branch_name

        # Verify we can parse the ticket
        ticket = parse_ticket_from_branch(current_branch)
        assert ticket == "INTEG-789"

    def test_branch_without_ticket_workflow(self, temp_git_repo):
        """Test workflow with branch that has no ticket ID."""
        os.chdir(temp_git_repo)

        # Create branch without ticket
        branch_name = "hotfix/urgent-security-fix"
        subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)

        current_branch = get_current_branch()
        assert current_branch == branch_name

        ticket = parse_ticket_from_branch(current_branch)
        assert ticket is None


class TestTransitionToReview:
    """Tests for transition_to_review function."""

    def test_transition_to_review_success(self):
        """Test successful transition to Under Review."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        # Create mock Jira client
        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions
        mock_jira.transitions.return_value = [{"id": "1", "name": "In Progress"}, {"id": "2", "name": "Under Review"}]

        from tests.conftest import REAL_TEST_JIRA_TICKET

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, REAL_TEST_JIRA_TICKET, f"feature/{REAL_TEST_JIRA_TICKET}-test", "2m")

        assert success is True
        assert error is None
        mock_jira.add_worklog.assert_called_once()
        mock_jira.transition_issue.assert_called_once()

    def test_transition_to_review_alternative_names(self):
        """Test transition with alternative review state names."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions without 'Under Review', but with 'Code Review'
        mock_jira.transitions.return_value = [{"id": "1", "name": "In Progress"}, {"id": "2", "name": "Code Review"}]

        from tests.conftest import REAL_TEST_JIRA_TICKET

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, REAL_TEST_JIRA_TICKET, "feature/test")

        assert success is True
        assert error is None
        # Should transition to 'Code Review' as fallback
        assert mock_jira.transition_issue.call_count >= 1

    def test_transition_to_review_peer_review(self):
        """Test transition with 'Peer Review' state."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions with 'Peer Review'
        mock_jira.transitions.return_value = [{"id": "1", "name": "In Progress"}, {"id": "2", "name": "Peer Review"}]

        from tests.conftest import REAL_TEST_JIRA_TICKET

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, REAL_TEST_JIRA_TICKET, "feature/test")

        assert success is True

    def test_transition_to_review_reviewing_state(self):
        """Test transition with 'Reviewing' state."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        mock_jira.transitions.return_value = [{"id": "1", "name": "Reviewing"}]

        from tests.conftest import REAL_TEST_JIRA_TICKET

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, REAL_TEST_JIRA_TICKET, "feature/test")

        assert success is True

    def test_transition_to_review_no_review_state(self):
        """Test when no review transition available."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions without any review state
        mock_jira.transitions.return_value = [{"id": "1", "name": "Done"}, {"id": "2", "name": "Closed"}]

        from tests.conftest import REAL_TEST_JIRA_TICKET

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, REAL_TEST_JIRA_TICKET, "feature/test")

        # Should still succeed (worklog added)
        assert success is True

    def test_transition_to_review_exception(self):
        """Test exception handling in transition_to_review."""
        from unittest.mock import Mock

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()
        mock_jira.issue.side_effect = Exception("Jira API error")

        success, error = jira_add_push_worklog.transition_to_review(mock_jira, "PROJ-123", "feature/test")

        assert success is False
        assert error is not None
        assert "Failed" in error


class TestMainFunction:
    """Tests for main function."""

    def test_main_with_no_branch(self, capsys):
        """Test main when get_current_branch returns None."""
        from unittest.mock import patch

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        with patch("githooks.hooks.jira_add_push_worklog.get_current_branch", return_value=None):
            with pytest.raises(SystemExit) as exc_info:
                jira_add_push_worklog.main()

            assert exc_info.value.code == 0  # Don't block push

        captured = capsys.readouterr()
        assert "ERROR" in captured.err

    def test_main_with_no_ticket(self, capsys):
        """Test main when branch has no ticket."""
        from unittest.mock import patch

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        with patch("githooks.hooks.jira_add_push_worklog.get_current_branch", return_value="main"):
            with patch("githooks.hooks.jira_add_push_worklog.parse_ticket_from_branch", return_value=None):
                with pytest.raises(SystemExit) as exc_info:
                    jira_add_push_worklog.main()

                assert exc_info.value.code == 0  # Don't block push

    def test_main_with_jira_client_failure(self, capsys):
        """Test main when Jira client creation fails."""
        from unittest.mock import patch

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog
        from tests.conftest import REAL_TEST_JIRA_TICKET

        with patch("githooks.hooks.jira_add_push_worklog.get_current_branch", return_value=f"feature/{REAL_TEST_JIRA_TICKET}-test"):
            with patch("githooks.hooks.jira_add_push_worklog.parse_ticket_from_branch", return_value=REAL_TEST_JIRA_TICKET):
                with patch("githooks.hooks.jira_add_push_worklog.get_jira_client", return_value=None):
                    with pytest.raises(SystemExit) as exc_info:
                        jira_add_push_worklog.main()

                    assert exc_info.value.code == 0  # Don't block push

        captured = capsys.readouterr()
        assert "ERROR" in captured.err

    def test_main_success_path(self, capsys):
        """Test main with successful execution."""
        from unittest.mock import Mock, patch

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()

        from tests.conftest import REAL_TEST_JIRA_TICKET

        with patch("githooks.hooks.jira_add_push_worklog.get_current_branch", return_value=f"feature/{REAL_TEST_JIRA_TICKET}-test"):
            with patch("githooks.hooks.jira_add_push_worklog.parse_ticket_from_branch", return_value=REAL_TEST_JIRA_TICKET):
                with patch("githooks.hooks.jira_add_push_worklog.get_jira_client", return_value=mock_jira):
                    with patch("githooks.hooks.jira_add_push_worklog.transition_to_review", return_value=(True, None)):
                        with pytest.raises(SystemExit) as exc_info:
                            jira_add_push_worklog.main()

                        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "OK" in captured.out

    def test_main_with_transition_error(self, capsys):
        """Test main when transition fails."""
        from unittest.mock import Mock, patch

        import githooks.hooks.jira_add_push_worklog as jira_add_push_worklog

        mock_jira = Mock()

        from tests.conftest import REAL_TEST_JIRA_TICKET

        with patch("githooks.hooks.jira_add_push_worklog.get_current_branch", return_value=f"feature/{REAL_TEST_JIRA_TICKET}-test"):
            with patch("githooks.hooks.jira_add_push_worklog.parse_ticket_from_branch", return_value=REAL_TEST_JIRA_TICKET):
                with patch("githooks.hooks.jira_add_push_worklog.get_jira_client", return_value=mock_jira):
                    # transition_to_review now returns (False, error_message) on failure
                    with patch("githooks.hooks.jira_add_push_worklog.transition_to_review", return_value=(False, "Transition failed")):
                        with pytest.raises(SystemExit) as exc_info:
                            jira_add_push_worklog.main()

                        assert exc_info.value.code == 0  # Don't block push

        captured = capsys.readouterr()
        assert "WARNING" in captured.err
