# Code Smell: Feature Envy

**Purpose**: Identify and avoid methods that use more data from other objects
**Audience**: You + AI (code review, refactoring)
**Category**: Couplers (Too Tightly Connected)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Feature Envy** occurs when a method of one class spends too much time using data from other classes.

A method should primarily work with the data of its own class. When a method accesses another object's fields/methods more than its own, it indicates:
- The method is in the wrong class
- Responsibility is misplaced
- Classes are too tightly coupled
- The method should be moved to where the data lives

### Why It Matters

Feature Envy causes:
- ❌ Tight coupling between classes
- ❌ Classes depend on each other's internal structure
- ❌ Hard to change one class without affecting another
- ❌ Method logic scattered across multiple classes
- ❌ Difficult to test without complex setup

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Method using another object's data more than its own
class Order {
  items: OrderItem[];
  customerId: string;
}

class OrderProcessor {
  // This method is envious of Order's data
  calculateOrderTotal(order: Order): number {
    let total = 0;

    // Accessing order.items extensively
    for (let item of order.items) {
      total += item.price * item.quantity;
    }

    // Accessing order.items again for discount
    if (order.items.length > 10) {
      total *= 0.9;
    }

    // Accessing order.customerId
    const customer = this.getCustomer(order.customerId);
    if (customer.isPremium) {
      total *= 0.95;
    }

    return total;
  }

  private getCustomer(id: string) { /* ... */ }
}

// OrderProcessor.calculateOrderTotal() uses:
// - order.items (3 times) ✓
// - order.customerId (1 time) ✓
// - Doesn't use: OrderProcessor's own data ✗
// This method belongs in Order class!
```

**Symptoms**:
- [ ] Method accessing another object's fields more than its own
- [ ] Method calls many getters/setters on another object
- [ ] Method working with another object's internal structure
- [ ] Similar method exists on the "envied" class
- [ ] Moving the method would reduce parameter passing
- [ ] The other class has all needed data
- [ ] Method name describes the other object's domain, not this class's

---

## 💔 Why It's Bad

### Problem 1: Tight Coupling

```typescript
// ❌ OrderProcessor coupled to Order's internal structure
class OrderProcessor {
  calculateTotal(order: Order): number {
    // Depends on Order.items structure
    // Depends on Order.customerId structure
    // If Order changes structure, this breaks
  }
}

// ✅ Order responsible for its own calculations
class Order {
  calculateTotal(): number {
    // Uses its own internal data
    // Can change structure without affecting other classes
  }
}
```

### Problem 2: Changes Ripple Outward

```typescript
// When Order structure changes:
// Original: order.items is array of objects with price, quantity
class Order {
  items: OrderItem[];
}

// New: items is now a Map for performance
class Order {
  items: Map<string, OrderItem>;
}

// Now OrderProcessor breaks!
class OrderProcessor {
  calculateTotal(order: Order): number {
    for (let item of order.items) {  // ❌ Breaks! Can't iterate Map like array
      total += item.price * item.quantity;
    }
  }
}

// If Order had the method, it would just work:
class Order {
  calculateTotal(): number {
    let total = 0;
    // Iterates Map correctly
    for (let item of this.items.values()) {
      total += item.price * item.quantity;
    }
    return total;
  }
}
```

### Problem 3: Hard to Test

```typescript
// ❌ Testing Feature Envy requires mocking another class
describe('OrderProcessor', () => {
  it('should calculate total', () => {
    const mockOrder = {
      items: [
        { price: 10, quantity: 2 },
        { price: 5, quantity: 3 },
      ],
      customerId: 'cust123',
    };

    const mockCustomer = {
      isPremium: true,
    };

    const processor = new OrderProcessor();
    processor.getCustomer = jest.fn().mockReturnValue(mockCustomer);

    const result = processor.calculateOrderTotal(mockOrder);

    expect(result).toBe(42.75);
  });
});

// ✅ Testing when logic is in Order
describe('Order', () => {
  it('should calculate total', () => {
    const order = new Order([
      new OrderItem(10, 2),
      new OrderItem(5, 3),
    ]);

    const result = order.calculateTotal();

    expect(result).toBe(50);
  });
});
// Much simpler!
```

### Problem 4: Misplaced Responsibility

```typescript
// ❌ Confused about where responsibility lies
class Customer {
  name: string;
  email: string;
  orders: Order[];
}

