# Code Smell: Data Clumps

**Purpose**: Identify and avoid groups of fields that always appear together
**Audience**: You + AI (code review, refactoring)
**Category**: Bloaters (Code That's Too Much)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Data Clumps** occur when the same group of variables appear together in multiple places.

These related fields should be grouped into a single object. When you see the same 3+ fields appearing together repeatedly, they form a "clump" that belongs in its own class.

### Why It Matters

Data clumps cause:
- ❌ Scattered related data across codebase
- ❌ Inconsistent access patterns
- ❌ Hard to maintain all occurrences together
- ❌ Easy to miss one occurrence when making changes
- ❌ Parameters lists grow unnecessarily long

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Same three fields everywhere
class UserService {
  createUser(firstName: string, lastName: string, email: string) {
    // firstName, lastName, email together
  }

  updateUser(id: string, firstName: string, lastName: string, email: string) {
    // Same three fields
  }

  validateUser(firstName: string, lastName: string, email: string): boolean {
    // Same three fields again!
  }
}

class UserRepository {
  save(firstName: string, lastName: string, email: string) {
    // Still the same three fields!
    db.insert('users', { firstName, lastName, email });
  }
}

class UserController {
  handleRequest(firstName: string, lastName: string, email: string) {
    // And again...
  }
}

// firstName, lastName, email appear together:
// - UserService.createUser
// - UserService.updateUser
// - UserService.validateUser
// - UserRepository.save
// - UserController.handleRequest
// = 5 locations! This is a DATA CLUMP
```

**Symptoms**:
- [ ] Same 3+ fields appear in multiple functions/classes
- [ ] You often pass the same parameters together
- [ ] Function signatures look similar across different classes
- [ ] Method parameters are always used together
- [ ] Creating a new use case requires copying the same fields
- [ ] Changes to one field must be replicated in multiple places
- [ ] Fields represent a concept (e.g., "name" fields = a person's identity)

---

## 💔 Why It's Bad

### Problem 1: Changes Ripple Everywhere

```typescript
// ❌ Before: Requirement = Add "middleName" to user
class UserService {
  createUser(firstName, lastName, email) { /* ... */ }
}

class UserRepository {
  save(firstName, lastName, email) { /* ... */ }
}

class UserController {
  handleRequest(firstName, lastName, email) { /* ... */ }
}

// Now must update:
// - UserService.createUser() signature
// - UserRepository.save() signature
// - UserController.handleRequest() signature
// - All callers of these functions
// - Tests for all these functions

// If you miss one location, bug created!
```

### Problem 2: Inconsistency

```typescript
// ❌ Different handling of same data clump
function validateUserName(firstName: string, lastName: string) {
  return firstName.length > 0 && lastName.length > 0;
}

function validateUserForDatabase(firstName: string, lastName: string) {
  if (!firstName || !lastName) return false;  // Different validation!
  if (firstName.length > 100) return false;   // Has length check
  return true;
}

// Same fields, different validation rules!
// Which one is correct?
// When to use which?
```

### Problem 3: Long Parameter Lists

```typescript
// ❌ Parameters grow with clumps
function processUser(
  firstName, lastName, email,  // Clump 1
  street, city, state, zip,     // Clump 2
  phone, countryCode,           // Clump 3
  birthDate, ssn                // Clump 4
) {
  // 12 parameters! Hard to remember order
  // Hard to test
  // Easy to pass wrong values
}
```

### Problem 4: Hard to Understand Intent

```typescript
// ❌ Unclear why these parameters are together
function calculateShipping(
  firstName: string,
  lastName: string,
  email: string,
  shippingStreet: string,
  shippingCity: string,
  shippingState: string,
  shippingZip: string
) {
  // Why does calculateShipping care about firstName, lastName, email?
  // These are about the person, but shipping needs address
  // Unclear intent
}

// ✅ Clear intent with grouped data
class Person {
  firstName: string;
  lastName: string;
  email: string;
}

class ShippingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
}

function calculateShipping(address: ShippingAddress) {
  // Clear: only needs address
}
```

---

## ✅ Refactoring Solutions

### Solution 1: Extract Class

```typescript
// ❌ BEFORE: Data clump scattered
function createUser(firstName: string, lastName: string, email: string) {
  db.insert('users', {
    firstName,
    lastName,
    email,
  });
}

