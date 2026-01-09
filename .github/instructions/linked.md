# Core Principle: Linked Notes

**Purpose**: Connect notes with context-full links to create mind map
**Audience**: You + AI (building knowledge graph)
**Focus**: Meaningful connections that reveal relationships

---

## 🎯 What is a Linked Note?

A linked note is:


- **Connected to other notes** (not orphaned)
- **With context for the link** (explains WHY connected)
- **Part of a knowledge graph** (see relationships)
- **Bi-directional** (A links to B, B references A)
- **Discoverable** (follow links to find related ideas)

**Core Idea**: Links create your mind map. Links with context create understanding.

---

## 🔑 Principle: Links Have Context

Every link must explain **WHY** the notes are connected.


**Bad link** (no context):

```
See also: [[Error Handling]]
```

❌ Why are they related?
❌ How does this connect?
❌ When would I follow this link?


**Good link** (with context):

```
See also: [[Error Handling with Try/Catch]]
- why: Shows the error handling pattern used in this authentication flow
- when: If you need to understand how errors are caught during login
- alternative: [[Promise Error Patterns]] for callback-based approach
```

✅ Clear relationship
✅ Understand context immediately
✅ Know when to follow

---

## 🧭 Principle: Build Mind Maps

Links between notes create a **knowledge graph** - your mind map.

**Example Mind Map**:

```
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

Notice:

- `[[SSH into Production Server]]` appears in multiple paths
- `[[Check Server Logs]]` is reused in troubleshooting and monitoring
- Links show relationships
- Mind map connects all processes

---

## 🔗 Principle: No Orphaned Notes


Every note should be **linked from somewhere** and **link to somewhere**.

**Orphaned note** (bad):

```
# Error Handling Pattern

Pattern: try/catch blocks
...
(No links to it, not referenced anywhere)
```


❌ Why does this exist?
❌ When would I find it?
❌ How does it fit in my knowledge?

**Integrated note** (good):

```
# Error Handling with Try/Catch

Pattern: ...

Used in:
- [[Authentication Flow]] (handles login errors)
- [[API Error Handling]] (handles request errors)
- [[Deploy Application]] (handles deployment errors)

Related patterns:
- [[Guard Clause Pattern]] (alternative for simple checks)
- [[Promise Error Handling]] (async approach)
- [[Error Boundary Pattern]] (React context)

References this in code:
- src/middleware/error.ts:42
- src/auth/login.ts:18
```

✅ Clear where it's used
✅ Related notes linked
✅ Code references included
✅ Part of knowledge graph

---

## 🔄 Principle: Bi-Directional Links


When A links to B, B should reference A (when relevant).

**Example**:

Note A: `[[Deploy Application]]`


```
Step 3: [[Run Database Migrations]]
- why: Updates database schema for new code
```

Note B: `[[Run Database Migrations]]`

```
Used in: [[Deploy Application]] (step 3, schema updates)
Rollback: [[Rollback Migrations]] (undo if deployment fails)
```

Both notes reference each other. You can start from either and understand the relationship.

---

## 📍 Principle: Links Show Navigation Paths

Links reveal **how ideas relate** and create **discovery paths**.

**Discovery Paths**:

```
Path 1: Learn Deployment
→ [[Deploy Application]] (start here, overview)
→ [[SSH into Server]] (first step)
→ [[Pull Code]] (second step)
→ [[Verify Deployment]] (last step)

Path 2: Handle Failures
→ [[Deploy Application]] (when it fails)
→ [[Troubleshoot Failed Deployment]] (diagnose)
→ [[Check Server Logs]] (investigate)
→ [[Emergency Rollback]] (recover)

Path 3: Understand SSH
→ [[SSH into Server]] (atomic concept)
→ [[Generate SSH Key]] (prerequisite)
→ [[Security: SSH Best Practices]] (related concept)
→ [[VPN Connection]] (alternative network access)
```

Users can follow different paths depending on their goal.


---

## 🎯 Principle: Link Types and Context

Different link types, each with context:

### Type 1: Part Of

```

This is part of a larger task:

