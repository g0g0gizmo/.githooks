---
description: 'Define complete, bounded tasks with atomic subtasks and clear scope boundaries'
applyTo: '**/*'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [Atomic Notes](atomic-notes-principle.instructions.md) - Subtasks are atomic and reusable
- [DRY (Don't Repeat Yourself)](dry-principle.instructions.md) - Reference atomic notes instead of duplicating

When implementing these guidelines, always consider how they reinforce these core principles.

# Scoped Notes Principle

## Overview

A scoped note defines a complete task with clear boundaries - what's included, what's excluded, and all atomic subtasks needed for execution. It represents a complete workflow from start to finish, composed of atomic steps that can be executed or referenced.

Scoped notes ensure:

- Clear task boundaries
- Explicit scope (inclusions and exclusions)
- Atomic subtasks
- No hidden dependencies
- Repeatable execution
- Reusable workflows

## Core Concepts

### 1. Clear Scope Boundaries

Each scoped note has explicit boundaries defining exactly what the task covers.

**Components**:
- **What's included**: Everything needed to complete the task
- **What's excluded**: Related tasks that are separate
- **When to use**: Specific situations where this task applies
- **When NOT to use**: Situations outside scope
- **Prerequisites**: What comes before
- **Outcomes**: What comes after

**Example — Bad (Scope unclear)**:

```text
# Deploy

Run deployment
Check if it works
Fix if needed
```

❌ Scope is fuzzy
❌ What does "deployment" include?
❌ What's "check if it works"?
❌ What if it fails?

**Example — Good (Scope clear)**:

```text
# Deploy Application

## Scope
Includes:
- SSH into server
- Pull latest code
- Run migrations
- Restart service
- Verify deployment

Excludes:
- Key generation (see [[Generate SSH Key]])
- Code review (happens before)
- Rollback (separate task: [[Emergency Rollback]])

Prerequisites: [[SSH into Production Server]]
Time: ~5 minutes
Rollback: [[Emergency Rollback]]
```

---

### 2. Atomic Subtasks

Every subtask in a scoped note is **atomic** - a single command, action, or reference.

No subtask should need explanation or further breakdown.

**Types of subtasks**:

**Type 1: Reference to Another Atomic Note**
```text
[[SSH into Production Server]]
```
Single reference. User knows to follow that process.

**Type 2: Single Command**
```text
git pull origin main
```
One command. No explanation needed (command is clear).

**Type 3: Single Item/Action**
```text
Verify deployment shows "200 OK"
```
One action. Simple. Verifiable.

**Type 4: Simple Decision**
```text
If deployment fails, run [[Emergency Rollback]]
```
One decision. Clear outcome.

**Example — Bad (Not atomic)**:

```text
# Deploy Application

1. Get on the server and pull the latest code
2. Run any migrations that are needed and restart the service
3. Make sure everything is working
```

❌ Multiple actions per step
❌ Vague ("make sure everything is working")
❌ Not executable

**Example — Good (Atomic)**:

```text
# Deploy Application

1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
4. [[Restart Application Service]]
5. [[Verify Deployment]]

If step fails: [[Emergency Rollback]]
```

✅ Each step is atomic
✅ Each step references one clear task
✅ Executable

---

### 3. No Hidden Dependencies

All prerequisites and dependencies are **explicit** in the scoped note.

**Bad (Hidden dependencies)**:

```text
# Deploy Application

1. Pull code
2. Run migrations
3. Restart service
```

Hidden assumptions:
- Already SSHed into server?
- VPN connected?
- SSH key available?
- Database credentials configured?

**Good (Explicit dependencies)**:

```text
# Deploy Application

Prerequisites:
- [[SSH Key Available]]
- [[VPN Connected]]
- [[Database Credentials Configured]]

Steps:
1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
4. [[Restart Application Service]]
5. [[Verify Deployment]]
```

---

### 4. Complete from Start to Finish

A scoped note is **complete** - it contains every step from beginning to end.

**Structure**:

```text
# Task Name

## Scope
Includes: [what's in]
Excludes: [what's out]
When to use: [situations]

## Prerequisites
- [[Prerequisite 1]]
- [[Prerequisite 2]]

## Steps
1. [[Atomic Step 1]]
2. [[Atomic Step 2]]
3. [[Atomic Step 3]]

## Verification
- [How to verify success]

## Rollback
If fails: [[Rollback Procedure]]

## Related
- [[Related Task 1]]
- [[Related Task 2]]
```

**Example**:

```text
# Deploy Application to Production

## Scope
Includes:
- SSH connection
- Code deployment
- Database migrations
- Service restart
- Deployment verification

Excludes:
- Code review (done before)
- SSH key generation (one-time setup)
- Monitoring setup (separate task)

When to use: Deploying approved code to production
Time: ~5 minutes

## Prerequisites
- [[Code Review Approved]]
- [[Tests Passing]]
- [[SSH Key Available]]
- [[VPN Connected]]

## Steps
1. [[SSH into Production Server]]
2. [[Pull Latest Code from Main Branch]]
3. [[Run Database Migrations]]
4. [[Restart Application Service]]
5. [[Verify Deployment Health Check]]

## Verification
- Health check returns 200 OK
- Application logs show "Started successfully"
- No errors in last 5 minutes

## Rollback
If any step fails: [[Emergency Rollback]]

## Related
- [[Monitor Production After Deployment]]
- [[Troubleshoot Failed Deployment]]
```

---

## Application Checklist

- [ ] Scope is clearly defined (includes/excludes)
- [ ] All prerequisites are explicit
- [ ] Every subtask is atomic (single action or reference)
- [ ] No hidden dependencies
- [ ] Complete from start to finish
- [ ] Verification criteria are clear
- [ ] Rollback procedure is documented
- [ ] Time estimate is provided
- [ ] Related tasks are linked

### When Creating Scoped Notes

1. **Define Boundaries**: What's in scope, what's out?
2. **List Prerequisites**: What must be true before starting?
3. **Break Into Atomic Steps**: Each step is single action or reference
4. **Add Verification**: How do you know it worked?
5. **Document Rollback**: What if it fails?
6. **Estimate Time**: How long does this take?

### When Reviewing Scoped Notes

- Are boundaries explicit?
- Are all dependencies visible?
- Is each subtask atomic?
- Could someone execute this without asking questions?
- Is verification clear?

---

## Related Principles

- [Atomic Notes](atomic-notes-principle.instructions.md) - Subtasks are atomic notes
- [Linked Notes](linked-notes-principle.instructions.md) - Scoped notes link to atomic tasks
- [DRY Principle](dry-principle.instructions.md) - Reference atomic notes instead of duplicating

---

## Anti-Patterns

### Anti-Pattern 1: Fuzzy Scope

```text
# Deploy

Do the deployment
Check it works
Fix any issues
```

**Fix**: Define clear boundaries:
```text
# Deploy Application

Scope: Code deployment to production (excludes rollback)
Steps: SSH, pull code, migrate DB, restart service, verify
Time: 5 minutes
```

### Anti-Pattern 2: Non-Atomic Subtasks

```text
1. Get onto the server and pull the code
2. Run migrations and restart everything
3. Check that it's all working properly
```

**Fix**: Make each step atomic:
```text
1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
4. [[Restart Application Service]]
5. [[Verify Deployment]]
```

### Anti-Pattern 3: Hidden Dependencies

```text
# Deploy Application

1. Pull code
2. Restart service
```

**Fix**: Make dependencies explicit:
```text
# Deploy Application

Prerequisites:
- [[SSH Key Available]]
- [[VPN Connected]]
- [[Database Credentials Set]]

Steps:
1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Restart Application Service]]
```

### Anti-Pattern 4: Incomplete Task

```text
# Deploy

Run deployment script
```

**Fix**: Make it complete:
```text
# Deploy Application

Scope: Full production deployment
Prerequisites: [[Code Review Approved]], [[Tests Pass]]

Steps:
1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
4. [[Restart Service]]
5. [[Verify Deployment]]

Verification: Health check returns 200
Rollback: [[Emergency Rollback]]
Time: 5 minutes
```

---

## Why Scoped Notes Matter

✅ **Clarity** - Explicit boundaries eliminate ambiguity
✅ **Completeness** - Everything needed in one place
✅ **Repeatability** - Can be executed consistently
✅ **Composability** - Built from atomic, reusable pieces
✅ **Traceability** - Dependencies are visible
✅ **Maintainability** - Update atomic notes independently

Master scoped notes, and your workflows become clear, complete, and executable processes built from atomic, reusable components.
