# Core Principle: Refactoring Techniques

**Purpose**: Common patterns for improving code structure and maintainability
**Audience**: You + AI (refactoring tasks, code improvement)
**Focus**: 5 essential refactoring techniques with when and how to apply

---

## 🎯 What is Refactoring?

Refactoring is: **Improve code structure without changing its behavior**.

Essential techniques:
1. Extract Function
2. Extract Class/Module
3. Simplify Conditionals
4. Use Async/Await
5. Dependency Injection

**Core Idea**: These 5 techniques solve 90% of refactoring needs.

---

## 🔑 Technique 1: Extract Function

**Purpose**: Break complex logic into smaller functions

**When to use**:
- Multiple lines doing one thing
- Code is repeated (copy-paste)
- Function is too long (>50 lines)
- Logic is hard to understand

**How it works**:
1. Identify logical block
2. Extract into new function
3. Replace original with function call
4. Test still works

### Example - Extract Function

**Before** (Too much in one function):
```typescript
function processUser(user) {
  // Format name (3 lines)
  const name = user.firstName + ' ' + user.lastName;

  // Format email (2 lines)
  const email = user.email.toLowerCase();

  // Create object (2 lines)
  const formatted = { name, email };

  return formatted;
}
```

**After** (Extract logical blocks):
```typescript
function formatUserEmail(email: string): string {
  return email.toLowerCase();
}

function getFullName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}

function processUser(user) {
  const name = getFullName(user);
  const email = formatUserEmail(user.email);
  return { name, email };
}
```

**Benefits**:
- ✅ Each function does one thing
- ✅ Functions are reusable (formatUserEmail used elsewhere)
- ✅ Easy to test individually
- ✅ Clear what each step does

---

## 🔑 Technique 2: Extract Class / Module

**Purpose**: Break responsibilities into separate classes

**When to use**:
- Class has too many responsibilities
- Multiple reasons to change same class
- Group of methods belong together
- Related data scattered across class

**How it works**:
1. Identify responsibility to extract
2. Create new class for that responsibility
3. Move methods and data
4. Replace with instance of new class

### Example - Extract Class

**Before** (Too many responsibilities):
```typescript
// ❌ UserService does too much
class UserService {
  createUser(email, password) { }
  validateEmail(email) { }
  hashPassword(password) { }
  sendEmail(email, subject, message) { }
  generateToken(userId) { }
  verifyToken(token) { }
}

// 6 different reasons to modify this class!
```

**After** (Responsibilities separated):
```typescript
// ✅ Each class one responsibility
class UserService {
  constructor(
    private validator: EmailValidator,
    private passwordService: PasswordService,
    private emailService: EmailService,
    private tokenService: TokenService
  ) {}

  createUser(email: string, password: string) {
    this.validator.validate(email);
    const hashed = this.passwordService.hash(password);
    // Create user with email and hashed password
  }
}

class EmailValidator {
  validate(email: string): boolean { }
}

class PasswordService {
  hash(password: string): string { }
}

class EmailService {
  send(email: string, subject: string, message: string) { }
}

class TokenService {
  generate(userId: string): string { }
  verify(token: string): boolean { }
}
```

**Benefits**:
- ✅ Each class easier to understand
- ✅ Each class one reason to change
- ✅ Classes reusable in other contexts
- ✅ Easier to test

---

## 🔑 Technique 3: Simplify Conditionals

**Purpose**: Make conditional logic clearer and more readable

**Patterns**:
1. Guard clauses (early return)
2. Extract boolean to variable
3. Convert to switch statement
4. Use polymorphism instead

### Pattern A: Guard Clauses (Early Return)

**Before** (Nested conditions):
```typescript
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.permissions.includes('admin')) {
        return performAdminAction(user);
      } else {
        return performUserAction(user);
      }
    }
  }
  return null;
}
```

**After** (Guard clauses):
```typescript
function processUser(user) {
  // Guard clauses: exit early if conditions not met
  if (!user) return null;
  if (!user.isActive) return null;
  if (!user.permissions.includes('admin')) {
    return performUserAction(user);
  }
  return performAdminAction(user);
}
```

**Benefits**:
- ✅ Clearer flow
- ✅ Less nesting
- ✅ Failures handled first

### Pattern B: Extract Boolean to Variable

**Before** (Conditions hard to read):
```typescript
if (user.age > 18 && user.status === 'active' && user.credits > 100) {
  allowPurchase();
}
```

