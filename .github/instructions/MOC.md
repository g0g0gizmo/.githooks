# Core Principles: Master of Contents

**Location**: `~/AppData/Roaming/Code/User/core/`
**Purpose**: Map all zettlekasten core principles
**Audience**: You + AI (building mind-mapped knowledge system)

---

## 🎯 What Are Core Principles?

Core principles are the **foundational rules** for building and maintaining atomic, reusable, interconnected notes.

They guide how you:
- Write notes (atomic, scoped, complete)
- Link notes (context-full connections)
- Organize notes (discoverable, composable)
- Maintain notes (evergreen, evolving)

---

## 📋 Core Principles

### 1. **Atomic** ✅
**File**: `atomic.md`
**Concept**: Each note = ONE idea (task, concept, command)
**Key Rules**:
- One idea, one note
- Standalone (complete without others)
- Concise (≤1000 chars)
- Reusable (works in many contexts)
- Linkable (references other notes)

**Why**: Eliminate duplication. Write once, link everywhere.

**Example**: `[[SSH into Production Server]]` written once, referenced in Deploy, Troubleshoot, Restart Service, etc.

---

### 2. **Scoped** (Coming)
**File**: `scoped.md`
**Concept**: Task is complete start-to-finish with atomic subtasks
**Key Rules**:
- Task has clear boundaries (scope)
- Subtasks are atomic (single command/item)
- Everything needed to complete is included
- Clear what's before/after

**Why**: Define exact scope. No hidden dependencies. Complete workflows.

**Example**: `[[Deploy Application]]` scoped: includes SSH, pull code, migrate, restart, verify. Each subtask atomic.

---

### 3. **Linked** (Coming)
**File**: `linked.md`
**Concept**: Notes connected with context-full links
**Key Rules**:
- Links have WHY (explain connection)
- No orphaned notes
- Bi-directional where relevant
- Creates mind map structure

**Why**: Build knowledge graph. Discover relationships. Context matters.

**Example**: `[[SSH into Server]]` links to [[Deploy]] with context: "first step in deployment process"

---

### 4. **Code-Synced** (Coming)
**File**: `code-synced.md`
**Concept**: Notes reference actual code locations
**Key Rules**:
- Every concept links to code: `file:line_number`
- Keeps docs in sync with implementation
- Implementation examples included
- Real, working code

**Why**: Truth is in the code. Docs should match.

**Example**: `[[Error Handling Pattern]]` links to `src/middleware/error.ts:42` showing actual implementation

---

