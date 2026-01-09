# Single Responsibility Principle (SRP)

**Purpose**: Each class/module/function should have one reason to change
**Audience**: Developers, architects, code reviewers
**Focus**: Separation of concerns and cohesion

---

## 🎯 Core Concept

**Definition**: Each class/module/function has **one reason to change**.

In other words: One job, one responsibility, one reason to modify.

**Why**: When something has multiple reasons to change, modifying for one reason breaks another.

---

## 📝 The Test

Can I describe the class in one sentence without "and"?

- ✅ "UserService creates users"
- ❌ "UserService creates users and validates emails and hashes passwords"

---

## ❌ Anti-Pattern: Multiple Responsibilities

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

---

## ✅ Proper Implementation

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

---

## 🔍 Identifying Violations

**Warning Signs**:

- Class name contains "and" or "Manager"
- Multiple unrelated methods
- Large number of imports
- Difficult to name the class clearly
- Hard to summarize what the class does
- Changes in different areas require touching the same class

---

## 🎓 When to Apply

**Apply SRP when**:

- Designing new classes
- Class grows beyond 200-300 lines
- Multiple team members frequently change same class
- Testing becomes difficult
- Extracting interface feels unnatural

**Balance with**:

- [KISS](../../.github/copilot/core/principles/KISS.md) - Don't over-engineer with too many classes
- Pragmatism - Sometimes a small amount of related responsibility is OK

---

## 🔗 Relationships

**Enables**:

- [Open/Closed Principle](../../.github/copilot/core/principles/open-closed-principle.md) - Easier to extend when focused
- [Interface Segregation](../../.github/copilot/core/principles/interface-segregation-principle.md) - Natural small interfaces
- [Dependency Inversion](../../.github/copilot/core/principles/dependency-inversion-principle.md) - Clear abstractions emerge

**Related Concepts**:

- [Atomic](../../.github/copilot/core/principles/atomic-notes.md) - SRP makes classes atomic
- [Cohesion](../../.github/copilot/core/principles/cohesion.md) - High cohesion within, low coupling between
- [Separation of Concerns](../../.github/copilot/core/principles/separation-of-concerns.md) - SRP is the class-level application

**Part of**:

- [SOLID Principles](../../.github/copilot/core/principles/SOLID.md) - The foundation principle

---

## 📚 Real-World Example

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

---

## ✅ Checklist

Before committing a class, verify:

- [ ] Can describe the class in one clear sentence
- [ ] Class has one primary reason to change
- [ ] All methods support the single responsibility
- [ ] No unrelated utility methods
- [ ] Easy to name without "Manager", "Helper", or "Util"
- [ ] Changes in different features don't affect this class

---

**Version**: 1.0
**Created**: 2025-11-28
**Last Updated**: 2025-11-28
**Tags**: #solid #design-principles #architecture #cohesion
