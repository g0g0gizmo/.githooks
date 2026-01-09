---
description: 'Atomic conventional commits with gitmoji - Comprehensive guidelines for generating structured, semantic commit messages'
applyTo: '**'
---

# Atomic Conventional Commits with Gitmoji


- Use ATOMIC conventional commits: `type(scope): gitmoji description`. Keep subject under 50 chars.
- **Always include scope** - use package name, filename, module, section, area, or system component.
- Break up staged files into hunks if possible to create the most atomic commits.
- Use imperative mood: 'Add feature' not 'Added feature' or 'Adding feature'.
- **If a Jira ticket is assigned, reference the ticket using Jira Smart Commit syntax in your commit message.**

## Jira Smart Commit Integration

- **If a Jira ticket is assigned** (branch name follows pattern `<INITIALS>_<JIRA-KEY>_description`), use Jira Smart Commit commands to automatically update issues.
- See [smart-commit.instructions.md](smart-commit.instructions.md) for comprehensive Jira Smart Commits documentation including:
  - Branch naming requirements and detection
  - Smart Commit syntax and commands (#comment, #time, #resolve, etc.)
  - Advanced usage patterns
  - Troubleshooting guide


## Types

- **feat**: Introduces a new feature to the codebase. Often a minor version bump.
- **fix**: Patches a bug in the codebase. Often a patch version bump.
- **docs**: Changes related to documentation only.
- **style**: Changes that do not affect the meaning of the code (e.g., whitespace, formatting, missing semicolons).
- **refactor**: Code change that neither fixes a bug nor adds a feature. Restructuring without altering external behavior.
- **perf**: Code change that improves performance.
- **test**: Adding missing tests or correcting existing tests.
- **build**: Changes that affect the build system or external dependencies (e.g., gulp, npm).
- **ci**: Changes to CI configuration files and scripts (e.g., Travis, Circle, GitLab CI).
- **chore**: Other changes that don't modify source or test files. Maintenance tasks and tooling updates.
- **revert**: Reverts a previous commit. The body should reference the commit being reverted.


## Scope Instructions

- **Scope is required** - always include a scope in your commit message.
- **VERY IMPORTANT:** Check if scope already exists—do not duplicate scope (e.g., avoid `auth:auth:` or `package:package:`).
- **VERY IMPORTANT:** Check for previous scope before adding a new one. Duplicate scopes are not allowed.
- Use package name, filename, module, section, area, or system component.
- Examples of valid scopes:
  - **Filenames**: `package.json`, `readme`, `dockerfile`, `tsconfig`
  - **Modules**: `auth`, `database`, `proxy`, `analytics`, `branding`
  - **Packages**: `express`, `cheerio`, `axios`, `openai`, `jest`
  - **Areas/Systems**: `ci`, `build`, `config`, `scripts`, `docs`

VERY IMPORTANT (repeat x10):

- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.
- Check for previous scope. Do NOT duplicate.

Scope format rule:

- Use exactly one colon after type and scope: `type(scope):`.
- Never use patterns like `scope:scope:` — only one `:` belongs between type(scope) and description.


## Emoji Usage Examples

- Always start description with a relevant emoji matching the change type, chosen from the [approved GitHub emoji list](https://github.com/ikatyang/emoji-cheat-sheet).
- The approved emoji list is extensive—select the emoji that best fits your change type and scope. Do not limit yourself to the examples below.
- Examples of approved emojis for commit messages:
  - `feat(scope): :sparkles:` for new features
  - `feat(scope)!: :boom:` for breaking changes
  - `fix(scope): :bug:` for bug fixes
  - `fix(scope): :ambulance:` for critical hotfixes
  - `docs(scope): :memo:` for documentation
  - `docs(scope): :bulb:` for inline comments
  - `style(scope): :art:` for formatting
  - `style(scope): :lipstick:` for UI/CSS improvements
  - `refactor(scope): :recycle:` for code restructuring without changing behavior
  - `perf(scope): :zap:` for performance improvements
  - `test(scope): :white_check_mark:` for adding tests
  - `test(scope): :green_heart:` for fixing CI/test issues
  - `build(scope): :package:` for dependency updates
  - `build(dep): :heavy_plus_sign:` for adding deps
  - `build(dep): :heavy_minus_sign:` for removing deps
  - `ci(scope): :construction_worker:` for CI config
  - `ci(scope): :green_heart:` for fixing build/CI
  - `chore(scope): :wrench:` for config changes
  - `chore(scope): :truck:` for moving/renaming files

Refer to the [GitHub emoji cheat sheet](https://github.com/ikatyang/emoji-cheat-sheet) for the full list. Do not use emojis outside this list. Always choose the most relevant emoji for your change.


## Body Instructions

- (Optional) Add a body section for additional context about the change.
- Explain WHY change was needed and contrast with previous behavior.
- For body: Use bullet points (`-`) for multiple items.

## Footer Instructions
