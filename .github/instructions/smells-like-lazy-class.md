# Code Smell: Lazy Class

**Purpose**: Identify and eliminate classes that don't do much
**Audience**: You + AI (code review, refactoring)
**Category**: Dispensables (Unnecessary Code)
**Severity**: 🟢 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Lazy Class** is a class that isn't doing enough to pay for itself.

Classes have overhead: naming, inheritance, testing, documentation. If a class doesn't justify this overhead, it should be eliminated or merged with another class.

### Why It Matters

Lazy classes cause:
- ❌ Unnecessary complexity
- ❌ Extra files to maintain
- ❌ Confusing class hierarchies
- ❌ Over-engineering
- ❌ Harder to understand relationships

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Lazy class doing almost nothing
class UserValidator {
  // Only one method!
  // Could be part of User or UserService
  validateEmail(email: string): boolean {
    return email.includes('@');
  }
}

// ❌ SMELL: Subclass barely doing anything
abstract class Vehicle {
  drive() { }
}

class RollerSkates extends Vehicle {
  // Almost identical to Vehicle
  // Minimal specific behavior
  drive() {
    return 'rolling...';
  }
}

// ❌ SMELL: Wrapper adding no value
class UserHelper {
  // Only delegates to User
  getFullName(user: User): string {
    return user.getFullName();
  }

  isActive(user: User): boolean {
    return user.status === 'active';
  }
}

// Why is this class needed?
```

**Symptoms**:
- [ ] Class has only 1-2 methods
- [ ] Methods are just delegation
- [ ] No real behavior or logic
- [ ] Class is never subclassed
- [ ] Could easily be merged with another class
- [ ] Reason for existence is unclear

---

## 💔 Why It's Bad

### Problem 1: Unnecessary Complexity

```typescript
// ❌ Extra complexity for minimal benefit
class EmailFormatter {
  format(email: string): string {
    return email.toLowerCase();
  }
}

class EmailService {
  sendEmail(email: string) {
    const formatter = new EmailFormatter();
    const formatted = formatter.format(email);
    // Send email
  }
}

// Why is EmailFormatter its own class?
// Just use email.toLowerCase() directly
// Adds mental overhead without benefit
```

### Problem 2: Inflated Class Hierarchy

```typescript
// ❌ Too many classes for similar things
abstract class DataStore { }

class UserStore extends DataStore {
  // Just holds users
}

class ProductStore extends DataStore {
  // Just holds products
}

class OrderStore extends DataStore {
  // Just holds orders
}

// All almost identical
// Creates meaningless hierarchy
```

### Problem 3: Hard to Find Functionality

```typescript
// ❌ Where is the logic?
class OrderValidator {
  validate(order: Order): boolean {
    // Delegates to OrderService
    return OrderService.validate(order);
  }
}

class OrderService {
  static validate(order: Order): boolean {
    // Real validation logic
  }
}

// Searching for validation logic
// Finds OrderValidator first (which does nothing)
// Must dig deeper to find real implementation
```

---

## ✅ Refactoring Solutions

### Solution 1: Inline Class

```typescript
// ❌ BEFORE: Lazy wrapper class
class EmailFormatter {
  format(email: string): string {
    return email.toLowerCase();
  }
}

class EmailService {
  private formatter = new EmailFormatter();

  sendEmail(email: string) {
    const formatted = this.formatter.format(email);
    this.send(formatted);
  }
}

// ✅ AFTER: Inline the formatting
class EmailService {
  sendEmail(email: string) {
    const formatted = email.toLowerCase();
    this.send(formatted);
  }
}

// Simpler without EmailFormatter
```

### Solution 2: Merge with Another Class

```typescript
// ❌ BEFORE: Separate classes
class User {
  firstName: string;
  lastName: string;
  email: string;
}

class UserHelper {
  getFullName(user: User): string {
    return `${user.firstName} ${user.lastName}`;
  }

  isValidEmail(user: User): boolean {
    return user.email.includes('@');
  }
}

// ✅ AFTER: Merge into User
class User {
  firstName: string;
  lastName: string;
  email: string;

  getFullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  isValidEmail(): boolean {
    return this.email.includes('@');
  }
}

// Everything in one place
```

### Solution 3: Collapse Hierarchy

```typescript
// ❌ BEFORE: Lazy subclass
class Product {
  name: string;
  price: number;

  describe(): string {
    return `${this.name}: $${this.price}`;
  }
}

class DigitalProduct extends Product {
  // Doesn't add any behavior
  // Just marks as digital
  // Could be a property instead
}

// ✅ AFTER: Remove subclass, use property
class Product {
  name: string;
  price: number;
  isDigital: boolean;

  describe(): string {
    return `${this.name}: $${this.price}`;
  }
}

// Simpler without unnecessary subclass
```

### Solution 4: Use Composition

```typescript
// ❌ BEFORE: Unnecessary subclass
class BaseRepository {
  find(id: string) { }
  save(item: any) { }
}

class UserRepository extends BaseRepository {
  // Doesn't add anything
  // Just restricts to User type
}

// ✅ AFTER: Use composition
class Repository<T> {
  find(id: string): T { }
  save(item: T): void { }
}

const userRepository = new Repository<User>();

// Generic composition is cleaner
// No unnecessary subclass
```

---

## 📚 Relationship to Core Principles

- **YAGNI** - Don't create classes "just in case"
- **Simplicity** - Fewer classes = simpler codebase
- **ETC** - Lazy classes make changes harder

---

## ✅ Checklist: Avoid Lazy Classes

When creating classes:

- [ ] Does this class have meaningful responsibility?
- [ ] Would it be simpler to merge with another class?
- [ ] Is this class ever subclassed?
- [ ] Does this class justify its overhead?

---

## ✨ Remember

**DON'T DO**: Create classes that don't do enough.

**DO**: Merge lazy classes with classes they belong with.

**Rule of thumb**: If a class could be a property or method of another class, it probably should be.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-lazy-class.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Remove lazy classes. Merge lightweight classes together.**
