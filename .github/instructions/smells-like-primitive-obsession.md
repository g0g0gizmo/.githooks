# Code Smell: Primitive Obsession

**Purpose**: Identify and avoid over-reliance on primitive types
**Audience**: You + AI (code review, refactoring)
**Category**: Bloaters (Code That's Too Much)
**Severity**: 🟡 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Primitive Obsession** occurs when you use primitives (strings, numbers, booleans) instead of small domain objects.

Primitives should be wrapped in objects that represent their domain meaning. Using bare primitives makes code less type-safe and harder to understand.

### Why It Matters

Primitive obsession causes:
- ❌ Type-unsafe operations (string treated as phone number)
- ❌ Missing validation (negative ages accepted)
- ❌ Scattered logic (parsing date strings everywhere)
- ❌ Easy to make mistakes (mixing up types)
- ❌ Hard to add domain logic

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Using primitives instead of domain objects
class User {
  name: string;              // Could be Name object
  email: string;             // Could be Email object
  phone: string;             // Could be PhoneNumber object
  age: number;               // Could be Age object
  joinDate: string;          // Could be Date or DateTime object
  status: string;            // Could be UserStatus enum
  address: string;           // Could be Address object
}

// Problems:
// - Can pass invalid email as name
// - Can pass negative number as age
// - Phone number stored as plain string, no validation
// - Date stored as string, hard to compare dates
// - Status could be "avtive" (typo) instead of "active"
// - Address is one field, but should be structured

function updateUserAge(user: User, age: number) {
  user.age = age;  // Could be -5, nobody validates!
}

function sendEmail(user: User, subject: string, body: string) {
  // user.email is just a string
  // Could contain invalid email "notanemail"
  // No validation that it's actually an email
}
```

**Symptoms**:
- [ ] Using strings for things that should be typed (statuses, enums)
- [ ] Using numbers without validation (ages, quantities)
- [ ] Parsing dates/times from strings in multiple places
- [ ] No object to hold related primitive data
- [ ] Same validation logic in multiple places
- [ ] Easy to pass wrong type of primitive to function
- [ ] Comments explaining what a primitive means (smell indicator!)

---

## 💔 Why It's Bad

### Problem 1: No Type Safety

```typescript
// ❌ Primitives are not type-safe
function bookHotel(numberOfGuests: number, roomsNeeded: number, adults: number) {
  // Which parameter is which?
  // All are numbers!
}

// Called wrong:
bookHotel(5, 10, 2);  // Is this 5 guests, 10 rooms? Or vice versa?

// ✅ Type-safe with objects
class GuestCount {
  constructor(readonly value: number) {}
}

class RoomCount {
  constructor(readonly value: number) {}
}

function bookHotel(guests: GuestCount, rooms: RoomCount) {
  // Can't mix them up - different types!
}

bookHotel(new GuestCount(5), new RoomCount(10));  // Clear intent
```

### Problem 2: Missing Validation

```typescript
// ❌ Validation scattered or missing
function setUserAge(user, age: number) {
  if (age < 0 || age > 150) {
    throw new Error('Invalid age');
  }
  user.age = age;
}

function setProductPrice(product, price: number) {
  if (price < 0) {
    throw new Error('Invalid price');
  }
  product.price = price;
}

function setOrderQuantity(order, quantity: number) {
  if (quantity < 0) {
    throw new Error('Invalid quantity');
  }
  order.quantity = quantity;
}

// Same validation pattern repeated!
// What if validation requirements change?

// ✅ Encapsulated in objects
class Age {
  constructor(readonly value: number) {
    if (value < 0 || value > 150) {
      throw new Error('Invalid age');
    }
  }
}

class Money {
  constructor(readonly amount: number) {
    if (amount < 0) {
      throw new Error('Invalid amount');
    }
  }
}

class Quantity {
  constructor(readonly value: number) {
    if (value < 0) {
      throw new Error('Invalid quantity');
    }
  }
}

// Validation in one place
// Used everywhere
```

### Problem 3: Scattered Logic

```typescript
// ❌ Logic scattered across codebase
function getUserAge(birthDateString: string): number {
  const parts = birthDateString.split('-');
  const year = parseInt(parts[0]);
  const month = parseInt(parts[1]);
  const day = parseInt(parts[2]);
  const today = new Date();
  // complex age calculation...
}

// Used in 10 different files
// What if date format changes?
// Must update all 10 files

// ✅ Logic in one place
class BirthDate {
  constructor(readonly value: Date) {}

  getAge(): number {
    const today = new Date();
    // Complex calculation in one place
  }
}
```

### Problem 4: Mixing Concepts

```typescript
// ❌ Can't tell primitives apart
function processTransaction(
  accountId: string,
  transactionId: string,
  userId: string,
  orderId: string
) {
  // All strings! Easy to mix up
}

processTransaction("123", "456", "789", "999");  // Which is which?

// ✅ Different types for different concepts
class AccountId {
  constructor(readonly value: string) {}
}

class TransactionId {
  constructor(readonly value: string) {}
}

class UserId {
  constructor(readonly value: string) {}
}

class OrderId {
  constructor(readonly value: string) {}
}

function processTransaction(
  accountId: AccountId,
  transactionId: TransactionId,
  userId: UserId,
  orderId: OrderId
) {
  // Can't mix them up - different types
}
```

---

## ✅ Refactoring Solutions

### Solution 1: Replace Primitive with Object

```typescript
// ❌ BEFORE: Status as string
class User {
  status: string;  // "active", "inactive", "suspended"
}

function isUserActive(user: User): boolean {
  return user.status === 'active';
}

// ✅ AFTER: Status as enum
enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  SUSPENDED = 'suspended',
}

