
## Custom Git Flow

### Automated JIRA Lifecycle Tracking

Every phase of your development workflow automatically synchronizes with JIRA, eliminating manual status updates and providing real-time work tracking:

---

### `git-go start <project-name> <jira-issue-id>`

**Purpose:** Initiate development on a JIRA issue with full automation

**Automatic Actions:**

| Stage                 | Action                      | JIRA Impact             | Notes                                                  |
| --------------------- | --------------------------- | ----------------------- | ------------------------------------------------------ |
| **Branch Creation**   | Create feature branch       | Issue link updated      | Branch named: `JT_PTEAE-<id>_description`              |
| **Remote Setup**      | Track remote branch         | Remote tracking enabled | Ready for team collaboration                           |
| **JIRA Transition**   | Transition to "In Progress" | Status updated          | Searches for transition containing "progress"          |
| **Work Logging**      | Log initial 5 minutes       | Time tracked            | Default: 5m (configurable: `hooks.jira.worklog.start`) |
| **Issue Description** | Auto-populate description   | Context added           | Branch name + developer + timestamp                    |

**JIRA Transitions Attempted (in order):**

1. Search for transition with "in progress" in name
2. Fall back to "development" if available
3. Skip if not found (non-blocking)

**Configuration:**

```bash
git config hooks.jira.url "https://your-org.atlassian.net"
git config hooks.jira.worklog.start "5m"        # Time logged at start
git config hooks.jira.autoTransition true       # Enable transitions
```

**Output:**

```text
✓ Created branch: JT_PTEAE-2930_feature-name
✓ Tracking remote branch
✓ JT_PTEAE-2930: Transitioned to 'In Progress'
✓ JT_PTEAE-2930: Logged 5m work
```

---

### `git-go finish <project-name> <jira-issue-id>`

**Purpose:** Create pull request and notify reviewers with JIRA status update

**Automatic Actions:**

| Stage                   | Action                          | JIRA Impact      | Trigger                        |
| ----------------------- | ------------------------------- | ---------------- | ------------------------------ |
| **Push Attempt**        | Validate branch                 | Work logged      | `pre-push` hook fires          |
| **Work Logging**        | Log 15 minutes                  | Time tracked     | Automatic on push              |
| **JIRA Transition**     | Transition to "Code Review"     | Status updated   | Looks for "review" keywords    |
| **PR Creation**         | Create pull request             | Linked to issue  | Title includes `JT_PTEAE-<id>` |
| **Reviewer Assignment** | Auto-assign based on CODEOWNERS | Team notified    | Follows GitHub CODEOWNERS file |
| **Description**         | Generate from commit messages   | Context provided | Includes change summary        |

**JIRA Transitions Attempted (in order):**

1. "Under Review"
2. "Code Review"
3. "Peer Review"
4. "In Review"
5. Skip if none found (non-blocking)

**Hooks Involved:**

- **`pre-push/jira-add-push-worklog.hook`** — Logs work and transitions to review status
- **`commit-msg/*`** — Validates issue number in commit message
- **`prepare-commit-msg/classify-commit-type-by-diff.hook`** — Auto-classifies commit type

**Configuration:**

```bash
git config hooks.jira.worklog.finish "2m"      # Time logged before review
git config hooks.jira.autoTransition true       # Enable transitions
git config hooks.codeowners "CODEOWNERS"        # File path for reviewers
```

**Output:**

```text
✓ Pre-push: JT_PTEAE-2930: Logged 2m work
✓ Pre-push: JT_PTEAE-2930: Transitioned to 'Code Review'
✓ Pull Request created: JT_PTEAE-2930: Add feature name
✓ Reviewers assigned: @dev1, @dev2
```

---

### `git-go publish <project-name>`

**Purpose:** Merge PR, cleanup, and mark issue as complete

**Automatic Actions:**

| Stage                | Action                | JIRA Impact        | Details                           |
| -------------------- | --------------------- | ------------------ | --------------------------------- |
| **PR Merge**         | Merge to main/develop | Issue linked       | Requires approvals (configurable) |
| **Branch Cleanup**   | Delete local + remote | Refs updated       | Clean workspace                   |
| **Work Logging**     | Log 1 minute          | Final time tracked | Completion marker                 |
| **JIRA Transition**  | Transition to "Done"  | Issue closed       | Final status update               |
| **Changelog Update** | Auto-generate entry   | Release tracked    | From conventional commits         |

