# Installing Git Hooks

This directory contains a collection of useful Git hooks. Git hooks are scripts that run automatically when certain Git events occur (like committing, pushing, etc.).

## Why aren't my hooks being called?

Git hooks must be located in the `.git/hooks` directory of your repository to work. This collection is a library of hooks that need to be installed into your actual Git repositories.

## Quick Installation

**Unified Installer (Recommended)**: We now provide a single Python-based installer with platform-specific wrappers:

```bash
# Navigate to your Git repository
cd /path/to/your/repo

# Run the installer (choose your platform)
python /path/to/.githooks/install.py              # All platforms
/path/to/.githooks/install.bat                    # Windows CMD
/path/to/.githooks/install.ps1                    # PowerShell
/path/to/.githooks/install.sh                     # Bash/Zsh
```

The installer will:

1. Install hooks with automatic dispatchers
2. Copy hook files to `.git/hooks/` (local) or `~/.git-hooks/` (global)
3. Set up dispatcher scripts to execute all `.hook` files for each hook type

**Note:** The installer uses your current Python environment. Ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

### Installation Options

**Local Installation** (single repository):

```bash
# From within your repository
python install.py
```

**Global Installation** (all repositories):

```bash
# Install hooks globally
python install.py --global
install.bat . global              # Windows CMD
install.ps1 -Global               # PowerShell
install.sh --global               # Bash/Zsh
```

**Advanced Options**:

```bash
# Force reinstall (overwrite existing hooks)
python install.py --force

# Specify repository path
python install.py --repo-path /path/to/repo

# Get help
python install.py --help
```

## Manual Installation (Advanced)

If you need manual control over which hooks are installed:

1. Navigate to your Git repository
2. Go to the `.git/hooks` directory
3. Copy the desired hook file from this collection
4. Rename it to match the exact hook name (remove any suffixes)
5. On Unix systems, make it executable with `chmod +x hookname`

### Modular Hook Architecture

Each hook type (e.g., `pre-commit`) can have multiple `.hook` files in its directory. The installer creates a dispatcher that automatically runs all `.hook` files for that hook type, allowing you to:

- Enable/disable individual hooks by adding/removing `.hook` files
- Maintain separation of concerns (one file per check)
- Easily customize your workflow

## Dependencies for Conventional Commit Hooks

To use the conventional commit enforcement and auto-versioning hooks, you need Node.js and npm installed.

Install the required tools globally (recommended):

```sh
npm install -g @commitlint/cli @commitlint/config-conventional standard-version
```

Or add them to your project as devDependencies:

```sh
npm install --save-dev @commitlint/cli @commitlint/config-conventional standard-version
```

You may also need a `commitlint.config.js` in your repo root:

```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

For more info, see https://commitlint.js.org/ and https://github.com/conventional-changelog/standard-version

## Awesome hooks and features

- **pre-commit/prevent-commit-to-main-or-develop.hook**: Prevents direct commits to `main` or `develop` branches. Enforces feature branch workflow.
- **prepare-commit-msg/classify-commit-type-by-diff.hook**: Analyzes staged changes and auto-suggests commit type (`docs:`, `test:`) if only docs or tests are changed.

## Available hooks in this collection

- **applypatch-msg**: Check log messages when applying patches
- **commit-msg**: Validate commit messages (e.g., JIRA ticket integration)
- **post-commit**: Actions after successful commits
- **post-receive**: Server-side hook after receiving pushes
- **post-rewrite**: Actions after rewriting commits
- **pre-auto-gc**: Checks before automatic garbage collection
- **pre-commit**: Validation before commits (e.g., linting, formatting)
- **pre-push**: Validation before pushes (e.g., protect branches)
- **pre-rebase**: Checks before rebasing
- **pre-receive**: Server-side validation before accepting pushes
- **prepare-commit-msg**: Modify commit messages before editing

## Important notes

1. **Hook names must be exact**: No file extensions like `.sh`, `.ps1`, etc.
2. **Location matters**: Hooks must be in `.git/hooks/` directory
3. **Permissions**: On Unix systems, hooks must be executable
4. **One hook per type**: If you need multiple actions for one hook type, combine them into a single script
5. **Testing**: Test your hooks with `git commit --dry-run` or similar commands

## Customizing hooks

Most hooks in this collection are examples that may need customization for your specific project:

- Update file paths and tool locations
- Modify validation rules
- Adjust branch names and patterns
- Configure integration with your tools (JIRA, linters, etc.)

## Troubleshooting

If hooks aren't running:

1. Check the file exists in `.git/hooks/` with the correct name
2. Verify file permissions (executable on Unix)
3. Check for syntax errors in the script
4. Test with `git --version` to ensure Git is working
5. Use `git config core.hooksPath` to check if a custom hooks directory is set
