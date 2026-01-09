# Core Principle: Review Dimensions

**Purpose**: Standard dimensions for evaluating code quality, architecture, and design
**Audience**: You + AI (code review, architecture review, security review)
**Focus**: 5 key dimensions to assess any system or code

---

## 🎯 What are Review Dimensions?

Review dimensions are **5 aspects you evaluate** when reviewing code or architecture:

1. **Modularity** - Is code properly separated into pieces?
2. **Scalability** - Can it handle growth?
3. **Maintainability** - Can someone understand and change it?
4. **Testability** - Can it be tested easily?
5. **Reliability** - Does it handle failures?

**Core Idea**: Evaluate everything against these 5 dimensions.

---

## 🔑 Dimension 1: Modularity

**Definition**: Code is properly separated into independent, reusable pieces.

**What to check**:
- Are concerns properly separated? (auth, database, API separate?)
- Can modules be changed independently?
- Is there clear module responsibility?
- Are module boundaries clear?

### Red Flags 🚩 (Modularity Problems)

- ❌ Circular dependencies (A imports B, B imports A)
- ❌ Modules tightly coupled (changing one requires changing many)
- ❌ Too many dependencies between modules
- ❌ One module doing too much (multiple responsibilities)
- ❌ Unclear which functions belong together
- ❌ Hard to identify module boundaries

### Good Signs ✅ (Good Modularity)

- ✅ Clear module boundaries (knows where each piece lives)
- ✅ Modules have single responsibility
- ✅ Dependencies flow one direction (no circles)
- ✅ Easy to test in isolation
- ✅ Can change one module without touching others
- ✅ Clear what goes in each module

### Example - Bad Modularity

```
❌ Everything in one file
src/app.ts (2000 lines)
├── User management
├── Database access
├── API endpoints
├── Authentication
├── Email sending
└── Error handling
(Impossible to change one thing)
```

### Example - Good Modularity

```
✅ Clear separation
src/
├── users/
│   ├── user.service.ts (user logic)
│   ├── user.controller.ts (API endpoints)
│   └── user.test.ts
├── auth/
│   ├── auth.service.ts (authentication logic)
│   └── auth.middleware.ts
├── database/
│   ├── database.service.ts (data access)
│   └── models/
└── email/
    └── email.service.ts (email sending)
(Each module independent, can be changed separately)
```

---

## 🔑 Dimension 2: Scalability

**Definition**: System can handle growth (more users, data, features).

**What to check**:
- Can system handle growth without rewriting?
- Can new features be added without major refactoring?
- Is there room for performance improvement?
- Is architecture flexible for change?

### Red Flags 🚩 (Scalability Problems)

