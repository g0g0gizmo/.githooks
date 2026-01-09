---
description: 'Refactor code for clarity, performance, or maintainability with depth and scope control'
---

# Refactor Code

Improve code quality, readability, performance, or maintainability through targeted refactoring. Supports both quick improvements and deep architectural refactoring.

## Core Principles

This content applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Eliminate duplication in code structure
- [KISS (Keep It Simple, Stupid)](../core/principles/KISS.md) - Simplify logic and structure
- [SOLID Principles](../core/principles/principles-solid.md) - Improve modularity and maintainability
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Enhance readability, testability, and efficiency

---

## Interactive Setup

**Ask the user:**

1. **What scope of refactoring?**
   - Quick (targeted improvements to specific functions/classes)
   - Module (refactor an entire module or feature)
   - System (refactor across multiple files/systems)

2. **What's the primary goal?**
   - Clarity (improve readability and understanding)
   - Performance (optimize speed or resource usage)
   - Maintainability (reduce duplication, improve structure)
   - Testing (improve testability)
   - Security (improve security posture)
   - All (balanced improvement across dimensions)

3. **Depth of expertise needed?**
   - Quick suggestions (surface-level improvements)
   - Comprehensive analysis (detailed review with priorities)
   - Deep architectural redesign (consider fundamental changes)

---

## Refactoring Types

### Quick Refactoring (Targeted)
**Scope**: Single function, class, or small section
**Time**: 15-60 minutes
**Focus**: Immediate clarity improvements

**Techniques**:
- Extract method/function
- Rename variables for clarity
- Remove duplicate logic
- Simplify conditionals
- Extract magic numbers to constants
- Improve function signatures

**Example**:
```python
# Before
def process(x, y, z):
    result = x * y + z
    return result if result > 0 else 0

# After
def calculate_adjusted_value(base, multiplier, adjustment):
    """Calculate value with minimum floor of zero."""
    raw_value = base * multiplier + adjustment
    return max(0, raw_value)
```

### Module-Level Refactoring
**Scope**: Entire module, feature, or component
**Time**: 1-4 hours
**Focus**: Structure and organization

**Techniques**:
- Reorganize class responsibilities
- Extract helper classes/functions
- Consolidate related functions
- Improve separation of concerns
- Reduce interdependencies
- Extract interfaces

**Checklist**:
- [ ] All functions have clear, single purpose
- [ ] Related logic grouped together
- [ ] Dependencies are explicit
- [ ] No circular dependencies
- [ ] Testability improved
- [ ] Code duplication reduced

### System-Level Refactoring
**Scope**: Multiple modules/systems, architectural changes
**Time**: 1-3 days
**Focus**: Fundamental improvements

**Techniques**:
- Redesign module interfaces
- Refactor data models
- Improve error handling patterns
- Restructure for scalability
- Implement design patterns
- Reduce coupling across systems

**Considerations**:
- Backward compatibility impacts
- Migration strategy for existing code
- Testing approach (incremental vs full)
- Performance implications
- Documentation updates needed

---

## Refactoring by Goal

### Goal: Clarity

**Techniques**:
1. **Rename for clarity** (variables, functions, classes)
   - Use domain language
   - Avoid abbreviations (unless standard)
   - Make intent obvious

2. **Extract complex logic** into well-named functions
   - Each function should be understandable in seconds
   - Comments should explain "why", not "what"

3. **Simplify conditionals**
   - Reduce nesting depth (max 2-3 levels)
   - Use guard clauses to exit early
   - Extract complex boolean logic to named functions

4. **Improve structure**
   - Group related code together
   - Remove dead code
   - Separate concerns

**Example**:
```python
# Before (unclear)
def process_payment(amount, tax, discount, method):
    if method == 'cc':
        total = amount * (1 + tax) - discount
        if total > 0:
            # process credit card
            return charge_cc(total)
    elif method == 'bank':
        # similar logic repeated
        pass
    return None

# After (clear intent)
def process_payment(amount: float, tax_rate: float, discount: float, payment_method: str) -> Payment:
    """Process payment with tax and discount applied."""
    total = calculate_final_amount(amount, tax_rate, discount)
    validate_payment_amount(total)

    processor = get_payment_processor(payment_method)
    return processor.charge(total)
```

### Goal: Performance

**Analysis First**:
1. Profile the code to identify bottlenecks
2. Measure baseline performance
3. Apply targeted optimizations
4. Verify improvement with metrics

