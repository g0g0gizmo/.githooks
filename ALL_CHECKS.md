# All Checks Overview

This document lists everything enforced or surfaced by the Git hooks in this repository, grouped by hook stage. For each check you’ll see when it runs, what it does, whether it blocks the action, and any dependencies or notes.

Tip: Most pre-commit checks are orchestrated via the Python dispatcher. You can enable/disable individual checks by adding/removing the corresponding .hook file in the hook folder.

## Pre-commit checks (before creating a commit)

- prevent-commit-to-main-or-develop.hook
  - What: Blocks direct commits to main or develop; suggests creating a feature/issue branch.
  - Blocks: Yes
  - Notes: Runs on the current branch name.

- format-code.hook
  - What: Runs Maven formatter mvn fmt:format and re-adds changed files to the index.
  - Blocks: Yes if mvn fmt:format fails; No if Maven isn’t installed (prints a skip warning)
  - Deps: Maven (mvn)

- search-term.hook
  - What: Fails if staged diff contains added lines with the term “FIXME:”.
  - Blocks: Yes on match

- spell-check-md-files.hook
  - What: Spell-checks Markdown files under the content/ directory using aspell.
  - Blocks: Yes if spelling errors are found; No if aspell is missing or content/ doesn’t exist (skips)
  - Deps: aspell
  - Notes: Only scans content/**/*.md

- verify-name-and-email.hook
  - What: Ensures git config user.name and user.email match expected values.
  - Blocks: Yes on mismatch
  - Notes: Expected values are hardcoded in the script; adjust to your identity if needed.

- prefix-commit-type-by-diff.hook
  - What: Heuristically prepends a Conventional Commit prefix (feat:, fix:, docs:, test:, chore:) into COMMIT_EDITMSG based on staged files.
  - Blocks: No

- dotenvx.hook.disabled (optional)
  - What: Pre-commit integration with dotenvx to prevent committing .env secrets.
  - Blocks: Yes (if enabled and dotenvx precommit fails)
  - Deps: Bash, dotenvx
  - Notes: Disabled by default; rename file to enable per instructions in the header.

Dispatcher files
- dispatcher.py: Python dispatcher that runs every .hook in pre-commit/ (stops on first non-zero exit).
- pre-commit.sh: Shell wrapper to invoke the dispatcher (useful for cross-env compatibility).

New hygiene and config checks
- trailing-whitespace.hook
  - What: Trims trailing spaces/tabs in staged text files and re-adds them to index.
  - Blocks: Yes (fixes in place; fails only on error)

- end-of-file-fixer.hook
  - What: Ensures files end with a single newline (POSIX-style EOL).
  - Blocks: Yes (fixes in place; fails only on error)

- mixed-line-ending.hook
  - What: Normalizes mixed CRLF/LF endings to LF in text files.
  - Blocks: Yes (fixes in place; fails only on error)
  - Notes: Honor repo policies (e.g., core.autocrlf) as needed.

- check-merge-conflict.hook
  - What: Blocks commits containing unresolved Git conflict markers (<<<<<<<, =======, >>>>>>>).
  - Blocks: Yes

- check-added-large-files.hook
  - What: Blocks newly added files larger than policy threshold (default 500KB). Suggests Git LFS.
  - Blocks: Yes
  - Notes: Adjust MAX_KB inside the hook to match policy.

- check-json.hook / check-toml.hook / check-yaml.hook
  - What: Syntax (and basic policy) checks for JSON, TOML, YAML files. YAML uses yamllint if available, otherwise PyYAML parse.
  - Blocks: Yes on invalid files

- shellcheck.hook
  - What: Runs ShellCheck on staged shell scripts using shellcheck-py (works on Windows).
  - Blocks: Yes on issues

- detect-secrets.hook
  - What: Blocks newly introduced secrets not present in the repository baseline (.secrets.baseline) using detect-secrets.
  - Blocks: Yes when new potential secrets are detected or when baseline is missing
  - Notes: Create a baseline once with `detect-secrets scan > .secrets.baseline` and audit with `detect-secrets audit .secrets.baseline`.

- warn-if-lv-hooks-missing.hook
  - What: If staged files include LabVIEW artifacts (vi/vim/ctl/lvclass/lvlib/lvproj, etc.) and LV Git Hooks are not installed, prints an install hint (non-blocking).
  - Blocks: No
  - Notes: Install LV Git Hooks with `pwsh ./install-lv-hooks.ps1`. Configure hooks in `.lv-git-hooks-config.json`.

## Prepare-commit-msg checks (before the editor opens or when message is prepared)

- insert-issue-id.hook
  - What: If no JIRA-like ID is present in the draft commit message, prepends ISSUE-0000: .
  - Blocks: No (mutates message)

- classify-commit-type-by-diff.hook
  - What: Inserts a Conventional Commit prefix with a scope derived from staged files (docs(scope):, test(scope):, feat(scope):, fix(scope):, chore(scope):) when no conventional header is present; respects a leading JIRA token.
  - Blocks: No (mutates message)

- enforce-jira-id-match-branch.hook
  - What: Enforces that a commit message’s JIRA ID matches the branch ID if the branch contains one; disallows having a JIRA ID in the message on a non-JIRA branch.
  - Special: Allows ISSUE-0000 on any branch.
  - Blocks: Yes on mismatch

## Commit-msg checks (after you finish editing the commit message)

- conventional-commitlint.hook
  - What: Runs commitlint against the message.
  - Blocks: Behavior depends on the path used in the file (the file contains both a warning-only and a strict mode). In default form, it returns commitlint’s exit code (blocking on failure); a warning-only variant is present above it.
  - Deps: Node.js + npx, @commitlint/cli, @commitlint/config-conventional

