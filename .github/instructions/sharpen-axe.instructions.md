---
description: Sharpen Axe Agent implementation and tracking instructions — for use with sharpen-axe.agent.md
applyTo: '**'
---


# Sharpen Axe Agent Implementation Instructions



These instructions define the process for implementing the plan for `sharpen-axe.agent.md` using progressive tracking and change records. All plans, research, changes, details, and prompts must be managed under the official `.github/` workspace structure as defined in [copilot-workspace-structure.instructions.md]. Follow this guide to ensure systematic, high-quality, and fully traceable implementation.

## Reference: [copilot-workspace-structure.instructions.md]
See that file for full directory, naming, and content separation rules. All instructions here are subordinate to the workspace structure specification.

## 1. Preparation and Plan Analysis

  - **MANDATORY:** Read and fully understand the complete plan file for `sharpen-axe.agent.md` (in `.github/plans/`)
  - **MANDATORY:** Read and fully understand the corresponding changes file (in `.github/plans/`)
  - **MANDATORY:** Identify and review all referenced files in the plan for context
  - **MANDATORY:** Understand current project structure, conventions, and agent requirements

## 2. Systematic Implementation Process

- Process tasks in the plan sequentially, one at a time
  - **Before implementing any task:**
    - Ensure the task is associated with the plan for `sharpen-axe.agent.md` in `.github/plans/`
    - Read the full details for the task from the relevant `.github/` subfolder
    - Gather any additional required context
- Implement the task completely, following workspace patterns and conventions
- Validate that the implementation meets all requirements from the details file
- Mark the task complete `[x]` in the plan file
- **After every task:**
  - Update the changes file in `.github/plans/` by appending to Added, Modified, or Removed sections with relative file paths and a one-sentence summary
  - If any changes diverge from the plan/details, call out the divergence and reason in the changes file
  - If all tasks in a phase are complete, mark the phase header as `[x]`

## 3. Implementation Quality Standards

- Follow workspace and agent code conventions
- Implement complete, working functionality for each task
- Include error handling and documentation for complex logic
- Ensure compatibility with existing systems and dependencies

## 4. Continuous Progress and Validation

- After each task, validate changes against requirements
- Fix any issues before moving to the next task
- Update the plan and changes files as described above
- Continue until all tasks and phases are marked complete `[x]`

## 5. Completion and Documentation

- Implementation is complete when:
  - All plan tasks are marked complete `[x]`
  - All specified files exist with working code
  - All success criteria are verified
  - No implementation errors remain
- **Final step:** Add a Release Summary to the changes file after all phases are complete

## 6. Problem Resolution

- Document any implementation issues clearly
- Try alternative approaches or search terms as needed
- Use workspace patterns as fallback
- Note unresolved issues in the plan for future reference


## Changes File Template

<!-- markdownlint-disable-file -->
# Release Changes: Sharpen Axe Agent

**Related Plan**: sharpen-axe.agent.md
**Implementation Date**: {{YYYY-MM-DD}}

## Summary

{{Brief description of the overall changes made for this release}}

## Changes

### Added

- {{relative-file-path}} - {{one sentence summary of what was implemented}}

### Modified

- {{relative-file-path}} - {{one sentence summary of what was changed}}

### Removed

- {{relative-file-path}} - {{one sentence summary of what was removed}}

## Release Summary

**Total Files Affected**: {{number}}

### Files Created ({{count}})

- {{file-path}} - {{purpose}}

### Files Modified ({{count}})

- {{file-path}} - {{changes-made}}

### Files Removed ({{count}})

- {{file-path}} - {{reason}}

### Dependencies & Infrastructure

- **New Dependencies**: {{list-of-new-dependencies}}
- **Updated Dependencies**: {{list-of-updated-dependencies}}
- **Infrastructure Changes**: {{infrastructure-updates}}
- **Configuration Updates**: {{configuration-changes}}

### Deployment Notes

{{Any specific deployment considerations or steps}}
