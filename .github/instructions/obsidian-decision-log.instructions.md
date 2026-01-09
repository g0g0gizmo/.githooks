---
description: 'Obsidian decision log format and documentation standards for architectural decisions'
applyTo: '**/*.md'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../../.github/copilot/copilot/guidelines/dry-principle.md) - Document decisions once, reference everywhere
- [Small Steps](../../.github/copilot/copilot/guidelines/small-steps.md) - Record decisions as they're made
- [Code Quality Goals](../../.github/copilot/copilot/guidelines/code-quality-goals.md) - Maintain decision traceability for long-term quality

When implementing these guidelines, always consider how they reinforce these core principles.

## Decision Log Structure

### Required Format

```markdown
# DECISION: [Concise Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Deciders:** [Names or roles]
**Tags:** #decision #architecture #[domain]

## Context

[Describe the situation requiring a decision. What problem are we solving? What constraints exist?]

## Options Considered

### Option 1: [Name]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

**Trade-offs:**
- [What we gain vs what we sacrifice]

### Option 2: [Name]

[Same structure as Option 1]

### Option 3: [Name]

[Same structure as Option 1]

## Decision

**Chosen:** [Option Name]

**Rationale:**
[Explain WHY this option was selected over alternatives. Reference specific constraints, requirements, or principles that drove the decision.]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Cost or limitation 1]
- [Cost or limitation 2]

### Neutral
- [Change that is neither positive nor negative]

## Implementation

**Timeline:** [When this will be implemented]
**Effort:** [T-shirt size: S/M/L or story points]
**Dependencies:** [What must be in place first]
**Risks:** [What could go wrong during implementation]

## Related Decisions

- [Link to related decision 1]
- [Link to related decision 2]

## References

- [Links to documentation, research, or external resources]
- [Jira ticket: JIRA-123]
- [PR: #850]

## Review

**Review Date:** [When to revisit this decision]
**Review Trigger:** [Conditions that would prompt re-evaluation]
```

### Complete Example

```markdown
# DECISION: OAuth2 Provider for SSO Integration

**Date:** 2025-11-30
**Status:** Accepted
**Deciders:** Engineering Team, Security Lead
**Tags:** #decision #architecture #authentication #security

## Context

We need to integrate enterprise single sign-on (SSO) for our application to support customers using Google Workspace, Microsoft 365, and Okta. Currently, we only support username/password authentication, which doesn't meet enterprise security requirements. The solution must support multiple identity providers without requiring code changes for each new provider.

**Constraints:**
- Must comply with OWASP authentication standards
- Cannot store passwords or credentials
- Must support provider discovery
- Implementation timeline: 2 weeks

## Options Considered

### Option 1: OAuth2 with Dynamic Provider Configuration

**Pros:**
- Industry standard protocol
- Supports multiple providers (Google, Microsoft, Okta)
- Configuration via environment variables
- Well-tested libraries available

**Cons:**
- Requires token refresh logic
- More complex than hardcoded providers
- Slightly higher initial development effort

**Trade-offs:**
- Gain flexibility at cost of initial complexity

### Option 2: SAML 2.0 Integration

**Pros:**
- Enterprise-standard protocol
- Strong security model
- Provider-agnostic

**Cons:**
- More complex implementation
- Requires XML parsing
- Less developer familiarity
- Longer implementation time (4 weeks)

**Trade-offs:**
- Higher security at cost of development time

### Option 3: Hardcoded OAuth per Provider

**Pros:**
- Simpler initial implementation
- Provider-specific optimizations possible

**Cons:**
- Code change required for each new provider
- Higher maintenance burden
- Doesn't scale

**Trade-offs:**
- Short-term speed at long-term maintenance cost

## Decision

**Chosen:** OAuth2 with Dynamic Provider Configuration

**Rationale:**

OAuth2 with dynamic configuration strikes the best balance between flexibility, security, and implementation effort. Key factors:

1. **Timeline:** Can be implemented in 2-week sprint using existing libraries (passport.js, OAuth2orize)
2. **Scalability:** Adding new providers requires only environment configuration, not code changes
3. **Security:** Meets OWASP standards; delegates authentication to trusted identity providers
4. **Developer Experience:** Team has OAuth2 experience from previous projects
5. **Industry Adoption:** OAuth2 is widely supported by all target identity providers

SAML was rejected due to 4-week implementation time. Hardcoded approach was rejected due to poor scalability and maintenance burden.

## Consequences

### Positive
- Customers can use existing enterprise identity providers
- No password storage or management required
- Easy to add new providers (config-only)
- Improved security posture
- Meets compliance requirements

### Negative
- Token refresh adds complexity to session management
- Requires environment configuration per deployment
- Slightly increased memory usage for token caching

### Neutral
- Changes authentication flow from form-based to redirect-based
- Adds OAuth2 library dependency (passport.js)

## Implementation

**Timeline:** Sprint 24 (2 weeks starting 2025-12-01)

**Effort:** Medium (5 story points)

**Dependencies:**
- Environment configuration for client IDs/secrets
- SSL certificate for callback URL
- Provider app registration (Google, Microsoft, Okta)

**Risks:**
- Provider-specific quirks may require custom handling
- Token storage strategy needs security review
- Migration path for existing username/password users

## Related Decisions

- [DECISION: Token Storage Strategy](./token-storage-strategy.md)
- [DECISION: Session Management Approach](./session-management.md)

## References

- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Jira Epic: JIRA-123](https://jira.example.com/browse/JIRA-123)
- [Research Spike: OAuth Provider Comparison](./research/oauth-providers.md)

## Review

**Review Date:** 2026-06-01 (6 months)

**Review Trigger:**
- New identity provider requirement not supported by OAuth2
- Performance issues with token refresh
- Security vulnerability discovered in OAuth2 flow
- Major version upgrade of OAuth library
```

