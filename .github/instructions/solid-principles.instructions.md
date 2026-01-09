---
description: 'Five design principles for modular, flexible, and maintainable code'
---

# SOLID Principles

## Overview

SOLID is an acronym for five design principles that guide developers toward building modular, flexible, and maintainable code that resists breaking when changes occur. These principles help you write code that is easier to test, understand, and extend without requiring modifications to existing code.

SOLID principles ensure that:

- Code is modular and loosely coupled
- Each class has a single, well-defined responsibility
- New features can be added without changing existing code
- Dependencies are managed through abstractions
- Interfaces are focused and minimal
- Subtypes properly honor their parent contracts

## Core Concepts

### 1. Single Responsibility Principle (S)

**Definition**: Each class, module, or function should have **one reason to change**.

A class should do one thing and do it well. Multiple responsibilities mean multiple reasons to change, which increases coupling and fragility.

#### Test for Single Responsibility

```typescript
// ❌ Bad: Multiple responsibilities
class UserService {
  createUser(email: string, password: string) { }
  validateEmail(email: string) { }
  hashPassword(password: string) { }
  sendWelcomeEmail(user: User) { }
  // This class changes if user creation, validation, hashing, OR email logic changes
}

// ✅ Good: Each class one responsibility
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

**Quick Test**: Can I describe the class in one sentence without "and"?
- ✅ Yes: "UserService creates users"
- ❌ No: "UserService creates users and validates emails and hashes passwords"

---

### 2. Open/Closed Principle (O)

**Definition**: Software should be **open for extension, closed for modification**.

You should be able to add new features without changing existing code. Use abstraction and polymorphism to enable extension.

#### Extension Without Modification

```typescript
// ❌ Bad: Requires modification to add features
class PaymentProcessor {
  process(type: string, amount: number) {
    if (type === 'credit') {
      // credit logic
    } else if (type === 'paypal') {
      // paypal logic
    }
    // To add Stripe: must modify this function!
  }
}

// ✅ Good: Extend through new implementations
interface PaymentMethod {
  process(amount: number): boolean;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number) { /* credit logic */ }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number) { /* paypal logic */ }
}

class StripePayment implements PaymentMethod {
  process(amount: number) { /* stripe logic */ }
  // New! No existing code changed.
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}

  process(amount: number) {
    return this.method.process(amount);
  }
}
```

**Quick Test**: Can I add a feature without touching existing code?
- ✅ Yes: Create new class implementing interface
- ❌ No: Must edit existing classes/conditionals

---

### 3. Liskov Substitution Principle (L)

**Definition**: Subtypes must be **substitutable for base types**.

If B is a subtype of A, you should be able to use B anywhere A is expected without breaking behavior. Violations break polymorphism and create runtime surprises.

#### Proper Type Hierarchies

```typescript
// ❌ Bad: Dog extends Bird but breaks Bird contract
class Bird {
  fly() { }
}

class Dog extends Bird {
  fly() {
    throw new Error('Dogs cannot fly!');
  }
}

// Problem: Function expects Bird, gets Dog, crashes
function makeBirdFly(bird: Bird) {
  bird.fly(); // Crashes if bird is actually a Dog!
}

// ✅ Good: Proper hierarchy respects substitution
class Animal {
  move() { }
}

class Bird extends Animal {
  fly() { }
}

class Dog extends Animal {
  run() { }
}

// Now:
// - Any Animal can move() (Bird and Dog)
// - Only Bird can fly()
// - Only Dog can run()
// Substitution works!

function moveAnimal(animal: Animal) {
  animal.move(); // Works for Dog and Bird
}
```

**Quick Test**: If B extends A, can I use B everywhere A is expected?
- ✅ Yes: Substitution works properly
- ❌ No: Violates principle, creates bugs

---

### 4. Interface Segregation Principle (I)

**Definition**: Clients depend on **small, specific interfaces**, not fat ones.

Don't force classes to depend on methods they don't use. Split large interfaces into smaller, focused ones. Fat interfaces create unnecessary coupling.

#### Focused Interfaces

```typescript
// ❌ Bad: Fat interface forces implementations it doesn't need
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { }
  eat() { throw new Error('Robots do not eat'); }
  sleep() { throw new Error('Robots do not sleep'); }
}