**JIRA Transitions Attempted (in order):**

1. "Done"
2. "Completed"
3. "Closed"
4. Skip if none found (non-blocking)

**Post-Merge Hooks:**

- **`post-commit/autoversion-conventional-commit.hook`** — Calculates version bump and generates changelog
- **JIRA worklog completion** — Records final time spent

**Configuration:**

```bash
git config hooks.jira.worklog.finish "1m"      # Time logged on merge
git config hooks.jira.autoTransition true       # Enable transitions
git config hooks.releaseNotes.auto true         # Generate changelog
```

**Output:**

```text
✓ Pull Request merged
✓ Branch deleted (local + remote)
✓ JT_PTEAE-2930: Logged 1m work
✓ JT_PTEAE-2930: Transitioned to 'Done'
✓ Changelog updated: Version 1.2.0
```

---

### `git-go status <project-name>`

**Purpose:** Display current workflow status across all phases

**Displays:**

```text
📊 Workflow Status: JT_PTEAE-2930_feature-name

┌─ Git Status ─────────────────────────────────┐
│ Branch:      JT_PTEAE-2930_feature-name       │
│ Changes:     3 files modified                 │
│ Untracked:   0 files                          │
└───────────────────────────────────────────────┘

┌─ JIRA Status ────────────────────────────────┐
│ Issue:       JT_PTEAE-2930                    │
│ Title:       Implement new authentication    │
│ Status:      In Progress                      │
│ Time Logged: 8m / Estimate: 2h 30m            │
│ Assignee:    you@company.com                  │
│ PRs Linked:  1 (Draft)                        │
└───────────────────────────────────────────────┘

┌─ Commits ────────────────────────────────────┐
│ • feat(auth): add new provider support       │
│ • test(auth): add integration tests          │
│ • docs(auth): update readme                  │
└───────────────────────────────────────────────┘

⏭️  Next: Push to create PR and transition to review
```

---

## Overhead Reduction Strategy

### What Gets Automated (You Don't Do These)

- ❌ Manually transition JIRA status
- ❌ Type issue keys in messages
- ❌ Log time manually to JIRA
- ❌ Assign reviewers manually
- ❌ Update branch descriptions
- ❌ Calculate version bumps
- ❌ Type PR descriptions from scratch

### What You Still Do (Intentional)

- ✅ Write meaningful commit messages (enforced format)
- ✅ Approve PR code changes (required)
- ✅ Merge to main (final quality gate)
- ✅ Decide branch creation (conscious start)

---

## JIRA Integration Requirements

### Environment Setup

```bash
# Required for JIRA authentication
export JIRA_USERNAME="your.email@company.com"
export JIRA_TOKEN="your_api_token_or_password"
export JIRA_SERVER="https://your-org.atlassian.net"
```

### Git Configuration

```bash
# Enable JIRA automation (required)
git config hooks.jira.enabled true

# JIRA instance details
git config hooks.jira.url "$JIRA_SERVER"
git config hooks.jira.username "$JIRA_USERNAME"

# Customize worklog times
git config hooks.jira.worklog.start "5m"
git config hooks.jira.worklog.push "2m"
git config hooks.jira.worklog.merge "1m"

# Transition customization
git config hooks.jira.autoTransition true              # Enable auto-transitions
git config hooks.jira.transition.start "In Progress"   # Override start state
git config hooks.jira.transition.review "Code Review"  # Override review state
git config hooks.jira.transition.done "Done"           # Override done state
```

### First-Time Setup

```bash
# 1. Install hooks
python install.py

# 2. Configure JIRA credentials (one-time)
git config hooks.jira.enabled true
# Credentials will be prompted on first hook execution

# 3. Verify connection
git config hooks.jira.test  # Validates JIRA connection

# 4. View stored config
git config --get-regexp hooks\.jira
```

---

## Workflow Scenarios

### Scenario 1: Bug Fix Sprint

