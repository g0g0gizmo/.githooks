---
name: create-standup
description: 'Generate daily standup report from Jira and Git activity with Yesterday/Today/Blockers format'
model: anthropic/claude-3.7-sonnet
target: markdown
metadata:
  category: automation
  version: 1.0.0
  tags:
    - standup
    - jira
    - git
    - daily-report
  owner: automation-team
---

# Create Daily Standup Report

**Purpose:** Generate a structured daily standup report in markdown format by analyzing Jira activity, Git commits, and GitHub PR data from the last 24 hours.

## Input Variables

- `{date}` - Target date for standup report (format: YYYY-MM-DD)
- `{yesterday}` - JSON array of work items completed yesterday
  - Format: `[{"jira_key": "JIRA-123", "title": "...", "status": "Done"}]`
- `{today}` - JSON array of work items planned for today
  - Format: `[{"jira_key": "JIRA-456", "title": "...", "priority": "High"}]`
- `{blockers}` - JSON array of blocking items
  - Format: `[{"jira_key": "JIRA-789", "title": "...", "blocker_reason": "..."}]`

## Output Format

Generate a markdown standup report following this exact structure:

```markdown
## Standup - {date}

**Yesterday**: {yesterday_summary}

**Today**: {today_summary}

**Blockers**: {blockers_summary or "None."}
```

## Generation Rules

### Yesterday Section

1. **Extract from `{yesterday}` array:**
   - Completed Jira issues (status = "Done")
   - Merged PRs from Git commits
   - Code reviews completed

2. **Format:**
   - Semicolon-separated sentences
   - Include Jira keys in format: `Completed JIRA-123 user authentication`
   - Past tense verbs (completed, fixed, reviewed)
   - Order by priority/significance

3. **Deduplication:**
   - If multiple commits reference same Jira key, mention issue once
   - Group related activities (e.g., "Reviewed 3 PRs (#841-843)")

4. **Example output:**
   ```
   **Yesterday**: Completed JIRA-321 OAuth2 integration; reviewed PR #842 for API refactoring; fixed validation bug JIRA-456.
   ```

### Today Section

1. **Extract from `{today}` array:**
   - Top 3 Jira issues by priority
   - Scheduled meetings requiring preparation
   - Planned PR reviews

2. **Format:**
   - Semicolon-separated sentences
   - Include Jira keys and automation IDs if applicable
   - Present/future tense (will work on, plan to)
   - Order by priority

3. **Example output:**
   ```
   **Today**: Implement branch naming hook (JIRA-100 / A1); begin standup generator script (JIRA-101 / A2); review architectural decisions for dashboard.
   ```

### Blockers Section

1. **Extract from `{blockers}` array:**
   - Jira issues with status "Blocked"
   - Items waiting on external dependencies
   - Missing information or credentials

2. **Format:**
   - Semicolon-separated sentences if multiple blockers
   - Include what's blocking and what's blocked
   - Provide context for resolution
   - Use "None." if `{blockers}` array is empty

3. **Example outputs:**
   ```
   **Blockers**: Waiting on Jira API token from IT (needed for A2); design approval required before implementing dashboard UI (JIRA-150).
   ```

   Or if no blockers:
   ```
   **Blockers**: None.
   ```

## Quality Guidelines

### Clarity
- Use specific Jira keys and PR numbers
- Provide enough context to understand work without asking questions
- Avoid acronyms unless team-standard (OAuth, API, PR, etc.)

### Conciseness
- 1-3 sentences per section maximum
- Combine related items with semicolons
- Focus on outcomes, not activities (e.g., "Completed authentication" not "Wrote code for authentication")

### Consistency
- Always capitalize section names: **Yesterday**, **Today**, **Blockers**
- Use consistent Jira key format: `JIRA-123`
- Include automation IDs when applicable: `(A1)`, `(A2)`

## Example Prompts

### Example 1: Active Development Day

