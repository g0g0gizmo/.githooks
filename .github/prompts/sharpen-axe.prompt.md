---
description: 'Use Sharpen Axe agent methodology aligned with core principles for comprehensive task planning'
mode: 'sharpen-axe'
tools:
- 'edit'
- 'runNotebooks'
- 'search'
- 'new'
- 'runCommands'
- 'runTasks'
- 'GitKraken/*'
- 'betterthantomorrow.joyride/joyride-eval'
- 'betterthantomorrow.joyride/human-intelligence'
- 'usages'
- 'vscodeAPI'
- 'problems'
- 'changes'
- 'testFailure'
- 'openSimpleBrowser'
- 'fetch'
- 'githubRepo'
- 'github.vscode-pull-request-github/copilotCodingAgent'
- 'github.vscode-pull-request-github/issue_fetch'
- 'github.vscode-pull-request-github/suggest-fix'
- 'github.vscode-pull-request-github/searchSyntax'
- 'github.vscode-pull-request-github/doSearch'
- 'github.vscode-pull-request-github/renderIssues'
- 'github.vscode-pull-request-github/activePullRequest'
- 'github.vscode-pull-request-github/openPullRequest'
- 'ms-python.python/getPythonEnvironmentInfo'
- 'ms-python.python/getPythonExecutableCommand'
- 'ms-python.python/installPythonPackage'
- 'ms-python.python/configurePythonEnvironment'
- 'sonarsource.sonarlint-vscode/sonarqube_getPotentialSecurityIssues'
- 'sonarsource.sonarlint-vscode/sonarqube_excludeFiles'
- 'sonarsource.sonarlint-vscode/sonarqube_setUpConnectedMode'
- 'sonarsource.sonarlint-vscode/sonarqube_analyzeFile'
- 'extensions'
- 'todos'
- 'runSubagent'
- 'runTests'
---

# Sharpen Axe Guided Planning - Align Task with Principles

## Purpose

This prompt guides you to use the **Sharpen Axe agent** methodology in conjunction with core engineering principles (SOLID, DRY, KISS, Design by Contract, Testing Standards, Security Standards, Orthogonality, Problem Decomposition) to create exhaustive, principle-aligned tracking for complex tasks.

**The outcome**: A comprehensive planning package with research documentation, detailed tracking, implementation guidance, and change tracking—ready for systematic execution.

**Philosophy**: Go slow to be fast. Thorough preparation beats rushed execution.

---

## Input Template

Replace these placeholders with your specific task:

```
TASK: [Brief title of what needs to be built/changed]
GOAL: [What success looks like in 1-2 sentences]
CONSTRAINTS: [Timeline, team size, budget, scope limits]
CONTEXT: [Why this matters, what problem it solves]
```

**Example Input**:

```
TASK: Implement user authentication for dashboard application
GOAL: Enable secure login/logout with JWT tokens and role-based access control
CONSTRAINTS: 2 weeks, 2 engineers, must integrate with existing API
CONTEXT: Dashboard currently lacks auth; multiple user roles need different permissions
```

---

## Planning Phases with Principle Alignment

### Phase 0: Deep Research (Principles: DRY, Problem Decomposition)

**Goal**: Exhaustively research existing solutions, patterns, and approaches

**Principle Application**:

- **DRY**: Search for existing auth implementations to avoid reinventing
- **Problem Decomposition**: Break authentication into: (1) token generation, (2) validation, (3) storage, (4) role checking

**Research Checklist**:

- [ ] Codebase search: Find existing auth patterns, conventions, libraries already used
- [ ] GitHub search: Find 3-5 similar projects, reference implementations, best practices
- [ ] Internet search: JWT standards, OAuth vs session-based, auth libraries for your stack
- [ ] Document: What exists? What's proven? What does your team know?

**Output File**: `.github/tracking/YYYYMMDDHH-task-description-research.md`

- Document all searches performed (codebase, GitHub, internet)
- List 3-5 approaches evaluated with pros/cons and evidence
- Recommend one approach with clear rationale
- Remove unselected alternatives from final document to avoid redundancy

