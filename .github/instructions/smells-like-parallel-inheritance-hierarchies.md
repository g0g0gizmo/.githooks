# Code Smell: Parallel Inheritance Hierarchies

**Purpose**: Identify when hierarchies mirror each other unnecessarily
**Audience**: You + AI (code review, refactoring)
**Category**: Object-Orientation Abusers (OOP Gone Wrong)
**Severity**: 🟡 MEDIUM
**Principle Type**: DON'T DO (Negative Principle)

---

## 🎯 What Is This Smell?

**Parallel Inheritance Hierarchies** occurs when every time you create a subclass in one hierarchy, you must create a subclass in another.

This indicates the hierarchies are tightly coupled and should be merged or refactored to use composition.

### Why It Matters

Parallel hierarchies cause:
- ❌ Tight coupling between hierarchies
- ❌ Hard to add new types (must add to both)
- ❌ Confusing relationships
- ❌ Easy to miss synchronization
- ❌ Violates DRY principle

---

## 🚩 Detection Signs

```typescript
// ❌ SMELL: Parallel hierarchies
// For every Vehicle type, need corresponding Handler

class Vehicle { }
class Car extends Vehicle { }
class Truck extends Vehicle { }
class Bicycle extends Vehicle { }

class VehicleHandler { }
class CarHandler extends VehicleHandler { }
class TruckHandler extends VehicleHandler { }
class BicycleHandler extends VehicleHandler { }

// New requirement: Add Motorcycle
// Must add to both:
class Motorcycle extends Vehicle { }
class MotorcycleHandler extends VehicleHandler { }

// Parallel hierarchies!
// One for each type of vehicle
// And one handler for each type
// Tightly coupled
```

**Symptoms**:
- [ ] Every subclass in one hierarchy has corresponding subclass in another
- [ ] Class names mirror each other (Vehicle/VehicleHandler, Car/CarHandler)
- [ ] Adding new subclass requires changes in multiple hierarchies
- [ ] Hierarchies are always synchronized
- [ ] Difficult to add new subtypes

---

## 💔 Why It's Bad

### Problem 1: Hard to Add Types

```typescript
// ❌ Adding new type requires changes everywhere
// Vehicle hierarchy:
class Animal { }
class Dog extends Animal { }
class Cat extends Animal { }

// Behavior hierarchy:
class AnimalBehavior { }
class DogBehavior extends AnimalBehavior { }
class CatBehavior extends AnimalBehavior { }

// New requirement: Add Bird
// Must add:
class Bird extends Animal { }
class BirdBehavior extends AnimalBehavior { }

// And update maps/factories:
const behaviorMap = {
  'dog': DogBehavior,
  'cat': CatBehavior,
  'bird': BirdBehavior  // ← Must add
};

// Tight coupling!
```

### Problem 2: Easy to Synchronize Incorrectly

```typescript
// ❌ Hierarchies must stay synchronized
// Someone adds Dog:
class Dog extends Animal { }

// But forgets DogHandler:
class AnimalHandler { }
class CatHandler extends AnimalHandler { }

// Now Dog has no handler
// Runtime error when Dog used
// Silent bug
```

---

## ✅ Refactoring Solutions

### Solution 1: Use Strategy Pattern

```typescript
// ❌ BEFORE: Parallel hierarchies
class Vehicle { }
class Car extends Vehicle { }
class Truck extends Vehicle { }

class VehicleHandler { }
class CarHandler extends VehicleHandler { }
class TruckHandler extends VehicleHandler { }

// ✅ AFTER: Use Strategy pattern
interface VehicleHandler {
  handle(vehicle: Vehicle): void;
}

class Vehicle {
  constructor(private handler: VehicleHandler) {}

  handle(): void {
    this.handler.handle(this);
  }
}

class Car implements Vehicle {
  constructor() {
    super(new CarHandler());
  }
}

class CarHandler implements VehicleHandler {
  handle(vehicle: Vehicle): void {
    // Handle car
  }
}

// No parallel hierarchies
// Handler is part of vehicle
```

### Solution 2: Move Methods to Common Hierarchy

```typescript
// ❌ BEFORE: Parallel hierarchies
class Animal { }
class Dog extends Animal { }
class Cat extends Animal { }

class AnimalBehavior { }
class DogBehavior extends AnimalBehavior { }
class CatBehavior extends AnimalBehavior { }

// ✅ AFTER: Move behavior into animal classes
abstract class Animal {
  abstract performBehavior(): void;
}

class Dog extends Animal {
  performBehavior(): void {
    console.log('Barking...');
  }
}

class Cat extends Animal {
  performBehavior(): void {
    console.log('Meowing...');
  }
}

// Single hierarchy
// Behavior is part of each type
```

### Solution 3: Extract Data into Object

```typescript
// ❌ BEFORE: Parallel hierarchies
class Report { }
class SalesReport extends Report { }
class ErrorReport extends Report { }

class ReportFormatter { }
class SalesReportFormatter extends ReportFormatter { }
class ErrorReportFormatter extends ReportFormatter { }

// ✅ AFTER: Use composition
class Report {
  constructor(
    readonly type: string,
    readonly data: any,
    private formatter: ReportFormatter
  ) {}

  format(): string {
    return this.formatter.format(this);
  }
}

interface ReportFormatter {
  format(report: Report): string;
}

const salesReport = new Report('sales', data, new SalesReportFormatter());
const errorReport = new Report('error', data, new ErrorReportFormatter());

// No parallel hierarchies
// Behavior is injected
```

### Solution 4: Move Responsibility

```typescript
// ❌ BEFORE: Parallel Ship and ShipDriver hierarchies
class Ship { }
class Battleship extends Ship { }
class Freighter extends Ship { }

class ShipDriver { }
class BattleshipDriver extends ShipDriver { }
class FreighterDriver extends ShipDriver { }

// ✅ AFTER: Ship handles its own logic
abstract class Ship {
  abstract navigate(): void;
  abstract fire(): void;  // Not all ships have this
}

class Battleship extends Ship {
  navigate(): void { }
  fire(): void { }  // Has fire
}

class Freighter extends Ship {
  navigate(): void { }
  fire(): void { throw new Error('Cannot fire'); }  // No fire
}

// Or better - use composition:
abstract class Ship {
  abstract navigate(): void;
}

interface Weapon {
  fire(): void;
}

class Battleship extends Ship {
  private weapon: Weapon = new Cannon();

  navigate(): void { }
  getWeapon(): Weapon { return this.weapon; }
}

class Freighter extends Ship {
  navigate(): void { }
  // No weapon - clean!
}

// No parallel hierarchies
```

---

## 📚 Relationship to Core Principles

- **DRY Principle** - Parallel hierarchies duplicate the type structure
- **SOLID-S** - Single responsibility means not duplicating structure
- **Composition** - Better than parallel hierarchies

---

## ✅ Checklist: Avoid Parallel Inheritance

When designing hierarchies:

- [ ] Do I have matching subclasses in different hierarchies?
- [ ] Could I use composition instead?
- [ ] Could I move behavior into one hierarchy?
- [ ] Would strategy pattern work better?

---

## ✨ Remember

**DON'T DO**: Create parallel inheritance hierarchies.

**DO**: Use composition and strategy pattern.

**Rule of thumb**: If hierarchies mirror each other, merge them or use composition.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/smells-like-parallel-inheritance-hierarchies.md`
**Created**: 2025-11-09
**Source**: https://refactoring.guru/refactoring/smells
**Principle Type**: DON'T DO (Negative Principle)

🚀 **Eliminate parallel hierarchies. Use composition.**