- ❌ Hardcoded limits (max 1000 users, max 100 items)
- ❌ Monolithic architecture (all in one place)
- ❌ No separation of concerns
- ❌ Tight coupling (can't extract piece without rewriting)
- ❌ Performance bottlenecks (database, memory, CPU)
- ❌ Can't add new feature types without full rewrite

### Good Signs ✅ (Good Scalability)

- ✅ Horizontal scaling possible (add more servers)
- ✅ Vertical scaling possible (upgrade hardware)
- ✅ New features added without touching existing code
- ✅ Configurable limits (can increase without code change)
- ✅ Database queries optimized
- ✅ Caching strategy in place
- ✅ Can add new feature types easily

### Example - Bad Scalability

```typescript
// ❌ Hardcoded limits, will break at scale
const MAX_USERS = 1000;
const MAX_POSTS_PER_USER = 100;

const users = []; // Array grows unbounded
const posts = []; // Single array for all posts

function addUser(user) {
  if (users.length >= MAX_USERS) throw new Error('Too many users');
  users.push(user); // O(1) but array grows unbounded
}

// At 2000 users: breaks
// At 1M users: memory fails
// Can't add new features: would require full rewrite
```

### Example - Good Scalability

```typescript
// ✅ Scalable architecture
interface Database {
  insert(table: string, data: any): Promise<any>;
  query(sql: string, params: any[]): Promise<any[]>;
  // Database handles scaling: can add servers, sharding, etc.
}

class UserService {
  constructor(private db: Database) {}

  async addUser(user: User): Promise<User> {
    // No hardcoded limits
    // Database handles scaling
    return this.db.insert('users', user);
  }
}

// New feature easy: just add new endpoint, new database table
// Database scales horizontally: add more servers
// Can handle millions of users
```

---

## 🔑 Dimension 3: Maintainability

**Definition**: Code is easy to understand, change, and modify.

**What to check**:
- Is code easy to understand?
- Can developers make changes confidently?
- Are dependencies clear?
- Is code well-documented?
- Are naming conventions clear?

### Red Flags 🚩 (Maintainability Problems)

- ❌ Complex interdependencies (hard to trace)
- ❌ Magic numbers or undocumented behavior
- ❌ Difficult to trace execution flow
- ❌ Unclear variable/function names
- ❌ No documentation or comments
- ❌ Code mixed with unrelated logic
- ❌ Inconsistent coding style

### Good Signs ✅ (Good Maintainability)

- ✅ Clear naming and structure
- ✅ Code easy to follow (top-to-bottom)
- ✅ Documentation explains WHY (not WHAT)
- ✅ Consistent style throughout
- ✅ Related code grouped together
- ✅ Easy to find what you need
- ✅ Comments where logic isn't obvious

### Example - Bad Maintainability

```typescript
// ❌ Hard to understand
function f(u, p) {
  const h = crypto.createHash('sha256').update(p).digest('hex');
  const r = db.q(`SELECT * FROM u WHERE n = '${u}'`); // SQL injection!
  return r[0].p === h; // Magic: what is p? Which p?
}

// Questions:
// - What does f do?
// - What are u and p?
// - Why is there a SHA256?
// - What's in r?
// - SQL injection vulnerability!
```

### Example - Good Maintainability

```typescript
// ✅ Easy to understand
function validateUserPassword(username: string, password: string): boolean {
  // Hash the provided password
  const hashedPassword = hashPassword(password);

  // Look up user in database
  const user = this.userDatabase.findByUsername(username);

  // Compare hashes (not plaintext passwords)
  return user && user.passwordHash === hashedPassword;
}

// Clear:
// - Function name explains what it does
// - Variable names are descriptive
// - Logic is easy to follow
// - No SQL injection (using ORM)
```

---

## 🔑 Dimension 4: Testability

**Definition**: Code can be easily tested in isolation.

**What to check**:
- Can components be tested independently?
- Are dependencies mockable?
- Is there clear input/output?
- Can I test without side effects?

### Red Flags 🚩 (Testability Problems)

- ❌ Hardcoded dependencies (new Database() in class)
- ❌ Global state (singletons, global variables)
- ❌ Side effects hidden in functions
- ❌ No clear input/output
- ❌ External API calls in business logic
- ❌ Mixing concerns (UI, logic, data in one class)

### Good Signs ✅ (Good Testability)

- ✅ Dependency injection (dependencies injected)
- ✅ Pure functions (same input = same output)
- ✅ Clear interfaces (input/output obvious)
- ✅ No global state
- ✅ Easy to mock dependencies
- ✅ Side effects isolated
- ✅ Can test without touching database/API

### Example - Bad Testability

```typescript
// ❌ Hard to test
class UserService {
  private db = new PostgresDatabase(); // Hardcoded!

  async createUser(email: string, password: string) {
    // Need actual database connection to test
    this.db.insert('users', { email, password });

    // Need actual email service to test
    const mailer = new GmailService();
    mailer.send(email, 'Welcome');

    return { success: true };
  }
}

// Can't test without:
// 1. Actual PostgreSQL database
// 2. Actual Gmail account
// 3. Multiple seconds per test (API calls)
```

### Example - Good Testability

```typescript
// ✅ Easy to test
class UserService {
  constructor(
    private db: Database, // Injected
    private mailer: Mailer // Injected
  ) {}

  async createUser(email: string, password: string) {
    await this.db.insert('users', { email, password });
    await this.mailer.send(email, 'Welcome');
    return { success: true };
  }
}

// Test with mocks
const mockDb = { insert: jest.fn() };
const mockMailer = { send: jest.fn() };
const service = new UserService(mockDb, mockMailer);

await service.createUser('test@example.com', 'pass');
expect(mockDb.insert).toHaveBeenCalled();
expect(mockMailer.send).toHaveBeenCalled();
// Test in milliseconds, no external calls
```

---

## 🔑 Dimension 5: Reliability

**Definition**: System handles failures gracefully.

**What to check**:
- What happens when things fail?
- Is there proper error handling?
- Does system recover from failures?
- Is failure monitored?

### Red Flags 🚩 (Reliability Problems)

- ❌ No error handling (crashes silently)
- ❌ Silent failures (fails but no one knows)
- ❌ No retry logic (fails once, stays broken)
- ❌ No monitoring/logging (can't diagnose)
- ❌ No fallbacks (no plan B if something fails)
- ❌ Single point of failure (everything depends on one thing)

### Good Signs ✅ (Good Reliability)

- ✅ Proper error handling (try/catch or error handling middleware)
- ✅ Errors logged with context
- ✅ Retry logic for transient failures
- ✅ Monitoring and alerting in place
- ✅ Graceful degradation (partial service if component fails)
- ✅ Fallback options (if primary fails, use secondary)
- ✅ Health checks (know when something breaks)

### Example - Bad Reliability

```typescript
// ❌ No error handling
async function deployApp() {
  const code = await git.pull(); // What if fails?
  await db.migrate(); // No error handling
  await service.restart(); // If this fails, no one knows
  return { success: true }; // Always returns success
}

// Problems:
// - If git.pull() fails, nobody knows
// - If db.migrate() fails, app crashes
// - If service.restart() fails, user sees success
```

### Example - Good Reliability

```typescript
// ✅ Proper error handling
async function deployApp() {
  try {
    const code = await git.pull();
    logger.info('Code pulled successfully');

    await db.migrate();
    logger.info('Database migrated');

    await service.restart();
    logger.info('Service restarted');

    // Health check
    const healthy = await checkHealth();
    if (!healthy) {
      logger.error('Health check failed after deploy');
      return { success: false, error: 'Health check failed' };
    }

    return { success: true };
  } catch (error) {
    logger.error('Deployment failed', {
      error: error.message,
      step: error.step,
      timestamp: new Date()
    });

    // Attempt rollback
    try {
      await rollback();
      logger.info('Rollback successful');
    } catch (rollbackError) {
      logger.error('Rollback failed', rollbackError);
      sendAlert('CRITICAL: Deployment failed and rollback failed');
    }

    return { success: false, error: error.message };
  }
}

// Good practices:
// - Logging at each step
// - Error caught and handled
// - Rollback attempted
// - Alert sent if critical
// - Health check validates
```

---

## ✅ Review Checklist

When reviewing code or architecture:

**Modularity**:
- [ ] Concerns properly separated?
- [ ] Dependencies flow one direction?
- [ ] Can change one module independently?
- [ ] Module boundaries clear?

**Scalability**:
- [ ] Can handle growth?
- [ ] No hardcoded limits?
- [ ] New features addable without refactor?
- [ ] Database/infrastructure designed for scale?

**Maintainability**:
- [ ] Easy to understand?
- [ ] Clear naming and structure?
- [ ] Well documented?
- [ ] Consistent style?

**Testability**:
- [ ] Dependencies injectable?
- [ ] No hardcoded instances?
- [ ] Clear input/output?
- [ ] Can test without external calls?

**Reliability**:
- [ ] Errors handled?
- [ ] Failures logged?
- [ ] Retry logic present?
- [ ] Monitoring in place?
- [ ] Fallbacks available?

---

## 🔄 Review Workflow

### When Reviewing Code

```
1. Read code
2. Evaluate each dimension:
   - Is it modular?
   - Could it scale?
   - Is it maintainable?
   - Can it be tested?
   - Is it reliable?
3. For each dimension:
   - Red flags? Point them out
   - Good signs? Note them
   - Improvements? Suggest them
4. Provide report (see report-format.md)
```

---

## 💡 Examples: Reviewing Real Code

### Example 1: Review User Service

**Code**:
```typescript
class UserService {
  constructor(private db: Database, private mail: Mailer) {}

  async createUser(email: string, password: string) {
    if (!email) throw new Error('Email required');

    const hash = await this.hash(password);
    await this.db.insert('users', { email, password_hash: hash });

    try {
      await this.mail.sendWelcome(email);
    } catch (error) {
      logger.error('Welcome email failed', { email, error });
      // Don't fail user creation if email fails
    }

    return { success: true, email };
  }

  private async hash(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }
}
```

**Review Against 5 Dimensions**:

| Dimension | Assessment |
|-----------|-----------|
| **Modularity** | ✅ Good: Service, Database, Mailer separate. Clear responsibility. |
| **Scalability** | ✅ Good: Uses database (scales). No hardcoded limits. |
| **Maintainability** | ✅ Good: Clear names, one job, good structure. |
| **Testability** | ✅ Good: Injected deps, can mock db/mail, easy to test. |
| **Reliability** | ✅ Good: Error handling on mail, logged. Continues if email fails. |

**Overall**: Strong code. Few concerns.

---

## 🎓 Philosophy

Review dimensions help you:

✅ **Be consistent** - Always evaluate same 5 things
✅ **Be complete** - Don't miss important aspects
✅ **Be objective** - Clear criteria, not opinion
✅ **Be constructive** - Feedback backed by principles
✅ **Improve code** - Find real problems and solutions

---

## 📚 Relationship to Core Principles

- **Atomic**: Modularity ensures each piece is atomic
- **Scoped**: Testability requires clear scope
- **Linked**: Dependencies shown in reliability
- **SOLID**: These dimensions reflect SOLID principles

---

## ✨ Remember

5 Review Dimensions:
```
1. Modularity - Are things properly separated?
2. Scalability - Can it grow?
3. Maintainability - Can I understand and change it?
4. Testability - Can I test it easily?
5. Reliability - Does it handle failures?
```

Evaluate everything against these 5.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/review-dimensions.md`
**Created**: 2025-11-09
**Purpose**: Single source of truth for code/architecture review dimensions
**Referenced by**: code-review.prompt.md, architecture-review.prompt.md, security-review.prompt.md, all review chatmodes

🚀 **Master these dimensions. Review everything better.**
