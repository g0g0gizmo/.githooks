# Code Smell: Long Parameter List

**Purpose**: Identify and avoid functions with too many parameters
**Audience**: You + AI (code review, refactoring)
**Category**: Bloaters (Code That's Too Much)
**Severity**: 🟡 MEDIUM-HIGH
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Long Parameter List** is a function that requires too many parameters to be called.

Functions should have few parameters (ideally 1-3). When a function needs 5+ parameters, it usually indicates:
- Function does too much
- Parameters should be grouped into objects
- Function is too tightly coupled to its callers

### Why It Matters

Long parameter lists are:
- ❌ Hard to remember (parameter order matters)
- ❌ Easy to misuse (wrong parameters, wrong order)
- ❌ Hard to extend (adding parameters breaks all callers)
- ❌ Hard to test (must provide many test values)
- ❌ Indicates design problems (too many concerns)

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Long Parameter List
function calculatePrice(
  productId,
  quantity,
  customerId,
  discountPercentage,
  taxRate,
  shippingCost,
  insuranceFee,
  warehouseFee,
  handlingFee,
  promotionCode,
  loyaltyPoints,
  regionId,
  channelId,
  currency,
  timezone
) {
  // 15 parameters!
  // What's the order again?
  // Which are optional?
  // What if I forget one?
}

// Usage (error-prone):
calculatePrice(
  123,                 // productId?
  5,                   // quantity?
  456,                 // customerId?
  0.2,                 // discountPercentage?
  0.08,                // taxRate?
  10,                  // shippingCost?
  2,                   // insuranceFee?
  1,                   // warehouseFee?
  0.5,                 // handlingFee?
  'SUMMER20',          // promotionCode?
  100,                 // loyaltyPoints?
  'US_EAST',           // regionId?
  'ONLINE',            // channelId?
  'USD',               // currency?
  'EST'                // timezone?
);

// Easy to pass parameters in wrong order
// Easy to forget one
// Easy to misunderstand
```

**Symptoms**:
- [ ] Function has 5+ parameters
- [ ] Parameter order is important (hard to remember)
- [ ] Parameters seem unrelated
- [ ] Callers repeat the same parameter combinations
- [ ] Hard to test (must provide many values)
- [ ] Adding new parameter breaks all callers
- [ ] Some callers don't use all parameters

---

## 💔 Why It's Bad

### Problem 1: Wrong Order

```typescript
// ❌ Easy to confuse parameter order
function createUser(email, password, name, age, country, role, status) {
  // ...
}

// Called correctly:
createUser('john@example.com', 'pass123', 'John', 30, 'US', 'admin', 'active');

// Called wrong (hard to spot):
createUser('john@example.com', 'pass123', 30, 'John', 'US', 'active', 'admin');
// Age and name swapped, role and status swapped
// Runtime error deep in the logic
```

### Problem 2: Adding Parameters Breaks Everything

```typescript
// Original function
function sendEmail(to, subject, body) { }

// Calls everywhere:
sendEmail('user@example.com', 'Welcome', 'Hello user');

// Requirement: Add CC parameter
function sendEmail(to, cc, subject, body) { }

// NOW ALL CALLS BREAK!
// Must find and update every call site
// Easy to miss one, creating bugs
```

### Problem 3: Hard to Test

```typescript
// ❌ Testing function with many parameters
describe('calculatePrice', () => {
  it('should calculate correct price', () => {
    const result = calculatePrice(
      123,      // productId
      5,        // quantity
      456,      // customerId
      0.2,      // discountPercentage
      0.08,     // taxRate
      10,       // shippingCost
      2,        // insuranceFee
      1,        // warehouseFee
      0.5,      // handlingFee
      'SUMMER', // promotionCode
      100,      // loyaltyPoints
      'US',     // regionId
      'WEB',    // channelId
      'USD',    // currency
      'EST'     // timezone
    );

    expect(result).toBe(expectedValue);
  });

  // Test setup longer than actual test!
  // Hard to understand what's being tested
  // Hard to change one parameter without breaking others
});
```

### Problem 4: Indicates Design Problem

```typescript
// ❌ Many parameters = function does too much
function processOrder(
  orderId,
  customerId,
  items,
  shippingAddress,
  billingAddress,
  paymentMethod,
  discountCode,
  taxRate,
  shippingCost,
  insuranceOption,
  giftWrap,
  giftMessage,
  notificationPreferences,
  analyticsData
) {
  // This function probably:
  // - Validates data
  // - Calculates totals
  // - Processes payment
  // - Sends emails
  // - Logs events
  // - Updates database
  // Too much!
}
```

---

## ✅ Refactoring Solutions

### Solution 1: Introduce Parameter Object

```typescript
// ✅ FIXED: Group related parameters

interface PricingRequest {
  productId: number;
  quantity: number;
  customerId: number;
}

interface Discounts {
  percentage: number;
  promotionCode: string;
  loyaltyPoints: number;
}

interface Costs {
  tax: number;
  shipping: number;
  insurance: number;
  warehouse: number;
  handling: number;
}

interface Context {
  region: string;
  channel: string;
  currency: string;
  timezone: string;
}

function calculatePrice(
  request: PricingRequest,
  discounts: Discounts,
  costs: Costs,
  context: Context
): number {
  // Clear what each parameter is
  // Easy to add new fields
  // Easy to test
  // Self-documenting
}

// Usage (clear):
const price = calculatePrice(
  { productId: 123, quantity: 5, customerId: 456 },
  { percentage: 0.2, promotionCode: 'SUMMER20', loyaltyPoints: 100 },
  { tax: 0.08, shipping: 10, insurance: 2, warehouse: 1, handling: 0.5 },
  { region: 'US_EAST', channel: 'ONLINE', currency: 'USD', timezone: 'EST' }
);
```

### Solution 2: Preserve Whole Object

```typescript
// ❌ BEFORE: Extract individual fields
function calculateTotal(email, name, age, country, status, purchaseHistory, preferences) {
  // 7 parameters
}

// ✅ AFTER: Pass entire object
interface Customer {
  email: string;
  name: string;
  age: number;
  country: string;
  status: string;
  purchaseHistory: Purchase[];
  preferences: Preferences;
}

function calculateTotal(customer: Customer): number {
  // 1 parameter
  // All customer data available
  // Easy to extend without changing signature
}
```

### Solution 3: Use Builder Pattern

```typescript
// ✅ For complex construction
class EmailBuilder {
  private email: any = {};

  to(recipient: string) {
    this.email.to = recipient;
    return this;
  }

  cc(recipients: string[]) {
    this.email.cc = recipients;
    return this;
  }

  subject(subject: string) {
    this.email.subject = subject;
    return this;
  }

  body(body: string) {
    this.email.body = body;
    return this;
  }

  attachments(files: string[]) {
    this.email.attachments = files;
    return this;
  }

  build() {
    return this.email;
  }
}

// Usage (clear, flexible):
const email = new EmailBuilder()
  .to('user@example.com')
  .cc(['admin@example.com'])
  .subject('Welcome')
  .body('Hello!')
  .attachments(['logo.png'])
  .build();

sendEmail(email);
```

### Solution 4: Extract Method

```typescript
// ❌ BEFORE: One function with many parameters
function processUserRegistration(
  email,
  password,
  name,
  address,
  city,
  state,
  zip,
  country,
  phone,
  birthDate,
  preferences
) {
  // 11 parameters!
}

// ✅ AFTER: Extract into smaller functions
function validateUserInput(email, password, name) {
  // 3 parameters - validation focused
}

function validateAddress(address, city, state, zip, country) {
  // 5 parameters - address focused
}

function createUserProfile(email, name, birthDate, preferences) {
  // 4 parameters - profile focused
}

function processUserRegistration(userData) {
  validateUserInput(userData.email, userData.password, userData.name);
  validateAddress(userData.address, userData.city, userData.state, userData.zip, userData.country);
  createUserProfile(userData.email, userData.name, userData.birthDate, userData.preferences);
}
```

---

## 🔍 The Parameter Count Rule

**Guideline**: Functions should have 1-3 parameters.

| Count | Status | Action |
|-------|--------|--------|
| 0-1 parameter | ✅ Good | Ideal |
| 2-3 parameters | ✅ Good | Normal |
| 4 parameters | ⚠️ Watch | Consider grouping |
| 5+ parameters | 🚩 Problem | Definitely group |
| 7+ parameters | 🔴 Critical | Extract immediately |

---

## 🔄 Parameter Type Levels

**Level 1**: Primitives (string, number, boolean)
```typescript
function sendEmail(to: string, subject: string, body: string) { }
// 3 parameters OK
```

**Level 2**: One object
```typescript
function sendEmail(config: EmailConfig) { }
// 1 parameter, cleaner
```

**Level 3**: Different object types
```typescript
function createOrder(request: OrderRequest, customer: Customer, discount: Discount) { }
// 3 parameters, each represents a concept
```

**Level 4: Red Flag**
```typescript
function complexFunction(a, b, c, d, e, f, g, h) { }
// 8 parameters - too many!
```

---

## 📚 Relationship to Core Principles

- **Single Responsibility** - Many parameters = function does too much
- **Refactoring Techniques** - Introduce Parameter Object solves this
- **ETC Principle** - Long parameter lists make code harder to change
- **Review Dimensions** - Maintainability and Testability suffer
- **SOLID Principles** - Parameter objects reduce coupling

---

## ✅ Checklist: Avoid Long Parameter Lists

When defining functions:

- [ ] Does this function have < 4 parameters?
- [ ] Could related parameters be grouped into an object?
- [ ] Are all parameters actually used by the function?
- [ ] Could I describe parameters in a clear order?
- [ ] Would adding another parameter break many callers?
- [ ] Can a new developer remember the parameter order?
- [ ] Is testing this function straightforward?
- [ ] Are some parameters optional? (Consider object)
- [ ] Could this indicate the function does too much?

---

## ✨ Remember

**DON'T DO**: Create functions with 5+ parameters.

**DO**: Group related parameters into objects.

**Rule of thumb**: If you need more than 3 parameters, introduce a parameter object.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells/smells-like-long-parameter-list.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Reduce parameters. Group into objects.**
