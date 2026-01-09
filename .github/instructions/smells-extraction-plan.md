# Code Smells Extraction Plan

**Source**: https://refactoring.guru/refactoring/smells
**Purpose**: Create individual core principle files for each code smell (negative principles / "don't do")
**Format**: Each smell gets its own .md file following the core principle template
**Total Smells**: 23

---

## 📋 Code Smells by Category

### 1. BLOATERS (Code That's Too Much)

Bloaters are code elements that have increased to such gargantuan proportions that they are hard to work with.

- [ ] `long-method-smell.md` - Long Method
- [ ] `large-class-smell.md` - Large Class
- [ ] `primitive-obsession-smell.md` - Primitive Obsession
- [ ] `long-parameter-list-smell.md` - Long Parameter List
- [ ] `data-clumps-smell.md` - Data Clumps

**Total**: 5 smells

---

### 2. OBJECT-ORIENTATION ABUSERS (OOP Gone Wrong)

These smells represent incomplete or incorrect application of object-oriented programming principles.

- [ ] `alternative-classes-smell.md` - Alternative Classes with Different Interfaces
- [ ] `refused-bequest-smell.md` - Refused Bequest
- [ ] `switch-statements-smell.md` - Switch Statements
- [ ] `temporary-field-smell.md` - Temporary Field

**Total**: 4 smells

---

### 3. CHANGE PREVENTERS (Hard to Modify)

These smells make it difficult to change code because changes ripple through the system in unexpected ways.

- [ ] `divergent-change-smell.md` - Divergent Change
- [ ] `parallel-inheritance-smell.md` - Parallel Inheritance Hierarchies
- [ ] `shotgun-surgery-smell.md` - Shotgun Surgery

**Total**: 3 smells

---

### 4. DISPENSABLES (Unnecessary Code)

These smells are "pointless and unneeded" elements that should be removed.

- [ ] `comments-smell.md` - Comments (Excessive/Misleading Comments)
- [ ] `duplicate-code-smell.md` - Duplicate Code
- [ ] `data-class-smell.md` - Data Class
- [ ] `dead-code-smell.md` - Dead Code
- [ ] `lazy-class-smell.md` - Lazy Class
- [ ] `speculative-generality-smell.md` - Speculative Generality

**Total**: 6 smells

---

### 5. COUPLERS (Too Tightly Connected)

These smells contribute to excessive coupling between classes and objects.

- [ ] `feature-envy-smell.md` - Feature Envy
- [ ] `inappropriate-intimacy-smell.md` - Inappropriate Intimacy
- [ ] `incomplete-library-smell.md` - Incomplete Library Class
- [ ] `message-chains-smell.md` - Message Chains
- [ ] `middle-man-smell.md` - Middle Man

**Total**: 5 smells

---

## 📊 Organization Strategy

### File Naming Convention
All smell files follow pattern: `{smell-name}-smell.md`

Examples:
- `long-method-smell.md`
- `large-class-smell.md`
- `duplicate-code-smell.md`

### File Structure (Template)
Each smell file will include:

```
# Code Smell: {Smell Name}

**Purpose**: Identify and understand this code smell
**Audience**: You + AI (code review, refactoring)
**Category**: [Bloaters/OO Abusers/Change Preventers/Dispensables/Couplers]
**Severity**: [Low/Medium/High]

---

## 🎯 What Is This Smell?

[Definition and why it matters]

---

## 🚩 Detection Signs

[Checklist of how to recognize this smell]

---

## 💔 Why It's Bad

[Impacts and consequences]

---

## ✅ Refactoring Solutions

[How to fix this smell, with examples]

---

## 🔍 When It Might Be OK

[Exceptions where this smell might be acceptable]

---

## 📚 Relationship to Core Principles

[Links to other core principles]

---

## ✨ Remember

[Key takeaway]
```

---

## 🎯 Recommended Implementation Plan

### Phase 1: Foundation (Immediate)
Start with the most common and impactful smells:
1. `duplicate-code-smell.md` - Most common
2. `long-method-smell.md` - Very common
3. `large-class-smell.md` - Very common
4. `long-parameter-list-smell.md` - Very common
5. `feature-envy-smell.md` - Common coupling issue

**Effort**: ~2-3 hours for 5 smells
**Impact**: High - covers most code review issues

### Phase 2: Essential (High Priority)
Next batch of important smells:
6. `switch-statements-smell.md`
7. `data-clumps-smell.md`
8. `primitive-obsession-smell.md`
9. `temporary-field-smell.md`
10. `shotgun-surgery-smell.md`
11. `divergent-change-smell.md`
12. `inappropriate-intimacy-smell.md`

**Effort**: ~4-5 hours for 7 smells
**Impact**: High - covers architectural issues

### Phase 3: Complete (Lower Priority)
Remaining smells:
13. `comments-smell.md`
14. `dead-code-smell.md`
15. `lazy-class-smell.md`
16. `speculative-generality-smell.md`
17. `refused-bequest-smell.md`
18. `parallel-inheritance-smell.md`
19. `alternative-classes-smell.md`
20. `data-class-smell.md`
21. `incomplete-library-smell.md`
22. `message-chains-smell.md`
23. `middle-man-smell.md`

**Effort**: ~5-6 hours for 11 smells
**Impact**: Medium - covers edge cases and refinements

---

## 🔗 Supporting Files Needed

1. **smells-moc.md** - Master index of all code smells
   - Organized by category
   - Links to all individual smell files
   - Quick reference guide

2. **Update core/MOC.md** - Link to smells section
   - Add "Code Smells" category
   - Reference smells-moc.md

---

## 💾 Total Project Scope

- **Files to Create**: 23 individual smell files + 1 smells-moc.md = 24 files
- **Total Size Estimate**: ~200 KB (assuming 8-10 KB per smell)
- **Time Estimate**: 10-15 hours total (3 phases)
- **Folder**: C:\Users\g0g0g\AppData\Roaming\Code\User\core\smells\

---

## ✨ Outcomes

After completing all code smells:

✅ **Comprehensive Code Smell Catalog**
- All 23 refactoring.guru smells covered
- Consistent structure and depth
- Real-world examples and solutions

✅ **Enhanced Code Review System**
- Report format + quality patterns + code smells
- Three levels of issue detection
- Complete quality vocabulary

✅ **Better Code Decisions**
- Know what to avoid ("don't do" principles)
- Understand consequences
- Know how to fix issues

---

## 🚀 Next Steps

**Option 1**: Start with Phase 1 immediately (5 core smells)
**Option 2**: Create all 24 files in one session
**Option 3**: Create smells-moc.md first, then start with Phase 1

Recommendation: Phase 1 first (high ROI), then Phase 2 (essential), then Phase 3 (comprehensive).

---

**Version**: 1.0
**Created**: 2025-11-09
**Purpose**: Plan extraction of all refactoring.guru code smells
**Next**: Choose phase and begin creating individual smell files

