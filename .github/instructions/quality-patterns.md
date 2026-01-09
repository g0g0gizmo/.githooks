# Core Principle: Quality Patterns

**Purpose**: Catalog of anti-patterns and their solutions
**Audience**: You + AI (identifying and fixing code quality issues)
**Focus**: 10 common anti-patterns with detection and resolution
**Philosophy**: Learn patterns, recognize issues, apply fixes

---

## 🎯 What Are Quality Patterns?

Quality patterns are:
- ✅ **Anti-Patterns**: Code structures that indicate problems
- ✅ **Detection Signs**: How to recognize them
- ✅ **Why They're Bad**: Impact on code quality
- ✅ **Refactoring Solutions**: How to fix them
- ✅ **Prevention**: How to avoid them

---

## 📋 10 Anti-Patterns

---

## 1. God Object (Swiss Army Class)

**Description**: One class does everything; has too many responsibilities

### 🚩 Detection Signs

```typescript
// ❌ Typical God Object
class Application {
  // User management (20 methods)
  createUser() { }
  deleteUser() { }
  // ...

  // Payment processing (15 methods)
  processPayment() { }
  refund() { }
  // ...

  // Email sending (10 methods)
  sendEmail() { }
  // ...

  // Logging (8 methods)
  log() { }
  // ...

  // Database operations (12 methods)
  query() { }
  insert() { }
  // ...

  // Total: 65 methods, 3000 lines
}
```

**Symptoms**:
- [ ] Class with 50+ methods
- [ ] Class with 1000+ lines
- [ ] Multiple reasons to change the class
- [ ] Methods don't share data
- [ ] Hard to understand class purpose
- [ ] Hard to test class independently
- [ ] Can't reuse parts of class elsewhere

### 💔 Why It's Bad

- ❌ Multiple reasons to change
- ❌ Hard to understand
- ❌ Hard to test
- ❌ Can't reuse parts
- ❌ Every method affects everything
- ❌ Team doesn't know what's responsible for what

### ✅ Solution: Extract Classes

```typescript
// After: Each class one responsibility

class UserService {
  createUser() { }
  deleteUser() { }
}

class PaymentService {
  processPayment() { }
  refund() { }
}

class EmailService {
  sendEmail() { }
}

class LogService {
  log() { }
}

class DatabaseService {
  query() { }
  insert() { }
}
```

**Benefits**:
- ✅ Each class one responsibility
- ✅ Easy to understand
- ✅ Easy to test
- ✅ Can reuse parts
- ✅ Changes localized

---

## 2. Shotgun Surgery (Ripple Effect)

**Description**: Changes to one requirement require modifying many scattered places

### 🚩 Detection Signs

```typescript
// ❌ Typical Shotgun Surgery
// Requirement: "Add 'admin' field to users"

// Change in UserModel
class UserModel {
  constructor(name, email) {
    this.name = name;
    this.email = email;
    // Add: this.admin = false;
  }
}

// Change in UserValidator
function validateUser(user) {
  if (!user.email) throw new Error('Email required');
  if (!user.name) throw new Error('Name required');
  // Add: if (!user.admin) throw new Error('Admin required');
}

// Change in UserRepository
class UserRepository {
  save(user) {
    db.insert('users', {
      name: user.name,
      email: user.email,
      // Add: admin: user.admin
    });
  }
}

// Change in UserAPI
app.post('/api/users', (req, res) => {
  const user = {
    name: req.body.name,
    email: req.body.email,
    // Add: admin: req.body.admin
  };
  userService.createUser(user);
});

// Change in UserUI
function CreateUserForm() {
  return (
    <form>
      <input name="name" />
      <input name="email" />
      {/* Add: <input name="admin" /> */}
    </form>
  );
}

// Change in many tests
// Change in documentation
// ...

// One requirement → 10+ places to modify
```

**Symptoms**:
- [ ] One requirement touches 5+ files
- [ ] Similar changes in multiple places
- [ ] Changes aren't in obvious locations
- [ ] Easy to forget a location (creating bug)

### 💔 Why It's Bad

- ❌ One change → many places to update
- ❌ Easy to miss a location
- ❌ Creates bugs when you forget
- ❌ Slow to implement changes
- ❌ High risk of introducing bugs

### ✅ Solution: Extract Shared Logic

