---
description: 'Establish consistent testing practices for confidence, documentation, and regression prevention'
---

# Testing Standards

## Overview

Testing is a foundational practice for building reliable, maintainable software. This principle establishes consistent testing practices that provide confidence in code quality while serving as living documentation of how code should be used.

Testing Standards ensure:

- Code works as intended (confidence)
- System behavior is documented through tests
- Breaking changes are caught early (regression prevention)
- Refactoring is safe and verifiable
- New developers understand intended usage
- Quality gates are consistent across projects

## Core Concepts

### Test Philosophy

Tests serve three primary purposes:

1. **Confidence**: Code works as intended
2. **Documentation**: How the code is meant to be used
3. **Regression Prevention**: Catch breaking changes early

Tests should be:

- ✅ Fast (< 1000ms per test)
- ✅ Isolated (no dependencies between tests)
- ✅ Repeatable (same result every time)
- ✅ Clear (intent obvious without reading implementation)
- ✅ Maintained (kept up-to-date with code)

---

### AAA Pattern (Arrange-Act-Assert)

**Every test follows this structure:**

```typescript
describe('UserService.createUser', () => {
  it('should create user with valid email', () => {
    // ARRANGE: Set up test data and mocks
    const email = 'test@example.com';
    const password = 'SecurePass123';
    const mockRepository = {
      save: jest.fn().mockResolvedValue({ id: '123', email })
    };
    const service = new UserService(mockRepository);

    // ACT: Perform the action being tested
    const result = await service.createUser(email, password);

    // ASSERT: Verify the expected outcome
    expect(result.id).toBe('123');
    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ email })
    );
  });
});
```

**Why AAA?**

- Clear structure anyone can follow
- Separates concerns (setup, action, verification)
- Makes tests scannable
- Reduces debugging time

---

## Test Pyramid

```
        △ E2E Tests
       ╱ ╲ (10%)
      ╱   ╲  Integration Tests
     ╱     ╲ (30%)
    ╱_______╲
   ╱ Unit T ╲ (60%)
  ╱_________╲
```

### Unit Tests (60% of tests)

- **What**: Test single function/method in isolation
- **How**: Mock external dependencies
- **Speed**: < 100ms per test
- **Coverage Target**: 80%+

```typescript
// ✅ Unit test: Tests calculateAge function alone
describe('calculateAge', () => {
  it('should return correct age for birthday', () => {
    const birthday = new Date('1990-01-01');
    const result = calculateAge(birthday);
    expect(result).toBeGreaterThan(30);
  });

  it('should throw error for future date', () => {
    const futureDate = new Date('2030-01-01');
    expect(() => calculateAge(futureDate)).toThrow();
  });
});
```

### Integration Tests (30% of tests)

- **What**: Test multiple components working together
- **How**: Use real dependencies where possible
- **Speed**: 100ms - 1000ms per test
- **Coverage Target**: Key workflows only

```typescript
// ✅ Integration test: Tests UserService + Repository + Database
describe('UserService.createUser (Integration)', () => {
  it('should create user and save to database', async () => {
    const service = new UserService(realDatabaseConnection);
    const user = await service.createUser('test@example.com', 'password');

    expect(user.id).toBeDefined();

    // Verify it was actually saved
    const saved = await database.findById(user.id);
    expect(saved.email).toBe('test@example.com');
  });
});
```

### E2E Tests (10% of tests)

