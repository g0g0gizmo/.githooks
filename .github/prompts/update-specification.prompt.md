---
description: 'Update, review, and refine existing specifications, plans, or designs'
---

# Update Specification

Modify, improve, and refine existing specifications, implementation plans, designs, or project documentation. Handles updates based on feedback, changing requirements, or new insights.

## Core Principles

This content applies the following foundational principles:

- [Design by Contract](../core/principles/design-by-contract.md) - Maintain contract integrity while updating
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Keep specifications clear and maintainable
- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Avoid duplication across versions

---

## Interactive Setup

**Ask the user:**

1. **What type of specification are you updating?**
   - Feature Specification
   - Requirement Specification
   - Implementation Plan
   - Project Plan
   - Technical Design
   - API Contract
   - Other

2. **What's changing?**
   - Scope change (requirements added/removed)
   - Feedback incorporation (from review or stakeholders)
   - Clarification (make unclear parts explicit)
   - Error correction (fix mistakes/inaccuracies)
   - New insights (discovered information that affects spec)
   - Migration to new format (restructure existing spec)

3. **Update depth?**
   - Minor (section updates, quick fixes)
   - Moderate (restructure some sections, add clarity)
   - Comprehensive (major revision, significant changes)

---

## Update Strategy by Type

### Updating Feature Specifications

**What typically changes**:
- User benefits clarification
- New use cases discovered
- Edge cases identified
- Acceptance criteria refined
- Constraints or dependencies updated

**Review Checklist**:
- [ ] User benefits still accurate
- [ ] Acceptance criteria measurable and testable
- [ ] Edge cases identified and documented
- [ ] Dependencies listed and current
- [ ] Performance requirements still realistic
- [ ] Related features documented

**Example Update**:
```markdown
# Feature: User Authentication

## Updated User Benefits
- Clear (was: "Users can log in")
- Users can securely authenticate with email/password or OAuth
- Users' sessions persist across browser sessions
- Users can reset forgotten passwords
- Users can enable 2FA for additional security

## Refined Acceptance Criteria
- Users can create account with valid email and password
  UPDATED: Password must meet security requirements (12+ chars, mixed case, numbers, symbols)
  UPDATED: Email must be verified before account activation
- Users can log in with correct credentials
  UPDATED: Failed login attempts locked after 5 tries for 15 minutes
  UPDATED: Session timeout after 1 hour of inactivity
- Users can reset password
  NEW: Reset token expires after 24 hours
  NEW: Resetting password invalidates all existing sessions
```

### Updating Requirement Specifications

**What typically changes**:
- Functional requirements clarified or added
- Non-functional requirements (performance, security) updated
- Constraints discovered or changed
- Success metrics refined
- Acceptance criteria adjusted

**Review Checklist**:
- [ ] All functional requirements still valid
- [ ] Non-functional requirements realistic
- [ ] Constraints properly documented
- [ ] Success metrics measurable
- [ ] Dependencies accurate
- [ ] Feasibility confirmed

**Example Update**:
```markdown
# Requirement: Payment Processing

## Functional Requirements (Updated)

### NEW: Multi-Currency Support
- System must support USD, EUR, GBP, JPY, CAD, AUD
- Currency conversion using live exchange rates (updated hourly)
- User can select currency in checkout

### UPDATED: Payment Methods
- REMOVED: PayPal (cost analysis showed Stripe better)
- ADD: Google Pay and Apple Pay (mobile support)
- Keep: Credit/debit cards via Stripe

## Non-Functional Requirements (Updated)

### Performance
- UPDATED: Payment processing latency < 500ms (was 1000ms)
- Reason: Mobile users need faster response

### Security
- NEW: PCI-DSS Level 1 compliance required
- NEW: Tokenization for all card data (no direct storage)
- UPDATED: TLS 1.3 minimum (was 1.2)
```

### Updating Implementation Plans

**What typically changes**:
- Task breakdown refined after starting work
- Timeline estimates adjusted based on progress
- Resource allocation changed
- Risk assessments updated
- Testing strategy refined

**Review Checklist**:
- [ ] Task breakdown reflects actual work
- [ ] Timeline updated with actual progress
- [ ] Blockers identified and communicated
- [ ] Risk assessments current
- [ ] Resource allocation realistic
- [ ] Dependencies still accurate
- [ ] Completion criteria clear

**Example Update**:
```markdown
# Implementation Plan - Authentication Module

## Timeline Updates

### Phase 1: Database & Models (Week 1)
- UPDATED: Database schema finalized (was pending)
- UPDATED: Review completed, 2 minor changes needed
- NEW: Migration script created and tested
- STATUS: 90% complete (was 50%)

### Phase 2: API Endpoints (Weeks 2-3)
- UPDATED: Estimated 3 days for endpoint testing (was 1 day)
- Reason: OAuth integration more complex than expected
- NEW: Need external OAuth provider testing
- REMAINING: Login, logout, refresh endpoints

## Risk Updates

### NEW RISK: OAuth Provider Downtime
- Impact: Users unable to authenticate with OAuth
- Mitigation: Fallback to email/password auth
- Probability: Medium | Impact: High

### MITIGATED RISK: Complex token management
- Original concern: JWT refresh token rotation
- Solution: Using provider's token management
- Status: RESOLVED
```