```typescript
// After: Define once, use everywhere

// 1. Define the schema in one place
const UserSchema = {
  name: { required: true },
  email: { required: true },
  admin: { required: false, default: false }
};

// 2. Generate validation from schema
function validateUser(user) {
  for (const [field, rules] of Object.entries(UserSchema)) {
    if (rules.required && !user[field]) {
      throw new Error(`${field} required`);
    }
  }
}

// 3. Generate database schema from schema
const createUsersTable = () => {
  db.schema.createTable('users', (table) => {
    for (const [field, rules] of Object.entries(UserSchema)) {
      if (field === 'name') table.string('name');
      if (field === 'email') table.string('email');
      if (field === 'admin') table.boolean('admin').default(false);
    }
  });
};

// 4. Use schema in API
app.post('/api/users', (req, res) => {
  const user = {
    name: req.body.name,
    email: req.body.email,
    admin: req.body.admin // From schema
  };
  validateUser(user);
  userService.createUser(user);
});

// New requirement: Add 'email' field
// Change: UserSchema (ONE place)
// Everything else auto-updates!
```

---

## 3. Feature Envy

**Description**: A method uses more data from another class than its own

### 🚩 Detection Signs

```typescript
// ❌ Feature Envy
class UserValidator {
  validate(user) {
    // Accessing order data instead of using OrderValidator
    if (user.order.total < 0) return false;
    if (user.order.items.length === 0) return false;
    if (user.order.customer.email === '') return false;
    return true;
  }
}

// Uses more data from Order than from User
```

**Symptoms**:
- [ ] Method accesses another object's fields
- [ ] Method doesn't use own class's data
- [ ] Method calls many methods on another object

### ✅ Solution: Move Logic to Owner

```typescript
// ✅ After: Each class validates its own data

class OrderValidator {
  validate(order) {
    if (order.total < 0) return false;
    if (order.items.length === 0) return false;
    if (order.customer.email === '') return false;
    return true;
  }
}

class UserValidator {
  validate(user) {
    // Validate user's own data
    if (!user.email) return false;
    if (!user.name) return false;
    return true;
  }
}

// Usage:
const userValid = userValidator.validate(user);
const orderValid = orderValidator.validate(user.order);
```

---

## 4. Temporary Fields

**Description**: Object has fields that are only used in some cases

### 🚩 Detection Signs

```typescript
// ❌ Temporary Fields
class User {
  name: string;
  email: string;
  // Only used when resetting password
  resetToken?: string;
  resetTokenExpiry?: number;
  resetTokenUsed?: boolean;

  // Only used when uploading profile picture
  tempImagePath?: string;
  tempImageName?: string;

  // Only used during registration
  verificationCode?: string;
}

// Object has too many optional fields
// Hard to understand when fields are set/used
```

**Symptoms**:
- [ ] Many optional/nullable fields
- [ ] Fields only used in specific contexts
- [ ] Can't understand class without reading all methods

### ✅ Solution: Extract into Separate Classes

```typescript
// ✅ After: Each context has its own class

class User {
  name: string;
  email: string;
  // Only core fields
}

class PasswordReset {
  userId: string;
  resetToken: string;
  resetTokenExpiry: number;
  resetTokenUsed: boolean;
}

class ProfilePictureUpload {
  userId: string;
  tempImagePath: string;
  tempImageName: string;
}

class Registration {
  email: string;
  verificationCode: string;
}

// Each context has exactly what it needs
```

---

## 5. Duplicate Code

**Description**: Same code logic appears in multiple places

### 🚩 Detection Signs

```typescript
// ❌ Duplicate Code
function validateUserEmail(email: string) {
  return email.includes('@') && email.length > 5;
}

function validateAdminEmail(email: string) {
  return email.includes('@') && email.length > 5;  // Duplicate!
}

function validateContactEmail(email: string) {
  return email.includes('@') && email.length > 5;  // Duplicate!
}
```

**Symptoms**:
- [ ] Same logic in 2+ places
- [ ] Copy-paste code visible
- [ ] Changing one copy but not others creates bugs

### ✅ Solution: Extract to Shared Function

```typescript
// ✅ After: One function, used everywhere

function validateEmail(email: string) {
  return email.includes('@') && email.length > 5;
}

const userEmail = validateEmail(email);
const adminEmail = validateEmail(email);
const contactEmail = validateEmail(email);

// Change validation once; everywhere uses new rule
```

---

## 6. Long Parameter Lists

**Description**: Function has too many parameters

### 🚩 Detection Signs

