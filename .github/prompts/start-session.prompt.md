---
name: start-session
description: 'Initialize focused work session with Jira context, Obsidian note, and Outlook focus blocks'
model: anthropic/claude-3.7-sonnet
target: automation
metadata:
  category: workflow
  version: 1.0.0
  tags:
    - focus-session
    - jira
    - obsidian
    - outlook
    - productivity
  owner: automation-team
---

# Start Focus Session

**Purpose:** Initialize a focused work session by preparing all necessary context: opening Jira issue, creating/opening Obsidian work note, loading relevant code files, and blocking calendar for deep work.

## Input Variables

- `{jiraKey}` - Jira issue key to work on (e.g., "JIRA-123")
- `{jiraTitle}` - Issue title from Jira
- `{jiraDescription}` - Full issue description with acceptance criteria
- `{jiraStatus}` - Current issue status ("To Do", "In Progress", etc.)
- `{top_tasks}` - Array of subtasks or action items for this issue
  - Format: `[{"id": 1, "description": "...", "status": "not-started"}]`
- `{context_files}` - Array of relevant code files to open
  - Format: `[{"path": "...", "reason": "..."}]`
- `{estimated_hours}` - Estimated work time (e.g., "2", "4", "8")
- `{focus_mode}` - Type of work: "implementation", "review", "research", "debugging"

## Output Actions

This prompt triggers multiple automation actions:

1. **Jira Transition:** Move issue to "In Progress" status
2. **Obsidian Note:** Create or open work note with structure
3. **VSCode Context:** Open relevant files in editor
4. **Outlook Block:** Create focus time block on calendar
5. **Status Bar:** Update VSCode status bar with current Jira key
6. **Slack Status:** Set "In Focus" status with Jira reference

## Obsidian Note Structure

Create note at: `{ObsidianVault}/Work/{jiraKey}-{kebab-title}.md`

**Template:**
```markdown
---
jira: {jiraKey}
title: {jiraTitle}
status: {jiraStatus}
started: {current_timestamp}
focus_mode: {focus_mode}
tags:
  - work
  - {jiraKey}
  - {focus_mode}
---

# {jiraKey}: {jiraTitle}

## Context

**Jira Link:** [{jiraKey}]({jiraUrl})
**Status:** {jiraStatus}
**Started:** {current_timestamp}
**Estimated:** {estimated_hours} hours

### Description

{jiraDescription}

## Top Tasks

{top_tasks_checklist}

## Session Log

### {current_date} - {current_time}

**Session Start**
- Focus mode: {focus_mode}
- Estimated time: {estimated_hours}h
- Context loaded: {context_files_count} files

**Notes:**
-

## Decisions

<!-- Link decision documents as they're created -->

## Blockers

<!-- Document blockers as they arise -->

## References

<!-- Links to related documentation, PRs, issues -->

---

**Next Session:** <!-- Quick notes for future pickup -->
```

## Context Files Loading

**Extract from `{context_files}` array:**

```json
[
  {
    "path": "src/auth/oauth-provider.ts",
    "reason": "Main implementation file for OAuth logic"
  },
  {
    "path": "src/auth/__tests__/oauth-provider.test.ts",
    "reason": "Test file to understand existing coverage"
  },
  {
    "path": "docs/architecture/authentication.md",
    "reason": "Architectural context for auth module"
  }
]
```

**Actions:**
1. Open each file in VSCode in order listed
2. Focus on first file (primary implementation)
3. Create vertical split if > 2 files
4. Add comment to Obsidian note with file list

**Obsidian Note Addition:**
```markdown
### Context Files Loaded

- `src/auth/oauth-provider.ts` - Main implementation
- `src/auth/__tests__/oauth-provider.test.ts` - Tests
- `docs/architecture/authentication.md` - Architecture
```

## Outlook Focus Block

**Calendar Entry:**
- **Title:** `🎯 Focus: {jiraKey} - {jiraTitle}`
- **Duration:** `{estimated_hours}` hours from now
- **Status:** Busy (blocks meeting invites)
- **Location:** Remote (or configured work location)
- **Body:**
  ```
  Focus session for {jiraKey}

  Tasks:
  {top_tasks_list}

  Obsidian Note: {obsidian_note_path}
  ```

