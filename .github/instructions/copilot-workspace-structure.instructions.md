---
description: 'GitHub Copilot workspace file organization - official structure based on Microsoft and GitHub documentation'
applyTo: '**'
---


## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](dry-principle.instructions.md) - Single source of truth for file locations
- [Atomic Notes](atomic-notes.instructions.md) - Organize content into focused, reusable units
- [Linked Notes](linked-notes-principle.instructions.md) - Cross-reference related content

When implementing these guidelines, always consider how they reinforce these core principles.

# GitHub Copilot Workspace File Organization

## Overview

This document defines the **workspace-level** file organization structure for GitHub Copilot based on official VS Code and GitHub best practices. It specifies where to place custom instructions, prompts, documentation, and tracking files within your project repository.

**Purpose**: Single source of truth for workspace file paths, naming conventions, and organizational standards.

**Benefit**: Team-shared configurations committed to version control, ensuring consistent AI assistance across all developers.

**Based on**:

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/copilot-customization)
- [VS Code Workspace Context](https://code.visualstudio.com/docs/copilot/workspace-context)

---

## Workspace Directory Structure

All workspace-level Copilot files are organized under `.github/` for team collaboration and version control.

```
.github/
├── copilot-instructions.md           # Repository-wide instructions (OFFICIAL)
├── instructions/                     # Path-specific instructions (OFFICIAL)
│   └── *.instructions.md
├── prompts/                          # Reusable task prompts
│   └── *.prompt.md
├── plans/                            # Implementation plans and strategy
│   └── YYYYMMDDHHMM-*.plan.md            # AI-generated summaries should just check off plans with comments on implementation
├── research/                         # Research documentation
│   └── YYYYMMDDHHMM-*.research.md
├── actions/                          # Reusable GitHub Actions (OFFICIAL)
│   └── {action-name}/
│       ├── action.yml
│       └── README.md
└── workflows/                        # GitHub Actions workflows (OFFICIAL)
    └── *.yml

docs/                                 # Human-authored documentation
├── architecture/
├── api/
└── guides/

AGENTS.md                             # Agent instructions (OFFICIAL, optional)
CLAUDE.md                             # Claude-specific (alternative to AGENTS.md)
GEMINI.md                             # Gemini-specific (alternative to AGENTS.md)

.vscode/
├── settings.json                     # Workspace VS Code settings
└── mcp.json                          # MCP server configurations
```

---

## Directory Reference & Rationale

### `.github/` - Official Copilot Configuration Location

**Purpose**: Official location for all GitHub Copilot repository-level configurations.

**Reference**: [GitHub Docs - Adding Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

**Why this location**:

- Official GitHub standard for repository metadata and configurations
- Automatically discovered by GitHub Copilot
- Version controlled and shared across team
- Follows GitHub's established conventions (like `.github/workflows/`)

**Contains**:

- Custom instructions (repository-wide and path-specific)
- Prompts, plans, research, and summaries
- GitHub Actions workflows and reusable actions

---

### `.github/copilot-instructions.md` - Repository-Wide Instructions

**Purpose**: Apply instructions to all files in the repository.

**Reference**: [GitHub Docs - Creating Repository-Wide Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot#creating-repository-wide-custom-instructions)

**Why this location**:

- **Official GitHub specification**: Must be at `.github/copilot-instructions.md`
- Automatically loaded by GitHub Copilot for all chat interactions
- Applies to all files unless overridden by path-specific instructions

**File Limit**: Maximum 2 pages of content

**Scope**: All Copilot chat interactions in this repository

**Example Content**:

```markdown
# Repository Coding Standards

- Use TypeScript for new features
- Follow functional programming patterns
- Write tests for all new code
- Use conventional commit messages
```

**When to Use**:

- Project-wide coding standards
- Team conventions and practices
- Build/test/deployment instructions
- Architecture patterns

---

### `.github/instructions/` - Path-Specific Instructions

**Purpose**: Apply instructions to specific file patterns using glob syntax.

**Reference**: [GitHub Docs - Creating Path-Specific Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot#creating-path-specific-custom-instructions)

**Why this location**:

- **Official GitHub specification**: Must be `.github/instructions/`
- Files must end with `.instructions.md`
- Requires `applyTo` frontmatter with glob pattern
- Combines with repository-wide instructions when applicable

**Required Frontmatter**:

```yaml
---
description: 'Brief description'
applyTo: '**/*.py'  # Glob pattern for file types
excludeAgent: 'code-review'  # Optional: exclude specific agents
---
```

**Glob Pattern Examples**:

- `**/*.py` - All Python files recursively
- `src/**/*.tsx` - All TypeScript React files in src/
- `**` - All files

**When to Use**:

- Language-specific coding standards (Python, TypeScript, etc.)
- Framework-specific rules (React, Django, etc.)
- Directory-specific conventions (tests/, docs/, etc.)

**Example**: `.github/instructions/python-standards.instructions.md`

```yaml
---
description: 'Python coding standards'
applyTo: '**/*.py'
---

# Python Standards

- Use type hints for all functions
- Follow PEP 8 style guide
- Use pytest for all tests
```

---

### `.github/prompts/` - Reusable Task Prompts

**Purpose**: Reusable templates for common development tasks.

**Reference**: [VS Code Docs - Prompt Files](https://code.visualstudio.com/docs/copilot/copilot-customization#prompt-files)

**Why this location**:

- Logical grouping with other Copilot configurations
- Version controlled and team-shared
- Discovered by workspace context indexing

**Naming Convention**: `{action}-{target}.prompt.md`

**Frontmatter**:

```yaml
---
mode: 'agent'
description: 'Brief description of prompt purpose'
---
```

**When to Use**:

- Scaffolding components, routes, or tests
- Code review checklists
- Documentation generation
- Refactoring patterns

**Example**: `.github/prompts/create-component.prompt.md`

```yaml
---
mode: 'agent'
description: 'Generate React component with TypeScript'
---

Create a React component with:
1. TypeScript interface for props
2. Functional component with hooks
3. Unit tests using Jest
4. Storybook story
```

---

### `.github/plans/` - Implementation Plans

**Purpose**: Strategic planning documents for features, refactoring, or architectural changes.

**Why this location**:

- Clear separation from code documentation
- Version controlled planning artifacts
- Team visibility into implementation strategy
- Historical record of design decisions

**Naming Convention**: `YYYYMMDD-{feature-name}.plan.md`

**When to Use**:

- Feature implementation plans
- Refactoring strategies
- Migration plans
- Architecture decision records (ADRs)

**Example**: `.github/plans/20251215-api-authentication.plan.md`

```markdown
# API Authentication Implementation Plan

## Objective
Implement JWT-based authentication for REST API

## Phases
1. Setup JWT library and configuration
2. Implement token generation/validation
3. Add authentication middleware
4. Update API endpoints

## Success Criteria
- All endpoints require valid JWT
- Token refresh mechanism working
- Tests cover all auth scenarios
```

---

### `.github/research/` - Research Documentation

**Purpose**: Technical research, alternatives analysis, and investigation results.

**Why this location**:

- Separates exploratory work from implementation
- Documents alternatives considered
- Reference for future similar decisions
- Knowledge sharing across team

**Naming Convention**: `YYYYMMDD-{topic}.research.md`

**When to Use**:

- Evaluating libraries or frameworks
- Investigating approaches to solve a problem
- Performance benchmarking
- Security analysis

**Example**: `.github/research/20251215-state-management.research.md`

```markdown
# State Management Research

## Alternatives Evaluated
1. Redux Toolkit
2. Zustand
3. Jotai

## Recommendation
Zustand - simpler API, smaller bundle size

## References
- [Zustand GitHub](https://github.com/pmndrs/zustand)
- [State Management Comparison](https://...)
```

---

### `.github/summaries/` - AI-Generated Summaries

**Purpose**: Copilot-generated summaries, meeting notes, and automated documentation.

**Why this location**:

- **Clear separation from human-authored documentation** (prevents confusion)
- Indicates content is AI-generated (requires human review)
- Allows different retention/archival policies
- Team knows these need validation before trusting

**Naming Convention**: `YYYYMMDD-{topic}.summary.md`

**When to Use**:

- Meeting summaries generated by AI
- Code review summaries
- Pull request summaries
- Change log summaries

**Important**: Content here is **AI-generated** and should be reviewed before being trusted or moved to official documentation.

**Example**: `.github/summaries/20251215-sprint-planning.summary.md`

```markdown
<!-- AI-GENERATED - Requires Human Review -->

# Sprint Planning Summary - Dec 15, 2025

## Attendees
[Generated from meeting captions]

## Key Decisions
[AI-extracted key points]

## Action Items
[AI-identified tasks]
```

---

### `docs/` - Human-Authored Documentation

**Purpose**: Official, human-written and maintained documentation.

**Why this location**:

- Standard location for project documentation
- Separate from `.github/` metadata
- Indexed by documentation generators
- Clear ownership and authority

**Structure**:

```
docs/
├── architecture/        # System design, diagrams, ADRs
├── api/                 # API reference documentation
├── guides/              # How-to guides and tutorials
├── setup/               # Installation and setup
└── contributing/        # Contribution guidelines
```

**When to Use**:

- User-facing documentation
- Developer guides
- API documentation
- Architecture diagrams

**Key Difference from `.github/summaries/`**:

- `docs/` = **Human-authored, authoritative, reviewed**
- `.github/summaries/` = **AI-generated, requires review, preliminary**

---

### `.github/actions/` - Reusable GitHub Actions

**Purpose**: Custom composite actions for CI/CD workflows.

**Reference**: [GitHub Docs - Creating Actions](https://docs.github.com/en/actions/creating-actions/about-custom-actions)

**Why this location**:

- **Official GitHub specification**: Actions stored in `.github/actions/` are auto-discoverable
- Can be referenced in workflows using relative paths
- Version controlled with repository code
- Enables code reuse across multiple workflows

**Structure**:

```
.github/actions/
├── build-and-test/
│   ├── action.yml          # Action definition
│   └── README.md           # Action documentation
├── deploy-staging/
│   ├── action.yml
│   └── README.md
└── notify-teams/
    ├── action.yml
    └── README.md
```

**When to Use**:

- Reusable CI/CD steps across multiple workflows
- Custom build/test/deploy logic
- Integration with external services
- Complex multi-step operations

**Example**: `.github/actions/build-and-test/action.yml`

```yaml
name: 'Build and Test'
description: 'Build application and run tests'
inputs:
  node-version:
    description: 'Node.js version'
    required: true
    default: '18'
runs:
  using: 'composite'
  steps:
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - name: Install dependencies
      run: npm ci
      shell: bash
    - name: Run tests
      run: npm test
      shell: bash
```

**Usage in Workflow**:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/build-and-test
        with:
          node-version: '20'
```

---

### `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` - Agent Instructions

**Purpose**: Instructions for specific AI agents (Claude, Gemini, custom agents).

**Reference**: [GitHub Docs - Agent Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot#creating-custom-instructions)

**Why this location**:

- **Official GitHub specification**: Can be anywhere in repository
- Nearest file to current location takes precedence
- Agent-specific behavior customization

**Important Limitation**:

- ❌ **Cannot link to or import user-level agents** from VS Code user folder (`%APPDATA%\Code\User\agents\`)
- ❌ **Cannot reference external files** outside the repository
- ✅ **Repository-scoped only**: Each repository must have its own agent instructions
- 💡 **Workaround**: Copy relevant user-level agent content into repository-specific `AGENTS.md` when needed

**When to Use**:

- Customize behavior for specific AI agents
- Override repository defaults for certain tasks
- Define agent-specific capabilities

**Example**: `AGENTS.md`

```markdown
# Agent Instructions

## Code Review Agent
- Check for security vulnerabilities
- Verify test coverage > 80%
- Ensure documentation is updated

## Planning Agent
- Read-only access to codebase
- Generate implementation plans only
- Do not modify code
```

---

### `.vscode/settings.json` - Workspace Settings

**Purpose**: VS Code workspace configuration including Copilot settings.

**Reference**: [VS Code Docs - Settings](https://code.visualstudio.com/docs/getstarted/settings#_workspace-settings)

**Why this location**:

- **Official VS Code specification**: Workspace-level settings
- Applies to all developers in the workspace
- Version controlled team configuration

**Copilot-Related Settings**:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.chat.localization": "en"
}
```

---

### `.vscode/mcp.json` - MCP Server Configurations

**Purpose**: Model Context Protocol server configurations for extending chat capabilities.

**Reference**: [VS Code Docs - MCP Servers](https://code.visualstudio.com/docs/copilot/chat/chat-tools)

**Why this location**:

- Workspace-specific tool integrations
- Version controlled server configurations
- Team-shared external service connections

**Example**:

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["path/to/github-server.js"]
    }
  }
}
```

---

## Workspace Context & Indexing

### How VS Code Indexes Your Workspace

**Automatic Indexing**:

- **Remote (GitHub/Azure DevOps)**: Creates index from repository (unlimited files)
- **Local**: Indexes up to 2,500 files from workspace
- **Hybrid**: Uses remote index + local uncommitted changes

**Reference**: [VS Code Docs - Workspace Context](https://code.visualstudio.com/docs/copilot/workspace-context)

**What Gets Indexed**:

- All files not matching `.gitignore` patterns
- Uncommitted changes (local only)
- File content, structure, and relationships

**Performance Best Practices**:

- Use `.gitignore` to exclude unnecessary files
- Prefer remote indexing for repositories > 2,500 files
- Push code to GitHub regularly for up-to-date remote index
- Avoid deep nesting (5 levels max for remote, 3 for local)

---

## File Naming Conventions

### General Rules

- **Use kebab-case**: `my-file-name.md` (NOT `MyFileName.md`)
- **Include type suffix**: `.instructions.md`, `.prompt.md`, `.plan.md`, `.research.md`, `.summary.md`
- **Date prefix for tracking**: `YYYYMMDD-` for timestamped files
- **Descriptive names**: Clear, concise, self-explanatory

### Specific Patterns

| Type                    | Pattern                        | Example                               |
| ----------------------- | ------------------------------ | ------------------------------------- |
| Repository Instructions | `copilot-instructions.md`      | `.github/copilot-instructions.md`     |
| Path-Specific           | `{topic}.instructions.md`      | `python-standards.instructions.md`    |
| Prompts                 | `{action}-{target}.prompt.md`  | `create-component.prompt.md`          |
| Plans                   | `YYYYMMDD-{topic}.plan.md`     | `20251215-api-auth.plan.md`           |
| Research                | `YYYYMMDD-{topic}.research.md` | `20251215-state-mgmt.research.md`     |
| Summaries               | `YYYYMMDD-{topic}.summary.md`  | `20251215-meeting.summary.md`         |
| GitHub Actions          | `{action-name}/action.yml`     | `build-and-test/action.yml`           |
| Agent Instructions      | `AGENTS.md`, `CLAUDE.md`       | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` |

---

## Frontmatter Standards

### Path-Specific Instructions

```yaml
---
description: 'Brief description'
applyTo: '**/*.{ext}'        # Glob pattern for file types
excludeAgent: 'agent-name'   # Optional: exclude specific agents
---
```

### Prompts

```yaml
---
mode: 'agent'
description: 'Brief description of prompt purpose'
---
```

### Plans

```yaml
---
description: 'Brief plan description'
status: 'draft|in-progress|completed'
owner: 'team-or-person'
---
```

### Research

```yaml
---
description: 'Research topic'
date: '2025-12-15'
alternatives: 3
recommendation: 'Chosen approach'
---
```

### Summaries (AI-Generated)

```yaml
---
description: 'Summary topic'
ai-generated: true
requires-review: true
source: 'meeting|pull-request|code-review'
---
```

### GitHub Actions

```yaml
name: 'Action Name'
description: 'Brief description of what the action does'
author: 'team-or-person'
inputs:
  input-name:
    description: 'Input description'
    required: true|false
    default: 'default-value'
outputs:
  output-name:
    description: 'Output description'
runs:
  using: 'composite|node20|docker'
  steps: [...]  # For composite actions
```

---

## Best Practices

### File Organization

✅ **DO**:

- Use `.github/` for all Copilot configurations
- Follow official naming conventions
- Include required frontmatter
- Separate AI-generated content from human-authored
- Keep repository-wide instructions under 2 pages
- Use path-specific instructions for different file types

❌ **DON'T**:

- Mix AI-generated summaries with official documentation
- Put instructions outside `.github/instructions/`
- Use inconsistent naming conventions
- Create files without frontmatter
- Duplicate content across locations
- Index build artifacts or node_modules

### Content Separation

| Type              | Location                | Authority      | Review Required       |
| ----------------- | ----------------------- | -------------- | --------------------- |
| **Official Docs** | `docs/`                 | Human-authored | No (already reviewed) |
| **AI Summaries**  | `.github/summaries/`    | AI-generated   | **Yes (required)**    |
| **Instructions**  | `.github/instructions/` | Human-authored | No (team standards)   |
| **Plans**         | `.github/plans/`        | Human-authored | No (strategic docs)   |
| **Research**      | `.github/research/`     | Human-authored | No (analysis docs)    |

---

## Integration with VS Code Copilot Chat

### Enable Custom Instructions

Add to `.vscode/settings.json`:

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "github.copilot.chat.chat.codeGeneration.useInstructionFiles": true
}
```

### Using Prompts

1. Create `.github/prompts/{name}.prompt.md`
2. Open Copilot Chat
3. Reference prompt: `@workspace /prompt-name`

### Agent Instructions

1. Create `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`
2. Place in repository (nearest file wins)
3. Instructions apply automatically

---

## Quick Reference

### Common Workspace Locations

```bash
# Repository-wide instructions
.github/copilot-instructions.md

# Path-specific instructions
.github/instructions/python-standards.instructions.md
.github/instructions/typescript-react.instructions.md

# Prompts
.github/prompts/create-component.prompt.md
.github/prompts/generate-tests.prompt.md

# Plans
.github/plans/20251215-feature-name.plan.md

# Research
.github/research/20251215-library-evaluation.research.md

# AI-Generated Summaries (require review)
.github/summaries/20251215-meeting-notes.summary.md

# GitHub Actions
.github/actions/build-and-test/action.yml
.github/actions/deploy-staging/action.yml

# Human-Authored Documentation (authoritative)
docs/architecture/system-design.md
docs/api/endpoints.md
docs/guides/getting-started.md

# Agent Instructions
AGENTS.md
CLAUDE.md
GEMINI.md

# Workspace Settings
.vscode/settings.json
.vscode/mcp.json
```

---

## Resources & Documentation

**Custom Instructions**:

- [GitHub Docs: Adding Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [VS Code: Copilot Customization](https://code.visualstudio.com/docs/copilot/copilot-customization)

**Workspace Context**:

- [VS Code: Workspace Context](https://code.visualstudio.com/docs/copilot/workspace-context)
- [VS Code: Copilot Overview](https://code.visualstudio.com/docs/copilot/overview)

**Prompt Crafting**:

- [VS Code: Prompt Crafting](https://code.visualstudio.com/docs/copilot/chat/prompt-crafting)

**Indexing & Performance**:

- [GitHub Code Search Technology](https://github.blog/2023-02-06-the-technology-behind-githubs-new-code-search)

---

## Summary: Key Differences

| Aspect             | This Structure                         | Reason                                           |
| ------------------ | -------------------------------------- | ------------------------------------------------ |
| **Scope**          | Workspace-only                         | Focus on team-shared, version-controlled configs |
| **Official Paths** | `.github/copilot-instructions.md`      | Official GitHub specification                    |
|                    | `.github/instructions/`                | Official GitHub specification                    |
| **Summaries**      | `.github/summaries/` (separate)        | AI-generated, requires review, not authoritative |
| **Documentation**  | `docs/` (authoritative)                | Human-authored, official, reviewed               |
| **Plans**          | `.github/plans/` (kept)                | Strategic planning, team visibility              |
| **References**     | Every folder includes rationale & docs | Clear justification from official sources        |

---

**Last Updated**: 2025-12-15

**Based on Official Documentation**: GitHub Copilot Docs, VS Code Copilot Customization, VS Code Workspace Context

**For any file creation or organization question, always reference this document as the single source of truth for workspace-level structure.**
