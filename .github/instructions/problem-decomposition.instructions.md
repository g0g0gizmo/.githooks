---
description: 'Break complex problems into smaller, manageable subproblems that are easier to solve'
applyTo: '**/*'
---

# Problem Decomposition - Break Complex Problems Into Solvable Parts

## Overview

Problem decomposition is the art of taking a complex problem and breaking it down into smaller, manageable subproblems that are easier to understand, solve, and verify. A complex problem is just multiple simpler problems solved sequentially or in parallel.

Problem Decomposition ensures:

- Reduced cognitive load
- Easier verification of correctness
- Ability to work on subproblems in parallel
- Creation of reusable solutions
- Simplified testing and debugging
- Clearer understanding of problem space

## Core Concepts

### Three Primary Decomposition Techniques

#### 1. Sequential Decomposition

**Solve subproblems one after another, with later solutions depending on earlier ones.**

```typescript
// Problem: Process user registration flow
// Decompose into sequential steps:

function registerUser(userData: UserData): User {
  // Step 1: Validate input data
  const validatedData = validateUserData(userData);

  // Step 2: Check if user already exists
  const existingUser = findUserByEmail(validatedData.email);
  if (existingUser) throw new UserAlreadyExistsError();

  // Step 3: Hash password
  const hashedPassword = hashPassword(validatedData.password);

  // Step 4: Create database record
  const user = await database.createUser({
    ...validatedData,
    password: hashedPassword
  });

  // Step 5: Send confirmation email
  await emailService.sendConfirmation(user.email);

  // Step 6: Create audit log
  await logger.logUserCreation(user.id);

  return user;
}

// Key insight: Each step depends on previous step's output
// Intermediate properties: validatedData → exists check → user → confirmation
```

**When to use**:

- Processing pipelines
- Installation/setup procedures
- Data transformation flows
- Sequential workflows

**Advantages**:

- Clear sequence
- Easy to understand
- Natural flow
- Easy to debug

**Challenges**:

- Can become monolithic
- Hard to parallelize
- Dependencies can grow complex

---

#### 2. Case Analysis (Divide by Cases)

**Split problem into distinct cases, solve each independently, recombine.**

```typescript
// Problem: Calculate shipping cost
// Decompose by cases:

function calculateShippingCost(order: Order, destination: Location): number {
  // Case 1: Domestic shipping
  if (isDomestic(destination)) {
    return calculateDomesticShipping(order.weight, destination.zone);
  }

  // Case 2: International shipping
  if (isInternational(destination)) {
    return calculateInternationalShipping(
      order.weight,
      destination.country
    );
  }

  // Case 3: Local pickup (no shipping cost)
  if (isLocalPickup(destination)) {
    return 0;
  }

  throw new InvalidDestinationError();
}

// Key insight: Problem space divided into mutually exclusive cases
// Each case handled independently
// Results combined into final answer
```

**When to use**:

- Classification problems
- Different rules for different inputs
- State machines
- Decision logic

**Advantages**:

- Clear logic
- Easy to test each case
- No overlap
- Maintainable conditions

**Challenges**:

- Must cover all cases
- Cases must be truly independent
- Can become complex with many cases

---

#### 3. Inductive Decomposition (Recursion)

**Break into smaller instances of the same problem, solve those recursively, combine.**

```typescript
// Problem: Search for value in tree
// Decompose inductively:

function searchTree<T>(node: TreeNode<T>, target: T): boolean {
  // Base case: empty tree
  if (node === null) return false;

  // Base case: found target
  if (node.value === target) return true;

  // Recursive case: search in smaller subproblems
  const foundInLeft = searchTree(node.left, target);
  if (foundInLeft) return true;

  const foundInRight = searchTree(node.right, target);
  return foundInRight;
}

// Problem size decreases: full tree → subtrees → single nodes → null
// Base case stops recursion
// Combine: OR of left/right results
```

**When to use**:

- Tree/graph problems
- Hierarchical data
- Factorial, fibonacci, etc.
- Divide-and-conquer algorithms

**Advantages**:

- Elegant for recursive structures
- Natural for trees/graphs
- Mathematical foundation
- Can be very efficient

**Challenges**:

- Easy to create infinite loops
- Stack overflow risk
- Can be hard to understand
- Base case critical

---

## Application Checklist

- [ ] Problem is clearly stated and bounded
- [ ] Decomposition technique matches problem structure
- [ ] Each subproblem is clearly defined
- [ ] Subproblems don't overlap (or overlap is intentional)
- [ ] Solution to each subproblem is understandable
- [ ] Subproblems can be tested independently
- [ ] Recombination step is clear
- [ ] Edge cases identified and handled
- [ ] Solution can be implemented and verified

### Problem-Solving Process

#### Step 1: Understand the Problem

```text
Questions to ask:
- What exactly are we solving?
- What are inputs and outputs?
- What are constraints?
- What are edge cases?
- How will we know it's correct?

Example:
Problem: "Sort an array of numbers"
- Input: array of integers
- Output: sorted array (ascending or descending?)
- Constraints: in-place? stable? what size?
- Edge cases: empty array, single element, duplicates, negatives
- Correctness: every element <= next element
```

#### Step 2: Identify Problem Structure

