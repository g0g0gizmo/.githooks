# Code Smell: Temporary Field

**Purpose**: Identify and avoid fields only sometimes populated
**Audience**: You + AI (code review, refactoring)
**Category**: Object-Orientation Abusers (OOP Gone Wrong)
**Severity**: 🟡 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Temporary Field** occurs when an object has fields that are only used in certain scenarios.

Fields should always have meaningful values. When a field is empty/null for most of an object's lifetime, it indicates design problems or that the field belongs in a different class.

### Why It Matters

Temporary fields cause:

- ❌ Confusing when fields are populated
- ❌ Easy to forget to initialize
- ❌ Hard to understand object state
- ❌ Null checks scattered throughout code
- ❌ Indicates incomplete design

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Fields only sometimes populated
class Wizard {
  name: string;
  level: number;
  spell?: string;           // Only used during castSpell()
  spellTarget?: string;     // Only used during castSpell()
  spellPower?: number;      // Only used during castSpell()

  castSpell(spell: string, target: string, power: number): void {
    this.spell = spell;
    this.spellTarget = target;
    this.spellPower = power;

    // Use the temporary fields
    console.log(`${this.name} casts ${this.spell} on ${this.spellTarget}`);

    // Clear them after
    this.spell = undefined;
    this.spellTarget = undefined;
    this.spellPower = undefined;
  }

  attack(): void {
    // spell, spellTarget, spellPower are undefined here!
    console.log(`${this.name} attacks`);
  }
}

// Problems:
// - spell, spellTarget, spellPower empty most of the time
// - Must check if defined before use
// - Easy to forget to initialize
// - Unclear what valid states are
```

**Symptoms**:

- [ ] Fields with `?` (optional) but used frequently
- [ ] Fields initialized in some methods but not others
- [ ] Null checks for specific fields
- [ ] Comments like "only used in X scenario"
- [ ] Fields set then immediately cleared
- [ ] Not all methods use all fields
- [ ] Fields have "temporary" in name or comments

---

## 💔 Why It's Bad

### Problem 1: Confusing Object State

```typescript
// ❌ Unclear when fields are valid
class ReportGenerator {
  reportTitle: string;
  reportDate?: Date;
  reportContent?: string;  // Only set after generate()
  reportFormat?: string;   // Only set if user specifies

  generate(title: string): void {
    this.reportTitle = title;
    this.reportDate = new Date();
  }

  setFormat(format: string): void {
    this.reportFormat = format;
  }

  render(): string {
    // reportContent might be undefined!
    // Must check or will crash
    return this.reportContent || '';
  }
}

// What states is ReportGenerator valid in?
// After constructor? After generate()? After setFormat()?
// Unclear!
```

### Problem 2: Null Checks Everywhere

```typescript
// ❌ Must check temporary fields constantly
class Order {
  items: OrderItem[];
  specialDiscount?: number;  // Only for VIP orders

  getTotal(): number {
    let total = this.items.reduce((sum, item) => sum + item.price, 0);

    // Must check if specialDiscount exists
    if (this.specialDiscount) {
      total -= this.specialDiscount;
    }

    return total;
  }

  applyTax(): number {
    // Must check again
    let taxable = this.items.reduce((sum, item) => sum + item.price, 0);

    if (this.specialDiscount) {
      taxable -= this.specialDiscount;
    }

    return taxable * 0.08;
  }

  getDescription(): string {
    // And again
    let description = `Order with ${this.items.length} items`;

    if (this.specialDiscount) {
      description += ` (VIP discount: ${this.specialDiscount})`;
    }

    return description;
  }
}

// Check repeated in every method
// What if we forget one?
```

### Problem 3: Missing Initialization

```typescript
// ❌ Easy to forget temporary fields
class PaymentProcessor {
  amount?: number;
  currency?: string;
  paymentMethod?: string;

  constructor() {
    // Forgot to initialize temporary fields!
  }

  processPayment(amount: number, currency: string, method: string): void {
    this.amount = amount;
    this.currency = currency;
    this.paymentMethod = method;
  }

  log(): void {
    // amount might be undefined!
    console.log(`Processing ${this.amount} ${this.currency}`);
  }
}

const processor = new PaymentProcessor();
processor.log();  // Logs "undefined undefined"
processor.processPayment(100, 'USD', 'card');
processor.log();  // Now logs correctly
```

---

## ✅ Refactoring Solutions

### Solution 1: Extract Class

```typescript
// ❌ BEFORE: Temporary spell fields
class Wizard {
  name: string;
  level: number;
  spell?: string;
  spellTarget?: string;
  spellPower?: number;

  castSpell(spell: string, target: string, power: number): void {
    this.spell = spell;
    this.spellTarget = target;
    this.spellPower = power;
    // Use fields
  }
}

// ✅ AFTER: Extract Spell class
class Spell {
  constructor(
    readonly name: string,
    readonly target: string,
    readonly power: number
  ) {}
}

class Wizard {
  name: string;
  level: number;

  castSpell(spell: Spell): void {
    // Use spell object, not scattered fields
    console.log(`${this.name} casts ${spell.name} on ${spell.target}`);
  }
}
```

### Solution 2: Introduce Parameter Object

```typescript
// ❌ BEFORE: Temporary fields for calculation
class PriceCalculator {
  basePrice?: number;
  discountPercent?: number;
  taxRate?: number;

