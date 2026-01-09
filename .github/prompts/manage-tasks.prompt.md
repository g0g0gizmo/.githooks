---
description: 'Add, list, filter, and complete tasks in workspace TODO.md file'
---

# Manage Tasks

Create, update, and track tasks in your workspace TODO.md file. Supports adding new tasks, listing tasks, filtering by category, and marking tasks complete.

## Core Principles

This content applies the following foundational principles:

- [KISS](../core/principles/KISS.md) - Keep task management simple and focused
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Clear, organized task tracking

---

## Task File Location

Default: `${workspaceRoot}/TODO.md`

Format: Markdown with clear structure and categories

---

## Operations

### 1. Add New Task

**Ask the user:**
- Task description (what needs to be done?)
- Category (optional: feature, bug, refactor, doc, test, etc.)
- Priority (optional: high, medium, low, or default: medium)
- Due date (optional)
- Assigned to (optional)

**Format:**
```markdown
- [ ] Task description @category #priority ~duedate @assignee
```

**Examples:**
```markdown
- [ ] Implement user authentication @feature #high ~2025-12-15 @john
- [ ] Fix login bug @bug #critical ~2025-11-30
- [ ] Refactor database layer @refactor #medium
- [ ] Update API documentation @doc
```

### 2. List All Tasks

Shows all tasks in TODO.md with:
- Task description
- Category (if present)
- Priority (if present)
- Due date (if present)
- Status (completed or pending)

**Output:**
```
Current Tasks (5 total):
✓ Setup project structure (@setup)
✗ Implement authentication @feature #high ~2025-12-15
✗ Fix login bug @bug #critical ~2025-11-30
✗ Refactor database @refactor
✗ Update API docs @doc
```

### 3. Filter Tasks

**Filter by:**
- Category: `@feature`, `@bug`, `@refactor`, `@doc`, `@test`
- Priority: `#critical`, `#high`, `#medium`, `#low`
- Status: completed (`✓`) or pending (`✗`)
- Due soon: tasks due in next 7 days
- Overdue: tasks past due date

**Examples:**
```
List all features: Show tasks @feature
List high-priority bugs: Show tasks @bug #high
List overdue: Show tasks past due
List due this week: Show tasks due in 7 days
```

### 4. Complete Task

Mark task as done by:
- Task number or name
- Auto-updates checkbox `[ ]` to `[x]`

**Format:**
```markdown
- [x] Task description @category
```

### 5. Update Task

Modify existing task:
- Change priority
- Update due date
- Add category
- Change description
- Reassign

### 6. Archive Completed

Move completed tasks to completed section or separate file:
- Keep TODO.md clean
- Preserve task history
- Option to archive to COMPLETED.md

---

## File Structure

```markdown
# TODO - Active Tasks

## High Priority
- [ ] Task 1 @feature #critical
- [ ] Task 2 @bug #high

## Medium Priority
- [ ] Task 3 @refactor
- [ ] Task 4 @doc

## Backlog
- [ ] Future task

## Completed
- [x] Done task 1
- [x] Done task 2
```

---

## Task Categories

| Category | Use For | Example |
|----------|---------|---------|
| `@feature` | New functionality | Add authentication system |
| `@bug` | Defect fixes | Fix login timeout issue |
| `@refactor` | Code improvement | Simplify payment module |
| `@doc` | Documentation | Update API reference |
| `@test` | Testing work | Add integration tests |
| `@perf` | Performance | Optimize database queries |
| `@security` | Security work | Add input validation |
| `@setup` | Infrastructure | Configure CI/CD |
| `@review` | Code review | Review PR #123 |

---

## Priority Levels

| Priority | Urgency | Timeframe |
|----------|---------|-----------|
| `#critical` | Do immediately | Today |
| `#high` | Do soon | This week |
| `#medium` | Normal priority | This month |
| `#low` | Can wait | Backlog |

---

## Task Naming Tips

✓ **Clear**: "Add user authentication with JWT"
❌ Vague: "Fix stuff"

✓ **Actionable**: "Write unit tests for payment module"
❌ Not actionable: "Payment module"

✓ **Specific**: "Reduce API response time from 500ms to <100ms"
❌ Vague: "Make it faster"

---

## Using Tasks with Projects

Link tasks to GitHub/GitLab:
- Reference issue numbers: "#123 Implement feature"
- Reference PRs: "PR #456 Code review"
- Link to discussion: "@team discussion in #general"

---

## Task Lifecycle

```
CREATE → ASSIGN → ESTIMATE → IMPLEMENT → REVIEW → COMPLETE → ARCHIVE
   ↓
Active task in TODO.md → Tracked in issue system → Completed and marked done → Moved to archive
```

---

## Integration with Workflow

### During Planning
- Create tasks for sprint
- Categorize and prioritize
- Assign to team members

### During Development
- Reference task in commits: "feat: implement auth [#task-name]"
- Update task status
- Move between categories as needed

### During Review
- Update task with feedback
- Link to PR for code review
- Track blockers

### After Completion
- Mark task complete
- Update time spent
- Archive task
- Document learnings

---

## Best Practices

- ✓ **Keep TODO.md simple**: One file, clear structure
- ✓ **Review regularly**: Update tasks weekly
- ✓ **Keep it current**: Remove completed tasks promptly
- ✓ **Be specific**: Clear descriptions prevent misunderstanding
- ✓ **Link context**: Reference issues, PRs, discussions
- ✓ **Archive history**: Keep completed record separately
- ❌ **Don't**: Use for long-term backlog (use project boards instead)
- ❌ **Don't**: Leave thousands of items (prioritize, archive)

---

## Keyboard Shortcuts (if using IDE extensions)

Common task management extensions:
- TODO Highlight
- Todo Tree
- Tasks (VS Code)

Check extension documentation for keyboard shortcuts.

---

## Integration with Other Tools

### GitHub
```
- [ ] Task description [#issue-number](github.com/user/repo/issues/123)
```

### Jira
```
- [ ] Task @jira [PROJ-123](jira.atlassian.net/...)
```

### GitLab
```
- [ ] Task [#issue-number](gitlab.com/user/repo/-/issues/123)
```

---

## Export & Reporting

Generate reports:
- By category
- By priority
- By assignee
- Completed rate
- Burndown chart

---

## Next Steps

After managing tasks:
1. [ ] Review TODO.md regularly (weekly)
2. [ ] Update task status as you work
3. [ ] Archive completed tasks monthly
4. [ ] Share with team for visibility
5. [ ] Link to project board if large project

---

## Related Content

- For detailed project planning: `create-specification.prompt.md`
- For breaking down work: `test-breakdown.prompt.md`
- For team coordination: Use project boards or Jira
- For memory/learning: `remember.prompt.md`