// Problem: Robot forced to implement eat() and sleep() it doesn't need

// ✅ Good: Small, focused interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

// Human implements all
class Human implements Workable, Eatable, Sleepable {
  work() { }
  eat() { }
  sleep() { }
}

// Robot only implements what it needs
class Robot implements Workable {
  work() { }
}
```

**Quick Test**: Does the implementation need every method in the interface?
- ✅ Yes: Interface is properly segregated
- ❌ No: Interface is too fat, split it

---

### 5. Dependency Inversion Principle (D)

**Definition**: Depend on **abstractions**, not concrete implementations.

High-level modules shouldn't depend on low-level modules. Both should depend on abstractions. This enables flexibility, testability, and easy swapping of implementations.

#### Abstracting Dependencies

```typescript
// ❌ Bad: Hardcoded concrete dependency
class UserService {
  constructor() {
    this.db = new PostgresDatabase(); // Hardcoded!
  }

  createUser(email: string) {
    this.db.insert({ email });
  }
}

// Problem:
// - Can't swap to MongoDB without changing UserService
// - Can't test with mock database
// - UserService depends on concrete PostgresDatabase

// ✅ Good: Depends on abstraction
interface Database {
  insert(data: any): void;
  query(sql: string): any[];
}

class UserService {
  constructor(private db: Database) {}

  createUser(email: string) {
    this.db.insert({ email });
  }
}

// Implementations
class PostgresDatabase implements Database {
  insert(data: any) { /* postgres logic */ }
  query(sql: string) { /* postgres logic */ }
}

class MongoDatabase implements Database {
  insert(data: any) { /* mongo logic */ }
  query(sql: string) { /* mongo logic */ }
}

// Usage: Inject any Database implementation
const postgres = new PostgresDatabase();
const service = new UserService(postgres); // Works!

const mongo = new MongoDatabase();
const service2 = new UserService(mongo); // Also works!

// Testing: Easy with mock
class MockDatabase implements Database {
  insert(data: any) { /* test logic */ }
  query(sql: string) { /* test logic */ }
}

const testService = new UserService(new MockDatabase());
```

**Quick Test**: Can I swap implementations without changing the dependent code?
- ✅ Yes: Depends on abstraction
- ❌ No: Depends on concrete class

---

## Application Checklist

Review code against all SOLID principles:

- [ ] **Single Responsibility**: Each class has one reason to change
- [ ] **Open/Closed**: Can extend without modifying existing code
- [ ] **Liskov Substitution**: All subtypes properly honor parent contracts
- [ ] **Interface Segregation**: Interfaces are small and focused
- [ ] **Dependency Inversion**: Depends on abstractions, not concrete implementations

### When Refactoring

1. Does this class have one responsibility? → Single Responsibility
2. Can I extend without modifying? → Open/Closed
3. Are subtypes properly substitutable? → Liskov Substitution
4. Are interfaces focused? → Interface Segregation
5. Do I depend on abstractions? → Dependency Inversion

### When Designing New Features

Apply in order:

1. **S**: Keep responsibilities separate
2. **O**: Design for extension through abstraction
3. **L**: Ensure proper type hierarchies
4. **I**: Use focused, minimal interfaces
5. **D**: Depend on abstractions

### When Reviewing Code

Ask for each principle:

- Can this class be simplified? (S)
- Would extension require modification? (O)
- Are all subtype contracts honored? (L)
- Can this interface be split? (I)
- Can this dependency be abstracted? (D)

---

## Related Principles

- [Design by Contract](../../.github/copilot/instructions/design-by-contract.instructions.md) - SOLID builds on contract-based design
- [DRY Principle](../../.github/copilot/instructions/dry-principle.instructions.md) - SOLID avoids repeating responsibility patterns
- [KISS Principle](../../.github/copilot/instructions/kiss-principle.instructions.md) - SOLID achieves simplicity through separation of concerns
- [Code Quality Goals](../../.github/copilot/instructions/code-quality-goals.instructions.md) - SOLID improves all quality dimensions

---

## Anti-Patterns

### Anti-Pattern 1: God Object (S Violation)

```typescript
// ❌ Bad: One class doing everything
class User {
  validateEmail() { }
  hashPassword() { }
  sendEmail() { }
  saveToDatabase() { }
  generateToken() { }
  checkPermissions() { }
  logActivity() { }
}

