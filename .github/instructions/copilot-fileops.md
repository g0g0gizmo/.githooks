# Copilot File Operations Configuration

**Purpose**: Single source of truth for all file paths, naming conventions, and output specifications. All prompts, agents, and instructions reference this file instead of hardcoding paths.

**Benefit**: Changing a file location or naming pattern requires only one update here, automatically cascading to all dependent content.

---

## Directory Structure

### Root-Level Directories
```
├── agents/                 # Agent definitions (.agent.md files)
├── collections/            # Collections of related content (.collection.yml files)
├── core/                   # Core principles and configuration
│   ├── principles/         # Foundational principles (.md files)
│   ├── copilot-fileops.md # This file - centralized configuration
│   └── LINKING.md         # Principle reference mappings
├── docs/                   # Documentation and generated files
│   ├── adr/              # Architecture Decision Records
│   ├── spikes/           # Technical spikes and research
│   └── README.*.md        # Generated documentation
├── instructions/           # Coding standards and best practices
├── pipeline/              # Workflow definitions and automation
│   ├── definitions/       # Pipeline definitions
│   └── prompts/          # Pipeline-specific prompts
├── prompts/               # Reusable prompts and chatmodes
├── scripts/               # Automation and utility scripts
└── .github/
    ├── copilot-instructions.md   # VSCode Copilot configuration
    ├── prompts/                  # Internal prompt storage
    └── instructions/             # Internal instruction storage (memory, workflows)
```

---

## File Type Specifications

### 1. PLANS - Implementation Plans

**Purpose**: Structured implementation roadmaps for features, refactoring, or infrastructure work.

**Location**: `.github/prompts/`

**Naming Convention**: `YYYYMMDD-HHMM-{description}.plan.md`

**Examples**:
- `20231128-1430-auth-refactoring.plan.md`
- `20231128-1445-database-migration.plan.md`
- `20231128-1500-api-versioning.plan.md`

**Metadata**:
```yaml
---
created: YYYY-MM-DD HH:MM UTC
purpose: "Brief description of plan"
target_deliverable: "Main outcome or feature"
estimated_phases: N
---
```

**Structure**:
- Phase breakdown (numbered, sequential)
- Dependencies between phases
- Success criteria per phase
- Risk assessment and mitigation
- Rollback procedures (if applicable)

---

### 2. RESEARCH - Technical Investigation

**Purpose**: Detailed research, spike results, and investigation findings.

**Location**: `.github/prompts/` or `docs/spikes/`

**Naming Convention**: `YYYYMMDD-HHMM-{description}.research.md` or `{category}-{description}-spike.md`

**Examples**:
- `.github/prompts/20231128-1400-oauth-evaluation.research.md`
- `docs/spikes/api-copilot-integration-spike.md`
- `docs/spikes/performance-realtime-audio-spike.md`

**Metadata**:
```yaml
---
type: "research|spike"
created: YYYY-MM-DD HH:MM UTC
topic: "Main investigation topic"
related_plan: "{plan-name}" # Optional - if this feeds a plan
---
```

**Structure**:
- Research question or scope
- Investigation methodology
- Findings and analysis
- Recommendations
- References and resources

---

### 3. IMPLEMENTATION - Feature/Fix Implementation

**Purpose**: Specific implementation instructions for a feature or fix.

**Location**: `prompts/` (for reusable) or `.github/prompts/` (for project-specific)

**Naming Convention**: `{domain}-{feature}.prompt.md` or `implement-{description}.prompt.md`

**Examples**:
- `prompts/dotnet-xunit.prompt.md` (reusable)
- `.github/prompts/implement-auth-refactoring.prompt.md` (project-specific)

**Frontmatter**:
```yaml
---
description: "Single-line description"
domain: "technology or area" # Optional
type: "implementation|feature|fix|refactoring"
related_plan: "YYYYMMDD-HHMM-description.plan.md" # Optional
related_research: "path/to/research.md" # Optional
---
```

---

### 4. ADR - Architecture Decision Records

**Purpose**: Record significant architectural decisions and their rationale.

**Location**: `docs/adr/`

**Naming Convention**: `adr-{NNNN}-{title-slug}.md`

