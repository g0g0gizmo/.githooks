# Code Smell: Large Class

**Purpose**: Identify and avoid classes that do too much
**Audience**: You + AI (code review, refactoring)
**Category**: Bloaters (Code That's Too Much)
**Severity**: 🔴 HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Large Class** is a class that has grown to do too much, combining multiple unrelated responsibilities.

A class should focus on one concept. When a class exceeds ~200-300 lines or has 10+ methods, it usually violates Single Responsibility Principle.

### Why It Matters

Large classes are:
- ❌ Hard to understand (too many methods and properties)
- ❌ Hard to maintain (multiple reasons to change)
- ❌ Hard to test (must test everything together)
- ❌ Hard to reuse (all or nothing)
- ❌ More likely to have bugs (complex state)

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Large Class (God Object)
class Application {
  // User management (25 methods)
  createUser() { }
  deleteUser() { }
  updateUser() { }
  getUser() { }
  // ... 21 more user methods

  // Payment processing (20 methods)
  processPayment() { }
  refund() { }
  getBalance() { }
  // ... 17 more payment methods

  // Email sending (15 methods)
  sendEmail() { }
  sendBulkEmail() { }
  // ... 13 more email methods

  // Logging (10 methods)
  log() { }
  logError() { }
  // ... 8 more logging methods

  // Database operations (18 methods)
  query() { }
  insert() { }
  update() { }
  // ... 15 more DB methods

  // File system (12 methods)
  readFile() { }
  writeFile() { }
  // ... 10 more file methods

  // Configuration (10 methods)
  getConfig() { }
  setConfig() { }
  // ... 8 more config methods

  // Total: 110+ methods, 3000+ lines
  // Multiple responsibilities
  // Multiple reasons to change
}
```

**Symptoms**:
- [ ] Class > 300 lines
- [ ] Class > 10 methods
- [ ] Class > 10 properties
- [ ] Methods don't use all properties
- [ ] Multiple "sections" with comments (// User Management, // Payments)
- [ ] Multiple reasons the class would change
- [ ] Can't describe class in one sentence without "and"
- [ ] Hard to find specific functionality
- [ ] New team members confused about class purpose
- [ ] Tests require mocking many dependencies

---

## 💔 Why It's Bad

### Problem 1: Multiple Reasons to Change

```typescript
// ❌ Class with multiple responsibilities
class UserService {
  createUser() { }        // Change: User creation logic
  hashPassword() { }      // Change: Hashing algorithm
  sendEmail() { }         // Change: Email service
  validateEmail() { }     // Change: Validation rules
  queryDatabase() { }     // Change: Database schema
}

// This class must change if:
// 1. User creation requirements change
// 2. Password hashing algorithm changes
// 3. Email service changes
// 4. Validation rules change
// 5. Database schema changes

// 5 reasons to change = HIGH MAINTENANCE COST
```

### Problem 2: Hard to Maintain

```
Finding a specific method in a 30-method class: 5 minutes
Understanding what a method does: 3 minutes
Understanding how methods interact: 10 minutes
Making a safe change: 20+ minutes

vs.

Small focused class (5 methods):
Finding a method: 1 minute
Understanding: 2 minutes
Making a change: 5 minutes
```

### Problem 3: Hard to Test

```typescript
// ❌ Testing a large class requires mocking everything
describe('UserService', () => {
  it('should create user', () => {
    // Must mock
    const mockDB = jest.fn();        // Database
    const mockEmail = jest.fn();     // Email
    const mockValidation = jest.fn(); // Validation
    const mockAuth = jest.fn();      // Auth
    const mockLogging = jest.fn();   // Logging
    const mockCache = jest.fn();     // Cache
    const mockFilesystem = jest.fn(); // Filesystem
    // ...and more

    // Now test setup is longer than actual test
    // Takes 500ms to run (should be < 1ms)
    // Team stops running tests
    // Bugs slip through
  });
});
```

### Problem 4: Can't Reuse Parts

```typescript
// ❌ Can't extract functionality
class Application {
  validateEmail() { }
  validatePhone() { }
  validatePassword() { }
  // ... 100 more methods
}

// Later: Need validation in another project
// Can't! It's buried in Application class
// Must copy-paste code (DRY violation)
```

---

## ✅ Refactoring Solutions

### Solution 1: Extract Classes

```typescript
// ❌ BEFORE: Large class with mixed responsibilities
class UserService {
  createUser(email, password) { }
  validateEmail(email) { }
  validatePassword(password) { }
  hashPassword(password) { }
  sendWelcomeEmail(email) { }
  logEvent(event) { }
  queryDatabase(sql) { }
}

// ✅ AFTER: Separated concerns

class UserService {
  constructor(
    private validator: UserValidator,
    private hasher: PasswordHasher,
    private emailService: EmailService,
    private userRepository: UserRepository,
    private logger: Logger
  ) {}

  createUser(email: string, password: string) {
    this.validator.validateEmail(email);
    this.validator.validatePassword(password);
    const hash = this.hasher.hash(password);
    const user = this.userRepository.save({ email, passwordHash: hash });
    this.emailService.sendWelcome(email);
    this.logger.info('User created', { userId: user.id });
    return user;
  }
}

class UserValidator {
  validateEmail(email: string): boolean { /* ... */ }
  validatePassword(password: string): boolean { /* ... */ }
}

class PasswordHasher {
  hash(password: string): string { /* ... */ }
}

class EmailService {
  sendWelcome(email: string): void { /* ... */ }
}

class UserRepository {
  save(user: any): any { /* ... */ }
  find(id: string): any { /* ... */ }
}

class Logger {
  info(message: string, data: any): void { /* ... */ }
}

// Benefits:
// - Each class does one thing
// - Easy to test individually
// - Easy to reuse parts
// - Easy to understand
// - Easy to change
```

### Solution 2: Extract by Feature

```typescript
// ❌ BEFORE: Large class with multiple features
class BankAccount {
  // Deposit feature (8 methods)
  deposit() { }
  validateDeposit() { }
  // ...

  // Withdrawal feature (8 methods)
  withdraw() { }
  validateWithdraw() { }
  // ...

  // Transfer feature (8 methods)
  transfer() { }
  validateTransfer() { }
  // ...

  // Balance feature (4 methods)
  getBalance() { }
  // ...

  // Statement feature (4 methods)
  getStatement() { }
  // ...
}

// ✅ AFTER: Separate each feature

class BankAccount {
  constructor(
    private depositService: DepositService,
    private withdrawalService: WithdrawalService,
    private transferService: TransferService,
    private balanceService: BalanceService,
    private statementService: StatementService
  ) {}

  deposit(amount) { return this.depositService.execute(this.id, amount); }
  withdraw(amount) { return this.withdrawalService.execute(this.id, amount); }
  transfer(toAccount, amount) { return this.transferService.execute(this.id, toAccount, amount); }
  getBalance() { return this.balanceService.get(this.id); }
  getStatement() { return this.statementService.generate(this.id); }
}

class DepositService {
  execute(accountId, amount) { /* ... */ }
}

class WithdrawalService {
  execute(accountId, amount) { /* ... */ }
}

class TransferService {
  execute(fromId, toId, amount) { /* ... */ }
}

class BalanceService {
  get(accountId) { /* ... */ }
}

class StatementService {
  generate(accountId) { /* ... */ }
}
```

### Solution 3: Extract by Data

```typescript
// ❌ BEFORE: Large class managing multiple data types
class Document {
  // User data properties
  userId: string;
  userName: string;
  userEmail: string;

  // Document data properties
  title: string;
  content: string;
  createdAt: Date;

  // Sharing data properties
  sharedWith: string[];
  permissions: string[];

  // Metadata properties
  tags: string[];
  category: string;

  // Methods that use different subsets of properties
  getAuthor() { return { userId: this.userId, name: this.userName }; }
  getContent() { return { title: this.title, content: this.content }; }
  getSharing() { return { sharedWith: this.sharedWith, permissions: this.permissions }; }
  // ...
}

// ✅ AFTER: Extract data into separate classes

class User {
  constructor(public id: string, public name: string, public email: string) {}
}

class DocumentContent {
  constructor(public title: string, public content: string, public createdAt: Date) {}
}

class DocumentSharing {
  constructor(public sharedWith: string[], public permissions: string[]) {}
}

class Document {
  constructor(
    public author: User,
    public content: DocumentContent,
    public sharing: DocumentSharing,
    public tags: string[],
    public category: string
  ) {}

  getAuthor() { return this.author; }
  getContent() { return this.content; }
  getSharing() { return this.sharing; }
}

// Benefits:
// - Each class small and focused
// - Properties grouped logically
// - Easy to understand what belongs together
// - Easy to test
// - Easy to reuse
```

---

## 🔍 The 200-300 Line Rule

**Guideline**: Classes should typically be 200-300 lines.

| Size | Status | Action |
|------|--------|--------|
| < 200 lines | ✅ Good | Keep as is |
| 200-300 lines | ⚠️ Watch | Consider splitting if unclear purpose |
| 300-500 lines | 🚩 Problem | Definitely split |
| 500+ lines | 🔴 Critical | Extract immediately |

**Symptoms of "too much"**:
- [ ] Can't describe purpose in one sentence
- [ ] Has 10+ public methods
- [ ] Has 10+ properties
- [ ] Multiple "sections" with comments
- [ ] Methods use different properties
- [ ] Hard to test without many mocks

---

## 🧪 The "Name Test"

**Good class name**: `UserValidator`, `EmailService`, `PaymentProcessor`
- Clear, specific, one concept

**Bad class name**: `Application`, `Helper`, `Manager`, `Processor`, `Service`
- Vague, indicates mixed concerns

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Large classes violate SRP
- **SOLID Principles** - Extract classes to achieve SOLID
- **Orthogonality** - Large classes are tightly coupled
- **Refactoring Techniques** - Extract Class solves large classes
- **Review Dimensions** - Modularity and Maintainability suffer

---

## ✅ Checklist: Avoid Large Classes

When designing classes:

- [ ] Does this class have one clear responsibility?
- [ ] Can I describe it in one sentence without "and"?
- [ ] Is it < 200 lines?
- [ ] Does it have < 10 public methods?
- [ ] Does it have < 10 instance variables?
- [ ] Do all methods use all properties?
- [ ] Could any group of methods/properties be extracted?
- [ ] Would extraction make the code clearer?
- [ ] Can someone understand this class in 5 minutes?
- [ ] Would other projects want to reuse parts?

---

## ✨ Remember

**DON'T DO**: Create large classes that mix multiple concerns.

**DO**: Keep classes focused on one concept.

**Single Responsibility Principle**: A class should have one reason to change.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells/smells-like-large-class.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Keep classes small. Extract when needed.**
