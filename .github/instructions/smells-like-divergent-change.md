# Code Smell: Divergent Change

**Purpose**: Identify and avoid classes changed for multiple unrelated reasons
**Audience**: You + AI (code review, refactoring)
**Category**: Change Preventers (Hard to Modify)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Divergent Change** occurs when a single class is modified for multiple, unrelated reasons.

A class should have one reason to change. When different types of changes affect the same class, it violates Single Responsibility and should be split.

### Why It Matters

Divergent change causes:
- ❌ Violates Single Responsibility Principle
- ❌ Class does too many things
- ❌ Hard to understand class purpose
- ❌ Difficult to test (must test multiple concerns)
- ❌ Changes for one reason break other functionality

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Class changed for multiple reasons
class UserService {
  // Reason 1: Business logic changes
  createUser(email: string, password: string) {
    // Business logic
  }

  updateProfile(userId: string, name: string) {
    // Business logic
  }

  // Reason 2: Database schema changes
  private mapUserToDatabase(user: User) {
    // Mapping logic
    // Must change when DB schema changes
  }

  saveToDatabase(user: User) {
    const dbUser = this.mapUserToDatabase(user);
    db.insert('users', dbUser);
  }

  // Reason 3: Email sending changes
  sendWelcomeEmail(user: User) {
    // Email logic
    // Must change when email service changes
  }

  // Reason 4: Logging changes
  private logUserAction(action: string, userId: string) {
    // Logging logic
    // Must change when logging format changes
  }

  // Reason 5: Password hashing changes
  private hashPassword(password: string) {
    // Hashing logic
    // Must change when hash algorithm changes
  }
}

// UserService changed because of:
// 1. Business rule changes
// 2. Database schema changes
// 3. Email service changes
// 4. Logging format changes
// 5. Password hashing algorithm changes
// = 5 DIFFERENT REASONS!
```

**Symptoms**:
- [ ] Multiple different reasons to change a class
- [ ] Comments like "// Database logic", "// Email logic", "// Validation"
- [ ] Different methods use different dependencies
- [ ] Hard to describe class purpose in one sentence
- [ ] Tests need to mock many different systems
- [ ] Change in one area breaks unrelated area

---

## 💔 Why It's Bad

### Problem 1: Changes Break Unrelated Code

```typescript
// ❌ Change email service → breaks user creation
class UserService {
  createUser(email: string, password: string) {
    // User creation logic
    const user = new User(email, password);
    this.sendWelcomeEmail(user);  // Email logic here!
    return user;
  }

  private sendWelcomeEmail(user: User) {
    // Email service call
    emailService.send(user.email, 'Welcome!');
  }
}

// Email service changes → sendWelcomeEmail() breaks
// This breaks createUser() even though business logic didn't change!
```

### Problem 2: Hard to Test

```typescript
// ❌ Must mock everything to test one thing
describe('UserService.createUser', () => {
  it('should create user with valid email', () => {
    // Mock database
    const mockDb = jest.fn();
    // Mock email service
    const mockEmailService = jest.fn();
    // Mock hashing service
    const mockHasher = jest.fn().mockReturnValue('hashed');
    // Mock logging service
    const mockLogger = jest.fn();
    // Mock validation service
    const mockValidator = jest.fn().mockReturnValue(true);

    // Now test setup is huge
    const service = new UserService(mockDb, mockEmailService, mockHasher, mockLogger, mockValidator);

    const result = service.createUser('test@example.com', 'password123');

    expect(result.email).toBe('test@example.com');
  });

  // Test is 30 lines for 5 lines of actual logic!
});
```

### Problem 3: Unclear Responsibility

```typescript
// ❌ What is UserService responsible for?
class UserService {
  // Is it responsible for validation?
  validateEmail(email: string): boolean { }

  // Is it responsible for persistence?
  saveUser(user: User): void { }

  // Is it responsible for communication?
  sendEmail(user: User): void { }

  // Is it responsible for hashing?
  hashPassword(password: string): string { }

  // Is it responsible for logging?
  logUserAction(action: string): void { }

  // Is it responsible for user business logic?
  updateProfile(userId: string, profile: Profile): void { }
}

// Answer: Too many things!
// Hard to understand what UserService "is"
```

### Problem 4: Code Fragility

```typescript
// ❌ Unrelated changes break things
class OrderService {
  // Order creation (business logic)
  createOrder(items: Item[]): Order {
    return new Order(items);
  }

  // Payment processing (payment logic)
  processPayment(order: Order, amount: number) {
    // Process payment
    this.recordPayment(order, amount);
    this.sendPaymentEmail(order);  // Email here!
  }

  // Tax calculation (tax logic)
  calculateTax(amount: number): number {
    // Calculate tax
  }

  // Email sending (communication logic)
  private sendPaymentEmail(order: Order) {
    // Send email
  }

  // Logging (monitoring logic)
  private recordPayment(order: Order, amount: number) {
    logger.info(`Payment: ${amount}`);
  }
}

// Change requirements:
// Tax rates change → Must edit OrderService.calculateTax()
// Email template changes → Must edit OrderService.sendPaymentEmail()
// Payment processor changes → Must edit OrderService.processPayment()
// All touching the same class!
```

---

## ✅ Refactoring Solutions

### Solution 1: Extract Class by Responsibility

```typescript
// ❌ BEFORE: Multiple responsibilities
class UserService {
  createUser(email: string, password: string) {
    // Validate
    if (!this.validateEmail(email)) throw new Error('Invalid email');
    if (!this.validatePassword(password)) throw new Error('Invalid password');

    // Hash password
    const hash = bcrypt.hash(password);

    // Create user
    const user = new User(email, hash);

    // Save to DB
    db.insert('users', user);

    // Send email
    emailService.send(email, 'Welcome!');

    // Log
    logger.info('User created', { email });

    return user;
  }

