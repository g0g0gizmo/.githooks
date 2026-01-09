---
description: 'Build for what you know, not for uncertain futures - YAGNI principle'
applyTo: '**/*'
---


## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](dry-principle.instructions.md) - Minimize code duplication and maximize reusability
- [Design by Contract](design-by-contract.instructions.md) - Establish explicit pre-conditions, post-conditions, and invariants

When implementing these guidelines, always consider how they reinforce these core principles.

# No Fortune Telling (YAGNI)

## Overview

**No Fortune Telling** = Don't design for speculative future needs

> "Don't try to predict uncertain future needs. Design for replaceability instead."

When you try to anticipate future requirements, you:
- ❌ Add complexity you don't need
- ❌ Create code that's hard to understand
- ❌ Spend time on features nobody asked for
- ❌ Make wrong predictions 80% of the time
- ❌ Build for a future that never comes

Instead:
- ✅ Build for what you know (current requirements)
- ✅ Make code easy to change
- ✅ Design for replaceability (not extensibility)
- ✅ Solve problems when they arrive
- ✅ Keep code simple

## Red Flags (Fortune Telling)

### Anti-Pattern 1: Speculative Extensibility

```typescript
// ❌ Fortune telling: "What if we need to support multiple types?"
interface PaymentProcessor {
  process(amount: number, method: PaymentMethod): PaymentResult;
  refund(amount: number, method: PaymentMethod): RefundResult;
  verify(method: PaymentMethod): VerificationResult;
  tokenize(method: PaymentMethod): TokenResult;
  webhook(event: WebhookEvent): void;
  reconcile(method: PaymentMethod, period: DateRange): ReconciliationResult;
  // ... 20 more methods for "future flexibility"
}

// Reality: You only need to process credit cards
// All this code is complexity for requirements that don't exist
```

### Anti-Pattern 2: Premature Optimization

```typescript
// ❌ Fortune telling: "We'll have millions of users, so optimize now"
function getGreeting(userId: number) {
  // 100 lines of caching logic
  // 50 lines of format logic
  // 50 lines of locale logic
  const greeting = `Hello, ${getUser(userId).name}`; // The actual logic!
  // ...
}

// Reality: Greeting shows on profile (viewed maybe 10 times)
// All that caching is overkill
```

## Good Signs (Building for Reality)

### Pattern 1: Minimal, Focused Implementation

```typescript
// ✅ Build for what you know
function calculatePrice(product, customer) {
  const basePrice = product.price * customer.quantity;
  const discount = customer.isPremium ? 0.2 : 0;
  return basePrice * (1 - discount);
}

// Simple, clear, easy to test
// When you need taxes: add it
// When you need promos: add it
// One thing at a time
```

### Pattern 2: Design for Replaceability

```typescript
// ✅ Don't design for uncertain extension, design for easy replacement
interface PaymentProcessor {
  process(amount: number, token: string): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor {
  async process(amount: number, token: string): Promise<PaymentResult> {
    // Process credit card
    return result;
  }
}

// If you need PayPal later:
class PayPalProcessor implements PaymentProcessor {
  async process(amount: number, token: string): Promise<PaymentResult> {
    // Process PayPal
    return result;
  }
}

// No speculative design
// No unused code
// Interface only grows when needed
```

## How to Avoid Fortune Telling

### The "But We Might" Test

```
Question: "Should I implement this feature?"

❌ "But we might need it later"
❌ "But it's good design for the future"
❌ "But someone might want this"

✅ "Because the current requirements ask for it"
✅ "Because someone specifically asked for it"
✅ "Because I have a use case I'm implementing now"
```

**If you use "might," "could," "probably," "eventually" → fortune telling**

### The "YAGNI" Question

```
For every feature you want to add:
"Are we actually gonna need it?"

Only YES answers get implemented.
Maybe, probably, might, could → NO
```

## No Fortune Telling Workflow

### When Tempted to Over-Design

```
1. Notice temptation
   "Maybe we should add support for X"

2. Ask: Is X in current requirements?
   - Yes? Build it
   - No? Stop

3. Ask: Has someone specifically asked for X?
   - Yes? Build it
   - No? Stop

4. Ask: Can I add X later easily?
   - Yes? Wait; add when needed
   - No? Maybe build it now (reconsider)

5. Ask: Will X simplify current code?
   - Yes? Add it
   - No? Don't add it
```

## No Fortune Telling Checklist

When adding a feature:

- [ ] Is this in the current requirements?
- [ ] Did someone specifically ask for this?
- [ ] Am I solving a problem that actually exists?
- [ ] Would the code be simpler without this?
- [ ] Could I add this later if needed?
- [ ] Is this essential for today's functionality?
- [ ] Am I building for "might" or for "is"?
- [ ] Is this speculative?

If mostly YES to the first group and NO to the last: Build it.
Otherwise: Wait.

## Remember

**Don't fortune tell. Build for what you know.**

- 🎯 Implement current requirements
- 📝 Add features when asked
- 🔄 Refactor when needed
- 🧠 Keep it simple
- 📦 Design for replaceability (not extensibility)
- ⏰ Solve problems when they arrive

**When in doubt: YAGNI (You Aren't Gonna Need It)**
