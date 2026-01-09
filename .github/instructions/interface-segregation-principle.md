# Interface Segregation Principle

**Core Concept**: Clients should not be forced to depend on methods they don't use. Use small, focused interfaces instead of fat ones.

**Test Question**: "Does the implementation need every method in the interface?"

---

## ❌ Anti-Pattern: Fat Interface

```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { console.log('Working'); }
  eat() { throw new Error('Robots do not eat'); } // Forced!
  sleep() { throw new Error('Robots do not sleep'); } // Forced!
}
// Problems: Robot forced to implement irrelevant methods, throws exceptions
```

---

## ✅ Proper Implementation: Segregated Interfaces

```typescript
interface Workable { work(): void; }
interface Eatable { eat(): void; }
interface Sleepable { sleep(): void; }

class Human implements Workable, Eatable, Sleepable {
  work() { console.log('Working'); }
  eat() { console.log('Eating'); }
  sleep() { console.log('Sleeping'); }
}

class Robot implements Workable {
  work() { console.log('Working'); }
  // No forced eat() or sleep() implementation!
}

function makeWork(worker: Workable) {
  worker.work(); // Works for both Human and Robot
}

function feedWorker(eater: Eatable) {
  eater.eat(); // Only Human, Robot cannot be passed (type-safe!)
}
```

---

## 🎯 Key Takeaway

**Design interfaces from the client's perspective, not the implementer's.** If implementations throw "NotImplemented" or leave methods empty, the interface is too fat.

---

## 🔗 Related

- [[single-responsibility-principle]] - Interfaces have one purpose
- [[dependency-inversion-principle]] - Abstractions are focused
- [[composition-over-inheritance]] - Multiple small interfaces compose well

---

**Part of**: [[SOLID]]
**Tags**: #solid #interface-segregation #interfaces #api-design
