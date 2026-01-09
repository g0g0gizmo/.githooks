# Code Smells Master Index

**Purpose**: Central reference for all code smell documentation
**Source**: https://refactoring.guru/refactoring/smells
**Total Smells**: 23 across 5 categories
**Status**: Phase 1 (5 smells) ✅ Complete | Phase 2 (7 smells) ✅ Complete | Phase 3 (11 smells) ✅ Complete

---

## 📊 Quick Reference Table

| Status    | Count | Focus                                 | Impact   |
| --------- | ----- | ------------------------------------- | -------- |
| ✅ Phase 1 | 5     | High-frequency issues in code reviews | Critical |
| ✅ Phase 2 | 7     | Essential architectural issues        | High     |
| ✅ Phase 3 | 11    | Edge cases and refinements            | Medium   |

---

## 🎯 Phase 1: High-Impact Smells ✅

**5 most common and impactful smells you'll encounter in code reviews**

### Bloaters Category (Code That's Too Much)

1. **[Long Method](smells-like-long-method.md)**
   - Functions that do too much (>50 lines)
   - Guideline: 20-50 lines optimal
   - Solutions: Extract Method, Replace Temp with Query, Parameter Object
   - Severity: 🔴 HIGH

2. **[Large Class](smells-like-large-class.md)**
   - Classes that combine multiple responsibilities (>300 lines)
   - Guideline: <200-300 lines, <10 methods, <10 properties
   - Solutions: Extract Classes, Extract by Feature, Extract by Data
   - Severity: 🔴 HIGH

3. **[Long Parameter List](smells-like-long-parameter-list.md)**
   - Functions with too many parameters (5+)
   - Guideline: 1-3 parameters ideal
   - Solutions: Parameter Object, Preserve Whole Object, Builder Pattern
   - Severity: 🟡 MEDIUM-HIGH

### Dispensables Category (Unnecessary Code)

4. **[Duplicate Code](smells-like-duplicate-code.md)**
   - Same logic appears in 2+ places
   - Solutions: Extract Function, Extract Module, Utility Library
   - Severity: 🔴 HIGH
   - Impact: Maintenance cost multiplies with each copy

### Couplers Category (Too Tightly Connected)

5. **[Feature Envy](smells-like-feature-envy.md)**
   - Method uses more data from another class
   - Solutions: Move Method, Extract Method, Pass Derived Values
   - Severity: 🟡 MEDIUM-HIGH
   - Impact: Tight coupling between classes

---

## ✅ Phase 2: Essential Smells - COMPLETE

**7 important smells covering architectural issues and design problems**

### Bloaters Category

6. **[Data Clumps](smells-like-data-clumps.md)** - Related data fields that should be grouped
   - Signs: Same 3+ fields appear together in multiple places
   - Solutions: Extract Class, Introduce Parameter Object
   - Severity: 🟡 MEDIUM-HIGH

7. **[Primitive Obsession](smells-like-primitive-obsession.md)** - Using primitives instead of small objects
   - Signs: Excessive use of strings/numbers instead of domain objects
   - Solutions: Replace Primitive with Object, Replace Type Code with Polymorphism
   - Severity: 🟡 MEDIUM

### Object-Orientation Abusers Category

8. **[Switch Statements](smells-like-switch-statements.md)** - Complex conditionals that should be polymorphism
   - Signs: Multiple switch/if-else based on object type
   - Solutions: Replace Type Code with Polymorphism, Replace Type Code with State/Strategy
   - Severity: 🟡 MEDIUM-HIGH

9. **[Temporary Field](smells-like-temporary-field.md)** - Fields only sometimes populated
   - Signs: Fields with comments like "only used in X scenario"
   - Solutions: Extract Class, Introduce Parameter Object
   - Severity: 🟡 MEDIUM

### Change Preventers Category

10. **[Shotgun Surgery](smells-like-shotgun-surgery.md)** - Small change requires edits in many places
    - Signs: Single change affects 5+ classes
    - Solutions: Move Method, Move Field, Inline Class
    - Severity: 🟡 MEDIUM-HIGH

11. **[Divergent Change](smells-like-divergent-change.md)** - One class changed for multiple reasons
    - Signs: Different methods change for different reasons (SRP violation)
    - Solutions: Extract Class by responsibility
    - Severity: 🟡 MEDIUM-HIGH

### Couplers Category

12. **[Inappropriate Intimacy](smells-like-inappropriate-intimacy.md)** - Classes know too much about each other
    - Signs: One class accessing another's private data
    - Solutions: Move Method, Extract Class, Hide Delegate
    - Severity: 🟡 MEDIUM-HIGH

---

## ✅ Phase 3: Comprehensive Coverage - COMPLETE

**11 remaining smells covering edge cases and refinements**

### Dispensables Category

13. **[Comments](smells-like-comments.md)** - Excessive or misleading comments
    - Signs: Comments explaining obvious code, comments more than code
    - Solutions: Rename methods, Extract Function, Self-documenting code
    - Severity: 🟢 MEDIUM

