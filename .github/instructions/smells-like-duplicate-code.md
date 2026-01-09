# Code Smell: Duplicate Code

**Purpose**: Identify and avoid duplicated code logic
**Audience**: You + AI (code review, refactoring)
**Category**: Dispensables (Unnecessary Code)
**Severity**: 🔴 HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Duplicate Code** occurs when the same logic appears in multiple places in your codebase.

The same code block, function, or logic is copied and pasted rather than extracted into a shared location.

### Why It Matters

Duplicate code violates the **DRY principle** (Don't Repeat Yourself):
- ❌ When you need to fix a bug, you must fix it in multiple places
- ❌ When you need to change behavior, you must change it everywhere
- ❌ Easy to miss one copy, creating inconsistencies
- ❌ Maintenance cost multiplies with each duplicate
- ❌ Code size increases unnecessarily

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Exact code duplication
function validateUserEmail(email: string) {
  if (!email.includes('@')) return false;
  if (email.length < 5) return false;
  return true;
}

function validateAdminEmail(email: string) {
  if (!email.includes('@')) return false;
  if (email.length < 5) return false;
  return true;
}

function validateContactEmail(email: string) {
  if (!email.includes('@')) return false;
  if (email.length < 5) return false;
  return true;
}

// Same validation logic in 3 places!
```

**Symptoms**:
- [ ] Same code block in 2+ functions
- [ ] Copy-paste code visible in commit history
- [ ] Similar class structures with identical methods
- [ ] Same SQL queries in multiple repositories
- [ ] Identical HTML/JSX templates
- [ ] Same test setup code repeated
- [ ] Identical configuration logic
- [ ] Same error handling in multiple places

### Detection Tools

```bash
# Find duplicate code patterns
git log -p | grep -A5 -B5 "duplicate pattern"

# Code duplication analyzers
npm install --save-dev jscpd          # JavaScript
pylint --duplicate-code-check         # Python
sonar-scanner                         # Multi-language
```

---

## 💔 Why It's Bad

### Problem 1: Maintenance Burden

```typescript
// Original validation logic in 3 places
// Requirement: "Email must include a domain"

// Change 1:
function validateUserEmail(email: string) {
  const hasAt = email.includes('@');
  const hasDomain = email.split('@')[1]?.length > 0;
  return hasAt && hasDomain && email.length > 5;
}

// Change 2: (forgot this one!)
function validateAdminEmail(email: string) {
  if (!email.includes('@')) return false;
  if (email.length < 5) return false;
  return true;
  // ❌ Not updated! Bug created!
}

// Change 3:
function validateContactEmail(email: string) {
  const hasAt = email.includes('@');
  const hasDomain = email.split('@')[1]?.length > 0;
  return hasAt && hasDomain && email.length > 5;
}

// Now we have inconsistent validation across the system
```

### Problem 2: Code Size Explosion

```
Original: 50 lines of validation logic
Duplicated 5 times: 250 lines
Maintenance cost: 5x higher
Testing cost: 5x higher
Bug fix cost: 5x higher
```

### Problem 3: Inconsistency Risk

```typescript
// Same logic, slightly different implementation
// User validation
if (user.email.includes('@') && user.email.length > 5) {
  // valid
}

// Admin validation
const emailValid = user.email.indexOf('@') !== -1 && user.email.length >= 5;
if (emailValid) {
  // valid
}

// Contact validation
const parts = user.email.split('@');
if (parts.length === 2 && user.email.length > 5) {
  // valid
}

// Three implementations of the same rule!
// One has a bug, one is correct, one is different
// Inconsistent behavior across system
```

### Problem 4: Harder to Find & Fix Bugs

```
Bug: Email validation accepts "a@"
Location: validateUserEmail() line 45

Fix there. But did you also fix it in:
- validateAdminEmail()?
- validateContactEmail()?
- validateNotificationEmail()?
- validatePaymentEmail()?
- validateSupportEmail()?
- validateAPIKeyEmail()?

Easy to miss 2-3 locations. Creates support tickets.
```

---

## ✅ Refactoring Solutions

### Solution 1: Extract Function

```typescript
// ✅ FIXED: Single source of truth

function validateEmail(email: string): boolean {
  return email.includes('@') && email.length > 5;
}

// Use everywhere
const userValid = validateEmail(userEmail);
const adminValid = validateEmail(adminEmail);
const contactValid = validateEmail(contactEmail);

// Change validation once → all uses update automatically
```

### Solution 2: Extract Shared Module

```typescript
// validation/email-validator.ts
export class EmailValidator {
  validate(email: string): boolean {
    const hasAt = email.includes('@');
    const hasLength = email.length > 5;
    const hasDomain = email.split('@')[1]?.length > 0;
    return hasAt && hasLength && hasDomain;
  }
}

// user/user-service.ts
import { EmailValidator } from '../validation/email-validator';
export class UserService {
  constructor(private emailValidator: EmailValidator) {}

  createUser(email: string) {
    if (!this.emailValidator.validate(email)) {
      throw new Error('Invalid email');
    }
    // ...
  }
}

// admin/admin-service.ts
import { EmailValidator } from '../validation/email-validator';
export class AdminService {
  constructor(private emailValidator: EmailValidator) {}

  createAdmin(email: string) {
    if (!this.emailValidator.validate(email)) {
      throw new Error('Invalid email');
    }
    // ...
  }
}

// Single validation logic, used everywhere
```

### Solution 3: Utility Library

```typescript
// utils/validators.ts
export const validators = {
  email: (email: string) => email.includes('@') && email.length > 5,
  phone: (phone: string) => /^\d{3}-\d{4}$/.test(phone),
  password: (pwd: string) => pwd.length >= 8,
  url: (url: string) => url.startsWith('http'),
};

// Usage
if (validators.email(email)) { /* ... */ }
if (validators.phone(phone)) { /* ... */ }
if (validators.password(password)) { /* ... */ }
```

### Solution 4: Configuration-Driven

```typescript
// config/validation.ts
const ValidationRules = {
  email: {
    required: true,
    pattern: /.+@.+\..+/,
    minLength: 5,
  },
  phone: {
    required: true,
    pattern: /^\d{3}-\d{4}$/,
  },
  password: {
    required: true,
    minLength: 8,
  },
};

// Generic validator
function validate(value: string, rules: any): boolean {
  if (rules.required && !value) return false;
  if (rules.pattern && !rules.pattern.test(value)) return false;
  if (rules.minLength && value.length < rules.minLength) return false;
  return true;
}

// Use for all validation
validate(email, ValidationRules.email);
validate(phone, ValidationRules.phone);
validate(password, ValidationRules.password);
```

### Solution 5: Template Pattern (for larger duplicates)

```typescript
// ❌ Duplicate database query logic
class UserRepository {
  getUser(id: string) {
    const result = db.query('SELECT * FROM users WHERE id = ?', [id]);
    if (!result) throw new Error('Not found');
    return new User(result);
  }
}

class ProductRepository {
  getProduct(id: string) {
    const result = db.query('SELECT * FROM products WHERE id = ?', [id]);
    if (!result) throw new Error('Not found');
    return new Product(result);
  }
}

// ✅ Fixed: Extract to base class
abstract class BaseRepository<T> {
  protected abstract tableName: string;
  protected abstract createEntity(row: any): T;

  get(id: string): T {
    const result = db.query(`SELECT * FROM ${this.tableName} WHERE id = ?`, [id]);
    if (!result) throw new Error('Not found');
    return this.createEntity(result);
  }
}

class UserRepository extends BaseRepository<User> {
  protected tableName = 'users';
  protected createEntity(row: any) { return new User(row); }
}

class ProductRepository extends BaseRepository<Product> {
  protected tableName = 'products';
  protected createEntity(row: any) { return new Product(row); }
}

// Logic in one place, specific implementations separate
```

---

## 🔍 When It Might Be OK

### Exception 1: Different Domains

```typescript
// ✓ OK: Different domains, similar logic
// user/validation/email.ts
function validateUserEmail(email) {
  // User-specific validation
  return email.includes('@') && email.length > 5 && !email.includes(' ');
}

// payment/validation/email.ts
function validatePaymentEmail(email) {
  // Payment-specific validation
  return email.includes('@') && email.length > 10;
}

// Different rules, even though both check '@'
// Extract common parts only
```

### Exception 2: Very Short Code

```typescript
// ✓ OK: Too short to extract, common pattern
const min = (a, b) => a < b ? a : b;
const max = (a, b) => a > b ? a : b;

// Simple enough that extracting is overkill
```

### Exception 3: Auto-Generated Code

```typescript
// ✓ OK: Generated by tool, not hand-duplicated
// generated/api-client-v1.ts (auto-generated from OpenAPI)
// generated/api-client-v2.ts (auto-generated from OpenAPI)

// Don't manually deduplicate auto-generated code
// Fix the generator instead
```

---

## 🔄 Detection Workflow

### Step 1: Recognize Duplication

```typescript
// ❌ Pattern spotted: validation code repeated
// File 1: user.service.ts line 45
// File 2: admin.service.ts line 32
// File 3: contact.service.ts line 78
```

### Step 2: Assess Impact

```
- How many places duplicated? (3)
- How often will it change? (Frequently)
- How hard to extract? (Easy)
→ Severity: HIGH - EXTRACT IMMEDIATELY
```

### Step 3: Choose Solution

```
Duplication type: Validation logic
Complexity: Simple (5 lines)
Scope: Multiple services
Solution: Extract to shared function
Effort: 30 minutes
```

### Step 4: Extract & Verify

```
1. Create shared function
2. Update all locations to use it
3. Run tests
4. Delete old code
5. Verify behavior unchanged
```

---

## 📊 Duplication Levels

| Level | Example | Action |
|-------|---------|--------|
| **2 occurrences** | Same logic in 2 files | Extract immediately |
| **3+ occurrences** | Same logic in 3+ files | Definitely extract |
| **Similar patterns** | 80% same, 20% different | Extract common, parameterize difference |
| **Generated code** | From OpenAPI, protobuf, etc | Fix generator, not code |

---

## 📚 Relationship to Core Principles

- **DRY Principle** - Duplicate code violates DRY (write once, link everywhere)
- **Small Steps** - Extract small duplications incrementally
- **SOLID-S** - Duplication often indicates mixing concerns
- **Refactoring Techniques** - Extract Function solves duplication
- **Quality Patterns** - Anti-pattern that hurts maintainability

---

## ✅ Checklist: Avoid Duplicate Code

When writing code:

- [ ] Is this logic used elsewhere?
- [ ] Could I extract this to a shared location?
- [ ] Would extraction make maintenance easier?
- [ ] Is the code complex enough to extract? (>5 lines)
- [ ] Can I make the extraction generic/parameterized?
- [ ] Have I tested after extraction?
- [ ] Do all uses behave identically?
- [ ] Is the extracted function well-named?
- [ ] Could I eliminate this duplication?

---

## ✨ Remember

**DON'T DO**: Duplicate the same code logic in multiple places.

**DO**: Extract logic to a single location and reference it everywhere.

**Cost of duplication**: Maintenance burden multiplies with each copy.

**Cost of extraction**: One-time effort, forever savings.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells/smells-like-duplicate-code.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Don't duplicate. Extract once. Use everywhere.**