[[Run Database Migrations]]
- part of: [[Deploy Application]] (step 3 of 5)
- executed after: [[Pull Latest Code]]
- before: [[Restart Service]]
```


### Type 2: Prerequisite

```
This must happen first:

[[SSH into Production Server]]
- prerequisites: [[Get SSH Key from Vault]], [[VPN Connection]]
```

### Type 3: Related Pattern


```
Similar or alternative approach:

[[Error Handling with Try/Catch]]
- related patterns:
  - [[Guard Clause Pattern]] (for simple checks)
  - [[Promise Error Handling]] (for promises)
  - [[Error Boundary Pattern]] (for React)
```


### Type 4: Rollback/Recovery

```
How to undo this:

[[Deploy Application]]
- if fails: [[Troubleshoot Failed Deployment]]
- emergency undo: [[Emergency Rollback]]

```

### Type 5: Code Reference

```
Actual implementation:

[[Error Handling Pattern]]
- implemented in: src/middleware/error.ts:42
- used in: src/auth/login.ts:18, src/api/handlers.ts:5
```

### Type 6: Concept Reference

```
Theoretical foundation:

[[Deployment Strategy]]
- based on: [[Blue-Green Deployment Pattern]]
- similar to: [[Canary Deployment]], [[Rolling Deployment]]
```

---

## ❌ Anti-Patterns: Don't Do This

### Anti-Pattern 1: Links Without Context

```
❌ See also: [[Error Handling]]
   (Why? When? How related?)

✅ See also: [[Error Handling with Try/Catch]]
   - why: Shows error pattern used here
   - when: If you need to understand error handling
```

### Anti-Pattern 2: Orphaned Notes

```
❌ Note exists but isn't linked from anywhere

✅ Note is referenced in:
   - [[Parent Task]] (as a step)
   - [[Related Task]] (alternative approach)
   - [[Learning Path]] (in a sequence)
```

### Anti-Pattern 3: One-Way Links Only

```
❌ [[Deploy]] → [[SSH]]
   But [[SSH]] doesn't mention [[Deploy]]

✅ [[Deploy]] → [[SSH]] (step 1)
   [[SSH]] ← [[Deploy]] (used in deployments)
   Bi-directional
```

### Anti-Pattern 4: Too Many Links (Link Spam)

```
❌ [[Concept A]] links to 50 other notes
   (Unfocused, no priority)

✅ [[Concept A]] links to:
   - [[Prerequisite]] (must know)
   - [[Related Pattern]] (alternative)
   - [[Code Example]] (reference)
   - [[Next Steps]] (what follows)
   (Focused, contextual)
```

### Anti-Pattern 5: Circular Loops Without Context

```
❌ A → B → C → A (loops with no purpose)

✅ A → B (B builds on A)
   B → C (C extends B)
   C → A (back to A with context: "compare with original")
   Clear path, not confusing
```

---

## ✅ Checklist: Linked Note Quality

A good linked note:

- [ ] **Connected**: Has links from other notes
- [ ] **Links out**: References related notes
- [ ] **Context**: Each link explains WHY
- [ ] **No orphans**: Every note has a purpose
- [ ] **Bi-directional**: Related notes reference back
- [ ] **Clear paths**: Easy to follow discovery paths
- [ ] **Focused links**: Relevant, not spam
- [ ] **Code-synced**: Links to actual implementation

---

## 🔄 Linking Workflow

### When Creating a New Note

```
1. Create the atomic or scoped note
2. Identify: where does this fit in my knowledge?
3. Find related notes
4. Link from existing notes TO this one
5. Link from this note to related ones
6. Add context for each link
7. Make sure not orphaned (has at least 2-3 links)
8. Done
```

### When Updating Links

```
1. Review existing links
2. Are they still relevant?
3. Are contexts still accurate?
4. Missing any obvious connections?
5. Add new links if appropriate
6. Remove outdated links
7. Test following links
8. Done
```

### When Following a Link

```
1. Read the source note context
2. Understand why you're following this link
3. Read the linked note
4. Understand how it relates
5. Follow other links from there if needed
6. Back to source to continue
```

---

## 💡 Examples: Linking in Action

### Example 1: Complete Linking for Deploy Task

```
# Deploy Application

This is a scoped task. Full structure:

