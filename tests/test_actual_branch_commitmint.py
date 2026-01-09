"""
Tests for commitmint on an actual Git branch with multiple bad commits.

Verifies that the commitmint correction pipeline can identify and fix various
commit message issues on a real branch with multiple commits using the actual
test-repo which is configured in global Git config.
"""

import os
import subprocess
from datetime import datetime

from githooks.cli.commitmint import (
    add_footer_if_breaking_change,
    ensure_ticket_in_header,
    extract_ticket_from_branch,
    fix_duplicate_scope,
    get_current_branch,
    has_conventional_type,
    suggest_type_header,
)
from tests.conftest import REAL_TEST_REPO_BRANCHES_URL, REAL_TEST_REPO_URL


def test_actual_branch_with_multiple_bad_commits(real_test_repo):
    """Create actual branch with multiple bad commits and verify corrections work.

    Uses the real test-repo (see REAL_TEST_REPO_URL constant).
    Creates a branch following the naming convention JT_ISSUE-1234_test_datetime,
    commits multiple files with various commit message issues, then verifies that
    the commitmint correction helpers can fix each commit message.
    """
    repo = real_test_repo

    ticket = "ISSUE-1234"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"JT_{ticket}_test_{timestamp}"

    # Create and checkout the test branch
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo, check=True, capture_output=True)

    # Verify branch was created correctly
    current_branch = get_current_branch(repo)
    assert current_branch == branch_name, f"Expected branch {branch_name}, got {current_branch}"

    # Verify ticket can be extracted from branch name
    extracted_ticket = extract_ticket_from_branch(branch_name)
    assert extracted_ticket == ticket, f"Expected ticket {ticket}, got {extracted_ticket}"

    # Create commits with various issues
    bad_commits_data = [
        # (filename, commit_message, issue_description)
        ("file1.txt", "add new feature", "Missing type and ticket"),
        ("file2.txt", "fix the bug", "Missing type and ticket"),
        ("file3.txt", "feat: add widget", "Missing ticket"),
        ("file4.txt", "fix: correct timeout", "Missing ticket"),
        ("file5.txt", "feat(core): core: implement feature", "Duplicate scope, missing ticket"),
        ("file6.txt", "fix(api): api: resolve timeout", "Duplicate scope, missing ticket"),
        ("file7.txt", "docs: update readme", "Missing ticket"),
        ("file8.txt", "feat(auth): auth: add oauth", "Duplicate scope and missing ticket"),
        ("file9.txt", "feat(api)!: change request format", "Breaking change missing footer"),
        ("file10.txt", "refactor(core)!: rewrite engine", "Breaking change missing footer"),
    ]

    # Create all commits
    for filename, msg, _ in bad_commits_data:
        file_path = repo / filename
        file_path.write_text(f"Content for {filename}\n", encoding="utf-8")
        subprocess.run(["git", "add", str(filename)], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", msg, "--no-verify"], cwd=repo, check=True, capture_output=True)

    # Verify commits were created
    result = subprocess.run(["git", "log", "--oneline", "--no-decorate"], cwd=repo, check=True, capture_output=True, text=True)
    commit_count = len([line for line in result.stdout.strip().split("\n") if line])
    assert commit_count >= len(bad_commits_data), f"Expected at least {len(bad_commits_data)} commits, got {commit_count}"

    # Now iterate through each commit and collect corrections
    corrections = {}  # Maps commit hash to corrected message
    total_commits = len(bad_commits_data)

    # Collect all corrections first
    for idx in range(total_commits):
        offset = total_commits - idx - 1

        # Get commit hash
        commit_hash = subprocess.run(
            ["git", "log", f"HEAD~{offset}", "-1", "--pretty=%H"], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()

        # Get original commit message
        result = subprocess.run(["git", "log", f"HEAD~{offset}", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
        original_msg = result.stdout.strip()

        # Apply correction pipeline
        corrected_msg = original_msg

        # Check for breaking change FIRST using original message
        is_breaking = ("!" in original_msg.split("\n")[0]) or "BREAKING CHANGE:" in original_msg

        # Stage 0: Type suggestion (only if missing type)
        if not has_conventional_type(corrected_msg):
            corrected_msg = suggest_type_header(corrected_msg)

        # Stage 1: Duplicate scope fix
        corrected_msg = fix_duplicate_scope(corrected_msg)

        # Stage 2: Ticket insertion
        corrected_msg = ensure_ticket_in_header(corrected_msg, ticket)

        # Stage 3: Breaking change footer (if needed)
        if is_breaking:
            final_msg = add_footer_if_breaking_change(corrected_msg, ticket)
        else:
            final_msg = corrected_msg

        # If message changed, store the correction
        if final_msg != original_msg:
            corrections[commit_hash] = final_msg
            print(f"  Commit {idx + 1}/{total_commits}: Will correct '{original_msg[:50]}...' -> '{final_msg[:50]}...'")

        # Validate final message has required elements
        assert has_conventional_type(final_msg), f"Commit {idx + 1} still missing conventional type: {final_msg}"
        assert ticket in final_msg, f"Commit {idx + 1} still missing ticket {ticket}: {final_msg}"

        # For breaking changes, ensure footer is present OR breaking indicator exists
        if is_breaking:
            footer_present = f"{ticket} #comment" in final_msg
            breaking_in_header = "!" in final_msg.split("\n")[0]
            assert footer_present or breaking_in_header, f"Commit {idx + 1} missing breaking change indicator: {final_msg}"

    # Apply all corrections using a single filter-branch operation
    if corrections:
        print(f"\n✓ Applying {len(corrections)} corrections using git filter-branch...")

        # Build case statement for all corrections
        case_statements = []
        for commit_hash, new_msg in corrections.items():
            case_statements.append(
                f"""
            {commit_hash})
                cat << 'COMMIT_MSG_EOF'
{new_msg}
COMMIT_MSG_EOF
                ;;"""
            )

    # Create the filter script
    filter_script = f"""#!/bin/bash
case "$GIT_COMMIT" in
{''.join(case_statements)}
            *)
                cat
                ;;
esac
"""

    # Write script to file
    script_file = repo / ".rewrite-all-msgs.sh"
    script_file.write_text(filter_script, encoding="utf-8")

    try:
        # Convert Windows path to Git Bash path format
        script_path_abs = str(script_file.absolute())
        # Convert C:\path\to\file to /c/path/to/file for Git Bash
        if script_path_abs[1:3] == ":\\":
            drive = script_path_abs[0].lower()
            path_part = script_path_abs[3:].replace("\\", "/")
            bash_path = f"/{drive}/{path_part}"
        else:
            bash_path = script_path_abs.replace("\\", "/")

        # Use filter-branch to rewrite all commits at once
        env = os.environ.copy()
        env["FILTER_BRANCH_SQUELCH_WARNING"] = "1"

        subprocess.run(
            ["git", "filter-branch", "-f", "--msg-filter", f"bash {bash_path}", f"HEAD~{total_commits}..HEAD"],
            cwd=repo,
            check=True,
            capture_output=True,
            env=env,
        )

        print(f"✓ Successfully rewrote {len(corrections)} commit messages")
    finally:
        script_file.unlink(missing_ok=True)

    # Verify that corrections were actually needed and applied
    assert len(corrections) >= 8, f"Expected at least 8 corrections, but only found {len(corrections)}"

    # Clean up filter-branch refs
    subprocess.run(["git", "update-ref", "-d", "refs/original/refs/heads/" + branch_name], cwd=repo, capture_output=True, check=False)

    # Verify the corrections stuck by re-reading all commits
    print(f"\n✓ Amended {len(corrections)} commits on branch {branch_name}")
    for idx in range(total_commits):
        offset = total_commits - idx - 1
        result = subprocess.run(["git", "log", f"HEAD~{offset}", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
        amended_msg = result.stdout.strip()
        print(f"  Commit {idx + 1}: {amended_msg.split(chr(10))[0][:80]}")  # First line only

    # Push the branch to remote so it appears on REAL_TEST_REPO_BRANCHES_URL
    # Use --force since we rewrote commit history
    try:
        subprocess.run(["git", "push", "--force", "-u", "origin", branch_name], cwd=repo, check=True, capture_output=True, timeout=30)
        print(f"\n✓ Branch '{branch_name}' pushed to {REAL_TEST_REPO_URL}")
        print(f"  View at: {REAL_TEST_REPO_BRANCHES_URL}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n⚠ Warning: Failed to push branch to remote: {e}")
        # Don't fail the test if push fails (might be auth issue)

    # Cleanup is handled by the real_test_repo fixture


def test_actual_branch_all_correction_types(real_test_repo):
    """Comprehensive test covering all correction types on actual branch.

    Uses the real test-repo (see REAL_TEST_REPO_URL constant).
    Creates a branch with commits exhibiting every type of issue that commitmint
    should fix, verifying each correction type works correctly.
    """
    repo = real_test_repo
    ticket = "ISSUE-5678"
    branch_name = f"JT_{ticket}_comprehensive_test"

    # Create and checkout branch
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo, check=True, capture_output=True)

    # Test cases with expected corrections
    test_cases = [
        {
            "file": "test_missing_type.txt",
            "original": "add authentication module",
            "should_add_type": True,
            "should_add_ticket": True,
            "should_fix_scope": False,
            "should_add_footer": False,
        },
        {
            "file": "test_missing_ticket.txt",
            "original": "feat(auth): add login endpoint",
            "should_add_type": False,
            "should_add_ticket": True,
            "should_fix_scope": False,
            "should_add_footer": False,
        },
        {
            "file": "test_duplicate_scope.txt",
            "original": "fix(database): database: optimize query performance",
            "should_add_type": False,
            "should_add_ticket": True,
            "should_fix_scope": True,
            "should_add_footer": False,
        },
        {
            "file": "test_breaking_change.txt",
            "original": "feat(api)!: redesign authentication flow",
            "should_add_type": False,
            "should_add_ticket": True,
            "should_fix_scope": False,
            "should_add_footer": True,
        },
        {
            "file": "test_complex.txt",
            "original": "refactor(utils): utils: utils: extract helper functions",
            "should_add_type": False,
            "should_add_ticket": True,
            "should_fix_scope": True,
            "should_add_footer": False,
        },
    ]

    # Create commits for each test case
    for test_case in test_cases:
        file_path = repo / test_case["file"]
        file_path.write_text(f"Test content for {test_case['file']}\n", encoding="utf-8")
        subprocess.run(["git", "add", test_case["file"]], cwd=repo, check=True, capture_output=True)
        # Use --no-verify to skip hooks that might add feat: prefix
        subprocess.run(["git", "commit", "-m", test_case["original"], "--no-verify"], cwd=repo, check=True, capture_output=True)

    # Verify each commit and actually amend them with corrections
    corrections_made = []

    for idx, test_case in enumerate(test_cases):
        offset = len(test_cases) - idx - 1

        # Get commit hash and original message
        commit_hash = subprocess.run(
            ["git", "log", f"HEAD~{offset}", "-1", "--pretty=%H"], cwd=repo, check=True, capture_output=True, text=True
        ).stdout.strip()

        result = subprocess.run(["git", "log", f"HEAD~{offset}", "-1", "--pretty=%B"], cwd=repo, check=True, capture_output=True, text=True)
        original_msg = result.stdout.strip()

        # Apply correction pipeline
        corrected_msg = original_msg

        # Type suggestion
        if test_case["should_add_type"] and not has_conventional_type(corrected_msg):
            corrected_msg = suggest_type_header(corrected_msg)
            assert has_conventional_type(corrected_msg), f"Failed to add type to: {original_msg}"

        # Duplicate scope fix
        if test_case["should_fix_scope"]:
            before_fix = corrected_msg
            corrected_msg = fix_duplicate_scope(corrected_msg)
            # Only assert if there was actually a duplicate to fix
            if "database: database:" in before_fix or "utils: utils:" in before_fix:
                assert corrected_msg != before_fix, f"Failed to fix duplicate scope in: {original_msg}"

        # Ticket insertion
        if test_case["should_add_ticket"]:
            before_ticket = corrected_msg
            corrected_msg = ensure_ticket_in_header(corrected_msg, ticket)
            assert ticket in corrected_msg, f"Failed to add ticket to: {original_msg}"
            if ticket not in before_ticket:
                assert corrected_msg != before_ticket, f"Ticket insertion didn't modify: {original_msg}"

        # Breaking change footer
        if test_case["should_add_footer"]:
            corrected_msg = add_footer_if_breaking_change(corrected_msg, ticket)
            assert f"{ticket} #comment" in corrected_msg, f"Failed to add footer to: {original_msg}"
            assert "#resolve" in corrected_msg, f"Footer missing #resolve in: {original_msg}"

        # If message changed, track it for rewriting
        if corrected_msg != original_msg:
            corrections_made.append((commit_hash, corrected_msg))

    # Apply all corrections using filter-branch
    if corrections_made:
        env = os.environ.copy()
        env["FILTER_BRANCH_SQUELCH_WARNING"] = "1"

        # Create mapping script for all commits
        rewrite_script = '#!/bin/bash\ncase "$GIT_COMMIT" in\n'
        for commit_hash, new_msg in corrections_made:
            rewrite_script += f"  {commit_hash})\n    cat << 'EOF'\n{new_msg}\nEOF\n    ;;\n"
        rewrite_script += "  *)\n    cat\n    ;;\nesac\n"

        script_file = repo / ".rewrite-all-msgs.sh"
        script_file.write_text(rewrite_script, encoding="utf-8")

        try:
            # Convert Windows path to Git Bash path format
            script_path_abs = str(script_file.absolute())
            # Convert C:\path\to\file to /c/path/to/file for Git Bash
            if script_path_abs[1:3] == ":\\":
                drive = script_path_abs[0].lower()
                path_part = script_path_abs[3:].replace("\\", "/")
                bash_path = f"/{drive}/{path_part}"
            else:
                bash_path = script_path_abs.replace("\\", "/")

            subprocess.run(
                ["git", "filter-branch", "-f", "--msg-filter", f"bash {bash_path}", "HEAD~" + str(len(test_cases)) + "..HEAD"],
                cwd=repo,
                check=True,
                capture_output=True,
                env=env,
            )
            print(f"\n✓ Amended {len(corrections_made)} commits with corrections")
        finally:
            script_file.unlink(missing_ok=True)

        # Clean up filter-branch refs
        subprocess.run(["git", "update-ref", "-d", "refs/original/refs/heads/" + branch_name], cwd=repo, capture_output=True, check=False)

    # Push the branch to remote (force push since we rewrote history)
    try:
        subprocess.run(["git", "push", "--force", "-u", "origin", branch_name], cwd=repo, check=True, capture_output=True, timeout=30)
        print(f"\n✓ Branch '{branch_name}' pushed to {REAL_TEST_REPO_URL}")
        print(f"  View at: {REAL_TEST_REPO_BRANCHES_URL}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n⚠ Warning: Failed to push branch to remote: {e}")

    # Cleanup is handled by the real_test_repo fixture


def test_actual_branch_extract_ticket_from_branch(real_test_repo):
    """Test that ticket extraction works correctly with actual branch names.

    Uses the real test-repo (see REAL_TEST_REPO_URL constant).
    """
    repo = real_test_repo

    test_branches = [
        ("JT_ISSUE-1234_test_feature", "ISSUE-1234"),
        ("JT_ABCD-5678_bug_fix", "ABCD-5678"),
        ("JT_PROJ-999_refactoring", "PROJ-999"),
    ]

    for branch_name, expected_ticket in test_branches:
        # Delete branch if it already exists (from previous test runs)
        subprocess.run(["git", "branch", "-D", branch_name], cwd=repo, capture_output=True, check=False)
        
        # Create branch from current HEAD (don't need to switch back)
        result = subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo, capture_output=True, check=False)
        if result.returncode != 0:
            print(f"\nError creating branch {branch_name}:")
            print(f"STDOUT: {result.stdout.decode()}")
            print(f"STDERR: {result.stderr.decode()}")
            raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)

        # Extract ticket
        extracted = extract_ticket_from_branch(branch_name)
        assert extracted == expected_ticket, f"Expected {expected_ticket}, got {extracted}"

    # Push all test branches to remote
    try:
        for branch_name, _ in test_branches:
            subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo, check=True, capture_output=True, timeout=30)
        print(f"\n✓ Test branches pushed to {REAL_TEST_REPO_URL}")
        print(f"  View at: {REAL_TEST_REPO_BRANCHES_URL}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n⚠ Warning: Failed to push branches to remote: {e}")

    # Cleanup is handled by the real_test_repo fixture


def test_actual_branch_get_current_branch(real_test_repo):
    """Test that get_current_branch works correctly on actual branches.

    Uses the real test-repo (see REAL_TEST_REPO_URL constant).
    """
    repo = real_test_repo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"JT_ISSUE-1234_test_{timestamp}"

    # Get the initial branch (could be main, master, or develop)
    initial_branch = get_current_branch(repo)
    assert initial_branch is not None, "Should have an initial branch"
    assert len(initial_branch) > 0, "Initial branch name should not be empty"

    # Create and switch to test branch
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo, check=True, capture_output=True)

    # Verify we're on the new branch
    current = get_current_branch(repo)
    assert current == branch_name, f"Expected {branch_name}, got {current}"

    # Push the branch to remote
    try:
        subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo, check=True, capture_output=True, timeout=30)
        print(f"\n✓ Branch '{branch_name}' pushed to {REAL_TEST_REPO_URL}")
        print(f"  View at: {REAL_TEST_REPO_BRANCHES_URL}")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"\n⚠ Warning: Failed to push branch to remote: {e}")

    # Cleanup is handled by the real_test_repo fixture
