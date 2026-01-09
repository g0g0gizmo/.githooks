# Incomplete Library Class

**Core Concept**: A third-party library lacks methods you need, forcing workarounds throughout the codebase instead of extending the library properly.

**Test Question**: "Am I repeatedly working around missing library functionality?"

---

## ❌ Anti-Pattern: Scattered Workarounds

```typescript
// Third-party Date library lacks "addBusinessDays" method
import { DateUtils } from 'third-party-lib';

class OrderProcessor {
  calculateDeliveryDate(orderDate: Date): Date {
    let date = orderDate;
    let daysAdded = 0;
    while (daysAdded < 5) {
      date = DateUtils.addDays(date, 1);
      if (date.getDay() !== 0 && date.getDay() !== 6) {
        daysAdded++;
      }
    }
    return date;
  }
}

class InvoiceService {
  getDueDate(invoiceDate: Date): Date {
    let date = invoiceDate;
    let daysAdded = 0;
    while (daysAdded < 30) {
      date = DateUtils.addDays(date, 1);
      if (date.getDay() !== 0 && date.getDay() !== 6) {
        daysAdded++;
      }
    }
    return date;
  }
}
// Problem: Same workaround duplicated everywhere
```

---

## ✅ Proper Implementation: Extend Library

```typescript
import { DateUtils } from 'third-party-lib';

// Extension class with needed functionality
class ExtendedDateUtils extends DateUtils {
  static addBusinessDays(date: Date, days: number): Date {
    let result = new Date(date);
    let daysAdded = 0;

    while (daysAdded < days) {
      result = this.addDays(result, 1);
      if (result.getDay() !== 0 && result.getDay() !== 6) {
        daysAdded++;
      }
    }
    return result;
  }
}

// Now use extended version everywhere
class OrderProcessor {
  calculateDeliveryDate(orderDate: Date): Date {
    return ExtendedDateUtils.addBusinessDays(orderDate, 5);
  }
}

class InvoiceService {
  getDueDate(invoiceDate: Date): Date {
    return ExtendedDateUtils.addBusinessDays(invoiceDate, 30);
  }
}
```

---

## 🎯 Key Takeaway

**Extend libraries centrally, don't work around them repeatedly.** Create wrapper classes or extension methods to add missing functionality once, then use consistently throughout the codebase.

---

## 🔗 Related

- [[dont-repeat-yourself]] - Don't repeat workarounds
- [[smells-like-duplicate-code]] - Repeated library workarounds
- [[composition-over-inheritance]] - Wrapper pattern

**Part of**: [[smells-moc]]
**Tags**: #code-smell #coupler #library #extension
