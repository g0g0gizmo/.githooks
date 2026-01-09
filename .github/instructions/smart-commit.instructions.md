---
description: 'Jira Smart Commits - Comprehensive guidelines for generating structured, semantic commit messages with Jira integration'
applyTo: '**'
---

# Jira Smart Commits

Based on [Atlassian Smart Commits Documentation](https://confluence.atlassian.com/jirasoftwareserver0814/processing-issues-with-smart-commits-1043892464.html)

## Overview

Jira Smart Commits allow you to interact with Jira issues directly from your commit messages. Automatically:

- Add comments to issues
- Log work and time tracking
- Transition issues through workflow states
- Update multiple issues in a single commit

## Requirements

- **Jira Administrator must enable Smart Commits** for your repository (Bitbucket, GitHub, FishEye, or Crucible).
- **Your Git email must exactly match a Jira user email** with appropriate permissions.
- Issue key format: **Two or more uppercase letters, hyphen, followed by number** (e.g., `ABC-123`).
- Time tracking must be enabled on your Jira instance (for `#time` commands).
- Smart Commits are processed asynchronously—allow a few moments for changes to appear.

## Syntax

```text
<ignored text> ISSUE_KEY <ignored text> #COMMAND <optional arguments>
```

The basic structure:

- Any text before/after the issue key and command is ignored.
- Multiple commands can be used on the same line or on separate lines.
- Multiple issue keys can be specified (space or comma separated).
- A single command can span **only one line** (no carriage returns within a command).

## Supported Commands

### Comment

Add a comment to a Jira issue. Text after `#comment` becomes the comment body.

```text
ISSUE-123 #comment Fixed typo in docs
```

**Note**: The committer's email must match a Jira user with permission to comment on issues.

### Time

Log work against an issue. Supported units: `w` (weeks), `d` (days), `h` (hours), `m` (minutes). Each can be decimal.

```text
ISSUE-123 #time 2d 4h 30m Refactored module
ISSUE-123 #time 1.5h Reviewed code
ISSUE-123 #time 3w Completed feature
```

**Notes**:

- Your Jira administrator must enable time tracking.
- The comment after the time values is optional but recommended.
- The committer's email must match a Jira user with permission to log work.

### Workflow Transition

Transition an issue to a workflow state. The transition name becomes the command (e.g., `#resolve`, `#close`, `#start`, `#reopen`).

```text
ISSUE-123 #resolve All tests passing
ISSUE-123 #close Fixed bug
ISSUE-123 #start Beginning work
```

**Important**:

- Smart Commits only consider the part of a transition name BEFORE the first space.
- For ambiguous transitions (e.g., "Start Progress" vs "Start Review"), use hyphens: `#start-progress` or `#start-review`.
- Find valid transitions: Open an issue in Jira → Click "View Workflow" to see available transitions.
- A comment is automatically added without needing `#comment` when you use a transition command.

## Advanced Usage

### Multiple Commands on One Issue

```text
ISSUE-123 #comment Ready for review #resolve
```

This adds a comment and transitions the issue in a single commit.

### Multiple Issues with Single Command

Separate issue keys with whitespace or commas:

```text
ISSUE-123 ISSUE-456 ISSUE-789 #resolve
```

This resolves all three issues in one commit.

### Multiple Commands on Multiple Issues

```text
ISSUE-123 ISSUE-456 #resolve #time 1h #comment Finished
```

This applies all three actions (resolve, log time, comment) to both issues.

## Best Practices

- **Verify your Git email matches a Jira user** before assuming Smart Commits aren't working.
  - Check: `git config user.email`
  - Compare with your Jira profile email—they must match exactly.
- **Always use the correct issue key format** (e.g., `ABC-123`, not `abc-123` or `ABC123`).
- **Check available transitions** in Jira: Open an issue → Click "View Workflow".
- **Use hyphens for multi-word transitions** (e.g., `#finish-work` instead of `#finish work`).
- **Put Smart Commit commands on separate lines** after the conventional commit header for clarity.
- **Test with a simple command first** (e.g., `ISSUE-123 #comment test`) to verify Smart Commits are enabled.
- **One-line limit per command**: Do not use carriage returns within a single Smart Commit command.
- **Batch related operations**: Use multiple commands on a single line when they're part of the same logical change.

## Integration with Conventional Commits

When a Jira ticket is assigned, combine conventional commit format with Smart Commit commands:

```text
<type(scope): emoji description>
<ISSUE_KEY> #<COMMAND> <optional arguments>
```

### Example Combined Commits

**Simple feature with resolution:**

```text
feat(api): ✨ Add new endpoint
ABC-123 #resolve
```

**Feature with comment and transition:**

```text
feat(api): ✨ Add new endpoint
ABC-123 #comment Implemented and tested all scenarios #resolve
```

**Bug fix with time logging:**

```text
fix(auth): 🐛 Fix login timeout issue
ABC-124 #time 2h 30m Fixed concurrent session bug #resolve
```

**Multiple issues, multiple commands:**

```text
fix(core): 🐛 Fix data race condition
ABC-123 ABC-124 #time 1h #comment Fixed in both services #resolve
```

**Refactoring with documentation:**

```text
refactor(utils): ♻️ Extract shared utility functions
ABC-125 #comment Moved to common module #resolve
```

## Troubleshooting

### Smart Commits Not Working?

**Email Mismatch** (Most Common)

- Your Git email doesn't match any Jira user.
- Fix: `git config user.email "your.email@company.com"`
- Verify in Jira: Profile → Email

**Insufficient Permissions**

- Your Jira user lacks permission to comment, log time, or transition issues.
- Fix: Request permission from your Jira project administrator.

**Issue Key Format Error**

- Invalid format: `abc-123`, `ABC123`, or `ABC-123a`
- Correct format: `ABC-123` (uppercase letters, hyphen, number)

**Smart Commits Not Enabled**

- Repository hasn't been configured for Smart Commits.
- Fix: Jira Admin → Administration → Applications → Accounts → Enable for your repository.

**Time Tracking Disabled**

- Your Jira administrator hasn't enabled time tracking.
- Fix: Jira Admin → System → Time Tracking → Enable

**Asynchronous Processing**

- Smart Commits are processed in the background—not instant.
- Fix: Wait a few moments and refresh the Jira issue.

**Check for Failure Notifications**

- Jira sends email notifications if Smart Commits fail.
- Check your email (sent to committer's email or Jira user email).

## Supported Platforms

- Bitbucket Server
- Bitbucket Cloud
- GitHub
- FishEye
- Crucible

## References

- [Jira Smart Commits Documentation](https://confluence.atlassian.com/jirasoftwareserver0814/processing-issues-with-smart-commits-1043892464.html)
- [Logging Work on Issues](https://confluence.atlassian.com/jirasoftwareserver0814/logging-work-on-issues-1043892947.html)
- [Transitioning an Issue](https://confluence.atlassian.com/jirasoftwareserver0814/transitioning-an-issue-1043892466.html)
