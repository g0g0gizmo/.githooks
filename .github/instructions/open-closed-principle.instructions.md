---
description: 'Software should be open for extension, closed for modification - enabling safe evolution'
applyTo: '**/*'
---

# Open/Closed Principle (OCP)

## Core Concept

**Definition**: Software should be **open for extension, closed for modification**.

In other words: Add new features without changing existing code.

**Why**: Changes to existing code risk breaking things. Extensions add safely.

## The Test

Can I add a feature without touching existing code?

- ✅ Yes (create new class)
- ❌ No (must edit existing class)

## Anti-Pattern: Modification Required

```typescript
// ❌ To add new payment type, must modify existing code
class PaymentProcessor {
  process(type: string, amount: number) {
    if (type === 'credit') {
      // credit logic
    } else if (type === 'paypal') {
      // paypal logic
    }
    // To add Stripe: modify this function!
  }
}
```

**Problem**:

- Adding Stripe means changing existing, tested code
- Risk of breaking credit card or PayPal processing
- Violates [Single Responsibility Principle](./single-responsibility-principle.instructions.md) - changes for multiple reasons
- Testing requires re-testing all payment types

## Proper Implementation

```typescript
// ✅ New payment types added without modifying existing code
interface PaymentMethod {
  process(amount: number): boolean;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number) {
    // Credit card specific logic
  }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number) {
    // PayPal specific logic
  }
}

class StripePayment implements PaymentMethod {
  process(amount: number) {
    // Stripe specific logic
  }
  // New! No existing code changed.
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}

  process(amount: number) {
    return this.method.process(amount);
  }
}
```

**Benefits**:

- Add new payment methods by creating new classes
- Existing code remains untouched and stable
- Each payment method tested independently
- No risk of regression in existing payments

## Design Strategies

### Strategy 1: Abstraction + Polymorphism

Use interfaces/abstract classes to define extension points:

```typescript
interface NotificationChannel {
  send(message: string, recipient: string): void;
}

// Extensions don't modify existing code
class EmailNotification implements NotificationChannel { }
class SmsNotification implements NotificationChannel { }
class SlackNotification implements NotificationChannel { }
```

### Strategy 2: Plugin Architecture

```typescript
interface Plugin {
  name: string;
  execute(context: Context): void;
}

class PluginManager {
  private plugins: Plugin[] = [];

  register(plugin: Plugin) {
    this.plugins.push(plugin);
  }

  executeAll(context: Context) {
    this.plugins.forEach(p => p.execute(context));
  }
}
```

### Strategy 3: Template Method Pattern

```typescript
abstract class DataProcessor {
  process(data: Data) {
    const validated = this.validate(data);
    const transformed = this.transform(validated);
    return this.save(transformed);
  }

  abstract validate(data: Data): Data;
  abstract transform(data: Data): Data;
  abstract save(data: Data): void;
}

// Extensions override specific methods
class CsvDataProcessor extends DataProcessor { }
class JsonDataProcessor extends DataProcessor { }
```

## Identifying Violations

**Warning Signs**:

- Long if-else or switch statements on type codes
- Frequently modified classes
- "Just one more case" syndrome
- Fear of touching existing code
- Regression bugs after adding features

## When to Apply

**Apply OCP when**:

- Feature variations are likely
- Code is used by multiple clients
- Building frameworks or libraries
- High cost of bugs in existing code

**Balance with**:

- [YAGNI Principle](../../.github/instructions/yagni-principle.instructions.md) - Don't over-abstract prematurely
- Simplicity - Sometimes modification is simpler than abstraction
- Known requirements - Don't guess at future extensions

## Trade-offs

**Advantages**:

- ✅ Stable existing code
- ✅ Safe to extend
- ✅ Parallel development possible
- ✅ Easier testing

**Disadvantages**:

- ❌ More upfront design
- ❌ Additional abstraction layers
- ❌ Potentially more files/classes
- ❌ Can be over-engineered

## Relationships

**Requires**:

- [Single Responsibility Principle](./single-responsibility-principle.instructions.md) - Clear extension points
- [Dependency Inversion Principle](../../.github/instructions/dependency-inversion-principle.instructions.md) - Depend on abstractions

**Enables**:

- [Liskov Substitution Principle](../../.github/instructions/liskov-substitution-principle.instructions.md) - Polymorphic extensions

**Part of**:

- [SOLID Principles](../../.github/instructions/solid-principles.instructions.md) - Enables safe evolution

## Real-World Example

### Report Generator

**Bad** (Closed for Extension):

```typescript
class ReportGenerator {
  generate(data: Data, format: string) {
    if (format === 'pdf') {
      return this.generatePdf(data);
    } else if (format === 'excel') {
      return this.generateExcel(data);
    } else if (format === 'csv') {
      return this.generateCsv(data);
    }
    // Need to modify this method for new formats!
  }
}
```

**Good** (Open for Extension):

```typescript
interface ReportFormatter {
  format(data: Data): Report;
}

class PdfFormatter implements ReportFormatter {
  format(data: Data): Report { }
}

class ExcelFormatter implements ReportFormatter {
  format(data: Data): Report { }
}

class CsvFormatter implements ReportFormatter {
  format(data: Data): Report { }
}

class ReportGenerator {
  constructor(private formatter: ReportFormatter) {}

  generate(data: Data): Report {
    return this.formatter.format(data);
  }
}

// Adding JSON support - no existing code changes!
class JsonFormatter implements ReportFormatter {
  format(data: Data): Report { }
}
```

## Checklist

Before adding a feature, verify:

- [ ] Can I add this without modifying existing classes?
- [ ] Are extension points defined via interfaces/abstractions?
- [ ] Would a switch/if-else chain grow with new features?
- [ ] Is polymorphism used instead of type checking?
- [ ] Can existing code remain stable?
- [ ] Are new features additive, not modifications?

## Why Open/Closed Matters

✅ **Stability** - Existing code remains untouched and proven
✅ **Safety** - Extensions don't risk breaking existing functionality
✅ **Testability** - New extensions tested independently
✅ **Maintainability** - Changes are additive, not modifications
✅ **Parallel Development** - Teams can add features without conflicts

Master Open/Closed, and your codebase evolves safely through extension rather than risky modification.
