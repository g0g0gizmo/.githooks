---
name: create-pr
description: 'Generate comprehensive pull request description with Jira links, changes summary, decisions, and quality checklist'
model: anthropic/claude-3.7-sonnet
target: markdown
metadata:
  category: git
  version: 1.0.0
  tags:
    - pull-request
    - jira
    - code-review
    - quality-gates
  owner: automation-team
---

# Create Pull Request Description

**Purpose:** Generate a comprehensive, structured pull request description that includes Jira references, changes summary, architectural decisions, testing evidence, and quality checklist.

## Input Variables

- `{jiraKey}` - Jira issue key (e.g., "JIRA-123")
- `{jiraTitle}` - Jira issue title
- `{jiraUrl}` - Full URL to Jira issue
- `{jiraType}` - Type of work: "Feature", "Bug Fix", "Chore", "Refactor"
- `{changes_summary}` - JSON object describing code changes
  - Format: `{"added": [...], "modified": [...], "removed": [...]}`
- `{decisions}` - Array of decision log references
  - Format: `[{"title": "...", "path": "..."}]`
- `{tests}` - JSON object with test evidence
  - Format: `{"coverage_before": 85, "coverage_after": 92, "tests_added": 5, "screenshot_paths": [...], "commands": [...]}`

## Output Format

Generate a pull request description following this structure:

```markdown
## Summary

{summary_paragraph}

## Jira Reference

**Issue:** [{jiraKey}]({jiraUrl})
**Type:** {jiraType}
**Status:** In Review

## Changes

### Added
{added_items}

### Modified
{modified_items}

### Removed
{removed_items}

## Testing

### Test Coverage
- [x] Unit tests added/updated (coverage: {coverage_before}% → {coverage_after}%)
- [x] Integration tests passing
- [x] Manual testing completed

### Test Evidence
{test_evidence}

### Test Commands
{test_commands}

## Decisions

{decisions_section}

## Risk Assessment

**Risk Level:** {risk_level}

### Identified Risks
{risk_items}

### Mitigations
{mitigation_items}

## Checklist

### Code Quality
- [x] Code follows project conventions
- [x] No commented-out code or debug statements
- [x] Error handling implemented
- [x] Logging added for key operations

### Testing
- [x] All tests passing locally
- [x] CI/CD pipeline green
- [x] Test coverage maintained or improved
- [x] Edge cases covered

### Documentation
- [x] README updated (if needed)
- [x] API documentation updated (if applicable)
- [x] Decision log entry created (if architectural)
- [x] Migration guide provided (if breaking)

### Security
- [x] No secrets or credentials committed
- [x] Input validation implemented
- [x] Security scan passed
- [x] Dependencies updated

### Review
- [x] Self-review completed
- [ ] Requested reviewers assigned
- [ ] All comments addressed
- [ ] Approved by required reviewers
```

## Generation Rules

### Summary Section

**Requirements:**
- 2-3 sentences maximum
- Written for non-technical stakeholders
- States business value or impact
- Avoids implementation details

**Template:**
```
This PR implements {jiraTitle} to address {business_need}.
{High-level approach summary}.
{Expected impact or benefit}.
```

**Example:**
```markdown
## Summary

This PR implements OAuth2 authentication to support enterprise SSO requirements.
The solution uses dynamic provider configuration via environment variables, enabling support for Google, Microsoft, and Okta without code changes.
This improves security by delegating authentication to trusted identity providers and eliminates password management.
```

### Changes Section

**Extract from `{changes_summary}` JSON:**

```json
{
  "added": [
    "OAuth2 authentication provider integration",
    "Environment configuration for SSO settings",
    "Provider selection UI component"
  ],
  "modified": [
    "User authentication flow to support multiple providers",
    "Login UI to display provider selection",
    "Session management to handle OAuth tokens"
  ],
  "removed": [
    "Deprecated basic auth fallback",
    "Legacy password reset flow"
  ]
}
```

