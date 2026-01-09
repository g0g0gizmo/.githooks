---
mode: agent
model: claude-3.5-sonnet
tools:
  - runCommands
description: 'Scaffold VS Code Copilot workspace folder structure only: creates .github directory hierarchy with agents, instructions, prompts, tracking, copilot, and workflows folders.'
---

# Scaffold VS Code Copilot Workspace Folders

## Core Principles

This content applies the following foundational principles:

- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain high standards for clarity and quality
- [DRY (Don't Repeat Yourself)](../core/principles/dry-principle.md) - Promote reusability and efficiency
- [Problem Decomposition](../core/principles/problem-decomposition.md) - Break complex setup into manageable steps

---

## Task: Create Workspace-Level Folder Structure Only

Create the essential VS Code Copilot directory hierarchy in this repository.

**Scope**: Folders only - No file generation.

---

## Folder Structure to Create

```
.github/
├── agents/                              # Custom agents
├── instructions/                        # Technology-specific instructions
├── prompts/                             # Reusable workflow prompts
├── copilot/
│   ├── guidelines/                      # Source of truth standards
│   └── tracking/                        # Tracking and change management
│   └── mcp/                             # MCP server configurations
└── workflows/                           # GitHub Actions workflows

.vscode/                                 # Create if not exists

toolsets/                                # Tool configurations
```

---

## Execution Steps

Create all folders using command-line:

```bash
mkdir -p .github/agents
mkdir -p .github/instructions
mkdir -p .github/prompts
mkdir -p .github/tracking
mkdir -p .github/copilot/guidelines
mkdir -p .github/copilot/mcp
mkdir -p .github/workflows
mkdir -p .vscode
mkdir -p toolsets
```

Or combined:

```bash
mkdir -p .github/{agents,instructions,prompts,tracking,copilot/{guidelines,mcp},workflows} .vscode toolsets
```

---

## Verification

After creation, verify structure:

```bash
tree .github -L 2
```

Expected output:

```
.github/
├── agents/
├── copilot/
│   ├── guidelines/
│   └── mcp/
├── instructions/
├── tracking/
├── prompts/
└── workflows/
```

---

## Success Criteria

- [ ] `.github/agents/` folder exists
- [ ] `.github/instructions/` folder exists
- [ ] `.github/prompts/` folder exists
- [ ] `.github/tracking/` folder exists
- [ ] `.github/copilot/guidelines/` folder exists
- [ ] `.github/copilot/mcp/` folder exists
- [ ] `.github/workflows/` folder exists
- [ ] `.vscode/` folder exists (or created)
- [ ] `toolsets/` folder exists

---

## Next Steps

Once folders are created:

1. **Add .gitkeep files** to ensure empty folders are tracked in git

   ```bash
   touch .github/agents/.gitkeep
   touch .github/instructions/.gitkeep
   touch .github/prompts/.gitkeep
   touch .github/tracking/.gitkeep
   touch .github/copilot/guidelines/.gitkeep
   touch .github/copilot/mcp/.gitkeep
   touch .github/workflows/.gitkeep
   touch toolsets/.gitkeep
   ```

2. **Commit to version control**

   ```bash
   git add .github .vscode toolsets
   git commit -m "chore: scaffold VS Code Copilot workspace folder structure"
   ```

3. **Begin using the structure** - Add files to these folders as needed
   - Add agents to `.github/agents/`
   - Add instructions to `.github/instructions/`
   - Add prompts to `.github/prompts/`
   - Add planning docs to `.github/tracking/`
   - Add guidelines to `.github/copilot/guidelines/`
   - Add MCP config to `.github/copilot/mcp/`
   - Add workflows to `.github/workflows/`
   - Add toolset configs to `toolsets/`

---

## Complete