**Common Optimizations**:
- Reduce algorithm complexity (O(n²) → O(n log n))
- Cache expensive computations
- Batch database operations
- Lazy load data when possible
- Use appropriate data structures
- Minimize allocations in hot loops
- Parallelize independent operations

**Verification**:
- [ ] Profiled and identified bottleneck
- [ ] Measured baseline performance
- [ ] Applied optimization
- [ ] Verified improvement (minimum 10-20%)
- [ ] No regression in other areas
- [ ] Trade-offs documented

### Goal: Maintainability

**Techniques**:
1. **Apply SOLID principles**
   - Single Responsibility: one reason to change
   - Open/Closed: open for extension, closed for modification
   - Liskov Substitution: interchangeable implementations
   - Interface Segregation: small, focused interfaces
   - Dependency Inversion: depend on abstractions

2. **Reduce duplication** (DRY principle)
   - Extract common logic to shared functions
   - Use inheritance or composition for shared behavior
   - Consolidate similar patterns

3. **Improve testability**
   - Inject dependencies (easier to mock)
   - Separate concerns (easier to test in isolation)
   - Remove hidden state (easier to reason about)
   - Use pure functions when possible

4. **Better abstractions**
   - Hide implementation details
   - Expose only necessary interfaces
   - Use meaningful types/classes

**Example**:
```python
# Before (low maintainability)
class UserService:
    def __init__(self, db_host, db_user, db_pass):
        self.db = connect_db(db_host, db_user, db_pass)

    def get_user(self, user_id):
        # tight coupling to DB implementation
        return self.db.query(f"SELECT * FROM users WHERE id={user_id}")

# After (improved maintainability)
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository  # dependency injection

    def get_user(self, user_id: UserId) -> User:
        """Retrieve user by ID, raising NotFound if missing."""
        return self.repository.find_by_id(user_id)

# Easy to test - inject mock repository
class MockUserRepository:
    def find_by_id(self, user_id):
        return User(id=user_id, name="Test User")

service = UserService(MockUserRepository())
user = service.get_user(UserId(123))
```

### Goal: Testability

**Improvements**:
1. **Reduce dependencies** - fewer things to mock/set up
2. **Extract logic** - separate logic from infrastructure
3. **Pure functions** - no hidden state to manage
4. **Small methods** - easier to test in isolation
5. **Clear interfaces** - obvious contracts to test against

**Refactoring Pattern**:
```python
# Before (hard to test)
def process_order(order_id):
    order = database.get_order(order_id)  # hidden dependency
    if order is None:
        send_email("Order not found")  # hidden dependency
        return False
    total = order.items.sum(lambda x: x.price)
    database.update_order(order_id, {"total": total})  # hidden dependency
    return True

# After (easy to test)
def calculate_order_total(items: List[Item]) -> Decimal:
    """Pure function - no dependencies."""
    return sum(item.price for item in items)

def process_order(order_id: int, repository: OrderRepository, notifier: Notifier) -> bool:
    """Testable - dependencies injected."""
    order = repository.get_order(order_id)
    if not order:
        notifier.send_not_found(order_id)
        return False

    total = calculate_order_total(order.items)
    repository.update_total(order_id, total)
    return True

# Easy to test
def test_process_order():
    mock_repo = MockRepository()
    mock_notifier = MockNotifier()
    assert process_order(123, mock_repo, mock_notifier) == True
```

---

## Refactoring Process

### Step 1: Understand Current State
- [ ] Read the code thoroughly
- [ ] Identify why it needs refactoring
- [ ] Run tests (should be passing)
- [ ] Measure baseline (performance, complexity, coverage)
- [ ] Document current behavior

### Step 2: Plan Refactoring
- [ ] Identify target state (what should improve?)
- [ ] Break into small, safe steps
- [ ] Plan testing strategy
- [ ] Consider rollback options

### Step 3: Refactor Incrementally
- [ ] Make one small change at a time
- [ ] Run tests after each change
- [ ] Commit working versions frequently
- [ ] Don't mix refactoring with new features

### Step 4: Verify Improvements
- [ ] Run full test suite
- [ ] Measure final metrics
- [ ] Compare before/after
- [ ] Document changes
- [ ] Code review before merging

### Step 5: Update Documentation
- [ ] Update design documentation
- [ ] Update code comments (if needed)
- [ ] Update related documentation
- [ ] Share learnings with team

---

## Refactoring Safety Checklist