**Categories:** "Focus Time", "Development"

**Reminder:** 5 minutes before end (to wrap up cleanly)

## VSCode Status Bar

**Update status bar item:**
```
🎯 {jiraKey} | {focus_mode} | {elapsed_time}
```

**Click Actions:**
- Left click: Open Jira issue in browser
- Right click: Context menu
  - "Open Obsidian Note"
  - "View Related PRs"
  - "Add Blocker"
  - "End Session"

**Update Frequency:** Every 1 minute to show elapsed time

## Slack Status Update

**Status:**
```
🎯 In Focus - {jiraKey}
```

**Expiration:** `{estimated_hours}` hours from now

**Status Emoji:** `:dart:` (target/focus icon)

**Status Text:** "In Focus - {jiraKey}"

## Top Tasks Checklist

**Extract from `{top_tasks}` array:**

```json
[
  {"id": 1, "description": "Design OAuth provider interface", "status": "not-started"},
  {"id": 2, "description": "Implement token refresh logic", "status": "not-started"},
  {"id": 3, "description": "Add unit tests for provider selection", "status": "not-started"},
  {"id": 4, "description": "Update documentation", "status": "not-started"}
]
```

**Generate Markdown Checklist:**
```markdown
## Top Tasks

- [ ] 1. Design OAuth provider interface
- [ ] 2. Implement token refresh logic
- [ ] 3. Add unit tests for provider selection
- [ ] 4. Update documentation
```

## Example Prompts

### Example 1: Implementation Session

**Input:**
```json
{
  "jiraKey": "JIRA-123",
  "jiraTitle": "OAuth2 SSO Integration",
  "jiraDescription": "Implement OAuth2 authentication...",
  "jiraStatus": "To Do",
  "top_tasks": [
    {"id": 1, "description": "Design provider interface", "status": "not-started"},
    {"id": 2, "description": "Implement token logic", "status": "not-started"},
    {"id": 3, "description": "Add unit tests", "status": "not-started"}
  ],
  "context_files": [
    {"path": "src/auth/oauth-provider.ts", "reason": "Main implementation"},
    {"path": "src/auth/__tests__/oauth-provider.test.ts", "reason": "Tests"}
  ],
  "estimated_hours": "4",
  "focus_mode": "implementation"
}
```

**Actions Triggered:**
1. ✅ Jira JIRA-123 transitioned to "In Progress"
2. ✅ Obsidian note created: `Work/JIRA-123-oauth2-sso-integration.md`
3. ✅ VSCode opened: `oauth-provider.ts`, `oauth-provider.test.ts`
4. ✅ Outlook blocked: 4 hours starting now
5. ✅ Status bar: `🎯 JIRA-123 | implementation | 0:00`
6. ✅ Slack status: `🎯 In Focus - JIRA-123` (expires in 4h)

### Example 2: Debugging Session

**Input:**
```json
{
  "jiraKey": "JIRA-456",
  "jiraTitle": "Fix Email Validation",
  "jiraDescription": "Email validation incorrectly rejects plus addressing...",
  "jiraStatus": "To Do",
  "top_tasks": [
    {"id": 1, "description": "Reproduce bug with test case", "status": "not-started"},
    {"id": 2, "description": "Identify regex issue", "status": "not-started"},
    {"id": 3, "description": "Fix and verify", "status": "not-started"}
  ],
  "context_files": [
    {"path": "src/validation/email.ts", "reason": "Validation logic"},
    {"path": "src/validation/__tests__/email.test.ts", "reason": "Existing tests"},
    {"path": "docs/bugs/email-validation-report.md", "reason": "Bug report"}
  ],
  "estimated_hours": "2",
  "focus_mode": "debugging"
}
```

