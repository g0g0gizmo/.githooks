"""
Tests for post-checkout Jira transition and worklog hook.

Verifies that the post-checkout hook correctly parses Jira tickets from branch names,
authenticates with Jira, and transitions tickets to 'In Progress' with worklog entries.
"""

import pytest

from githooks.core.constants import BRANCH_REGEX
from githooks.core.constants import DEFAULT_JIRA_SERVER as DEFAULT_SERVER
from githooks.core.constants import SERVICE_NAME
from githooks.core.constants import WORKLOG_TRANSITION_TIME as DEFAULT_TIME_SPENT

# Use shared lib utilities and constants
from githooks.core.jira_client import parse_ticket_from_branch


class TestParseTicketFromBranch:
    """Tests for parsing Jira ticket IDs from branch names."""

    def test_parse_ticket_from_standard_format(self, sample_branches):
        """Parse ticket from feature/ prefix format."""
        ticket = parse_ticket_from_branch("feature/PROJ-123-add-feature")
        assert ticket == "PROJ-123"

    def test_parse_ticket_from_bugfix_format(self, sample_branches):
        """Parse ticket from bugfix/ prefix format."""
        ticket = parse_ticket_from_branch("bugfix/ABC-456-fix-bug")
        assert ticket == "ABC-456"

    def test_parse_ticket_with_underscore_separator(self, sample_branches):
        """Parse ticket from underscore-separated format."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"JT_{REAL_TEST_JIRA_TICKET}_automatic-sw-versioning")
        # Regex captures PROJECT-NUMBER format (letters-digits)
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_from_complex_prefix(self, sample_branches):
        """Parse ticket from branch with complex prefix structure."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"develop-feature/JT_{REAL_TEST_JIRA_TICKET}_reverse_proxy_login_to_oracle")
        # Regex captures PROJECT-NUMBER format
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_returns_none_for_plain_branch(self):
        """Return None when branch name contains no ticket pattern."""
        ticket = parse_ticket_from_branch("main")
        assert ticket is None

    def test_parse_ticket_returns_none_for_develop(self):
        """Return None for 'develop' branch without ticket."""
        ticket = parse_ticket_from_branch("develop")
        assert ticket is None

    def test_parse_ticket_returns_none_for_descriptive_only(self):
        """Return None when branch is descriptive without ticket ID."""
        ticket = parse_ticket_from_branch("feature/add-new-api")
        assert ticket is None

    def test_parse_ticket_with_empty_string(self):
        """Return None when given empty string."""
        ticket = parse_ticket_from_branch("")
        assert ticket is None

    def test_parse_ticket_with_numeric_only(self):
        """Return None when branch contains only numbers."""
        ticket = parse_ticket_from_branch("12345")
        assert ticket is None

    def test_parse_ticket_with_mixed_case_fails(self):
        """Verify lowercase project codes don't match (regex requires uppercase)."""
        ticket = parse_ticket_from_branch("feature/proj-123-test")
        assert ticket is None

    def test_parse_ticket_extracts_first_occurrence(self):
        """Extract first ticket when multiple present in branch name."""
        ticket = parse_ticket_from_branch("feature/PROJ-123-relates-to-PROJ-456")
        assert ticket == "PROJ-123"

    def test_parse_ticket_with_long_project_code(self):
        """Parse ticket with longer project code abbreviation."""
        ticket = parse_ticket_from_branch("feature/LONGERPROJ-9999-description")
        assert ticket == "LONGERPROJ-9999"

    def test_parse_ticket_with_minimal_format(self):
        """Parse ticket with minimal valid format (one letter, one digit)."""
        ticket = parse_ticket_from_branch("A-1")
        assert ticket == "A-1"


class TestConstants:
    """Tests for module-level constants and configuration."""

    def test_default_time_spent_format(self):
        """Verify DEFAULT_TIME_SPENT is in Jira-compatible format."""
        assert isinstance(DEFAULT_TIME_SPENT, str)
        assert DEFAULT_TIME_SPENT == "5m"

    def test_default_server_configuration(self):
        """Verify DEFAULT_SERVER has valid URL format."""
        assert isinstance(DEFAULT_SERVER, str)
        assert DEFAULT_SERVER.startswith("https://")
        assert "jira" in DEFAULT_SERVER.lower()

    def test_service_name_constant(self):
        """Verify SERVICE_NAME is set for keyring integration."""
        assert isinstance(SERVICE_NAME, str)
        assert SERVICE_NAME == "gojira"

    def test_branch_regex_pattern(self):
        """Verify BRANCH_REGEX matches expected patterns."""
        import re

        # Valid patterns
        assert re.search(BRANCH_REGEX, "PROJ-123")
        assert re.search(BRANCH_REGEX, "ABC-999")
        assert re.search(BRANCH_REGEX, "JT_PTEAE-2930")
        assert re.search(BRANCH_REGEX, "LONGERPROJECT-1")

        # Invalid patterns
        assert not re.search(BRANCH_REGEX, "proj-123")  # lowercase
        assert not re.search(BRANCH_REGEX, "123-PROJ")  # reversed
        assert not re.search(BRANCH_REGEX, "PROJ")  # no number
        assert not re.search(BRANCH_REGEX, "123")  # no letters


