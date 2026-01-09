"""Debug script to test the commitmint functions."""
import subprocess
from pathlib import Path
import tempfile
from githooks.cli.commitmint import (
    has_conventional_type,
    suggest_type_header,
    ensure_ticket_in_header,
    fix_duplicate_scope,
    add_footer_if_breaking_change,
)

# Create a temp test repo
with tempfile.TemporaryDirectory() as tmpdir:
    repo = Path(tmpdir)

    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=repo, capture_output=True, check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@test.com'], cwd=repo, check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo, check=True)

    # Create a branch and add commits
    subprocess.run(['git', 'checkout', '-b', 'testbranch'], cwd=repo, check=True, capture_output=True)

    # Add test commits
    test_cases = [
        ('file1.txt', 'add authentication module'),
        ('file2.txt', 'feat(auth): add login endpoint'),
        ('file3.txt', 'fix(database): database: optimize query performance'),
        ('file4.txt', 'feat(api)!: redesign authentication flow'),
        ('file5.txt', 'refactor(utils): utils: utils: extract helper functions'),
    ]

    for filename, msg in test_cases:
        file_path = repo / filename
        file_path.write_text(f'Content for {filename}\n', encoding='utf-8')
        subprocess.run(['git', 'add', filename], cwd=repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', msg, '--no-verify'], cwd=repo, check=True, capture_output=True)

    # Now retrieve the 4th commit (feat(api)!...)
    result = subprocess.run(['git', 'log', 'HEAD~1', '-1', '--pretty=%B'], cwd=repo, check=True, capture_output=True, text=True)
    msg = result.stdout.strip()
    print(f'Original message from git: {repr(msg)}')
    print(f'Expected: {repr("feat(api)!: redesign authentication flow")}')
    print()

    # Now test the pipeline
    corrected_msg = msg
    ticket = "ISSUE-5678"

    # Type suggestion - should be skipped
    print(f"has_conventional_type(msg): {has_conventional_type(msg)}")
    if not has_conventional_type(msg):
        corrected_msg = suggest_type_header(msg)
        print(f"After suggest_type_header: {repr(corrected_msg)}")
    else:
        print("Skipped suggest_type_header (already has type)")

    # Duplicate scope fix - should be skipped
    print(f"\nBefore fix_duplicate_scope: {repr(corrected_msg)}")
    before_fix = corrected_msg
    corrected_msg = fix_duplicate_scope(corrected_msg)
    if corrected_msg != before_fix:
        print(f"After fix_duplicate_scope: {repr(corrected_msg)}")
    else:
        print("No change from fix_duplicate_scope")

    # Ticket insertion
    print(f"\nBefore ensure_ticket_in_header: {repr(corrected_msg)}")
    before_ticket = corrected_msg
    corrected_msg = ensure_ticket_in_header(corrected_msg, ticket)
    print(f"After ensure_ticket_in_header: {repr(corrected_msg)}")

    # Breaking change footer
    print(f"\nBefore add_footer_if_breaking_change: {repr(corrected_msg)}")
    corrected_msg = add_footer_if_breaking_change(corrected_msg, ticket)
    print(f"After add_footer_if_breaking_change: {repr(corrected_msg)}")
    print(f"Contains '{ticket} #comment': {ticket + ' #comment' in corrected_msg}")
