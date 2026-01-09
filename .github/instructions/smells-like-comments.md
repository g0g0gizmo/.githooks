# Code Smell: Comments

**Purpose**: Identify and avoid excessive or misleading comments
**Audience**: You + AI (code review, refactoring)
**Category**: Dispensables (Unnecessary Code)
**Severity**: 🟢 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Comments** is a smell when excessive comments indicate unclear code that should be refactored.

Comments should explain "why", not "what". If you need comments to understand "what" the code does, the code should be refactored to be self-documenting.

### Why It Matters

Excessive comments cause:
- ❌ Indicate code is unclear
- ❌ Comments drift out of sync with code
- ❌ Maintenance burden (update code AND comments)
- ❌ Hide poor naming or logic
- ❌ False confidence (comments might be wrong)

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Comments explaining what code does
class User {
  // The user's first name
  firstName: string;

  // The user's email address
  email: string;

  // Gets the full name by combining firstName and lastName
  getFullName(): string {
    // Split the first and last names
    const names = this.fullName.split(' ');
    // Return the first element (first name)
    return names[0];
  }

  // Validate the email address
  validateEmail(): boolean {
    // Check if email includes @ symbol
    if (!this.email.includes('@')) {
      // Return false if @ not found
      return false;
    }

    // Check if email has a domain
    const parts = this.email.split('@');
    // Return true if both parts exist
    return parts.length === 2;
  }
}

// Every line has a comment explaining what it does
// Comments are noise
// Code should be self-explanatory
```

**Symptoms**:
- [ ] Comments explain what code does (not why)
- [ ] Comments repeat what code already says
- [ ] Comments for every method or property
- [ ] Comments more lines than code
- [ ] Comments are outdated/incorrect
- [ ] Comments explain obvious code
- [ ] Need comments to understand method names

---

## 💔 Why It's Bad

### Problem 1: Comments Drift from Reality

```typescript
// ❌ Comments don't match code
class PaymentProcessor {
  // Processes payment and sends confirmation
  processPayment(amount: number) {
    this.charge(amount);
    // Comment says "sends confirmation" but this doesn't!
    // Only charges, doesn't send email
  }

  // Only dev can see this drift
  // Users expect confirmation email
  // Silent bug
}
```

### Problem 2: False Confidence

```typescript
// ❌ Comment might be wrong
function calculateDiscount(amount: number, percent: number): number {
  // Returns 10% discount
  // But actually returns 20% discount!
  return amount * 0.2;
}

// Someone reads the comment
// Trusts it's correct
// Uses wrong calculation
```

### Problem 3: Maintenance Burden

```typescript
// ❌ Must update code AND comment
function getUsersByAge(age: number): User[] {
  // Return users older than age
  return this.users.filter(u => u.age > age);
}

// Requirement change: Return users AGE OR OLDER
function getUsersByAge(age: number): User[] {
  // Return users older than age  ← FORGOT TO UPDATE COMMENT!
  return this.users.filter(u => u.age >= age);
}

// Comment now incorrect
```

### Problem 4: Hiding Bad Code

```typescript
// ❌ Comments enable bad code to stay
function x(a, b, c) {
  // First parameter is user ID
  // Second parameter is order amount
  // Third parameter is discount percent
  // Returns discounted price
  return (a * b) * (1 - c / 100);
}

// If code was clear, wouldn't need these comments!

// ✅ Better: Self-documenting
function calculateDiscountedPrice(
  userId: string,
  orderAmount: number,
  discountPercent: number
): number {
  return orderAmount * (1 - discountPercent / 100);
}

// No comments needed!
```

---

## ✅ Refactoring Solutions

### Solution 1: Rename Method/Variable

```typescript
// ❌ BEFORE: Unclear name, needs comment
class PaymentService {
  // Process payment and update inventory
  executeTransaction(payment: any) {
    // ...
  }
}

// ✅ AFTER: Clear name, no comment needed
class PaymentService {
  processPaymentAndUpdateInventory(payment: Payment) {
    // No comment needed!
  }
}
```

### Solution 2: Extract Method

```typescript
// ❌ BEFORE: Complex logic with comments
function getUserEmail(userId: string): string {
  // Get user from database
  const user = db.query('SELECT * FROM users WHERE id = ?', [userId]);

  // Check if user exists
  if (!user) return '';

  // Return user's email if not marked as private
  if (user.emailIsPrivate) return '';

  // Format email for safe display
  return user.email.toLowerCase();
}

