# Data Class

**Core Concept**: A class that contains only fields and getter/setter methods with no meaningful behavior, violating object-oriented encapsulation principles.

**Test Question**: "Does this class do anything besides hold data?"

---

## ❌ Anti-Pattern: Anemic Domain Model

```typescript
class User {
  private name: string;
  private email: string;
  private registrationDate: Date;

  getName(): string { return this.name; }
  setName(name: string): void { this.name = name; }

  getEmail(): string { return this.email; }
  setEmail(email: string): void { this.email = email; }

  getRegistrationDate(): Date { return this.registrationDate; }
  setRegistrationDate(date: Date): void { this.registrationDate = date; }
}

// All behavior lives elsewhere
class UserService {
  isActive(user: User): boolean {
    const daysSinceRegistration =
      (Date.now() - user.getRegistrationDate().getTime()) / (1000 * 60 * 60 * 24);
    return daysSinceRegistration <= 365;
  }
}
```

---

## ✅ Proper Implementation: Rich Domain Model

```typescript
class User {
  constructor(
    private name: string,
    private email: string,
    private registrationDate: Date
  ) {}

  isActive(): boolean {
    const daysSinceRegistration =
      (Date.now() - this.registrationDate.getTime()) / (1000 * 60 * 60 * 24);
    return daysSinceRegistration <= 365;
  }

  updateEmail(newEmail: string): void {
    if (!this.isValidEmail(newEmail)) {
      throw new Error('Invalid email format');
    }
    this.email = newEmail;
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // Expose only necessary data
  getContactInfo(): { name: string; email: string } {
    return { name: this.name, email: this.email };
  }
}
```

---

## 🎯 Key Takeaway

**Move behavior to the data.** Objects should contain both data and the operations that work on that data. If behavior lives in separate service classes, consider moving it to the domain objects.

---

## 🔗 Related

- [[single-responsibility-principle]] - Each class has clear purpose
- [[smells-like-feature-envy]] - Methods in wrong class
- [[smells-like-primitive-obsession]] - Value objects vs primitives

**Part of**: [[smells-moc]]
**Tags**: #code-smell #dispensable #encapsulation #domain-model
