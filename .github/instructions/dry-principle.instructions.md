---
description: 'Every piece of knowledge must have a single, authoritative representation'
applyTo: '**/*'
---

# DRY Principle - Don't Repeat Yourself

## Overview

DRY (Don't Repeat Yourself) is a fundamental principle that states: every piece of knowledge must have a single, unambiguous, authoritative representation within a system. When the same information appears in multiple places, maintaining consistency becomes exponentially harder. This principle applies to code, documentation, configuration, data definitions, and all forms of system knowledge.

The DRY principle ensures:

- Single source of truth for every fact
- Change once, everywhere updated automatically
- Perfect consistency across the system
- Reduced maintenance burden
- Fewer bugs from inconsistent updates
- Easier debugging and tracing

## Core Concepts

### 1. Code Duplication

**Problem**: Same logic implemented in multiple places

```typescript
// ❌ DRY violation: code duplicated
function validateUserEmail(email: string): boolean {
  return email.includes('@') && email.length > 5;
}

function validateAdminEmail(email: string): boolean {
  return email.includes('@') && email.length > 5;
}

function validateContactEmail(email: string): boolean {
  return email.includes('@') && email.length > 5;
}

// Change validation rule → must update 3 places
// Miss one place? Inconsistency bug
```

**Solution**: Extract to single function, reference everywhere

```typescript
// ✅ DRY: single source of truth
function validateEmail(email: string): boolean {
  return email.includes('@') && email.length > 5;
}

const userEmail = validateEmail(email);
const adminEmail = validateEmail(email);
const contactEmail = validateEmail(email);

// Change validation → update one function
// All usages get the new behavior automatically
```

---

### 2. Documentation Duplication

**Problem**: Same information in multiple documents

```text
❌ DRY violation:
- README.md has installation steps
- CONTRIBUTING.md has installation steps
- docs/setup.md has installation steps
- docs/getting-started.md has installation steps

Change installation? Update 4 places. Miss one? Outdated docs.
```

**Solution**: Single source document, others link to it

```text
✅ DRY: single source of truth
- docs/installation.md (authoritative source)
- README.md → "See docs/installation.md for setup"
- CONTRIBUTING.md → "See docs/installation.md for setup"
- docs/getting-started.md → "See docs/installation.md"

Change installation? Update docs/installation.md once.
Everyone links to the current version.
```

---

### 3. Configuration Duplication

**Problem**: Same settings in multiple config files

```typescript
// ❌ DRY violation: duplicated settings
// config/dev.js
export const MAX_USERS = 100;
export const TIMEOUT = 5000;

// config/test.js
export const MAX_USERS = 100;
export const TIMEOUT = 5000;

// config/prod.js
export const MAX_USERS = 100;
export const TIMEOUT = 5000;

// Change timeout → must update 3 files
// Different configs might diverge
```

**Solution**: Common config with environment-specific overrides

```typescript
// ✅ DRY: single source of truth
// config/defaults.ts
export const config = {
  MAX_USERS: 100,
  TIMEOUT: 5000,
};

// config/dev.ts
import { config } from './defaults';
export default { ...config, DEBUG: true };

// config/test.ts
import { config } from './defaults';
export default { ...config, TIMEOUT: 1000 }; // Override only what differs

// config/prod.ts
import { config } from './defaults';
export default { ...config, LOG_LEVEL: 'error' };

// Change MAX_USERS? Update config/defaults.ts
// All environments inherit the change
```

---

### 4. Data Definition Duplication

**Problem**: Same data structure defined in multiple places

```typescript
// ❌ DRY violation: duplicated types
// frontend/User.ts
interface User {
  id: string;
  email: string;
  name: string;
  age: number;
}

// backend/models/user.ts
interface User {
  id: string;
  email: string;
  name: string;
  age: number;
}

// database/schema.sql
CREATE TABLE users (
  id VARCHAR(36),
  email VARCHAR(100),
  name VARCHAR(100),
  age INT
);

// Change User structure → update 3 places
// Database and code might get out of sync
```

**Solution**: Single schema definition, import everywhere

```typescript
// ✅ DRY: single source of truth
// shared/User.ts (authoritative)
export interface User {
  id: string;
  email: string;
  name: string;
  age: number;
}

// frontend/types.ts
export { User } from '../shared/User';

// backend/models.ts
export { User } from '../shared/User';

// database/migrations/001_create_users.ts
// Generated from User interface, validates schema matches

// Change User? Update shared/User.ts
// Database migrations and code both use current definition
```

---

### 5. Knowledge Duplication

**Problem**: Same knowledge in comments, documentation, and code

```typescript
// ❌ DRY violation: knowledge scattered
function f(items, threshold) {
  // This filters items (comment)
  // No clear name
  // Documentation somewhere else
  // Tests don't show intent
  return items.filter(item => item.value > threshold);
}
```

**Solution**: Clear intent in code, reference external docs

```typescript
// ✅ DRY: single source of truth
function filterHighValueItems(
  items: Item[],
  threshold: number
): Item[] {
  // Name explains what it does
  // Implementation is clear
  // Why? See: docs/filtering-rules.md
  return items.filter(item => item.value > threshold);
}

// Tests show intent
describe('filterHighValueItems', () => {
  test('returns items with value > threshold', () => {
    // Test behavior, not explanation
  });
});
```

---

## Application Checklist

When writing code, configuration, or documentation:

- [ ] Is this information already defined somewhere else?
- [ ] Should I extract this to a shared function/module?
- [ ] Could I import this definition instead of duplicating?
- [ ] Is this configuration hardcoded instead of centralized?
- [ ] Is this documentation repeated in multiple places?
- [ ] Can I link to one authoritative source instead?
- [ ] Would future changes require updating this in multiple places?
- [ ] Can I use constants instead of magic numbers?
- [ ] Can I generate code from a single definition?

### When Refactoring for DRY

1. **Identify Duplication**: Find all instances of repeated code/knowledge
2. **Extract to One Place**: Create single source of truth
3. **Reference Everywhere**: Import/link/reference the single source
4. **Verify Consistency**: Ensure all usages get the same behavior
5. **Update Tests**: Tests should reference the single source too

### When Designing New Code

1. **Check Existing Code**: Does this logic already exist?
2. **Use Shared Modules**: Import instead of duplicate
3. **Centralize Configuration**: Extract magic numbers to config
4. **Link Documentation**: Reference instead of duplicate
5. **Plan for Change**: How will changing this affect other parts?

---

## Related Principles

- SOLID principles - DRY reduces duplicated logic across modules
- KISS - DRY helps keep systems simple by centralizing logic
- Design by Contract - DRY helps keep contracts consistent across code and tests

---

## Anti-Patterns

### Anti-Pattern 1: Copy-Paste Code

```typescript
// ❌ Copy-paste is the #1 DRY violation
function processUserPayment(userId, amount) {
  const user = db.getUser(userId);
  if (!user) throw new Error('User not found');
  if (amount <= 0) throw new Error('Invalid amount');

  const receipt = {
    userId,
    amount,
    date: new Date(),
    type: 'payment'
  };

  db.saveReceipt(receipt);
  emailService.send(user.email, `Payment of $${amount} received`);
}

function processRefund(userId, amount) {
  const user = db.getUser(userId);
  if (!user) throw new Error('User not found');
  if (amount <= 0) throw new Error('Invalid amount');

  const receipt = {
    userId,
    amount,
    date: new Date(),
    type: 'refund'  // Only difference!
  };

  db.saveReceipt(receipt);
  emailService.send(user.email, `Refund of $${amount} issued`);
}

// Problem: 95% of code is identical
// Change validation? Update 2 places. Miss one? Bug.

// ✅ Fix: Extract common logic
function processTransaction(userId, amount, type, message) {
  const user = db.getUser(userId);
  if (!user) throw new Error('User not found');
  if (amount <= 0) throw new Error('Invalid amount');

  const receipt = { userId, amount, date: new Date(), type };
  db.saveReceipt(receipt);
  emailService.send(user.email, message);
}

function processUserPayment(userId, amount) {
  return processTransaction(
    userId,
    amount,
    'payment',
    `Payment of $${amount} received`
  );
}

function processRefund(userId, amount) {
  return processTransaction(
    userId,
    amount,
    'refund',
    `Refund of $${amount} issued`
  );
}
```

### Anti-Pattern 2: Multiple Documentation Sources

```text
❌ Which one is correct?
- User's Guide Version 1 (outdated)
- User's Guide Version 2 (different info)
- Wiki (different info)
- README (different info)
- Code comment (different info)
- Developer "tribal knowledge" (only in heads)

All different! Impossible to maintain.

✅ Solution:
- docs/api.md (authoritative source)
- README.md → links to docs/api.md
- Wiki → links to docs/api.md
- Code comments → link to docs/api.md
- Team shares docs/api.md
```

### Anti-Pattern 3: Hardcoded Magic Numbers

```typescript
// ❌ Magic number appears in many places
if (user.age >= 18) { /* ... */ }
if (customer.age >= 18) { /* ... */ }
if (visitor.age >= 18) { /* ... */ }

// What is 18? Why? If it changes to 21 → find all places!

// ✅ Solution: Centralize
const LEGAL_AGE = 18;

if (user.age >= LEGAL_AGE) { /* ... */ }
if (customer.age >= LEGAL_AGE) { /* ... */ }
if (visitor.age >= LEGAL_AGE) { /* ... */ }

// Change legal age? Update one constant
```

### Anti-Pattern 4: Database-Code Mismatch

```typescript
// ❌ Schema and code out of sync
// Database has 'created_at', code expects 'createdAt'
// Database requires 'email', code doesn't validate
// Code has field 'role', database doesn't have it

// Leads to:
// - Runtime errors (unexpected null values)
// - Data inconsistency
// - Hard to debug

// ✅ Solution: Single source definition
// User.ts (shared)
export interface User {
  id: string;
  email: string;
  createdAt: Date;
}

// Database migration validates against User.ts
// API validators use User.ts
// Frontend form uses User.ts
// All stay in sync
```

### Anti-Pattern 5: Similar But Different Logic

```typescript
// ❌ Almost the same logic, but slightly different
class ActiveUserFilter {
  filter(users) {
    return users.filter(
      u => u.status === 'active' && u.lastLogin > 30DaysAgo
    );
  }
}

class PremiumUserFilter {
  filter(users) {
    return users.filter(
      u => u.status === 'active' &&
           u.lastLogin > 30DaysAgo &&
           u.isPremium
    );
  }
}

// Shared logic duplicated
// Change the shared part → update 2 places

// ✅ Solution: Extract shared logic
function isRecentlyActive(user) {
  return user.status === 'active' && user.lastLogin > 30DaysAgo;
}

class ActiveUserFilter {
  filter(users) {
    return users.filter(user => isRecentlyActive(user));
  }
}

class PremiumUserFilter {
  filter(users) {
    return users.filter(
      user => isRecentlyActive(user) && user.isPremium
    );
  }
}

// Shared logic in one place
```

---

## DRY Techniques

### Technique 1: Extract Function

```typescript
// Before: Logic repeated
if (user.status === 'active' && user.credits > 0 && !user.banned) {
  // User is eligible
}

if (customer.status === 'active' && customer.credits > 0 && !customer.banned) {
  // Customer is eligible
}

// After: Extract to function
function isEligible(actor: { status: string; credits: number; banned: boolean }): boolean {
  return actor.status === 'active' && actor.credits > 0 && !actor.banned;
}

if (isEligible(user)) { /* ... */ }
if (isEligible(customer)) { /* ... */ }
```

### Technique 2: Shared Module

```typescript
// shared/validation.ts
export const rules = {
  email: (email: string) => email.includes('@'),
  password: (pwd: string) => pwd.length >= 8,
  username: (name: string) => name.length >= 3,
};

// userService.ts
import { rules } from './shared/validation';
if (!rules.email(email)) throw new Error('Invalid email');

// adminService.ts
import { rules } from './shared/validation';
if (!rules.email(email)) throw new Error('Invalid email');

// Change email rule? Update shared/validation.ts once
```

### Technique 3: Inheritance/Generics

```typescript
// Before: Definition repeated
class UserRepository {
  getUser(id) { /* ... */ }
  saveUser(user) { /* ... */ }
}

class AdminRepository {
  getAdmin(id) { /* ... */ }
  saveAdmin(admin) { /* ... */ }
}

// After: Single generic base class
abstract class BaseRepository<T> {
  get(id: string): T { /* ... */ }
  save(item: T): void { /* ... */ }
}

class UserRepository extends BaseRepository<User> {}
class AdminRepository extends BaseRepository<Admin> {}
```

### Technique 4: Template/Scaffolding

```typescript
// Before: Boilerplate repeated
class UserService {
  constructor(private db: Database) {}
  async getAll() { /* ... */ }
  async getById(id) { /* ... */ }
  async create(data) { /* ... */ }
}

class ProductService {
  constructor(private db: Database) {}
  async getAll() { /* ... */ }
  async getById(id) { /* ... */ }
  async create(data) { /* ... */ }
}

// After: Generic base
abstract class BaseService<T> {
  constructor(protected db: Database, protected table: string) {}
  async getAll(): Promise<T[]> { /* ... */ }
  async getById(id: string): Promise<T> { /* ... */ }
  async create(data: Partial<T>): Promise<T> { /* ... */ }
}

class UserService extends BaseService<User> {
  constructor(db: Database) { super(db, 'users'); }
}

class ProductService extends BaseService<Product> {
  constructor(db: Database) { super(db, 'products'); }
}
```

### Technique 5: Configuration Over Hardcoding

```typescript
// Before: Values scattered
if (user.age < 18) { /* ... */ }
if (users.length >= 1000) { /* ... */ }
setTimeout(() => { /* ... */ }, 5000);

// After: Centralized
const config = {
  MIN_AGE: 18,
  MAX_USERS: 1000,
  TIMEOUT_MS: 5000,
};

if (user.age < config.MIN_AGE) { /* ... */ }
if (users.length >= config.MAX_USERS) { /* ... */ }
setTimeout(() => { /* ... */ }, config.TIMEOUT_MS);
```

---

## Why DRY Matters

✅ **Maintenance Efficiency** - Change once, everywhere updated
✅ **Consistency** - No diverging copies
✅ **Bug Prevention** - Fewer places to make mistakes
✅ **Onboarding** - New team members find the single source
✅ **Scalability** - Works even with 100+ files/locations
✅ **Testing** - Test one place, confidence everywhere

## DRY in Practice

The goal: When you update a fact once, the entire system reflects that change.

Key insight: DRY is about knowledge, not code lines. If something appears in 2 places and you maintain both, that's DRY violation—even if they're different implementations.

Master DRY, and your codebase becomes easier to evolve, maintain, and scale.