**After** (Clear intent):
```typescript
const isAdult = user.age > 18;
const isActive = user.status === 'active';
const hasEnoughCredits = user.credits > 100;

if (isAdult && isActive && hasEnoughCredits) {
  allowPurchase();
}
```

**Benefits**:
- ✅ Easy to understand what you're checking
- ✅ Can reuse conditions elsewhere

### Pattern C: Use Polymorphism Instead

**Before** (Type-based conditionals):
```typescript
function calculateBonus(employee) {
  if (employee.type === 'manager') {
    return employee.salary * 0.2;
  } else if (employee.type === 'developer') {
    return employee.salary * 0.15;
  } else if (employee.type === 'designer') {
    return employee.salary * 0.1;
  }
}
```

**After** (Polymorphism):
```typescript
interface Employee {
  calculateBonus(): number;
}

class Manager implements Employee {
  calculateBonus() { return this.salary * 0.2; }
}

class Developer implements Employee {
  calculateBonus() { return this.salary * 0.15; }
}

class Designer implements Employee {
  calculateBonus() { return this.salary * 0.1; }
}

// Usage: same for all types
function giveBonus(employee: Employee) {
  return employee.calculateBonus();
}
```

---

## 🔑 Technique 4: Use Async/Await

**Purpose**: Make asynchronous code clearer and more maintainable

**When to use**:
- Code uses `.then()` chains
- Mixing promises and callbacks
- Error handling gets complex

**How it works**:
- Replace `.then()` chains with await
- Use try/catch for errors
- Code reads top-to-bottom

### Example - Async/Await

**Before** (Promise chains):
```typescript
function deployApp(appId) {
  return fetchApp(appId)
    .then(app => {
      return pullCode(app.repo)
        .then(code => {
          return runMigrations(app.db)
            .then(migrations => {
              return restartService(app.service)
                .then(service => {
                  return verifyDeployment(app.url);
                });
            });
        });
    })
    .catch(error => {
      console.error('Deployment failed:', error);
      return rollback(appId);
    });
}
```

**After** (Async/Await):
```typescript
async function deployApp(appId) {
  try {
    const app = await fetchApp(appId);
    const code = await pullCode(app.repo);
    const migrations = await runMigrations(app.db);
    const service = await restartService(app.service);
    const verified = await verifyDeployment(app.url);
    return verified;
  } catch (error) {
    console.error('Deployment failed:', error);
    return rollback(appId);
  }
}
```

**Benefits**:
- ✅ Reads top-to-bottom like sync code
- ✅ Easier to understand flow
- ✅ Error handling simpler
- ✅ Debugging easier

---

## 🔑 Technique 5: Dependency Injection

**Purpose**: Make dependencies explicit and swappable

**When to use**:
- Class hardcodes dependencies (new Class())
- Hard to test because can't mock
- Need to swap implementations

**How it works**:
1. Add constructor parameter for dependency
2. Store as instance variable
3. Use instance variable instead of creating

### Example - Dependency Injection

**Before** (Hardcoded dependencies):
```typescript
class UserService {
  constructor() {
    this.db = new PostgresDatabase(); // Hardcoded!
    this.mailer = new GmailService(); // Hardcoded!
  }

  createUser(email: string, password: string) {
    this.db.insert({ email, password });
    this.mailer.send(email, 'Welcome!');
  }
}

// Problems:
// - Can't test without actual database and email service
// - Can't swap to MongoDB or different email provider
```

**After** (Dependency injection):
```typescript
class UserService {
  constructor(
    private db: Database,
    private mailer: Mailer
  ) {}

  createUser(email: string, password: string) {
    this.db.insert({ email, password });
    this.mailer.send(email, 'Welcome!');
  }
}

// Usage with real dependencies
const postgres = new PostgresDatabase();
const gmail = new GmailService();
const service = new UserService(postgres, gmail);

// Usage with mocks for testing
const mockDb = { insert: jest.fn() };
const mockMailer = { send: jest.fn() };
const testService = new UserService(mockDb, mockMailer);
testService.createUser('test@example.com', 'pass');
expect(mockDb.insert).toHaveBeenCalled();
```

**Benefits**:
- ✅ Easy to test (inject mocks)
- ✅ Easy to swap implementations
- ✅ Dependencies are explicit
- ✅ Follows Dependency Inversion

---

## ✅ Refactoring Goals

Apply these techniques to achieve:

1. **Clarity**: Code is easy to understand
2. **Maintainability**: Easy to change and extend
3. **Performance**: No unnecessary operations
4. **Testability**: Can be easily tested
5. **Reusability**: Can be reused elsewhere

