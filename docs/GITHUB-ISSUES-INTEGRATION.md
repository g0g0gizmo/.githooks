# GitHub Issues Integration Guide

## Overview

The Git hooks system now supports **both JIRA and GitHub Issues** for issue tracking. The system automatically detects which tracker you're using based on your branch naming pattern.

## Supported Branch Naming Patterns

### JIRA Branches
- `JT_PTEAE-2930_feature-description`
- `PROJ-123_fix-bug`
- `feature/ABC-456`

Pattern: `[A-Z]+-\d+` (Project code + hyphen + number)

### GitHub Issue Branches
- `issue-123-description`
- `gh-123-fix-bug`
- `#123-feature`
- `123-simple-fix` (number at start)

Pattern: `(?:issue|gh|#)?-?(\d+)` (Optional prefix + number)

## Authentication

### GitHub Token Setup

The hooks need a GitHub Personal Access Token (PAT) with the following permissions:
- `repo` (full control of private repositories)
- `public_repo` (access to public repositories)

**Option 1: Environment Variable** (Recommended)
```bash
export GITHUB_TOKEN="ghp_your_token_here"
# Or
export GH_TOKEN="ghp_your_token_here"
```

**Option 2: Keyring** (Secure storage)
The hook will prompt you to enter your token and optionally save it to your system's keyring:
```bash
[INFO] GitHub token not found in environment or keyring
Enter your GitHub personal access token: ghp_xxxxx
Save token to system keyring? (y/n): y
[OK] Token saved to keyring
```

**Option 3: Interactive Prompt**
If neither environment variable nor keyring has a token, the hook will prompt you each time.

## How It Works

### 0. Git-Go Start Command (Optional)

You can use the `git-go start` command to automatically create a branch from a GitHub issue:

```bash
# Start work on GitHub issue #123
git-go start test 123
# Or with # prefix
git-go start test #123
```

The command automatically:
1. Fetches the issue details from GitHub (title, description)
2. Creates a branch: `issue-123-issue-title-formatted`
3. Pushes the branch to the remote
4. Adds the `in progress` label to the issue
5. Adds a comment: `🚀 Work started on branch 'issue-123-...'`

Output:
```
[INFO] 🚀 Starting work on GitHub issue #123 in test repository
[INFO] Issue title: Implement OAuth authentication
[INFO] Branch name: issue-123-implement-oauth-authentication
[OK] Added label 'in progress' to issue #123
[OK] Added comment to issue #123
[OK] ✅ Success! You're ready to work on #123
[INFO]    Repository: /path/to/repo
[INFO]    Branch: issue-123-implement-oauth-authentication
[INFO]    GitHub Issue: https://github.com/owner/repo/issues/123
```

**For JIRA tickets**, use the existing format:
```bash
git-go start test PROJ-123
```

### 1. Post-Checkout Hook (Automatic)

When you switch to a branch with a GitHub issue:
```bash
git checkout issue-123-implement-feature
```

The hook automatically:
1. Detects it's a GitHub issue branch
2. Parses issue number: `#123`
3. Adds the `in progress` label to the issue
4. Adds a comment: `🚀 Work started on branch 'issue-123-implement-feature'`

Output:
```
[INFO] Detected GitHub issue: #123
[OK] Added label 'in progress' to issue #123
[OK] Added comment to issue #123
[OK] #123: Transitioned to 'in progress'
```

### 2. Pre-Push Hook (Automatic)

When you push code from a GitHub issue branch:
```bash
git push origin issue-123-implement-feature
```

The hook automatically:
1. Detects it's a GitHub issue branch
2. Removes the `in progress` label (if present)
3. Adds the `in review` label
4. Adds a comment: `🔍 Code pushed for review from branch 'issue-123-implement-feature'`

Output:
```
[INFO] Detected GitHub issue: #123
[OK] Added label 'in review' to issue #123
[OK] Added comment to issue #123
[OK] #123: Transitioned to 'in review'
```

### 3. Commit Message Validation (Automatic)

The `enforce-insert-issue-number.hook` validates that your commit messages contain the issue reference:

For GitHub issues:
```bash
# ✅ Valid commit messages
git commit -m "feat: Add login feature (#123)"
git commit -m "#123 - Fix authentication bug"
git commit -m "Update README for issue #123"

# ❌ Invalid (warns but doesn't block)
git commit -m "Add login feature"
```

Output:
```
commit-msg: Detected GitHub issue branch #123
commit-msg: WARNING! The commit message should contain '#123'
```

## Example Workflows

### Workflow 1: Simple Bug Fix

```bash
# 1. Create branch from GitHub issue #42
git checkout -b 42-fix-login-timeout

# Hook automatically:
# - Detects GitHub issue #42
# - Adds 'in progress' label
# - Comments on issue

# 2. Make changes
git add .
git commit -m "fix: Increase login timeout (#42)"

# 3. Push for review
git push origin 42-fix-login-timeout

# Hook automatically:
# - Removes 'in progress' label
# - Adds 'in review' label
# - Comments on issue

# 4. Create Pull Request (manual)
# Link PR to issue: "Closes #42" in PR description
```

### Workflow 2: Feature Implementation

```bash
# 1. Create feature branch
git checkout -b issue-123-implement-oauth

# Hook: Adds 'in progress' label to #123

# 2. Multiple commits
git commit -m "feat: Add OAuth provider interface (#123)"
git commit -m "feat: Implement Google OAuth (#123)"
git commit -m "test: Add OAuth tests (#123)"

# 3. Push for review
git push origin issue-123-implement-oauth

# Hook: Transitions to 'in review'

# 4. PR merged, close issue manually or via "Closes #123" in PR
```

