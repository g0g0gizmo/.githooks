# Liskov Substitution Principle

**Core Concept**: Subtypes must be substitutable for base types without breaking behavior. If B extends A, B should work anywhere A works without surprises.

**Test Question**: "Can I use B everywhere A is expected without breaking expectations?"

---

## ❌ Anti-Pattern: Broken Substitution

```typescript
class Bird {
  fly() { /* Birds fly */ }
}

class Dog extends Bird {
  fly() {
    throw new Error('Dogs cannot fly!'); // Breaks Bird contract!
  }
}

function makeBirdFly(bird: Bird) {
  bird.fly(); // Crashes if bird is actually a Dog!
}

makeBirdFly(new Dog()); // Runtime error!
// Problem: Dog claims to be a Bird but violates Bird's behavior
```

---

## ✅ Proper Implementation: Behavioral Compatibility

```typescript
class Animal {
  move() { /* All animals can move */ }
}

class Bird extends Animal {
  fly() { /* Specific to birds */ }
  move() { this.fly(); } // Birds move by flying
}

class Dog extends Animal {
  run() { /* Specific to dogs */ }
  move() { this.run(); } // Dogs move by running
}

function moveAnimal(animal: Animal) {
  animal.move(); // Works safely for both Bird and Dog!
}

moveAnimal(new Bird()); // ✅ Works
moveAnimal(new Dog());  // ✅ Works
// Proper abstraction: each subtype honors Animal.move() contract
```

---

## 🎯 Key Takeaway

**LSP is about behavioral compatibility, not just structural compatibility.** Inheritance should mean "behaves-like", not just "has-same-methods". If clients need type checking, the hierarchy is broken.

---

## 🔗 Related

- [[single-responsibility-principle]] - Clear contracts
- [[open-closed-principle]] - Safe polymorphic extensions
- [[composition-over-inheritance]] - Alternative to fragile hierarchies
- [[design-by-contract]] - Explicit behavioral contracts

---

**Part of**: [[SOLID]]
**Tags**: #solid #liskov-substitution #inheritance #polymorphism
