---
description: 'Build reusable, linkable knowledge with small, self-contained notes - one idea per note. Includes instructions for dumping notes to docs folder.'
applyTo: '**/*.md'
---

# Atomic Notes Principle

## Overview

An atomic note represents exactly one idea, task, concept, or command. It is complete, standalone, self-contained (≤1000 chars), and reusable. The core philosophy is: write it once, link it everywhere. Never copy. Never duplicate.

Atomic notes ensure:

- One idea per note for clarity
- Standalone completeness
- Reusability across contexts
- Precise referencing
- Independent updates
- Context-free understanding

## Core Concepts

### 1. One Idea Per Note

Each atomic note represents **exactly one thing**:

- One process (SSH into server, deploy app, run tests)
- One concept (error handling pattern, naming convention)
- One task (create user, validate email, handle timeout)
- One command (install package, start service)

**Why this matters**:

- Understood without context
- Referenced precisely
- Updated without affecting others
- Reused in different contexts
- Linked to other ideas

**Example — Bad (multiple ideas)**:

```text
# Server Setup & Deployment

SSH into production server
Run migrations
Deploy code
Check logs
Restart service
```

**Example — Good (atomic)**:

```text
# SSH into Production Server

SSH command: ssh user@prod.example.com
Port: 22
Key location: ~/.ssh/prod-key
```

Then link to: [[Run Database Migrations]], [[Deploy Code]], [[Check Logs]]

---

### 2. Complete from Start to Finish

An atomic note is **complete** - it contains everything needed to understand or execute the one thing.

Someone (you or AI) should read it and be able to:

- Understand what it is
- Know why it matters
- Know how to do it
- See what comes before/after


**Structure (compact, ≤1000 chars)**:

```text
# Task Name

What: One sentence defining it
Why: Why does it matter?
How: Steps or explanation
Before: What comes before this
After: What comes next
Command/Code: If applicable
Reference: Link to related notes
```

**Example — SSH into production**:

```text
# SSH into Production Server

What: Connect to production via SSH
Why: Required for deployment, debugging, log inspection
How:
  1. Connect to VPN: [[Connect to Production VPN]]
  2. Run: ssh user@prod.example.com
  3. Key: ~/.ssh/prod-key
Port: 22
Before: [[Get SSH Key from Vault]]
After: [[Pull Latest Code]], [[Check Logs]]
```

---

### 3. Self-Contained

An atomic note should be readable **without needing context from other notes**.

**Bad (requires context)**:

```text
# Step 3

Run the migrations command
Check that it worked
```

**Good (self-contained)**:

```text
# Run Database Migrations

Command: npm run migrate
Expected output: "All migrations completed"
If fails: [[Rollback Migrations]]
Related: [[Database Backup Strategy]]
```

---

### 4. Reusable

Atomic notes can be used in multiple workflows without modification.

**Example - Atomic note used in multiple contexts**:

```text
[[Check Server Logs]] used in:
- [[Deploy Application]] workflow
- [[Troubleshoot Production Issues]] workflow
- [[Monitor Service Health]] workflow
- [[Emergency Incident Response]] workflow

Single definition, many uses.
```

---

### 5. Linkable

Atomic notes reference other atomic notes to build complete workflows.

**Bad (monolithic)**:

```text
# Deploy Everything

1. SSH into server (ssh user@prod.example.com, port 22)
2. Pull code (git pull origin main)
3. Run migrations (npm run migrate)
4. Restart (sudo systemctl restart app)
5. Check logs (tail -f /var/log/app.log)
```

**Good (atomic and linked)**:

```text
# Deploy Application

1. [[SSH into Production Server]]
2. [[Pull Latest Code]]
3. [[Run Database Migrations]]
4. [[Restart Application Service]]
5. [[Verify Deployment]]

If deployment fails: [[Emergency Rollback]]
Related: [[Monitor Service Health]]
```

Each linked note is atomic and can be reused elsewhere.

---

