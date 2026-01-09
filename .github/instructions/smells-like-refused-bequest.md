# Code Smell: Refused Bequest

**Purpose**: Identify when subclasses don't use inherited methods
**Audience**: You + AI (code review, refactoring)
**Category**: Object-Orientation Abusers (OOP Gone Wrong)
**Severity**: 🟡 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Refused Bequest** occurs when a subclass inherits methods it doesn't use or overrides with "not implemented" errors.

Subclasses should be specializations of their parent, not just "kind of like" the parent. If a subclass refuses parts of its inheritance, the hierarchy is wrong.

### Why It Matters

Refused bequest causes:
- ❌ Wrong inheritance hierarchy
- ❌ Violates Liskov Substitution Principle
- ❌ Confusing code contracts
- ❌ Runtime errors ("not implemented")
- ❌ Indicates poor design

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Subclass refusing inherited methods
class Bird {
  fly(): string {
    return 'Flying...';
  }

  walk(): string {
    return 'Walking...';
  }

  eat(): string {
    return 'Eating...';
  }
}

class Penguin extends Bird {
  // Penguin can walk and eat, but not fly!
  fly(): string {
    throw new Error('Penguins cannot fly!');  // ← Refusing bequest
  }

  walk(): string {
    return 'Waddling...';
  }

  eat(): string {
    return 'Eating fish...';
  }
}

class Ostrich extends Bird {
  fly(): string {
    throw new Error('Ostriches cannot fly!');  // ← Refusing bequest
  }
}

// Problems:
// - Bird contract says "can fly"
// - Penguin breaks that contract
// - Can't use Penguin where Bird is expected
// - Violates Liskov Substitution Principle
```

**Symptoms**:
- [ ] Subclass throws "not implemented" error
- [ ] Subclass overrides method to do nothing
- [ ] Subclass has comment "don't use this method"
- [ ] Subclass casts parent methods to specific child type
- [ ] Not all inherited methods are used

---

## 💔 Why It's Bad

### Problem 1: Violates Substitutability

```typescript
// ❌ Can't substitute Penguin for Bird
function birdRoutine(bird: Bird) {
  console.log(bird.fly());   // Works for Bird, Sparrow
                             // Crashes for Penguin!
}

const sparrow = new Sparrow();
birdRoutine(sparrow);  // OK

const penguin = new Penguin();
birdRoutine(penguin);  // ❌ ERROR: Penguins cannot fly!

// Breaks Liskov Substitution Principle
// Can't safely use subclass where parent expected
```

### Problem 2: Confusing Contracts

```typescript
// ❌ Unclear which methods work for which birds
class Bird {
  fly(): string { }
  walk(): string { }
  swim(): string { }
}

class Sparrow extends Bird {
  fly(): string { return 'Flying...'; }
  walk(): string { return 'Walking...'; }
  swim(): string { throw new Error('Cannot swim'); }
}

class Duck extends Bird {
  fly(): string { return 'Flying...'; }
  walk(): string { return 'Walking...'; }
  swim(): string { return 'Swimming...'; }
}

class Penguin extends Bird {
  fly(): string { throw new Error('Cannot fly'); }
  walk(): string { return 'Waddling...'; }
  swim(): string { return 'Swimming...'; }
}

// Which methods work for which bird?
// Must know each bird's specifics
// No clear contract
```

### Problem 3: Runtime Errors

```typescript
// ❌ Silent runtime errors
function createDefaultBird(): Bird {
  return new Penguin();  // Programmer's mistake
}

// Later:
const bird = createDefaultBird();
bird.fly();  // ❌ Runtime error: "Cannot fly"

// If Penguin wasn't a Bird, error would be caught at compile time
```

---

## ✅ Refactoring Solutions

### Solution 1: Replace Inheritance with Delegation

```typescript
// ❌ BEFORE: Wrong hierarchy
class Bird {
  fly(): string { return 'Flying...'; }
  walk(): string { return 'Walking...'; }
}

