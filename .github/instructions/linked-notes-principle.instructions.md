---
description: 'Connect notes with context-full links to create knowledge graphs and meaningful relationships'
applyTo: '**/*'
---


## Core Engineering Principles

This instruction set applies the following foundational principles:

- [Atomic Notes](atomic-notes.instructions.md) - Individual notes that can be linked
- [DRY (Don't Repeat Yourself)](dry-principle.instructions.md) - Link to existing knowledge instead of duplicating

When implementing these guidelines, always consider how they reinforce these core principles.

# Linked Notes Principle

## Overview

A linked note is connected to other notes through meaningful, contextual links that explain WHY the notes are related. Links create knowledge graphs that reveal relationships, enable discovery, and build understanding. Effective linking transforms isolated notes into a navigable mind map.

Linked notes ensure:

- Meaningful connections between ideas
- Context for every link (explains WHY)
- Bi-directional references
- Discoverable relationships
- Knowledge graph visualization
- No orphaned notes

## Core Concepts

### 1. Links Have Context

Every link must explain **WHY** the notes are connected, not just that they are.

**Bad link (no context)**:

```text
See also: [[Error Handling]]
```

❌ Why are they related?
❌ How does this connect?
❌ When would I follow this link?

**Good link (with context)**:

```text
See also: [[Error Handling with Try/Catch]]
- why: Shows the error handling pattern used in this authentication flow
- when: If you need to understand how errors are caught during login
- alternative: [[Promise Error Patterns]] for callback-based approach
```

✅ Clear relationship
✅ Understand context immediately
✅ Know when to follow

---

### 2. Bi-Directional References

If Note A links to Note B, Note B should reference Note A (or at least be discoverable from A).

**Example**:

**Note A - Deploy Application**:
```text
# Deploy Application

Steps:
1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
```

**Note B - SSH into Production Server**:
```text
# SSH into Production Server

Command: ssh user@prod.example.com
Used in: [[Deploy Application]], [[Troubleshoot Production]]
Related: [[Connect to VPN]]
```

Notice: Note B references where it's used (back-reference to Note A).

---

### 3. Build Knowledge Graphs

Links between notes create a **knowledge graph** - your navigable mind map.

**Example Mind Map**:

```text
[[Deploy Application]] (scoped task)
    ├─ Step 1: [[SSH into Production Server]] (atomic)
    │   └─ Prerequisites: [[Get SSH Key from Vault]] (atomic)
    │   └─ Related: [[VPN Connection]] (atomic, alternative path)
    │
    ├─ Step 2: [[Pull Latest Code]] (atomic)
    │   └─ Related: [[Merge Code Review]] (atomic, prerequisite)
    │
    ├─ Step 3: [[Run Database Migrations]] (atomic)
    │   └─ Related: [[Database Backup Strategy]] (atomic)
    │   └─ Rollback: [[Rollback Migrations]] (atomic)
    │
    ├─ Step 4: [[Restart Service]] (atomic)
    │   └─ Related: [[Monitor Service Health]] (atomic)
    │
    └─ Step 5: [[Verify Deployment]] (atomic)
        └─ If fails: [[Troubleshoot Failed Deployment]] (scoped)
            └─ [[Emergency Rollback]] (atomic)

[[Troubleshoot Failed Deployment]] (scoped)
    ├─ [[Check Server Logs]] (atomic, reused from other workflows)
    ├─ [[Check Error Patterns]] (atomic)
    ├─ [[Check Database State]] (atomic)
    └─ Recovery: [[Emergency Rollback]] (atomic)

[[Monitor Production]] (scoped)
    ├─ [[Check Server Logs]] (atomic, reused)
    ├─ [[Check Error Rates]] (atomic)
    └─ Alert on: [[Deployment Failures]] (atomic)
```

**Notice**:
- `[[SSH into Production Server]]` appears in multiple paths
- `[[Check Server Logs]]` is reused in troubleshooting and monitoring
- Links show relationships
- Mind map connects all processes

---

### 4. Link Types

Different types of links serve different purposes:

**Sequential Links** (workflow steps):
```text
1. [[SSH into Server]]
2. [[Pull Code]]
3. [[Run Migrations]]
```

**Prerequisite Links** (dependencies):
```text
Prerequisites: [[Get SSH Key]], [[Connect to VPN]]
```

**Alternative Links** (different approaches):
```text
Alternative: [[Deploy via Docker]] instead of [[Manual Deployment]]
```

**Related Links** (conceptual connections):
```text
Related: [[Error Handling Patterns]], [[Monitoring Strategy]]
```

**Rollback Links** (recovery paths):
```text
If fails: [[Emergency Rollback]]
```

**Reference Links** (more information):
```text
For details: [[Database Migration Guide]]
```

---

## Application Checklist

- [ ] Every link has context explaining WHY it's connected
- [ ] Links specify WHEN to follow them
- [ ] Bi-directional references exist where appropriate
- [ ] No orphaned notes (every note is linked from somewhere)
- [ ] Link types are clear (sequential, prerequisite, alternative, etc.)
- [ ] Links enable discovery of related concepts
- [ ] Knowledge graph is navigable
- [ ] Links don't duplicate content (link instead of copy)

### When Creating Links

1. **Identify Relationships**: How are these notes related?
2. **Add Context**: Why is this link meaningful?
3. **Specify When**: When should someone follow this link?
4. **Choose Link Type**: Sequential, prerequisite, alternative, related?
5. **Create Back-References**: Does the target note reference back?
6. **Verify Navigation**: Can you navigate the knowledge graph?

### When Reviewing Links

- Does the link have context?
- Is it clear WHY these notes are connected?
- Can I navigate both directions?
- Are there orphaned notes?
- Is the relationship type clear?

---

## Related Principles

- [Atomic Notes](atomic-notes.instructions.md) - Individual notes that form the nodes in the knowledge graph
- [Scoped Notes](scoped-notes-principle.instructions.md) - Larger workflows built from linked atomic notes
- [DRY Principle](dry-principle.instructions.md) - Link instead of duplicate

---

## Anti-Patterns

### Anti-Pattern 1: Context-Free Links

```text
See also: [[Error Handling]]
See also: [[Authentication]]
See also: [[Database]]
```

**Fix**: Add context to every link:
```text
Error handling:
- [[Try/Catch Patterns]] - Used in this authentication flow
- [[Promise Error Handling]] - Alternative for async operations

Related concepts:
- [[Authentication Strategies]] - Overview of auth approaches
- [[Database Connection Pooling]] - Performance consideration for auth queries
```

### Anti-Pattern 2: Orphaned Notes

```text
Note exists but is never linked from anywhere.
Can't discover it through navigation.
```

**Fix**: Ensure every note is referenced:
- Add to relevant workflow
- Link from related concepts
- Include in index/MOC (Map of Contents)

### Anti-Pattern 3: One-Way Links Only

```text
Note A links to Note B
Note B doesn't reference Note A
Can't navigate back
```

**Fix**: Add back-references:
```text
# Note B

Used in: [[Note A]], [[Note C]]
Related: [[Note D]]
```

### Anti-Pattern 4: Duplicating Content Instead of Linking

```text
# Deploy Application

Step 1: SSH into production server
Command: ssh user@prod.example.com
Port: 22

Step 2: Pull latest code
Command: git pull origin main

(Content duplicated instead of linked)
```

**Fix**: Link to atomic notes:
```text
# Deploy Application

1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
```

---

## Link Context Template

When creating links, use this template for clarity:

```text
[[Target Note]]
- why: Explains the relationship
- when: When to follow this link
- alternative: Other options if applicable
- prerequisite: What comes before
```

**Example**:

```text
[[Error Handling with Try/Catch]]
- why: Authentication flow uses try/catch for API errors
- when: Understanding how errors are caught during login
- alternative: [[Promise.catch()]] for promise-based code
- prerequisite: [[JavaScript Error Basics]]
```

---

## Why Linked Notes Matter

✅ **Discoverability** - Navigate from concept to concept
✅ **Understanding** - Context reveals relationships
✅ **Reusability** - Find existing notes to reference
✅ **Knowledge Graph** - Visual map of all concepts
✅ **Bi-directional Navigation** - Explore in any direction
✅ **Prevents Duplication** - Link instead of copy

Master linked notes, and your knowledge base becomes a navigable, interconnected mind map that enables discovery and understanding.