```typescript
// ❌ Long Parameter List
function calculatePrice(
  productId,
  quantity,
  customerId,
  discountPercentage,
  taxRate,
  shippingCost,
  insuranceFee,
  warehouseFee,
  handlingFee,
  promotionCode,
  loyaltyPoints
) {
  // Hard to remember parameter order
  // Easy to pass parameters in wrong order
  // Hard to extend without breaking callers
}

// Usage (error-prone):
calculatePrice(123, 5, 456, 0.2, 0.08, 10, 5, 2, 1, 'PROMO', 100);
// Which parameter is which?
```

**Symptoms**:
- [ ] Function with 5+ parameters
- [ ] Parameter order is easy to confuse
- [ ] Parameters seem unrelated

### ✅ Solution: Group into Objects

```typescript
// ✅ After: Related parameters grouped

interface PriceCalculation {
  product: Product;
  quantity: number;
  customer: Customer;
  discounts: {
    percentage: number;
    promotionCode: string;
    loyaltyPoints: number;
  };
  costs: {
    tax: number;
    shipping: number;
    insurance: number;
    warehouse: number;
    handling: number;
  };
}

function calculatePrice(calculation: PriceCalculation) {
  // Clear what each parameter is
  // Easy to add new parameters
  // Self-documenting
}

// Usage (clear):
const price = calculatePrice({
  product,
  quantity: 5,
  customer,
  discounts: { percentage: 0.2, promotionCode: 'PROMO', loyaltyPoints: 100 },
  costs: { tax: 0.08, shipping: 10, insurance: 5, warehouse: 2, handling: 1 }
});
```

---

## 7. Primitive Obsession

**Description**: Using primitives instead of small objects for simple concepts

### 🚩 Detection Signs

```typescript
// ❌ Primitive Obsession
function createUser(name: string, email: string, phone: string) {
  // What if email is invalid?
  // What if phone is malformed?
  // No encapsulation of validation logic
}

const user = createUser('John', 'invalid-email', '555-1234');
// Accepted invalid data!

// Or scattered validation:
if (!email.includes('@')) { /* error */ }
if (!phone.match(/\d{3}-\d{4}/)) { /* error */ }
// Validation scattered everywhere
```

**Symptoms**:
- [ ] Primitives used for concepts
- [ ] Validation logic scattered
- [ ] Same validation in multiple places

### ✅ Solution: Create Value Objects

```typescript
// ✅ After: Value objects encapsulate validation

class Email {
  constructor(value: string) {
    if (!value.includes('@')) {
      throw new Error('Invalid email');
    }
    this.value = value;
  }

  toString() { return this.value; }
}

class Phone {
  constructor(value: string) {
    if (!value.match(/\d{3}-\d{4}/)) {
      throw new Error('Invalid phone');
    }
    this.value = value;
  }

  toString() { return this.value; }
}

function createUser(name: string, email: Email, phone: Phone) {
  // Email and Phone already validated
  // Validation logic in one place
}

const user = createUser('John', new Email('john@example.com'), new Phone('555-1234'));
// Invalid data rejected at construction
```

---

## 8. Switch Statements

**Description**: Complex switch/if-else chains that should be polymorphism

### 🚩 Detection Signs

```typescript
// ❌ Switch Statements
function calculateBonus(employeeType: string, salary: number) {
  switch (employeeType) {
    case 'manager':
      return salary * 0.2;
    case 'developer':
      return salary * 0.15;
    case 'designer':
      return salary * 0.1;
    case 'intern':
      return salary * 0.05;
    default:
      return 0;
  }
}

// Adding new employee type requires modifying this function
```

**Symptoms**:
- [ ] Large switch/if-else statements
- [ ] Adding new case requires modifying function
- [ ] Logic repeated in similar cases

### ✅ Solution: Use Polymorphism

```typescript
// ✅ After: Polymorphism

interface Employee {
  calculateBonus(): number;
}

class Manager implements Employee {
  constructor(private salary: number) {}
  calculateBonus() { return this.salary * 0.2; }
}

class Developer implements Employee {
  constructor(private salary: number) {}
  calculateBonus() { return this.salary * 0.15; }
}

class Designer implements Employee {
  constructor(private salary: number) {}
  calculateBonus() { return this.salary * 0.1; }
}

class Intern implements Employee {
  constructor(private salary: number) {}
  calculateBonus() { return this.salary * 0.05; }
}

// Adding new type: just create new class, no existing code changes
```

---

## 9. Lazy Class

**Description**: Class that doesn't do much and isn't worth keeping

### 🚩 Detection Signs