// ✅ Good: Multiple classes, each with one responsibility
class User { /* just user data */ }
class EmailValidator { }
class PasswordService { }
class EmailSender { }
class UserRepository { }
class AuthTokenService { }
class PermissionChecker { }
class ActivityLogger { }
```

### Anti-Pattern 2: Closed for Extension (O Violation)

```typescript
// ❌ Bad: Adding features requires modifying existing code
if (paymentType === 'credit') { ... }
else if (paymentType === 'paypal') { ... }
else if (paymentType === 'stripe') { ... }
// To add ApplePay: modify this whole function!

// ✅ Good: Add implementations without changing existing code
interface PaymentMethod { process(): void; }
class ApplePayment implements PaymentMethod { }
// No existing code touched
```

### Anti-Pattern 3: Improper Hierarchies (L Violation)

```typescript
// ❌ Bad: Subclass doesn't honor parent contract
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
}

class Square extends Rectangle {
  setWidth(w: number) { this.width = w; this.height = w; }
  setHeight(h: number) { this.height = h; this.width = h; }
}

// Problem: Square client using Rectangle breaks
const rect: Rectangle = new Square();
rect.setWidth(5);
rect.setHeight(10);
// For Square, width becomes 10! Not what caller expected

// ✅ Good: Use composition or proper hierarchies
interface Shape { area(): number; }
class Rectangle implements Shape { }
class Square implements Shape { }
```

### Anti-Pattern 4: Fat Interfaces (I Violation)

```typescript
// ❌ Bad: Implementations forced to implement unused methods
interface FileHandler {
  read(): string;
  write(data: string): void;
  execute(): void;
  compress(): void;
  encrypt(): void;
}

class TextFileHandler implements FileHandler {
  read() { }
  write(data) { }
  execute() { throw new Error('Text files do not execute'); }
  compress() { throw new Error('Not implemented'); }
  encrypt() { throw new Error('Not implemented'); }
}

// ✅ Good: Split into focused interfaces
interface Readable { read(): string; }
interface Writable { write(data: string): void; }
interface Executable { execute(): void; }
interface Compressible { compress(): void; }
interface Encryptable { encrypt(): void; }

class TextFileHandler implements Readable, Writable { }
class ExecutableFile implements Readable, Executable { }
```

### Anti-Pattern 5: Concrete Dependencies (D Violation)

```typescript
// ❌ Bad: Hardcoded concrete class dependencies
class OrderService {
  constructor() {
    this.emailService = new GmailService();
    this.paymentProcessor = new StripeProcessor();
    this.database = new PostgresDatabase();
  }
}

// Problems:
// - Can't swap implementations
// - Can't test with mocks
// - Tightly coupled to specific implementations

// ✅ Good: Injected abstract dependencies
class OrderService {
  constructor(
    private emailService: EmailService,
    private paymentProcessor: PaymentProcessor,
    private database: Database
  ) {}
}

// Usage with different implementations
new OrderService(
  new GmailService(),
  new StripeProcessor(),
  new PostgresDatabase()
);

// Usage with mocks for testing
new OrderService(
  new MockEmailService(),
  new MockPaymentProcessor(),
  new MockDatabase()
);
```

## Common Violations & Fixes

| Violation   | Symptom                                      | Fix                                            |
| ----------- | -------------------------------------------- | ---------------------------------------------- |
| S Violation | Class has many reasons to change             | Extract responsibilities into separate classes |
| O Violation | New features require modifying existing code | Use abstraction and polymorphism               |
| L Violation | Subclass breaks parent contract              | Fix hierarchy or use composition               |
| I Violation | Implementations have unused methods          | Split interface into focused ones              |
| D Violation | Hard to test or swap implementations         | Inject abstractions, not concrete classes      |

---

## Why SOLID Matters

✅ **Maintainability** - Easy to change without unintended side effects
✅ **Testability** - Classes can be tested in isolation
✅ **Reusability** - Components work in different contexts
✅ **Clarity** - Each part has clear, focused purpose
✅ **Flexibility** - Easy to extend and adapt to new requirements
✅ **Scalability** - Code structure scales with project growth

Master SOLID, and your code becomes more professional, maintainable, and resilient to change.