- **What**: Test complete user workflows
- **How**: Use actual application
- **Speed**: 1000ms+ per test (OK, they're slow)
- **Coverage Target**: Critical paths only

```typescript
// ✅ E2E test: User flow from login to purchase
describe('Purchase Workflow (E2E)', () => {
  it('user should complete purchase from login to confirmation', async () => {
    await page.goto('https://example.com/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await page.goto('https://example.com/products');
    await page.click('button.add-to-cart');

    await page.goto('https://example.com/checkout');
    await page.click('button.checkout');

    expect(await page.textContent('.order-confirmation')).toContain('Thank you');
  });
});
```

---

## Mocking Strategy

### Mock Only External Dependencies

**❌ DON'T mock**:
- Classes you own
- Pure functions
- Business logic
- Data transformations

**✅ DO mock**:
- API calls
- Database connections
- File system operations
- External services
- Time-dependent code

```typescript
// ❌ Bad: Mocking too much (mocking your own classes)
describe('UserService', () => {
  it('should create user', () => {
    const mockPassword = { hash: jest.fn() };  // Don't mock this!
    const mockUser = { validate: jest.fn() };  // Don't mock this!

    // Test is too isolated, doesn't test real behavior
  });
});

// ✅ Good: Mock only external dependencies
describe('UserService', () => {
  it('should create user', async () => {
    // Mock external services
    const mockEmailService = { send: jest.fn() };
    const mockDatabase = { insert: jest.fn() };

    const service = new UserService(mockDatabase, mockEmailService);

    // Test real behavior (no mocks for your own classes)
    const result = service.createUser('test@example.com', 'password');

    expect(result.email).toBe('test@example.com');
    expect(mockDatabase.insert).toHaveBeenCalled();
    expect(mockEmailService.send).toHaveBeenCalled();
  });
});
```

### Verification Strategies

```typescript
// Verify the method was called
expect(mockApi.get).toHaveBeenCalled();

// Verify it was called with specific arguments
expect(mockApi.get).toHaveBeenCalledWith('/users/123');

// Verify number of calls
expect(mockEmail.send).toHaveBeenCalledTimes(1);

// Verify with partial matching
expect(mockDb.insert).toHaveBeenCalledWith(
  expect.objectContaining({
    email: 'test@example.com'
  })
);

// Verify return value was used correctly
expect(result).toEqual(expectedValue);
```

---

## Coverage Targets

| Level          | Target | What It Means              |
| -------------- | ------ | -------------------------- |
| **Lines**      | 80%+   | 80% of code lines executed |
| **Branches**   | 70%+   | All if/else paths covered  |
| **Functions**  | 80%+   | All functions called       |
| **Statements** | 80%+   | All statements executed    |

**Important**: Coverage is a minimum, not a goal.

- High coverage (100%) without meaningful tests = waste
- Lower coverage (60%) with meaningful tests = valuable
- Aim for high coverage on critical paths, not everywhere

```bash
# Generate coverage report
jest --coverage

# Example output:
# Statements   : 85% ( 340/400 )
# Branches     : 78% ( 45/58 )
# Functions    : 82% ( 50/61 )
# Lines        : 84% ( 330/392 )
```

---

## Application Checklist

- [ ] Unit tests for all business logic (60% of tests)
- [ ] Integration tests for key workflows (30% of tests)
- [ ] E2E tests for critical user paths (10% of tests)
- [ ] All tests follow AAA pattern
- [ ] External dependencies are mocked
- [ ] Tests are fast (< 1000ms each)
- [ ] Tests are isolated (no inter-test dependencies)
- [ ] Tests are repeatable (deterministic)
- [ ] Test names describe what is being tested
- [ ] Coverage > 80% on critical paths
- [ ] No test duplication
- [ ] Tests serve as documentation
- [ ] Flaky tests are identified and fixed
- [ ] Tests run on every commit

### When Writing Tests

1. **Identify What to Test**: Business logic, edge cases, error paths
2. **Choose Test Type**: Unit, integration, or E2E?
3. **Set Up Test Data**: Arrange phase
4. **Perform Action**: Act phase
5. **Verify Outcome**: Assert phase
6. **Clean Up**: Teardown if needed

### When Reviewing Tests

- Are tests clear and focused?
- Does each test test one thing?
- Are external dependencies mocked?
- Are assertions meaningful?
- Is test data minimal and clear?
- Could this test catch a real bug?

---

## Related Principles

- [Design by Contract](../../.github/copilot/instructions/design-by-contract.instructions.md) - Contracts make testing clearer
- [SOLID Principles](../../.github/copilot/instructions/solid-principles.instructions.md) - SOLID code is easier to test
- [Code Quality Goals](../../.github/copilot/instructions/code-quality-goals.instructions.md) - Testing ensures quality

---

## Anti-Patterns

### Anti-Pattern 1: Testing Implementation Details

```typescript
// ❌ Bad: Testing internals, not behavior
test('should call database 3 times', () => {
  const mockDb = jest.fn();
  service.processUsers(mockDb);
  expect(mockDb).toHaveBeenCalledTimes(3);
  // Test breaks if implementation changes but behavior is the same
});

// ✅ Good: Testing observable behavior
test('should return processed users', () => {
  const result = service.processUsers(mockDb);
  expect(result).toHaveLength(3);
  expect(result[0]).toHaveProperty('processed', true);
  // Test remains valid if implementation details change
});
```

### Anti-Pattern 2: Tests That Are Too Tight

```typescript
// ❌ Bad: Brittle test, tightly coupled to implementation
test('should return exact format', () => {
  const result = service.getUser();
  expect(result).toEqual({
    id: '123',
    name: 'John',
    email: 'john@example.com',
    createdAt: 1234567890
  });
  // Test breaks if any field changes, even non-essential ones
});

// ✅ Good: Test what matters, ignore implementation details
test('should return user with required fields', () => {
  const result = service.getUser();
  expect(result).toHaveProperty('id');
  expect(result).toHaveProperty('name');
  expect(result).toHaveProperty('email');
  expect(result.email).toMatch(/@/);
  // Test focuses on contract, not exact format
});
```

### Anti-Pattern 3: Slow Tests

```typescript
// ❌ Bad: Tests that are unnecessarily slow
test('should process users', async () => {
  // Waits for real API
  const users = await api.getUsers();
  // Writes to real database
  await database.insert(users);
  // Real file I/O
  fs.writeFileSync('users.json', JSON.stringify(users));
  // Total: 5+ seconds per test
});

// ✅ Good: Fast tests with mocks
test('should process users', async () => {
  const mockApi = { getUsers: jest.fn().mockResolvedValue(users) };
  const mockDb = { insert: jest.fn() };
  const mockFs = { writeFile: jest.fn() };

  await service.processUsers(mockApi, mockDb, mockFs);

  expect(mockDb.insert).toHaveBeenCalledWith(users);
  // Total: < 100ms
});
```

### Anti-Pattern 4: No Error Testing

```typescript
// ❌ Bad: Only testing happy path
test('should create user', () => {
  const result = service.createUser('test@example.com', 'password');
  expect(result.email).toBe('test@example.com');
});

// ✅ Good: Test error paths too
describe('UserService.createUser', () => {
  test('should create user with valid input', () => {
    const result = service.createUser('test@example.com', 'password');
    expect(result.email).toBe('test@example.com');
  });

  test('should throw error for invalid email', () => {
    expect(() => {
      service.createUser('invalid', 'password');
    }).toThrow('Invalid email');
  });

  test('should throw error for weak password', () => {
    expect(() => {
      service.createUser('test@example.com', 'weak');
    }).toThrow('Password too weak');
  });
});
```

### Anti-Pattern 5: No Test Documentation

```typescript
// ❌ Bad: Unclear test names
test('test1', () => {
  const x = service.process(data);
  expect(x).toBe(expected);
});

// ✅ Good: Clear test names that document behavior
test('should calculate discount as 10% for orders over $100', () => {
  const result = service.calculateDiscount(150);
  expect(result).toBe(10);
});
```

---

## Success Indicators

You're applying testing standards well when:

- Tests run fast (suite completes in < 5 minutes)
- Tests are deterministic (always pass or fail consistently)
- New developers understand code through tests
- Tests catch regressions before production
- Test failures point to specific problems
- Tests document intended behavior
- No flaky tests that fail intermittently
- Code coverage is > 80% on critical paths

---

## Why Testing Matters

✅ **Confidence** - Know code works as intended
✅ **Documentation** - Tests show how to use code
✅ **Regression Prevention** - Catch breaking changes early
✅ **Refactoring Safety** - Change with confidence
✅ **Debugging** - Failures point to root cause
✅ **Design** - Writing testable code improves design

Master testing standards, and your codebase becomes more reliable, maintainable, and easier to modify with confidence.
