---
description: 'Each class/module/function should have one reason to change - the foundation of SOLID principles'
applyTo: '**/*'
---


## Core Engineering Principles

This instruction set applies the following foundational principles:

- [SOLID Principles](solid-principles.md) - Single Responsibility is the foundation of SOLID
- [DRY (Don't Repeat Yourself)](dry-principle.instructions.md) - SRP helps avoid duplication by focusing responsibilities
- [Cohesion](cohesion.instructions.md) - SRP ensures high cohesion within classes
- [Orthogonality](orthogonality.instructions.md) - SRP creates independent, non-interfering components

When implementing these guidelines, always consider how they reinforce these core principles.

# Single Responsibility Principle (SRP)

## Core Concept

**Definition**: Each class/module/function has **one reason to change**.

In other words: One job, one responsibility, one reason to modify.

**Why**: When something has multiple reasons to change, modifying for one reason breaks another.

## The Test

Can I describe the class in one sentence without "and"?

- ✅ "UserService creates users"
- ❌ "UserService creates users and validates emails and hashes passwords"

## Anti-Pattern: Multiple Responsibilities

```typescript
// ❌ UserService does TOO MUCH
class UserService {
  createUser(email: string) { }
  validateEmail(email: string) { }
  hashPassword(password: string) { }
  sendWelcomeEmail(user: User) { }
}

// If email validation changes → update UserService
// If password hashing changes → update UserService
// If email sending changes → update UserService
// 3 reasons to change!
```

**Problem**: This class will change when:

1. User creation logic changes
2. Email validation rules change
3. Password hashing algorithm changes
4. Email sending mechanism changes

## Proper Implementation

```typescript
// ✅ Each class has ONE reason to change
class UserService {
  createUser(email: string, hashedPassword: string) { }
  // Only reason to change: user creation logic
}

class EmailValidator {
  validate(email: string): boolean { }
  // Only reason to change: validation rules
}

class PasswordService {
  hash(password: string): string { }
  // Only reason to change: hashing algorithm
}

class EmailSender {
  sendWelcomeEmail(user: User) { }
  // Only reason to change: email sending logic
}
```

**Benefits**:

- Each class is focused and easy to understand
- Changes are localized
- Testing is simpler (fewer dependencies)
- Reusability increases (can use EmailValidator elsewhere)

## Identifying Violations

**Warning Signs**:

- Class name contains "and" or "Manager"
- Multiple unrelated methods
- Large number of imports
- Difficult to name the class clearly
- Hard to summarize what the class does
- Changes in different areas require touching the same class

## When to Apply

**Apply SRP when**:

- Designing new classes
- Class grows beyond 200-300 lines
- Multiple team members frequently change same class
- Testing becomes difficult
- Extracting interface feels unnatural

**Balance with**:

- [KISS Principle](../../.github/instructions/kiss-principle.instructions.md) - Don't over-engineer with too many classes
- Pragmatism - Sometimes a small amount of related responsibility is OK

## Relationships


**Enables**:

- [Open/Closed Principle](open-closed-principle.instructions.md) - Easier to extend when focused
- [Interface Segregation Principle](interface-segregation-principle.instructions.md) - Natural small interfaces
- [Dependency Inversion Principle](dependency-inversion-principle.instructions.md) - Clear abstractions emerge


**Related Concepts**:

- [Atomic Notes Principle](atomic-notes.instructions.md) - SRP makes classes atomic
- [Cohesion](cohesion.instructions.md) - High cohesion within, low coupling between


**Part of**:

- [SOLID Principles](solid-principles.md) - The foundation principle

## Real-World Example

### Authentication System

**Bad** (God Class):

```typescript
class AuthService {
  validateCredentials(username, password) { }
  hashPassword(password) { }
  generateToken(user) { }
  sendPasswordReset(email) { }
  logAuthAttempt(username, success) { }
  checkRateLimit(ip) { }
}
```

**Good** (SRP Applied):

```typescript
class AuthService {
  authenticate(credentials: Credentials): AuthResult { }
}

class PasswordHasher {
  hash(password: string): string { }
  verify(password: string, hash: string): boolean { }
}

class TokenGenerator {
  generate(user: User): Token { }
  validate(token: Token): boolean { }
}

class PasswordResetService {
  requestReset(email: string): void { }
  completeReset(token: string, newPassword: string): void { }
}

class AuthLogger {
  logAttempt(username: string, success: boolean): void { }
}

class RateLimiter {
  checkLimit(ip: string): boolean { }
  recordAttempt(ip: string): void { }
}
```

## Checklist

Before committing a class, verify:

- [ ] Can describe the class in one clear sentence
- [ ] Class has one primary reason to change
- [ ] All methods support the single responsibility
- [ ] No unrelated utility methods
- [ ] Easy to name without "Manager", "Helper", or "Util"
- [ ] Changes in different features don't affect this class

## Why Single Responsibility Matters

✅ **Maintainability** - Changes are localized and predictable
✅ **Testability** - Single responsibility means simpler tests
✅ **Reusability** - Focused classes work in multiple contexts
✅ **Understandability** - Clear purpose makes code easy to read
✅ **Flexibility** - Easy to extend or replace focused components

Master Single Responsibility, and your codebase becomes modular, testable, and maintainable.
