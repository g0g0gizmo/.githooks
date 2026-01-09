# JIRA Integration Guide

Complete documentation for JIRA automation in Git hooks, covering configuration, workflows, and best practices to minimize development overhead.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup & Configuration](#setup--configuration)
- [Workflow Automation](#workflow-automation)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Overview

This Git hooks library provides **automatic JIRA synchronization** at critical workflow points:

- **Branch creation** → Transition issue to "In Progress", log work
- **Code push** → Log work, transition to "Under Review"
- **Merge to main** → Transition to "Done", log final time

**Result:** Eliminate manual JIRA updates, maintain accurate time tracking, keep team visibility in real-time.

### Time Savings Example

| Manual Process                              | Automated Process      | Saved           |
| ------------------------------------------- | ---------------------- | --------------- |
| Type ticket → Transition → Log time (5 min) | Automatic on git event | 5 min/start     |
| Update status when pushing (3 min)          | Automatic on pre-push  | 3 min/push      |
| Mark as done after merge (2 min)            | Automatic on merge     | 2 min/merge     |
| **Per 5-PR week**                           | **~1.25 hours**        | **~1.25 hours** |

---

## Architecture

### Hooks Involved

| Hook                                               | Trigger       | JIRA Action                     |
| -------------------------------------------------- | ------------- | ------------------------------- |
| `post-checkout/jira-transition-worklog.hook`       | Branch switch | Transition + log work           |
| `pre-push/jira-add-push-worklog.hook`              | Before push   | Log work + transition to review |
| `post-commit/autoversion-conventional-commit.hook` | After merge   | Record final work               |

### Authentication Flow

```text
1. Check environment variables (JIRA_USERNAME, JIRA_TOKEN)
   ↓
2. Fall back to keyring storage (secure credential caching)
   ↓
3. Prompt user on first execution
   ↓
4. Create JIRA client with basic_auth
```

**Key Point:** Credentials are stored securely in OS keyring, not in git config.

### State Transitions

```text
START (git-go start)
  └─→ [Branch created]
      └─→ [post-checkout hook fires]
          └─→ Transition: ? → "In Progress"
          └─→ Log: 5m work
          └─→ Add comment: "Started work on branch-name"

DEVELOPMENT
  └─→ [Commits made]
      └─→ [Conventional commit messages enforced]

PUSH (git push)
  └─→ [pre-push hook fires]
      └─→ Log: 2m work (overhead tracking)
      └─→ Transition: "In Progress" → "Code Review"
      └─→ Add comment: "Pushed for review from branch-name"

REVIEW
  └─→ [PR created - GitHub automation]
      └─→ [Linked to JIRA issue]
      └─→ [Reviewers assigned]

MERGE (git-go publish)
  └─→ [post-commit hook fires]
      └─→ Log: 1m work (merge ceremony)
      └─→ Transition: "Code Review" → "Done"
      └─→ Add comment: "Merged to main"

COMPLETE
  └─→ [Issue closed]
      └─→ [Time logged: ~8m total]
```

---

## Setup & Configuration

### Prerequisites

1. **JIRA Cloud account** with API token access
2. **Git 2.0+** with hooks installed via `python install.py`
3. **Python 3.9+** with jira, keyring packages

### Step 1: Install Hooks

```bash
cd /path/to/your/repo
python /path/to/githooks/install.py
```

Verifies:

- `.git/hooks/` populated with dispatcher hooks
- Dispatcher scripts created for each hook type
- Dependencies installed in your Python environment

### Step 2: Configure JIRA Connection

```bash
# Enable JIRA automation (required)
git config hooks.jira.enabled true

# Set JIRA instance
git config hooks.jira.url "https://your-org.atlassian.net"

# Optional: Set username (or prompted on first use)
git config hooks.jira.username "your.email@company.com"
```

### Step 3: Provide Credentials

Three ways to authenticate:

**Option A: Environment Variables (CI/CD, automated)**

```bash
export JIRA_USERNAME="your.email@company.com"
export JIRA_TOKEN="your_api_token"  # From JIRA > Settings > API tokens
export JIRA_SERVER="https://your-org.atlassian.net"
```

**Option B: OS Keyring (Interactive, secure)**

Credentials stored in Windows Credential Manager / macOS Keychain / Linux pass:

```bash
# First hook execution prompts for password
git-go start myproject JT_PTEAE-2930
# → Prompts: Enter Jira password: [hidden input]
# → Saves to keyring automatically
```

#### Option C: Git Config (Not recommended for passwords)

```bash
# Username OK in git config
git config hooks.jira.username "your.email@company.com"

# Token should NOT be stored here (use env var instead)
```

### Step 4: Verify Setup

```bash
# Test JIRA connection
python -c "
from jira import JIRA
import os
jira = JIRA(server=os.getenv('JIRA_SERVER'), basic_auth=(
    os.getenv('JIRA_USERNAME'),
    os.getenv('JIRA_TOKEN')
))
print('✓ Connected to JIRA')
print(f'✓ Logged in as: {jira.current_user()}')
"

# Verify hooks are active
ls -la .git/hooks/post-checkout
# Should be executable dispatcher hook
```

---

## Workflow Automation

### Automatic Issue Transitions

The hooks search for JIRA workflow transitions containing specific keywords:

#### Start Workflow (post-checkout)

Searches for transitions in this order:

1. Contains "progress" → "In Progress", "Development", "In Development"
2. Contains "open" → "Open", "Reopened"
3. Skip if none found (non-blocking)

**Example JIRA Workflows That Work:**

- ✅ "To Do" → "In Progress" → "Code Review" → "Done"
- ✅ "Backlog" → "Development" → "In Review" → "Resolved"
- ✅ "New" → "In Development" → "Peer Review" → "Closed"

#### Push Workflow (pre-push)

Searches for transitions containing:

1. "review" → "Under Review", "Code Review", "In Review", "Peer Review", "Reviewing"
2. Skip if none found (non-blocking)

#### Merge Workflow (post-commit)

Searches for transitions containing:

1. "done" → "Done", "Completed", "Resolved"
2. "closed" → "Closed"
3. Skip if none found (non-blocking)

### Customizing Transitions

If your JIRA workflow uses different state names:

```bash
# Override automatic detection
git config hooks.jira.transition.start "Development"      # Instead of "In Progress"
git config hooks.jira.transition.review "Peer Review"     # Instead of "Code Review"
git config hooks.jira.transition.done "Resolved"          # Instead of "Done"
```

### Work Logging Configuration

Fine-tune how time is logged:

```bash
# Time logged at each stage (default: 5m, 2m, 1m)
git config hooks.jira.worklog.start "5m"      # Branch creation
git config hooks.jira.worklog.push "2m"       # Push for review
git config hooks.jira.worklog.merge "1m"      # Merge to main

# Disable work logging entirely
git config hooks.jira.worklog.enabled false

# Set global defaults (applied to all repos)
git config --global hooks.jira.worklog.start "10m"
```

### Per-Project Configuration

Different projects may have different JIRA instances or workflows:

```bash
# Switch to project A
cd /path/to/project-a
git config --local hooks.jira.url "https://org-a.atlassian.net"
git config --local hooks.jira.transition.start "In Progress"

# Switch to project B
cd /path/to/project-b
git config --local hooks.jira.url "https://org-b.atlassian.net"
git config --local hooks.jira.transition.start "Development"

# View what's applied (shows precedence)
git config --show-origin hooks.jira.url
```

---

## Workflow Automation

### Full Lifecycle Example

```bash
# ============ MONDAY: Start Feature ============
git-go start myproject JT_PTEAE-2930

# Post-checkout hook executes:
# ✓ Created branch: JT_PTEAE-2930_user-authentication
# ✓ JT_PTEAE-2930: Transitioned to 'In Progress'
# ✓ JT_PTEAE-2930: Logged 5m work
# ✓ Comment added: "Started work on JT_PTEAE-2930_user-authentication"

# ============ WEDNESDAY: Push for Review ============
git commit -m "feat(auth): implement OAuth provider support"
git push origin JT_PTEAE-2930_user-authentication

# Pre-push hook executes:
# ✓ JT_PTEAE-2930: Logged 2m work
# ✓ JT_PTEAE-2930: Transitioned to 'Code Review'
# ✓ Comment added: "Pushed code from JT_PTEAE-2930_user-authentication for review"

# ============ THURSDAY: PR Approved ============
# [Manual: Reviewer approves PR on GitHub]
# [Manual: You click "Merge" button]

# Post-commit hook executes:
# ✓ JT_PTEAE-2930: Logged 1m work
# ✓ JT_PTEAE-2930: Transitioned to 'Done'
# ✓ Comment added: "Merged to main"
# ✓ Branch deleted (local + remote)

echo "====== JIRA Summary ======"
# Total time logged: 8 minutes
# Status: Done
# Completed by: Automation
```

### What's Tracked in JIRA

Each automation step adds a worklog comment:

```text
Worklog History for JT_PTEAE-2930:

[5m] 09:00 AM - "Started work on JT_PTEAE-2930_user-authentication"
[2m] 02:30 PM - "Pushed code from JT_PTEAE-2930_user-authentication for review"
[1m] 04:15 PM - "Merged to main"

Total Time: 8m
Status: Done
```

---

## Troubleshooting

### Issue: Hook Not Running

**Symptom:** Branch created but JIRA not updated.

**Diagnosis:**

```bash
# Check if hooks are installed
ls -la .git/hooks/ | grep post-checkout

# Check if hook is executable
chmod +x .git/hooks/post-checkout

# Test hook manually
python3 .git/hooks/post-checkout manual
```

**Solution:**

```bash
# Reinstall hooks
python /path/to/githooks/install.py --force

# Or make executable manually
chmod +x .git/hooks/post-checkout
chmod +x .git/hooks/pre-push
```

### Issue: "JIRA transition failed - not allowed"

**Symptom:**

```text
[WARNING] JT_PTEAE-2930: Failed to transition: Transition not found
```

**Cause:** Transition doesn't exist in your JIRA workflow.

**Solution:**

```bash
# View available transitions in your workflow
git config hooks.jira.debug true  # Enable debug output
git push  # Watch what transitions are available

# Customize based on your workflow
git config hooks.jira.transition.push "Peer Review"
git config hooks.jira.transition.done "Resolved"

# Or disable automatic transitions
git config hooks.jira.autoTransition false
```

### Issue: "Authentication failed"

**Symptom:**

```text
[ERROR] Failed to create Jira client: Invalid username, password, or token
```

**Causes:**

- Expired API token
- Wrong JIRA instance URL
- Credentials stored incorrectly

**Solution:**

```bash
# Check your config
git config --get-regexp hooks.jira

# Test authentication manually
python3 -c "
from jira import JIRA
import os
try:
    jira = JIRA(
        server='https://your-org.atlassian.net',
        basic_auth=('your.email@company.com', 'YOUR_TOKEN')
    )
    print('✓ Auth OK')
except Exception as e:
    print(f'✗ Auth failed: {e}')
"

# Clear cached credentials and retry
# Windows: Control Panel > Credential Manager > Remove "gojira" entries
# macOS: security delete-generic-password -s gojira.jira.password
# Linux: pass rm gojira/jira/password

# Next hook will prompt for password again
git-go start myproject JT_PTEAE-2930
```

### Issue: "Time logging blocked"

**Symptom:**

```text
[WARNING] JT_PTEAE-2930: Failed to add worklog: This issue already has time logged today
```

**Cause:** Some JIRA configurations prevent multiple worklogs on the same day per user.

**Solution:**

```bash
# Option A: Increase time spent per log (log less frequently)
git config hooks.jira.worklog.push "30m"  # Skip logging for brief pushes

# Option B: Disable work logging, enable transitions only
git config hooks.jira.worklog.enabled false
git config hooks.jira.autoTransition true

# Option C: Check JIRA configuration
# Admin Settings > Issue Types > Workflows > Check worklog restrictions
```

### Issue: Wrong Transition Applied

**Symptom:** Issue transitioned to wrong state (e.g., "Testing" instead of "Code Review").

**Cause:** Keyword matching found unexpected transition.

**Solution:**

```bash
# Explicitly set the transition
git config hooks.jira.transition.review "Code Review"
git config hooks.jira.transition.done "Resolved"

# Verify config
git config --get hooks.jira.transition.review
```

### Debug Output

Enable detailed logging:

```bash
# Show all hook output
export DEBUG_HOOKS=1
git push

# Or check hook logs
tail -50 .git/hooks/post-checkout.log  # If logging enabled
```

---

## Best Practices

### 1. Branch Naming Convention

Include JIRA ticket in branch name for automatic detection:

```bash
# ✅ Good - Hook extracts ticket number
git checkout -b JT_PTEAE-2930_user-authentication

# ✅ Good - Multiple formats supported
git checkout -b feature/PROJ-123-description
git checkout -b JIRA-456/my-feature

# ❌ Bad - No ticket number, hooks skip silently
git checkout -b feature/user-auth
git checkout -b my-new-feature
```

### 2. Commit Message Format

Use conventional commits (enforced by pre-commit hooks):

```bash
# ✅ Good - Provides context for auto-classification
git commit -m "feat(auth): add OAuth support"
git commit -m "fix(login): resolve session timeout"
git commit -m "docs(readme): update installation steps"

# ❌ Bad - Rejected by commit-msg hook
git commit -m "added some stuff"
git commit -m "updated file"
```

### 3. Time Tracking Accuracy

Work logs represent **overhead tracking**, not total effort:

- **5m (start)** — Time for branch setup, hook execution
- **2m (push)** — Time for writing commit messages, pushing
- **1m (merge)** — Time for merge ceremony

**Not included (track separately if needed):**

- Actual development time (estimated in JIRA original estimate)
- Code review time (track separately as reviewer)

### 4. Credential Management

**DO:**

- ✅ Use environment variables for CI/CD
- ✅ Use OS keyring for interactive work
- ✅ Rotate API tokens regularly

**DON'T:**

- ❌ Store tokens in git config (visible in `.git/config`)
- ❌ Commit credentials to repository
- ❌ Share credentials across team members

### 5. Disable for Sensitive Branches

For hotfixes or urgent patches, temporarily disable automation:

```bash
# Cherry-pick without JIRA overhead
git config --local hooks.jira.enabled false
git-go start myproject JT_PTEAE-9999

# Re-enable when done
git config --local hooks.jira.enabled true
```

### 6. Monitor Automation

Check that automation is working:

```bash
# View recent transitions in JIRA issue
# Open issue → Activity tab → See all transitions logged with comments

# Verify hooks ran
git log --oneline -10 | grep -i "transitioned\|logged"

# Generate automation report
git config --get-regexp hooks.jira
```

### 7. Team Coordination

For team environments:

```bash
# Set team-level defaults in global config
git config --global hooks.jira.url "https://team.atlassian.net"
git config --global hooks.jira.worklog.start "5m"

# Document in README:
# "After cloning, run: python install.py"
# "First hook will prompt for JIRA credentials"

# Add to CI/CD:
# export JIRA_USERNAME="build-bot@company.com"
# export JIRA_TOKEN="ci_bot_token"
```

---

## Configuration Reference

### All JIRA Configuration Options

```bash
# Connection
hooks.jira.enabled           # true/false - Enable/disable all JIRA automation
hooks.jira.url               # https://org.atlassian.net - JIRA instance
hooks.jira.username          # your.email@company.com - JIRA username

# Transitions
hooks.jira.autoTransition    # true/false - Automatic status transitions
hooks.jira.transition.start  # "In Progress" - Custom start state
hooks.jira.transition.review # "Code Review" - Custom review state
hooks.jira.transition.done   # "Done" - Custom done state

# Work Logging
hooks.jira.worklog.enabled   # true/false - Enable work logging
hooks.jira.worklog.start     # "5m" - Time logged at start
hooks.jira.worklog.push      # "2m" - Time logged on push
hooks.jira.worklog.merge     # "1m" - Time logged on merge

# Debugging
hooks.jira.debug             # true/false - Enable debug output
hooks.jira.test              # Run connection test
```

### Environment Variables

```bash
JIRA_USERNAME      # JIRA email/username
JIRA_TOKEN         # JIRA API token (not password)
JIRA_SERVER        # https://org.atlassian.net
DEBUG_HOOKS        # Set to 1 to enable debug output
```

---

## FAQ

**Q: Can I disable automation for specific issues?**

A: Yes - remove ticket number from branch name:

```bash
git checkout -b hotfix-urgent-fix
# No ticket → hooks skip silently
```

**Q: What if my JIRA workflow is different?**

A: Customize transitions:

```bash
git config hooks.jira.transition.start "Development"
git config hooks.jira.transition.review "Peer Review"
git config hooks.jira.transition.done "Resolved"
```

**Q: Can multiple team members use same JIRA account?**

A: Not recommended - each developer should have their own JIRA account for attribution. Use CI bot account only for automated processes.

**Q: How much time should I log?**

A: Log **overhead only**, not actual development hours. Examples:

- Start: 5 minutes (branch setup, automation)
- Push: 2 minutes (commit polishing, pushing)
- Merge: 1 minute (merge ceremony)
- Total: ~8 minutes per issue regardless of development time

**Q: Can I use this with Jira Server (self-hosted)?**

A: Yes - set `hooks.jira.url` to your server URL:

```bash
git config hooks.jira.url "https://jira.company.internal"
```

Requires valid SSL certificate and network access.

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: JIRA Auto-Transition

on:
  push:
    branches: [main, develop]

jobs:
  jira:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Extract JIRA ticket
        id: ticket
        run: |
          TICKET=$(git log -1 --pretty=%B | grep -oE '[A-Z]+-[0-9]+' | head -1)
          echo "ticket=$TICKET" >> $GITHUB_OUTPUT

      - name: Transition JIRA on merge
        if: steps.ticket.outputs.ticket
        uses: atlassian/gajira-transition@v3
        with:
          issue: ${{ steps.ticket.outputs.ticket }}
          transition: "Done"
```

### Local CI (pre-push)

```bash
# In pre-push hook, add:
export JIRA_USERNAME="ci-bot@company.com"
export JIRA_TOKEN="$CI_JIRA_TOKEN"  # From environment
# Then standard hooks run automatically
```

---

## Additional Resources

- [JIRA API Documentation](https://developer.atlassian.com/cloud/jira/rest/v3/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
