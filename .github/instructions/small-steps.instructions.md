---
description: 'Make consistent progress through incremental, feedback-driven changes'
applyTo: '**/*'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../../.github/copilot/copilot/guidelines/dont-repeat-yourself.md) - Minimize code duplication and maximize reusability
- [Problem Decomposition](problem-decomposition.instructions.md) - Break complex problems into smaller, manageable subproblems

When implementing these guidelines, always consider how they reinforce these core principles.

# Small Steps

## Overview

**Take Small Steps** = Make small, focused changes. Get feedback. Course-correct.

Rather than big, risky changes that might break everything, take tiny, validated steps:

- ✅ Change is small (low risk)
- ✅ Feedback is immediate (fast validation)
- ✅ Course correction is cheap (easy to adjust)
- ✅ Progress is visible (momentum)

Large changes are risky. Small steps are safe.

With small steps:

- You catch errors early (feedback loops)
- You adjust quickly (can change direction)
- You keep moving (momentum)
- You build confidence (tests pass)

## Why Small Steps Matter

### Feedback Loops

Large changes have long feedback loops. Small changes have short ones.

```
Large Change (Long Feedback):
1. Design feature (days)
2. Implement feature (weeks)
3. Test feature (days)
4. Discover problem (weeks too late!)
5. Redesign from scratch

Small Steps (Short Feedback):
1. Implement one function (hours)
2. Test (minutes - feedback!)
3. Adjust (based on feedback)
4. Next function (hours)
5. Problem caught immediately
```

### Risk Mitigation

Small changes have low risk. Large changes have high risk.

```
Large Change Risk:
- Feature takes 3 months
- 1000 lines of code added
- 50 things could break
- Rollback is expensive

Small Step Risk:
- Feature takes 3 months (same time!)
- But 20 lines of code per step
- Only 1 thing could break per step
- Rollback is cheap (revert one commit)
```

### Course Correction

With small steps, you can pivot easily based on feedback.

```
Without Small Steps:
Weeks into development → "Wait, requirement changed"
→ Entire rewrite needed
→ Wasted weeks

With Small Steps:
After 2 days → "Wait, requirement changed"
→ Adjust next step
→ Continue forward
```

## How to Take Small Steps

### The Small Step Workflow

```
1. Identify next smallest valuable step
   What's the tiniest thing I can implement that moves forward?

2. Implement that step
   Write code for just that one thing

3. Test the step
   Does it work? Get feedback immediately

4. Commit the step
   Lock in progress (version control)

5. Reflect
   Did it work? Adjust approach if needed

6. Repeat
   Go to step 1
```

### Guidelines for Sized Steps

```
✅ Good Step Size:
- Takes 15 minutes to 2 hours
- Adds 1 small function
- Tests pass immediately
- Can be reverted easily
- Moves toward goal

❌ Too Big:
- Takes days
- Adds entire feature
- Tests fail for unknown reasons
- Hard to debug
- Risky to revert

❌ Too Small:
- Takes 30 seconds
- Changes one character
- No meaningful progress
- Wastes time
```

## Small Steps in Practice

### Example: Refactoring

```typescript
// ❌ Big step: Refactor entire class at once
class UserService {
  // 500 lines of code
  // Refactor everything → risky, hard to test
}

// ✅ Small steps: Refactor method by method

// Step 1: Extract one method
createUser() { /* ... */ }
// Test: Does createUser still work? ✓

// Step 2: Extract another method
updateUser() { /* ... */ }
// Test: Does updateUser still work? ✓

// Step 3: Repeat for all methods
// Each step is tested and validated
```

### Example: New Feature

```typescript
// ❌ Big step: Build entire payment system
class PaymentSystem {
  // Implement payments, refunds, subscriptions,
  // invoices, receipts all at once
  // Weeks of work, no feedback until done
}

// ✅ Small steps: Build one capability at a time

// Step 1: Process simple payment
processPayment(amount) { /* ... */ }
// Test: Can I charge $10? ✓

// Step 2: Add validation
validateAmount(amount) { /* ... */ }
// Test: Does it reject invalid amounts? ✓

// Step 3: Add error handling
handlePaymentError(error) { /* ... */ }
// Test: Does it handle errors gracefully? ✓

// Step 4: Continue building...
```

## Small Steps Checklist

Before making a change:

- [ ] Can I break this into smaller steps?
- [ ] What's the smallest meaningful change?
- [ ] Can I test this change in isolation?
- [ ] Will this change take less than 2 hours?
- [ ] Can I commit this change independently?
- [ ] Is this change focused on one thing?
- [ ] Will I get immediate feedback after this change?
- [ ] Can I easily revert this change if needed?

## Remember

**Take small, focused steps. Get feedback. Course-correct.**

- 🎯 Make tiny, focused changes
- 📝 Test immediately
- 🔄 Commit frequently
- 🧠 Reflect and adjust
- ⏰ Keep momentum

**Small steps compound into big progress.**