class Invoice {
  // Who should calculate customer's total spending?
  // Invoice? Customer? Both?
  calculateCustomerTotal(customer: Customer): number {
    return customer.orders
      .reduce((sum, order) => sum + order.total, 0);
  }
}

// ✅ Clear responsibility
class Customer {
  name: string;
  email: string;
  orders: Order[];

  getTotalSpending(): number {
    return this.orders
      .reduce((sum, order) => sum + order.total, 0);
  }
}

class Invoice {
  // Calls the method on the owner
  customer: Customer;

  getCustomerTotal(): number {
    return this.customer.getTotalSpending();
  }
}
```

---

## ✅ Refactoring Solutions

### Solution 1: Move Method

```typescript
// ❌ BEFORE: Feature Envy
class Order {
  items: OrderItem[];
}

class OrderCalculator {
  // Envious of Order.items
  calculateTotal(order: Order): number {
    let total = 0;
    for (let item of order.items) {
      total += item.price * item.quantity;
    }
    return total;
  }
}

// ✅ AFTER: Move method to Order
class Order {
  items: OrderItem[];

  calculateTotal(): number {
    let total = 0;
    for (let item of this.items) {
      total += item.price * item.quantity;
    }
    return total;
  }
}

class OrderCalculator {
  // No longer needs Order's data
  // Or is eliminated entirely if not needed
}

// Usage
const total = order.calculateTotal();
```

### Solution 2: Extract Method First

```typescript
// When moving is complex, extract first
class OrderProcessor {
  // Complex method with feature envy
  processOrder(order: Order): void {
    // Validation using order data
    if (!order.items || order.items.length === 0) {
      throw new Error('No items');
    }

    // Calculation using order data
    const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    // Business logic using order data
    if (total > 1000) {
      order.premium = true;
    }

    // Saving
    this.database.save(order);
  }
}

// ✅ Extract the envious part first
class OrderProcessor {
  processOrder(order: Order): void {
    this.validateOrder(order);
    order.calculateTotal();  // Move responsibility
    this.applyPremium(order);
    this.database.save(order);
  }

  private validateOrder(order: Order): void {
    order.validate();  // Move to Order
  }

  private applyPremium(order: Order): void {
    order.applyPremiumIfEligible();  // Move to Order
  }
}

class Order {
  items: OrderItem[];
  premium: boolean;

  validate(): void {
    if (!this.items || this.items.length === 0) {
      throw new Error('No items');
    }
  }

  calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  applyPremiumIfEligible(): void {
    const total = this.calculateTotal();
    if (total > 1000) {
      this.premium = true;
    }
  }
}
```

### Solution 3: Pass Derived Value

```typescript
// ❌ Method envies multiple fields of another object
class User {
  firstName: string;
  lastName: string;
  email: string;
  joinDate: Date;
}

class UserAnalytics {
  analyzeUser(user: User): Report {
    // Envy: accessing user.firstName, user.lastName, user.email, user.joinDate
    const fullName = `${user.firstName} ${user.lastName}`;
    const emailDomain = user.email.split('@')[1];
    const yearsActive = new Date().getFullYear() - user.joinDate.getFullYear();

    return {
      name: fullName,
      domain: emailDomain,
      tenure: yearsActive,
    };
  }
}

// ✅ Pass derived values instead
class User {
  firstName: string;
  lastName: string;
  email: string;
  joinDate: Date;

  getFullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  getEmailDomain(): string {
    return this.email.split('@')[1];
  }

  getYearsActive(): number {
    return new Date().getFullYear() - this.joinDate.getFullYear();
  }
}

class UserAnalytics {
  analyzeUser(user: User): Report {
    // Now takes derived data, not raw fields
    return {
      name: user.getFullName(),
      domain: user.getEmailDomain(),
      tenure: user.getYearsActive(),
    };
  }
}
```

### Solution 4: Introduce Parameter Object

```typescript
// When method envies many fields, group them
class Document {
  title: string;
  author: string;
  createdDate: Date;
  lastModified: Date;
  wordCount: number;
}