**Examples**:
- `docs/adr/adr-0001-database-selection.md`
- `docs/adr/adr-0002-microservices-architecture.md`
- `docs/adr/adr-0003-authentication-strategy.md`

**Numbering**: Use next sequential 4-digit number (0001, 0002, 0003, etc.)

**Metadata**:
```yaml
---
status: "Proposed|Accepted|Deprecated|Superseded"
date: YYYY-MM-DD
decision_id: "ADR-NNNN"
related_plans: ["plan-1", "plan-2"] # Optional
---
```

**Required Sections**:
1. Context - Problem and background
2. Decision - What was decided
3. Rationale - Why this decision
4. Consequences - Positive and negative impacts
5. Alternatives - Other options considered

---

### 5. AGENTS - Custom AI Agents

**Purpose**: Specialized AI agents for specific roles or domains.

**Location**: `agents/`

**Naming Convention**: `{role|domain}-{specialty}.agent.md`

**Examples**:
- `agents/expert-dotnet-software-engineer.agent.md`
- `agents/principal-software-engineer.agent.md`
- `agents/proxmox-infrastructure-architect.agent.md`

**Frontmatter**:
```yaml
---
description: "Single-line description of agent purpose"
type: "agent"
domain: "primary domain"
tools: [list of available tools]
---
```

---

### 6. COLLECTIONS - Themed Content Groups

**Purpose**: Organize related prompts, agents, and instructions by theme.

**Location**: `collections/`

**Naming Convention**: `{theme}-{specialty}.collection.yml`

**Examples**:
- `collections/dotnet-development.collection.yml`
- `collections/infrastructure-automation.collection.yml`

**Structure**:
```yaml
name: "Collection Name"
description: "Purpose and scope"
type: "development|infrastructure|testing|documentation"
items:
  - type: "agent|prompt|instruction"
    path: "agents/..."
  - type: "agent|prompt|instruction"
    path: "prompts/..."
```

---

### 7. INSTRUCTIONS - Coding Standards & Best Practices

**Purpose**: Language-specific or framework-specific guidelines and standards.

**Location**: `instructions/`

**Naming Convention**: `{language|framework}-{specialty}.instructions.md`

**Examples**:
- `instructions/csharp.instructions.md`
- `instructions/typescript-5-es2022.instructions.md`
- `instructions/dotnet-architecture-good-practices.instructions.md`
- `instructions/testing-jest-typescript.instructions.md`

**Frontmatter**:
```yaml
---
description: "Single-line description"
type: "language|framework|methodology"
applies_to: "technology or language"
related_principles: ["principle-1", "principle-2"]
---
```

---

### 8. MEMORY - Context & State Storage

**Purpose**: Persistent user preferences, project context, and agent state.

**Location**: `.github/instructions/memory.instruction.md`

**Usage**: Accessed by agents to understand user preferences and project state.

**Frontmatter**:
```yaml
---
type: "memory"
scope: "user|project|session"
updated: YYYY-MM-DD HH:MM UTC
---
```

**Structure**:
- User preferences and settings
- Project-specific context
- Previous decisions and their reasoning
- Known constraints and requirements

---

### 9. PROMPTS - Reusable Task Templates

**Purpose**: Reusable prompts for common AI tasks.

**Location**: `prompts/`

**Naming Convention**: `{action}-{domain|target}.prompt.md`

**Examples**:
- `prompts/create-readme.prompt.md`
- `prompts/test-generation.prompt.md`
- `prompts/code-review.prompt.md`
- `prompts/doc-update-oo-component.prompt.md`

**Frontmatter**:
```yaml
---
description: "Single-line description of prompt purpose"
type: "prompt|chatmode"
domain: "applicable domain or empty for cross-cutting"
related_principles: ["principle-1", "principle-2"]
---
```

---

### 10. SPECIFICATIONS - Requirements & Specs

**Purpose**: Formal specifications for features, APIs, or systems.

**Location**: `docs/specs/` or `.github/specs/`

**Naming Convention**: `{domain}-{feature}.spec.md` or `spec-{YYYYMMDD}-{description}.md`

**Examples**:
- `docs/specs/api-authentication.spec.md`
- `docs/specs/database-schema.spec.md`