## Section Guidelines

### Context Section

**Purpose:** Provide enough background for someone unfamiliar with the problem to understand why a decision is needed.

**Content:**
- Problem statement
- Business drivers
- Technical constraints
- Timeline requirements
- Stakeholder needs

**Best Practices:**
- Write for future readers (assume no context)
- Include links to related documentation
- Mention relevant principles or standards
- State constraints explicitly

### Options Considered Section

**Purpose:** Document alternatives evaluated to show decision was thoughtful.

**Minimum:** 2 options (usually 3-5)

**Content per Option:**
- Clear name describing the approach
- Pros: 2-5 advantages
- Cons: 2-5 disadvantages
- Trade-offs: What's gained vs sacrificed

**Best Practices:**
- Present options neutrally (don't favor chosen option yet)
- Include "do nothing" option when relevant
- Mention implementation effort differences
- Reference research or prototypes

### Decision Section

**Purpose:** State what was chosen and why.

**Content:**
- Explicitly name chosen option
- Provide detailed rationale (3-5 paragraphs)
- Reference specific factors from Context
- Explain why alternatives were rejected

**Best Practices:**
- Use data to support rationale when available
- Mention who made the decision
- Reference principles or standards applied
- Be honest about trade-offs accepted

### Consequences Section

**Purpose:** Document expected outcomes (positive, negative, neutral).

**Content:**
- Positive: Benefits expected
- Negative: Costs or limitations accepted
- Neutral: Changes without clear value judgment

**Best Practices:**
- Be realistic about negative consequences
- Don't minimize downsides
- Include both immediate and long-term consequences
- Mention impact on different stakeholders

### Implementation Section

**Purpose:** Bridge decision to execution.

**Content:**
- Timeline for implementation
- Effort estimate
- Dependencies required
- Risks during implementation

**Best Practices:**
- Use concrete dates or sprint numbers
- Identify blocking dependencies early
- Flag risks that might invalidate decision
- Link to implementation plan if available

## File Naming Convention

Decision logs stored in Obsidian vault:

```
{ObsidianVault}/
└── Decisions/
    ├── oauth-provider-selection.md
    ├── token-storage-strategy.md
    └── session-management.md
```

**Pattern:** `{topic}-{aspect}.md` (kebab-case)

**Examples:**
- `authentication-oauth-provider.md`
- `database-schema-migration.md`
- `api-rate-limiting-strategy.md`

## Status Lifecycle

**Proposed** → **Accepted** → **Deprecated** → **Superseded**

- **Proposed:** Under consideration, not yet implemented
- **Accepted:** Decided and being/has been implemented
- **Deprecated:** Still in use but discouraged for new work
- **Superseded:** Replaced by newer decision (link to replacement)

**Status Updates:**

When deprecating:
```markdown
**Status:** Deprecated (Superseded by [New Decision](./new-decision.md))
**Deprecation Date:** YYYY-MM-DD
**Reason:** [Why this decision is no longer recommended]
```

## Integration with PRs

### Linking from PR

Pull requests MUST link to decision logs when implementing architectural changes:

```markdown
## Decisions

### Architectural Decisions
- [DECISION: OAuth Provider Selection](../../obsidian/decisions/oauth-provider-selection.md)
  - Context: Multiple SSO providers needed
  - Options: OAuth2, SAML, Hardcoded
  - Chosen: OAuth2 dynamic config
  - Rationale: Best balance of flexibility and implementation time
```

### Creating During PR

If architectural decision emerges during implementation:

1. **Pause implementation**
2. **Create decision document**
3. **Get stakeholder input**
4. **Update PR description** with decision link
5. **Resume implementation**

## Common Decision Types

### Technology Selection

```markdown
# DECISION: Frontend Framework for Dashboard

**Context:** Need interactive, real-time dashboard...

**Options:**
- React
- Vue
- Angular

**Chosen:** React
**Rationale:** Team expertise, ecosystem, TypeScript support
```

### Architecture Pattern

```markdown
# DECISION: Microservices vs Monolith

**Context:** Scaling application to handle 10x traffic...

**Options:**
- Monolith with horizontal scaling
- Microservices architecture
- Serverless functions

**Chosen:** Monolith with horizontal scaling
**Rationale:** Simpler deployment, adequate for current scale
```

### Data Model Design

```markdown
# DECISION: User Session Storage Strategy

**Context:** Need to persist user sessions across server restarts...

**Options:**
- In-memory (Redis)
- Database (PostgreSQL)
- Stateless (JWT tokens)

**Chosen:** Redis with PostgreSQL backup
**Rationale:** Performance + reliability
```

## Anti-Patterns to Avoid

❌ **Vague Context:** "We need to improve the system"
✅ **Specific Context:** "Current authentication has 30% failure rate due to password resets"

❌ **Single Option:** Only documenting chosen approach
✅ **Multiple Options:** Present 2-5 alternatives considered

❌ **No Rationale:** "We chose React"
✅ **Detailed Rationale:** "React chosen because: team expertise, TypeScript support, component ecosystem, hiring availability"

❌ **Ignoring Negatives:** Only listing benefits
✅ **Honest Consequences:** Document both positive and negative outcomes

❌ **No Review Plan:** Decision permanent
✅ **Review Scheduled:** "Review in 6 months or if performance degrades"

## Validation Checklist

Before finalizing decision document:

- [ ] Context clearly explains why decision needed
- [ ] At least 2 options considered (usually 3-5)
- [ ] Each option has pros, cons, trade-offs
- [ ] Decision explicitly states chosen option
- [ ] Rationale explains why chosen over alternatives
- [ ] Consequences cover positive, negative, neutral
- [ ] Implementation section provides timeline and effort
- [ ] Related decisions linked
- [ ] References to research included
- [ ] Review plan specified

## References

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [DECISION Pattern by Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Daily Needs Decision Logging](../../.github/docs/my-daily-needs.md#decision-logging-pattern)

## Related Documentation

- [PR Quality Gates](./pr-quality-gates.instructions.md)
- [Branch & Commit Policy](./branch-commit-policy.instructions.md)
- [Standup Format Standards](./standup-format.instructions.md)