// ✅ AFTER: Extract methods with clear names
function getUserEmail(userId: string): string {
  const user = this.findUser(userId);
  if (!user) return '';

  if (user.emailIsPrivate) return '';

  return this.formatEmail(user.email);
}

private formatEmail(email: string): string {
  return email.toLowerCase();
}

// No comments needed - methods are self-explanatory
```

### Solution 3: Better Variable Names

```typescript
// ❌ BEFORE: Bad names, needs comments
function processOrder(order) {
  // Calculate tax (8% in most states)
  const t = order.amount * 0.08;

  // Get shipping cost from ZIP code
  const s = this.getShippingByZip(order.zip);

  // Total is amount + tax + shipping
  const total = order.amount + t + s;

  return total;
}

// ✅ AFTER: Clear names, no comments
function processOrder(order) {
  const tax = order.amount * TAX_RATE;
  const shipping = this.getShippingByZip(order.zip);
  const total = order.amount + tax + shipping;
  return total;
}

// Clear what each variable is!
```

### Solution 4: Introduce Constant

```typescript
// ❌ BEFORE: Magic number, needs comment
function calculateSalary(baseSalary: number): number {
  // We give 5% bonus for seniority
  return baseSalary * 1.05;
}

// ✅ AFTER: Named constant explains the why
const SENIORITY_BONUS_MULTIPLIER = 1.05;

function calculateSalary(baseSalary: number): number {
  return baseSalary * SENIORITY_BONUS_MULTIPLIER;
}

// Magic number is now named
```

### Solution 5: Replace Comment with Assertion

```typescript
// ❌ BEFORE: Comment explaining assumption
function calculateDiscount(user: User, amount: number): number {
  // User must be premium to get discount
  if (!user.isPremium) return amount;

  return amount * 0.9;
}

// What if user is not premium?
// Comment doesn't enforce it

// ✅ AFTER: Assertion makes assumption clear
function calculateDiscount(user: User, amount: number): number {
  if (!user.isPremium) {
    throw new Error('User must be premium to get discount');
  }

  return amount * 0.9;
}

// Now requirement is enforced!
```

---

## 🔍 When Comments ARE Appropriate

**Good comments explain "why"**:

```typescript
// ✅ Explains business rule
const MAXIMUM_RETRY_ATTEMPTS = 3;  // Retry limit per SLA agreement with customer

// ✅ Explains non-obvious algorithm choice
function findNearestMatch(items: Item[]): Item {
  // Use binary search for O(log n) performance
  // Linear search would be O(n) and too slow for 1M+ items
  return binarySearch(items);
}

// ✅ Explains hack/workaround
function handleBrowserBug(): void {
  // Chromium bug #12345: Setting opacity causes flicker
  // Workaround: use visibility instead (hidden/visible instead of opacity 0)
  element.style.visibility = 'hidden';
}

// ✅ Explains warning
function clearDatabase(): void {
  // WARNING: This operation cannot be undone!
  // Always run in test environment first
  db.clear();
}

// ✅ Explains complex math/algorithm
function calculateLeapYear(year: number): boolean {
  // Leap year if:
  // - Divisible by 400, OR
  // - Divisible by 4 AND not divisible by 100
  return (year % 400 === 0) || (year % 4 === 0 && year % 100 !== 0);
}
```

**Bad comments repeat code**:

```typescript
// ❌ Bad: Comments repeat what code says
const age = user.dateOfBirth.getFullYear() - new Date().getFullYear();  // Calculate age

function findUser(id: string): User {  // Find user by id
  return this.users.find(u => u.id === id);
}

// Remove these! Code is already clear
```

---

## 📚 Relationship to Core Principles

- **Clarity** - Self-documenting code is clearer than comments
- **DRY Principle** - Comments + code = duplication
- **Refactoring** - Replace comments with better code structure

---

## ✅ Checklist: Avoid Comment Smell

When writing code:

- [ ] Are these comments explaining "why" or "what"?
- [ ] Could the code be clearer instead?
- [ ] Could I rename methods/variables to avoid this comment?
- [ ] Could I extract this into a well-named function?
- [ ] Are these comments necessary or just noise?

---

## ✨ Remember

**DON'T DO**: Use comments to explain unclear code.

**DO**: Write clear, self-documenting code instead.

**Rule of thumb**: If you need a comment to explain "what", refactor to make it obvious. Use comments for "why".

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-comments.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Write clear code. Let comments explain why, not what.**