14. **[Dead Code](smells-like-dead-code.md)** - Code that's never executed
    - Signs: Unused variables, unreachable conditions, deprecated functions
    - Solutions: Delete it, or restore from version control if needed
    - Severity: 🟢 MEDIUM

15. **[Lazy Class](smells-like-lazy-class.md)** - Classes that don't do much
    - Signs: Classes with minimal methods or minimal reasoning to exist
    - Solutions: Inline Class, Collapse Hierarchy
    - Severity: 🟢 MEDIUM

16. **[Speculative Generality](smells-like-speculative-generality.md)** - Generic code for features that may never exist
    - Signs: Generic methods with unused parameters, "just in case" abstraction
    - Solutions: Inline Class, Remove Parameter, Simplify
    - Severity: 🟢 MEDIUM

### Object-Orientation Abusers Category

17. **[Refused Bequest](smells-like-refused-bequest.md)** - Subclass doesn't use inherited methods
    - Signs: Subclass overrides methods with "not implemented" or ignores them
    - Solutions: Replace Inheritance with Delegation, Inline Class
    - Severity: 🟡 MEDIUM-HIGH

18. **[Parallel Inheritance Hierarchies](smells-like-parallel-inheritance-hierarchies.md)** - Need subclass in one hierarchy for each subclass in another
    - Signs: Every subclass of A requires a corresponding subclass of B
    - Solutions: Move Method, Move Field, Extract Class
    - Severity: 🟡 MEDIUM

19. **[Alternative Classes with Different Interfaces](smells-like-alternative-classes-with-different-interfaces.md)** - Classes do similar things but have different interfaces
    - Signs: Multiple classes with similar methods but different names
    - Solutions: Rename Method, Move Method, Extract Superclass
    - Severity: 🟡 MEDIUM

### Couplers Category

20. **[Message Chains](smells-like-message-chains.md)** - Long chain of method calls (train wrecks)
    - Signs: `a.getB().getC().getD().getValue()`
    - Solutions: Hide Delegate, Extract Method, Move Method
    - Severity: 🟡 MEDIUM

21. **[Middle Man](smells-like-middle-man.md)** - Class just delegates to another class
    - Signs: Every method just calls method on field object
    - Solutions: Remove Middle Man, Inline Class, Replace Delegation with Inheritance
    - Severity: 🟢 MEDIUM

22. **[Incomplete Library Class](smells-like-incomplete-library-class.md)** - Library lacks features you need
    - Signs: Need to extend or modify third-party library
    - Solutions: Introduce Foreign Method, Introduce Local Extension, Wrapper
    - Severity: 🟢 MEDIUM

23. **[Data Class](smells-like-data-class.md)** - Class only contains getters/setters
    - Signs: No meaningful behavior, just data containers
    - Solutions: Encapsulate Field, Extract Method, Move Method
    - Severity: 🟢 MEDIUM

---

## 🔍 Smells by Category

### 1️⃣ Bloaters (Code That's Too Much) - 5 Smells

*Bloaters are code elements that have become too large or complex*

| #   | Smell               | Status    | Link                                   |
| --- | ------------------- | --------- | -------------------------------------- |
| 1   | Long Method         | ✅ Phase 1 | [[smells-like-long-method.md]]         |
| 2   | Large Class         | ✅ Phase 1 | [[smells-like-large-class.md]]         |
| 3   | Long Parameter List | ✅ Phase 1 | [[smells-like-long-parameter-list.md]] |
| 6   | Data Clumps         | ⏳ Phase 2 | -                                      |
| 7   | Primitive Obsession | ⏳ Phase 2 | -                                      |

**Common Theme**: Break things into smaller, focused pieces
**Key Principle**: Single Responsibility, Small Steps

---

### 2️⃣ Object-Orientation Abusers (OOP Gone Wrong) - 4 Smells

*Incomplete or incorrect application of OOP principles*

| #   | Smell                | Status    | Link |
| --- | -------------------- | --------- | ---- |
| 8   | Switch Statements    | ⏳ Phase 2 | -    |
| 9   | Temporary Field      | ⏳ Phase 2 | -    |
| 17  | Refused Bequest      | ⏳ Phase 3 | -    |
| 18  | Parallel Inheritance | ⏳ Phase 3 | -    |

**Common Theme**: Use polymorphism instead of conditionals
**Key Principle**: SOLID principles, especially Open/Closed

---

### 3️⃣ Change Preventers (Hard to Modify) - 3 Smells

*Make it difficult to change code; changes ripple unexpectedly*

| #   | Smell                            | Status    | Link |
| --- | -------------------------------- | --------- | ---- |
| 10  | Shotgun Surgery                  | ⏳ Phase 2 | -    |
| 11  | Divergent Change                 | ⏳ Phase 2 | -    |
| 44  | Parallel Inheritance Hierarchies | ⏳ Phase 3 | -    |

**Common Theme**: Tight coupling prevents easy modification
**Key Principle**: ETC (Easier To Change), Orthogonality

---

### 4️⃣ Dispensables (Unnecessary Code) - 6 Smells

*Code that shouldn't be there; pointless and unneeded*

