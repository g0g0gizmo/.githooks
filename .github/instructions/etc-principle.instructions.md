---
description: Design code that is easy to modify, extend, and maintain - the fundamental principle for software
applyTo: '**/*'
---


## Core Engineering Principles

This instruction set applies the following foundational principles:

- DRY (Don't Repeat Yourself) - Minimize duplication and maximize reuse
- SOLID principles - Modular, flexible, maintainable design

When implementing these guidelines, always consider how they reinforce these core principles.

# ETC (Easier To Change)

## Overview

### ETC = Easier To Change

This is the fundamental principle from *The Pragmatic Programmer* that underlies all good design decisions. Rather than memorizing a dozen design patterns or principles, ask one simple question:

**Will this change make the code easier to change in the future?**

If yes: do it. If no: find another way.

## Core Concept

Good design is not about following rules. Good design is about **making code that is easy to change**.

Everything else in software design—SOLID principles, refactoring techniques, design patterns, testing strategies—exists to serve this one goal: **make code easier to change**.

### Why ETC Matters

Every line of code you write will eventually need to change. Requirements change. Technologies evolve. Bugs emerge. Features expand. If your code is hard to change, these inevitable changes become costly, risky, and painful.

Easy-to-change code means:

- ✅ Changes don't break unrelated functionality
- ✅ New features can be added safely
- ✅ Bugs can be fixed quickly
- ✅ Refactoring is low-risk
- ✅ Team moves faster
- ✅ Less fear when modifying code

## The Universal Test

When facing a design decision, ask:

> Will this make code easier or harder to change?

Apply this to:

- Function design (should we extract this?)
- Class structure (too many responsibilities?)
- Module boundaries (how should we organize?)
- Testing approach (what's easiest to test?)
- Documentation (will future developers understand?)
- Naming (will others understand this without explanation?)
- Architecture (can we replace this component?)

### Decision Framework

```text
Design Decision
    ↓
Does it make code easier to change?
    ↓
YES → Do it
NO  → Don't do it / Find another way
```

## Red Flags (Harder to Change)

### Anti-Pattern 1: Tight Coupling

Components depend heavily on each other. Changing one requires changing many.

```typescript
// ❌ Hard to change: tight coupling
class PaymentProcessor {
  private emailService = new GmailService(); // Hardcoded
  private database = new PostgresDatabase(); // Hardcoded

  async processPayment(amount: number) {
    this.database.save({ amount });
    this.emailService.send('payment@example.com', 'Payment received');
  }
}

// Problem: To swap Gmail for SendGrid or Postgres for MongoDB,
// must change PaymentProcessor. This is HARD to change.
```

### Anti-Pattern 2: Mixing Concerns

Multiple responsibilities in one place. Changing one concern affects others.

```typescript
// ❌ Hard to change: mixed concerns
class UserService {
  // User CRUD + email + logging + validation + billing
  createUser() { /* ... */ }
  sendEmail() { /* ... */ }
  logActivity() { /* ... */ }
  validateInput() { /* ... */ }
  processBilling() { /* ... */ }
}

// Problem: Changing email logic risks breaking user creation.
// This is HARD to change.
```

## Good Signs (Easier to Change)

### Pattern 1: Loose Coupling

Components depend on abstractions, not concrete implementations.

```typescript
// ✅ Easy to change: loose coupling
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class PaymentProcessor {
  constructor(
    private emailService: EmailService,
    private database: Database
  ) {}

  async processPayment(amount: number) {
    await this.database.save({ amount });
    await this.emailService.send('payment@example.com', 'Payment received');
  }
}

// Swap email providers without changing PaymentProcessor
// This is EASY to change.
```

### Pattern 2: Single Responsibility

Each module does one thing well.

```typescript
// ✅ Easy to change: single responsibility
class UserRepository {
  create(user: User): Promise<User> { /* ... */ }
  findById(id: string): Promise<User> { /* ... */ }
  update(user: User): Promise<User> { /* ... */ }
}

class EmailService {
  sendWelcomeEmail(user: User): Promise<void> { /* ... */ }
}

class UserValidator {
  validate(user: User): ValidationResult { /* ... */ }
}

// Each class has one reason to change
// This is EASY to change.
```

## ETC in Practice

### Example 1: Configuration

```typescript
// ❌ Hard to change: hardcoded values
function connectDatabase() {
  return connect('localhost', 5432, 'mydb', 'admin', 'password123');
}

// ✅ Easy to change: externalized configuration
function connectDatabase(config: DatabaseConfig) {
  return connect(
    config.host,
    config.port,
    config.database,
    config.user,
    config.password
  );
}
```

### Example 2: Dependencies

```typescript
// ❌ Hard to change: concrete dependency
class OrderService {
  private stripe = new StripePaymentGateway();

  processOrder(order: Order) {
    this.stripe.charge(order.total);
  }
}

// ✅ Easy to change: dependency injection
class OrderService {
  constructor(private paymentGateway: PaymentGateway) {}

  processOrder(order: Order) {
    this.paymentGateway.charge(order.total);
  }
}
```

### Example 3: Testability

```typescript
// ❌ Hard to change: hard to test
class UserService {
  register(email: string) {
    const timestamp = Date.now(); // Hardcoded dependency on time
    const id = Math.random(); // Hardcoded dependency on random
    // ...
  }
}

// ✅ Easy to change: easy to test
class UserService {
  constructor(
    private clock: Clock,
    private idGenerator: IdGenerator
  ) {}

  register(email: string) {
    const timestamp = this.clock.now();
    const id = this.idGenerator.generate();
    // ...
  }
}
```

## ETC Checklist

When making a design decision:

- [ ] Will this change make the code easier or harder to change?
- [ ] Are components loosely coupled?
- [ ] Does each module have a single, clear responsibility?
- [ ] Can I test this change in isolation?
- [ ] Can I replace this component without affecting others?
- [ ] Will future developers understand my intent?
- [ ] Is configuration externalized?
- [ ] Are dependencies injected (not hardcoded)?
- [ ] Can this be extended without modification?

## Remember

**The single most important design principle: Will this make code easier to change?**

- 🎯 Design for change
- 📝 Loose coupling over tight coupling
- 🔄 Single responsibility over multiple concerns
- 🧠 Abstractions over concrete implementations
- ⏰ Externalize configuration

**If it makes code harder to change, find another way.**