function validateUser(firstName: string, lastName: string, email: string): boolean {
  return firstName.length > 0 && lastName.length > 0 && email.includes('@');
}

function printUser(firstName: string, lastName: string, email: string) {
  console.log(`${firstName} ${lastName} (${email})`);
}

// ✅ AFTER: Extract class
class User {
  constructor(
    public firstName: string,
    public lastName: string,
    public email: string
  ) {}

  validate(): boolean {
    return this.firstName.length > 0 && this.lastName.length > 0 && this.email.includes('@');
  }

  toString(): string {
    return `${this.firstName} ${this.lastName} (${this.email})`;
  }
}

function createUser(user: User) {
  db.insert('users', user);
}

// Now the clump is in one place
```

### Solution 2: Introduce Parameter Object

```typescript
// ❌ BEFORE: Multiple address fields
function calculateDistance(
  startStreet: string,
  startCity: string,
  startState: string,
  endStreet: string,
  endCity: string,
  endState: string
): number {
  // 6 parameters for two addresses
}

// Called many places:
calculateDistance(
  userStreet, userCity, userState,
  shippingStreet, shippingCity, shippingState
);

// ✅ AFTER: Group into objects
class Address {
  constructor(
    public street: string,
    public city: string,
    public state: string
  ) {}
}

function calculateDistance(start: Address, end: Address): number {
  // Clear: two addresses
}

// Much clearer
calculateDistance(userAddress, shippingAddress);
```

### Solution 3: Preserve Whole Object

```typescript
// ❌ BEFORE: Passing individual fields
class Order {
  customer: Customer;
}

function validateOrder(
  customerId: string,
  customerName: string,
  customerEmail: string,
  amount: number
): boolean {
  // Clump: customer fields scattered
}

// ✅ AFTER: Pass entire object
function validateOrder(order: Order, amount: number): boolean {
  return order.customer.isValid() && amount > 0;
  // Use customer object methods
}
```

### Solution 4: Extract Method to Use the Clump

```typescript
// ❌ BEFORE: Clump used in multiple places
class ReportService {
  generateUserReport(firstName, lastName, email) {
    this.validateUser(firstName, lastName, email);
    this.formatOutput(firstName, lastName, email);
    this.sendEmail(email);
  }

  private validateUser(firstName, lastName, email) {
    // Uses clump
  }

  private formatOutput(firstName, lastName, email) {
    // Uses clump
  }

  private sendEmail(email) {
    // Only uses one part
  }
}

// ✅ AFTER: Extract to own class
class User {
  constructor(firstName, lastName, email) {
    this.validate();
  }

  validate() {
    // Validation uses all fields
  }

  format(): string {
    // Formatting uses all fields
  }

  getEmail() {
    return this.email;
  }
}

class ReportService {
  generateUserReport(user: User) {
    this.formatOutput(user);
    this.sendEmail(user.getEmail());
  }

  private formatOutput(user: User) {
    return user.format();
  }

  private sendEmail(email: string) {
    // Now receives what it needs
  }
}
```

---

## 🔍 The "Clump Index"

**When is it really a clump?**

```typescript
// If the same 3+ fields appear together in:
// 1 location: Not a clump yet (could be coincidence)
// 2 locations: Possible clump (watch it)
// 3+ locations: DEFINITELY A CLUMP (extract)
```

| Appearances | Status | Action |
|-------------|--------|--------|
| 1 | ✅ Single use | Monitor |
| 2 | ⚠️ Possible pattern | Consider extracting |
| 3+ | 🚩 Definite clump | Extract immediately |

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Related data should be together
- **DRY Principle** - Don't repeat data field lists
- **Orthogonality** - Related data grouped = better organization
- **Small Steps** - Extract clumps incrementally
- **Long Parameter List** - Clumps make parameter lists long

---

## ✅ Checklist: Avoid Data Clumps

When writing code:

- [ ] Do these 3+ fields always appear together?
- [ ] Could they form a concept (User, Address, etc.)?
- [ ] Would extracting reduce parameter lists?
- [ ] Do they get passed to multiple functions?
- [ ] Would grouping make code clearer?
- [ ] Would it reduce duplication?

---

## ✨ Remember

**DON'T DO**: Scatter related data across multiple fields and parameters.

**DO**: Group related data into objects that represent concepts.

**Rule of thumb**: If you pass the same 3 fields together, extract them into a class.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-data-clumps.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Group related data. Extract clumps into objects.**
