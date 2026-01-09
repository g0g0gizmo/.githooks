# Dependency Inversion Principle

**Core Concept**: High-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).

**Test Question**: "Can I swap implementations without changing dependent code?"

---

## ❌ Anti-Pattern: Concrete Dependencies

```typescript
class UserService {
  constructor() {
    this.db = new PostgresDatabase(); // Hardcoded!
  }

  createUser(email: string) {
    this.db.insert({ email });
  }
}
// Problems: Cannot switch databases, impossible to test, tight coupling
```

---

## ✅ Proper Implementation: Depend on Abstraction

```typescript
// Abstraction defined by high-level module
interface Database {
  insert(data: any): void;
  query(sql: string): any[];
}

// High-level depends on abstraction
class UserService {
  constructor(private database: Database) {} // Injected!

  createUser(email: string) {
    this.database.insert({ email });
  }
}

// Low-level implements abstraction
class PostgresDatabase implements Database {
  insert(data: any) { /* Postgres-specific */ }
  query(sql: string) { return []; }
}

class MockDatabase implements Database {
  insert(data: any) { /* Test stub */ }
  query(sql: string) { return []; }
}

// Easy testing!
const service = new UserService(new MockDatabase());
```

---

## 🎯 Key Takeaway

**Depend on abstractions, not concretions.** If you can't test it easily or swap implementations, you're violating DIP.

---

## 🔗 Related

- [[open-closed-principle]] - Extensions via implementations
- [[interface-segregation-principle]] - Focused abstractions
- [[dependency-injection]] - Technique for DIP

---

**Part of**: [[SOLID]]
**Tags**: #solid #dependency-inversion #abstraction #decoupling