```typescript
// ❌ Lazy Class
class UserWrapper {
  constructor(private user: User) {}

  getName() {
    return this.user.name;  // Just delegates
  }

  getEmail() {
    return this.user.email;  // Just delegates
  }

  setName(name) {
    this.user.name = name;  // Just delegates
  }
}

// This class adds no value; just wraps another class
```

**Symptoms**:
- [ ] Class only wraps another class
- [ ] Methods just delegate to another object
- [ ] No additional logic or validation
- [ ] Only one client uses it

### ✅ Solution: Inline or Remove

```typescript
// ✅ Option 1: Remove wrapper
const user = new User();
user.getName();  // Use directly

// ✅ Option 2: If wrapper adds value, keep it
class ValidatedUser {
  constructor(private user: User) {}

  setName(name: string) {
    if (!name || name.length === 0) {
      throw new Error('Name required');
    }
    this.user.name = name;
  }

  getName() {
    return this.user.name;
  }
}

// Now wrapper adds validation logic; it's worth keeping
```

---

## 10. Parallel Inheritance Hierarchies

**Description**: When you add a subclass of A, you must also add a subclass of B

### 🚩 Detection Signs

```typescript
// ❌ Parallel Hierarchies
// Transportation
class Vehicle { }
class Car extends Vehicle { }
class Truck extends Vehicle { }
class Bicycle extends Vehicle { }

// Driver - must mirror transportation
class Driver { }
class CarDriver extends Driver { }
class TruckDriver extends Driver { }
class BicycleDriver extends Driver { }

// Add new vehicle type? Must add new driver type too
// Classes are tightly coupled
```

**Symptoms**:
- [ ] Similar class names in two hierarchies
- [ ] Adding subclass to one requires adding to other
- [ ] One hierarchy mirrors another

### ✅ Solution: Composition Over Inheritance

```typescript
// ✅ After: Use composition

class Vehicle { }
class Car extends Vehicle { }
class Truck extends Vehicle { }

interface CanDrive {
  drive(): void;
}

class Driver {
  constructor(private vehicle: Vehicle & CanDrive) {}

  drive() {
    this.vehicle.drive();
  }
}

// Add new vehicle? Just implement CanDrive
class Bicycle extends Vehicle implements CanDrive {
  drive() { /* bicycle logic */ }
}

const cyclist = new Driver(new Bicycle());
// No parallel class needed
```

---

## 📝 Detection Template

Use this when you suspect an anti-pattern:

```
ANTI-PATTERN DETECTION

Pattern Suspected: [Which pattern?]
File/Class: [Location]
Evidence:
  - [Sign 1]
  - [Sign 2]
  - [Sign 3]

Impact:
  - [How does this harm code quality?]
  - [What will break when requirements change?]

Suggested Fix:
  - [Apply which refactoring?]
  - [Which principle does it serve?]

Effort to Fix:
  - [ ] Low (< 1 hour)
  - [ ] Medium (1-4 hours)
  - [ ] High (> 4 hours)

Priority:
  - [ ] Critical (fix immediately)
  - [ ] Important (fix soon)
  - [ ] Nice to have (fix when time permits)
```

---

## ✅ Anti-Pattern Prevention Checklist

To avoid anti-patterns:

- [ ] Does this class have one clear responsibility?
- [ ] Can I describe it in one sentence without "and"?
- [ ] Would changing it require changing other classes?
- [ ] Can I test this independently?
- [ ] Are there other classes with similar logic?
- [ ] Are my parameters getting out of hand?
- [ ] Do I have optional/unused fields?
- [ ] Am I duplicating validation logic?
- [ ] Am I using primitives for concepts?
- [ ] Could polymorphism replace these conditionals?

---

## 📚 Relationship to Core Principles

- **SOLID Principles**: Anti-patterns violate SOLID
- **Refactoring Techniques**: Fixes use refactoring patterns
- **Review Dimensions**: Anti-patterns hurt multiple dimensions
- **ETC Principle**: Anti-patterns make code harder to change
- **DRY**: Duplication and Feature Envy violate DRY

---

## ✨ Remember

**Anti-patterns are guides, not rules.**

The goal isn't to follow patterns perfectly. The goal is to:
- ✅ Recognize when patterns emerge
- ✅ Understand why they're problematic
- ✅ Apply appropriate fixes
- ✅ Keep code maintainable

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/quality-patterns.md`
**Created**: 2025-11-09
**Purpose**: Catalog of anti-patterns and solutions
**Philosophy**: Learn patterns, recognize issues, apply fixes

🚀 **Learn patterns. Recognize issues. Build better code.**
