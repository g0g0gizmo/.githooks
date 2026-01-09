---
description: 'Design independent, self-contained components that do not interfere with each other'
applyTo: '**/*'
---

# Orthogonality - Independent, Non-Interfering Components

## Overview

Orthogonality is a design principle where components are independent and self-contained—changes to one component don't require changes to others. The term comes from mathematics where orthogonal vectors don't influence each other. In software, orthogonal components don't interfere, making systems easier to change, test, and maintain.

Orthogonality ensures:

- Changes are localized to single components
- Components can be tested independently
- Debugging is straightforward
- Components are naturally reusable
- Scaling systems is feasible
- Low coupling between components

## Core Concepts

### 1. Low Coupling (Dependencies)

**Coupling** = How much one component depends on another

```typescript
// ✅ Low coupling: components don't depend on each other
class UserService {
  getUser(id: string) { /* ... */ }
}

class EmailService {
  sendEmail(email: string, message: string) { /* ... */ }
}

class PaymentService {
  processPayment(amount: number) { /* ... */ }
}

// Each service is independent
// Change UserService? Doesn't affect EmailService
// Swap PaymentService? Doesn't affect others
```

---

### 2. High Cohesion (Relatedness)

**Cohesion** = How much things within a component belong together

```typescript
// ✅ High cohesion: related things in one place
class UserService {
  getUser(id: string) { /* ... */ }
  createUser(email: string, name: string) { /* ... */ }
  updateUser(id: string, data: Partial<User>) { /* ... */ }
  deleteUser(id: string) { /* ... */ }
  // All about users; all belong together
}

// ❌ Low cohesion: unrelated things mixed
class UserManager {
  getUser(id: string) { /* ... */ }
  calculateTax(amount: number) { /* ... */ }
  sendEmail(to: string, message: string) { /* ... */ }
  processPayment(amount: number) { /* ... */ }
  // Unrelated concerns mixed together
}
```

### The Sweet Spot

Key idea: **Excellent design = Low Coupling + High Cohesion**

- Each module handles one thing (high cohesion)
- Modules don't depend on each other (low coupling)

---

## Application Checklist

- [ ] Each component has single, clear responsibility
- [ ] Components can be tested independently
- [ ] No circular dependencies between modules
- [ ] No unnecessary global state
- [ ] Dependencies are explicit (injected, not hidden)
- [ ] Components can be reused in different contexts
- [ ] No inappropriate access to private members
- [ ] Changes to one component don't affect others
- [ ] No hidden dependencies
- [ ] Clear boundaries between components

### When Designing Components

1. **Define Responsibility**: What does this component do?
2. **Identify Dependencies**: What does it need from others?
3. **Make Dependencies Explicit**: Inject, don't hide
4. **Minimize Coupling**: Only depend on what's needed
5. **Maximize Cohesion**: Keep related things together

### When Reviewing Code

- Does this component have one clear responsibility?
- Could this component be used elsewhere?
- Are dependencies obvious?
- Can this be tested without other components?
- Would changes cascade to other components?

---

## Related Principles

- SOLID principles - SRP and DIP encourage orthogonal components
- DRY - avoids duplicated logic that creates hidden coupling
- KISS - simpler systems are naturally more orthogonal

---

## Anti-Patterns

### Anti-Pattern 1: Chain of Dependencies

```typescript
// ❌ High coupling: long chain of dependencies
class A {
  method() {
    const b = new B();
    b.doSomething();
  }
}

class B {
  method() {
    const c = new C();
    c.doSomething();
  }
}

class C {
  method() {
    const d = new D();
    d.doSomething();
  }
}

// Problem: To change D, must go through A → B → C
// To use A separately, need B, C, D
// Change D? Might break A, B, C

// ✅ Fix: Inject dependencies explicitly
class A {
  constructor(private b: B) {}
  method() { this.b.doSomething(); }
}

class B {
  constructor(private c: C) {}
  method() { this.c.doSomething(); }
}

class C {
  constructor(private d: D) {}
  method() { this.d.doSomething(); }
}
```

### Anti-Pattern 2: Circular Dependencies

```typescript
// ❌ High coupling: circular dependency
// User.ts
import { Department } from './Department';
class User {
  department: Department;
}

// Department.ts
import { User } from './User';
class Department {
  users: User[];
}

// Problem: Neither can exist independently
// Circular dependency is sign of poor design

// ✅ Fix: Create interface to break cycle
// Entity.ts
export interface Entity {
  id: string;
}

// User.ts
import { Entity } from './Entity';
export interface User extends Entity {
  departmentId: string;  // Reference, not import
}

// Department.ts
import { Entity } from './Entity';
export interface Department extends Entity {
  userIds: string[];  // References, not imports
}
```

