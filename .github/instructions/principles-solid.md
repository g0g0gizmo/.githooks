# SOLID Principles

## Overview

SOLID is an acronym for five fundamental principles of object-oriented design that make software more maintainable, flexible, and easier to understand. When applied together, these principles lead to code that is easier to modify, test, and extend.

## The Five SOLID Principles

### 1. Single Responsibility Principle (SRP)

**A class should have one, and only one, reason to change.**

Each class should have a single, well-defined responsibility. When a class tries to do too many things, changes to one responsibility can break another.

**Learn more**: [Single Responsibility Principle](./single-responsibility-principle.md)

**Example:**
```typescript
// ❌ Bad: Multiple responsibilities
class UserManager {
  saveUser(user: User) { /* database logic */ }
  sendWelcomeEmail(user: User) { /* email logic */ }
  generateReport(user: User) { /* reporting logic */ }
}

// ✅ Good: Single responsibility per class
class UserRepository {
  saveUser(user: User) { /* database logic only */ }
}

class EmailService {
  sendWelcomeEmail(user: User) { /* email logic only */ }
}

class ReportGenerator {
  generateUserReport(user: User) { /* reporting logic only */ }
}
```

### 2. Open/Closed Principle (OCP)

**Software entities should be open for extension but closed for modification.**

You should be able to extend behavior without modifying existing code. Use abstraction and polymorphism to achieve this.

**Learn more**: [Open/Closed Principle](./open-closed-principle.md)

**Example:**
```typescript
// ❌ Bad: Must modify class to add new discount types
class PriceCalculator {
  calculate(price: number, discountType: string): number {
    if (discountType === 'seasonal') {
      return price * 0.9;
    } else if (discountType === 'clearance') {
      return price * 0.5;
    }
    return price;
  }
}

// ✅ Good: Extend through new classes
interface DiscountStrategy {
  apply(price: number): number;
}

class SeasonalDiscount implements DiscountStrategy {
  apply(price: number): number {
    return price * 0.9;
  }
}

class ClearanceDiscount implements DiscountStrategy {
  apply(price: number): number {
    return price * 0.5;
  }
}

class PriceCalculator {
  calculate(price: number, discount: DiscountStrategy): number {
    return discount.apply(price);
  }
}
```

### 3. Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for their base types without breaking the program.**

Derived classes should extend base classes without changing their behavior in unexpected ways.

**Learn more**: [Liskov Substitution Principle](./liskov-substitution-principle.md)

**Example:**
```typescript
// ❌ Bad: Square violates LSP (changes width also changes height)
class Rectangle {
  constructor(protected width: number, protected height: number) {}

  setWidth(width: number) { this.width = width; }
  setHeight(height: number) { this.height = height; }

  getArea(): number { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(width: number) {
    this.width = width;
    this.height = width; // Unexpected side effect!
  }
}

// ✅ Good: Use composition or separate hierarchies
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  getArea(): number { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  getArea(): number { return this.side * this.side; }
}
```

### 4. Interface Segregation Principle (ISP)

**No client should be forced to depend on methods it does not use.**

Create specific, focused interfaces rather than large, general-purpose ones. Clients should only implement the methods they actually need.

**Learn more**: [Interface Segregation Principle](./interface-segregation-principle.md)

**Example:**
```typescript
// ❌ Bad: Worker forced to implement methods it doesn't use
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* do work */ }
  eat() { /* Robots don't eat! */ throw new Error("Not applicable"); }
  sleep() { /* Robots don't sleep! */ throw new Error("Not applicable"); }
}

// ✅ Good: Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Robot implements Workable {
  work() { /* do work */ }
}

class Human implements Workable, Eatable, Sleepable {
  work() { /* do work */ }
  eat() { /* eat food */ }
  sleep() { /* sleep */ }
}
```

### 5. Dependency Inversion Principle (DIP)

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

Depend on interfaces or abstract classes rather than concrete implementations. This decouples components and makes them easier to test and modify.

**Learn more**: [Dependency Inversion Principle](./dependency-inversion-principle.md)

**Example:**
```typescript
// ❌ Bad: High-level class depends on low-level implementation
class MySQLDatabase {
  save(data: string) { /* MySQL-specific code */ }
}

class UserService {
  private db = new MySQLDatabase(); // Tightly coupled!

  saveUser(user: User) {
    this.db.save(JSON.stringify(user));
  }
}

// ✅ Good: Both depend on abstraction
interface Database {
  save(data: string): void;
}

class MySQLDatabase implements Database {
  save(data: string) { /* MySQL-specific code */ }
}

class PostgreSQLDatabase implements Database {
  save(data: string) { /* PostgreSQL-specific code */ }
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction

  saveUser(user: User) {
    this.db.save(JSON.stringify(user));
  }
}

// Easy to swap implementations
const mysqlService = new UserService(new MySQLDatabase());
const postgresService = new UserService(new PostgreSQLDatabase());
```

## Why SOLID Matters

### 1. Maintainability
- Changes are localized and predictable
- Easier to find and fix bugs
- Reduced cognitive load when understanding code

### 2. Testability
- Components can be tested in isolation
- Dependencies can be mocked or stubbed
- Tests are faster and more reliable

### 3. Flexibility
- New features can be added with minimal changes
- Components can be easily replaced or extended
- System architecture can evolve without breaking existing code

### 4. Reusability
- Components are more focused and generic
- Easier to extract and reuse in other contexts
- Less duplication across the codebase

## Applying SOLID in Practice

### Start with SRP
Begin by ensuring classes have a single responsibility. This is the foundation for other principles.

### Use Interfaces
Define abstractions (interfaces/abstract classes) before implementations. This supports OCP, ISP, and DIP.

### Refactor Gradually
Apply SOLID principles incrementally during refactoring. Don't try to perfect everything at once.

### Balance with Pragmatism
SOLID principles guide design but shouldn't lead to over-engineering. Apply them where they provide clear value.

## Connection to Other Principles

- [Cohesion](./cohesion.md): SOLID principles promote high cohesion
- [Separation of Concerns](./separation-of-concerns.md): SOLID enforces clear separation
- [Code Quality Standards](./code-quality-standards.md): SOLID is a cornerstone of quality
- [Testing Standards](./testing-standards.md): SOLID makes code more testable
- [Refactoring](./refactoring-techniques.md): Use these techniques to achieve SOLID design

## Common Pitfalls

❌ **Over-Abstraction**: Creating interfaces for every class
❌ **Premature Optimization**: Applying SOLID before understanding requirements
❌ **Rigidity**: Following SOLID dogmatically without context
❌ **Complexity**: Adding unnecessary layers and indirection

## Quick Reference

| Principle | Focus                        | Key Benefit                     |
| --------- | ---------------------------- | ------------------------------- |
| **S**RP   | One responsibility per class | Easier to understand and change |
| **O**CP   | Extend without modifying     | Stable, flexible codebase       |
| **L**SP   | Substitutability of subtypes | Reliable polymorphism           |
| **I**SP   | Focused interfaces           | No unused dependencies          |
| **D**IP   | Depend on abstractions       | Loose coupling, testability     |

## Summary

SOLID principles are not rules to be followed blindly, but guidelines that help create maintainable, flexible, and testable code. They work together to promote:

- **Low coupling**: Components are independent
- **High cohesion**: Components have focused responsibilities
- **Clear abstractions**: Interfaces define contracts
- **Easy testing**: Dependencies can be mocked
- **Sustainable growth**: Code can evolve without breaking

**Remember**: SOLID is a means to an end—better software. Apply these principles judiciously to serve your project's needs.