## Application Checklist

- [ ] Note represents exactly one idea/task/concept
- [ ] Note is complete from start to finish
- [ ] Note is self-contained (no external context required)
- [ ] Note is ≤1000 characters
- [ ] Note can be reused in multiple contexts
- [ ] Note links to related atomic notes
- [ ] Note has clear "before" and "after" context
- [ ] Note includes command/code if applicable
- [ ] Note explains WHY, not just WHAT

### When Creating Atomic Notes

1. **Identify the Single Idea**: What exactly is this note about?
2. **Make it Complete**: What does someone need to know?
3. **Keep it Bounded**: Only include what's essential
4. **Add Context**: What comes before/after?
5. **Link Related Notes**: What other notes connect?
6. **Verify Independence**: Can it stand alone?

### When Reviewing Notes

- Does this note represent one thing?
- Is it complete without external context?
- Could it be reused elsewhere?
- Are links to related notes clear?
- Is it under 1000 characters?

---

## Related Principles

- [DRY Principle](../archive-of-instructions/dry-principle.instructions.md) - Atomic notes embody DRY by being written once and linked everywhere
- [Scoped Notes](../archive-of-instructions/scoped-notes-principle.instructions.md) - Scoped notes are composed of atomic subtasks
- [Linked Notes](../archive-of-instructions/linked-notes-principle.instructions.md) - Atomic notes are connected through meaningful links

---

## Anti-Patterns

### Anti-Pattern 1: Multiple Ideas in One Note

```text
# Deployment and Monitoring

Deploy code to production
Monitor service health
Check error rates
Set up alerts
Review logs
```

**Fix**: Split into atomic notes:

- [[Deploy to Production]]
- [[Monitor Service Health]]
- [[Check Error Rates]]
- [[Set Up Monitoring Alerts]]
- [[Review Application Logs]]


### Anti-Pattern 2: Incomplete Notes

```text
# Deploy

Run deployment script
```

**Fix**: Make it complete:

```text
# Deploy Application to Production


What: Deploy latest code to production server
Command: ./deploy-prod.sh
Prerequisites: [[SSH into Production Server]]
Expected output: "Deployment successful"
Time: ~5 minutes
If fails: [[Emergency Rollback]]
Related: [[Verify Deployment]]
```

### Anti-Pattern 3: Context-Dependent Notes

```text
# Step 2

Now pull the latest changes
```

**Fix**: Make it self-contained:

```text

# Pull Latest Code

Command: git pull origin main
Location: /var/www/app
Expected: "Already up to date" or "Updating..."
Before: [[SSH into Production Server]]
After: [[Run Database Migrations]]
```

---

## Why Atomic Notes Matter

✅ **Reusability** - Write once, use everywhere
✅ **Clarity** - One idea is easy to understand
✅ **Maintainability** - Update in one place
✅ **Composability** - Build workflows from atomic pieces
✅ **Independence** - Change one without affecting others
✅ **Discoverability** - Easy to find and reference

Master atomic notes, and your knowledge base becomes modular, reusable, and maintainable.

---

# Dumping Atomic Notes to the docs Folder

## Overview

When creating or exporting atomic notes, always dump (save) them as individual markdown files into the `docs` folder. This ensures discoverability, versioning, and easy linking.

## Instructions

- If the `docs` folder does not exist at the project root, create it before dumping any notes.
- Each atomic note should be saved as a separate `.md` file in the `docs` folder.
- File names should be descriptive, kebab-case, and reflect the note's single idea (e.g., `ssh-into-production-server.md`).
- Only markdown files (`*.md`) are included in this process.
- When linking, always reference the markdown file in `docs` (e.g., `[[docs/ssh-into-production-server.md]]`).
- Do not duplicate notes—write once, link everywhere.

## Example

To dump an atomic note:

1. Check if `docs` exists; if not, create it.
2. Save the note as `docs/task-name.md`.
3. Link to it from other notes or workflows as needed.

---
