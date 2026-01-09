---
description: 'Jest testing framework best practices for TypeScript applications'
applyTo: '**/*.test.ts,**/*.spec.ts'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Reuse test utilities, fixtures, and helper functions
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain high test coverage and clear assertions
- [Testing Standards](../core/principles/testing-standards.md) - Follow AAA pattern and test organization best practices

When writing tests, always consider how they reinforce these core principles and contribute to sustainable, maintainable test suites.

---

# Jest + TypeScript Testing

## Overview

Jest is a modern testing framework optimized for TypeScript applications. TypeScript adds static type checking that can significantly improve test quality by catching errors at compile time rather than runtime.

## Jest Configuration

### tsconfig.json for Tests
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

### jest.config.js
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 75,
      lines: 75,
      statements: 75
    }
  }
};
```

## Test File Organization

### Directory Structure
```
src/
├── services/
│   ├── auth.service.ts
│   ├── __tests__/
│   │   └── auth.service.test.ts
├── utils/
│   ├── helpers.ts
│   └── __tests__/
│       └── helpers.test.ts
└── components/
    ├── Button.tsx
    └── __tests__/
        └── Button.test.tsx
```

### File Naming Convention
- Unit tests: `*.test.ts` or `*.spec.ts`
- Integration tests: `*.integration.test.ts`
- E2E tests: `*.e2e.test.ts`
- Test utilities: `*.test-utils.ts` or `test-helpers.ts`

## Test Structure (AAA Pattern)

All tests must follow the **Arrange-Act-Assert** pattern for clarity and maintainability:

```typescript
describe('UserService', () => {
  // Arrange: Set up test fixtures and dependencies
  let userService: UserService;
  let mockDatabase: jest.Mocked<Database>;

  beforeEach(() => {
    mockDatabase = createMockDatabase();
    userService = new UserService(mockDatabase);
  });

  it('should create a new user with valid input', () => {
    // Arrange: Prepare test data
    const userData = { name: 'John Doe', email: 'john@example.com' };

    // Act: Execute the code under test
    const result = userService.createUser(userData);

    // Assert: Verify the expected outcome
    expect(result).toEqual(expect.objectContaining({
      id: expect.any(String),
      name: 'John Doe',
      email: 'john@example.com'
    }));
    expect(mockDatabase.save).toHaveBeenCalledWith(expect.objectContaining(userData));
  });
});
```

## Mocking and Fixtures

### Mock Functions
```typescript
describe('PaymentService', () => {
  it('should call payment gateway on checkout', () => {
    const mockPaymentGateway = jest.fn().mockResolvedValue({ transactionId: '123' });
    const service = new PaymentService(mockPaymentGateway);

    const result = service.processPayment(100);

    expect(mockPaymentGateway).toHaveBeenCalledWith(100);
    expect(result).resolves.toEqual({ transactionId: '123' });
  });
});
```

### Mock Modules
```typescript
jest.mock('../services/api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'Test User' })
}));

import { fetchUser } from '../services/api';

describe('UserComponent', () => {
  it('should display user data', async () => {
    const user = await fetchUser(1);
    expect(user.name).toBe('Test User');
  });
});
```

### Test Fixtures and Builders
```typescript
// Avoid repetition with builder pattern
class UserBuilder {
  private user: Partial<User> = {
    id: '1',
    name: 'Test User',
    email: 'test@example.com'
  };

  withName(name: string): UserBuilder {
    this.user.name = name;
    return this;
  }

  withEmail(email: string): UserBuilder {
    this.user.email = email;
    return this;
  }

  build(): User {
    return this.user as User;
  }
}

// Usage in tests
const adminUser = new UserBuilder()
  .withEmail('admin@example.com')
  .build();
```

## Async Testing

### Promise-Based Tests
```typescript
describe('AsyncService', () => {
  it('should resolve with data', async () => {
    const data = await asyncService.fetchData();
    expect(data).toBeDefined();
  });

  it('should handle rejections', async () => {
    await expect(asyncService.failingOperation()).rejects.toThrow('Error message');
  });
});
```

### Fake Timers
```typescript
describe('Debounce', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  it('should debounce function calls', () => {
    const mockFn = jest.fn();
    const debounced = debounce(mockFn, 1000);

    debounced();
    debounced();
    debounced();

    expect(mockFn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1000);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});
```

## Type Safety in Tests

### Strongly Typed Mocks
```typescript
interface UserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<void>;
}

// Type-safe mock
const mockRepository = {
  findById: jest.fn<Promise<User>, [string]>(),
  save: jest.fn<Promise<void>, [User]>()
} as jest.Mocked<UserRepository>;

