# Code Smell: Dead Code

**Purpose**: Identify and remove unreachable or unused code
**Audience**: You + AI (code review, refactoring)
**Category**: Dispensables (Unnecessary Code)
**Severity**: 🟢 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Dead Code** is code that's never executed or used anywhere in the codebase.

This includes unreachable code paths, unused methods, properties that are never read, and deprecated functions that haven't been removed.

### Why It Matters

Dead code causes:
- ❌ Confuses readers (why is this here?)
- ❌ Increases maintenance burden
- ❌ Makes refactoring harder
- ❌ Takes up mental load
- ❌ Easy to forget what it was for

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Dead code everywhere
class UserService {
  // Method never called (unreachable)
  @deprecated
  oldGetUser(id: string): User {
    // This method is never called
    // Left for "backward compatibility" but nobody uses old API
    return this.users.find(u => u.id === id);
  }

  // Property never read
  internalCounter: number = 0;  // Never read or used

  // Dead condition
  validateUser(user: User): boolean {
    if (false) {  // Always false
      // This code never runs
      console.log('Validating premium users...');
    }
    return user.isValid();
  }

  // Dead method never called
  private calculateCommission(): number {
    // Never called, not used anywhere
    return this.salary * 0.1;
  }
}

// Users of service
const service = new UserService();
const user = service.getUser('123');  // Only method called
// oldGetUser, internalCounter, validateUser's dead condition, calculateCommission never used
```

**Symptoms**:
- [ ] Methods with @deprecated decorator not removed
- [ ] Code after return/throw statement
- [ ] If conditions that are always true/false
- [ ] Properties/variables never read
- [ ] Methods never called
- [ ] Entire classes that are never instantiated
- [ ] Switch cases that are unreachable

---

## 💔 Why It's Bad

### Problem 1: Confuses Readers

```typescript
// ❌ Dead code raises questions
function processUser(user: User) {
  const temp = user.email;  // ← This is never used!
  const fullName = user.firstName + ' ' + user.lastName;
  sendWelcomeEmail(user.email);
  return fullName;
}

// Reader: Why is `temp` assigned but not used?
// Is it a bug? Should I use it?
// Wasting mental energy
```

### Problem 2: Hard to Maintain

```typescript
// ❌ Multiple code paths to maintain
function calculatePrice(order: Order, isPreview: boolean) {
  if (isPreview) {
    // Old preview logic (never used anymore)
    return this.legacyCalculatePrice(order);
  } else {
    // Current logic
    return this.calculateCurrentPrice(order);
  }

  // If you fix a bug, fix it in both places?
  // Or is one dead?
  // Unclear!
}

// Later, someone tries to refactor:
// Do I need to maintain legacyCalculatePrice?
// Is it used anywhere?
// Can't tell!
```

### Problem 3: Difficult to Refactor

```typescript
// ❌ Dead code prevents refactoring
class OldUserManager {
  // Old API (dead)
  getUser(id: string) { }

  // Old API (dead)
  createUser(email: string) { }

  // New API (used)
  findUserById(id: string) { }

  // New API (used)
  registerUser(email: string, password: string) { }
}

// Can I delete getUser and createUser?
// Are they used in external code?
// Don't know without searching
// Risky!
```

---

## ✅ Refactoring Solutions

### Solution 1: Delete It

```typescript
// ❌ BEFORE: Dead method
class UserService {
  getCurrentUser(): User {
    return this.user;
  }

  // Never called
  getLegacyUser(): User {
    return this.legacyUser;
  }
}

// ✅ AFTER: Delete dead method
class UserService {
  getCurrentUser(): User {
    return this.user;
  }
}

// If it's needed, it's in git history
```

### Solution 2: Remove Unreachable Code

```typescript
// ❌ BEFORE: Code after return
function processOrder(order: Order) {
  if (order.isValid()) {
    return this.completeOrder(order);
  }
  return null;

  // This code never runs
  console.log('Logging order...');
  sendConfirmation(order);
}

// ✅ AFTER: Remove unreachable code
function processOrder(order: Order) {
  if (order.isValid()) {
    return this.completeOrder(order);
  }
  return null;
}

// Dead code deleted
```

### Solution 3: Remove Dead Conditions

```typescript
// ❌ BEFORE: Always true/false
function calculateDiscount(user: User) {
  if (true) {  // Always true!
    return user.loyalty * 0.1;
  }

  // Never reached
  return 0;
}

// ✅ AFTER: Remove dead condition
function calculateDiscount(user: User) {
  return user.loyalty * 0.1;
}

// Clearer what always happens
```

### Solution 4: Properly Deprecate (If Public API)

```typescript
// ❌ BEFORE: Just left in code
class API {
  oldMethod() {
    // This is never called
    // But external code might use it
  }
}

// ✅ AFTER: Properly deprecate
class API {
  @deprecated('Use newMethod() instead. Will be removed in v3.0')
  oldMethod() {
    return this.newMethod();
  }

  newMethod() {
    // Real implementation
  }
}

// Users see warning
// Have time to migrate
// Then delete in future version
```

### Solution 5: Move to Archive

```typescript
// ❌ BEFORE: Dead code in main codebase
class Order {
  // Current logic
  calculateTotal(): number { }

  // Old calculation logic (never used)
  calculateTotalLegacy(): number { }

  // Old calculation logic (never used)
  calculateTotalOld(): number { }
}

// ✅ AFTER: Move to archive if historical interest
// archive/order-calculations-v1.ts
class OrderLegacy {
  calculateTotal(): number { }  // v1 implementation
  calculateTotalOld(): number { }  // v0 implementation
}

// Current file stays clean
// History is available if needed
```

---

## 🔍 Finding Dead Code

**Tools help identify**:
- IDEs: "Find Usages" shows if method/property is used
- Linters: Detect unused variables
- Code coverage: Shows which code paths run
- Grep: Search for method calls to find usage

```bash
# Find unused methods
grep -r "oldMethod" src/  # If no results, it's dead

# Find unused variables (in TypeScript)
# tslint/eslint rules for "no-unused-variables"
```

---

## 📚 Relationship to Core Principles

- **DRY Principle** - Dead code is waste
- **ETC (Easier To Change)** - Dead code makes changes harder
- **Small Steps** - Remove dead code incrementally

---

## ✅ Checklist: Avoid Dead Code

When refactoring:

- [ ] Is this code actually used?
- [ ] Can I find any callers?
- [ ] Is this method in public API?
- [ ] Should I deprecate rather than delete?
- [ ] Should I move to archive/history?

---

## ✨ Remember

**DON'T DO**: Leave dead code hoping it might be useful.

**DO**: Delete unused code; it's in git history if needed.

**Rule of thumb**: If code isn't used, delete it. Version control preserves history.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-dead-code.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Delete dead code. Version control keeps the history.**