  private validateEmail(email: string) { }
  private validatePassword(password: string) { }
  private mapUserToDatabase(user: User) { }
}

// ✅ AFTER: Each responsibility is own class
class PasswordHasher {
  hash(password: string): string {
    return bcrypt.hash(password);
  }
}

class UserValidator {
  validateEmail(email: string): boolean {
    return email.includes('@');
  }

  validatePassword(password: string): boolean {
    return password.length >= 8;
  }
}

class UserRepository {
  save(user: User): void {
    db.insert('users', user);
  }

  find(id: string): User {
    return db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

class UserNotificationService {
  sendWelcomeEmail(email: string): void {
    emailService.send(email, 'Welcome!');
  }
}

class UserService {
  constructor(
    private validator: UserValidator,
    private hasher: PasswordHasher,
    private repository: UserRepository,
    private notificationService: UserNotificationService,
    private logger: Logger
  ) {}

  createUser(email: string, password: string) {
    this.validator.validateEmail(email);
    this.validator.validatePassword(password);

    const hash = this.hasher.hash(password);
    const user = new User(email, hash);

    this.repository.save(user);
    this.notificationService.sendWelcomeEmail(email);
    this.logger.info('User created', { email });

    return user;
  }
}

// Now:
// - Password changes → edit PasswordHasher
// - Validation changes → edit UserValidator
// - Database changes → edit UserRepository
// - Email changes → edit UserNotificationService
// - Each change isolated to one class!
```

### Solution 2: Move Methods to Specialized Classes

```typescript
// ❌ BEFORE: Scattered payment logic
class OrderService {
  calculateTax(order: Order): number {
    // Tax calculation
  }

  applyDiscount(order: Order, percent: number): number {
    // Discount calculation
  }

  processPayment(order: Order, amount: number): void {
    // Payment processing
  }

  recordPayment(order: Order): void {
    // Logging
  }

  sendConfirmation(order: Order): void {
    // Email sending
  }
}

// ✅ AFTER: Extract to specialized classes
class TaxCalculator {
  calculate(order: Order): number {
    // Tax calculation only
  }
}

class DiscountCalculator {
  apply(order: Order, percent: number): number {
    // Discount calculation only
  }
}

class PaymentProcessor {
  process(order: Order, amount: number): void {
    // Payment processing only
  }
}

class OrderLogger {
  record(order: Order): void {
    // Logging only
  }
}

class OrderNotificationService {
  sendConfirmation(order: Order): void {
    // Email sending only
  }
}

class OrderService {
  constructor(
    private taxCalculator: TaxCalculator,
    private discountCalculator: DiscountCalculator,
    private paymentProcessor: PaymentProcessor,
    private logger: OrderLogger,
    private notificationService: OrderNotificationService
  ) {}

  createOrder(items: OrderItem[], discountPercent: number = 0) {
    const order = new Order(items);
    const tax = this.taxCalculator.calculate(order);
    const discount = this.discountCalculator.apply(order, discountPercent);
    // ...
  }
}
```

### Solution 3: Dependency Injection

```typescript
// ❌ BEFORE: Mixed concerns
class ReportGenerator {
  generate(format: string): string {
    const data = this.fetchData();        // Reason: Data access
    const formatted = this.format(data);  // Reason: Formatting
    this.save(formatted);                 // Reason: Persistence
    this.email(formatted);                // Reason: Communication
    return formatted;
  }

  private fetchData() { }
  private format(data: any) { }
  private save(formatted: string) { }
  private email(formatted: string) { }
}

// ✅ AFTER: Inject dependencies
class ReportGenerator {
  constructor(
    private dataSource: DataSource,
    private formatter: ReportFormatter,
    private persistence: ReportPersistence,
    private emailService: EmailService
  ) {}

  generate(format: string): string {
    const data = this.dataSource.fetch();
    const formatted = this.formatter.format(data, format);
    this.persistence.save(formatted);
    this.emailService.send(formatted);
    return formatted;
  }
}

// Now each dependency represents a reason to change
// Can be updated independently
```

---

## 🔍 Detecting Divergent Change

**Watch for patterns**:
- Multiple unrelated imports
- Multiple unrelated dependencies
- Methods grouped by concern (comments like "// Email", "// Database")
- Hard to describe class purpose
- Changes in one method break unrelated method

---

## 📚 Relationship to Core Principles

- **SOLID-S** - Single Responsibility Principle (core principle)
- **ETC (Easier To Change)** - Multiple reasons = harder to change
- **Orthogonality** - Concerns should be independent
- **Review Dimensions** - Modularity and separation of concerns

---

## ✅ Checklist: Avoid Divergent Change

When designing classes:

- [ ] Does this class have one reason to change?
- [ ] Could I describe its purpose in one sentence without "and"?
- [ ] Are there methods for different concerns?
- [ ] Would extracting reduce dependencies?
- [ ] Do different methods use different injected dependencies?

---

## ✨ Remember

**DON'T DO**: Create classes with multiple reasons to change.

**DO**: Extract each reason to change into its own class.

**Rule of thumb**: If a class changes for multiple reasons, it should be multiple classes.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-divergent-change.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Extract responsibilities. One reason to change per class.**