**Format:**
```markdown
### Added
- OAuth2 authentication provider integration
- Environment configuration for SSO settings
- Provider selection UI component

### Modified
- User authentication flow to support multiple providers
- Login UI to display provider selection
- Session management to handle OAuth tokens

### Removed
- Deprecated basic auth fallback
- Legacy password reset flow
```

### Testing Section

**Extract from `{tests}` JSON:**

```json
{
  "coverage_before": 85,
  "coverage_after": 92,
  "tests_added": 12,
  "screenshot_paths": ["screenshots/oauth-selection.png"],
  "log_output": "Test results: 45/45 passing",
  "performance_metric": "Login time < 500ms (measured: 320ms)",
  "commands": ["npm test", "npm run test:integration"]
}
```

**Generate:**
```markdown
### Test Coverage
- [x] Unit tests added/updated (coverage: 85% → 92%)
- [x] Integration tests passing
- [x] Manual testing completed

### Test Evidence
- Screenshot: OAuth provider selection UI (screenshots/oauth-selection.png)
- Log output: Test results: 45/45 passing
- Performance: Login time < 500ms (measured: 320ms)

### Test Commands
\`\`\`powershell
npm test
npm run test:integration
\`\`\`
```

### Decisions Section

**Extract from `{decisions}` array:**

```json
[
  {
    "title": "OAuth Provider Selection Strategy",
    "path": "../../obsidian/decisions/oauth-provider-selection.md",
    "context": "Multiple SSO providers needed",
    "chosen": "Dynamic configuration via environment variables",
    "rationale": "Flexibility without code changes"
  }
]
```

**Generate:**
```markdown
## Decisions

### Architectural Decisions
- [DECISION: OAuth Provider Selection Strategy](../../obsidian/decisions/oauth-provider-selection.md)
  - Context: Multiple SSO providers needed
  - Options: Hardcode vs Dynamic configuration
  - Chosen: Dynamic via environment variables
  - Rationale: Flexibility without code changes

### Trade-offs
- **Performance:** Added 50ms for provider discovery (acceptable for login flow)
- **Complexity:** Increased configuration surface (mitigated with validation)
- **Security:** Delegated to OAuth providers (reduced attack surface)
```

### Risk Assessment Section

**Risk Level Determination:**
- **Low:** < 100 lines changed, no breaking changes, isolated module
- **Medium:** 100-400 lines, minor breaking changes, affects 1-2 modules
- **High:** > 400 lines, major breaking changes, affects core functionality

**Template:**
```markdown
## Risk Assessment

**Risk Level:** {Low | Medium | High}

### Identified Risks
- **{Risk Category}:** {Specific risk description with severity}
- **{Risk Category}:** {Specific risk description with severity}

### Mitigations
- {Risk Category}: {Mitigation strategy and verification}
- {Risk Category}: {Mitigation strategy and verification}
```

**Example:**
```markdown
## Risk Assessment

**Risk Level:** Medium

### Identified Risks
- **Breaking Change:** Old clients using basic auth will fail after deployment
- **Performance:** Provider discovery adds 50ms to login flow
- **Configuration:** Missing environment variables cause startup failure

### Mitigations
- Breaking Change: Deprecation notice sent to API consumers; 30-day transition period
- Performance: Acceptable for login flow; provider list cached after first request
- Configuration: Startup validation checks for required env vars; clear error messages
```

## Example Prompts

### Example 1: Feature Implementation

**Input:**
```json
{
  "jiraKey": "JIRA-123",
  "jiraTitle": "OAuth2 SSO Integration",
  "jiraUrl": "https://jira.example.com/browse/JIRA-123",
  "jiraType": "Feature",
  "changes_summary": {
    "added": ["OAuth2 provider integration", "SSO configuration"],
    "modified": ["Authentication flow", "Login UI"],
    "removed": ["Basic auth fallback"]
  },
  "decisions": [
    {
      "title": "OAuth Provider Selection",
      "path": "../../obsidian/decisions/oauth-provider.md"
    }
  ],
  "tests": {
    "coverage_before": 85,
    "coverage_after": 92,
    "tests_added": 12,
    "commands": ["npm test"]
  }
}
```

