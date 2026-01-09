---
applyTo: '**/.copilot-tracking/*.md'
description: 'Instructions for implementing task plans with progressive tracking - Brought to you by microsoft/edge-ai'
---

# Task Plan Implementation Instructions

## Overview

This instruction file guides implementation of task plans using a single tracking file system:

- **`.copilot-tracking/TODO.md`** - Main tracking file that documents progress and changes
- **`.copilot-tracking/plans/*.md`** - Referenced plan files containing task lists and requirements

The TODO.md file links to a specific plan and tracks all implementation progress, changes, and completion status in one place.

## File Structure Setup

### Before Starting Implementation

You MUST have these files in place:

1. **Plan File** (`.copilot-tracking/plans/YYYYMMDD-task-name.md`):
   - Pre-exists before you start
   - Contains task lists, requirements, and success criteria
   - You will reference this but NOT modify it

2. **TODO File** (`.copilot-tracking/TODO.md`):
   - Created at the start of implementation if it doesn't exist
   - Links to the active plan file
   - Tracks progress and changes as you work
   - You will update this throughout implementation

### Initial TODO.md Creation

If `.copilot-tracking/TODO.md` does not exist, create it using the template at the end of this document. The template includes:
- Link to the plan file
- Task checklist (copied from plan)
- Jira ticket hyperlinks for each task (format: `[TICKET-0000](https://...)` or `[Create Ticket]()`)
- Changes tracking sections (Added, Modified, Removed)
- Release summary section (completed at the end)

## Core Implementation Process

### Phase 1: Preparation

**Complete these steps before implementing any tasks:**

1. Locate and open the plan file referenced in `.copilot-tracking/TODO.md`
2. Read the complete plan including:
   - Project scope and objectives
   - All task phases and checklist items
   - Success criteria and requirements
3. Examine the TODO.md file completely - ensure you have the full context
4. Identify all files mentioned in the plan and review them for context
5. Understand the project structure and coding conventions (check workspace patterns)

### Phase 2: Task-by-Task Implementation

**For each unchecked task `[ ]` in TODO.md:**

1. **Understand the Task**:
   - Review the task description in the plan file
   - Check the Jira ticket hyperlink in the task description for additional context
   - Gather any additional context needed from the workspace
   - Identify which files need to be created or modified

2. **Implement the Task**:
   - Follow existing workspace patterns and conventions
   - Create complete, working functionality
   - Include proper error handling and documentation
   - Follow best practices from the workspace

3. **Validate the Implementation**:
   - Test that the implementation works correctly
   - Verify it meets the task requirements from the plan
   - Fix any issues before proceeding

4. **Update TODO.md** (REQUIRED after EVERY task):
   - Mark the task complete: change `[ ]` to `[x]`
   - Add entries to the Changes section:
     - **Added**: New files with one-sentence description
     - **Modified**: Changed files with one-sentence description
     - **Removed**: Deleted files with one-sentence description
   - If changes diverge from the plan, note the divergence and reason
   - If ALL tasks in a phase are complete, mark the phase header `[x]`

5. **Continue to Next Task**:
   - Move to the next unchecked `[ ]` task
   - Repeat until all tasks are complete

### Phase 3: Completion

**When all tasks are marked complete `[x]`:**

1. Verify all success criteria from the plan are met
2. Ensure all specified files exist with working code
3. Complete the Release Summary section in TODO.md:
   - Document total files affected
   - List all files created, modified, and removed
   - Note any dependencies or infrastructure changes
   - Add deployment notes if applicable

## Implementation Quality Standards

**Every implementation MUST meet these standards:**

- **Follow Workspace Patterns**: Use consistent naming, structure, and conventions from existing code
- **Complete Functionality**: Implement fully working features, not partial solutions
- **Error Handling**: Include appropriate validation and error handling
- **Documentation**: Add comments for complex logic and update relevant documentation
- **Compatibility**: Ensure changes work with existing systems and dependencies
- **Testing**: Validate that implementations work as expected

## Progress Tracking Requirements

**You MUST update TODO.md after completing each task:**

