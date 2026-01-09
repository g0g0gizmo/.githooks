---
description: 'Keep related things together - Measure how closely related and focused the responsibilities of a module are'
applyTo: '**/*'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [SOLID Principles](solid-principles.instructions.md) - Single Responsibility Principle ensures high cohesion
- [DRY (Don't Repeat Yourself)](../../.github/copilot/copilot/guidelines/dont-repeat-yourself.md) - High cohesion supports DRY by keeping related logic together

When implementing these guidelines, always consider how they reinforce these core principles.

# Cohesion

## Overview

Cohesion measures how closely related and focused the responsibilities of a single module, class, or component are. High cohesion means that elements within a module work together to fulfill a single, well-defined purpose. Low cohesion indicates a module is doing too many unrelated things.

**Cohesion is the glue that holds a module together. Strong cohesion means everything in the module belongs together.**

High cohesion leads to:
- Easier understanding (focused purpose)
- Better reusability (self-contained functionality)
- Simpler maintenance (changes are localized)
- Improved testability (clear boundaries)

Low cohesion leads to:
- Confusing code (too many responsibilities)
- Tight coupling (changes ripple through system)
- Difficult testing (many dependencies to mock)
- Poor reusability (can't extract useful parts)

## Types of Cohesion (Best to Worst)

### 1. Functional Cohesion (Highest ⭐⭐⭐⭐⭐)

**All elements contribute to a single, well-defined task.**

This is the ideal. Every method and property works together to accomplish one clear purpose.

```typescript
// ✅ Excellent: High functional cohesion
class EmailValidator {
  validate(email: string): boolean {
    return this.hasAtSymbol(email) &&
           this.hasValidDomain(email) &&
           this.hasValidLocalPart(email);
  }

  private hasAtSymbol(email: string): boolean {
    return email.includes('@');
  }

  private hasValidDomain(email: string): boolean {
    const domain = email.split('@')[1];
    return domain && domain.includes('.');
  }

  private hasValidLocalPart(email: string): boolean {
    const localPart = email.split('@')[0];
    return localPart && localPart.length > 0;
  }
}
```

All methods work together toward one goal: validating email addresses.

### 2. Sequential Cohesion (Strong ⭐⭐⭐⭐)

**Elements are grouped because the output of one is the input to the next.**

Good for pipeline or workflow scenarios.

```typescript
// ✅ Good: Sequential cohesion
class DataProcessor {
  process(rawData: string): ProcessedData {
    const cleaned = this.cleanData(rawData);
    const validated = this.validateData(cleaned);
    return this.transformData(validated);
  }

  private cleanData(data: string): string { /* ... */ }
  private validateData(data: string): ValidatedData { /* ... */ }
  private transformData(data: ValidatedData): ProcessedData { /* ... */ }
}
```

### 3. Communicational Cohesion (Moderate ⭐⭐⭐)

**Elements operate on the same data or contribute to the same output.**

Acceptable when elements share data but serve different aspects of a task.

```typescript
// ⚠️ Acceptable: Communicational cohesion
class CustomerReport {
  constructor(private customer: Customer) {}

  printAddress() { /* uses customer data */ }
  printPurchaseHistory() { /* uses customer data */ }
  printContactInfo() { /* uses customer data */ }
}
```

Better approach: Split into focused classes if these grow complex.

### 4. Low Cohesion (Avoid ❌)

**Elements are grouped arbitrarily with no clear relationship.**

```typescript
// ❌ Bad: Low cohesion - unrelated responsibilities
class Utilities {
  validateEmail(email: string): boolean { /* ... */ }
  calculateTax(amount: number): number { /* ... */ }
  formatDate(date: Date): string { /* ... */ }
  sendNotification(message: string): void { /* ... */ }
  hashPassword(password: string): string { /* ... */ }
}
```

## Achieving High Cohesion

### Pattern 1: Single Responsibility

```typescript
// ❌ Low cohesion: Multiple unrelated responsibilities
class UserManager {
  createUser() { /* ... */ }
  deleteUser() { /* ... */ }
  sendEmail() { /* ... */ }
  logActivity() { /* ... */ }
  generateReport() { /* ... */ }
}

// ✅ High cohesion: Split into focused classes
class UserRepository {
  create(user: User): User { /* ... */ }
  delete(id: string): void { /* ... */ }
  findById(id: string): User { /* ... */ }
}

class EmailService {
  send(to: string, subject: string, body: string): void { /* ... */ }
}

class ActivityLogger {
  log(event: string, details: object): void { /* ... */ }
}

class ReportGenerator {
  generate(type: string, data: object): Report { /* ... */ }
}
```

### Pattern 2: Group Related Operations

```typescript
// ✅ High cohesion: Related operations grouped together
class ShoppingCart {
  private items: CartItem[] = [];

  addItem(item: Product): void {
    this.items.push(item);
  }

  removeItem(itemId: string): void {
    this.items = this.items.filter(item => item.id !== itemId);
  }

  getTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  clear(): void {
    this.items = [];
  }
}
```

## Cohesion Checklist

When designing a module:

- [ ] Does every element contribute to a single, clear purpose?
- [ ] Can I describe the module's purpose in one sentence?
- [ ] Are all methods related to the same concept?
- [ ] If I remove one method, do the others still make sense together?
- [ ] Would I be comfortable with this module's name?
- [ ] Can I test this module in isolation?
- [ ] Are there any "utility" or "helper" methods that don't belong?

## Remember

**Keep related things together. High cohesion means focused, single-purpose modules.**

- 🎯 Each module should have one clear responsibility
- 📝 All elements should contribute to that responsibility
- 🔄 Related operations belong together
- 🧠 Unrelated operations should be separated
- ⏰ High cohesion improves maintainability

**If a module does too many unrelated things, split it.**