### Updating Project Plans

**What typically changes**:
- Project scope refined or expanded
- Milestones adjusted
- Team composition changed
- Success criteria clarified
- Delivery timeline updated

**Review Checklist**:
- [ ] Project goals still aligned with business
- [ ] Scope clearly defined (in/out)
- [ ] Milestones achievable with resources
- [ ] Team roles and responsibilities clear
- [ ] Dependencies identified
- [ ] Success criteria measurable
- [ ] Risk mitigation plans in place

**Example Update**:
```markdown
# Project Plan - Mobile App Redesign

## Scope Updates

### NEW IN SCOPE
- Redesign of user dashboard (discovered UX issue)
- Dark mode support (customer request)

### REMOVED FROM SCOPE
- Offline sync (moved to Phase 2)
- Advanced analytics (moved to Phase 2)
- REASON: Timeline constraint - ship Phase 1 by Q1

## Milestone Updates

### Milestone 1: Design & Planning (4 weeks)
- UPDATED: +1 week for stakeholder feedback cycle
- NEW: User testing with 20 beta users
- CHANGED DATES: Feb 1 - Mar 10

### Milestone 2: Development (8 weeks)
- UPDATED: -1 week (better estimation after Phase 1)
- KEEPS: Mar 11 - May 5 (end date maintained)
```

### Updating Technical Designs

**What typically changes**:
- Architecture refined after deeper analysis
- Component design updated based on constraints
- Technology choices changed
- Data structures modified
- Performance considerations updated

**Review Checklist**:
- [ ] Architecture diagram updated
- [ ] Component responsibilities clear
- [ ] Data flow accurate
- [ ] Technology choices documented
- [ ] Performance assumptions validated
- [ ] Scaling strategy addressed
- [ ] Error handling strategy complete
- [ ] Security measures documented

**Example Update**:
```markdown
# Technical Design - User Service

## Architecture Changes

### Database Layer Update
- CHANGED: From single PostgreSQL to read replicas
- REASON: Read-heavy workload (10:1 read/write ratio)
- CONFIG: 1 primary + 2 read replicas in different regions
- IMPACT: Connection pooling required

### Caching Layer Addition
- NEW: Redis cache for frequently accessed user data
- TTL: 5 minutes for user profile, 1 minute for preferences
- FALLBACK: Direct DB query if cache miss
- MONITORING: Cache hit rate target > 85%

## Component Design Updates

### Authentication Service
- UPDATED: JWT expiration from 1 hour to 15 minutes
- REASON: Better security posture for mobile apps
- MITIGATED: Refresh token enables long-lived sessions
- TESTED: Token rotation stress tested at 1000 req/s
```

### Updating API Contracts

**What typically changes**:
- Endpoint behavior clarified
- Request/response formats adjusted
- Error handling improved
- Versioning strategy applied
- Rate limiting updated

**Review Checklist**:
- [ ] Endpoint paths and methods current
- [ ] Request schemas complete
- [ ] Response schemas accurate
- [ ] Error codes comprehensive
- [ ] Examples match actual behavior
- [ ] Rate limits documented
- [ ] Pagination/filtering complete
- [ ] Authentication requirements clear

**Example Update**:
```markdown
# API Contract - User Management

## Endpoint Updates

### GET /users/{id}
- UPDATED: Add `include_preferences` query param
  - Default: false (faster response)
  - true: includes user preferences object
- NEW: Add `Cache-Control` header (max-age=300)
- UPDATED: Response includes `updated_at` timestamp

## Error Code Updates

### NEW Error: 429 Too Many Requests
- Rate limit: 100 requests per minute per user
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Retry-After: Included in response

### UPDATED Error: 401 Unauthorized
- ADDED: `error_code` field
- ADDED: `message` field with specific reason
- Example: `{"error_code": "TOKEN_EXPIRED", "message": "Token expired. Please refresh."}`

## Response Format Updates

### User Object
```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "created_at": "ISO8601 timestamp",
  "updated_at": "ISO8601 timestamp (NEW)",
  "is_verified": "boolean (NEW)",
  "preferences": {
    "theme": "light|dark (NEW)",
    "notifications_enabled": "boolean (NEW)"
  }
}
```
```

---

## Update Process

### Step 1: Gather Context
- [ ] Read current specification thoroughly
- [ ] Collect feedback or change requests
- [ ] Identify what needs to change
- [ ] Understand why changes are needed
- [ ] Assess impact of changes

### Step 2: Plan Updates
- [ ] Categorize changes (scope, clarification, correction, etc.)
- [ ] Prioritize changes
- [ ] Identify sections affected
- [ ] Plan review/approval process
- [ ] Determine impact on implementation

### Step 3: Document Changes
- [ ] Mark what's UPDATED (with old value shown)
- [ ] Mark what's NEW (completely added)
- [ ] Mark what's REMOVED (if significant)
- [ ] Explain why changes were made
- [ ] Reference feedback/requirements
- [ ] Show before/after where helpful