**Input:**
```json
{
  "date": "2025-11-30",
  "yesterday": [
    {"jira_key": "JIRA-321", "title": "OAuth2 Integration", "status": "Done"},
    {"jira_key": "JIRA-456", "title": "Validation Bug", "status": "Done"},
    {"pr_number": 842, "action": "reviewed"}
  ],
  "today": [
    {"jira_key": "JIRA-100", "title": "Branch Naming Hook", "priority": "High", "automation_id": "A1"},
    {"jira_key": "JIRA-101", "title": "Standup Generator", "priority": "High", "automation_id": "A2"}
  ],
  "blockers": []
}
```

**Output:**
```markdown
## Standup - 2025-11-30

**Yesterday**: Completed JIRA-321 OAuth2 integration; reviewed PR #842 for API refactoring; fixed validation bug JIRA-456.

**Today**: Implement branch naming hook (JIRA-100 / A1); begin standup generator script (JIRA-101 / A2).

**Blockers**: None.
```

### Example 2: Blocked Work

**Input:**
```json
{
  "date": "2025-11-30",
  "yesterday": [
    {"jira_key": "JIRA-123", "title": "OAuth Research", "activity": "research"}
  ],
  "today": [
    {"jira_key": "JIRA-123", "title": "OAuth Implementation", "status": "blocked"}
  ],
  "blockers": [
    {
      "jira_key": "JIRA-123",
      "blocker_reason": "Waiting on API credentials from IT",
      "requested_date": "2025-11-28"
    }
  ]
}
```

**Output:**
```markdown
## Standup - 2025-11-30

**Yesterday**: Researched OAuth2 providers for JIRA-123; evaluated integration options.

**Today**: Waiting on API credentials to continue JIRA-123 OAuth implementation.

**Blockers**: Jira API token pending from IT (requested 2025-11-28); blocking JIRA-123 implementation.
```

### Example 3: Review-Heavy Day

**Input:**
```json
{
  "date": "2025-11-30",
  "yesterday": [
    {"pr_number": 840, "action": "reviewed"},
    {"pr_number": 841, "action": "reviewed"},
    {"pr_number": 842, "action": "reviewed"},
    {"pr_number": 843, "action": "reviewed"},
    {"pr_number": 844, "action": "reviewed"}
  ],
  "today": [
    {"jira_key": "JIRA-200", "title": "API Pairing Session", "type": "pairing"}
  ],
  "blockers": []
}
```

**Output:**
```markdown
## Standup - 2025-11-30

**Yesterday**: Reviewed 5 PRs (#840-844) across authentication and API modules; provided architectural feedback.

**Today**: Pair with team on JIRA-200 API refactor; follow up on PR review comments.

**Blockers**: None.
```

## Integration Context

This prompt is used by:

1. **Standup Generator Script** (`.joyride/src/standup_generate.cljs`)
   - Fetches data from Jira and GitHub APIs
   - Populates variables from collected data
   - Invokes this prompt to generate standup text
   - Writes output to `automation/standup/{date}.md`

2. **Manual Standup Command** (`dailyctl standup`)
   - Collects data interactively or from recent activity
   - Allows manual editing before posting
   - Copies to clipboard or posts to Slack

3. **Standup Agent** (`.github/agents/standup-generator.agent.md`)
   - Uses this prompt as template
   - Adds additional context from calendar and meetings
   - Handles edge cases (Monday standups, vacation days)

## Error Handling

### Empty Yesterday
If `{yesterday}` array is empty:
```markdown
**Yesterday**: Addressed PR review comments; updated documentation.
```

### No Today Items
If `{today}` array is empty:
```markdown
**Today**: Review backlog priorities; plan next sprint tasks.
```

### Multiple Blockers
If `{blockers}` has multiple items, list all:
```markdown
**Blockers**: Waiting on API credentials (JIRA-123); design approval needed (JIRA-150); dependency upgrade blocked by test failures.
```

## Related Documentation

- [Standup Format Standards](../instructions/standup-format.instructions.md)
- [Daily Needs Workflow](../../docs/my-daily-needs.md#daily-ritual-am--pm)
- [Automation Backlog (A2)](../../docs/my-daily-needs.md#automation-backlog)
