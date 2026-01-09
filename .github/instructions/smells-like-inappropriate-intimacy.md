# Code Smell: Inappropriate Intimacy

**Purpose**: Identify and avoid classes knowing too much about each other
**Audience**: You + AI (code review, refactoring)
**Category**: Couplers (Too Tightly Connected)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Inappropriate Intimacy** occurs when one class accesses the private data/methods of another class.

Classes should respect boundaries. When Class A knows about Class B's internals, they're tightly coupled and fragile.

### Why It Matters

Inappropriate intimacy causes:
- ❌ Tight coupling between classes
- ❌ Hard to change one class without breaking another
- ❌ Encapsulation is violated
- ❌ Classes depend on implementation details
- ❌ Hard to understand relationships

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Class accessing another's private data
class Customer {
  private firstName: string;
  private lastName: string;
  private email: string;
  private orders: Order[] = [];
}

class OrderService {
  generateShippingLabel(customer: Customer, order: Order): string {
    // Inappropriately accessing private Customer fields
    const name = `${customer['firstName']} ${customer['lastName']}`;  // ← Private access
    const address = customer['address'];                              // ← Private access

    // Inappropriately accessing private Order fields
    const items = order['items'];                                     // ← Private access
    const weight = order['calculateWeight']();                        // ← Private method

    return `Ship to: ${name}, ${address}. Weight: ${weight}`;
  }
}

// Problems:
// - OrderService knows about Customer's internals
// - OrderService knows about Order's internals
// - Change Customer structure → breaks OrderService
// - Can't refactor either class independently
```

**Symptoms**:
- [ ] Accessing fields with private/protected modifier
- [ ] Accessing methods that should be internal
- [ ] Using `['fieldName']` to bypass access control
- [ ] Knowing about implementation details
- [ ] Multiple classes accessing same private fields
- [ ] Comments explaining what a private field is used for
- [ ] Difficult to change class structure

---

## 💔 Why It's Bad

### Problem 1: Tight Coupling

```typescript
// ❌ Classes tightly coupled via private access
class BankAccount {
  private balance: number = 0;
  private transactions: Transaction[] = [];

  deposit(amount: number): void {
    this.balance += amount;
    this.transactions.push(new Transaction('deposit', amount));
  }
}

class AuditService {
  // Inappropriately accessing private fields
  getBalance(account: BankAccount): number {
    return account['balance'];  // Private access!
  }

  getTransactionHistory(account: BankAccount): Transaction[] {
    return account['transactions'];  // Private access!
  }

  getTotalDeposits(account: BankAccount): number {
    return account['transactions']
      .filter(t => t.type === 'deposit')
      .reduce((sum, t) => sum + t.amount, 0);
  }
}

// Now AuditService is tightly coupled to BankAccount's structure
// Can't refactor BankAccount without breaking AuditService
```

### Problem 2: Implementation Details Exposed

```typescript
// ❌ Must know implementation to use correctly
class Document {
  private content: string = '';
  private metadata: Map<string, string> = new Map();
}

class DocumentPrinter {
  print(doc: Document): void {
    // Must know Document stores content as string
    const content = doc['content'];  // Assumes it's public!

    // Must know Document uses Map for metadata
    const title = doc['metadata'].get('title');  // Assumes it's a Map!

    // What if Document changes structure?
    // DocumentPrinter breaks!
  }
}

// DocumentPrinter depends on Document's implementation
// Can't change Document without breaking DocumentPrinter
```

### Problem 3: Indirect Modification

```typescript
// ❌ Accessing and modifying private state
class ShoppingCart {
  private items: Item[] = [];
  private total: number = 0;
}

class CartManager {
  addItem(cart: ShoppingCart, item: Item): void {
    // Directly modifying private fields!
    cart['items'].push(item);           // ← Modifying private array
    cart['total'] += item.price;        // ← Modifying private number

    // But what if there's special logic for adding items?
    // CartManager bypassed it!
    // What if there are constraints?
    // CartManager ignored them!
  }
}

// ShoppingCart lost control of its state
// CartManager is now responsible for maintaining consistency
```

### Problem 4: Unclear Relationships

```typescript
// ❌ Confusing web of private access
class User {
  private profile: Profile = new Profile();
}

class Profile {
  private preferences: Preferences = new Preferences();
}

class PreferenceManager {
  setTheme(user: User, theme: string): void {
    // Accessing User.profile (private)
    const profile = user['profile'];
    // Accessing Profile.preferences (private)
    const prefs = profile['preferences'];
    // Accessing Preferences.theme (private)
    prefs['theme'] = theme;
  }
}

// Confusing dependency chain
// Must know User → Profile → Preferences structure
// Hard to understand relationships
```

---

## ✅ Refactoring Solutions

### Solution 1: Move Method

```typescript
// ❌ BEFORE: OrderService accessing Customer internals
class Customer {
  private firstName: string;
  private lastName: string;
  private email: string;
}

class OrderService {
  getCustomerDisplayName(customer: Customer): string {
    // Inappropriately accessing private fields
    return `${customer['firstName']} ${customer['lastName']}`;
  }
}

// ✅ AFTER: Move method to Customer
class Customer {
  private firstName: string;
  private lastName: string;
  private email: string;

