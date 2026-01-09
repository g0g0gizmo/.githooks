# Code Smell: Shotgun Surgery

**Purpose**: Identify and avoid changes requiring edits in many places
**Audience**: You + AI (code review, refactoring)
**Category**: Change Preventers (Hard to Modify)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Shotgun Surgery** occurs when a single change requires modifications in many unrelated places.

Every change should be localized to one or a few classes. When change ripples across 5+ classes, it indicates tight coupling or scattered responsibility.

### Why It Matters

Shotgun surgery causes:
- ❌ Fragile code (change breaks many things)
- ❌ Easy to miss locations (introduces bugs)
- ❌ Hard to understand relationships
- ❌ Tight coupling between classes
- ❌ Difficult and risky refactoring

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Change requires editing many classes
// Requirement: Add "middle name" field to users

// Must change:
class User {
  firstName: string;
  middleName: string;  // ← Added
  lastName: string;
}

class UserRepository {
  save(user: User) {
    db.insert('users', {
      firstName: user.firstName,
      middleName: user.middleName,  // ← Added
      lastName: user.lastName,
    });
  }

  getUser(id: string): User {
    const row = db.query('SELECT * FROM users WHERE id = ?', [id]);
    return new User(
      row.firstName,
      row.middleName,  // ← Added
      row.lastName
    );
  }
}

class UserService {
  createUser(firstName: string, middleName: string, lastName: string) {  // ← Added param
    const user = new User(firstName, middleName, lastName);
    return this.userRepository.save(user);
  }

  validateUser(firstName: string, middleName: string, lastName: string): boolean {  // ← Added param
    return firstName.length > 0 && middleName.length > 0 && lastName.length > 0;
  }

  printUser(user: User): string {  // ← Modified
    return `${user.firstName} ${user.middleName} ${user.lastName}`;
  }
}

class UserController {
  handleRequest(req: Request) {
    const { firstName, middleName, lastName } = req.body;  // ← Added
    return this.userService.createUser(firstName, middleName, lastName);
  }
}

class UserAPI {
  @Post('/users')
  createUser(
    @Body('firstName') firstName: string,
    @Body('middleName') middleName: string,  // ← Added
    @Body('lastName') lastName: string
  ) {
    return this.userService.createUser(firstName, middleName, lastName);
  }
}

// Changed 5 classes!
// Easy to miss one → Bug
// Risky change for simple requirement
```

**Symptoms**:
- [ ] Single change requires editing 5+ classes
- [ ] Changes to one class force changes to others
- [ ] Method signatures change frequently
- [ ] Adding field requires updating many places
- [ ] Related logic scattered across classes
- [ ] Classes seem coupled but don't know why

---

## 💔 Why It's Bad

### Problem 1: Cascading Changes

```typescript
// ❌ Change Payment → must change 6+ classes
class Payment {
  amount: number;
  // Add: method: string
}

// Now must update:
class PaymentRepository {  // ✓ Must save method
  save(payment: Payment) { }
}

class PaymentValidator {  // ✓ Must validate method
  validate(payment: Payment): boolean { }
}

class PaymentProcessor {  // ✓ Must process with method
  process(payment: Payment) { }
}

class PaymentService {  // ✓ Must pass method to processor
  createPayment(amount, method) { }
}

class PaymentController {  // ✓ Must accept method from request
  @Post('/payments')
  create(@Body() body) { }
}

class BillingReporter {  // ✓ Must include method in reports
  generateReport(payments: Payment[]) { }
}

class AuditLog {  // ✓ Must log method for compliance
  logPayment(payment: Payment) { }
}

// 8 classes changed!
```

### Problem 2: Easy to Miss Updates

```typescript
// ❌ Missed one update
class Order {
  items: OrderItem[];
  // Add: discount: number
}

// Updated OrderService:
class OrderService {
  createOrder(items, discount) {  // ✓ Added param
    return new Order(items, discount);
  }
}

// Forgot to update OrderRepository:
class OrderRepository {
  save(order: Order) {
    db.insert('orders', {
      items: order.items,
      // ✗ Forgot discount!
    });
  }
}

// Silently ignores discount → Bug in production
```

### Problem 3: Risky Refactoring

```typescript
// ❌ Need to refactor, but changes cascade
// Refactor: Extract email validation to separate class

// Changes needed:
class User {
  email: string;
  // Must use new Email class
}

class UserService {
  validateUser(user) {
    // Must call new Email validation
  }
}

class UserRepository {
  save(user) {
    // Must handle new Email type
  }

class UserController {
  create(req) {
    // Must create Email object
  }
}

class UserAPI {
  @Post('/users')
  create(@Body() body) {
    // Must parse Email from request
  }
}

// 5+ changes for simple extraction!
// Risk not worth benefit
```

---

## ✅ Refactoring Solutions

### Solution 1: Move Method and Field

```typescript
// ❌ BEFORE: Related logic scattered
class Order {
  items: OrderItem[];

  calculateTotal(): number {  // Calculation logic
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }
}

class OrderService {
  applyDiscount(order: Order, percent: number): number {  // Discount logic
    const total = order.calculateTotal();
    return total * (1 - percent / 100);
  }

  applyTax(order: Order): number {  // Tax logic
    const total = order.calculateTotal();
    return total * 1.08;
  }

  getTotal(order: Order): number {  // Gets total
    return order.calculateTotal();
  }
}

// If Order structure changes, must update:
// - Order.calculateTotal()
// - OrderService.applyDiscount()
// - OrderService.applyTax()
// - OrderService.getTotal()

// ✅ AFTER: Keep related logic together
class Order {
  items: OrderItem[];

  calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  applyDiscount(percent: number): number {
    return this.calculateTotal() * (1 - percent / 100);
  }

  applyTax(): number {
    return this.calculateTotal() * 1.08;
  }

  getFinal(discount: number = 0): number {
    return this.applyTax() - (this.calculateTotal() * discount / 100);
  }
}

// Now Order changes only affect Order class
```

### Solution 2: Extract Class for Related Logic

```typescript
// ❌ BEFORE: Email logic scattered
class User {
  email: string;

  setEmail(email: string) {
    if (!email.includes('@')) throw new Error('Invalid');
    this.email = email;
  }

  sendEmail(message: string) {
    // Email sending logic
    smtp.send(this.email, message);
  }

  getEmailDomain(): string {
    return this.email.split('@')[1];
  }
}

class UserService {
  validateEmail(user: User, email: string): boolean {
    if (!email.includes('@')) return false;
    if (email.includes(' ')) return false;
    return true;
  }

  sendWelcomeEmail(user: User) {
    const template = this.getEmailTemplate('welcome', user.getEmailDomain());
    user.sendEmail(template);
  }
}

// Email logic in User and UserService
// Change to email format → update both

// ✅ AFTER: Extract Email class
class Email {
  constructor(readonly value: string) {
    if (!value.includes('@')) throw new Error('Invalid');
    if (value.includes(' ')) throw new Error('Invalid');
  }

  getDomain(): string {
    return this.value.split('@')[1];
  }

  send(message: string): void {
    smtp.send(this.value, message);
  }
}

class User {
  email: Email;
}

class UserService {
  sendWelcomeEmail(user: User) {
    const template = this.getEmailTemplate('welcome', user.email.getDomain());
    user.email.send(template);
  }
}

// Now email changes only affect Email class
```

### Solution 3: Inline Class (Reverse Extraction)

```typescript
// ❌ BEFORE: Scattered Payment logic
class PaymentProcessor {
  process(payment: Payment) {
    // Uses PaymentValidation
    const validator = new PaymentValidation();
    if (!validator.isValid(payment)) return;
    // Uses PaymentLogger
    const logger = new PaymentLogger();
    logger.log(payment);
    // Uses PaymentRecorder
    const recorder = new PaymentRecorder();
    recorder.record(payment);
  }
}

// Change Payment → must update:
// - PaymentValidation
// - PaymentLogger
// - PaymentRecorder
// - PaymentProcessor

// ✅ AFTER: Consolidate
class PaymentProcessor {
  process(payment: Payment) {
    if (!this.isValid(payment)) return;
    this.log(payment);
    this.record(payment);
  }

  private isValid(payment: Payment): boolean {
    return payment.amount > 0;
  }

  private log(payment: Payment): void {
    console.log(payment);
  }

  private record(payment: Payment): void {
    db.insert('payments', payment);
  }
}

// Now all payment logic in one place
```

### Solution 4: Encapsulation

```typescript
// ❌ BEFORE: External modification of internal structure
class Customer {
  orders: Order[] = [];
  totalSpent: number = 0;
}

class OrderService {
  addOrder(customer: Customer, order: Order) {
    customer.orders.push(order);                           // Modifying internal array
    customer.totalSpent += order.getTotal();              // Modifying internal state
  }

  removeOrder(customer: Customer, order: Order) {
    const index = customer.orders.indexOf(order);
    if (index > -1) customer.orders.splice(index, 1);     // Modifying internal array
    customer.totalSpent -= order.getTotal();              // Modifying internal state
  }
}

// Change Customer internal structure → must update OrderService

// ✅ AFTER: Encapsulate changes
class Customer {
  private orders: Order[] = [];
  private totalSpent: number = 0;

  addOrder(order: Order) {
    this.orders.push(order);
    this.totalSpent += order.getTotal();
  }

  removeOrder(order: Order) {
    const index = this.orders.indexOf(order);
    if (index > -1) {
      this.orders.splice(index, 1);
      this.totalSpent -= order.getTotal();
    }
  }

  getTotalSpent(): number {
    return this.totalSpent;
  }
}

class OrderService {
  addOrder(customer: Customer, order: Order) {
    customer.addOrder(order);  // Use encapsulated method
  }

  removeOrder(customer: Customer, order: Order) {
    customer.removeOrder(order);  // Use encapsulated method
  }
}

// Now internal changes only affect Customer class
```

---

## 🔍 Shotgun Surgery Severity

| Changes Needed | Severity | Action |
|---|---|---|
| 1-2 places | ✅ Acceptable | OK to change |
| 3-4 places | ⚠️ Watch | Consider consolidation |
| 5+ places | 🚩 Problem | Definitely refactor |
| 10+ places | 🔴 Critical | Major design issue |

---

## 📚 Relationship to Core Principles

- **ETC (Easier To Change)** - Changes should be localized
- **DRY Principle** - Related logic scattered indicates duplication
- **Orthogonality** - Coupled changes indicate poor orthogonality
- **SOLID-S** - Classes should have single reason to change

---

## ✅ Checklist: Avoid Shotgun Surgery

When making changes:

- [ ] How many classes must I edit?
- [ ] Is there a pattern to the changes?
- [ ] Could I consolidate related logic?
- [ ] Are changes scattered across unrelated classes?
- [ ] Would extraction make changes localized?

---

## ✨ Remember

**DON'T DO**: Make changes that ripple across many classes.

**DO**: Keep related logic together; localize changes.

**Rule of thumb**: If a change requires editing 5+ classes, refactor to consolidate.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-shotgun-surgery.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Consolidate related logic. Localize changes.**
