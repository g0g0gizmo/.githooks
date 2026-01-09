# Code Smell: Speculative Generality

**Purpose**: Identify and remove over-engineered "just in case" code
**Audience**: You + AI (code review, refactoring)
**Category**: Dispensables (Unnecessary Code)
**Severity**: 🟢 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Speculative Generality** occurs when you write generic code for features that may never exist.

Code should be written for current needs, not hypothetical future needs. YAGNI: You Aren't Gonna Need It.

### Why It Matters

Speculative generality causes:
- ❌ Unnecessary complexity
- ❌ Code that's never used
- ❌ Hard to understand (supports features that don't exist)
- ❌ Hard to test (generic code is harder to test)
- ❌ Maintenance burden (code for features that won't happen)

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Generic code for imagined features
class DataTransformer<T, U> {
  // Overly generic for uncertain needs
  // Takes unused type parameters
  // Has confusing abstract methods

  transform(input: T[], options?: any): U[] {
    // What type is U?
    // When would you use this?
    // It's too abstract
  }

  filterBy(predicate?: (item: T) => boolean): T[] {
    // Optional parameter suggests uncertainty
    // Maybe it's not needed?
  }

  mapTo<V>(mapper?: (item: T) => V): V[] {
    // Another optional generic parameter
    // For a hypothetical future use case?
  }
}

// Similar: Lazy abstract classes
abstract class ConfigurationManager {
  // Abstract for "future extensibility"
  // But we only need JSON configuration
  // Why is it abstract?

  abstract parse(input: string): Config;
  abstract validate(config: Config): boolean;
  abstract serialize(config: Config): string;
}

class JSONConfigurationManager extends ConfigurationManager {
  // Only implementation
  // Ever will be only implementation
}
```

**Symptoms**:
- [ ] Unused parameters
- [ ] Generic/abstract code with only one implementation
- [ ] Abstract classes never subclassed
- [ ] Parameters with default values that are rarely used
- [ ] Code with "future-proofing" comments
- [ ] Over-parameterized functions/classes
- [ ] Hard to understand actual purpose

---

## 💔 Why It's Bad

### Problem 1: Unnecessary Complexity

```typescript
// ❌ Over-engineered for imagined needs
function processData(
  data: any[],
  parser?: (d: any) => any,  // Optional, rarely used
  validator?: (d: any) => boolean,  // Optional, rarely used
  transformer?: (d: any) => any,  // Optional, rarely used
  formatter?: (d: any) => string  // Optional, rarely used
): string {
  // Code is complex and hard to understand
  // 4 optional parameters "just in case"
}

// ✅ Simple for current needs
function processData(data: any[]): string {
  return data
    .map(d => JSON.parse(d))
    .filter(d => d.isValid)
    .map(d => d.toString())
    .join(', ');
}

// Much clearer!
// When you actually need customization, refactor then
```

### Problem 2: Hard to Understand

```typescript
// ❌ Confusing generic code
class Container<T, U, V extends Record<string, any>> {
  // What are these types?
  // Why is V constrained to Record?
  // When would this be used?

  process(
    input: T,
    converter: (t: T) => U,
    validator: (u: U) => V
  ): V {
    // Complex for uncertain use case
  }
}

// Usage:
const container = new Container<string, JSON, {valid: boolean}>();
// Why is this so complicated?

// ✅ Simple specific code
function parseJSON(input: string): JSON {
  return JSON.parse(input);
}

// Clear, simple, fits current need
```

### Problem 3: Never Used

```typescript
// ❌ Infrastructure for features that don't exist
class PluginSystem {
  // Imagined future: "We'll have plugins"
  // Reality: We never created any

  private plugins: Map<string, Plugin> = new Map();
  private hooks: Map<string, Hook[]> = new Map();

  registerPlugin(name: string, plugin: Plugin): void { }
  executeHook(hookName: string): void { }
  loadPluginFromFile(path: string): Promise<Plugin> { }
}

// 100 lines of plugin infrastructure
// Zero plugins ever created
// Maintenance burden for no benefit
```

---

## ✅ Refactoring Solutions

### Solution 1: Remove Unused Parameters

```typescript
// ❌ BEFORE: Optional parameters never used
function calculatePrice(
  basePrice: number,
  quantity: number,
  discount?: number,      // Never used in practice
  taxRate?: number,       // Never used in practice
  shippingCost?: number   // Never used in practice
): number {
  return basePrice * quantity;
}

// ✅ AFTER: Remove unused parameters
function calculatePrice(basePrice: number, quantity: number): number {
  return basePrice * quantity;
}

// When discount needed, extend then
```

### Solution 2: Simplify Generic Code

```typescript
// ❌ BEFORE: Over-generic
class Cache<K, V> {
  private data: Map<K, V> = new Map();

  get(key: K): V | undefined {
    return this.data.get(key);
  }

  set(key: K, value: V): void {
    this.data.set(key, value);
  }

  // 10 more methods for theoretical use cases
}

// ✅ AFTER: Specific to actual need
class UserCache {
  private data: Map<string, User> = new Map();

  getUser(id: string): User | undefined {
    return this.data.get(id);
  }

  setUser(id: string, user: User): void {
    this.data.set(id, user);
  }
}

// Clear and simple for actual need
```

### Solution 3: Inline Abstract Classes

```typescript
// ❌ BEFORE: Abstract for theoretical extensibility
abstract class Logger {
  abstract log(message: string): void;
  abstract error(message: string): void;
  abstract warn(message: string): void;
}

class ConsoleLogger extends Logger {
  log(message: string): void {
    console.log(message);
  }
  error(message: string): void {
    console.error(message);
  }
  warn(message: string): void {
    console.warn(message);
  }
}

// No other logger implementations exist or are planned

// ✅ AFTER: Remove abstract, use concrete
class Logger {
  log(message: string): void {
    console.log(message);
  }
  error(message: string): void {
    console.error(message);
  }
  warn(message: string): void {
    console.warn(message);
  }
}

// If different logger needed later, abstract then
```

### Solution 4: Collapse Unnecessary Hierarchy

```typescript
// ❌ BEFORE: Deep hierarchy for theoretical use
class Vehicle { }
class LandVehicle extends Vehicle { }
class MotorizedLandVehicle extends LandVehicle { }
class Car extends MotorizedLandVehicle { }

// But only Car is ever instantiated!
// Why the intermediate classes?

// ✅ AFTER: Direct to what's needed
class Car {
  // All properties and methods directly
}

// If you need hierarchy, create when you have multiple implementations
```

---

## 📚 Relationship to Core Principles

- **YAGNI** - You Aren't Gonna Need It
- **Simplicity** - Simple code for current needs
- **ETC** - Generic code is harder to change

---

## ✅ Checklist: Avoid Speculative Generality

When writing code:

- [ ] Am I writing this for an actual requirement?
- [ ] Is this feature used anywhere?
- [ ] Am I over-parameterizing?
- [ ] Could I write simpler code for the current need?
- [ ] When should I actually add generality? When needed, not before.

---

## ✨ Remember

**DON'T DO**: Write generic code for features you might not need.

**DO**: Write simple code for current needs. Refactor when requirements change.

**Rule of thumb**: YAGNI - You Aren't Gonna Need It. Build what you need now.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-speculative-generality.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Build for now. Refactor when requirements change.**