---

## 🔄 Refactoring Workflow

### When to Refactor
1. Code is hard to understand
2. Same logic repeated (DRY violation)
3. Function/class too long
4. Hard to test
5. New feature requires changing many places

### How to Refactor
```
1. Identify problem (too complex, too big, repeated)
2. Choose technique (extract function, extract class, etc.)
3. Apply refactoring
4. Run tests - should still pass
5. Verify behavior unchanged
6. Done!
```

### What to Check After
- [ ] All tests pass?
- [ ] Behavior unchanged?
- [ ] Code clearer?
- [ ] Performance same or better?
- [ ] No new bugs?

---

## ❌ Anti-Patterns

### Anti-Pattern 1: Premature Extraction
```
❌ Extract function that's only used once (creates noise)
✅ Wait until used twice or logic is complex
```

### Anti-Pattern 2: Extract Without Testing
```
❌ Refactor without running tests
✅ Run tests before and after refactoring
```

### Anti-Pattern 3: Half-Finished Refactoring
```
❌ Extract function but leave related code together
✅ Extract related logic into same function/class
```

### Anti-Pattern 4: Wrong Level of Abstraction
```
❌ Extract function that mixes high and low level logic
✅ Keep same abstraction level in extracted function
```

---

## 💡 Examples: Refactoring in Practice

### Example 1: Complete Refactoring

**Original** (Too complex, too long):
```typescript
function handleUserRegistration(userData) {
  if (!userData.email) return { error: 'Email required' };
  const emailParts = userData.email.split('@');
  if (emailParts.length !== 2) return { error: 'Invalid email' };

  const user = { email: userData.email, name: userData.name };
  const db = new Database();
  db.insert('users', user);

  const mailer = new GmailService();
  mailer.send(userData.email, 'Welcome!', 'Thanks for signing up');

  const token = Math.random().toString();
  return { success: true, token: token };
}
```

**After Refactoring** (Clean, testable, maintainable):
```typescript
// Technique 1: Extract Functions
function validateEmail(email: string): { valid: boolean; error?: string } {
  if (!email) return { valid: false, error: 'Email required' };
  const emailParts = email.split('@');
  if (emailParts.length !== 2) return { valid: false, error: 'Invalid email' };
  return { valid: true };
}

// Technique 2: Extract Classes (Dependency Injection)
class UserService {
  constructor(private db: Database, private mailer: Mailer) {}

  createUser(email: string, name: string) {
    this.db.insert('users', { email, name });
  }
}

// Technique 3: Simplify Conditionals (Guard clause)
async function handleUserRegistration(userData, userService) {
  const validation = validateEmail(userData.email);
  if (!validation.valid) {
    return { error: validation.error };
  }

  userService.createUser(userData.email, userData.name);
  await userService.sendWelcomeEmail(userData.email);

  const token = userService.generateToken(userData.email);
  return { success: true, token };
}

// Usage
const db = new PostgresDatabase();
const mailer = new GmailService();
const service = new UserService(db, mailer);
const result = await handleUserRegistration(userData, service);
```

**Results**:
- ✅ Validation tested separately
- ✅ Can swap Database and Mailer
- ✅ Easy to understand flow
- ✅ Reusable pieces

---

## 🎓 Philosophy

Refactoring techniques are about making code:

✅ **Understandable** - Clear intent and logic
✅ **Testable** - Can test pieces independently
✅ **Reusable** - Can use pieces elsewhere
✅ **Maintainable** - Easy to modify without breaking
✅ **Scalable** - Adding features doesn't create chaos

Master these 5 techniques, and most refactoring needs are met.

---

## 📚 Relationship to Core Principles

- **Atomic**: Extract function/class to make atomic pieces
- **Scoped**: Simplify conditionals to clarify scope
- **Linked**: Dependency injection connects pieces
- **SOLID**: These techniques implement SOLID principles

---

## ✨ Remember

5 Essential Refactoring Techniques:
```
1. Extract Function - Break into smaller functions
2. Extract Class/Module - Break into separate classes
3. Simplify Conditionals - Clear up complex logic
4. Use Async/Await - Clean up promise chains
5. Dependency Injection - Make dependencies explicit
```

Apply these, and code improves dramatically.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/refactoring-techniques.md`
**Created**: 2025-11-09
**Purpose**: Single source of truth for refactoring techniques
**Referenced by**: refactor.prompt.md, /refactor chatmode

🚀 **Master refactoring. Improve code continuously.**
