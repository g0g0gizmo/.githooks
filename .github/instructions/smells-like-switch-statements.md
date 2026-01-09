# Code Smell: Switch Statements

**Purpose**: Identify and avoid complex switch statements that should be polymorphism
**Audience**: You + AI (code review, refactoring)
**Category**: Object-Orientation Abusers (OOP Gone Wrong)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Switch Statements** is a smell when you have complex conditionals based on type, instead of using polymorphism.

Switch statements checking `if (type === X)` or `switch(object.type)` indicate that behavior should be in separate classes, not one large function.

### Why It Matters

Switch statements cause:
- ❌ Hard to add new types (must edit switch everywhere)
- ❌ Violates Open/Closed Principle (hard to extend)
- ❌ Logic scattered across multiple places
- ❌ Easy to forget to update all switches
- ❌ Indicates inheritance hierarchy is needed

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Switch statement on type
class PaymentProcessor {
  processPayment(payment: Payment) {
    switch (payment.type) {
      case 'credit-card':
        // Credit card logic (20 lines)
        const fee = payment.amount * 0.029;
        const total = payment.amount + fee;
        this.chargeCard(payment.cardNumber, total);
        break;

      case 'paypal':
        // PayPal logic (15 lines)
        const ppResponse = this.callPayPalAPI(payment.email, payment.amount);
        this.recordTransaction(ppResponse.id);
        break;

      case 'bank-transfer':
        // Bank transfer logic (25 lines)
        this.initiateWireTransfer(payment.accountNumber, payment.amount);
        this.recordBankDetails(payment.routingNumber);
        break;

      case 'bitcoin':
        // Bitcoin logic (20 lines)
        const rate = this.getBitcoinRate();
        const btcAmount = payment.amount / rate;
        this.sendBitcoinTransaction(payment.walletAddress, btcAmount);
        break;

      default:
        throw new Error('Unknown payment type');
    }
  }
}

// Problems:
// - 80+ lines in one method
// - Adding new payment type requires editing this method
// - Logic for each type mixed in one function
// - Can't test credit card logic independently
```

**Symptoms**:
- [ ] Switch/if-else based on type field
- [ ] Same switch appears in multiple methods
- [ ] Adding new type requires finding all switches
- [ ] Switch statements span 50+ lines
- [ ] Each case has significantly different logic
- [ ] Cases handle completely different concerns

---

## 💔 Why It's Bad

### Problem 1: Hard to Add New Types

```typescript
// ❌ When new type needed, must find and update all switches
class OrderCalculator {
  calculateTax(order: Order): number {
    if (order.type === 'digital') {
      return 0;  // No tax
    } else if (order.type === 'physical') {
      return order.amount * 0.08;
    } else if (order.type === 'service') {
      return order.amount * 0.05;
    }
  }

  calculateShipping(order: Order): number {
    if (order.type === 'digital') {
      return 0;  // No shipping
    } else if (order.type === 'physical') {
      return 15;
    } else if (order.type === 'service') {
      return 0;  // No shipping
    }
  }

  calculateProcessingTime(order: Order): number {
    if (order.type === 'digital') {
      return 1;  // 1 hour
    } else if (order.type === 'physical') {
      return 24;  // 1 day
    } else if (order.type === 'service') {
      return 48;  // 2 days
    }
  }
}

// New requirement: Add "subscription" type
// Must find and update:
// - calculateTax()
// - calculateShipping()
// - calculateProcessingTime()
// - Plus 10+ other methods!
// Easy to miss one → bug

// ✅ Polymorphism: Add new class, done!
abstract class Order {
  abstract calculateTax(): number;
  abstract calculateShipping(): number;
  abstract calculateProcessingTime(): number;
}

class DigitalOrder extends Order {
  calculateTax() { return 0; }
  calculateShipping() { return 0; }
  calculateProcessingTime() { return 1; }
}

class PhysicalOrder extends Order {
  calculateTax() { return this.amount * 0.08; }
  calculateShipping() { return 15; }
  calculateProcessingTime() { return 24; }
}

