# Code Smell: Long Method

**Purpose**: Identify and avoid functions that do too much
**Audience**: You + AI (code review, refactoring)
**Category**: Bloaters (Code That's Too Much)
**Severity**: 🔴 HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Long Method** is a function or method that does too much and is too long to understand at a glance.

A method should be focused and concise. When a method exceeds a reasonable length (typically 20-50 lines), it usually does multiple things and should be broken down.

### Why It Matters

Long methods are:
- ❌ Hard to understand (take too long to read)
- ❌ Hard to test (must test entire function)
- ❌ Hard to reuse (functionality mixed together)
- ❌ Hard to modify (changes affect many parts)
- ❌ More likely to contain bugs (complex logic)

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Long Method (50+ lines)
function processUserRegistration(userData) {
  // Validate email
  if (!userData.email) throw new Error('Email required');
  const emailParts = userData.email.split('@');
  if (emailParts.length !== 2) throw new Error('Invalid email');
  if (emailParts[1].split('.').length < 2) throw new Error('Invalid domain');

  // Validate password
  if (!userData.password) throw new Error('Password required');
  if (userData.password.length < 8) throw new Error('Password too short');
  if (!/[A-Z]/.test(userData.password)) throw new Error('Need uppercase');
  if (!/[0-9]/.test(userData.password)) throw new Error('Need number');

  // Hash password
  const salt = bcrypt.genSaltSync(10);
  const hashedPassword = bcrypt.hashSync(userData.password, salt);

  // Check if user exists
  const existingUser = db.query('SELECT * FROM users WHERE email = ?', [userData.email]);
  if (existingUser) throw new Error('User already exists');

  // Create user
  const user = {
    email: userData.email,
    passwordHash: hashedPassword,
    createdAt: new Date(),
    verified: false,
  };
  const result = db.insert('users', user);

  // Send verification email
  const token = crypto.randomBytes(32).toString('hex');
  db.insert('verification_tokens', {
    userId: result.id,
    token: token,
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
  });

  const emailBody = `
    <h1>Verify Your Email</h1>
    <p>Click here to verify: <a href="http://example.com/verify?token=${token}">Verify</a></p>
  `;
  emailService.send(userData.email, 'Verify Email', emailBody);

  // Log event
  logger.info('User registered', { userId: result.id, email: userData.email });

  return { userId: result.id, email: userData.email };
}

// 60+ lines! Does: validation, hashing, database, email, logging
// Too many responsibilities
```

**Symptoms**:
- [ ] Function > 50 lines
- [ ] Function has 5+ indentation levels
- [ ] Multiple "sections" with comments (// Validate, // Hash, // Email)
- [ ] Multiple reasons the function would need to change
- [ ] Hard to understand what the function does
- [ ] Can't reuse parts of the function elsewhere
- [ ] Hard to test without mocking everything
- [ ] Lots of local variables
- [ ] Deep nesting (if/for/while inside each other)

---

## 💔 Why It's Bad

### Problem 1: Hard to Understand

```
Time to understand a 20-line function: 2 minutes
Time to understand a 50-line function: 15 minutes
Time to understand a 100-line function: 1 hour
Time to understand a 200-line function: ??? (usually give up)
```

### Problem 2: Hard to Test

```typescript
// ❌ Hard to test long method
function complexProcess() {
  // 50 lines of logic
  // Must mock database, email, external API, file system
  // Must set up 100 test fixtures
  // Takes 10 seconds per test (should be < 100ms)
}

// Test suite takes hours to run
// Developers stop running tests
// Bugs slip through
```

### Problem 3: Hard to Reuse

```typescript
// ❌ Can't reuse parts
function registerUser(userData) {
  // Email validation (20 lines)
  // Password hashing (10 lines)
  // Database insertion (5 lines)
  // Email sending (10 lines)
  // Logging (3 lines)
  // 48 lines total, all mixed together

  return userId;
}

// Later: Need to hash password elsewhere?
// Can't! It's inside registerUser

// Need to validate email elsewhere?
// Can't! It's inside registerUser
```

### Problem 4: Higher Bug Rate

Longer methods have exponentially more bugs:
- 20-line method: ~0.5 bugs typically
- 50-line method: ~2 bugs typically
- 100-line method: ~5+ bugs typically

More code = more logic paths = more bugs

---

## ✅ Refactoring Solutions

### Solution 1: Extract Method

```typescript
// ✅ FIXED: Break into focused methods

function validateEmail(email: string): void {
  if (!email) throw new Error('Email required');
  const emailParts = email.split('@');
  if (emailParts.length !== 2) throw new Error('Invalid email');
  if (emailParts[1].split('.').length < 2) throw new Error('Invalid domain');
}

function validatePassword(password: string): void {
  if (!password) throw new Error('Password required');
  if (password.length < 8) throw new Error('Password too short');
  if (!/[A-Z]/.test(password)) throw new Error('Need uppercase');
  if (!/[0-9]/.test(password)) throw new Error('Need number');
}

function createUser(email: string, passwordHash: string) {
  const existingUser = db.query('SELECT * FROM users WHERE email = ?', [email]);
  if (existingUser) throw new Error('User already exists');

  return db.insert('users', {
    email,
    passwordHash,
    createdAt: new Date(),
    verified: false,
  });
}

function sendVerificationEmail(userId: string, email: string): void {
  const token = crypto.randomBytes(32).toString('hex');
  db.insert('verification_tokens', {
    userId,
    token,
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
  });

  const emailBody = `
    <h1>Verify Your Email</h1>
    <p><a href="http://example.com/verify?token=${token}">Verify</a></p>
  `;
  emailService.send(email, 'Verify Email', emailBody);
}

// Main function now clear and focused
async function registerUser(userData) {
  validateEmail(userData.email);
  validatePassword(userData.password);

  const hashedPassword = await passwordService.hash(userData.password);
  const user = createUser(userData.email, hashedPassword);

  await sendVerificationEmail(user.id, userData.email);
  logger.info('User registered', { userId: user.id, email: userData.email });

  return { userId: user.id, email: userData.email };
}

// Benefits:
// - Each function <20 lines
// - Clear what each does
// - Easy to test individually
// - Easy to reuse parts
// - Easy to understand
```

### Solution 2: Replace Temp with Query

```typescript
// ❌ Long method with temp variables
function calculateTotal(order) {
  let subtotal = 0;
  for (let item of order.items) {
    subtotal += item.price * item.quantity;
  }

  let discount = 0;
  if (order.customer.isPremium) {
    discount = subtotal * 0.2;
  }

  let tax = 0;
  if (order.location === 'US') {
    tax = (subtotal - discount) * 0.08;
  }

  let total = subtotal - discount + tax;
  return total;
}

// ✅ Fixed: Extract calculations into methods
function calculateSubtotal(order) {
  return order.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
}

function calculateDiscount(order, subtotal) {
  return order.customer.isPremium ? subtotal * 0.2 : 0;
}

function calculateTax(order, taxableAmount) {
  if (order.location !== 'US') return 0;
  return taxableAmount * 0.08;
}

function calculateTotal(order) {
  const subtotal = calculateSubtotal(order);
  const discount = calculateDiscount(order, subtotal);
  const tax = calculateTax(order, subtotal - discount);
  return subtotal - discount + tax;
}
```

### Solution 3: Introduce Parameter Object

```typescript
// ❌ Long method with many parameters
function createInvoice(
  customerId, customerName, customerEmail,
  productId, productName, quantity, price,
  taxRate, shippingCost, discountPercent
) {
  // 50 lines using all these parameters
}

// ✅ Fixed: Group into objects
class Customer {
  constructor(public id: string, public name: string, public email: string) {}
}

class LineItem {
  constructor(
    public productId: string,
    public name: string,
    public quantity: number,
    public price: number
  ) {}
}

class InvoiceConfig {
  constructor(
    public taxRate: number,
    public shippingCost: number,
    public discountPercent: number
  ) {}
}

function createInvoice(customer: Customer, lineItems: LineItem[], config: InvoiceConfig) {
  // Much cleaner parameter list
  // Easier to understand
  // Easier to test
}
```

### Solution 4: Conditional Expression to Polymorphism

```typescript
// ❌ Long method with many conditionals
function getDeliveryTime(order) {
  let days = 3;

  if (order.shippingMethod === 'standard') {
    days = 5;
  } else if (order.shippingMethod === 'express') {
    days = 2;
  } else if (order.shippingMethod === 'overnight') {
    days = 1;
  }

  if (order.destination === 'international') {
    days += 3;
  }

  if (order.weight > 50) {
    days += 1;
  }

  // Many more conditions...

  return days;
}

// ✅ Fixed: Use polymorphism
interface ShippingStrategy {
  getDeliveryDays(order: Order): number;
}

class StandardShipping implements ShippingStrategy {
  getDeliveryDays(order: Order) {
    return 5;
  }
}

class ExpressShipping implements ShippingStrategy {
  getDeliveryDays(order: Order) {
    return 2;
  }
}

class OvernightShipping implements ShippingStrategy {
  getDeliveryDays(order: Order) {
    return 1;
  }
}

function getDeliveryTime(order: Order, shipping: ShippingStrategy) {
  let days = shipping.getDeliveryDays(order);
  if (order.destination === 'international') days += 3;
  if (order.weight > 50) days += 1;
  return days;
}
```

---

## 🔍 The 20-50 Line Rule

**Guideline**: Functions should typically be 20-50 lines.

| Length | Status | Action |
|--------|--------|--------|
| < 20 lines | ✅ Good | Keep as is |
| 20-50 lines | ⚠️ Watch | Consider breaking down if complex |
| 50-100 lines | 🚩 Problem | Definitely break down |
| 100+ lines | 🔴 Critical | Extract immediately |

**Note**: This is a guideline, not a hard rule. A 100-line method of simple assignments is better than a 10-line method with complex logic.

Focus on **readability and maintainability**, not arbitrary line counts.

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Long methods often do multiple things
- **ETC Principle** - Long methods are harder to change
- **Refactoring Techniques** - Extract Function solves long methods
- **Review Dimensions** - Maintainability suffers with long methods
- **Small Steps** - Break long methods into small steps

---

## ✅ Checklist: Avoid Long Methods

When writing methods:

- [ ] Is this method < 50 lines?
- [ ] Does it do one clear thing?
- [ ] Can I describe it in one sentence without "and"?
- [ ] Can someone understand it in < 5 minutes?
- [ ] Can I test it without mocking many things?
- [ ] Are there sections marked with comments? (Usually indicates multiple things)
- [ ] Could any part be extracted to a named method?
- [ ] Would extracting make the code clearer?
- [ ] Are there deeply nested conditions?

---

## ✨ Remember

**DON'T DO**: Write long methods that do multiple things.

**DO**: Break methods into small, focused, reusable pieces.

**Rule of thumb**: If you need a comment explaining what a section does, extract it to a named method.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells/smells-like-long-method.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Keep methods short. Extract when needed.**