- Mark the task complete `[x]` in the task checklist
- Ensure each task has a Jira ticket hyperlink: `[TICKET-0000](https://...)` or `[Create Ticket]()` if not yet created
- Add file changes to the appropriate section (Added/Modified/Removed)
- Include relative file paths and brief descriptions
- Note any divergences from the plan with reasons

This ensures:
- Continuous visibility into progress
- Accurate change tracking for releases
- Clear audit trail of implementation decisions

## Problem Resolution

**When encountering implementation challenges:**

1. Document the specific problem in TODO.md
2. Try alternative approaches based on workspace patterns
3. Use workspace conventions as guidance when external references are unclear
4. Continue with available information rather than stopping completely
5. Note unresolved issues in TODO.md for future reference

## Success Criteria

**Implementation is complete when:**

- ✅ All tasks in TODO.md are marked complete `[x]`
- ✅ All specified files contain working code
- ✅ Code follows workspace patterns and conventions
- ✅ All functionality works as expected
- ✅ Changes section in TODO.md is complete and accurate
- ✅ Release Summary section is documented
- ✅ All plan success criteria are verified

## Quick Reference: Implementation Workflow

```text
1. Read plan file linked in TODO.md
2. Review TODO.md task checklist completely
3. For each unchecked [ ] task:
   a. Understand requirements from plan
   b. Gather necessary context
   c. Implement with working code
   d. Validate implementation
   e. Mark task [x] in TODO.md
   f. Add changes to Added/Modified/Removed sections
4. Repeat until all tasks complete
5. Complete Release Summary section
6. Verify all success criteria met
```

## TODO.md Template

Use this template when creating `.copilot-tracking/TODO.md` at the start of implementation.
Replace `{{variables}}` with actual values.

<!-- <todo-template> -->
```markdown
<!-- markdownlint-disable-file -->
# TODO: {{Task Name}}

**Plan**: [{{plan-file-name}}](./plans/{{plan-file-name}})
**Started**: {{YYYY-MM-DD}}
**Status**: In Progress / Complete

## Task Checklist

{{Copy task checklist from plan file - maintain hierarchy and structure}}

Example:
### Phase 1: Foundation
- [ ] Task 1: Set up project structure [PROJ-1234](https://jira.company.com/browse/PROJ-1234)
- [ ] Task 2: Configure build system [PROJ-1235](https://jira.company.com/browse/PROJ-1235)
- [ ] Task 3: Create base classes [Create Ticket]()

### Phase 2: Core Features
- [ ] Task 4: Implement feature A [PROJ-1236](https://jira.company.com/browse/PROJ-1236)
- [ ] Task 5: Implement feature B [Create Ticket]()

## Changes

### Added

<!-- Add new files here as you create them -->
<!-- Example: - src/components/NewComponent.tsx - Created reusable button component -->

### Modified

<!-- Add modified files here as you change them -->
<!-- Example: - src/app/main.ts - Added new route configuration -->

### Removed

<!-- Add removed files here if you delete them -->
<!-- Example: - src/deprecated/OldHelper.ts - Removed unused utility class -->

## Notes

<!-- Document any important decisions, divergences from plan, or issues encountered -->

## Release Summary

<!-- Complete this section only when ALL tasks are marked [x] -->

**Total Files Affected**: {{count}}

### Files Created ({{count}})

- {{file-path}} - {{purpose}}

### Files Modified ({{count}})

- {{file-path}} - {{changes-made}}

### Files Removed ({{count}})

- {{file-path}} - {{reason-for-removal}}

### Dependencies & Infrastructure

- **New Dependencies**: {{list or "None"}}
- **Updated Dependencies**: {{list or "None"}}
- **Infrastructure Changes**: {{description or "None"}}
- **Configuration Updates**: {{description or "None"}}

### Deployment Notes

{{Any deployment considerations or steps needed, or "Standard deployment process applies"}}

### Completion

**Completed**: {{YYYY-MM-DD}}
**All Success Criteria Met**: Yes / No
**Ready for Release**: Yes / No
```
<!-- </todo-template> -->