class SubscriptionOrder extends Order {
  calculateTax() { /* subscription logic */ }
  calculateShipping() { return 0; }
  calculateProcessingTime() { return 2; }
}

// Need new type? Create new class, implement methods
// No modifications to existing code
```

### Problem 2: Logic Scattered

```typescript
// ❌ Animal behavior scattered across many functions
function makeSound(animal: { type: string }) {
  if (animal.type === 'dog') return 'Woof!';
  if (animal.type === 'cat') return 'Meow!';
  if (animal.type === 'cow') return 'Moo!';
}

function eat(animal: { type: string }) {
  if (animal.type === 'dog') return 'dog food';
  if (animal.type === 'cat') return 'cat food';
  if (animal.type === 'cow') return 'grass';
}

function move(animal: { type: string }) {
  if (animal.type === 'dog') return 'run';
  if (animal.type === 'cat') return 'jump';
  if (animal.type === 'cow') return 'walk';
}

// Dog's behavior split across 3 functions!
// Hard to understand what a dog does

// ✅ Polymorphism: Keep behaviors together
abstract class Animal {
  abstract makeSound(): string;
  abstract eat(): string;
  abstract move(): string;
}

class Dog extends Animal {
  makeSound() { return 'Woof!'; }
  eat() { return 'dog food'; }
  move() { return 'run'; }
}

class Cat extends Animal {
  makeSound() { return 'Meow!'; }
  eat() { return 'cat food'; }
  move() { return 'jump'; }
}

// Dog's behavior in one place!
// Clear what a dog does
```

### Problem 3: Missing Cases

```typescript
// ❌ Easy to forget case
function handleOrderStatus(order: { status: string }) {
  switch (order.status) {
    case 'pending':
      this.sendConfirmation(order);
      break;
    case 'shipped':
      this.updateTracking(order);
      break;
    case 'delivered':
      this.sendThankYou(order);
      break;
    // Forgot 'cancelled'!
  }
}

// New status added, switches not updated
// Silent bug

// ✅ Polymorphism: Compiler enforces all cases
abstract class OrderStatus {
  abstract handle(order: Order): void;
}

class PendingStatus extends OrderStatus {
  handle(order: Order) { /* ... */ }
}

class ShippedStatus extends OrderStatus {
  handle(order: Order) { /* ... */ }
}

class DeliveredStatus extends OrderStatus {
  handle(order: Order) { /* ... */ }
}

class CancelledStatus extends OrderStatus {
  handle(order: Order) { /* ... */ }
}

// Must implement handle() for each status
// Compiler enforces it
```

---

## ✅ Refactoring Solutions

### Solution 1: Replace Type Code with Polymorphism

```typescript
// ❌ BEFORE: Switch on type
class Bird {
  type: string;  // "european", "african", "norwegian"
  speed: number;

  getSpeed(): number {
    switch (this.type) {
      case 'european':
        return 24.5;
      case 'african':
        return this.isLoadedWithCoconuts() ? 16 : 24;
      case 'norwegian':
        return this.isNailed() ? 0 : 24;
      default:
        throw new Error('Unknown bird');
    }
  }

  private isLoadedWithCoconuts(): boolean { /* ... */ }
  private isNailed(): boolean { /* ... */ }
}

// ✅ AFTER: Polymorphism
abstract class Bird {
  abstract getSpeed(): number;
}

class EuropeanSwallow extends Bird {
  getSpeed(): number {
    return 24.5;
  }
}

class AfricanSwallow extends Bird {
  private loadedWithCoconuts: boolean;

  getSpeed(): number {
    return this.loadedWithCoconuts ? 16 : 24;
  }
}

class NorwegianBlue extends Bird {
  private nailed: boolean;