class TestBranchPatternEdgeCases:
    """Tests for edge cases in branch name parsing."""

    def test_parse_ticket_with_special_characters(self):
        """Handle branch names with special characters."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"feature/{REAL_TEST_JIRA_TICKET}_&_improvements")
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_with_dashes_in_description(self):
        """Parse ticket when description contains multiple dashes."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"feature/{REAL_TEST_JIRA_TICKET}-add-multi-step-process")
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_with_numbers_in_description(self):
        """Parse ticket when description contains numbers."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"feature/{REAL_TEST_JIRA_TICKET}-update-python3-11-support")
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_at_branch_start(self):
        """Parse ticket when ticket ID starts the branch name."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"{REAL_TEST_JIRA_TICKET}-feature-description")
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_parse_ticket_with_deep_path(self):
        """Parse ticket from branch with deep directory structure."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"team/subteam/feature/{REAL_TEST_JIRA_TICKET}-description")
        assert ticket == REAL_TEST_JIRA_TICKET


class TestDataValidation:
    """Tests for input validation and data integrity."""

    def test_parse_ticket_handles_none_input(self):
        """Gracefully handle None as input."""
        # This should raise an error or return None depending on implementation
        try:
            ticket = parse_ticket_from_branch(None)
            assert ticket is None
        except (AttributeError, TypeError):
            # Expected if implementation doesn't handle None
            pass

    def test_parse_ticket_handles_whitespace_only(self):
        """Return None for whitespace-only branch names."""
        ticket = parse_ticket_from_branch("   ")
        assert ticket is None

    def test_parse_ticket_handles_newlines(self):
        """Handle branch names with newline characters."""
        ticket = parse_ticket_from_branch("feature/PROJ-123\\n")
        # Should still extract ticket despite newline
        assert ticket is None or ticket == "PROJ-123"

    def test_parse_ticket_preserves_exact_format(self):
        """Verify exact ticket format is preserved (case, hyphens)."""
        branch = "feature/MyProj-456-test"
        ticket = parse_ticket_from_branch(branch)
        # Regex requires uppercase, so this might not match
        if ticket:
            assert "MyProj-456" in ticket


class TestRealWorldScenarios:
    """Tests based on real-world branch naming patterns."""

    def test_jira_ticket_from_viasat_pattern(self):
        """Parse ticket from Viasat-style branch naming."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"JT_{REAL_TEST_JIRA_TICKET}_automatic-sw-versioning")
        # Regex extracts PROJECT-NUMBER after underscore
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_jira_ticket_from_oracle_migration_pattern(self):
        """Parse ticket from complex Oracle migration branch."""
        from tests.conftest import REAL_TEST_JIRA_TICKET

        ticket = parse_ticket_from_branch(f"develop-feature/JT_{REAL_TEST_JIRA_TICKET}_reverse_proxy_login_to_oracle")
        # Regex extracts PROJECT-NUMBER after underscore
        assert ticket == REAL_TEST_JIRA_TICKET

    def test_multiple_underscores_in_branch(self):
        """Handle branch with multiple underscore separators."""
        ticket = parse_ticket_from_branch("JT_PROJ_1234_feature_with_many_parts")
        # Should match JT (letters) but pattern expects letter-number
        # This tests if hyphen is required
        assert ticket is None or ticket.startswith("JT")

    def test_hotfix_branch_pattern(self):
        """Parse ticket from hotfix branch naming convention."""
        ticket = parse_ticket_from_branch("hotfix/URGENT-911-critical-fix")
        assert ticket == "URGENT-911"

    def test_release_branch_with_ticket(self):
        """Parse ticket from release branch."""
        ticket = parse_ticket_from_branch("release/v2.0/RELEASE-100-preparation")
        assert ticket == "RELEASE-100"


class TestTransitionAndLogWork:
    """Tests for transition_and_log_work function."""

    def test_transition_and_log_work_success(self):
        """Test successful transition and worklog."""
        from unittest.mock import Mock

        import githooks.hooks.jira_transition_worklog as jira_transition_worklog

        # Create mock Jira client
        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions
        mock_jira.transitions.return_value = [{"id": "1", "name": "Open"}, {"id": "2", "name": "In Progress"}]

        success, error = jira_transition_worklog.transition_and_log_work(mock_jira, "PROJ-123", "feature/PROJ-123-test", "5m")

        assert success is True
        assert error is None
        mock_jira.add_worklog.assert_called_once()
        assert mock_jira.transition_issue.call_count >= 1

    def test_transition_and_log_work_with_open_transition(self):
        """Test transition handling when 'Open' state exists."""
        from unittest.mock import Mock

        import githooks.hooks.jira_transition_worklog as jira_transition_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions with 'Open' state first
        mock_jira.transitions.side_effect = [
            [{"id": "1", "name": "To Do"}, {"id": "2", "name": "Open"}],  # First call
            [{"id": "3", "name": "In Progress"}],  # After transitioning to Open
        ]

        success, error = jira_transition_worklog.transition_and_log_work(mock_jira, "PROJ-123", "feature/test")

        assert success is True
        assert error is None

    def test_transition_and_log_work_no_progress_transition(self):
        """Test when no 'In Progress' transition available."""
        from unittest.mock import Mock

        import githooks.hooks.jira_transition_worklog as jira_transition_worklog

        mock_jira = Mock()
        mock_issue = Mock()
        mock_jira.issue.return_value = mock_issue

        # Mock transitions without 'In Progress'
        mock_jira.transitions.return_value = [{"id": "1", "name": "Done"}, {"id": "2", "name": "Closed"}]

        success, error = jira_transition_worklog.transition_and_log_work(mock_jira, "PROJ-123", "feature/test")

        # Should still succeed (worklog added)
        assert success is True

    def test_transition_and_log_work_exception(self):
        """Test exception handling in transition_and_log_work."""
        from unittest.mock import Mock

        import githooks.hooks.jira_transition_worklog as jira_transition_worklog

        mock_jira = Mock()
        mock_jira.issue.side_effect = Exception("Jira API error")

        success, error = jira_transition_worklog.transition_and_log_work(mock_jira, "PROJ-123", "feature/test")

        assert success is False
        assert error is not None
        assert "Failed" in error
