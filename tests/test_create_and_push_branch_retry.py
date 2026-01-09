"""Tests for create_and_push_branch retry logic."""

import subprocess
import time
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

from githooks.core.github_utils import create_and_push_branch


class TestCreateAndPushBranchRetry:
    """Tests for create_and_push_branch with retry logic."""

    def test_successful_push_returns_true(self, temp_git_repo):
        """create_and_push_branch returns True on successful push."""
        branch_name = "test-branch"

        # Mock subprocess to simulate success
        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            # First call: rev-parse (branch doesn't exist)
            # Second call: checkout root branch (success)
            # Third call: checkout -b new branch (success)
            # Fourth call: git push (success)
            mock_results = [
                MagicMock(returncode=1, stderr=""),  # rev-parse: branch doesn't exist
                MagicMock(returncode=0),  # checkout root branch
                MagicMock(returncode=0),  # checkout -b
                MagicMock(returncode=0, stdout="", stderr=""),  # git push success
            ]
            mock_run.side_effect = mock_results

            result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop")
            assert result is True

    def test_branch_already_exists_locally(self, temp_git_repo):
        """create_and_push_branch handles existing local branch."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            # First call: rev-parse (branch exists)
            # Second call: checkout existing branch
            # Third call: git push success
            mock_results = [
                MagicMock(returncode=0),  # rev-parse: branch exists
                MagicMock(returncode=0),  # checkout existing branch
                MagicMock(returncode=0, stdout="", stderr=""),  # git push success
            ]
            mock_run.side_effect = mock_results

            result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop")
            assert result is True

    def test_branch_already_exists_on_remote(self, temp_git_repo):
        """create_and_push_branch succeeds if branch already exists on remote."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            # First call: rev-parse (branch doesn't exist locally)
            # Second call: checkout root
            # Third call: checkout -b new branch
            # Fourth call: git push fails with "already exists"
            mock_results = [
                MagicMock(returncode=1, stderr=""),
                MagicMock(returncode=0),
                MagicMock(returncode=0),
                MagicMock(returncode=1, stdout="", stderr="remote: error: branch already exists"),  # already exists
            ]
            mock_run.side_effect = mock_results

            result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop")
            assert result is True

    def test_transient_network_error_retries(self, temp_git_repo):
        """create_and_push_branch retries on transient network errors."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            with patch("time.sleep") as mock_sleep:
                # Setup: branch doesn't exist, need to create it
                # Then simulate: push fails with network error, then succeeds
                mock_results = [
                    MagicMock(returncode=1, stderr=""),  # rev-parse: doesn't exist
                    MagicMock(returncode=0),  # checkout develop
                    MagicMock(returncode=0),  # checkout -b
                    # First push attempt: network error (will be retried)
                    MagicMock(
                        returncode=1,
                        stdout="",
                        stderr="fatal: Connection reset by peer",
                    ),
                    # Second push attempt: success
                    MagicMock(returncode=0, stdout="", stderr=""),
                ]
                mock_run.side_effect = mock_results

                result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop", max_retries=3)
                assert result is True

                # Verify retry sleep was called (exponential backoff: 1s for first retry)
                mock_sleep.assert_called_with(1)

    def test_persistent_error_after_retries_fails(self, temp_git_repo):
        """create_and_push_branch fails after max retries."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            with patch("time.sleep"):
                # Setup branch creation
                # Then simulate: all push attempts fail with non-transient error
                mock_results = [
                    MagicMock(returncode=1, stderr=""),  # rev-parse
                    MagicMock(returncode=0),  # checkout develop
                    MagicMock(returncode=0),  # checkout -b
                    # All push attempts fail with permission denied (non-transient)
                    MagicMock(
                        returncode=1,
                        stdout="",
                        stderr="fatal: Could not read from remote repository. Permission denied",
                    ),
                    MagicMock(
                        returncode=1,
                        stdout="",
                        stderr="fatal: Could not read from remote repository. Permission denied",
                    ),
                    MagicMock(
                        returncode=1,
                        stdout="",
                        stderr="fatal: Could not read from remote repository. Permission denied",
                    ),
                    # Final verify via ls-remote fails
                    MagicMock(returncode=1, stdout="", stderr=""),
                ]
                mock_run.side_effect = mock_results

                result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop", max_retries=3)
                assert result is False

    def test_branch_verified_exists_via_ls_remote(self, temp_git_repo):
        """create_and_push_branch succeeds if branch exists on remote (verified via ls-remote)."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            with patch("time.sleep"):
                # Setup
                # Push fails multiple times
                # But ls-remote shows branch exists
                mock_results = [
                    MagicMock(returncode=1, stderr=""),  # rev-parse
                    MagicMock(returncode=0),  # checkout develop
                    MagicMock(returncode=0),  # checkout -b
                    # All push attempts fail
                    MagicMock(returncode=1, stdout="", stderr="network error"),
                    MagicMock(returncode=1, stdout="", stderr="network error"),
                    MagicMock(returncode=1, stdout="", stderr="network error"),
                    # ls-remote shows branch exists (on final attempt)
                    MagicMock(
                        returncode=0,
                        stdout="abc123def456\trefs/heads/test-branch",
                        stderr="",
                    ),
                ]
                mock_run.side_effect = mock_results

                result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop", max_retries=3)
                assert result is True

    def test_exponential_backoff_timing(self, temp_git_repo):
        """create_and_push_branch uses exponential backoff for retries."""
        branch_name = "test-branch"

        with patch("githooks.core.github_utils.subprocess.run") as mock_run:
            with patch("time.sleep") as mock_sleep:
                # Setup branch creation
                # Then simulate: multiple transient failures followed by success
                mock_results = [
                    MagicMock(returncode=1, stderr=""),  # rev-parse
                    MagicMock(returncode=0),  # checkout develop
                    MagicMock(returncode=0),  # checkout -b
                    # First push: connection refused (retry)
                    MagicMock(returncode=1, stdout="", stderr="connection refused"),
                    # Second push: connection reset (retry)
                    MagicMock(returncode=1, stdout="", stderr="connection reset"),
                    # Third push: success
                    MagicMock(returncode=0, stdout="", stderr=""),
                ]
                mock_run.side_effect = mock_results

                result = create_and_push_branch(Path(temp_git_repo), branch_name, "develop", max_retries=4)
                assert result is True

                # Verify exponential backoff: 1s, then 2s
                assert mock_sleep.call_count == 2
                mock_sleep.assert_any_call(1)  # 2^(1-1) = 1
                mock_sleep.assert_any_call(2)  # 2^(2-1) = 2