  getSpeed(): number {
    return this.nailed ? 0 : 24;
  }
}
```

### Solution 2: Replace Conditional with Polymorphism (Strategy Pattern)

```typescript
// ❌ BEFORE: Conditionals on strategy
class TextFormatter {
  format(text: string, style: string): string {
    if (style === 'uppercase') {
      return text.toUpperCase();
    } else if (style === 'lowercase') {
      return text.toLowerCase();
    } else if (style === 'title-case') {
      return text.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    }
  }
}

// ✅ AFTER: Strategy pattern
interface TextStrategy {
  format(text: string): string;
}

class UppercaseStrategy implements TextStrategy {
  format(text: string): string {
    return text.toUpperCase();
  }
}

class LowercaseStrategy implements TextStrategy {
  format(text: string): string {
    return text.toLowerCase();
  }
}

class TitleCaseStrategy implements TextStrategy {
  format(text: string): string {
    return text.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }
}

class TextFormatter {
  format(text: string, strategy: TextStrategy): string {
    return strategy.format(text);
  }
}
```

### Solution 3: Replace with State Pattern

```typescript
// ❌ BEFORE: Switch on state
class TCPConnection {
  state: 'listen' | 'established' | 'closed' = 'listen';

  open(): void {
    if (this.state === 'listen') {
      this.state = 'established';
    }
  }

  close(): void {
    if (this.state === 'established') {
      this.state = 'closed';
    }
  }

  send(data: string): void {
    if (this.state === 'established') {
      console.log('Sending', data);
    } else {
      throw new Error('Cannot send in ' + this.state + ' state');
    }
  }
}

// ✅ AFTER: State pattern
interface ConnectionState {
  open(context: TCPConnection): void;
  close(context: TCPConnection): void;
  send(context: TCPConnection, data: string): void;
}

class ListenState implements ConnectionState {
  open(context: TCPConnection): void {
    context.setState(new EstablishedState());
  }

  close(context: TCPConnection): void {
    throw new Error('Cannot close from listen state');
  }

  send(context: TCPConnection, data: string): void {
    throw new Error('Cannot send from listen state');
  }
}

class EstablishedState implements ConnectionState {
  open(context: TCPConnection): void {
    throw new Error('Already open');
  }

  close(context: TCPConnection): void {
    context.setState(new ClosedState());
  }

  send(context: TCPConnection, data: string): void {
    console.log('Sending', data);
  }
}

class TCPConnection {
  private state: ConnectionState = new ListenState();

  setState(state: ConnectionState): void {
    this.state = state;
  }

  open(): void {
    this.state.open(this);
  }

  close(): void {
    this.state.close(this);
  }

  send(data: string): void {
    this.state.send(this, data);
  }
}
```

---

## 🔍 When Switch Statements Are OK

Switch statements are acceptable:
- **On simple values** - `switch (dayOfWeek)` for days
- **Return values** - Single return, not complex logic
- **Constants** - Not changing frequently

```typescript
// ✅ OK: Simple switch
function getDayName(day: number): string {
  switch (day) {
    case 0: return 'Sunday';
    case 1: return 'Monday';
    // ...
    default: return 'Unknown';
  }
}
```

But:
- ❌ Complex logic in cases → Use polymorphism
- ❌ Same switch in multiple places → Use polymorphism
- ❌ Checking object type → Use polymorphism

---

## 📚 Relationship to Core Principles

- **SOLID-O** - Open/Closed: Polymorphism allows extension without modification
- **SOLID-L** - Liskov Substitution: Subclasses can replace parent class
- **Single Responsibility** - Each type in own class
- **Orthogonality** - Decouple type-specific logic

---

## ✅ Checklist: Avoid Switch Statements

When writing code:

- [ ] Is this switch checking object type/status?
- [ ] Are there multiple places with similar switch?
- [ ] Would polymorphism make this clearer?
- [ ] Could each case be a separate class?
- [ ] Would new types require code changes?

---

## ✨ Remember

**DON'T DO**: Use switch statements for type-checking; create complex conditionals.

**DO**: Use polymorphism; create separate classes for different types.

**Rule of thumb**: If you're switching on type, create an inheritance hierarchy instead.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-switch-statements.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Replace switch statements with polymorphism.**