```bash
# Friday evening: Start bug fix
git-go start myproject JT_PTEAE-2930
✓ JIRA auto-transitioned to "In Progress"
✓ 5m logged automatically

# Saturday morning: Push for code review
git push
✓ Pre-push hook fires
✓ 2m logged for development overhead
✓ JIRA auto-transitioned to "Code Review"

# Saturday afternoon: Merge after approval
git-go publish myproject
✓ Branch merged
✓ 1m logged
✓ JIRA auto-transitioned to "Done"
✓ Total tracked: 8m (realistic overhead)
```

### Scenario 2: Long-Running Feature

```bash
# Monday: Start feature
git-go start myproject JT_PTEAE-3100
✓ Tracked: 5m

# Wednesday: Push for early review (not merging)
git push origin feature-branch
✓ Tracked: 2m additional
✓ JIRA transitioned to "Code Review" with PR link

# Thursday: Continue development
git checkout develop  # Switch branch
✓ Post-checkout hook fires for develop
# Later...
git checkout JT_PTEAE-3100_feature
✓ Post-checkout hook re-engages JT_PTEAE-3100
✓ JIRA auto-updates with branch context

# Friday: Final push and merge
git-go publish myproject
✓ Tracked: 1m for merge ceremony
✓ Total: 8m for entire week-long feature
```

---

## Advanced Configuration

### Custom Transition Logic

```bash
# If your JIRA workflow uses different state names
git config hooks.jira.transition.start "Development"      # Instead of "In Progress"
git config hooks.jira.transition.review "Peer Review"     # Instead of "Code Review"
git config hooks.jira.transition.done "Resolved"          # Instead of "Done"
```

### Disable Specific Automations

```bash
# Log time but don't transition (safer for complex workflows)
git config hooks.jira.autoTransition false
git config hooks.jira.worklog.enabled true

# Transition but don't log time (time tracked elsewhere)
git config hooks.jira.autoTransition true
git config hooks.jira.worklog.enabled false
```

### Per-Project Configuration

```bash
# Set at repository level (overrides global)
cd /path/to/project
git config --local hooks.jira.worklog.start "10m"

# View what's configured at each level
git config --show-origin hooks.jira.worklog.start
```

---

## Troubleshooting JIRA Automation

### "JIRA transition failed - not allowed"

- **Cause:** Transition doesn't exist in your workflow

- **Fix:** Set `hooks.jira.autoTransition false` to disable, or customize transition names:

  ```bash
  git config hooks.jira.transition.start "Development"
  ```

### "Authentication failed"

- **Cause:** Credentials expired or incorrect format
- **Fix:** Re-run hook to refresh credentials:

  ```bash
  keyring-cli delete gojira.jira.password password

  # Next hook execution will prompt for new password
  ```

### "Time logging blocked"

- **Cause:** Already logged time for this issue today (some JIRA configs prevent duplicates)
- **Fix:** Configure longer intervals:

  ```bash
  git config hooks.jira.worklog.push "30m"  # Skip time logging for brief pushes
  git config hooks.jira.worklog.enabled false  # Disable entirely
  ```

### Verify Hook Execution

```bash
# Check if hooks ran (look for [OK] messages)
git-go start myproject JT_PTEAE-2930 2>&1 | grep -E "\[OK\]|\[ERROR\]"

# Enable debug output
export DEBUG_HOOKS=1
git push  # Watch detailed hook execution
```

---

## Metrics & Visibility

### Track Your Saved Time

With full JIRA automation, typical savings:

| Activity               | Before         | After         | Saved           |
| ---------------------- | -------------- | ------------- | --------------- |
| Manual status updates  | ~5 min/day     | Auto          | 5m/day          |
| Manual time logging    | ~3 min/day     | Auto          | 3m/day          |
| PR description writing | ~10 min/PR     | Template+Auto | 8m/PR           |
| Reviewer assignment    | ~5 min/PR      | Auto          | 5m/PR           |
| **Per week (5 PRS)**   | **~1.5 hours** | **~15 min**   | **~1.25 hours** |

### Monitor Automation

```bash
# View all hooks run and their outcomes
git log --format=%B | grep -E "JT_PTEAE.*Transitioned|logged.*work"

# Generate worklog report
git config --get-regexp hooks | grep worklog
```
