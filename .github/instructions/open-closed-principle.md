# Open/Closed Principle (OCP)

**Purpose**: Software should be open for extension, closed for modification
**Audience**: Developers, architects, framework designers
**Focus**: Extensibility without breaking existing code

---

## 🎯 Core Concept

**Definition**: Software should be **open for extension, closed for modification**.

In other words: Add new features without changing existing code.

**Why**: Changes to existing code risk breaking things. Extensions add safely.

---

## 📝 The Test

Can I add a feature without touching existing code?

- ✅ Yes (create new class)
- ❌ No (must edit existing class)

---

## ❌ Anti-Pattern: Modification Required

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
- Violates [Single Responsibility](../../.github/copilot/core/principles/single-responsibility-principle.md) - changes for multiple reasons
- Testing requires re-testing all payment types

---

## ✅ Proper Implementation

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

---

## 🎨 Design Strategies

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

---

## 🔍 Identifying Violations

**Warning Signs**:

- Long if-else or switch statements on type codes
- Frequently modified classes
- "Just one more case" syndrome
- Fear of touching existing code
- Regression bugs after adding features

---

## 🎓 When to Apply

**Apply OCP when**:

- Feature variations are likely
- Code is used by multiple clients
- Building frameworks or libraries
- High cost of bugs in existing code

**Balance with**:

- [YAGNI](../../.github/copilot/core/principles/no-fortune-telling.md) - Don't over-abstract prematurely
- Simplicity - Sometimes modification is simpler than abstraction
- Known requirements - Don't guess at future extensions

---

## ⚖️ Trade-offs

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

---

## 🔗 Relationships

**Requires**:

- [Single Responsibility](../../.github/copilot/core/principles/single-responsibility-principle.md) - Clear extension points
- [Dependency Inversion](../../.github/copilot/core/principles/dependency-inversion-principle.md) - Depend on abstractions

**Enables**:

- [Liskov Substitution](../../.github/copilot/core/principles/liskov-substitution-principle.md) - Polymorphic extensions
- [Plugin Architecture](../../.github/copilot/core/principles/plugin-architecture.md) - Runtime extensibility

**Related Concepts**:

- [Strategy Pattern](../../.github/copilot/core/principles/strategy-pattern.md) - Runtime algorithm selection
- [Template Method](../../.github/copilot/core/principles/template-method-pattern.md) - Fixed algorithm, variable steps
- [Factory Pattern](../../.github/copilot/core/principles/factory-pattern.md) - Object creation without modification

**Part of**:

- [SOLID Principles](../../.github/copilot/core/principles/SOLID.md) - Enables safe evolution

---

## 📚 Real-World Example

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

---

## ✅ Checklist

Before adding a feature, verify:

- [ ] Can I add this without modifying existing classes?
- [ ] Are extension points defined via interfaces/abstractions?
- [ ] Would a switch/if-else chain grow with new features?
- [ ] Is polymorphism used instead of type checking?
- [ ] Can existing code remain stable?
- [ ] Are new features additive, not modifications?

---

**Version**: 1.0
**Created**: 2025-11-28
**Last Updated**: 2025-11-28
**Tags**: #solid #design-principles #extensibility #polymorphism