### Anti-Pattern 3: Shared Mutable State

```typescript
// ❌ High coupling: shared mutable state
const globalState = {
  user: null,
  config: {},
  cache: {}
};

class UserService {
  getUser() {
    globalState.user = db.fetchUser();  // Shared state!
  }
}

class EmailService {
  send() {
    const user = globalState.user;  // Depends on global state
  }
}

// Problem: Services depend on global state
// Change globalState? Affects everything
// Hard to test: can't isolate services

// ✅ Fix: Pass state explicitly
class UserService {
  getUser(): User {
    return db.fetchUser();  // Return value, don't share state
  }
}

class EmailService {
  send(user: User) {  // Receive user as parameter
    // No hidden dependencies
  }
}
```

### Anti-Pattern 4: God Objects

```typescript
// ❌ High coupling: god object knows/does everything
class Application {
  createUser() { }
  getUser() { }
  updateUser() { }
  processPayment() { }
  refund() { }
  sendEmail() { }
  query() { }
  save() { }
  authorize() { }
  log() { }
  // 100+ methods, 2000+ lines
}

// Problem: One huge class doing everything
// To use one feature, depend on everything else

// ✅ Fix: Split into focused components
class UserService { }
class PaymentService { }
class EmailService { }
class Database { }
class AuthService { }
class Logger { }
```

### Anti-Pattern 5: Hidden Dependencies

```typescript
// ❌ High coupling: hidden dependencies
class OrderService {
  processOrder(orderId: string) {
    const order = db.getOrder(orderId);  // Hidden dependency
    Payment.process(order.amount);       // Hidden global
    Email.send(order.customer.email);    // Hidden global
    return order;
  }
}

// Problem: Dependencies hidden in method body
// Can't tell what OrderService needs
// Can't mock dependencies easily

// ✅ Fix: Make dependencies explicit
class OrderService {
  constructor(
    private db: Database,
    private payment: PaymentService,
    private email: EmailService
  ) {}

  processOrder(orderId: string) {
    const order = this.db.getOrder(orderId);
    this.payment.process(order.amount);
    this.email.send(order.customer.email);
    return order;
  }
}
```

### Anti-Pattern 6: Inappropriate Intimacy

```typescript
// ❌ High coupling: inappropriate access to internals
class UserRepository {
  private users = [];
}

class UserService {
  // Knows internals of UserRepository
  addUser(user) {
    userRepo.users.push(user);  // Should use method
  }

  getUser(id) {
    return userRepo.users.find(u => u.id === id);  // Direct access
  }
}

// Problem: Changes to internal structure break external code

// ✅ Fix: Use public methods only
class UserRepository {
  private users = [];

  add(user: User): void {
    this.users.push(user);
  }

  findById(id: string): User | null {
    return this.users.find(u => u.id === id) || null;
  }
}

class UserService {
  addUser(user: User) {
    this.repo.add(user);  // Use public method
  }

  getUser(id: string) {
    return this.repo.findById(id);  // Use public method
  }
}
```

---

## Measuring Orthogonality

### Questions to Ask

1. **Isolation**: Can I understand this component without understanding others?
2. **Reuse**: Can I use this component in a different project?
3. **Testing**: Can I test this without other components?
4. **Change**: If I change this, how many others are affected?
5. **Dependencies**: Are dependencies explicit or hidden?

### Red Flags for Poor Orthogonality

- "I need to understand module X to understand module Y"
- "Change in one module breaks another unrelated module"
- "Can't test this without spinning up the whole system"
- "There are circular dependencies"
- "Global state is modified everywhere"
- "Methods reference globals instead of parameters"

---

## Why Orthogonality Matters

✅ **Easier Changes** - Modify one component without affecting others
✅ **Better Testing** - Test components independently
✅ **Simpler Debugging** - Problem is isolated to one component
✅ **Component Reuse** - Use components in different contexts
✅ **Team Scaling** - Team members can work on different components
✅ **Parallel Development** - Teams don't block each other

Master orthogonality, and your system becomes more flexible, testable, and maintainable. Each component becomes a building block that can be understood, modified, and reused independently.
