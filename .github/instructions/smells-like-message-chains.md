# Message Chains

**Core Concept**: Long chains of method calls (train wrecks) that navigate through multiple objects, creating tight coupling and fragile code.

**Test Question**: "Does this code chain through multiple objects to get what it needs?"

---

## ❌ Anti-Pattern: Train Wreck

```typescript
class OrderProcessor {
  processOrder(order: Order) {
    // Train wreck: drilling through multiple objects
    const street = order.getCustomer().getAddress().getStreet();
    const city = order.getCustomer().getAddress().getCity();
    const zip = order.getCustomer().getAddress().getZipCode();

    // More chaining
    const discount = order.getCustomer().getMembershipLevel().getDiscountRate();
    const finalPrice = order.getTotal() * (1 - discount);

    console.log(`Shipping to: ${street}, ${city}, ${zip}`);
    console.log(`Final price: $${finalPrice}`);
  }
}

// Problem: Tightly coupled to object structure
// If Address moves from Customer to Order, this breaks
// Violates Law of Demeter (don't talk to strangers)
```

---

## ✅ Proper Implementation: Hide Delegate

```typescript
class Order {
  constructor(
    private customer: Customer,
    private total: number
  ) {}

  // Hide the navigation chain
  getShippingAddress(): string {
    return this.customer.getShippingAddress();
  }

  getDiscountedTotal(): number {
    return this.total * (1 - this.customer.getDiscount());
  }
}

class Customer {
  constructor(
    private address: Address,
    private membership: MembershipLevel
  ) {}

  getShippingAddress(): string {
    return this.address.getFormattedAddress();
  }

  getDiscount(): number {
    return this.membership.getDiscountRate();
  }
}

// Now: Simple, decoupled usage
class OrderProcessor {
  processOrder(order: Order) {
    console.log(`Shipping to: ${order.getShippingAddress()}`);
    console.log(`Final price: $${order.getDiscountedTotal()}`);
  }
}
```

---

## 🎯 Key Takeaway

**Each object should only talk to its immediate friends.** Hide navigation chains behind meaningful methods. Follow the Law of Demeter: use one dot, not many.

---

## 🔗 Related

- [[smells-like-feature-envy]] - Reaching into other objects
- [[smells-like-inappropriate-intimacy]] - Too much internal knowledge
- [[encapsulation]] - Hide internal structure

**Part of**: [[smells-moc]]
**Tags**: #code-smell #coupler #law-of-demeter #coupling