- [ ] **Tests passing** - full suite passes before refactoring starts
- [ ] **Incremental changes** - small, reviewable changes
- [ ] **Tests re-run** - run tests after each change
- [ ] **No feature changes** - refactoring only, no new behavior
- [ ] **Backwards compatible** - API changes documented
- [ ] **Performance verified** - measure if performance is a goal
- [ ] **Code reviewed** - another developer reviews changes
- [ ] **Documented** - explain why refactoring was needed

---

## Common Refactoring Patterns

### Extract Method
```python
# Before
def calculate_price(items):
    total = sum(item.price for item in items)
    tax = total * 0.1
    return total + tax

# After
def calculate_subtotal(items):
    return sum(item.price for item in items)

def apply_tax(subtotal):
    return subtotal * 1.1

def calculate_price(items):
    subtotal = calculate_subtotal(items)
    return apply_tax(subtotal)
```

### Extract Class
```python
# Before - God object
class User:
    def __init__(self, name, email, street, city, country):
        self.name = name
        self.email = email
        self.address = f"{street}, {city}, {country}"

    def send_email(self, message):
        # email sending logic
        pass

# After - Separated concerns
class User:
    def __init__(self, name: str, email: str, address: Address):
        self.name = name
        self.email = email
        self.address = address

class Address:
    def __init__(self, street: str, city: str, country: str):
        self.street = street
        self.city = city
        self.country = country
```

### Replace Conditional with Polymorphism
```python
# Before
def apply_discount(customer, price):
    if customer.type == 'premium':
        return price * 0.8
    elif customer.type == 'regular':
        return price * 0.9
    else:
        return price

# After
class Customer:
    def apply_discount(self, price):
        raise NotImplementedError

class PremiumCustomer(Customer):
    def apply_discount(self, price):
        return price * 0.8

class RegularCustomer(Customer):
    def apply_discount(self, price):
        return price * 0.9

# Usage
discounted = customer.apply_discount(price)
```

---

## Anti-Patterns to Avoid

❌ **Refactor while adding features** - causes bugs, harder to review
✅ **Do refactoring separately** - easier to review, easier to revert if needed

❌ **Refactor without tests** - no safety net
✅ **Ensure tests pass first** - green before refactoring

❌ **Large refactorings** - hard to review, easy to miss bugs
✅ **Small, incremental changes** - easier to understand and verify

❌ **Refactor code you don't understand** - will introduce bugs
✅ **Understand code first** - read, test, then refactor

❌ **Change APIs during refactoring** - breaks clients
✅ **Maintain API contracts** - refactor internals, preserve interfaces

---

## Refactoring Depth Guidelines

### Quick (Surface Level)
**Use when**: Need quick improvements, tight time constraints
**Techniques**: Renaming, extract method, remove dead code
**Time**: 15-60 minutes
**Risk**: Low
**Review**: Code review sufficient

### Comprehensive (Module Level)
**Use when**: Improving module quality, preparing for expansion
**Techniques**: SOLID principles, design patterns, restructure
**Time**: 2-8 hours
**Risk**: Medium (test thoroughly)
**Review**: Code review + testing

### Deep (Architectural)
**Use when**: Fundamental improvements needed, performance critical
**Techniques**: New design patterns, data structure changes, algorithm improvement
**Time**: 1-3 days
**Risk**: High (needs planning, testing, gradual rollout)
**Review**: Design review + comprehensive testing + gradual migration

---

## Related Content

- For analysis: `analyze-codebase.prompt.md` (understand current state)
- For testing: `test-breakdown.prompt.md` (testing strategy)
- For code review: Use expert code-review agents
- For performance: Profile first with specialized tools
- For design: `arch-gen-blueprint.prompt.md` (architecture planning)

---

## Questions to Ask Before Refactoring

1. **Why is this code hard to work with?** (clarity, performance, maintainability?)
2. **How will I know refactoring succeeded?** (specific metrics, tests, feedback)
3. **What could go wrong?** (risks, breaking changes, performance regressions)
4. **How will I verify safety?** (tests, gradual rollout, rollback plan)
5. **Is this the right time?** (after feature is stable, before next iteration)
6. **Do I have tests?** (must have tests before refactoring)

---

## Next Steps

After refactoring:
1. [ ] Verify all tests pass
2. [ ] Compare before/after metrics
3. [ ] Document improvements made
4. [ ] Share with team/code review
5. [ ] Update related documentation
6. [ ] Consider applying pattern elsewhere