## Overview
1. [[SSH into Production Server]]
   - why: Access server for deployment operations

2. [[Pull Latest Code]]
   - why: Get new code changes

3. [[Run Database Migrations]]
   - why: Update schema for new code
   - related: [[Database Backup Strategy]] (safety)
   - rollback: [[Rollback Migrations]]

4. [[Restart Service]]
   - why: Load new code

5. [[Verify Deployment]]
   - why: Confirm success

## If Deployment Fails
[[Troubleshoot Failed Deployment]]
- why: Diagnose and fix issues
- includes: [[Check Server Logs]], [[Emergency Rollback]]

## Related Workflows
- [[Blue-Green Deployment]] (alternative strategy)
- [[Canary Deployment]] (gradual rollout)
- [[Monitor Production]] (post-deployment)

## Safety
- Always check: [[Pre-Deployment Checklist]]
- Emergency: [[Emergency Rollback]]
- Questions: [[When to Deploy]]

## Code Reference
- Deployment script: scripts/deploy.sh
- Configuration: config/deploy.yml
```

Each link has context. Mind map is visible.

### Example 2: Concept with Multiple Link Types

```
# Error Handling with Try/Catch

## Definition
Try/catch pattern for synchronous and async error handling

## Used In (Part Of)
- [[Authentication Flow]] (handles login errors)
- [[API Error Handling]] (handles request errors)
- [[Deploy Application]] (handles deploy errors)

## Prerequisites (Learn First)
- [[JavaScript Promises]] (async concept)
- [[Error Objects]] (what are errors)

## Related Patterns (Alternatives)
- [[Guard Clause Pattern]] (simpler checks)
- [[Promise .catch()]] (promise-based)
- [[Error Boundary Pattern]] (React context)
- [[Result Type Pattern]] (functional approach)

## Code Example
src/middleware/error.ts:42
- Shows: actual try/catch pattern
- used in: src/auth/login.ts:18

## Learning Path
1. Start: [[JavaScript Promises]]
2. Then: [[Error Objects]]
3. Then: This note
4. Next: [[Advanced Error Handling]]

## When to Use
- Async functions
- Risky operations
- Need to catch and handle
- See also: [[Error Handling Decision Tree]]
```

Connected to everything. Clear why it matters.

---

## 🧠 Building Mind Maps Through Links

Your goal: **Create a mind map of your knowledge**.


```
Notes (atoms)
    ↓
Linked together
    ↓
Form mind map
    ↓
Discoverable from many angles
    ↓
Reusable across contexts
```

Example: Can I find "Error Handling" from:

- [[Deploy Application]]? Yes (step might have errors)
- [[API Design]]? Yes (endpoint errors)
- [[Authentication]]? Yes (login errors)
- [[Testing]]? Yes (test error cases)

One concept, reachable from many paths.

---

## 🎓 Philosophy

Linked notes are about **connection and discovery**:

✅ **Build knowledge graph** - See relationships
✅ **Create navigation** - Multiple paths to knowledge
✅ **Enable reuse** - Find existing solutions
✅ **Build context** - Understand relationships
✅ **Scale gracefully** - Add notes, all connected

This is how you turn isolated facts into interconnected knowledge.

---

## 📚 Relationship to Atomic and Scoped

- **Atomic**: One idea, standalone

- **Scoped**: One complete task, multiple atomic steps
- **Linked**: All connected, forming mind map

```
Atomic notes: Building blocks
Scoped notes: Workflows using building blocks
Linked: Connections showing relationships
Result: Mind map of interconnected knowledge
```

---

## ✨ Remember

A linked note is:

```
CONNECTED to other notes
WITH CONTEXT for links
PART OF a knowledge graph
DISCOVERABLE from multiple paths
BI-DIRECTIONAL where relevant
FOCUSED links (not spam)
```

Write notes that connect. Build a mind map.

That's linked.

---

**Version**: 1.0
**Location**: `~/AppData/Roaming/Code/User/core/linked.md`
**Created**: 2025-11-09
**Purpose**: Foundation for connecting notes into mind maps
**Prerequisites**: Understand [[atomic-notes]] and [[scoped.md]] first

🚀 **Link your notes. Build your mind map.**
