---
description: Guidelines for creating GitHub Pull Requests in this repository
applyTo: '**'
---

# Pull Request Guidelines

This document provides instructions for creating well-structured Pull Requests (PRs) that follow the repository's conventions.

## PR Template Structure

All PRs must follow the template defined below:

```markdown
# [JIRA_TICKET](https://jira.viasat.com/browse/JIRA_TICKET) / #{github_issue}


## Description

[Detailed description of changes]

# Test Steps

1. Step one
2. Step two
3. Step three


```

## Branch Naming Convention

Branches must follow the format: `JT_PTEAE-0000_short-description`

**Components:**

- `JT_PTEAE-0000`: Jira ticket number (exact format from Jira)
- `_`: Underscore separator
- `short-description`: Brief hyphen-separated description of the work

**Examples:**

- `JT_PTEAE-2930_automatic-sw-versioning`
- `JT_PTEAE-1234_fix-git-integration`
- `JT_PTEAE-5678_add-changelog-generation`

## PR Description File

Before creating a PR on GitHub, generate a description file:

1. **Filename format**: Use the branch name with `.md` extension
   - Example: `JT_PTEAE-2930_automatic-sw-versioning.md`

2. **Location**: Save in the repository root directory

3. **Content**: Must include:
   - Jira ticket link in header
   - GitHub issue reference (if applicable, otherwise leave blank)
   - Detailed description of changes
   - Numbered, actionable test steps for reviewers

## Creating the PR Description

### Automatic Generation

Use the prompt file at `.github/prompts/pull-request.prompt.md` with GitHub Copilot or AI assistants to automatically generate the PR description file.

### Manual Creation

If creating manually, ensure:

1. **Jira Ticket Reference**:
   - Extract ticket number from branch name
   - Create clickable link: `[JT_PTEAE-2930](https://jira.viasat.com/browse/JT_PTEAE-2930)`

2. **GitHub Issue Reference**:
   - Include if related: `#{issue_number}`
   - Leave blank if none: `#`

3. **Test Steps**:
   - Numbered list (1, 2, 3...)
   - Each step should be specific and actionable
   - Include commands where applicable
   - Verify steps actually test the changes made

4. **Description**:
   - Concise summary of what changed and why
   - Key changes as bulleted list
   - Technical details section if needed
   - Explain impact on existing functionality

## Test Steps Best Practices

Good test steps are:

- **Specific**: "Run `pytest tests`" not "Run tests"
- **Ordered**: Follow logical progression from setup to verification
- **Verifiable**: Clear success/failure criteria
- **Relevant**: Directly related to PR changes

**Example**:

```markdown
1. **Verify backward compatibility:**
   ```bash
   python -c "from bumpy import read_current_version; print('OK')"
   ```

2. **Run the full test suite:**

   ```bash
   pytest tests/ -v
   ```

3. **Test CLI functionality:**

   ```bash
   bumpy --help
   ```

```

## Commit Messages in PRs

All commits in the branch should follow conventional commit format:

- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `feat!:` or `BREAKING CHANGE:` - Breaking changes (major version bump)
- `docs:`, `style:`, `refactor:`, `test:`, `ci:`, `chore:` - No version bump

See `docs/COMMITS.md` for detailed commit guidelines.

## PR Checklist

Before submitting:

- [ ] Branch name follows `JT_PTEAE-0000_short-description` format
- [ ] PR description file created (`JT_PTEAE-0000_short-description.md`)
- [ ] Jira ticket linked in description
- [ ] Test steps are clear and actionable
- [ ] All commits follow conventional commit format
- [ ] Tests pass locally (`pytest tests/`)
- [ ] Code follows project style (Black + isort)
- [ ] Documentation updated if needed

## Workflow Integration

PRs trigger automatic validation:

1. **Commit validation**: Checks conventional commit format
2. **Test execution**: Runs full test suite
3. **Version analysis**: Calculates version bump based on commits
4. **Release automation**: Creates release on merge to main (if applicable)

See `.github/workflows/semantic-version.yml` for details.

## Common Issues

### Missing Jira Ticket in Branch Name

**Problem**: Branch named `fix-bug` instead of `JT_PTEAE-1234_fix-bug`

**Solution**: Rename branch or create new branch with correct format:
```bash
git checkout -b JT_PTEAE-1234_fix-bug
git push origin JT_PTEAE-1234_fix-bug
```

### Vague Test Steps

**Problem**: "Test the changes"

**Solution**: Be specific:

```markdown
1. Install updated package: `pip install -e .`
2. Run specific test: `pytest tests/test_new_feature.py -v`
3. Verify output contains "SUCCESS"
```

### Missing Description Context

**Problem**: "Fixed bug"

**Solution**: Explain what, why, and how:

```markdown
Fixed race condition in version file reading that caused intermittent
test failures. Added file locking mechanism and retry logic. Updated
tests to verify behavior under concurrent access.
```

## References

- Conventional Commits: `docs/COMMITS.md`
- Semantic Versioning: `docs/VERSIONING.md`
- Testing Guidelines: `.github/instructions/pytest.instructions.md`
- Python Style: `.github/instructions/python.instructions.md`
