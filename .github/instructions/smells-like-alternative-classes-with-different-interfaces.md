# Alternative Classes with Different Interfaces

**Core Concept**: Two classes perform similar operations but have different method signatures, making them harder to use interchangeably and creating unnecessary duplication.

**Test Question**: "Do these classes do the same thing but with different method names?"

---

## ❌ Anti-Pattern: Incompatible Interfaces

```typescript
class StripePaymentProcessor {
  processPayment(amount: number, cardToken: string): boolean {
    // Process payment via Stripe
    return true;
  }
}

class PayPalProcessor {
  executeTransaction(dollars: number, accountId: string): boolean {
    // Process payment via PayPal
    return true;
  }
}

// Problem: Can't use them interchangeably
function checkout(processor: any, amount: number, token: string) {
  // Need to know which processor type to call correct method
  if (processor instanceof StripePaymentProcessor) {
    return processor.processPayment(amount, token);
  } else {
    return processor.executeTransaction(amount, token);
  }
}
```

---

## ✅ Proper Implementation: Unified Interface

```typescript
interface PaymentProcessor {
  process(amount: number, token: string): boolean;
}

class StripePaymentProcessor implements PaymentProcessor {
  process(amount: number, token: string): boolean {
    // Process payment via Stripe
    return true;
  }
}

class PayPalProcessor implements PaymentProcessor {
  process(amount: number, token: string): boolean {
    // Process payment via PayPal
    return true;
  }
}

// Now: Type-safe polymorphism
function checkout(processor: PaymentProcessor, amount: number, token: string) {
  return processor.process(amount, token);
}
```

---

## 🎯 Key Takeaway

**Standardize interfaces for similar functionality.** When classes serve the same purpose, they should share a common interface to enable polymorphism and reduce client complexity.

---

## 🔗 Related

- [[interface-segregation-principle]] - Client-focused interfaces
- [[dependency-inversion-principle]] - Depend on abstractions
- [[smells-like-duplicate-code]] - Similar logic, different names

**Part of**: [[smells-moc]]
**Tags**: #code-smell #object-orientation #interfaces #polymorphism