class User {
  status: UserStatus;
}

function isUserActive(user: User): boolean {
  return user.status === UserStatus.ACTIVE;
}
```

### Solution 2: Introduce Value Object

```typescript
// ❌ BEFORE: Email as string
class User {
  email: string;
}

function sendEmail(user: User, message: string) {
  // No validation that email is valid
  smtp.send(user.email, message);
}

// ✅ AFTER: Email as value object
class Email {
  constructor(readonly value: string) {
    if (!this.isValidEmail(value)) {
      throw new Error('Invalid email');
    }
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  toString(): string {
    return this.value;
  }
}

class User {
  email: Email;
}

function sendEmail(user: User, message: string) {
  // user.email is guaranteed valid
  smtp.send(user.email.toString(), message);
}
```

### Solution 3: Replace Type Code with Enum

```typescript
// ❌ BEFORE: Order type as integer
class Order {
  type: number;  // 1 = express, 2 = standard, 3 = economy
}

function getShippingDays(order: Order): number {
  if (order.type === 1) return 1;
  if (order.type === 2) return 5;
  if (order.type === 3) return 10;
}

// ✅ AFTER: Type as enum
enum ShippingType {
  EXPRESS = 'express',
  STANDARD = 'standard',
  ECONOMY = 'economy',
}

class Order {
  type: ShippingType;
}

function getShippingDays(order: Order): number {
  switch (order.type) {
    case ShippingType.EXPRESS: return 1;
    case ShippingType.STANDARD: return 5;
    case ShippingType.ECONOMY: return 10;
  }
}
```

### Solution 4: Extract Method for Validation

```typescript
// ❌ BEFORE: Validation scattered
function createUser(name: string, email: string, age: number) {
  if (!name || name.length < 2) throw new Error('Invalid name');
  if (!email.includes('@')) throw new Error('Invalid email');
  if (age < 18 || age > 120) throw new Error('Invalid age');
  // Create user
}

function updateUser(name: string, email: string, age: number) {
  if (!name || name.length < 2) throw new Error('Invalid name');
  if (!email.includes('@')) throw new Error('Invalid email');
  if (age < 18 || age > 120) throw new Error('Invalid age');
  // Update user
}

// ✅ AFTER: Validation in objects
class UserName {
  constructor(readonly value: string) {
    if (!value || value.length < 2) {
      throw new Error('Invalid name');
    }
  }
}

class Email {
  constructor(readonly value: string) {
    if (!value.includes('@')) {
      throw new Error('Invalid email');
    }
  }
}

class Age {
  constructor(readonly value: number) {
    if (value < 18 || value > 120) {
      throw new Error('Invalid age');
    }
  }
}

function createUser(name: UserName, email: Email, age: Age) {
  // Validation already done by constructors
}

function updateUser(name: UserName, email: Email, age: Age) {
  // Validation already done by constructors
}
```

### Solution 5: Create Simple Class for Multiple Primitives

```typescript
// ❌ BEFORE: Multiple related strings
function sendEmail(
  recipientFirstName: string,
  recipientLastName: string,
  recipientEmail: string,
  senderFirstName: string,
  senderLastName: string,
  senderEmail: string
) {
  // 6 parameters, all strings
}

// ✅ AFTER: Group into Person objects
class Person {
  constructor(
    readonly firstName: string,
    readonly lastName: string,
    readonly email: string
  ) {}

  getFullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }
}

function sendEmail(recipient: Person, sender: Person) {
  // Clear intent, fewer parameters
}
```

---

## 🔍 Common Primitives to Replace

| Primitive | Better | Example |
|-----------|--------|---------|
| `string` (status) | `enum` | `UserStatus` |
| `string` (email) | Value Object | `Email` class |
| `number` (age) | Value Object | `Age` class |
| `number` (money) | Value Object | `Money` class |
| `string` (date) | `Date` object | Date/DateTime |
| `string` (ID) | Value Object or Type Alias | `UserId` class |
| `string` (phone) | Value Object | `PhoneNumber` class |
| `string` (URL) | Value Object | `Url` class |

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Each type should represent one concept
- **SOLID-S** - Domain logic should be encapsulated
- **Type Safety** - Value objects provide type safety
- **Orthogonality** - Separate concerns (Email vs. String)

---

## ✅ Checklist: Avoid Primitive Obsession

When writing code:

- [ ] Am I using string/number/boolean for domain concepts?
- [ ] Could I create a type/class for this concept?
- [ ] Is the same validation repeated in multiple places?
- [ ] Would an object make the code clearer?
- [ ] Could I prevent invalid states with a type?

---

## ✨ Remember

**DON'T DO**: Use primitives for everything; mix up domain concepts.

**DO**: Create objects/enums that represent domain concepts.

**Rule of thumb**: If you need a comment explaining what a primitive means, create a type for it.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-primitive-obsession.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Replace primitives with domain objects. Type safety matters.**