// Usage with type checking
describe('UserService', () => {
  it('should load and update user', async () => {
    const user: User = { id: '1', name: 'John' };
    mockRepository.findById.mockResolvedValue(user);

    const service = new UserService(mockRepository);
    const result = await service.updateUser('1', { name: 'Jane' });

    expect(mockRepository.save).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'Jane' })
    );
  });
});
```

### Generics in Test Utilities
```typescript
function createMock<T>(implementation?: Partial<T>): jest.Mocked<T> {
  const mock: any = {};
  const keys = Object.keys(implementation || {});

  keys.forEach(key => {
    mock[key] = jest.fn(implementation![key as keyof T]);
  });

  return mock;
}

// Usage
const mockLogger = createMock<Logger>({
  log: (msg) => console.log(msg)
});
```

## Test Coverage Standards

### Coverage Requirements
- **Statements**: Minimum 75%, target 85%+
- **Branches**: Minimum 75%, target 85%+
- **Functions**: Minimum 80%, target 90%+
- **Lines**: Minimum 75%, target 85%+

### Generate Coverage Report
```bash
npm test -- --coverage
```

### Coverage Configuration
```javascript
// jest.config.js
coveragePathIgnorePatterns: [
  '/node_modules/',
  '/dist/',
  '\.d\.ts$'
],
coverageReporters: ['text', 'lcov', 'html'],
```

## Common Patterns and Anti-Patterns

### ✓ Good Patterns

**1. Descriptive Test Names**
```typescript
it('should throw ValidationError when email format is invalid', () => {
  // Test implementation
});
```

**2. One Assertion Per Concept**
```typescript
it('should validate user email and return success', () => {
  const result = validateEmail('user@example.com');
  expect(result.isValid).toBe(true);
  expect(result.domain).toBe('example.com');
});
```

**3. DRY Test Code**
```typescript
// Extract common setup
function createTestUser(overrides?: Partial<User>): User {
  return { id: '1', name: 'Test', email: 'test@example.com', ...overrides };
}

it('should update user name', () => {
  const user = createTestUser({ name: 'John' });
  const updated = updateUser(user, { name: 'Jane' });
  expect(updated.name).toBe('Jane');
});
```

**4. Meaningful Error Messages**
```typescript
expect(result, 'User creation should include generated ID').toHaveProperty('id');
```

### ✗ Anti-Patterns to Avoid

**1. Tests Without Clear Purpose**
```typescript
// ✗ Bad: Unclear assertion
it('handles data', () => {
  const data = processData(input);
  expect(data).toBeDefined();
});

// ✓ Good: Clear assertion
it('should extract name field from raw user data', () => {
  const data = processData(rawUser);
  expect(data.name).toBe('John Doe');
});
```

**2. Testing Implementation Details**
```typescript
// ✗ Bad: Testing private methods and internal state
expect(service['_internalState']).toBe(true);

// ✓ Good: Test observable behavior
expect(service.isReady()).toBe(true);
```

**3. Coupled Tests**
```typescript
// ✗ Bad: Tests depending on execution order
it('step 1: create user', () => { /* ... */ });
it('step 2: fetch user', () => { /* ... */ });

// ✓ Good: Isolated, independent tests
it('should create user with auto-generated ID', () => { /* ... */ });
it('should fetch existing user by ID', () => { /* ... */ });
```

**4. Assertion Overload**
```typescript
// ✗ Bad: Too many assertions in one test
it('should process payment', () => {
  // 15 different assertions on different aspects
});

// ✓ Good: Focused test
it('should deduct amount from account balance', () => {
  expect(account.balance).toBe(originalBalance - amount);
});
```

## React Component Testing

### Testing Components with React Testing Library
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

describe('Button Component', () => {
  it('should call onClick handler when clicked', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);

    const button = screen.getByRole('button', { name: /click me/i });
    await userEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('should render disabled button when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
  });
});
```

## Best Practices Summary

1. **Write Tests First or Early**: Consider TDD approach for better design
2. **One Responsibility Per Test**: Each test should verify a single behavior
3. **Use Descriptive Names**: Test names should explain expected behavior
4. **Keep Tests Fast**: Avoid I/O operations, use mocks
5. **Test Edge Cases**: Null, empty, boundary conditions
6. **Maintain Test Code Quality**: Tests are code; apply same standards
7. **Use Type Assertions Wisely**: Don't over-test TypeScript types
8. **Review Coverage Reports**: Identify untested code paths
9. **Update Tests with Code**: Keep tests synchronized with implementation
10. **Refactor Tests**: Clean up duplication in test utilities

## Debugging Tests

### Debug Output
```typescript
describe('Complex Logic', () => {
  it('should handle edge case', () => {
    const result = complexFunction(input);
    console.log('Debug output:', { result, input }); // Visible with --verbose
    expect(result).toBeDefined();
  });
});
```

### Run Single Test
```bash
npm test -- --testNamePattern="should create user"
npm test -- --testPathPattern="auth.test.ts"
```

### Debug Mode
```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

---

## Related Instructions

- [Vitest for Node.js/JavaScript](./nodejs-javascript-vitest.instructions.md)
- [TypeScript Best Practices](./typescript-5-es2022.instructions.md)
- [Testing Standards Reference](./nodejs-javascript-vitest.instructions.md)
