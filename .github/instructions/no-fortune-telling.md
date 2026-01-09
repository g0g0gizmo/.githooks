# Core Principle: No Fortune Telling

**Purpose**: Don't speculate about future requirements; build for what you know
**Audience**: You + AI (design decisions, architecture planning)
**Focus**: Design for replaceability, not for uncertain futures
**Philosophy**: YAGNI - You Aren't Gonna Need It

---

## 🎯 What is No Fortune Telling?

**No Fortune Telling** = Don't design for speculative future needs

> "Don't try to predict uncertain future needs. Design for replaceability instead."

### The Problem

When you try to anticipate future requirements, you:
- ❌ Add complexity you don't need
- ❌ Create code that's hard to understand
- ❌ Spend time on features nobody asked for
- ❌ Make wrong predictions 80% of the time
- ❌ Build for a future that never comes

### The Solution

Instead:
- ✅ Build for what you know (current requirements)
- ✅ Make code easy to change (ETC principle)
- ✅ Design for replaceability (not extensibility)
- ✅ Solve problems when they arrive
- ✅ Keep code simple

---

## 💡 Core Concept

### The Reality of Predictions

```
Prediction: "We'll need multi-currency support eventually"
Reality: ❌ That feature never happened
         ✗ You spent 3 days on speculative code
         ✗ The code you added is now hard to understand
         ✗ Wasted effort

vs.

When actually needed:
✅ "Now we need multi-currency"
✅ Build it (maybe it's easier now anyway)
✅ Takes 2 days, but focused on actual requirement
✅ No wasted effort
```

### Famous Predictions That Failed

```
❌ "We'll need to support 1000 users"
   → Built for thousands, got millions (over-engineered wrong way)

❌ "This will need to run on Windows, Mac, and Linux"
   → Platform needs changed; refactored anyway

❌ "We should support multiple languages upfront"
   → Only used English; added 50% complexity for 0% value

❌ "We might need to cache this"
   → Never cached due to architecture changes
   → Caching layer sat unused

❌ "We should build this plugin architecture"
   → No plugins ever created
   → Architecture complexity hid the real logic
```

---

## 🚩 Red Flags (Fortune Telling)

### Anti-Pattern 1: Speculative Extensibility

```typescript
// ❌ Fortune telling: "What if we need to support multiple types?"
interface PaymentProcessor {
  process(amount: number, method: PaymentMethod): PaymentResult;
  refund(amount: number, method: PaymentMethod): RefundResult;
  verify(method: PaymentMethod): VerificationResult;
  tokenize(method: PaymentMethod): TokenResult;
  webhook(event: WebhookEvent): void;
  reconcile(method: PaymentMethod, period: DateRange): ReconciliationResult;
  // ... 20 more methods for "future flexibility"
}

// Reality: You only need to process credit cards
// All this code is complexity for requirements that don't exist
// Hard to understand
// Hard to test
// Hard to maintain
```

**Cost of speculation**: 500 lines of code. 90% of it unused. 10% actually used.

### Anti-Pattern 2: Premature Optimization

```typescript
// ❌ Fortune telling: "We'll have millions of users, so optimize now"
// Single responsibility: Generate greeting
function getGreeting(userId: number, locale: string, format: string, caching: CacheConfig, mempool: Mempool, ...) {
  // 100 lines of caching logic
  // 50 lines of format logic
  // 50 lines of locale logic
  // 10 lines of actual greeting logic

  const cacheKey = `${userId}-${locale}-${format}`;
  if (mempool.has(cacheKey) && !caching.isStale(cacheKey)) {
    return mempool.get(cacheKey);
  }

  const greeting = `Hello, ${getUser(userId).name}`; // The actual logic!

  if (caching.shouldCache(format, locale)) {
    mempool.set(cacheKey, greeting, caching.ttl);
  }

  return greeting;
}

// Reality: Greeting shows on profile (viewed maybe 10 times)
// All that caching is overkill
// Code is unmaintainable
```

### Anti-Pattern 3: Over-Parameterization

```typescript
// ❌ Fortune telling: "What if we need different behavior in different contexts?"
function calculatePrice(
  product,
  customer,
  promotion,
  location,
  dayOfWeek,
  weather,
  marketConditions,
  competitors,
  seasonalAdjustment,
  customerLoyalty,
  inventoryLevel,
  demandForecasting,
  historicalTrends,
  futureProjections,
  ...
) {
  // 500 lines of conditional logic
  // Most parameters never used
  // Impossible to understand
  // Impossible to test

  return product.price * someComplexCalculation(...params);
}

// Reality: You just need product price * customer discount
// Everything else is speculation
```