### Workflow 3: Multiple Issues in One Branch (Not Recommended)

```bash
# Branch focused on one primary issue
git checkout -b 456-refactor-auth

# Mention related issues in commit messages
git commit -m "refactor: Simplify auth flow (#456)"
git commit -m "fix: Also fixes timing issue from #123 (#456)"

# Primary issue #456 gets automatic updates
# Related issue #123 mentioned but not automatically updated
```

## Configuration

### Repository Setup

The hooks need to know your repository owner and name. They automatically parse this from your Git remote:

```bash
# Check your remote URL
git remote -v
# origin  https://github.com/username/repo.git (fetch)

# Or for SSH:
# origin  git@github.com:username/repo.git (fetch)
```

The hooks parse `username/repo` from the URL automatically.

### Custom Labels

By default, the hooks use these labels:
- `in progress` - Work started
- `in review` - Code pushed for review

These labels are created automatically if they don't exist in your repository.

To customize labels, you can modify:
- `githooks/core/github_issues.py` - Functions `transition_to_in_progress` and `transition_to_review`

## Troubleshooting

### Issue: "Failed to authenticate with GitHub"

**Solution**: Check your GitHub token:
```bash
# Verify token is set
echo $GITHUB_TOKEN

# Test token manually
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### Issue: "Could not determine Git remote URL"

**Solution**: Ensure you have a remote configured:
```bash
git remote -v

# If no remote:
git remote add origin https://github.com/username/repo.git
```

### Issue: Hook runs but doesn't update issue

**Solution**: Check your token has correct permissions:
- Go to GitHub → Settings → Developer settings → Personal access tokens
- Token needs `repo` scope for private repos or `public_repo` for public repos

### Issue: "Failed to fetch issue #123"

**Solution**:
- Verify the issue exists: `https://github.com/owner/repo/issues/123`
- Check you have access to the repository
- Ensure issue number is correct in branch name

## Disabling GitHub Issue Hooks

If you want to use JIRA only (or disable automatic issue updates), rename the hooks:

```bash
# Disable post-checkout GitHub integration
mv post-checkout/jira-transition-worklog.hook post-checkout/jira-transition-worklog.hook.disabled

# Disable pre-push GitHub integration
mv pre-push/jira-add-push-worklog.hook pre-push/jira-add-push-worklog.hook.disabled
```

The dispatcher automatically skips `.disabled` files.

## Comparison: JIRA vs GitHub Issues

| Feature        | JIRA                                        | GitHub Issues                                        |
| -------------- | ------------------------------------------- | ---------------------------------------------------- |
| Branch Pattern | `PROJ-123_description`                      | `issue-123-description`, `gh-123`, `123-description` |
| Authentication | JIRA username + API token                   | GitHub Personal Access Token                         |
| Work Logging   | Yes (time tracking)                         | No (only comments + labels)                          |
| Transitions    | Workflow states (In Progress, Review, Done) | Labels (`in progress`, `in review`)                  |
| Issue Fetching | Full issue details via API                  | Issue title, body, state, labels via API             |
| Comments       | Added automatically                         | Added automatically                                  |

## Best Practices

1. **Branch Naming**: Use descriptive names after the issue number:
   - ✅ `123-fix-login-timeout`
   - ✅ `issue-456-refactor-authentication`
   - ❌ `123` (too short, not descriptive)

2. **Commit Messages**: Always include issue reference:
   - ✅ `feat: Add OAuth support (#123)`
   - ✅ `#123 - Fix authentication bug`

3. **Issue Closing**: Use PR descriptions to auto-close:
   - Add `Closes #123` or `Fixes #456` in PR body
   - Issue closes automatically when PR merges

4. **Token Security**: Never commit tokens to Git:
   - Use environment variables
   - Use keyring for local storage
   - Add `.env` to `.gitignore`

## API Reference

See [API.md](API.md) for detailed function signatures:

- `githooks.core.issue_tracker.detect_issue_tracker(branch_name: str) -> str`
- `githooks.core.issue_tracker.parse_issue_from_branch(branch_name: str) -> Tuple`
- `githooks.core.github_issues.get_issue(owner: str, repo: str, number: int) -> Dict`
- `githooks.core.github_issues.add_comment(owner: str, repo: str, number: int, comment: str) -> bool`
- `githooks.core.github_issues.transition_to_in_progress(owner: str, repo: str, number: int, branch: str) -> bool`
- `githooks.core.github_issues.transition_to_review(owner: str, repo: str, number: int, branch: str) -> bool`

## FAQ

**Q: Can I use both JIRA and GitHub Issues in the same repository?**
A: Yes! The hooks automatically detect which system each branch uses based on the branch name pattern.

**Q: Do I need to create labels manually?**
A: No, the hooks will create `in progress` and `in review` labels automatically if they don't exist.

**Q: What if I don't want automatic issue updates?**
A: Rename the hook files to `.disabled` to disable them, or remove the hooks from `.git/hooks/`.

**Q: Can I customize the comments added to issues?**
A: Yes, edit the `transition_to_in_progress` and `transition_to_review` functions in `githooks/core/github_issues.py`.

**Q: Does this work with GitHub Enterprise?**
A: Yes, as long as your GitHub Enterprise instance uses the standard GitHub API.

## Next Steps

- [Installation Guide](INSTALL-GUIDE.md) - Install hooks in your repository
- [API Documentation](API.md) - Detailed API reference
- [JIRA Integration](JIRA-INTEGRATION.md) - JIRA-specific configuration