class Penguin extends Bird {
  fly(): string {
    throw new Error('Penguins cannot fly!');
  }
}

// ✅ AFTER: Use delegation
class Bird {
  fly(): string { return 'Flying...'; }
  walk(): string { return 'Walking...'; }
}

class Penguin {
  private bird: Bird;

  walk(): string {
    return this.bird.walk();  // Delegate what applies
  }

  // fly() is not available - correct!
  // Penguin is not a Bird
}

// Now clear: Penguin doesn't have fly()
// No false contracts
```

### Solution 2: Create Correct Hierarchy

```typescript
// ❌ BEFORE: Forcing hierarchy
class Animal {
  move(): string { }
  eat(): string { }
}

class Insect extends Animal {
  // Insect can move and eat
  // But doesn't fly or swim
}

// ✅ AFTER: Correct hierarchy
abstract class Animal {
  eat(): string { return 'Eating...'; }
}

abstract class FlyingAnimal extends Animal {
  fly(): string { return 'Flying...'; }
}

abstract class SwimmingAnimal extends Animal {
  swim(): string { return 'Swimming...'; }
}

class Sparrow extends FlyingAnimal { }

class Penguin extends SwimmingAnimal { }  // No fly() in hierarchy

class Duck extends FlyingAnimal, SwimmingAnimal { }  // Both if language supports

// Now hierarchy matches reality
// No refused methods
```

### Solution 3: Extract Superclass

```typescript
// ❌ BEFORE: Shared interface despite refusal
class Animal {
  walk(): string { }
  eat(): string { }
  sleep(): string { }
}

class Tiger extends Animal {
  // Uses all methods
}

class Snake extends Animal {
  walk(): string {
    throw new Error('Snakes slither, not walk!');
  }
  // Refuses walk()
}

// ✅ AFTER: Extract common behavior
abstract class Animal {
  eat(): string { return 'Eating...'; }
  sleep(): string { return 'Sleeping...'; }
}

class WalkingAnimal extends Animal {
  walk(): string { return 'Walking...'; }
}

class SlidingAnimal extends Animal {
  slide(): string { return 'Sliding...'; }
}

class Tiger extends WalkingAnimal { }
class Snake extends SlidingAnimal { }

// Now no refused methods
// Correct inheritance
```

### Solution 4: Use Composition

```typescript
// ❌ BEFORE: Forcing inheritance
class Vehicle {
  start(): void { }
  stop(): void { }
  fly(): void { }  // Not all vehicles fly!
}

class Car extends Vehicle {
  fly(): void {
    throw new Error('Cars cannot fly!');
  }
}

class Airplane extends Vehicle {
  // Uses all methods
}

// ✅ AFTER: Compose behaviors
class Vehicle {
  start(): void { }
  stop(): void { }
}

interface Flyable {
  fly(): void;
}

class Car implements Vehicle {
  start(): void { }
  stop(): void { }
  // No fly() - correct
}

class Airplane implements Vehicle, Flyable {
  start(): void { }
  stop(): void { }
  fly(): void { return 'Flying...'; }
}

// Clear what each can do
// No false contracts
```

---

## 📚 Relationship to Core Principles

- **SOLID-L** - Liskov Substitution Principle (core)
- **SOLID-O** - Open/Closed: Don't force subclasses to do unwanted things
- **Inheritance** - Use composition when hierarchy doesn't fit

---

## ✅ Checklist: Avoid Refused Bequest

When creating subclasses:

- [ ] Does this subclass use all inherited methods?
- [ ] Can I substitute this subclass for the parent?
- [ ] Or should it be separate?
- [ ] Should I use delegation instead?
- [ ] Is the inheritance hierarchy correct?

---

## ✨ Remember

**DON'T DO**: Create subclasses that refuse inherited methods.

**DO**: Use correct inheritance hierarchy where all methods make sense.

**Rule of thumb**: If subclass refuses a method, it shouldn't inherit from that parent.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-refused-bequest.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Use correct hierarchy. Don't refuse inheritance.**
