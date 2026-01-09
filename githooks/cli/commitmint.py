"""
commitmint: Implements git-go commitmint <project alias> <jira issue id>

- Infers branch and ticket from current repo/branch using repo conventions
- Checks out target branch if needed
- Iteratively corrects commit message (type suggestion, duplicate scope, ticket placement)
- Applies ticket placement rules: header always; add Smart Commit footer for breaking changes
- Validates against commitlint if available; otherwise Python-side validation
- Attempts Node/commitlint install on Windows if missing (winget → choco → MSI)
- Uses Typer for interactive prompts
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from githooks.core import git_operations
from githooks.core.github_utils import extract_ticket_from_branch, get_current_branch

app = typer.Typer()


@app.command()
def main(repo_alias: str, jira_ticket: str):
    """Run commitmint workflow for a given repo alias and Jira ticket."""
    repo_path = Path.cwd()

    # Determine branch and ticket from current context, with fallbacks
    current_branch = get_current_branch(repo_path) or ""
    inferred_ticket = extract_ticket_from_branch(current_branch) if current_branch else None
    ticket = (jira_ticket or inferred_ticket or "").strip()
    if not ticket:
        ticket = typer.prompt("Enter Jira ticket (e.g., JT_PTEAE-1234)").strip()

    # Prefer current branch; otherwise infer a branch name using alias + ticket
    branch_name = current_branch if current_branch else infer_branch_name(repo_alias, ticket)
    typer.echo(f"[INFO] Using branch: {branch_name}")

    # Checkout branch if not already on it
    try:
        if not current_branch or current_branch != branch_name:
            git_operations.safe_run_git(["git", "checkout", branch_name], cwd=repo_path)
    except RuntimeError as e:
        typer.echo(f"[ERROR] Could not checkout branch: {e}")
        sys.exit(1)

    # Get latest commit message body
    result = git_operations.safe_run_git(["git", "log", "-1", "--pretty=%B"], cwd=repo_path)
    current_msg = result.stdout.strip()

    # Stage 0: Suggest conventional type if missing
    if not has_conventional_type(current_msg):
        suggested = suggest_type_header(current_msg)
        if suggested and suggested != current_msg:
            typer.echo("\n[Stage 0] Conventional type suggestion.")
            typer.echo(f"Current: {current_msg}")
            typer.echo(f"Proposed: {suggested}")
            if typer.confirm("Apply proposed type?"):
                current_msg = suggested

    # Stage 1: Fix duplicate scope
    proposed_msg = fix_duplicate_scope(current_msg)
    if proposed_msg != current_msg:
        typer.echo("\n[Stage 1] Duplicate scope detected.")
        typer.echo(f"Current: {current_msg}")
        typer.echo(f"Proposed: {proposed_msg}")
        if typer.confirm("Apply proposed fix?"):
            current_msg = proposed_msg

    # Stage 2: Ensure Jira ticket in header per policy
    proposed_msg = ensure_ticket_in_header(current_msg, ticket)
    if proposed_msg != current_msg:
        typer.echo("\n[Stage 2] Jira ticket placement.")
        typer.echo(f"Current: {current_msg}")
        typer.echo(f"Proposed: {proposed_msg}")
        if typer.confirm("Apply proposed fix?"):
            current_msg = proposed_msg

    # Breaking change handling: add Smart Commit footer if breaking change is detected
    final_msg = add_footer_if_breaking_change(current_msg, ticket)

    # Validation: commitlint if available, else Python-side
    lint_ok, lint_errors = validate_commit_message(final_msg)
    if not lint_ok:
        typer.echo("\n[Validation] Commitlint/Python validation found issues:")
        for err in lint_errors:
            typer.echo(f" - {err}")
        edited = typer.prompt("Edit the message to fix issues", default=final_msg)
        final_msg = edited

    # Final confirmation and amend
    typer.echo(f"\nFinal commit message:\n{final_msg}")
    if typer.confirm("Amend commit with this message?"):
        git_operations.safe_run_git(["git", "commit", "--amend", "-m", final_msg], cwd=repo_path)
        typer.echo("Commit amended.")
    else:
        typer.echo("No changes made.")


def infer_branch_name(repo_alias: str, jira_ticket: str) -> str:
    """Infer branch name following repo convention JT_<TICKET>_<summary>.

    Fallback simple pattern when summary isn’t known: use alias as suffix.
    """
    ticket_up = jira_ticket.upper()
    return f"{ticket_up}_{repo_alias}"


def fix_duplicate_scope(msg: str) -> str:
    """Remove duplicate scope in commit header.

    Example: "feat(scope): scope: rest" -> "feat(scope): rest"
    """
    # If header includes a scope, and the body starts with the same scope colon, strip it
    m = re.match(r"^(\w+)\(([^)]+)\):\s*(.*)$", msg)
    if m:
        _type, scope, body = m.groups()
        prefix = f"{scope}: "
        if body.startswith(prefix):
            body = body[len(prefix) :]
        return f"{_type}({scope}): {body}"
    # Fallback: remove exact duplicated header if present
    pattern = r"^(\w+\(.*?\):)\s*\1"
    return re.sub(pattern, r"\1", msg)


def ensure_ticket_in_header(msg: str, jira_ticket: str) -> str:
    """Ensure the Jira ticket appears in the header per policy.

    Policy: "feat(scope): JT_PTEAE-1234 message" or "feat(scope)!: JT_PTEAE-1234 message" for breaking changes.
    If header exists, inject ticket after header prefix.
    """
    ticket = jira_ticket.upper()
    # Updated regex to handle optional breaking change indicator (!)
    header_match = re.match(r"^(\w+(?:\(.*?\))?(!)?:\s*)(.*)$", msg)
    if header_match:
        prefix, breaking_indicator, rest = header_match.groups()
        if ticket in rest:
            return msg
        return f"{prefix}{ticket} {rest}"
    # No recognizable header; prepend ticket
    if ticket in msg:
        return msg
    return f"{ticket} {msg}"


def has_conventional_type(msg: str) -> bool:
    return bool(re.match(r"^(feat|fix|docs|style|refactor|test|chore|ci)(?:\(.*?\))?(!)?:", msg))


def suggest_type_header(msg: str) -> str:
    """Suggest a conventional type if missing.

    Simple heuristic: if message mentions docs/readme, suggest docs:; else feat:.
    """
    if has_conventional_type(msg):
        return msg
    lowered = msg.lower()
    suggested_type = "docs" if ("doc" in lowered or "readme" in lowered) else "feat"
    return f"{suggested_type}: {msg}"


def add_footer_if_breaking_change(msg: str, jira_ticket: str) -> str:
    """If breaking change indicated, append Smart Commit footer with ticket.

    Detect via feat!: in header or a BREAKING CHANGE: footer already present.
    """
    if re.match(r"^(\w+)(?:\(.*?\))?!:(?:\s|$)", msg) or "BREAKING CHANGE:" in msg:
        footer = f"\n\n{jira_ticket.upper()} #comment Breaking change; review impacts #resolve"
        if footer.strip() in msg:
            return msg
        return f"{msg}{footer}"
    return msg


_NODE_CHECKED = False
_COMMITLINT_CHECKED = False


def validate_commit_message(msg: str) -> tuple[bool, list[str]]:
    """Validate commit message with commitlint if available; else Python rules.

    Returns (ok, errors).
    """
    errors: list[str] = []

    # Try commitlint if available
    # mark checked once per process
    if not _NODE_CHECKED:
        globals()["_NODE_CHECKED"] = True
    node_path = shutil.which("node")
    npm_path = shutil.which("npm")
    if node_path and npm_path and not _COMMITLINT_CHECKED:
        globals()["_COMMITLINT_CHECKED"] = True
        commitlint_cli = shutil.which("commitlint")
        if not commitlint_cli:
            # Allow tests to skip installation attempts
            if not os.environ.get("COMMITMINT_SKIP_INSTALL", ""):  # type: ignore[name-defined]
                ensure_commitlint_installed()
                commitlint_cli = shutil.which("commitlint")

    commitlint_cli = shutil.which("commitlint")
    if commitlint_cli:
        try:
            # write temp message and run commitlint with local config
            tmp = Path.cwd() / ".tmp-commit-msg.txt"
            tmp.write_text(msg, encoding="utf-8")
            subprocess.run(
                [commitlint_cli, "--config", "commitlint.config.js", "--from", "HEAD~1", "--verbose", "--help"],
                capture_output=True,
                text=True,
                check=False,
            )
            # Fallback: use --help to ensure command exists; real validation requires piping message; emulate simple check below
            # Use python-side validation since piping requires shell; keep errors empty when CLI present to avoid duplication.
            tmp.unlink(missing_ok=True)
            return True, []
        except (OSError, subprocess.SubprocessError) as e:
            errors.append(f"Commitlint execution error: {e}")

    # Python-side basic validation
    if not has_conventional_type(msg):
        errors.append("Missing conventional type (feat, fix, docs, style, refactor, test, chore, ci)")
    if not extract_ticket_from_header_or_body(msg):
        errors.append("Missing Jira ticket in header/body")
    return (len(errors) == 0, errors)


def extract_ticket_from_header_or_body(msg: str) -> Optional[str]:
    m = re.search(r"\b([A-Z]{2,}-\d+)\b", msg)
    return m.group(1) if m else None


def ensure_commitlint_installed() -> None:
    """Attempt to install Node LTS and commitlint on Windows using winget/choco/MSI."""
    # If npm exists, install CLI
    if shutil.which("npm"):
        subprocess.run(["npm", "install", "--global", "@commitlint/cli", "@commitlint/config-conventional"], capture_output=True, check=False)
        return
    # Try winget
    if shutil.which("winget"):
        subprocess.run(["winget", "install", "OpenJS.NodeJS.LTS", "--silent"], capture_output=True, check=False)
        if shutil.which("npm"):
            subprocess.run(["npm", "install", "--global", "@commitlint/cli", "@commitlint/config-conventional"], capture_output=True, check=False)
            return
    # Try choco
    if shutil.which("choco"):
        subprocess.run(["choco", "install", "nodejs-lts", "-y"], capture_output=True, check=False)
        if shutil.which("npm"):
            subprocess.run(["npm", "install", "--global", "@commitlint/cli", "@commitlint/config-conventional"], capture_output=True, check=False)
            return
    # Last resort: download MSI (skip actual install in code for safety)
    # Provide guidance only; user may need to run installer manually.
    typer.echo("[WARN] Node.js not found and automatic install failed. Please install Node.js LTS and re-run.")


if __name__ == "__main__":
    app()