### Step 4: Review & Approval
- [ ] Share with stakeholders
- [ ] Gather feedback on updates
- [ ] Iterate if needed
- [ ] Get sign-off from decision makers
- [ ] Document approvals

### Step 5: Communicate
- [ ] Notify affected teams (dev, design, QA)
- [ ] Explain impact of changes
- [ ] Share updated version
- [ ] Answer questions
- [ ] Update related documentation

---

## Change Notation Best Practices

### Clear Notation
```markdown
# Feature: User Authentication

- UPDATED: Login timeout from 1 hour to 30 minutes
  Reason: Security review feedback

- NEW: Two-factor authentication support
  Impact: Requires SMS gateway integration

- REMOVED: Social login via Twitter
  Reason: Low usage, maintenance burden

- CLARIFIED: Password reset flow
  See: Section 3.2 (revised flowchart)

- FIXED: Email validation regex was too restrictive
```

### Justification
Always explain **why** changes were made:
- Customer feedback
- Security review findings
- Performance analysis
- Technical constraints
- Budget/timeline constraints
- Risk mitigation
- Bug discovery

### Impact Assessment
Explain impact of changes:
- Implementation effort
- Timeline implications
- Resource requirements
- Breaking changes
- Testing requirements

---

## Update Scope Guidelines

### Minor Updates (Quick)
**Use when**: Small clarifications, typo fixes, minor additions
**Examples**: Fix wording, add example, clarify edge case
**Review**: Self-review sufficient
**Approval**: Usually doesn't need approval
**Time**: 15-30 minutes

### Moderate Updates (Standard)
**Use when**: Section revisions, requirement adjustments, new components
**Examples**: Update requirements, refine design, add new section
**Review**: Peer review recommended
**Approval**: May need stakeholder review
**Time**: 1-2 hours

### Comprehensive Updates (Major)
**Use when**: Significant scope changes, major refinements, new direction
**Examples**: Complete redesign, major scope change, new technology choice
**Review**: Formal review with multiple stakeholders
**Approval**: Requires stakeholder/decision maker approval
**Time**: 4+ hours (including feedback cycles)

---

## Updating for Different Audiences

### For Developers
- Add implementation details
- Update technical constraints
- Clarify edge cases
- Provide code examples if relevant
- Explain dependency changes

### For Product/Business
- Update business value
- Clarify customer benefits
- Explain timeline impact
- Show ROI implications
- Address competitive positioning

### For Design/UX
- Update user flows
- Clarify interaction patterns
- Update visual requirements
- Address accessibility changes
- Explain usability implications

### For QA/Testing
- Update test scenarios
- Clarify edge cases
- Explain new error conditions
- Describe testing approach
- List assumptions and constraints

---

## Common Update Patterns

### Pattern 1: Feedback-Driven Updates
1. Receive feedback from review/stakeholders
2. Categorize feedback
3. Incorporate relevant feedback
4. Mark changes clearly
5. Share revised version
6. Get approval

### Pattern 2: Discovery-Driven Updates
1. Discover new information during work
2. Assess impact on specification
3. Update relevant sections
4. Communicate changes early
5. Adjust timeline/resources as needed

### Pattern 3: Iterative Refinement
1. Create initial specification
2. Gather feedback in phases
3. Make incremental updates
4. Validate with stakeholders
5. Finalize when stable

### Pattern 4: Error Correction
1. Identify error in specification
2. Fix immediately
3. Assess impact of error
4. Notify affected teams
5. Update related documentation

---

## Update Checklist

- [ ] Current specification read thoroughly
- [ ] All changes identified and categorized
- [ ] Reason for each change documented
- [ ] Impact assessed
- [ ] Audience-appropriate updates made
- [ ] Changes clearly marked (UPDATED, NEW, REMOVED)
- [ ] Before/after shown where helpful
- [ ] Related documentation identified
- [ ] Stakeholders/approvers identified
- [ ] Timeline impact communicated
- [ ] Review scheduled
- [ ] Approval obtained
- [ ] Teams notified
- [ ] New version distributed

---

## Related Content

- For creating specifications: `create-specification.prompt.md`
- For analyzing impact: `arch-gen-blueprint.prompt.md`
- For implementation planning: Break tasks down with `test-breakdown.prompt.md`
- For feedback gathering: Use review/discussion modes
- For communication: `comment-generate-tutorial.prompt.md` for documentation

---

## Questions to Ask Before Updating

1. **What triggered this update?** (feedback, discovery, change, error?)
2. **What impact will changes have?** (scope, timeline, resources, implementation?)
3. **Who needs to approve this?** (stakeholders, decision makers?)
4. **How will this be communicated?** (to dev, design, QA teams?)
5. **What documentation needs updating?** (related specs, plans, implementation?)
6. **How will this be tested/verified?** (if implementation impact?)

---

## Next Steps

After updating specification:
1. [ ] Share updated version with stakeholders
2. [ ] Collect feedback on changes
3. [ ] Iterate if needed
4. [ ] Get approval/sign-off
5. [ ] Communicate to affected teams
6. [ ] Update related documentation
7. [ ] Archive previous version
8. [ ] Begin/resume implementation with updated spec