**Metadata**:
```yaml
---
type: "specification"
status: "Draft|Review|Approved|Implemented"
version: "1.0"
last_updated: YYYY-MM-DD
approval_required_from: ["role1", "role2"]
---
```

---

## Variable Substitution & Dynamic Paths

Use these variables in prompts when paths need to be dynamic:

| Variable | Example | Purpose |
|----------|---------|---------|
| `${input:Purpose}` | User-provided description | Prompt input from user |
| `${input:FolderPath\|default/path}` | Dynamic folder with fallback | User-specified location |
| `${YYYYMMDD-HHMM}` | Current timestamp | Unique timestamped filenames |
| `${UUID}` | Unique identifier | When order doesn't matter |
| `${SequentialID}` | 0001, 0002, 0003 | For ADRs and ordered items |

---

## Output Format Standards

### Markdown Frontmatter (YAML)
All content files MUST start with YAML frontmatter:
```yaml
---
description: "Clear, single-line description under 100 characters"
type: "document type"
created: YYYY-MM-DD HH:MM UTC
updated: YYYY-MM-DD HH:MM UTC # Update when modified
status: "draft|review|approved|published"
related_files: ["path/to/file1.md", "path/to/file2.md"]
---
```

### Header Structure
```markdown
# Main Title

## Section 1
### Subsection 1.1

## Section 2
```

### Link Format
All principle references use GitHub markdown syntax:
```markdown
[Principle Name](../core/principles/principle-name.md)
```

### Code Blocks
Always specify language:
````markdown
```csharp
// Code here
```
````

---

## File Output Checklist

When creating any content file, follow this checklist:

- [ ] File location matches specification above
- [ ] Naming convention follows pattern
- [ ] YAML frontmatter included with required fields
- [ ] Description is single-line and under 100 characters
- [ ] All principle references use `[Name](path)` format
- [ ] Headers follow standard structure (# Main, ## Sections)
- [ ] Code blocks specify language
- [ ] Related files are cross-referenced
- [ ] No hardcoded paths (except in copilot-fileops.md)
- [ ] Links to core principles where applicable

---

## Principle References

All file operation decisions are grounded in core principles:

- [DRY (Don't Repeat Yourself)](principles/dont-repeat-yourself.md) - Centralize configuration so changes only happen once
- [Problem Decomposition](principles/problem-decomposition.md) - Separate concerns by file type and purpose
- [Design by Contract](principles/design-by-contract.md) - Clear specifications for each file type
- [Orthogonality](principles/orthogonality.md) - Files should be independent and self-contained
- [KISS (Keep It Simple, Stupid)](principles/KISS.md) - Standard patterns are easier to follow than custom variations

---

## Usage Examples

### Reference from Prompts
```markdown
**Output Location**: See [Copilot File Operations - PLANS](../core/copilot-fileops.md#1-plans---implementation-plans)

Output file path: `.github/prompts/YYYYMMDD-HHMM-{description}.plan.md`
```

### Reference from Agents
```markdown
## File Operations

This agent follows the [Copilot File Operations Configuration](../core/copilot-fileops.md).

When creating research documents, use:
**Location**: See [File Operations - RESEARCH](../core/copilot-fileops.md#2-research---technical-investigation)
```

### Reference in CLAUDE.md Documentation
```markdown
All content must follow the standards defined in:
[Copilot File Operations Configuration](core/copilot-fileops.md)
```

---

## Migration Notes

### From Old to New Structure
| Old Pattern | New Pattern | Location |
|------------|------------|----------|
| `${input:FolderPath\|docs/spikes}` | `docs/spikes/` | copilot-fileops.md #5 |
| `.github\prompts\YYYYMMDD-HHMM-*.plan.md` | `.github/prompts/` + naming | copilot-fileops.md #1 |
| `/docs/adr/adr-NNNN-[slug].md` | `docs/adr/` + naming | copilot-fileops.md #4 |

---

## Maintenance

**Last Updated**: 2025-11-28

**Custodian**: Copilot File Operations

**Change Process**:
1. Update this file with new standards
2. Update all dependent prompts/agents to reference it
3. Commit with message: `docs(fileops): {change summary}`
4. Document change in CLAUDE.md

**Next Review**: When adding 5+ new content types or significant directory restructuring