### Anti-Pattern 4: Speculative Design Patterns

```typescript
// ❌ Fortune telling: "We might need the Strategy pattern here"
// Implement unused strategy pattern for payment
abstract class PaymentStrategy {
  abstract pay(amount: number): void;
  abstract refund(amount: number): void;
  abstract verify(): boolean;
}

class CreditCardStrategy extends PaymentStrategy {
  pay(amount: number) { /* ... */ }
  refund(amount: number) { /* ... */ }
  verify() { /* ... */ }
}

// Reality: Only credit cards used
// 90% of strategy pattern code is unused
// Simple if statement would suffice
// Added 50% code for 0% value
```

### Anti-Pattern 5: Speculative Configuration

```typescript
// ❌ Fortune telling: "We might need to configure everything"
const config = {
  database: {
    driver: configFile.db.driver,
    host: configFile.db.host,
    port: configFile.db.port,
    pool: {
      min: configFile.db.pool.min,
      max: configFile.db.pool.max,
      timeout: configFile.db.pool.timeout,
      // ... 20 more pool settings
    },
    ssl: {
      enabled: configFile.db.ssl.enabled,
      cert: configFile.db.ssl.cert,
      key: configFile.db.ssl.key,
      ca: configFile.db.ssl.ca,
      // ... 10 more ssl settings
    },
    // ... 100 more settings
  },
  // ... 1000 more settings
};

// Reality: You only need host and port
// All that configuration is unused
// Hard to understand what matters
```

---

## ✅ Good Signs (Building for Reality)

### Pattern 1: Minimal, Focused Implementation

```typescript
// ✅ Build for what you know
function calculatePrice(product, customer) {
  const basePrice = product.price * customer.quantity;
  const discount = customer.isPremium ? 0.2 : 0;
  return basePrice * (1 - discount);
}

// Simple
// Clear
// Easy to test
// Easy to understand
// When you need taxes: add it
// When you need promos: add it
// When you need bundles: add it
// One thing at a time
```

### Pattern 2: Design for Replaceability

```typescript
// ✅ Don't design for uncertain extension, design for easy replacement
interface PaymentProcessor {
  process(amount: number, token: string): Promise<PaymentResult>;
}

class CreditCardProcessor implements PaymentProcessor {
  async process(amount: number, token: string): Promise<PaymentResult> {
    // Process credit card
    return result;
  }
}

// If you need PayPal:
class PayPalProcessor implements PaymentProcessor {
  async process(amount: number, token: string): Promise<PaymentResult> {
    // Process PayPal
    return result;
  }
}

// Current: Credit card works
// Future: Easy to add PayPal (just implement interface)
// No speculative design
// No unused code
// Interface only grows when needed
```

### Pattern 3: Solve Problems When They Arrive

```typescript
// ✅ Wait for actual problem, then solve
// Stage 1: Single database query works
function getUsers() {
  return db.query("SELECT * FROM users");
}

// Stage 2 (months later): "This query is slow"
// Now add caching
function getUsers() {
  const cacheKey = 'all-users';
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  const users = db.query("SELECT * FROM users");
  cache.set(cacheKey, users, 300);
  return users;
}

// Stage 3 (months later): "Cache invalidation is wrong"
// Now solve that problem
function invalidateUsersCache() {
  cache.delete('all-users');
}

// Better than:
// Stage 1: Build entire caching framework "for future use"
//         Complexity for 0 value
```

### Pattern 4: YAGNI (You Aren't Gonna Need It)

```typescript
// ✅ Don't build features nobody asked for
// Current requirement: "Users need to upload profile picture"

// ❌ Speculative implementation:
class MediaUploadService {
  async upload(file: File, options: UploadOptions) {
    // Validate file type (8 types supported for "future")
    // Check size limits (20 different size rules)
    // Generate thumbnails (3 sizes: small, medium, large)
    // Create watermarks (5 watermark styles)
    // Extract metadata (20 metadata fields)
    // Organize in folders (complex folder hierarchy)
    // Support cloud storage (AWS, Azure, GCS integration)
    // Generate variants (10 variants)
    // ... 500 lines
  }
}

// ✅ Actual implementation:
class MediaUploadService {
  async upload(file: File) {
    // Check: is it an image?
    if (!file.type.startsWith('image/')) {
      throw new Error('Must be image');
    }

    // Check: under 5MB?
    if (file.size > 5_000_000) {
      throw new Error('Too large');
    }

    // Save to disk
    return saveFile(file);
  }
}

// 20 lines, not 500
// When you need thumbnails: add it
// When you need cloud storage: add it
// When you need watermarks: add it
```