**Actions Triggered:**
1. ✅ Jira JIRA-456 transitioned to "In Progress"
2. ✅ Obsidian note created with bug context
3. ✅ VSCode opened: validation files + bug report
4. ✅ Outlook blocked: 2 hours
5. ✅ Status bar: `🎯 JIRA-456 | debugging | 0:00`
6. ✅ Slack status: `🎯 In Focus - JIRA-456` (expires in 2h)

### Example 3: Research Session

**Input:**
```json
{
  "jiraKey": "JIRA-789",
  "jiraTitle": "Research Dashboard Frameworks",
  "jiraDescription": "Evaluate React vs Vue for dashboard...",
  "jiraStatus": "To Do",
  "top_tasks": [
    {"id": 1, "description": "Research React ecosystem", "status": "not-started"},
    {"id": 2, "description": "Research Vue ecosystem", "status": "not-started"},
    {"id": 3, "description": "Document comparison", "status": "not-started"}
  ],
  "context_files": [
    {"path": "docs/research/dashboard-requirements.md", "reason": "Requirements doc"},
    {"path": "docs/architecture/frontend-patterns.md", "reason": "Current patterns"}
  ],
  "estimated_hours": "3",
  "focus_mode": "research"
}
```

**Obsidian Note Special Section:**
```markdown
## Research Findings

### React
- Pros:
- Cons:
- Resources:

### Vue
- Pros:
- Cons:
- Resources:

## Recommendation

[To be completed after research]
```

## Focus Mode Variations

### Implementation Mode
- Opens: Implementation files + tests
- Obsidian: Task checklist emphasized
- Outlook: "Development - Do Not Disturb"
- Slack: Minimal interruptions expected

### Review Mode
- Opens: PRs, changed files, test results
- Obsidian: Feedback tracking section added
- Outlook: "Code Review - Limited Availability"
- Slack: Can respond to urgent messages

### Research Mode
- Opens: Documentation, requirements, examples
- Obsidian: Research findings section added
- Outlook: "Research - Do Not Disturb"
- Slack: Completely unavailable

### Debugging Mode
- Opens: Bug report, implementation, tests, logs
- Obsidian: Reproduction steps and hypotheses section
- Outlook: "Debugging - Critical Focus"
- Slack: Emergency only

## Session End Actions

When session completes (manual or timer):

1. **Obsidian Note:** Add closing timestamp and summary prompt
2. **Jira Comment:** Post session summary (time spent, progress)
3. **Git Status:** Check for uncommitted changes
4. **Slack Status:** Clear focus status
5. **VSCode Status Bar:** Clear Jira indicator
6. **Prompt:** "Create standup entry for today?" (if not yet done)

## Error Handling

### Jira Transition Failed
**Error:** Cannot move to "In Progress" (workflow constraint)

**Action:**
- Show warning notification
- Continue with other actions
- Log in Obsidian note: `⚠️ Manual Jira transition required`

### Obsidian Vault Not Found
**Error:** Configured vault path doesn't exist

**Action:**
- Create note in fallback location: `{workspace}/.obsidian-work/`
- Notify user to configure vault path
- Continue with other actions

### Outlook Not Available
**Error:** Outlook API unavailable or not configured

**Action:**
- Skip calendar block
- Notify user to manually block calendar
- Continue with other actions

## Integration Context

This prompt is used by:

1. **Start Focus Session Script** (`.joyride/src/start_focus_session.cljs`)
   - Primary trigger for all session initialization
   - Coordinates all integrations (Jira, Obsidian, VSCode, Outlook, Slack)
   - Handles errors gracefully

2. **Workflow Orchestrator Agent** (`.github/agents/workflow-orchestrator.agent.md`)
   - Suggests focus session when starting new Jira issue
   - Pre-populates context files from codebase analysis

3. **VSCode Command** (`dailyctl start {jiraKey}`)
   - Manual trigger for focus sessions
   - Allows override of estimated hours and context files

## Related Documentation

- [Daily Needs Workflow](../../docs/my-daily-needs.md#workflow-overview)
- [Jira Conventions](../../docs/my-daily-needs.md#jira-conventions)
- [Automation Backlog (A8)](../../docs/my-daily-needs.md#automation-backlog)
