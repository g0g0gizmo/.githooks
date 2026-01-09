---
description: 'Generate atomic Conventional Commits with gitmoji, scope, body & footer validation.'
mode: 'agent'
tools:
  - run_in_terminal
  - get_terminal_output
  - todos
---

# Conventional Commit Generator

## Instructions

Generate an atomic Conventional Commit message for your staged changes using the following rules:

1. **Scope**: Use VS Code environment variables to auto-fill scope:
   - `${fileBasename}` for filename
   - `${workspaceFolder}` for project/package name
   - You may also use module, section, or system component as scope if more appropriate.
2. **Format**: Follow the format `type(scope): gitmoji description` (subject under 50 chars).
3. **Guidelines**: See [conventional-commit.instructions.md](../.github/instructions/conventional-commit.instructions.md) for:
   - Commit types, scope rules, and emoji usage
   - How to avoid duplicate scopes
   - Imperative mood for descriptions
   - Breaking up changes for atomic commits
   - [GitHub emoji cheat sheet](https://github.com/ikatyang/emoji-cheat-sheet)
4. **Jira Integration**: If your branch matches `<INITIALS>_<JIRA-KEY>_description`, use Jira Smart Commit syntax (see [smart-commit.instructions.md](../.github/instructions/smart-commit.instructions.md)).
5. **Body & Footer**: Optionally add a body for context and a footer for references.

---

### Example

```
feat(${fileBasename}): :sparkles: Add new validation logic

- Refactored input checks for clarity
- Improved error messages

JT_PTEAE-1234 #resolve #comment Improved validation
```