### Pattern 5: Keep It Simple

```typescript
// ✅ Simplest solution first
// Need to manage feature flags?

// ❌ Speculative: Build full feature flag framework
class FeatureFlagManager {
  async evaluate(flagName: string, context: EvaluationContext) {
    // Load flags from database
    // Evaluate with complex rules
    // Track analytics
    // A/B test variants
    // Integrate with third-party services
    // ... 200 lines
  }
}

// ✅ Simple: Just check an object
const flags = {
  newDashboard: true,
  betaFeatures: false,
  darkMode: true,
};

if (flags.newDashboard) {
  // Show new dashboard
}

// When you need database-backed flags: refactor
// When you need analytics: add it
// Start simple, add complexity only when needed
```

---

## 🎯 How to Avoid Fortune Telling

### Heuristic 1: The "But We Might" Test

```
Question: "Should I implement this feature?"

❌ "But we might need it later"
❌ "But it's good design for the future"
❌ "But someone might want this"
❌ "But it only adds a little complexity"

✅ "Because the current requirements ask for it"
✅ "Because someone specifically asked for it"
✅ "Because I have a use case I'm implementing now"
✅ "Because it's simpler than the alternative"
```

**If you use "might," "could," "probably," "eventually" → fortune telling**

### Heuristic 2: The "Can I Replace It" Test

```
Question: "Is this speculative?"

If yes to: "Can I easily replace this if I'm wrong?"
  → OK, build it simple

If no to: "Can I easily replace this if I'm wrong?"
  → Don't build it, it's speculative
```

### Heuristic 3: The "YAGNI" Question

```
For every feature you want to add:
"Are we actually gonna need it?"

Only YES answers get implemented.
Maybe, probably, might, could → NO
```

---

## 🔄 No Fortune Telling Workflow

### When Tempted to Over-Design

```
1. Notice temptation
   "Maybe we should add support for X"

2. Ask: Is X in current requirements?
   - Yes? Build it
   - No? Stop

3. Ask: Has someone specifically asked for X?
   - Yes? Build it
   - No? Stop

4. Ask: Can I add X later easily?
   - Yes? Wait; add when needed
   - No? Maybe build it now (reconsider)

5. Ask: Will X simplify current code?
   - Yes? Add it
   - No? Don't add it

6. Ask: Will X make current code harder to understand?
   - Yes? Don't add it
   - No? Maybe add it (reconsider)
```

---

## 💡 Examples: No Fortune Telling in Action

### Example 1: Feature Request

**Bad Approach** (Fortune telling):
```typescript
Requirement: "Users need to login"

Speculation: "What if users want single sign-on?"
            "What if we need OAuth?"
            "What if we need SAML?"
            "What if we need 2FA?"
            "What if we need biometric login?"

Implementation: 500 lines of speculative code
               10 login methods
               Complex configuration
               Hard to understand

Result: Over-engineered for current requirement
        90% of code unused
        Hard to maintain
        Hard to debug
```

**Good Approach** (Build for requirements):
```typescript
Requirement: "Users need to login"

Implementation:
1. Simple email/password login (50 lines)
2. Test login works ✓
3. Deploy ✓

Future: "Add single sign-on"
  → Add SSO (50 lines)

Future: "Add 2FA"
  → Add 2FA (50 lines)

Total: Same features eventually, but built when needed
       Code is simple and focused
       Easy to understand and maintain
```

### Example 2: Database Design

