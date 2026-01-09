
## Implementation Plan: `git-go commitmint` Command

### 1. Research & Architecture Review

- Analyze current `git-go` architecture (dispatch, Typer usage, command pattern)
- Review branch naming conventions, commit message hooks, and validation logic
- Identify reusable code in `lib/` (e.g., `git_operations.py`, `jira_client.py`)
- Confirm Typer CLI patterns and interactive prompt best practices

Anchored by prior implementations already in the repo:

- Reuse `commitmint.py` correction helpers (duplicate scope, ticket insertion) and Typer prompt style.
- Align with `prepare-commit-msg/classify-commit-type-by-diff.hook` for type suggestion logic.
- Use `lib/git_operations.py` for branch detection and commit amend subprocess wrappers.
- Use `lib/jira_client.py` to extract Jira issue keys from branch names.

### 2. Command Design & Entry Point

- Add new Typer subcommand: `commitmint <project alias> <jira issue id>`
- Validate arguments, infer branch name using Jira ticket and alias
- Document command usage and options

Design notes:

- Wire the new subcommand into `git-go` dispatch consistently with existing special-cased commands.
- Typer interaction uses `typer.prompt` and `typer.confirm` with clear current vs proposed message rendering.

### 3. Branch Operations

- Use git operations to:
  - Locate remote branch matching Jira ticket
  - Clone branch locally if needed
  - Check out branch (create if missing)
- Error handling for missing branches, checkout failures

Branch inference rules and edge cases:

- Support `feature/` and similar prefixes (e.g., `bugfix/`, `hotfix/`).
- Extract ticket keys from branch names following `JT_PTEAE-0000_short-description` format.
- Handle multi-issue branches (multiple keys present): prefer the first key, show prompt to choose if ambiguity exists.
- Fallback prompt: if extraction fails, prompt for ticket ID explicitly.

### 4. Commit Message Correction Workflow

- Stage 1: Detect duplicate scope in commit message
  - Parse latest commit message
  - Identify scope duplication (e.g., `[scope]: [scope] ...`)
  - Propose fix, show current vs. proposed message
  - Interactive prompt: user accepts or edits
- Stage 2: Detect missing Jira ticket in commit message
  - Check for Jira ticket reference in message
  - Propose fix (insert ticket in correct format)
  - Interactive prompt: user accepts or edits
- Allow iterative editing until user confirms

Stage 0 (optional, before Stage 1): Conventional type suggestion

- If commit message lacks a conventional type (e.g., `feat:`, `fix:`), suggest a type using heuristics similar to `classify-commit-type-by-diff.hook`.
- Present suggested header with type and optional scope; allow user to accept, edit, or skip.

Ticket placement rules:

- Always place the Jira ticket in the header per Option A: `feat(scope): JT_PTEAE-1234 message`.
- When a breaking change is detected (either `feat!:` or `BREAKING CHANGE:` footer intent), include both Option A and Option B: add a Smart Commit footer line with commands (e.g., `JT_PTEAE-1234 #comment Breaking change; see details #resolve`).

### 5. Typer Interactive Prompts

- Use Typer's prompt and confirm features for step-by-step correction
- Display current and proposed commit messages
- Require explicit user confirmation before amending commit

### 6. Commit Amend & Validation

- Amend commit with corrected message
- Validate message against conventional commit and Jira rules
- Show final message and result

Validation flow and commitlint integration:

- If `commitlint` is installed, validate against `commitlint.config.js` prior to amend; show errors and allow edit.
- If `commitlint` is not available, perform Python-side validation (allowed types, basic format).
- Auto-install path on Windows if Node/commitlint are missing:
  - Try `winget install OpenJS.NodeJS.LTS` (requires winget availability).
  - Fallback: `choco install nodejs-lts -y` (if Chocolatey is installed).
  - Last resort: download Node.js LTS MSI via `Invoke-WebRequest` and `Start-Process msiexec`.
  - After Node is present, run `npm install --global @commitlint/cli @commitlint/config-conventional`.
- Cache detection: check once per session for Node and commitlint presence to avoid repeated installation attempts.

### 7. Testing & Edge Cases

- Add/extend tests in `tests/` for:
  - Branch inference logic
  - Commit message correction (duplicate scope, missing Jira)
  - Interactive prompt flow
  - Error scenarios (missing branch, invalid ticket)

Additional tests:

- Type suggestion behavior when only docs or config files change.
- Breaking change scenarios: ensure both header placement and Smart Commit footer are applied.
- Commitlint optional path: simulate presence/absence and verify fallback Python validation.

### 8. Documentation & Rollout

- Update `README.md` and relevant hook READMEs
- Document new command, usage, and troubleshooting
- Plan for safe rollout and rollback

Documentation notes:

- Clarify ticket placement policy and breaking-change footer addition.
- Provide Windows commands to install Node with winget/choco and global commitlint.
- List supported branch naming formats and how ambiguity is resolved.

---

#### Anchors & Milestones

1. Research & design complete (plan, architecture, edge cases)
2. Command entry and branch operations implemented
3. Commit message correction workflow implemented
4. Interactive prompt and validation logic complete
5. Tests and documentation updated
6. End-to-end validation and rollout

#### Risks & Mitigations

- Git operations may fail on edge cases (missing branch, permissions)
- Commit message parsing may miss nonstandard formats
- User may reject all proposed fixes (allow manual edit)
- Typer prompt flow must be robust to user input errors

Additional risks:

- Node/commitlint installation may be blocked by corporate policy; mitigation: keep Python-side validation as a reliable fallback.
- Multi-issue branches can produce ambiguity; mitigation: prompt selection and remember choice for session.
- Smart Commit footers may need project-specific commands; mitigation: make footer content configurable via repo config.
