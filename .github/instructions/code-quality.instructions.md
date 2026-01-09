---
description: 'Maintain standards for readability, performance, security, and maintainability'
applyTo: '**/*'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](./dont-repeat-yourself.md) - Minimize code duplication and maximize reusability
- [Code Quality Goals](./code-quality-goals.md) - Maintain standards for readability, performance, security, and maintainability

When implementing these guidelines, always consider how they reinforce these core principles.

# Code Quality Goals

## Overview

Code Quality Goals are specific, measurable targets for code improvement that reflect your quality standards.

Rather than vague aspirations ("write good code"), quality goals are concrete:
- ✅ Specific (exact metric)
- ✅ Measurable (can track progress)
- ✅ Achievable (realistic targets)
- ✅ Relevant (matters for your system)
- ✅ Time-bound (achieved by when?)

## The 5 Quality Dimensions

### 1. **Correctness** - Code Does What It Should

**Definition**: Code behavior matches requirements. No unexpected bugs or edge cases.

**Measurable Targets**:
- ✅ **Zero critical bugs** in production
- ✅ **Bug resolution time** < 24 hours for critical, < 1 week for minor
- ✅ **Bug escape rate** < 5% (bugs found in testing, not production)
- ✅ **Test coverage** > 80% for critical paths

**How to Achieve**:
- Test-driven development (write tests first)
- Code review before merging
- Automated testing in CI/CD
- Production monitoring and alerting

---

### 2. **Performance** - Code Runs Efficiently

**Definition**: Code executes quickly and uses resources efficiently without unnecessary waste.

**Measurable Targets**:
- ✅ **Response time** < 200ms for user-facing endpoints
- ✅ **Database queries** complete in < 50ms (no N+1 queries)
- ✅ **Memory usage** stable (no leaks)
- ✅ **Bundle size** < 500KB (JavaScript)
- ✅ **Page load time** < 3 seconds

**How to Achieve**:
- Profile code to find bottlenecks
- Cache strategically
- Optimize database queries
- Lazy load resources
- Monitor performance in production

---

### 3. **Clarity** - Code Is Easy to Understand

**Definition**: Code intent is obvious. Someone unfamiliar can understand purpose without excessive comments.

**Measurable Targets**:
- ✅ **Cyclomatic complexity** < 10 per function (simpler logic)
- ✅ **Function length** < 50 lines (focused responsibility)
- ✅ **Variable names** descriptive (no `x`, `temp`, `data`)
- ✅ **Code duplication** < 5% (no repeated patterns)
- ✅ **Time to understand** new code < 5 minutes

**How to Achieve**:
- Use meaningful names
- Keep functions small and focused
- Extract complex logic into well-named functions
- Write comments explaining WHY, not WHAT
- Refactor regularly

---

### 4. **Robustness** - Code Handles Edge Cases

**Definition**: Code gracefully handles unexpected inputs, errors, and edge cases without crashing.

**Measurable Targets**:
- ✅ **Error handling coverage** > 90% (all error paths handled)
- ✅ **No null pointer exceptions** in production
- ✅ **Boundary testing** for all input types
- ✅ **Timeout handling** on all external calls
- ✅ **Graceful degradation** when dependencies fail

**How to Achieve**:
- Test error conditions
- Add assertions and guards
- Use defensive programming
- Add timeouts to external calls
- Implement circuit breakers
- Log errors with context

---

### 5. **Maintainability** - Code Is Easy to Change

**Definition**: Code structure makes changes safe, quick, and low-risk.

**Measurable Targets**:
- ✅ **Coupling** measured (dependencies flow one direction)
- ✅ **Cohesion** high (related things together)
- ✅ **Module independence** high (can test/use separately)
- ✅ **Code review time** < 15 minutes (understandable)
- ✅ **Change impact** localized (changes don't ripple)

**How to Achieve**:
- Follow SOLID principles
- Decouple components (dependency injection)
- Keep modules focused
- Write tests (test-driven design)
- Refactor regularly
- Use architecture review

---

## How to Use Quality Goals

### Setting Goals

```
Step 1: Assess current state
  What are we measuring today?
  Example: Test coverage is 60%, P95 response time is 400ms

Step 2: Identify target
  What do we want to achieve?
  Example: Test coverage 85%, response time 150ms

Step 3: Set timeline
  When should we achieve this?
  Example: Next quarter (3 months)

Step 4: Plan improvements
  What actions improve this metric?
  Example: Add tests, optimize queries, cache results

Step 5: Monitor progress
  Track weekly/monthly progress toward goal
  Example: Coverage up to 70% after 1 month

Step 6: Celebrate success
  Acknowledge when goal is reached
  Example: Shipped version 2.0 at target metrics
```

### Using Goals in Development

**Before implementing feature**:
- Does this feature meet our quality goals?
- Will this improve or degrade quality?
- How will we test this?

**During code review**:
- Does this change move us toward goals?
- Any quality goals at risk?
- Should we refactor related code?

**After deployment**:
- Did we hit quality targets?
- Any metrics degraded?
- What should we improve next?

---

## Quality Goals by Project Phase

### Phase 1: Startup (MVP)
Focus on **correctness** and **robustness**
- No critical bugs
- Core features work
- Basic error handling
- Manual testing sufficient

### Phase 2: Growth (Scaling)
Add **performance** and **clarity**
- Response time matters
- Code becomes complex
- More team members
- Code clarity important

### Phase 3: Maturity (Optimization)
Refine **maintainability**
- Change speed matters
- Technical debt reduction
- Architectural clarity
- Team velocity

---

## Quality Goals Checklist

When setting goals:

- [ ] Is it specific? (not "improve quality")
- [ ] Is it measurable? (can track with a number)
- [ ] Is it achievable? (realistic timeline)
- [ ] Is it relevant? (matters for your system)
- [ ] Is it time-bound? (target date set)
- [ ] Have we communicated it? (team knows)
- [ ] Have we planned how to achieve it? (action items)
- [ ] Do we monitor progress? (weekly check-ins)
- [ ] Do we celebrate success? (acknowledged achievements)

---

## Remember

**Quality goals are:**
- ✅ Specific and measurable
- ✅ Achievable and realistic
- ✅ Relevant to your system
- ✅ Time-bound and tracked
- ✅ Communicated to team
- ✅ Regularly reviewed

**Not:**
- ❌ Vague ("write good code")
- ❌ Unmeasurable
- ❌ Unrealistic (100% uptime)
- ❌ Ignored (set and forgotten)
- ❌ Static (never updated)

**Quality improves through specific, measurable, tracked goals.**
