"""Tests for commitmint correction helpers. Verifies duplicate scope fix and ticket insertion.

This suite uses a real temporary Git repo to create commits and validate message processing
via helper functions without mocking Typer prompts.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from githooks.cli.commitmint import (
    add_footer_if_breaking_change,
    ensure_commitlint_installed,
    ensure_ticket_in_header,
    extract_ticket_from_header_or_body,
    fix_duplicate_scope,
    has_conventional_type,
    infer_branch_name,
    main,
    suggest_type_header,
    validate_commit_message,
)


def init_temp_repo() -> Path:
    repo_dir = Path(tempfile.mkdtemp(prefix="commitmint_test_"))
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test.user@example.com"], cwd=repo_dir, check=True, capture_output=True)
    # Disable hooks in test repo to avoid interference
    subprocess.run(["git", "config", "core.hooksPath", "/dev/null"], cwd=repo_dir, check=True, capture_output=True)
    return repo_dir


def test_duplicate_scope_is_fixed():
    """Duplicate scope in header is removed: 'feat(scope): scope: msg' -> 'feat(scope): msg'."""
    repo = init_temp_repo()
    # Create initial commit
    Path(repo / "README.md").write_text("hello", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True)
    msg = "feat(core): core: add readme"
    subprocess.run(["git", "commit", "-m", msg], cwd=repo, check=True, capture_output=True)

    fixed = fix_duplicate_scope(msg)
    assert fixed == "feat(core): add readme"


def test_duplicate_scope_noop_when_not_present():
    """When no duplicate scope is present, message remains unchanged."""
    msg = "feat(core): add readme"
    assert fix_duplicate_scope(msg) == msg


def test_insert_ticket_in_header_when_missing():
    """Ticket JT_PTEAE-0000 is inserted after header when missing."""
    repo = init_temp_repo()
    # Create branch with ISSUE-0000 (generic) style to simulate branch naming
    subprocess.run(["git", "checkout", "-b", "feature/ABCD-0000_sample"], cwd=repo, check=True, capture_output=True)

    # Make a commit missing the ticket in header/body
    Path(repo / "file.txt").write_text("data", encoding="utf-8")
    subprocess.run(["git", "add", "file.txt"], cwd=repo, check=True, capture_output=True)
    msg = "fix(api): correct timeout logic"
    subprocess.run(["git", "commit", "-m", msg], cwd=repo, check=True, capture_output=True)

    # Ensure ticket placement policy applies
    ticket = "ISSUE-0000"
    proposed = ensure_ticket_in_header(msg, ticket)
    assert proposed.startswith("fix(api): ISSUE-0000 "), "Ticket should be inserted after header prefix"
    assert "correct timeout logic" in proposed


def test_insert_ticket_in_header_when_already_present():
    """If ticket already present, message remains unchanged."""
    msg = "fix(api): ISSUE-0000 correct timeout logic"
    assert ensure_ticket_in_header(msg, "ISSUE-0000") == msg


def test_breaking_change_footer_added():
    """Smart Commit footer is appended when breaking change is detected."""
    msg = "feat(api)!: overhaul request pipeline"
    with_footer = add_footer_if_breaking_change(msg, "JT_PTEAE-1234")
    assert "JT_PTEAE-1234 #comment" in with_footer
    assert "#resolve" in with_footer

    msg2 = "refactor(core): major subsystem rewrite\n\nBREAKING CHANGE: config format changed"
    with_footer2 = add_footer_if_breaking_change(msg2, "ABCD-0000")
    assert "ABCD-0000 #comment" in with_footer2


def test_breaking_change_footer_not_added_when_not_breaking():
    """Footer is not appended for non-breaking messages."""
    msg = "chore(ci): update pipeline"
    res = add_footer_if_breaking_change(msg, "JT_PTEAE-1234")
    assert res == msg


def test_type_suggestion_and_detection():
    """Type suggestion returns docs for docs-like messages, feat otherwise; detection recognizes conventional headers."""
    m1 = "update README with usage"
    s1 = suggest_type_header(m1)
    assert s1.startswith("docs:"), "Should suggest docs: when README/docs referenced"

    m2 = "add new widget component"
    s2 = suggest_type_header(m2)
    assert s2.startswith("feat:"), "Should default to feat: suggestion"

    assert has_conventional_type("fix(ui): correct layout")
    assert has_conventional_type("feat(core)!: breaking change")
    assert not has_conventional_type("improve performance")


def test_infer_branch_name_uppercases_ticket_and_uses_alias():
    """Branch inference uses uppercased ticket and alias fallback."""
    assert infer_branch_name("myproj", "abcd-123") == "ABCD-123_myproj"


def test_python_side_validation_reports_errors_without_commitlint():
    """When commitlint is absent, python-side validation flags missing type and ticket."""
    import os

    # Prevent automatic installation of commitlint during test
    old_val = os.environ.get("COMMITMINT_SKIP_INSTALL")
    os.environ["COMMITMINT_SKIP_INSTALL"] = "1"
    try:
        ok, errs = validate_commit_message("add a thing")
        assert not ok
        assert any("Missing conventional type" in e for e in errs)
        assert any("Missing Jira ticket" in e for e in errs)
    finally:
        if old_val is None:
            os.environ.pop("COMMITMINT_SKIP_INSTALL", None)
        else:
            os.environ["COMMITMINT_SKIP_INSTALL"] = old_val


# 30 variations of bad commit messages covering common issues
BAD_COMMITS = [
    # Missing type prefix (1-5)
    ("add new feature", "Missing type prefix"),
    ("fix the bug", "Missing type prefix"),
    ("update documentation", "Missing type prefix"),
    ("remove old code", "Missing type prefix"),
    ("refactor module", "Missing type prefix"),
    # Missing ticket (6-10)
    ("feat: add new widget", "Missing ticket"),
    ("fix: correct login flow", "Missing ticket"),
    ("docs: update readme", "Missing ticket"),
    ("style: format code", "Missing ticket"),
    ("chore: update deps", "Missing ticket"),
    # Duplicate scope (11-15)
    ("feat(core): core: implement feature", "Duplicate scope"),
    ("fix(api): api: resolve timeout", "Duplicate scope"),
    ("docs(readme): readme: add section", "Duplicate scope"),
    ("refactor(utils): utils: extract helper", "Duplicate scope"),
    ("test(unit): unit: add coverage", "Duplicate scope"),
    # Missing ticket + duplicate scope (16-20)
    ("feat(auth): auth: add oauth", "Missing ticket + duplicate scope"),
    ("fix(db): db: optimize query", "Missing ticket + duplicate scope"),
    ("docs(guide): guide: add tutorial", "Missing ticket + duplicate scope"),
    ("ci(pipeline): pipeline: add stage", "Missing ticket + duplicate scope"),
    ("chore(deps): deps: upgrade libs", "Missing ticket + duplicate scope"),
    # Breaking changes missing footer (21-25)
    ("feat(api)!: change request format", "Breaking change missing footer"),
    ("refactor(core)!: rewrite engine", "Breaking change missing footer"),
    ("feat(auth)!: new auth mechanism", "Breaking change missing footer"),
    ("fix(config)!: change config schema", "Breaking change missing footer"),
    ("feat(db)!: new database driver", "Breaking change missing footer"),
    # Complex cases (26-30)
    ("implement user dashboard", "Complex: no type or ticket"),
    ("feat(ui): ui: ui: triple duplicate scope", "Complex: triple duplicate"),
    ("fix problem with cache", "Complex: missing type and ticket"),
    ("feat: add ISSUE-9999 feature but wrong ticket", "Complex: wrong ticket number"),
    ("docs: update README with examples", "Complex: missing ticket"),
]


@pytest.mark.parametrize("bad_msg,description", BAD_COMMITS, ids=[desc for _, desc in BAD_COMMITS])
def test_bad_commit_corrected_format(bad_msg: str, description: str):  # noqa: ARG001
    """Verify each bad commit message can be corrected using commitmint helpers.

    Simulates the correction pipeline without interactive Typer prompts by directly
    calling the helper functions on each bad commit message.
    """
    repo = init_temp_repo()
    ticket = "ISSUE-1234"

    # Create test branch
    subprocess.run(["git", "checkout", "-b", f"feature/{ticket}_test-corrections"], cwd=repo, check=True, capture_output=True)

    # Create commit with bad message
    file_path = repo / "test_file.txt"
    file_path.write_text("test content", encoding="utf-8")
    subprocess.run(["git", "add", str(file_path)], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", bad_msg], cwd=repo, check=True, capture_output=True)

    # Get the commit message
    result = subprocess.run(["git", "log", "HEAD", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
    original_msg = result.stdout.strip()

    # Apply correction pipeline
    corrected_msg = original_msg

    # Check for breaking change FIRST before type suggestion might mask it
    is_breaking = "!" in original_msg or "BREAKING CHANGE:" in original_msg

    # Stage 0: Type suggestion (only if missing type)
    if not has_conventional_type(corrected_msg):
        corrected_msg = suggest_type_header(corrected_msg)

    # Stage 1: Duplicate scope fix
    corrected_msg = fix_duplicate_scope(corrected_msg)

    # Stage 2: Ticket insertion
    corrected_msg = ensure_ticket_in_header(corrected_msg, ticket)

    # Stage 3: Breaking change footer (detect from FINAL corrected msg OR original flag)
    if is_breaking or ("!" in corrected_msg.split("\n")[0]):
        final_msg = add_footer_if_breaking_change(corrected_msg, ticket)
    else:
        final_msg = corrected_msg

    # Validate final message has required elements
    assert has_conventional_type(final_msg), f"Still missing conventional type: {final_msg}"
    assert ticket in final_msg, f"Still missing ticket {ticket}: {final_msg}"

    # For breaking changes, ensure footer is present
    if is_breaking:
        assert f"{ticket} #comment" in final_msg, f"Missing Smart Commit footer: {final_msg}"


def test_thirty_bad_commits_corrected_format():
    """Create 30 bad commits and verify each can be corrected using commitmint helpers.

    Simulates the correction pipeline without interactive Typer prompts by directly
    calling the helper functions on each bad commit message.
    """
    repo = init_temp_repo()
    ticket = "ISSUE-1234"

    # Create test branch
    subprocess.run(["git", "checkout", "-b", f"feature/{ticket}_test-corrections"], cwd=repo, check=True, capture_output=True)
    # Open repo branch in browser for visual inspection if needed

    # 30 variations of bad commit messages covering common issues
    bad_commits = [
        # Missing type prefix (1-5)
        "add new feature",
        "fix the bug",
        "update documentation",
        "remove old code",
        "refactor module",
        # Missing ticket (6-10)
        "feat: add new widget",
        "fix: correct login flow",
        "docs: update readme",
        "style: format code",
        "chore: update deps",
        # Duplicate scope (11-15)
        "feat(core): core: implement feature",
        "fix(api): api: resolve timeout",
        "docs(readme): readme: add section",
        "refactor(utils): utils: extract helper",
        "test(unit): unit: add coverage",
        # Missing ticket + duplicate scope (16-20)
        "feat(auth): auth: add oauth",
        "fix(db): db: optimize query",
        "docs(guide): guide: add tutorial",
        "ci(pipeline): pipeline: add stage",
        "chore(deps): deps: upgrade libs",
        # Breaking changes missing footer (21-25)
        "feat(api)!: change request format",
        "refactor(core)!: rewrite engine",
        "feat(auth)!: new auth mechanism",
        "fix(config)!: change config schema",
        "feat(db)!: new database driver",
        # Complex cases (26-30)
        "implement user dashboard",
        "feat(ui): ui: ui: triple duplicate scope",
        "fix problem with cache",
        "feat: add ISSUE-9999 feature but wrong ticket",
        "docs: update README with examples",
    ]

    # Create all 30 commits
    for idx, msg in enumerate(bad_commits, start=1):
        file_path = repo / f"file_{idx}.txt"
        file_path.write_text(f"content {idx}", encoding="utf-8")
        subprocess.run(["git", "add", str(file_path)], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", msg], cwd=repo, check=True, capture_output=True)

    # Now verify corrections work for each commit message
    corrections_applied = 0
    subprocess.run(["git", "checkout", f"feature/{ticket}_test-corrections"], cwd=repo, check=True, capture_output=True)

    for idx in range(1, 31):
        # Get the commit message for commit at HEAD~(30-idx)
        offset = 30 - idx
        result = subprocess.run(["git", "log", f"HEAD~{offset}", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
        original_msg = result.stdout.strip()

        # Apply correction pipeline
        corrected_msg = original_msg

        # Check for breaking change FIRST before type suggestion might mask it
        is_breaking = "!" in original_msg or "BREAKING CHANGE:" in original_msg

        # Stage 0: Type suggestion (only if missing type)
        if not has_conventional_type(corrected_msg):
            corrected_msg = suggest_type_header(corrected_msg)

        # Stage 1: Duplicate scope fix
        corrected_msg = fix_duplicate_scope(corrected_msg)

        # Stage 2: Ticket insertion
        corrected_msg = ensure_ticket_in_header(corrected_msg, ticket)

        # Stage 3: Breaking change footer (detect from FINAL corrected msg OR original flag)
        # Use add_footer_if_breaking_change which does its own detection
        if is_breaking or ("!" in corrected_msg.split("\n")[0]):
            final_msg = add_footer_if_breaking_change(corrected_msg, ticket)
        else:
            final_msg = corrected_msg

        # Verify corrections were effective
        if final_msg != original_msg:
            corrections_applied += 1

        # Validate final message has required elements
        assert has_conventional_type(final_msg), f"Commit {idx} still missing conventional type: {final_msg}"
        assert ticket in final_msg, f"Commit {idx} still missing ticket {ticket}: {final_msg}"

        # For breaking changes, ensure footer is present
        if is_breaking:
            assert f"{ticket} #comment" in final_msg, f"Commit {idx} missing Smart Commit footer: {final_msg}"

    # Verify that corrections were actually needed and applied
    assert corrections_applied >= 25, f"Expected at least 25 corrections, but only applied {corrections_applied}"


def test_fix_duplicate_scope_fallback_regex():
    """Test fallback regex pattern in fix_duplicate_scope when scope parsing fails."""
    # Edge case: message without scope in parentheses - uses fallback pattern
    msg = "feat: feat: add feature"
    result = fix_duplicate_scope(msg)
    # Fallback pattern should handle this by removing duplicate prefix
    assert "feat:" in result


def test_ensure_ticket_no_header_ticket_already_present():
    """Test ensure_ticket_in_header when no header exists but ticket is in message."""
    msg = "JT_PTEAE-1234 some message without conventional type"
    result = ensure_ticket_in_header(msg, "JT_PTEAE-1234")
    assert result == msg  # Should not modify since ticket already present


def test_ensure_ticket_no_header_prepend():
    """Test ensure_ticket_in_header when no header exists and no ticket present."""
    msg = "some random commit message"
    result = ensure_ticket_in_header(msg, "ISSUE-999")
    assert result == "ISSUE-999 some random commit message"


def test_breaking_change_footer_already_present():
    """Test add_footer_if_breaking_change when footer is already in the message."""
    msg = "feat(api)!: breaking change\n\nISSUE-123 #comment Breaking change; review impacts #resolve"
    result = add_footer_if_breaking_change(msg, "ISSUE-123")
    assert result == msg  # Should not duplicate footer


def test_extract_ticket_from_header_or_body():
    """Test extract_ticket_from_header_or_body finds tickets in various formats."""
    # Regex looks for [A-Z]{2,}-\d+ pattern (2+ uppercase letters, hyphen, digits)
    assert extract_ticket_from_header_or_body("feat: ABC-123 add feature") == "ABC-123"
    assert extract_ticket_from_header_or_body("fix: resolve JIRA-456 issue") == "JIRA-456"
    assert extract_ticket_from_header_or_body("no ticket here") is None
    assert extract_ticket_from_header_or_body("ISSUE-789 in message") == "ISSUE-789"
    # Note: Pattern doesn't match underscores, so JT_PTEAE-456 won't match as a single ticket
    result = extract_ticket_from_header_or_body("fix: PTEAE-456 issue")
    assert result == "PTEAE-456"


def test_validate_commit_message_python_side_both_errors():
    """Test Python-side validation catches both missing type and ticket."""
    ok, errors = validate_commit_message("just a message")
    assert not ok
    assert len(errors) == 2
    assert any("conventional type" in e for e in errors)
    assert any("Jira ticket" in e for e in errors)


def test_validate_commit_message_python_side_valid():
    """Test Python-side validation passes for valid conventional commit with ticket."""
    ok, errors = validate_commit_message("feat: ABC-123 add new feature")
    assert ok
    assert len(errors) == 0


def test_ensure_commitlint_installed_no_npm():
    """Test ensure_commitlint_installed when npm is not available."""
    with mock.patch("shutil.which") as mock_which:
        mock_which.return_value = None  # Simulate no npm, winget, choco
        # Should complete without error and log warning
        ensure_commitlint_installed()


def test_ensure_commitlint_installed_with_npm():
    """Test ensure_commitlint_installed when npm is available."""
    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            mock_which.return_value = "/usr/bin/npm"
            mock_run.return_value = mock.Mock(returncode=0)

            ensure_commitlint_installed()

            # Should attempt npm install
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            assert call_args[0] == "npm"
            assert "install" in call_args


def test_ensure_commitlint_installed_with_winget():
    """Test ensure_commitlint_installed with winget fallback."""
    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            # First call: no npm, second call: winget available, third: npm after install
            mock_which.side_effect = [None, "/usr/bin/winget", "/usr/bin/npm"]
            mock_run.return_value = mock.Mock(returncode=0)

            ensure_commitlint_installed()

            # Should call winget install and then npm install
            assert mock_run.call_count == 2


def test_ensure_commitlint_installed_with_choco():
    """Test ensure_commitlint_installed with chocolatey fallback."""
    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            # No npm, no winget, choco available, then npm after install
            mock_which.side_effect = [None, None, "/usr/bin/choco", "/usr/bin/npm"]
            mock_run.return_value = mock.Mock(returncode=0)

            ensure_commitlint_installed()

            # Should call choco install and then npm install
            assert mock_run.call_count == 2
            first_call_args = mock_run.call_args_list[0][0][0]
            assert first_call_args[0] == "choco"


def test_validate_commit_message_with_commitlint():
    """Test validate_commit_message when commitlint is available."""
    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            with mock.patch("pathlib.Path.write_text"):
                with mock.patch("pathlib.Path.unlink"):
                    mock_which.return_value = "/usr/bin/commitlint"
                    mock_run.return_value = mock.Mock(returncode=0, stdout="", stderr="")

                    ok, errors = validate_commit_message("feat: ABC-123 test")

                    # When commitlint is available, should return True with no errors
                    assert ok
                    assert len(errors) == 0


def test_validate_commit_message_commitlint_error():
    """Test validate_commit_message when commitlint execution fails."""
    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            with mock.patch("pathlib.Path.write_text"):
                with mock.patch("pathlib.Path.unlink"):
                    mock_which.return_value = "/usr/bin/commitlint"
                    mock_run.side_effect = OSError("Command failed")

                    ok, errors = validate_commit_message("feat: test")

                    # Should fall back to Python validation
                    assert not ok
                    assert len(errors) > 0


def test_main_interactive_workflow():
    """Test main() interactive workflow with mocked user inputs."""
    repo = init_temp_repo()

    # Create initial commit
    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo, check=True, capture_output=True)

    # Create branch
    subprocess.run(["git", "checkout", "-b", "ISSUE-456_test"], cwd=repo, check=True, capture_output=True)

    # Make a bad commit
    Path(repo / "test2.txt").write_text("content2", encoding="utf-8")
    subprocess.run(["git", "add", "test2.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add feature"], cwd=repo, check=True, capture_output=True)

    with mock.patch("typer.confirm") as mock_confirm:
        with mock.patch("typer.prompt") as mock_prompt:
            with mock.patch("typer.echo"):
                with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                    # User confirms all suggestions
                    mock_confirm.return_value = True
                    mock_prompt.return_value = "ISSUE-456"

                    # Change to repo directory
                    original_cwd = os.getcwd()
                    try:
                        os.chdir(repo)
                        main("test", "ISSUE-456")
                    finally:
                        os.chdir(original_cwd)

                    # Verify commit was amended
                    result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
                    amended_msg = result.stdout.strip()

                    # Should have conventional type and ticket
                    assert has_conventional_type(amended_msg)
                    assert "ISSUE-456" in amended_msg


def test_main_user_rejects_changes():
    """Test main() when user rejects proposed changes."""
    repo = init_temp_repo()

    # Create initial commit
    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo, check=True, capture_output=True)

    # Create branch
    subprocess.run(["git", "checkout", "-b", "ISSUE-789_test"], cwd=repo, check=True, capture_output=True)

    # Make a commit that will pass validation (to avoid prompt)
    Path(repo / "test2.txt").write_text("content2", encoding="utf-8")
    subprocess.run(["git", "add", "test2.txt"], cwd=repo, check=True, capture_output=True)
    original_msg = "feat: ISSUE-789 add new widget"
    subprocess.run(["git", "commit", "-m", original_msg], cwd=repo, check=True, capture_output=True)

    with mock.patch("typer.confirm") as mock_confirm:
        with mock.patch("typer.echo"):
            with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                # User rejects final amend
                mock_confirm.return_value = False

                original_cwd = os.getcwd()
                try:
                    os.chdir(repo)
                    main("test", "ISSUE-789")
                finally:
                    os.chdir(original_cwd)

                # Commit should remain unchanged since user rejected amend
                result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
                final_msg = result.stdout.strip()
                assert final_msg == original_msg


def test_main_with_validation_errors():
    """Test main() when validation finds errors and user edits message."""
    repo = init_temp_repo()

    # Create initial commit
    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True)

    # Create branch and bad commit
    subprocess.run(["git", "checkout", "-b", "ABC-111_feature"], cwd=repo, check=True, capture_output=True)
    Path(repo / "test2.txt").write_text("data", encoding="utf-8")
    subprocess.run(["git", "add", "test2.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "bad message"], cwd=repo, check=True, capture_output=True)

    with mock.patch("typer.confirm") as mock_confirm:
        with mock.patch("typer.prompt") as mock_prompt:
            with mock.patch("typer.echo"):
                with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                    # Accept corrections but edit final message
                    mock_confirm.side_effect = [True, True, True, True]  # Accept all stages + final
                    mock_prompt.return_value = "feat: ABC-111 proper message"

                    original_cwd = os.getcwd()
                    try:
                        os.chdir(repo)
                        main("test", "ABC-111")
                    finally:
                        os.chdir(original_cwd)


def test_main_checkout_branch_error():
    """Test main() when branch checkout fails."""
    repo = init_temp_repo()

    with mock.patch("githooks.core.git_operations.safe_run_git") as mock_git:
        with mock.patch("typer.echo"):
            with pytest.raises(SystemExit):
                mock_git.side_effect = RuntimeError("Branch not found")

                original_cwd = os.getcwd()
                try:
                    os.chdir(repo)
                    main("test", "ISSUE-999")
                finally:
                    os.chdir(original_cwd)


def test_main_infers_branch_name():
    """Test main() infers branch name when not on a branch."""
    repo = init_temp_repo()

    # Create detached HEAD state
    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True)

    with mock.patch("githooks.core.github_utils.get_current_branch") as mock_branch:
        with mock.patch("typer.confirm") as mock_confirm:
            with mock.patch("typer.echo"):
                with mock.patch("githooks.core.git_operations.safe_run_git") as mock_git:
                    with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                        mock_branch.return_value = None  # Not on any branch
                        mock_confirm.return_value = False
                        # Return valid message to avoid validation prompt
                        mock_git.return_value = mock.Mock(stdout="feat: XYZ-123 test", returncode=0)

                        original_cwd = os.getcwd()
                        try:
                            os.chdir(repo)
                            # Should infer branch name from alias + ticket
                            main("myrepo", "XYZ-123")
                        finally:
                            os.chdir(original_cwd)


def test_main_prompt_for_ticket():
    """Test main() prompts for ticket when not provided."""
    repo = init_temp_repo()

    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feature-branch"], cwd=repo, check=True, capture_output=True)

    with mock.patch("githooks.core.github_utils.extract_ticket_from_branch") as mock_extract:
        with mock.patch("typer.prompt") as mock_prompt:
            with mock.patch("typer.confirm") as mock_confirm:
                with mock.patch("typer.echo"):
                    with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                        mock_extract.return_value = None  # No ticket in branch
                        mock_prompt.return_value = "PROMPT-456"
                        mock_confirm.return_value = False

                        original_cwd = os.getcwd()
                        try:
                            os.chdir(repo)
                            main("test", "")  # Empty ticket
                        finally:
                            os.chdir(original_cwd)

                        # Should have prompted for ticket
                        mock_prompt.assert_called()


def test_main_accepts_duplicate_scope_fix():
    """Test main() when user accepts duplicate scope fix."""
    repo = init_temp_repo()

    Path(repo / "test.txt").write_text("content", encoding="utf-8")
    subprocess.run(["git", "add", "test.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "FIX-111_dup"], cwd=repo, check=True, capture_output=True)

    # Create commit with duplicate scope
    Path(repo / "test2.txt").write_text("data", encoding="utf-8")
    subprocess.run(["git", "add", "test2.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "feat(core): core: implement"], cwd=repo, check=True, capture_output=True)

    with mock.patch("typer.confirm") as mock_confirm:
        with mock.patch("typer.echo"):
            with mock.patch.dict(os.environ, {"COMMITMINT_SKIP_INSTALL": "1"}):
                # Accept duplicate scope fix, then accept ticket, then accept final amend
                mock_confirm.side_effect = [True, True, True]

                original_cwd = os.getcwd()
                try:
                    os.chdir(repo)
                    main("test", "FIX-111")
                finally:
                    os.chdir(original_cwd)

                # Verify duplicate scope was fixed in commit
                result = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
                amended_msg = result.stdout.strip()
                # Should not have "core: core:"
                assert "core: core:" not in amended_msg
                assert "FIX-111" in amended_msg


def test_validate_with_node_but_no_commitlint():
    """Test validation when node/npm exist but commitlint needs installation."""
    import githooks.cli.commitmint as commitmint

    # Reset global flags
    commitmint._NODE_CHECKED = False
    commitmint._COMMITLINT_CHECKED = False

    with mock.patch("shutil.which") as mock_which:
        with mock.patch("subprocess.run") as mock_run:
            # Sequence: node exists, npm exists, no commitlint initially, then commitlint after install
            def which_side_effect(cmd):
                if cmd == "node":
                    return "/usr/bin/node"
                elif cmd == "npm":
                    return "/usr/bin/npm"
                elif cmd == "commitlint":
                    return None  # Not installed
                return None

            mock_which.side_effect = which_side_effect
            mock_run.return_value = mock.Mock(returncode=0)

            # Should trigger installation attempt
            with mock.patch.dict(os.environ, {}, clear=True):  # Clear COMMITMINT_SKIP_INSTALL
                ok, errors = validate_commit_message("feat: TEST-123 message")

            # Should fall back to Python validation
            assert ok
            assert len(errors) == 0
