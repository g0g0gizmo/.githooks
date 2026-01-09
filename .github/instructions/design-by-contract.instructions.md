---
description: 'Establish explicit pre-conditions, post-conditions, and invariants in code'
---

# Design by Contract - Establish Clear Agreements

## Overview

Design by Contract (DbC) is a methodology for designing software that emphasizes establishing explicit agreements about what code expects and what it guarantees. Think of it like a legal contract: both parties have responsibilities, and if both honor their obligations, the system works reliably.

This principle ensures:

- Explicit pre-conditions that callers must respect
- Explicit post-conditions that code guarantees
- Invariants that remain true throughout an object's lifetime
- Clear failure points when contracts are violated
- Reduced need for defensive programming
- Better debugging when things go wrong

## Core Concepts

### 1. Preconditions (Client Responsibility)

**What must be true BEFORE the function is called**

```typescript
// Precondition: birthDate must be a valid Date in the past
function calculateAge(birthDate: Date): number {
  // Check: Client must provide valid Date
  if (birthDate > new Date()) {
    throw new Error("Precondition violated: birthDate must be in the past");
  }

  const today = new Date();
  return today.getFullYear() - birthDate.getFullYear();
}

// ✅ Correct usage (contract honored)
const age = calculateAge(new Date('1990-01-01'));

// ❌ Contract violation
const invalidAge = calculateAge(new Date('2030-01-01')); // Future date!
```

**Key Insight**: The client (caller) is responsible for meeting preconditions. If they violate the precondition, failure is their responsibility.

---

### 2. Postconditions (Supplier Responsibility)

**What the function GUARANTEES to be true after execution**

```typescript
// Postcondition: return value is between 0 and 20
function calculateDiscount(amount: number): number {
  if (amount < 100) return 0;
  if (amount < 500) return 10;
  return 20;

  // Guarantees: return value is always >= 0 and <= 20
  // Client can rely on this contract
}

// ✅ Valid: return value honored
const discount = calculateDiscount(150); // Returns 10

// If function returned -5, it would violate postcondition
```

**Key Insight**: The supplier (function) is responsible for meeting postconditions. If they violate the postcondition, failure is their responsibility.

---

### 3. Invariants (Class Contract)

**What remains true throughout an object's lifetime**

```csharp
public class BankAccount
{
    private decimal _balance;

    // INVARIANT: _balance must always be >= 0
    // This is true before and after every method call

    public void Withdraw(decimal amount)
    {
        // Precondition: amount must be positive
        if (amount <= 0) throw new InvalidOperationException();

        // Precondition: sufficient funds
        if (amount > _balance) throw new InsufficientFundsException();

        _balance -= amount;
        // Postcondition: _balance decreased by amount
        // Invariant still holds: _balance >= 0
    }

    public void Deposit(decimal amount)
    {
        // Precondition: amount must be positive
        if (amount <= 0) throw new InvalidOperationException();

        _balance += amount;
        // Postcondition: _balance increased by amount
        // Invariant still holds: _balance >= 0
    }
}
```

**Key Insight**: Invariants are checked at the boundaries of every public method. If any method violates an invariant, the class contract is broken.

---

## Implementation Strategies

### 1. Explicit Assertions

Use assertions to verify contracts in development:

```typescript
function processOrder(orderId: string, userId: string): Order {
  // Preconditions
  console.assert(orderId && orderId.length > 0, "orderId required");
  console.assert(userId && userId.length > 0, "userId required");

  const order = fetchOrder(orderId);
  console.assert(order !== null, "Order must exist");

  // Process order...

  // Postcondition
  console.assert(order.status === 'completed', "Order must be completed");

  return order;
}
```

---

### 2. Exception-Based Validation

Use exceptions when contract violations indicate real errors:

```typescript
function getUser(userId: string): User {
  // Precondition check
  if (!userId || userId.trim().length === 0) {
    throw new ValidationError("userId cannot be empty");
  }

  const user = database.findById(userId);

  // Postcondition check
  if (!user) {
    throw new NotFoundError(`User ${userId} does not exist`);
  }

  return user;
}
```

---

### 3. Type System Enforcement

Use types to express contracts:

```typescript
// Type system enforces precondition: userId must be string (not null/undefined)
function getUserOrders(userId: string): Order[] {
  // Precondition: userId exists and is non-empty
  if (!userId) throw new Error("userId is required");

  // Get and return orders
  const orders = database.findOrders(userId);

  // Postcondition: return array (may be empty, but never null)
  // Type system guarantees: Order[] not null
  return orders;
}
```

---

### 4. Documentation

Explicitly document contracts in comments and docs:

```typescript
/**
 * Calculates compound interest
 *
 * Preconditions:
 * - principal > 0: investment amount must be positive
 * - rate >= 0 && rate <= 100: interest rate between 0-100%
 * - years > 0: time period must be positive
 *
 * Postcondition:
 * - returns number >= principal: final amount >= investment
 *
 * Invariant:
 * - Pure function: no side effects
 *
 * @param principal Investment amount (must be positive)
 * @param rate Interest rate as percentage (0-100)
 * @param years Time period (must be positive)
 * @returns Final amount after compound interest
 */
function calculateInterest(
  principal: number,
  rate: number,
  years: number
): number {
  if (principal <= 0) throw new Error("Principal must be positive");
  if (rate < 0 || rate > 100) throw new Error("Rate must be 0-100%");
  if (years <= 0) throw new Error("Years must be positive");

  return principal * Math.pow(1 + rate / 100, years);
}
```

---

## Application Checklist