**Output:** (Full PR description as shown in Output Format section above)

### Example 2: Bug Fix

**Input:**
```json
{
  "jiraKey": "JIRA-456",
  "jiraTitle": "Fix Email Validation Regex",
  "jiraUrl": "https://jira.example.com/browse/JIRA-456",
  "jiraType": "Bug Fix",
  "changes_summary": {
    "added": [],
    "modified": ["Email validation regex pattern"],
    "removed": []
  },
  "decisions": [],
  "tests": {
    "coverage_before": 87,
    "coverage_after": 88,
    "tests_added": 3,
    "commands": ["npm test -- validation.test.js"]
  }
}
```

**Output:**
```markdown
## Summary

This PR fixes email validation to support plus addressing (e.g., user+tag@example.com).
The regex pattern now correctly accepts all RFC-compliant email formats.
This resolves JIRA-456 where valid emails were incorrectly rejected.

## Jira Reference

**Issue:** [JIRA-456](https://jira.example.com/browse/JIRA-456)
**Type:** Bug Fix
**Status:** In Review

## Changes

### Modified
- Email validation regex pattern to support plus addressing

## Testing

### Test Coverage
- [x] Unit tests added/updated (coverage: 87% → 88%)
- [x] Regression test added for reported examples
- [x] Manual testing with various email formats

### Test Evidence
- Regression test: Validates all reported failing email examples
- Manual test: Verified fix with 10+ email format variations

### Test Commands
\`\`\`powershell
npm test -- validation.test.js
\`\`\`

## Decisions

No architectural decisions required for this bug fix.

## Risk Assessment

**Risk Level:** Low

### Identified Risks
- **Regex Complexity:** New pattern slightly more complex

### Mitigations
- Regex Complexity: Pattern reviewed against RFC 5322 spec; unit tests cover edge cases

## Checklist

[Standard checklist with all items checked]
```

## Quality Guidelines

### Completeness
- Include all required sections
- Check all applicable checklist items
- Provide concrete test evidence

### Clarity
- Use specific terminology
- Avoid vague descriptions ("improved code")
- Include measurable outcomes (coverage %, performance ms)

### Traceability
- Link all related Jira issues
- Reference decision documents
- Mention impacted modules/components

## Integration Context

This prompt is used by:

1. **Git Jira Governor Agent** (`.github/agents/git-jira-governor.agent.md`)
   - Populates PR description when opening PR from branch
   - Validates Jira key from branch name
   - Auto-links to decision documents

2. **PR Creation Command** (`dailyctl pr create`)
   - Analyzes git diff for changes summary
   - Fetches Jira metadata
   - Generates test commands from package.json scripts

3. **Workflow Orchestrator** (`.github/agents/workflow-orchestrator.agent.md`)
   - Combines with branch/commit conventions
   - Ensures quality gates before merge

## Error Handling

### Missing Jira Data
If Jira API unavailable:
```markdown
**Issue:** JIRA-123 (Unable to fetch details - verify manually)
```

### No Decisions
If `{decisions}` array is empty:
```markdown
## Decisions

No architectural decisions were made for this change.
```

### Zero Test Coverage Change
If coverage unchanged:
```markdown
- [x] Unit tests passing (coverage maintained: 87%)
```

## Related Documentation

- [PR Quality Gates](../instructions/pr-quality-gates.instructions.md)
- [Branch & Commit Policy](../instructions/branch-commit-policy.instructions.md)
- [Decision Logging Pattern](../../docs/my-daily-needs.md#decision-logging-pattern)
