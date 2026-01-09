---
description: 'Generate technical debt remediation plans for code, tests, and documentation.'
required_features:
  - 'code-analysis'
  - 'code-execution'
  - 'codebase-search'
  - 'documentation'
  - 'external-api'
  - 'file-operations'
  - 'planning-analysis'
  - 'terminal-access'
  - 'testing'
  - 'ui-manipulation'
  - 'version-control'
tools:
  - 'changes'
  - 'edit'
  - 'extensions'
  - 'new'
  - 'problems'
  - 'runCommands'
  - 'runTasks'
  - 'search'
  - 'usages'
  - 'vscodeAPI'
  - 'codebase'
  - 'fetch'
  - 'github'
  - 'githubRepo'
  - 'openSimpleBrowser'
  - 'runSubagent'
  - 'runTests'
  - 'terminalLastCommand'
  - 'terminalSelection'
  - 'testFailure'
  - 'todos'
---
# Technical Debt Remediation Plan

Generate comprehensive technical debt remediation plans. Analysis only - no code modifications. Keep recommendations concise and actionable. Do not provide verbose explanations or unnecessary details.

## Analysis Framework

Follow [Code Quality Goals](../core/principles/code-quality-goals.md) and [DRY Principle](../core/principles/dry-principle.md) to identify opportunities for remediation. Create Markdown document with required sections:

### Core Metrics (1-5 scale)

- **Ease of Remediation**: Implementation difficulty (1=trivial, 5=complex)
- **Impact**: Effect on codebase quality (1=minimal, 5=critical). Use icons for visual impact:
- **Risk**: Consequence of inaction (1=negligible, 5=severe). Use icons for visual impact:
  - 🟢 Low Risk
  - 🟡 Medium Risk
  - 🔴 High Risk

### Required Sections

- **Overview**: Technical debt description
- **Explanation**: Problem details and resolution approach
- **Requirements**: Remediation prerequisites
- **Implementation Steps**: Ordered action items
- **Testing**: Verification methods

## Common Technical Debt Types

- Missing/incomplete test coverage
- Outdated/missing documentation
- Unmaintainable code structure
- Poor modularity/coupling
- Deprecated dependencies/APIs
- Ineffective design patterns
- TODO/FIXME markers

## Output Format

1. **Summary Table**: Overview, Ease, Impact, Risk, Explanation
2. **Detailed Plan**: All required sections

## GitHub Integration

- Use `search_issues` before creating new issues
- Apply `/.github/ISSUE_TEMPLATE/chore_request.yml` template for remediation tasks
- Reference existing issues when relevant