```text
Patterns to recognize:
- Sequential? → Use sequential decomposition
- Different cases? → Use case analysis
- Recursive structure? → Use inductive decomposition
- Combination? → Use hybrid approach

Example:
Sorting problem structure:
- Contains subproblems: partition array, sort partitions (recursive)
- Has cases: small arrays (direct), large arrays (divide)
- Hybrid: divide-and-conquer (quick sort)
```

#### Step 3: Choose Decomposition Technique

```text
Decision tree:
- If steps depend on each other → sequential
- If cases are independent → case analysis
- If self-similar problem → induction
- If multiple apply → use what's clearest

Example:
Sorting:
- Quick sort: Case analysis (pivot) + Induction (recursion)
- Merge sort: Sequential (divide) + Induction (recursion) + Sequential (merge)
- Insertion sort: Sequential (for each element)
```

#### Step 4: Solve Subproblems

```text
Focus on:
- Clear interface for each subproblem
- Minimum necessary logic
- Testable in isolation
- Reusable if possible
```

#### Step 5: Combine Solutions

```text
Recombination step:
- How do subproblem solutions combine?
- What's the recombination logic?
- Can it be tested independently?
```

#### Step 6: Verify Solution

```text
Testing:
- Does each subproblem work?
- Does recombination work?
- Do edge cases pass?
- Does full solution match problem statement?
```

---

## Related Principles

- SOLID principles - SRP supports focused subproblems
- KISS - simple subproblems are easier to understand and test
- Orthogonality - independent subproblems interfere less

---

## Anti-Patterns

### Anti-Pattern 1: Monolithic Solutions

```typescript
// ❌ Bad: Entire problem in one function
function processUserData(userData: any) {
  // Validation
  if (!userData.email) throw new Error('Email required');
  if (!userData.password) throw new Error('Password required');
  if (userData.age < 18) throw new Error('Must be 18+');
  if (userData.email.indexOf('@') === -1) throw new Error('Invalid email');
  if (userData.password.length < 8) throw new Error('Weak password');

  // Database operations
  const existing = db.query(
    `SELECT * FROM users WHERE email='${userData.email}'`
  );
  if (existing) throw new Error('User exists');

  // Hashing
  const salt = Math.random().toString();
  const hash = sha256(userData.password + salt);

  // Saving
  db.run(
    `INSERT INTO users VALUES ('${userData.email}', '${hash}')`
  );

  // Email
  sendEmail(userData.email, 'Welcome!');

  // Logging
  fs.appendFileSync('log.txt', `User created: ${userData.email}`);

  return { status: 'success' };
}

// ✅ Good: Decomposed into clear subproblems
function createUser(userData: UserData): User {
  const validated = validateUserData(userData);
  const existing = findExistingUser(validated.email);
  if (existing) throw new UserAlreadyExistsError();

  const hashedPassword = hashPassword(validated.password);
  const user = saveUser(validated, hashedPassword);

  sendWelcomeEmail(user.email);
  logUserCreation(user.id);

  return user;
}
```

### Anti-Pattern 2: Unclear Recombination

```typescript
// ❌ Bad: How does this combine?
function solve(problem) {
  const part1 = solvePart1(problem);
  const part2 = solvePart2(problem);
  const part3 = solvePart3(problem);
  // How do these combine? No clear logic
  return somehow(part1, part2, part3);
}

// ✅ Good: Clear combination logic
function solve(problem) {
  const part1 = solvePart1(problem);
  // part1 feeds into part2
  const part2 = solvePart2(problem, part1.result);
  // part2 feeds into part3
  const part3 = solvePart3(problem, part2.result);
  // Clear: combine results
  return combine(part1, part2, part3);
}
```

### Anti-Pattern 3: Missing Edge Cases

```typescript
// ❌ Bad: Edge cases not handled
function factorial(n) {
  if (n === 0) return 1;  // Base case
  return n * factorial(n - 1);  // Recursive case
  // What if n is negative? Infinite recursion
  // What if n is float? Wrong answer
}

// ✅ Good: All cases handled
function factorial(n: number): number {
  // Validate input
  if (!Number.isInteger(n)) {
    throw new Error('Input must be integer');
  }
  if (n < 0) {
    throw new Error('Input must be non-negative');
  }

  // Base case
  if (n === 0) return 1;

  // Recursive case
  return n * factorial(n - 1);
}
```

---

## Success Indicators

You're using problem decomposition well when:

- Complex problems feel manageable after decomposition
- Each subproblem is understandable on its own
- Subproblems can be tested independently
- Solution is easier to explain
- New team members understand the logic quickly
- Changes are localized to specific subproblems
- Solutions are reusable for similar problems

---

## Why Problem Decomposition Matters

✅ **Reduces Cognitive Load** - Smaller problems are easier to understand
✅ **Enables Parallelization** - Multiple people can work on subproblems
✅ **Improves Testability** - Test each subproblem independently
✅ **Creates Reusable Solutions** - Subproblem solutions work elsewhere
✅ **Simplifies Debugging** - Problem is isolated to specific subproblem
✅ **Clarifies Intent** - Decomposition explains how solution works

Master problem decomposition, and complex problems become series of simple, understandable, testable steps.
