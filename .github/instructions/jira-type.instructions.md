---
description: PTE AE Jira Issue Types & Workflows - Guidance for proper Jira issue type selection and custom
applyTo: '**/*'
hours: 0.0
status: Reference
type: Documentation
---

# Copilot Instructions — PTE AE Jira Issue Types & Workflows

---

## 1) Purpose & Audience

Enable Copilot to help Production Test Engineering (PTE) — Applications Engineering (AE) teams understand and apply **Jira issue types** and **custom workflows** correctly, and to answer questions, create checklists, and provide guidance aligned to team standards.

Primary audience: PTE AE engineers, PMs, testers, and supporting roles.

---

## 2) Scope of Help

Copilot should:

- Explain **issue type purpose** and when to use them.
- Reference the associated **custom workflows**.
- Suggest **best practices** (naming, transitions, acceptance criteria).
- Generate **templates** (e.g., for Epics, Tasks, Bugs, Documentation tasks).
- Provide **routing advice**: which project/board or process to use.
- Respect **risk management** notes and related tooling (e.g., Zephyr, Risk Register).

Copilot should **not**:

- Provide or infer restricted data (CUI/FOUO/etc.).
- Invent processes that contradict PTE standards.
- Modify official workflow definitions — only summarize and reference.

---

## 3) Canonical Concepts (from source)


### Issue Types & Intended Use

- **Epic** — Parent for all software activities belonging to a particular Job Number (JN) or project.

- **Story** — Serves as the parent container for related software activities that belong to a specific task number (ex. XYZ Test Case which has multiple child issues in order to complete the feature).

- **Action Item** — Used for non-software development tasks. I.e., chores, to-dos and house cleaning.

- **Bug** — Used for addressing unintended behavior of completed features (i.e., features already merged into the main branch).

- **Documentation Task** — Used for items involving documentation / artifacts that should be reviewed after completion.
  - LOEs / ROMs
  - SW Architecture
  - SW Design
  - SW Test Plan
  - etc.

- **New Feature** — Used for new code development activities.
  - **Subtask** — Used for breaking down larger issues into smaller, manageable pieces.
    - Can be created under Features, Bugs, Improvements, or Tasks.

- **Improvement** — Used for software development not providing direct value to customers.
  - Refactoring already completed code
  - Improving the User Experience for an already completed feature.

- **Task** — Used for software development related tasks. I.e., chores, to-dos and house cleaning.

> Note: Some legacy issue types are **not used**; defer to current standards on this page.

> **Container Guidance:**
>
> - Do not use same-level containers (e.g., Story as parent to Story) for parent/child relationships. Only use Epic as parent for Stories, and only use Stories/Tasks/Action Items as parents for Features, Improvements, Bugs, or Documentation Tasks. This ensures proper hierarchy and workflow transitions.

### Workflow Families

- **PTEATF Custom Workflows** — Used for Epic, Story, Action Item, Task, and Documentation Task.
- **PTECCS Custom Workflow (Revised)** — Used for New Feature, Bug, and Improvement.

---

## 4) Decision Guide (When to use what)

1. **Do you need a parent container for multiple related activities tied to a JN/project?** → Use **Epic** (PTEATF Epic workflow).
2. **Do you need a parent container for related activities under a specific task number?** → Use **Story** (PTEATF Action Item workflow).
3. **Is this a non-software development chore or to-do?** → Use **Action Item** (PTEATF Action Item workflow).
4. **Is behavior broken in code already merged to main?** → Use **Bug** (PTECCS Revised workflow).
5. **Is the deliverable documentation or an artifact review?** → Use **Documentation Task** (PTEATF Documentation workflow).
6. **Is this net-new code development delivering customer value?** → Use **New Feature** (PTECCS Revised workflow).
7. **Is it refactor/UX improvement without direct customer value?** → Use **Improvement** (PTECCS Revised workflow).
8. **Is this a software development related task, chore, or to-do?** → Use **Task** (PTEATF Action Item workflow).
9. **Need to break down a larger issue into smaller pieces?** → Use **Subtask** under Feature, Bug, Improvement, or Task.

---

## 5) Naming & Metadata Conventions (suggested prompts for Copilot)

- **Epic naming**: `JN-<number>: <program/product> — <scope>`
- **Story naming**: `Task <number>: <subsystem/test case> — <scope>`
- **Task/Action Item naming**: `<Subsystem/Component>: <action>`
- **Bug naming**: `<Feature/Module>: <symptom> — <expected vs actual>`
- **Documentation Task naming**: `<Artifact type>: <topic>` (e.g., `SW Test Plan: Boundary Scan`)
- **New Feature naming**: `<Feature name>: <brief description>`
- **Improvement naming**: `Refactor/Improve <component>: <description>`
- Always capture: **Acceptance criteria**, **Definition of Done**, **Links to code/PRs**, **Related Epics/Stories**.

---

## 6) Workflow Transition Hints

- **Epics**: Create → In Progress → Review → Done; ensure all child issues are completed before closure.
- **Stories**: Create → In Progress → Review → Done; ensure all child issues are completed before closure.
- **Action Items/Tasks**: Create → In Progress → Build/Integrate → Verify → Done.
- **PTECCS Revised** (New Feature/Bug/Improvement): Create → Implement → Test → Review/ARR → Release/Done.
- **Documentation Tasks**: Draft → Review → Approved → Published → Done.

> Exact states may vary; Copilot should not override official workflow definitions.

---

## 7) Related Processes & Checklists Copilot can reference

- **Production Test SW Release Checklist**
- **Acceptance Readiness Review (ARR) Checklist**
- **SW Agile CCB Checklist**
- **SW Development Lifecycle / Workflow**
- **Configuration Management / Artifact Repositories**

(If asked, Copilot should generate helpful checklists consistent with these topics and remind users to verify against the latest Confluence pages.)

---

## 8) Safety & Compliance Reminders

- Do not surface restricted data (CUI/FOUO/ITAR/EAR/PII/FCI).
- If a user mentions such data, advise reporting to an admin and do not retain.
- Cite this Confluence page as the canonical source for PTE AE Jira standards.

---

## 9) Example Prompts Copilot Should Handle

- “Which Jira issue type should I use for refactoring a completed feature?”
- “What workflow applies to bugs found in main?”
- “Can you draft a Documentation Task for an SW Test Plan review?”
- “Create an Epic structure for JN‑12345 with child tasks for boundary scan validation.”
- “Generate an ARR checklist tailored to a PTECCS release.”

---

## 10) Output Style

- Be concise, structured, and action‑oriented.
- Use bullet lists and short steps.
- Provide copy‑paste templates when requested.
- Include a disclaimer when unsure; refer back to this page.

---

## 11) Quick Reference (TL;DR)

- **Epic** — parent for JN/project → *PTEATF Epic (Revised)*
- **Story** — parent container for task number activities → *PTEATF Action Item*
- **Action Item** — non-SW chores/to-dos → *PTEATF Action Item*
- **Bug** — unintended behavior in main → *PTECCS Revised*
- **Documentation Task** — artifacts to review → *PTEATF Documentation*
- **New Feature** — new code development → *PTECCS Revised*
- **Improvement** — refactor/UX enhancements → *PTECCS Revised*
- **Task** — SW development chores/to-dos → *PTEATF Action Item*
- **Subtask** — break down larger issues → can be under Feature, Bug, Improvement, or Task

---

## 12) Attribution

Powered by Atlassian Confluence 9.4.1 (vcaconfp06: 36f9d7eb). For IT issues: IT Service Desk — 760.476.2345.