class DocumentAnalyzer {
  // Envious of many Document fields
  analyzeMetadata(doc: Document): Metadata {
    return {
      title: doc.title,
      author: doc.author,
      created: doc.createdDate,
      modified: doc.lastModified,
      size: doc.wordCount,
    };
  }
}

// ✅ Extract metadata into its own class
class DocumentMetadata {
  title: string;
  author: string;
  createdDate: Date;
  lastModified: Date;
}

class Document {
  metadata: DocumentMetadata;
  wordCount: number;
}

class DocumentAnalyzer {
  // Now takes a single parameter object
  analyzeMetadata(metadata: DocumentMetadata): Metadata {
    return {
      title: metadata.title,
      author: metadata.author,
      created: metadata.createdDate,
      modified: metadata.lastModified,
    };
  }
}
```

### Solution 5: Replace with Delegation

```typescript
// ❌ Feature Envy via delegation chain
class Order {
  customer: Customer;
}

class Customer {
  address: Address;
}

class Address {
  street: string;
  city: string;
  country: string;
}

class Shipper {
  // Envious chain: order → customer → address
  calculateShipping(order: Order): number {
    const country = order.customer.address.country;
    const rate = this.getShippingRate(country);
    return rate;
  }
}

// ✅ Add delegation methods to break envy
class Order {
  customer: Customer;

  getShippingCountry(): string {
    return this.customer.getShippingCountry();
  }
}

class Customer {
  address: Address;

  getShippingCountry(): string {
    return this.address.country;
  }
}

class Shipper {
  // Now only depends on Order's public interface
  calculateShipping(order: Order): number {
    const country = order.getShippingCountry();
    const rate = this.getShippingRate(country);
    return rate;
  }
}
```

---

## 🔍 The "Envy Index"

**How much is a method envious?**

```typescript
class Reporter {
  generateReport(user: User): string {
    // Accessing User's data:
    // - user.name (1 access)
    // - user.email (1 access)
    // - user.joinDate (1 access)
    // = 3 user accesses

    // Accessing Reporter's own data:
    // - this.template (1 access)
    // = 1 access

    // Envy Index: 3/1 = 3x
    // HIGH ENVY - move method to User
  }
}

class Reporter {
  generateReport(user: User): string {
    // Accessing Reporter's data:
    // - this.template (2 accesses)
    // - this.config (1 access)
    // = 3 accesses

    // Accessing User's data:
    // - user.name (1 access)
    // = 1 access

    // Envy Index: 1/3 = 0.3
    // LOW ENVY - acceptable
  }
}
```

| Envy Index | Status | Action |
|-----------|--------|--------|
| < 1.0 | ✅ Good | Keep as is |
| 1.0 - 2.0 | ⚠️ Watch | Consider moving if it makes sense |
| 2.0 - 3.0 | 🚩 Problem | Should move method |
| > 3.0 | 🔴 Critical | Move method immediately |

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Method should be in class responsible for that concern
- **Orthogonality** - Tightly coupled classes reduce orthogonality
- **SOLID-S** - Feature Envy violates Single Responsibility Principle
- **DRY Principle** - Moving methods eliminates duplicated structure knowledge
- **Review Dimensions** - Modularity and coupling directly affected

---

## ✅ Checklist: Avoid Feature Envy

When writing methods:

- [ ] Does this method use more of another object's data than its own?
- [ ] Would moving this method reduce coupling?
- [ ] Does the other object have all the data needed?
- [ ] Is there a better place for this method?
- [ ] Could I pass derived values instead of raw fields?
- [ ] Am I accessing another object's internal structure?
- [ ] Would this method make more sense in the other class?
- [ ] Could I use delegation to hide the accessed fields?

---

## ✨ Remember

**DON'T DO**: Write methods that spend more time with another object's data than their own.

**DO**: Keep methods in the class that owns the data they primarily work with.

**Rule of thumb**: If a method accesses another object's fields more than its own, move it.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells/smells-like-feature-envy.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Keep methods with their data. Move envy away.**