**Bad Approach** (Fortune telling):
```sql
-- Speculation: "What if users have multiple emails?"
-- "What if we need email history?"
-- "What if we need email verification status?"

CREATE TABLE user_emails (
  id INT PRIMARY KEY,
  user_id INT,
  email VARCHAR(255),
  verified BOOLEAN,
  verified_at TIMESTAMP,
  verification_token VARCHAR(500),
  verification_token_created_at TIMESTAMP,
  verification_token_expires_at TIMESTAMP,
  verification_attempts INT,
  last_verification_attempt TIMESTAMP,
  primary_email BOOLEAN,
  marked_as_spam BOOLEAN,
  spam_report_date TIMESTAMP,
  email_bounced BOOLEAN,
  bounce_date TIMESTAMP,
  bounce_reason VARCHAR(500),
  ...
);

-- 30 columns for speculative features
-- Most unused
-- Hard to understand
```

**Good Approach** (Build for requirements):
```sql
-- Requirement: "Users have one email, need to verify it"

CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  verified BOOLEAN,
  verified_at TIMESTAMP
);

-- Simple, clear
-- When multiple emails needed: add table
-- When history needed: add audit table
-- One thing at a time
```

### Example 3: API Versioning

**Bad Approach** (Fortune telling):
```typescript
// Speculation: "We'll need API versioning"

GET /api/v1/users
GET /api/v2/users
GET /api/v3/users
// ... v1, v2, v3 code all running
// ... support multiple versions "for backward compatibility"
// Complex routing
// Hard to maintain
// Most versions unused
```

**Good Approach** (Build for now):
```typescript
GET /api/users  // Version 1

// When requirement arises: "Need new API format"
GET /api/users       // Version 1 (old)
GET /api/v2/users    // Version 2 (new)

// Then deprecate v1 when ready
// One version at a time
// Simple routing
```

---

## 🎓 Philosophy

**Don't try to predict the future. Build for the present.**

You can't know:
- ❌ What features will actually be used
- ❌ What scale you'll reach
- ❌ What changes will come
- ❌ What the user's needs will evolve into

You should:
- ✅ Build what was asked
- ✅ Build it simply
- ✅ Make it easy to change
- ✅ Add features when requested
- ✅ Refactor when needed

**The best prediction: reality will surprise you.**

So build for reality, not your predictions.

---

## 📚 Relationship to Core Principles

- **ETC Principle**: Simple code (no speculation) is easier to change
- **YAGNI**: Don't over-engineer for might-happens
- **Small Steps**: Build what's needed, one step at a time
- **DRY**: Speculative code often violates DRY
- **Atomic Notes**: Focus on one thing, not many possibilities
- **Evergreen Principles**: Timeless patterns, not speculative features

---

## ✅ No Fortune Telling Checklist

When adding a feature:

- [ ] Is this in the current requirements?
- [ ] Did someone specifically ask for this?
- [ ] Am I solving a problem that actually exists?
- [ ] Would the code be simpler without this?
- [ ] Could I add this later if needed?
- [ ] Is this essential for today's functionality?
- [ ] Am I building for "might" or for "is"?
- [ ] Would I rate this a 9/10 necessity if it were the only thing to do?
- [ ] Is this speculative?
- [ ] Is this YAGNI?

If mostly YES to the first group and NO to the last group: Build it.
Otherwise: Wait.

---

## 🔄 Reality vs Speculation

| Aspect | Speculative ("Might") | Reality ("Is") |
|--------|----------------------|----------------|
| **Time** | Days spent on unused code | Days spent on what's needed |
| **Complexity** | High (handles many cases) | Low (handles current case) |
| **Testing** | Hard (many code paths) | Easy (few code paths) |
| **Understanding** | Hard (lots of options) | Easy (clear intent) |
| **Refactoring** | Hard (breaks speculation) | Easy (changing actual code) |
| **User Value** | Low (no one asked) | High (requested feature) |
| **Accuracy** | ~20% (mostly wrong) | ~100% (you know what's needed) |

**Build for reality. Refactor when needed.**

---

## ✨ Remember

**Don't fortune tell. Build for what you know.**

- 🎯 Implement current requirements
- 📝 Add features when asked
- 🔄 Refactor when needed
- 🧠 Keep it simple
- 📦 Design for replaceability (not extensibility)
- ⏰ Solve problems when they arrive

**When in doubt: YAGNI (You Aren't Gonna Need It)**

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/no-fortune-telling-principle.md`
**Created**: 2025-11-09
**Source**: The Pragmatic Programmer, 20th Anniversary Edition
**Alias**: YAGNI - You Aren't Gonna Need It
**Philosophy**: Build for reality, not predictions

🚀 **Stop fortune telling. Start building what's needed.**
