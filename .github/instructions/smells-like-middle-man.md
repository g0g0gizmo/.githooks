# Middle Man

**Core Concept**: A class exists only to delegate calls to another class, adding no value while increasing complexity and indirection.

**Test Question**: "Does this class do anything besides forward calls to another class?"

---

## ❌ Anti-Pattern: Unnecessary Wrapper

```typescript
class Person {
  constructor(private department: Department) {}

  getManager(): Manager {
    return this.department.getManager();
  }

  getDepartmentName(): string {
    return this.department.getName();
  }

  getDepartmentBudget(): number {
    return this.department.getBudget();
  }

  getDepartmentHeadcount(): number {
    return this.department.getHeadcount();
  }
}

class Department {
  constructor(
    private name: string,
    private manager: Manager,
    private budget: number,
    private headcount: number
  ) {}

  getManager(): Manager { return this.manager; }
  getName(): string { return this.name; }
  getBudget(): number { return this.budget; }
  getHeadcount(): number { return this.headcount; }
}

// Usage: Person adds no value
const person = new Person(dept);
const manager = person.getManager(); // Just forwarding
```

---

## ✅ Proper Implementation: Remove Middle Man

```typescript
class Person {
  constructor(
    private name: string,
    private department: Department
  ) {}

  // Keep Person-specific behavior
  getName(): string {
    return this.name;
  }

  // Expose department directly when it's just delegation
  getDepartment(): Department {
    return this.department;
  }
}

class Department {
  constructor(
    private name: string,
    private manager: Manager,
    private budget: number,
    private headcount: number
  ) {}

  getManager(): Manager { return this.manager; }
  getName(): string { return this.name; }
  getBudget(): number { return this.budget; }
  getHeadcount(): number { return this.headcount; }
}

// Usage: Direct access to what you need
const person = new Person("John", dept);
const manager = person.getDepartment().getManager();
const budget = person.getDepartment().getBudget();
```

---

## 🎯 Key Takeaway

**Remove layers that add no value.** If a class just delegates to another, expose the delegate directly or remove the middle man entirely. Only keep wrappers that add meaningful functionality.

---

## 🔗 Related

- [[smells-like-lazy-class]] - Classes doing too little
- [[smells-like-speculative-generality]] - Unnecessary abstraction
- [[KISS]] - Keep it simple

**Part of**: [[smells-moc]]
**Tags**: #code-smell #coupler #delegation #simplicity