  calculate(base: number, discount: number, tax: number): number {
    this.basePrice = base;
    this.discountPercent = discount;
    this.taxRate = tax;

    const discounted = this.basePrice * (1 - this.discountPercent / 100);
    const final = discounted * (1 + this.taxRate / 100);

    // Clear temporary fields
    this.basePrice = undefined;
    this.discountPercent = undefined;
    this.taxRate = undefined;

    return final;
  }
}

// ✅ AFTER: Use parameter object
class PriceRequest {
  constructor(
    readonly basePrice: number,
    readonly discountPercent: number,
    readonly taxRate: number
  ) {}
}

class PriceCalculator {
  calculate(request: PriceRequest): number {
    const discounted = request.basePrice * (1 - request.discountPercent / 100);
    return discounted * (1 + request.taxRate / 100);
  }
}
```

### Solution 3: Create Separate Class for Variants

```typescript
// ❌ BEFORE: Different temporary fields for different cases
class ReportGenerator {
  content: string;
  sqlQuery?: string;        // Only for DB reports
  fileContent?: string;     // Only for file reports
  apiEndpoint?: string;     // Only for API reports

  generateFromDatabase(query: string): string {
    this.sqlQuery = query;
    // Process
  }

  generateFromFile(filePath: string): string {
    this.fileContent = filePath;
    // Process
  }

  generateFromAPI(endpoint: string): string {
    this.apiEndpoint = endpoint;
    // Process
  }
}

// ✅ AFTER: Separate classes
abstract class ReportGenerator {
  abstract generate(): string;
}

class DatabaseReportGenerator extends ReportGenerator {
  constructor(private query: string) {}

  generate(): string {
    // Use query directly
  }
}

class FileReportGenerator extends ReportGenerator {
  constructor(private filePath: string) {}

  generate(): string {
    // Use filePath directly
  }
}

class APIReportGenerator extends ReportGenerator {
  constructor(private endpoint: string) {}

  generate(): string {
    // Use endpoint directly
  }
}
```

### Solution 4: Use Builder Pattern

```typescript
// ❌ BEFORE: Temporary configuration fields
class EmailBuilder {
  from?: string;
  to?: string;
  subject?: string;
  body?: string;
  cc?: string[];

  send(): void {
    // Check if all fields set
    if (!this.from || !this.to || !this.subject || !this.body) {
      throw new Error('Missing required fields');
    }
    // Send
  }
}

// ✅ AFTER: Build then use
class Email {
  constructor(
    readonly from: string,
    readonly to: string,
    readonly subject: string,
    readonly body: string,
    readonly cc?: string[]
  ) {}
}

class EmailBuilder {
  private from?: string;
  private to?: string;
  private subject?: string;
  private body?: string;
  private cc?: string[];

  setFrom(from: string) {
    this.from = from;
    return this;
  }

  setTo(to: string) {
    this.to = to;
    return this;
  }

  setSubject(subject: string) {
    this.subject = subject;
    return this;
  }

  setBody(body: string) {
    this.body = body;
    return this;
  }

  setCc(cc: string[]) {
    this.cc = cc;
    return this;
  }

  build(): Email {
    if (!this.from || !this.to || !this.subject || !this.body) {
      throw new Error('Missing required fields');
    }
    return new Email(this.from, this.to, this.subject, this.body, this.cc);
  }
}

// Use:
const email = new EmailBuilder()
  .setFrom('sender@example.com')
  .setTo('recipient@example.com')
  .setSubject('Hello')
  .setBody('Message')
  .build();
```

### Solution 5: Move to Subclass

```typescript
// ❌ BEFORE: Optional fields only in special case
class Person {
  name: string;
  age: number;
  specialCertification?: string;  // Only for certified professionals
  certificationLevel?: number;    // Only for certified professionals

  isCertified(): boolean {
    return !!this.specialCertification;
  }
}

// ✅ AFTER: Use inheritance
abstract class Person {
  constructor(
    readonly name: string,
    readonly age: number
  ) {}
}

class RegularPerson extends Person {}

class CertifiedProfessional extends Person {
  constructor(
    name: string,
    age: number,
    readonly specialCertification: string,
    readonly certificationLevel: number
  ) {
    super(name, age);
  }
}

// Now fields always exist for CertifiedProfessional
```

---

## 🔍 Detecting Temporary Fields

**Watch for patterns**:

- Fields with `?` (optional) that are frequently used
- Methods that initialize only some fields
- `this.field = undefined` to clear values
- Null checks before using field
- Comments like "only used in X"

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Class should have clear, consistent responsibility
- **SOLID-S** - Object should have one valid state, not multiple
- **Orthogonality** - Temporary fields create coupling to scenarios

---

## ✅ Checklist: Avoid Temporary Fields

When writing code:

- [ ] Are these fields only populated in certain methods?
- [ ] Do some methods skip initializing these fields?
- [ ] Could these belong in a separate class?
- [ ] Am I checking if fields are defined before use?
- [ ] Would extracting make the code clearer?

---

## ✨ Remember

**DON'T DO**: Create fields that are only sometimes populated.

**DO**: Extract temporary fields into their own classes.

**Rule of thumb**: If a field isn't used by all methods, move it to a separate class.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-temporary-field.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Remove temporary fields. Extract into focused classes.**