- [ ] Preconditions are validated at function entry
- [ ] Precondition violations throw meaningful errors
- [ ] Postconditions are documented or asserted
- [ ] Invariants are defined for classes
- [ ] Type system used to express contracts
- [ ] Contracts documented in comments/JSDoc
- [ ] Failure points are clear (precondition vs postcondition violation)
- [ ] Contract violations fail fast with clear messages
- [ ] Tests verify contract boundaries
- [ ] Defensive programming reduced through contracts

### When Designing Functions

1. **Define Preconditions**: What must be true before?
2. **Define Postconditions**: What will be true after?
3. **Document Contract**: Make it explicit in comments
4. **Validate Preconditions**: Check at function entry
5. **Verify Postconditions**: Ensure contract met before return

### When Testing

1. **Test Happy Path**: Valid preconditions, expected postcondition
2. **Test Precondition Violations**: Invalid inputs, expect exception
3. **Test Postcondition**: Verify return value meets guarantee
4. **Test Invariants**: Object state remains valid throughout

---

## Related Principles

- [SOLID Principles](../../.github/copilot/instructions/solid-principles.instructions.md) - Single Responsibility supports clear contracts
- [Testing Standards](../../.github/copilot/instructions/testing-standards.instructions.md) - Contracts make testing clearer
- [Code Quality Goals](../../.github/copilot/instructions/code-quality-goals.instructions.md) - Contracts improve reliability and maintainability

---

## Anti-Patterns

### Anti-Pattern 1: No Precondition Checks

```typescript
// ❌ Bad: No contract checking
function calculateAge(birthDate: Date): number {
  const today = new Date();
  return today.getFullYear() - birthDate.getFullYear();
  // What if birthDate is in the future? Wrong answer.
  // What if birthDate is null? Crashes.
}

// ✅ Good: Precondition validation
function calculateAge(birthDate: Date): number {
  if (!birthDate || birthDate > new Date()) {
    throw new Error("birthDate must be a valid date in the past");
  }
  return new Date().getFullYear() - birthDate.getFullYear();
}
```

### Anti-Pattern 2: Silent Failures

```typescript
// ❌ Bad: Violation silently returns wrong value
function getDiscount(amount: number): number {
  if (amount < 0) return 0; // Invalid precondition, but no error
  // Could also return undefined, null, or incorrect value
  return amount > 100 ? 10 : 0;
}

// ✅ Good: Contract violation fails explicitly
function getDiscount(amount: number): number {
  if (amount < 0) {
    throw new Error("Precondition violated: amount must be non-negative");
  }
  return amount > 100 ? 10 : 0;
}
```

### Anti-Pattern 3: Weak Postconditions

```typescript
// ❌ Bad: Postcondition not guaranteed
function getUserData(userId: string): User {
  const user = database.findById(userId);
  // No guarantee: might return null, undefined, or partial object
  return user;
}

// ✅ Good: Clear postcondition guarantee
function getUserData(userId: string): User {
  const user = database.findById(userId);
  if (!user) {
    throw new NotFoundError(`User ${userId} not found`);
  }
  // Guarantee: Never returns null or undefined
  return user;
}
```

### Anti-Pattern 4: Ambiguous Contracts

```typescript
// ❌ Bad: Contract is unclear
/**
 * Processes data
 * @param data - some data
 * @returns processed result
 */
function process(data) {
  // What must data contain?
  // What format is the result?
  // What errors can occur?
}

// ✅ Good: Contract is explicit
/**
 * Validates and processes user input
 *
 * Precondition:
 * - data must be a non-empty object with 'email' string field
 *
 * Postcondition:
 * - Returns User object with validated email
 * - Throws ValidationError if precondition violated
 *
 * Invariant:
 * - Email is always lowercase and trimmed
 */
function process(data: { email: string }): User {
  if (!data || !data.email || typeof data.email !== 'string') {
    throw new ValidationError("data must have email string field");
  }
  return { email: data.email.toLowerCase().trim() };
}
```

### Anti-Pattern 5: Violated Invariants

```typescript
// ❌ Bad: Invariant can be violated
class User {
  age: number;

  setAge(value: number) {
    // Invariant: age must be >= 0
    // But nothing prevents negative values
    this.age = value;
  }
}

// ✅ Good: Invariant is enforced
class User {
  private _age: number;

  // Invariant: _age must be >= 0
  setAge(value: number) {
    if (value < 0) {
      throw new Error("Invariant violation: age cannot be negative");
    }
    this._age = value;
  }

  getAge(): number {
    // Invariant guaranteed: always returns >= 0
    return this._age;
  }
}
```

---

## Benefits of Design by Contract

### 1. Clarity
- Explicit about what is expected
- Reduces ambiguity
- Makes assumptions visible
- Easier to understand code

### 2. Robustness
- Fails fast with clear errors
- Catches violations early
- Prevents silent failures
- Reduces defensive programming

### 3. Debuggability
- Identify exactly where contract breaks
- Know if caller or supplier violated contract
- Stack trace points to violation
- Blame assignment is clear

### 4. Confidence
- Know what to rely on
- Safe to make assumptions
- Don't need defensive checks everywhere
- Trust the contract

### 5. Testing
- Test contracts separately
- Verify preconditions enforced
- Verify postconditions met
- Test invariant preservation

---

## Why Design by Contract Matters

✅ **Reduces Bugs** - Explicit contracts prevent ambiguity
✅ **Improves Debuggability** - Clear failure points
✅ **Reduces Defensive Code** - Can trust contracts
✅ **Clarifies Intent** - What code expects is explicit
✅ **Makes Testing Easier** - Contract boundaries are clear
✅ **Improves Maintainability** - Changes to contracts are visible

Master Design by Contract, and your code becomes more reliable, maintainable, and easier to debug.