### 5. **Discoverable** (Coming)
**File**: `discoverable.md`
**Concept**: Notes findable via tags, MOCs, and navigation
**Key Rules**:
- Tagged for discovery (#task, #process, #concept)
- MOC provides navigation
- Clear hierarchy/structure
- Search-friendly naming

**Why**: Easy to find what you need. Your mind map is navigable.

**Example**: Tags: #deployment, #production, #server → find all related notes

---

### 6. **Composable** (Coming)
**File**: `composable.md`
**Concept**: Atomic notes combine into larger documents
**Key Rules**:
- Build docs from existing atoms
- No new content, just references
- Tutorials are sequences of atoms
- Reuse, don't recreate

**Why**: DRY principle for documentation. One fact, many uses.

**Example**: Tutorial: "Deploy to Production" = compose [[SSH]], [[Pull Code]], [[Migrate]], [[Restart]], [[Verify]]

---

### 7. **Evergreen** (Coming)
**File**: `evergreen.md`
**Concept**: Notes remain true over time
**Key Rules**:
- Principles, not implementation details
- Avoid version-specific info
- Timeless and reusable
- Update without breaking

**Why**: Long-lasting knowledge. Invest once, use forever.

**Example**: `[[Error Handling Pattern]]` is evergreen. `[[Using Node v16 for...]]` is not.

---

## 🔄 Principle Relationships

```
ATOMIC (foundation)
    ↓
  SCOPED (organize atomic into workflows)
    ↓
  LINKED (connect workflow steps)
    ↓
  CODE-SYNCED (tie to implementation)
    ↓
  DISCOVERABLE (make findable)
    ↓
  COMPOSABLE (build from atoms)
    ↓
  EVERGREEN (keep lasting)
```

**Start**: Master atomic first
**Then**: Expand to scoped, linked, etc.

---

## 📖 How to Use This MOC

### For Understanding
1. Read `atomic.md` - Learn foundation
2. Understand relationships above
3. Expand to other principles as needed

### For Building Notes
1. Check atomic.md - Is this atomic?
2. Check scoped.md - Is scope clear?
3. Check linked.md - Are connections context-full?
4. Check others as relevant

### For Maintaining Notes
1. Check principles regularly
2. Refactor non-atomic notes
3. Add missing links
4. Keep evergreen

---

## 🎯 Current Status

| Principle                     | Status     | File                              |
| ----------------------------- | ---------- | --------------------------------- |
| Atomic                        | ✅ Complete | `atomic.md`                       |
| Scoped                        | ✅ Complete | `scoped.md`                       |
| Linked                        | ✅ Complete | `linked.md`                       |
| SOLID Principles              | ✅ Complete | `principles-solid.md`             |
| Refactoring Techniques        | ✅ Complete | `refactoring-techniques.md`       |
| Review Dimensions             | ✅ Complete | `review-dimensions.md`            |
| File Naming Conventions       | ✅ Complete | `file-naming-conventions.md`      |
| ETC (Easier To Change)        | ✅ Complete | `etc-principle.md`                |
| DRY (Don't Repeat Yourself)   | ✅ Complete | `dry-principle.md`                |
| Orthogonality & Decoupling    | ✅ Complete | `orthogonality-principle.md`      |
| Take Small Steps              | ✅ Complete | `small-steps-principle.md`        |
| No Fortune Telling            | ✅ Complete | `no-fortune-telling-principle.md` |
| Code Quality Goals            | ✅ Complete | `code-quality-goals.md`           |
| Report Format                 | ✅ Complete | `report-format.md`                |
| Quality Patterns              | ✅ Complete | `quality-patterns.md`             |
| KISS (Keep It Simple, Stupid) | ✅ Complete | `kiss-principle.md`               |
| Testing Standards             | ✅ Complete | `testing-standards.md`            |
| Design by Contract            | ✅ Complete | `design-by-contract.md`           |
| Problem Decomposition         | ✅ Complete | `problem-decomposition.md`        |
| Code Smells (Phase 1)         | ✅ Complete | `smells/smells-moc.md`            |
| Code-Synced                   | ⏳ Coming   | `code-synced.md`                  |
| Discoverable                  | ⏳ Coming   | `discoverable.md`                 |
| Composable                    | ⏳ Coming   | `composable.md`                   |
| Evergreen                     | ⏳ Coming   | `evergreen.md`                    |

---

## 🚀 Quick Reference

### Core Zettelkasten Principles
- **How to write notes?** → `atomic.md`
- **How to organize tasks?** → `scoped.md`
- **How to connect notes?** → `linked.md`

### Code & Design Principles (Foundational)
- **How to design code?** → `principles-solid.md` (SOLID 5 principles)
- **How to refactor code?** → `refactoring-techniques.md` (5 patterns)
- **How to review code?** → `review-dimensions.md` (5 dimensions)
- **How to name files?** → `file-naming-conventions.md` (YYYY_Title.pdf, kebab-case)

### Code & Design Principles (Pragmatic Programmer)
- **How to design for change?** → `etc-principle.md` (Easier To Change - foundational principle)
- **How to avoid duplication?** → `dry-principle.md` (Don't Repeat Yourself)
- **How to decouple components?** → `orthogonality-principle.md` (Orthogonality & Decoupling)
- **How to develop safely?** → `small-steps-principle.md` (Take Small Steps)
- **How to avoid over-engineering?** → `no-fortune-telling-principle.md` (No Fortune Telling / YAGNI)
- **How to keep it simple?** → `kiss-principle.md` (Keep It Simple, Stupid - simplicity through clarity)

### Quality & Review Standards (Phase 2)
- **How to set quality targets?** → `code-quality-goals.md` (5 dimensions: Correctness, Performance, Clarity, Robustness, Maintainability)
- **How to structure code reviews?** → `report-format.md` (Standard review report format with findings and recommendations)
- **How to recognize code problems?** → `quality-patterns.md` (10 anti-patterns and their solutions)

### Advanced Principles (Phase 3)
- **How to establish clear contracts?** → `design-by-contract.md` (Preconditions, postconditions, invariants for robust code)
- **How to solve complex problems?** → `problem-decomposition.md` (Sequential, case analysis, and inductive decomposition techniques)
- **How to verify code correctness?** → `testing-standards.md` (AAA pattern, test pyramid, coverage targets)

### Code Smells & Anti-patterns (Phase 1-3)
- **What are code smells?** → `smells/smells-moc.md` (Master index of all 23 code smells organized by category)
- **Most common smells** → 5 Phase 1 smells: [Long Method](../../.github/copilot/core/principles/smells-like-long-method.md), [Large Class](../../.github/copilot/core/principles/smells-like-large-class.md), [Long Parameter List](../../.github/copilot/core/principles/smells-like-long-parameter-list.md), [Duplicate Code](../../.github/copilot/core/principles/smells-like-duplicate-code.md), [Feature Envy](../../.github/copilot/core/principles/smells-like-feature-envy.md)
- **How to identify and fix smells?** → Each smell file includes detection signs, why it's bad, and multiple refactoring solutions

### Platform Toolkit & Guides
- **VS Code + Copilot + Claude Integration** → `vscode-copilot-claude-toolkit.md` (Complete toolkit with capabilities, tools, tips, tricks, workflows, and extensions)
  - All VS Code features and keyboard shortcuts
  - GitHub Copilot commands and best practices
  - Claude Code tools and capabilities
  - 30+ Awesome VS Code extensions with ratings
  - Workflow recipes and tool combinations
  - Performance optimization tips
  - Online references and resources

### Coming Soon
- **How to tie to code?** → `code-synced.md`
- **How to find notes?** → `discoverable.md`
- **How to reuse notes?** → `composable.md`
- **How to keep notes fresh?** → `evergreen.md`

---

## 🔗 References

**Main MOC**: `~/AppData/Roaming/Code/User/MOC.md`
- Links to all prompts, chatmodes, instructions, guides
- Central hub for entire system

**Per-Repo**: `.github/copilot/guidelines/`
- Apply core principles to code guidelines
- Code standards follow atomic principle
- Security standards follow atomic principle
- All guidelines follow core principles

---

## 💡 Philosophy

Core principles answer: **How should knowledge be structured?**

Answer:
- ✅ Atomic (small, focused)
- ✅ Scoped (clear boundaries)
- ✅ Linked (connected, contextualized)
- ✅ Code-synced (tied to reality)
- ✅ Discoverable (easy to find)
- ✅ Composable (built from pieces)
- ✅ Evergreen (lasting value)

This structure enables:
- 🧠 Mind mapping (visualize knowledge)
- 🔗 Reusability (write once, use many times)
- 📈 Scaling (grow without bloat)
- 🎯 Precision (exact scopes, clear links)
- ⚡ Speed (scannable, findable)

---

## ✨ Remember

Your knowledge system is built on these core principles.

Master them, and everything else flows.

---

**Version**: 1.0
**Created**: 2025-11-09
**Purpose**: Map all core principles
**Next**: Read atomic.md, then expand to others

🚀 **Build your knowledge system right. Start with core principles.**