  getDisplayName(): string {
    return `${this.firstName} ${this.lastName}`;
  }
}

class OrderService {
  getCustomerDisplayName(customer: Customer): string {
    return customer.getDisplayName();  // Use public method
  }
}

// Now OrderService doesn't access private data
```

### Solution 2: Extract Method/Interface

```typescript
// ❌ BEFORE: Accessing private calculation
class Order {
  private items: OrderItem[] = [];

  private calculateSubtotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }
}

class OrderReporter {
  generateReport(order: Order): string {
    // Accessing private method!
    const subtotal = order['calculateSubtotal']();  // ← Private access

    return `Subtotal: $${subtotal}`;
  }
}

// ✅ AFTER: Extract to public method
class Order {
  private items: OrderItem[] = [];

  private calculateSubtotal(): number {
    return this.items.reduce((sum, item) => sum + item.price, 0);
  }

  getSubtotal(): number {
    return this.calculateSubtotal();
  }
}

class OrderReporter {
  generateReport(order: Order): string {
    const subtotal = order.getSubtotal();  // Use public method
    return `Subtotal: $${subtotal}`;
  }
}
```

### Solution 3: Use Delegation

```typescript
// ❌ BEFORE: Accessing through multiple layers
class Order {
  private customer: Customer;
}

class Customer {
  private address: Address;
}

class AddressValidator {
  validate(order: Order): boolean {
    // Accessing private fields through chain
    const address = order['customer']['address'];  // ← Double indirection
    return this.isValidAddress(address);
  }
}

// ✅ AFTER: Use delegation
class Order {
  private customer: Customer;

  getDeliveryAddress(): Address {
    return this.customer.getAddress();
  }
}

class Customer {
  private address: Address;

  getAddress(): Address {
    return this.address;
  }
}

class AddressValidator {
  validate(order: Order): boolean {
    const address = order.getDeliveryAddress();  // Clear delegation
    return this.isValidAddress(address);
  }
}

// No direct private access
```

### Solution 4: Hide Delegate

```typescript
// ❌ BEFORE: Accessing nested private fields
class Company {
  private manager: Manager;
}

class Manager {
  private telephone: string;
}

class HiringService {
  contactManager(company: Company): void {
    // Must navigate through Company to reach Telephone
    const phone = company['manager']['telephone'];  // ← Inappropriate intimacy
    phone.call();
  }
}

// ✅ AFTER: Hide the delegate
class Company {
  private manager: Manager;

  getManagerPhone(): string {
    return this.manager.getPhone();
  }
}

class Manager {
  private telephone: string;

  getPhone(): string {
    return this.telephone;
  }
}

class HiringService {
  contactManager(company: Company): void {
    const phone = company.getManagerPhone();  // Simple delegation
    phone.call();
  }
}

// No navigation through private fields
```

### Solution 5: Extract Data Class

```typescript
// ❌ BEFORE: Accessing private point fields
class Rectangle {
  private x: number;
  private y: number;
  private width: number;
  private height: number;
}

class ShapeRenderer {
  draw(rect: Rectangle): void {
    // Accessing private coordinate fields
    const x = rect['x'];
    const y = rect['y'];
    const width = rect['width'];
    const height = rect['height'];

    canvas.drawRect(x, y, width, height);
  }
}

// ✅ AFTER: Extract Point class
class Point {
  constructor(readonly x: number, readonly y: number) {}
}

class Dimension {
  constructor(readonly width: number, readonly height: number) {}
}

class Rectangle {
  private position: Point;
  private size: Dimension;

  getPosition(): Point {
    return this.position;
  }

  getSize(): Dimension {
    return this.size;
  }
}

class ShapeRenderer {
  draw(rect: Rectangle): void {
    const position = rect.getPosition();
    const size = rect.getSize();

    canvas.drawRect(position.x, position.y, size.width, size.height);
  }
}

// No direct private access
```

---

## 🔍 Detecting Inappropriate Intimacy

**Watch for**:
- Square brackets accessing properties: `object['field']`
- Comments explaining private fields
- Accessing multiple private fields from same class
- Knowing too much about internal structure
- Comments like "private implementation detail"

---

## 📚 Relationship to Core Principles

- **Orthogonality** - Inappropriate intimacy reduces orthogonality
- **Encapsulation** - Core OOP principle being violated
- **SOLID-D** - Depend on abstractions, not implementations
- **Feature Envy** - Often appears with inappropriate intimacy

---

## ✅ Checklist: Avoid Inappropriate Intimacy

When writing code:

- [ ] Am I accessing private fields or methods?
- [ ] Could I use a public method instead?
- [ ] Do I need to know about this class's internals?
- [ ] Could the other class provide a method for this?
- [ ] Would hiding the delegate make this clearer?
- [ ] Am I tightly coupling to implementation?

---

## ✨ Remember

**DON'T DO**: Access private fields or methods of other classes.

**DO**: Respect encapsulation; use public interfaces.

**Rule of thumb**: If you're accessing another class's private data, that method should be in that class.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-inappropriate-intimacy.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Respect encapsulation. Use public interfaces. Don't know internals.**