| #   | Smell                  | Status    | Link                              |
| --- | ---------------------- | --------- | --------------------------------- |
| 4   | Duplicate Code         | ✅ Phase 1 | [[smells-like-duplicate-code.md]] |
| 13  | Comments               | ⏳ Phase 3 | -                                 |
| 14  | Dead Code              | ⏳ Phase 3 | -                                 |
| 15  | Lazy Class             | ⏳ Phase 3 | -                                 |
| 16  | Speculative Generality | ⏳ Phase 3 | -                                 |
| 23  | Data Class             | ⏳ Phase 3 | -                                 |

**Common Theme**: Delete unnecessary code
**Key Principle**: DRY, YAGNI (You Aren't Gonna Need It)

---

### 5️⃣ Couplers (Too Tightly Connected) - 5 Smells

*Excessive coupling between classes and objects*

| #   | Smell                  | Status    | Link                            |
| --- | ---------------------- | --------- | ------------------------------- |
| 5   | Feature Envy           | ✅ Phase 1 | [[smells-like-feature-envy.md]] |
| 12  | Inappropriate Intimacy | ⏳ Phase 2 | -                               |
| 20  | Message Chains         | ⏳ Phase 3 | -                               |
| 21  | Middle Man             | ⏳ Phase 3 | -                               |
| 22  | Incomplete Library     | ⏳ Phase 3 | -                               |

**Common Theme**: Reduce coupling between classes
**Key Principle**: Orthogonality, SOLID-D (Dependency Inversion)

---

## 📊 Implementation Status

### Phase 1: Foundation (High ROI) ✅ COMPLETE

- [x] Long Method
- [x] Large Class
- [x] Long Parameter List
- [x] Duplicate Code
- [x] Feature Envy

**Time Invested**: ~2-3 hours
**ROI**: HIGH - Covers most code review issues
**Readiness**: Ready to use in code reviews

### Phase 2: Essential (High Priority) ✅ COMPLETE

- [x] Data Clumps
- [x] Primitive Obsession
- [x] Switch Statements
- [x] Temporary Field
- [x] Shotgun Surgery
- [x] Divergent Change
- [x] Inappropriate Intimacy

**Time Invested**: ~4-5 hours
**ROI**: HIGH - Covers architectural issues
**Readiness**: Ready to use in code reviews

### Phase 3: Complete (Lower Priority) ✅ COMPLETE

- [x] Comments
- [x] Dead Code
- [x] Lazy Class
- [x] Speculative Generality
- [x] Refused Bequest
- [x] Parallel Inheritance Hierarchies
- [x] Alternative Classes with Different Interfaces
- [x] Data Class
- [x] Incomplete Library Class
- [x] Message Chains
- [x] Middle Man

**Time Invested**: ~5-6 hours
**ROI**: MEDIUM - Edge cases and refinements
**Readiness**: Complete framework ready for use

---

## 🔗 Related Files

- **[[../smells-extraction-plan.md]]** - Original extraction plan with category breakdown
- **[[../code-quality-goals.md]]** - Quality dimensions (Correctness, Performance, Clarity, Robustness, Maintainability)
- **[[../quality-patterns.md]]** - Anti-patterns catalog (complementary to code smells)
- **[[../report-format.md]]** - Standard code review report structure

---

## 🎯 How to Use This Index

### For Code Reviews

1. When you find a problematic pattern, look up the smell name
2. Read the smell file to understand detection signs
3. Use the solutions section to guide refactoring discussion
4. Reference the severity to prioritize fixes

### For Learning

1. Start with Phase 1 (5 most impactful smells)
2. Learn to recognize each smell in your own code
3. Practice the refactoring solutions
4. Progress to Phase 2 for architectural understanding
5. Phase 3 for comprehensive smell coverage

### For Documentation

1. Link to smell documentation in code review comments
2. Use smell names as common vocabulary for team discussions
3. Reference severity levels when prioritizing technical debt

---

## 📈 Smell Distribution

```
Bloaters            [5] █████
Dispensables        [6] ██████
Couplers            [5] █████
OO Abusers          [4] ████
Change Preventers   [3] ███
```

**Most Common in Code Reviews**: Bloaters + Duplicate Code
**Most Impactful to Fix**: Change Preventers + Couplers
**Easiest to Spot**: Bloaters + Duplicate Code
**Hardest to Fix**: Change Preventers + OO Abusers

---

## ✨ Remember

**DON'T DO**: Ignore code smells or accumulate technical debt

**DO**: Recognize smells early and refactor incrementally

**Strategy**:

- Phase 1: Build vocabulary and understanding (5 smells)
- Phase 2: Tackle architectural issues (7 smells)
- Phase 3: Master all edge cases (11 smells)

**Outcome**: Complete framework for code quality, maintainability, and team communication

---

**Version**: 2.0
**Location**: `~/AppData/Roaming/Code/User/core/principles/smells-moc.md`
**Created**: 2025-11-09
**Updated**: 2025-11-28
**Source**: https://refactoring.guru/refactoring/smells
**Master Index**: Yes
**Completion Status**: All 23 code smells documented ✅

🚀 **Know the smells. Name them. Fix them. Build better code.**