---

### Phase 1: Base Camp Assessment (Principles: Orthogonality, SOLID)

**Goal**: Map current reality—codebase, team, risks, constraints

**Principle Application**:

- **Orthogonality**: Identify components that must be independent (auth service, database, UI layer)
- **SOLID Single Responsibility**: Auth should be isolated; routing, validation, token management separate

**Assessment Checklist**:

- [ ] Codebase architecture: Where does auth belong? How does it interact with existing components?
- [ ] Dependencies: What libraries/services already available? What would need to be added?
- [ ] Team skills: Does team know the chosen approach? What training needed?
- [ ] Technical debt: Are there design patterns we must respect? Existing patterns to follow?
- [ ] Constraints: Timeline realistic? Resources adequate? External dependencies?

**Questions to Answer**:

- Where will auth logic live (middleware, service, controller)?
- How does it integrate without breaking existing code (Orthogonality)?
- What existing patterns must we respect (DRY principle)?

---

### Phase 2: Route Planning (Principles: KISS, Design by Contract)

**Goal**: Design the solution with clear milestones, steps, and validation criteria

**Principle Application**:

- **KISS**: Simplest viable authentication (don't over-engineer with 2FA, OAuth, etc. unless required)
- **Design by Contract**: Preconditions (valid credentials), postconditions (valid token issued), invariants (no privilege escalation)

**Planning Steps**:

#### Step 1: Define Anchor Points (Major Milestones)

Each anchor = 1-3 days of focused work with clear deliverables

**Example Anchors for Auth Implementation**:

**Anchor 1: Foundation & Design**

- Deliverable: API contract defined, database schema, authentication flow diagram
- Validation: Team agrees on approach, schema reviewed, flow is secure
- Exit Criteria: No ambiguity about what token contains, when validated, how privileges checked

**Anchor 2: Token Generation & Storage**

- Deliverable: Login endpoint created, JWT tokens generated, storage mechanism implemented
- Validation: Token structure matches design, includes user ID and roles, signed securely
- Testing: Unit tests for token generation, edge cases (expired tokens, invalid credentials)

**Anchor 3: Token Validation Middleware**

- Deliverable: Middleware validates tokens on protected routes, extracts user context
- Validation: Invalid tokens rejected, expired tokens refreshed, user context accessible
- Testing: Valid tokens pass, invalid/expired tokens rejected, malformed tokens handled

**Anchor 4: Role-Based Access Control**

- Deliverable: Permission checking integrated, routes protected by role, unauthorized access rejected
- Validation: Users can access routes matching their role, cannot access restricted routes
- Testing: Admin can access admin routes, user cannot; edge cases tested (deleted role, modified token)

**Anchor 5: Integration & Security Review**

- Deliverable: Full integration with dashboard, security review completed, edge cases handled
- Validation: End-to-end flow works, no exposed tokens, no bypass vulnerabilities
- Testing: E2E tests passing, security checklist cleared, load testing completed

#### Step 2: Detail Each Pitch (Specific Steps Within Anchors)

**Example for Anchor 1**:

- [ ] Define token structure: `{ userId, role, expiresAt, issuer }`
- [ ] Design login endpoint: POST /api/auth/login with email/password
- [ ] Design password hashing: bcrypt with salt (Security Standards)
- [ ] Create database schema for users table with role field
- [ ] Design refresh token strategy (if needed)
- Verify: Design reviewed, no security gaps identified, team understands approach

#### Step 3: Identify Testing Strategy (Principle: Testing Standards)

- **Unit Tests**: Token generation, password hashing, role validation (60% of tests)
- **Integration Tests**: Login flow, database writes, middleware integration (30% of tests)
- **E2E Tests**: Full user journey: login → access protected resource → logout (10% of tests)

**Validation Checklist**:

- [ ] Unit test coverage > 80%
- [ ] All edge cases tested (expired tokens, invalid credentials, role changes)
- [ ] Security cases tested (token tampering, privilege escalation attempts)

---

### Phase 3: Reality Check (Principles: Orthogonality, Design by Contract)

**Goal**: Verify plan is feasible, identify remaining risks

**Checklist**:

- [ ] Are 5 anchors realistic given timeline? (2 weeks, 2 engineers)
- [ ] Does team have required skills (JWT, middleware, role-based auth)?
- [ ] External dependencies blocked? (Database available, libraries compatible?)
- [ ] Security requirements met? (Password hashing, token signing, HTTPS, no token in logs)
- [ ] Edge cases covered? (Token expiry, concurrent requests, role changes during session)

**Top 3 Risks**:

1. **Token expiry during long operations** → Mitigation: Implement refresh tokens
2. **Team unfamiliar with JWT** → Mitigation: Pair programming, documentation
3. **Performance impact of role checking on every request** → Mitigation: Cache roles, benchmark early

**Confidence Check**: ≥90% confident? If not, research more or adjust scope.

---

### Phase 4: Commit (Output Files)

**Create 5 Files** for complete planning package:

#### Core Planning Files (4 Required)

1. **Research Document** (`.github/tracking/YYYYMMDDHH-task-description-research.md`)
   - Document all searches performed (codebase, GitHub, internet) with specific queries
   - List 3-5 approaches evaluated with pros/cons and evidence
   - Recommend one approach with clear rationale
   - Remove unselected alternatives from final version

2. **Plan Instructions** (`.github/tracking/YYYYMMDDHH-task-description-plan.instructions.md`) - **The Mountain Map**
   - Executive summary with goal, success criteria, and constraints
   - Research foundation with selected approach and key learnings
   - Base camp assessment (codebase, team, timeline, constraints)
   - All anchors with deliverables, validation criteria, and exit conditions
   - Pitch-level steps with testing requirements
   - Risk register with top 3-5 risks and mitigations
   - **Primary source of truth - copied to tracking/ for active work**

3. **Details Document** (`.github/tracking/YYYYMMDDHH-task-description-details.md`)
   - API specifications with endpoint paths, request/response formats
   - Database schemas and data models
   - Architecture diagrams and component interactions
   - Line-level implementation guidance with code examples

4. **Implementation Prompt** (`.github/prompts/implement-task-description.prompt.md`)
   - Ready-to-execute guide for implementation team
   - Step-by-step execution instructions
   - Success criteria and validation checkpoints

#### Tracking File (1 Required)

5. **Changes Tracking** (`.github/copilot/tracking/changes/YYYYMMDDHH-task-description-changes.md`) - **The Climb Journal**
   - Progress tracking as implementation proceeds
   - Timestamped entries showing execution timeline
   - Added/Modified/Removed sections for all file changes
   - Completed steps with dates: `[x] Step - Completed YYYY-MM-DD HH:MM`
   - Milestone completions: `## ✅ Anchor N: Name - COMPLETED`
   - Key decisions made with rationale and timestamps
   - Blockers encountered, resolutions, and timeline impact
   - Scope updates with justifications
   - Testing and validation evidence
   - Confidence level updates
   - **Matches timestamp in filename for clear correlation**

---

## Principle-to-Phase Mapping Guide

Use this to ensure your plan aligns with core principles:

### Principle: DRY (Don't Repeat Yourself)

**Apply during Phase 0 (Research)**:

- Search for existing auth libraries/patterns
- Identify code that would duplicate across endpoints
- Document where a shared service/utility would prevent duplication

**Apply during Phase 2 (Planning)**:

- Centralize token generation logic (single function, used everywhere)
- Create shared middleware for validation
- Define role-checking utility once, reuse on all protected routes

**Validation**: Can you point to 2-3 places where code/logic would be unified?

### Principle: KISS (Keep It Simple, Stupid)

**Apply during Phase 0 (Research)**:

- Evaluate simplicity of each approach (JWT > OAuth for MVP)
- Identify unnecessary features (skip 2FA unless critical)

**Apply during Phase 2 (Planning)**:

- Make each anchor focused, not trying to solve everything at once
- Define simplest viable implementation at each step

**Validation**: Can you explain the approach in 1 minute without jargon?

### Principle: SOLID (Single Responsibility)

**Apply during Phase 1 (Base Camp)**:

- Identify components: TokenService, PasswordService, PermissionChecker, UserRepository
- Each has one reason to change

**Apply during Phase 2 (Planning)**:

- Design services with clear boundaries
- Specify which service handles what

**Validation**: Can each component be tested independently?

### Principle: Design by Contract

**Apply during Phase 1 (Base Camp)**:

- Define what auth guarantees: "Valid token always contains userId and role"
- Define what callers must provide: "Email and password must be provided"

**Apply during Phase 2 (Planning)**:

- Specify preconditions (login endpoint requires valid email/password)
- Specify postconditions (valid token returned with user context)
- Specify invariants (user privilege never escalates without explicit grant)

**Validation**: Can you list 3 preconditions and 3 postconditions for the auth system?

### Principle: Orthogonality (Independence)

**Apply during Phase 1 (Base Camp)**:

- Auth service must not depend on UI layer
- Permission checking must work independently of token generation

**Apply during Phase 2 (Planning)**:

- Design auth as independent service (can be replaced)
- Middleware should be agnostic to business logic
- Changes to role logic shouldn't affect token generation

**Validation**: Can you swap the auth service without changing other code?

### Principle: Problem Decomposition

**Apply during Phase 2 (Planning)**:

- Break auth into: token generation, validation, role checking (case analysis)
- Break login flow into: credential validation, hash comparison, token creation (sequential)
- Break testing into: unit/integration/E2E (layers)

**Validation**: Are your 5 anchors clear subproblems that combine into the whole?

### Principle: Testing Standards

**Apply during Phase 2 (Planning)**:

- Unit tests (60%): Token generation, password hashing, role logic
- Integration tests (30%): Database writes, middleware chains
- E2E tests (10%): Full login flow

**Apply during Phase 3 (Reality Check)**:

- Is test coverage > 80%?
- Are security cases tested?

**Validation**: Can you write test cases for each anchor before implementation?

### Principle: Security Standards

**Apply during Phase 1 (Base Camp)**:

- Identify security requirements: password hashing, token signing, HTTPS
- Research threats: token tampering, privilege escalation, credential stuffing

**Apply during Phase 2 (Planning)**:

- Specify hashing algorithm (bcrypt, not MD5)
- Specify token signing method (RSA, HS256)
- Specify where tokens stored (HttpOnly cookies, not localStorage)
- Specify what NOT to log (never log passwords or tokens)

**Validation**: Have you addressed OWASP Top 10 Auth vulnerabilities?

---

## Output File Templates

### Template 1: Research Document

```markdown
# Research: [Task Name]

## Searches Performed

### Codebase Search
- Keywords: "authentication", "auth", "token", "login"
- Found: [List existing patterns, files, libraries]

### GitHub Search
- Query 1: "jwt authentication nodejs"
- Found 5 projects: [List with pros/cons]
- Query 2: "role based access control"
- Found 3 projects: [List with pros/cons]

### Internet Search
- JWT standards: [Reference RFC 7519]
- Best practices: [Blog posts, official docs]
- Security considerations: [OWASP, Auth0 guides]

## Approaches Evaluated

### Approach 1: Session-Based Auth (Traditional)
**How**: Server stores session in database, returns session ID in cookie
**Pros**: Simple, server controls revocation
**Cons**: Doesn't scale across multiple servers, requires session database

### Approach 2: JWT (Recommended)
**How**: Server signs token with secret, client stores in cookie/header
**Pros**: Stateless, scales horizontally, industry standard
**Cons**: Token revocation harder, needs refresh token strategy

## Recommendation

**JWT** - Aligns with team's node.js experience, scales better than sessions, stateless design follows Orthogonality principle (auth independent of server state)

```

### Template 2: Plan Instructions

```markdown
# Plan Instructions: [Task Name]

## Anchors & Milestones

### Anchor 1: Foundation & Design
**Duration**: Day 1
**Deliverables**:
- [ ] API contract documented
- [ ] Database schema designed
- [ ] Auth flow diagram created
**Validation**: Design review completed, team alignment
**Exit Criteria**: Ready to code with no ambiguity

### Anchor 2: [Name]
**Duration**: Day 2
**Deliverables**:
- [ ] [Specific deliverable]
- [ ] [Specific deliverable]
**Validation**: [How to verify correctness]
**Exit Criteria**: [What must be true before moving on]

...

## Testing Strategy (Anchor N)
- Unit: [What to test in isolation]
- Integration: [How components work together]
- E2E: [Full user flow]

## Principle Alignment

**KISS**: Starting with simple JWT, no OAuth complexity
**SOLID**: Token service isolated from database service
**DRY**: Validation logic in one middleware, reused everywhere
**Design by Contract**: Precondition: valid credentials; Postcondition: valid token
**Orthogonality**: Auth service independent of business logic

```

---

## Operational Discipline - Do NOT End Your Turn Until

**CRITICAL**: Follow the agent's sacred oath—do not consider planning complete until ALL criteria are met:

### Research Completion Checklist

- [ ] Exhaustive codebase search performed (patterns, implementations, conventions documented)
- [ ] GitHub search completed (3-5 projects/libraries found and analyzed)
- [ ] Internet research done (Stack Overflow, docs, blogs, best practices verified)
- [ ] Multiple authoritative sources cross-referenced
- [ ] 3-5 alternative approaches evaluated with evidence
- [ ] Recommended approach selected with clear rationale
- [ ] Research file created: `.github/tracking/YYYYMMDDHH-task-description-research.md`

### Context Mapping Checklist

- [ ] Summit clarified (goal, success criteria, stakeholders, constraints)
- [ ] Terrain mapped (codebase state, technical debt, team capabilities)
- [ ] Research insights integrated into context
- [ ] Hazards identified (technical risks, dependencies, organizational risks)
- [ ] Team assessment complete (skills, time, tools, budget)

### Planning Completion Checklist

- [ ] Multiple routes proposed with evidence-based tradeoffs
- [ ] Anchors defined with clear deliverables and exit criteria
- [ ] Pitch-level steps detailed for each anchor
- [ ] Testing strategy comprehensive (unit/integration/E2E)
- [ ] Rollout and deployment plan created
- [ ] All 3 planning files created (plan.instructions.md, details.md, implement-*.prompt.md)

### Validation & Commitment Checklist

- [ ] Assumptions stress-tested against research findings
- [ ] Feasibility validated (timeline, skills, dependencies)
- [ ] Top 3-5 risks identified with mitigations
- [ ] Confidence level ≥90% for implementation
- [ ] Plan.instructions.md includes executive summary with goal and success criteria
- [ ] Tracking directory structure created: `.github/copilot/tracking/`
- [ ] Changes file initialized: `tracking/changes/YYYYMMDDHH-*-changes.md`
- [ ] Plan specific enough to hand directly to developer

### Quality Gates

- [ ] Each anchor has measurable exit criteria
- [ ] No vague milestones ("implementation phase" → specific deliverables)
- [ ] Edge cases and error scenarios addressed
- [ ] Team constraints considered in timeline
- [ ] Tradeoffs explicitly documented
- [ ] Todo lists use checkboxes and are sequential
- [ ] All 6 output files created and cross-referenced

**Only proceed when ALL checkboxes are complete. Go slow to be fast.**

---

## From Planning to Implementation

Once planning is complete, the outputs enable systematic implementation:

### Implementation Flow

1. **Handoff Package**: Developer receives 5 files
   - Research.md for context and approach understanding
   - Plan.instructions.md as the primary checklist and executive summary
   - Details.md for line-level implementation guidance
   - Implement-*.prompt.md for step-by-step execution
   - Changes.md (in tracking/) for progress documentation

2. **Systematic Execution** (follows `sharpen-axe.instructions.md`):
   - Copy plan files to `.github/copilot/tracking/` for active work
   - Read complete plan and understand all anchors
   - Process tasks sequentially, one at a time
   - Mark tasks complete `[x]` in tracking/tracking/YYYYMMDDHH-*-plan.instructions.md
   - Update tracking/changes/YYYYMMDDHH-*-changes.md after each task
   - Document in Added/Modified/Removed sections with timestamps
   - Validate implementation against details.md requirements
   - Continue until all phases marked complete

3. **Progress Tracking**:
   - Changes file documents every step with precise timestamps
   - Each entry shows: `YYYY-MM-DD HH:MM - [Action] - [File] - [Result]`
   - Divergences from plan noted with reasoning
   - Blockers and resolutions captured with timeline impact
   - Phase completions marked: `## ✅ Anchor N: Name - COMPLETED YYYY-MM-DD`

4. **Completion Criteria**:
   - All plan tasks marked `[x]` in tracking copy
   - All specified files exist with working code
   - All success criteria verified
   - No implementation errors remain
   - Release summary added to changes file with total timeline

### Tracking Directory Structure

Organize planning and implementation tracking with timestamped correlation:

```text
.github/
├── YYYYMMDDHH-PLAN.md              # Master plan (executive summary)
├── tracking/
│   ├── YYYYMMDDHH-task-description-research.md
│   ├── YYYYMMDDHH-task-description-plan.instructions.md
│   └── YYYYMMDDHH-task-description-details.md
├── prompts/
│   └── implement-task-description.prompt.md  # NO timestamp (reusable)
└── copilot/
    └── tracking/
        ├── tracking/
        │   └── YYYYMMDDHH-task-description-plan.instructions.md  # Working copy
        ├── changes/
        │   └── YYYYMMDDHH-task-description-changes.md  # Progress log
        └── details/
            └── YYYYMMDDHH-task-description-details.md  # Implementation specs
```

**Timestamp Format**: `YYYYMMDDHH` = Year Month Day Hour (e.g., `2025113014` = Nov 30, 2025 at 2 PM)

**Why This Structure**:

- `.github/tracking/` = Original planning artifacts (read-only after creation)
- `.github/copilot/tracking/` = Active implementation workspace
- Matching timestamps enable clear correlation between plan and execution
- Changes file provides detailed timeline of all implementation activity

## Success Criteria

A strong plan demonstrates:

✓ Comprehensive Phase 0 research documented with date-prefixed file
✓ Exhaustive GitHub & internet searching (3-5 main approaches found)
✓ Research showing what was searched, found, and why approach selected
✓ Thorough codebase exploration (patterns, conventions, related code)
✓ Complete context mapping (goals, constraints, team, risks, timeline)
✓ Multiple approaches considered with clear tradeoffs
✓ Evidence-based recommendations grounded in research findings
✓ Realistic anchors with measurable exit criteria
✓ Detailed pitch-level steps ready for implementation
✓ Comprehensive testing strategy (unit/integration/E2E)
✓ Risk register with mitigations
✓ Deployment and rollback planning
✓ Principle alignment documented throughout
✓ Security considerations addressed (OWASP compliance)
✓ All 5 output files created (4 planning + tracking changes file)
✓ Plan.instructions.md contains executive summary and all planning details
✓ Tracking structure initialized in `.github/copilot/tracking/`
✓ Timestamped changes file ready for implementation progress
✓ Plan specific enough to hand to developer
✓ Confidence ≥90% for implementation to begin

---

## Remember: Go Slow to Be Fast

> "Every hour spent in planning saves ten in execution. Every contingency planned prevents a disaster. Every principle honored prevents a misstep."

The time you invest now in thorough, principle-aligned planning directly determines implementation speed and quality later.

**Sharpen your axe. Plan comprehensively. Execute with confidence.**