- enforce-insert-issue-number.hook
  - What: On branches named like issue-<ID>, warns if the message does not start with ISSUE-<ID>.
  - Blocks: No (warns only)

- commit-msg-jira (template)
  - What: Template for validating JIRA ID or Merge keyword; currently commented out (no effect).
  - Blocks: No (as-is)

## Pre-push checks (before pushing)

- pre-push-protect-branches
  - What: Prevents force-pushing to protected branches (master, dev, release-*, patch-*).
  - Blocks: Yes when a force/delete push to a protected branch is detected
  - Notes: Bash script; intended for environments with Bash (e.g., Git Bash).

- prevent-bad-push.hook
  - What: Rejects the push if any to-be-pushed commit message starts with WIP.
  - Blocks: Yes when detected

## Pre-rebase checks (before rebasing)

- pre-rebase-rebaselock
  - What: Blocks rebase if git config branch.<branch>.rebaselock=true.
  - Blocks: Yes (when config is set)

- prevent-rebase.hook
  - What: Prevents rebasing topic branches that have already been merged into the publish branch next (example workflow safeguard).
  - Blocks: Yes when already published to next

## Server-side checks (on remotes)

- pre-receive/pre-receive-ban-on-push-to-branch
  - What: Blocks pushes to master by certain users (example list: junior1, junior2).
  - Blocks: Yes (server-side)

- post-receive/post-receive-specific-folder
  - What: On pushes to production, deploys the branch to a target working tree and tags a release (release_YYYYMMDD-HHMM).
  - Blocks: No (runs after refs updated)

- post-update/update-server-info.hook
  - What: Runs git update-server-info for dumb HTTP transports.
  - Blocks: No (utility)

## Post-* utilities and notifications (local)

- post-commit/autoversion-conventional-commit.hook
  - What: If the last commit is a conventional feat or fix (or BREAKING CHANGE), runs standard-version (without tagging/changelog/commit) to bump versions.
  - Blocks: Yes if npx is missing or standard-version fails; otherwise prints success.
  - Deps: Node.js + npx, standard-version

LabVIEW hooks integration
- .lv-git-hooks-config.json
  - What: Local config listing hook types and LabVIEW hook IDs to install (via LV Git Hooks).
  - Notes: Default includes pre-commit and commit-msg, with lv-fmt example.
- install-lv-hooks.ps1
  - What: Installs LV Git Hooks locally using g-cli (supports --lv-only).
  - Deps: LabVIEW + g-cli on PATH (LV Venv Tools).

- post-checkout/delete-pyc-files.hook
  - What: Intended to delete .pyc files on branch checkout.
  - Blocks: No
  - Notes: The example script is Python 2–style and may require fixes to run as-is.

- post-checkout/new-branch-alert.hook
  - What: Prints a notification when a new branch is checked out for the first time.
  - Blocks: No
  - Notes: The tail of the file includes leftover shell lines; trim if enabling.

- post-rewrite/post-rewrite-move-refs
  - What: After a rewrite (e.g., rebase), updates local refs pointing to rewritten commits.
  - Blocks: No

- applypatch-msg/applypatch-msg-check-log-message
  - What: Delegates to commit-msg to validate the patch’s log message.
  - Blocks: Yes if underlying commit-msg fails

- pre-auto-gc/pre-auto-gc-battery
  - What: Defers auto GC when not on AC power on Linux/macOS.
  - Blocks: Yes (skips repacking when on battery)

## Notes and configuration

- Dispatcher behavior: The pre-commit dispatcher runs .hook files in sorted order and stops on the first failure. Reorder or disable checks by renaming/removing files.
- Environment dependencies:
  - Python 3 is required for advanced hooks and dispatcher.
  - Node.js and npx are needed for commitlint and standard-version.
  - Maven is required for format-code.hook.
  - aspell is required for spell-check-md-files.hook.
- Windows support:
  - Most Python hooks work cross-platform.
  - Some Bash scripts (pre-push-protect-branches, dotenvx.hook.disabled, server-side examples) require a Bash-compatible environment.
- Identity check:
  - verify-name-and-email.hook has EXPECTED_NAME/EXPECTED_EMAIL hardcoded; customize to your identity or remove the hook.
- JIRA and issue conventions:
  - ISSUE-0000 is allowed anywhere by enforce-jira-id-match-branch.hook.
  - prepare-commit-msg helpers can automatically insert issue IDs and Conventional Commit prefixes.

## Quick enable/disable tips

- Disable a check: rename the .hook file extension to something else or remove the file from the hook folder.
- Enable optional checks: follow the header comments inside each file (e.g., rename dotenvx.hook.disabled to pre-commit to enable dotenvx integration).
- To run only a subset: remove or move unwanted .hook files; dispatcher will run whatever remains.

## Where these live

- applypatch-msg/: patch message validation
- commit-msg/: commit message linters and JIRA rules
- prepare-commit-msg/: auto-prefixing and JIRA branch-message enforcement
- pre-commit/: dispatcher plus formatting, name/email, search-term, spell check, branch guard, etc.
- pre-push/: push-time guards (force-push protection, WIP rejection)
- pre-rebase/: rebase locks and published-branch protection
- pre-receive/: server-side branch protection examples
- post-checkout/: local maintenance/alerts
- post-commit/: automated version bump after conventional commits
- post-receive/: server-side deploy/tag example
- post-rewrite/: ref maintenance after history rewrites
- post-update/: server-info maintenance

If you add a new .hook, document it here to keep this reference accurate.
