---
description: 'Implementation prompt for creating comprehensive automation engineering instruction set (4 files, 630 lines)'
---

# Implement: Comprehensive Automation Engineering Instruction Set

**Status**: Ready for execution
**Anchor**: 1-4 (Sequential implementation)
**Total Duration**: 7 days
**Output**: 4 instruction files in `.github/instructions/`

---

## Pre-Implementation Checklist

Before starting, verify:

- [ ] Read `20250130-automation-engineering-comprehensive-instructions-research.md` (understand approach)
- [ ] Read `20250130-automation-engineering-comprehensive-instructions-plan.instructions.md` (understand milestones)
- [ ] Read `20250130-automation-engineering-comprehensive-instructions-details.md` (understand specifications)
- [ ] Access to `docs/my-daily-needs.md` (reference your actual conventions)
- [ ] Access to git history (verify examples against reality)
- [ ] VS Code with Markdown preview enabled

---

## Anchor 1: automation-workflow-conventions.instructions.md

**Duration**: Days 1-2
**Target**: 200 lines
**ApplyTo**: `**/*.md,**/*.{js,py,sh}`

### Step 1: Create File and Frontmatter

Create file: `.github/instructions/automation-workflow-conventions.instructions.md`

Add frontmatter:

```yaml
---
description: 'Standards for branch naming, commits, PRs, and Definition of Ready/Done in automation engineering workflow'
applyTo: '**/*.md,**/*.{js,py,sh}'
---

# 🔄 Automation Workflow Conventions
```

**Verify**: File exists, YAML is valid

### Step 2: Write Core Principles Section

Based on specifications in details.md (Section 1 → Section 2):

```markdown
## Core Engineering Principles

This workflow applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dry-principle.md) -
  Establish branch/commit conventions once; apply everywhere without variation
- [Code Quality Goals](../core/principles/code-quality-goals.md) -
  Consistent workflow standards improve traceability and maintainability
```

**Verify**: Exactly 2 principle links, paths are relative, semantically aligned

### Step 3: Write Branch Naming Section

Create "## Branch Naming Conventions" section with:

- Pattern definition: `<type>/<JIRAKEY>-<kebab-case-description>`
- Required elements explanation
- 4 good examples (feature, fix, chore, other)
- 4 bad examples with explanations of what's wrong
- Validation rules (5 explicit checks)
- Bash command for local validation

Reference from specifications:

- Lines 26-55 in details.md

**Verify**:

- Pattern is crystal clear
- Examples match your actual branch names (check git branches)
- Validation rules match your pre-commit hook (A1)
- All 4 types shown

### Step 4: Write Commit Message Standards Section

Create "## Commit Message Standards" section with:

- Multi-line format (header, body, footer)
- Required elements explained
- 1 comprehensive good example with rationale explanation
- 4 bad examples with specific issues noted
- Validation rules (5 explicit checks)
- Tool recommendation (commitlint)

Reference from specifications:

- Lines 56-95 in details.md

**Verify**:

- Format is unambiguous (header/body/footer clearly separated)
- Good example shows WHY (rationale), not just WHAT
- Examples match your actual commit history (check git log)
- JIRAKEY requirement is clear and mandatory

### Step 5: Write Pull Request Standards Section

Create "## Pull Request Standards" section with:

- PR description template with all 8 required sections
- Checkboxes for testing and documentation
- Definition of Ready (5 criteria)
- Definition of Done (6 criteria)
- 1 well-formed example PR (all sections complete)
- 1 incomplete PR example with specific issues noted

Reference from specifications:

- Lines 96-145 in details.md

**Verify**:

- Template matches your actual PR template
- Checklist items are actionable
- Examples show realistic PRs (could copy from actual GitHub)
- Definition of Done matches your Jira Definition of Done

### Step 6: Write Key Takeaways Section

Create "## Key Takeaways" section with:

- 5 bullet points summarizing essentials
- Cross-references to other 3 instruction files
- Integration note (how this enables your workflow)

Reference from specifications:

- Lines 146-160 in details.md

**Verify**:

- All 5 key points are covered
- Other 3 files referenced with correct paths
- Integration note ties back to your automation workflow

### Step 7: Final Review

**Content Accuracy**:

- [ ] Branch naming pattern matches your actual branches
- [ ] Commit message format matches your git log
- [ ] PR template sections match what you actually use
- [ ] Definition of Ready/Done criteria match your Jira workflow
- [ ] All examples are realistic and accurate

**Principle Linkage**:

- [ ] 2 principles linked (DRY, Code Quality Goals)
- [ ] Links are valid relative paths
- [ ] Principles are semantically aligned

**Quality**:

- [ ] File is ~200 lines (count lines)
- [ ] Frontmatter is valid YAML
- [ ] Markdown syntax is correct
- [ ] No broken links or references
- [ ] Readable with clear hierarchy

**File location**: `.github/instructions/automation-workflow-conventions.instructions.md`

**Status**: ✅ Anchor 1 complete (ready to move to Anchor 2)

---

## Anchor 2: automation-scripting-standards.instructions.md

**Duration**: Days 3-4
**Target**: 180 lines
**ApplyTo**: `automation/**/*.{py,sh,js}`

### Step 1: Create File and Frontmatter

Create file: `.github/instructions/automation-scripting-standards.instructions.md`

Add frontmatter:

```yaml
---
description: 'Standards for Python, Bash, and Node.js scripts in automation engineering (error handling, logging, testing, structure)'
applyTo: 'automation/**/*.{py,sh,js}'
---

# 🔧 Automation Scripting Standards
```

**Verify**: File exists, YAML is valid

### Step 2: Write Core Principles Section

Based on specifications in details.md:

```markdown
## Core Engineering Principles

This instruction set applies the following foundational principles:

- [SOLID Principles](../core/principles/SOLID.md) -
  Single Responsibility: Each script has one purpose; Open/Closed: Easy to extend without modifying existing scripts
- [Design by Contract](../core/principles/design-by-contract.md) -
  Pre-conditions (valid inputs), post-conditions (expected outputs), error handling guarantees
```

**Verify**: 2 principles linked, relative paths correct

### Step 3: Write Script Structure Section

Create "## Script Structure & Organization" section covering:

- Python: Shebang `#!/usr/bin/env python3`, imports, functions, main() pattern
- Bash: Shebang, error handling with `set -e`, variable naming conventions
- Node: Shebang `#!/usr/bin/env node`, module structure, exports
- 3 examples (one per language) showing proper structure

Reference from specifications:

- Details.md: "Script Structure & Organization"

**Verify**:

- All 3 languages covered
- Examples are syntactically correct
- Structure patterns are enforceable

### Step 4: Write Error Handling Section

Create "## Error Handling & Resilience" section with:

- Python: Try/except patterns, custom exceptions, logging errors
- Bash: Exit codes, `set -e`, error traps
- Node: Try/catch, promise handling, async/await errors
- When to retry: Only transient errors (network, timeouts), not logic errors
- Retry backoff: Exponential backoff pattern
- 3 code examples (one per language)

Reference from specifications:

- Details.md: "Error Handling & Resilience" and example patterns

**Verify**:

- All 3 languages shown
- Error philosophy is consistent (fail fast, log details)
- Retry logic is conservative (don't retry forever)
- Examples are realistic

### Step 5: Write Logging Section

Create "## Logging & Observability" section with:

- When to log: Startup, major milestones, errors, completion
- Log levels: DEBUG, INFO, WARN, ERROR (with examples of each)
- Log format: `[LEVEL] TIMESTAMP - message - context`
- Stdout (INFO+) vs. stderr (errors)
- 3 examples (one per language): Good logging vs. useless logging

Reference from specifications:

- Details.md: "Logging Example" code samples

**Verify**:

- Log levels are clear and used consistently
- Examples show realistic scenarios
- Timestamp and context are emphasized

### Step 6: Write Testing Section

Create "## Testing & Validation" section with:

- Unit testing: pytest (Python), Bash test framework, Jest (Node)
- Test naming: `test_<function>_<scenario>` format
- What to test: Happy path, error paths, edge cases
- Minimum coverage: 80% (your standard)
- 2 examples: Well-tested function vs. inadequately tested function

Reference from specifications:

- Details.md: "Testing & Validation"

**Verify**:

- Testing frameworks are standard for each language
- Test naming is consistent
- Coverage expectations are clear (80%)

### Step 7: Write Key Takeaways Section

Create "## Key Takeaways" section with:

- Summarize structure, error handling, logging, testing
- Reference to workflow file (branch/commit context)
- Reference to knowledge file (documenting what scripts do)

**Verify**:

- All 4 main topics (structure, errors, logging, testing) mentioned
- Cross-references to other files present

### Step 8: Final Review

**Content Accuracy**:

- [ ] Script patterns match your automation scripts (check `automation/` folder)
- [ ] Error handling approach matches your scripts
- [ ] Logging format is consistent with your actual logs
- [ ] Testing approach is practical for your team

**Code Examples**:

- [ ] All Python code is syntactically correct
- [ ] All Bash code is syntactically correct
- [ ] All Node code is syntactically correct
- [ ] Examples are realistic and useful

**Quality**:

- [ ] File is ~180 lines
- [ ] Markdown is valid
- [ ] All links work
- [ ] Clear hierarchy and readability

**File location**: `.github/instructions/automation-scripting-standards.instructions.md`

**Status**: ✅ Anchor 2 complete (ready to move to Anchor 3)

---

## Anchor 3: automation-knowledge-capture.instructions.md

**Duration**: Days 5-6
**Target**: 150 lines
**ApplyTo**: `**/*.md,docs/**`

### Step 1: Create File and Frontmatter

Create file: `.github/instructions/automation-knowledge-capture.instructions.md`

Add frontmatter:

```yaml
---
description: 'Standards for decision logging, ADRs, and knowledge documentation in automation engineering (Obsidian, PR decisions, architecture)'
applyTo: '**/*.md,docs/**'
---

# 📚 Automation Knowledge & Documentation Standards
```

**Verify**: File exists, YAML is valid

### Step 2: Write Core Principles Section

Based on specifications:

```markdown
## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dry-principle.md) -
  Document decisions once in Obsidian; link from code, PRs, and other docs many times
- [Design by Contract](../core/principles/design-by-contract.md) -
  Document preconditions (what must be true before), postconditions (what's true after), and invariants (what never changes)
```

**Verify**: 2 principles linked, relative paths correct

### Step 3: Write Decision Logging Section

Create "## Decision Logging Format" section with:

- Pattern: `DECISION: <title>` → Context → Options → Rationale → Impact
- When to log: Architecture decisions, automation approach choices, tradeoff decisions
- Where: Obsidian notes (link in PR descriptions)
- Metadata: Date, decision maker, status (Active/Revisited/Superseded)
- 1 good example (detailed context, options, rationale)
- 1 bad example (missing context or options)

Reference from specifications:

- Details.md: "Decision Template (Obsidian)"

**Verify**:

- Format is clear and specific
- Example shows realistic decision (could be from your actual decisions)
- Status tracking is explained

### Step 4: Write ADR Section

Create "## Architecture Decision Record (ADR)" section with:

- Status field: Proposed, Accepted, Deprecated, Superseded
- Sections: Context, Decision, Consequences, Alternatives Considered
- File naming: `YYYY-MM-DD-<kebab-case-title>.md`
- Superseding decisions: How to update old ADRs
- 1 example ADR (complete and realistic)

Reference from specifications:

- Details.md: "ADR Template"

**Verify**:

- ADR structure is industry-standard
- File naming is consistent with your conventions
- Example is realistic and complete

### Step 5: Write Linking Section

Create "## Cross-Linking & Knowledge Web" section with:

- Obsidian wiki-links: `[[decision-title]]` for internal navigation
- GitHub markdown links: `[text](../path/to/file.md)` for cross-repo
- Linking strategy: Link from decision → affected code, from PR → decision, from code → decision
- Knowledge reuse: Document once, link many times
- 1 example: Well-linked documentation vs. isolated silos

Reference from specifications:

- Details.md: "Cross-Linking & Knowledge Web"

**Verify**:

- Both linking formats explained (wiki-style for Obsidian, markdown for GitHub)
- Linking philosophy is clear (reuse, not duplication)
- Example shows practical benefit

### Step 6: Write PR Integration Section

Create "## PR Integration" section with:

- Every PR should have Decisions section
- Format: Link to Obsidian decision notes
- When to link: Any decision affecting architecture, framework, or major approach
- Updating decision status: Mark as "Revisited" if code changes scope

**Verify**:

- PR integration is practical
- Linking format is clear

### Step 7: Write Key Takeaways Section

Create "## Key Takeaways" section with:

- Summary bullets (decision logging, ADRs, linking, PR integration)
- Cross-references to workflow and scripting files

**Verify**:

- All 4 main topics covered
- Cross-references present

### Step 8: Final Review

**Content Accuracy**:

- [ ] Decision logging format matches your Obsidian practice (check your notes)
- [ ] ADR structure matches any existing ADRs
- [ ] Linking strategy is practical for your team
- [ ] PR integration makes sense for your workflow

**Examples**:

- [ ] Decision example is realistic and well-reasoned
- [ ] ADR example is complete and actionable
- [ ] Bad examples clearly show problems

**Quality**:

- [ ] File is ~150 lines
- [ ] Markdown is valid
- [ ] Links are correct
- [ ] Clear hierarchy

**File location**: `.github/instructions/automation-knowledge-capture.instructions.md`

**Status**: ✅ Anchor 3 complete (ready to move to Anchor 4)

---

## Anchor 4: automation-metrics-tracking.instructions.md

**Duration**: Day 7
**Target**: 100 lines
**ApplyTo**: `docs/**/*.json,**/*.yaml`

### Step 1: Create File and Frontmatter

Create file: `.github/instructions/automation-metrics-tracking.instructions.md`

Add frontmatter:

```yaml
---
description: 'Standards for metrics tracking, snapshot exports, and dashboard generation in automation engineering (cycle time, WIP, lead time)'
applyTo: 'docs/**/*.json,**/*.yaml'
---

# 📊 Automation Metrics & Tracking Standards
```

**Verify**: File exists, YAML is valid

### Step 2: Write Core Principles Section

```markdown
## Core Engineering Principles

This instruction set applies the following foundational principle:

- [Code Quality Goals](../core/principles/code-quality-goals.md) -
  Metrics provide visibility and enable data-driven optimization of your automation engineering workflow
```

**Verify**: 1-2 principles linked, relative paths correct

### Step 3: Write Snapshot Format Section

Create "## Snapshot Format & Schema" section with:

- Required fields: date, open_prs, in_progress, blocked, avg_cycle_time_days, stale_branches
- Optional fields: avg_lead_time_days, pr_review_latency_hours, blocker_count, wip_adherence_percent
- JSON schema definition
- Validation rules (type, range, format for each field)
- 1 example snapshot (realistic numbers from your workflow)
- Verification: How to validate snapshot against schema

Reference from specifications:

- Details.md: "Snapshot JSON Schema"

**Verify**:

- Schema matches your actual snapshot format (check `docs/` folder)
- Validation rules are precise
- Example looks realistic

### Step 4: Write Cycle Time & Lead Time Section

Create "## Cycle Time & Lead Time Definitions" section with:

- Lead time: Issue creation → merged
- Cycle time: First commit → merged
- WIP limit: Your threshold (from my-daily-needs.md)
- Blocked state: Definition and triggers
- Tracking approach: How to capture timestamps

Reference from specifications:

- Details.md: "Cycle Time & Lead Time Definitions"

**Verify**:

- Definitions are clear and distinct
- WIP limit matches your actual practice
- Tracking approach is feasible

### Step 5: Write Collection & Reporting Section

Create "## Metrics Collection & Reporting" section with:

- Daily snapshot generation (reference A6 automation)
- Tools: Jira API, GitHub PR API, git log
- Reporting cadence: Daily snapshot, weekly trend, monthly analysis
- Dashboard visualization: What metrics matter
- 1 example: Sample report interpretation

Reference from specifications:

- Details.md: "Metrics Collection & Reporting"

**Verify**:

- Collection approach is practical for your tools
- Reporting cadence is realistic
- Example report is useful

### Step 6: Write Key Takeaways Section

Create "## Key Takeaways" section with:

- Summary of snapshot format, definitions, collection
- Reference to workflow file

**Verify**:

- All main topics covered
- Cross-reference present

### Step 7: Final Review

**Content Accuracy**:

- [ ] JSON schema matches your actual snapshots (check `docs/metrics/`)
- [ ] Metric definitions align with your tracking goals
- [ ] Collection approach matches your tools (Jira, GitHub)
- [ ] Reporting cadence is realistic for your workflow

**Examples**:

- [ ] Example snapshot conforms to schema
- [ ] Numbers are realistic (not made up)

**Quality**:

- [ ] File is ~100 lines
- [ ] Markdown is valid
- [ ] JSON syntax is correct
- [ ] Clear and actionable

**File location**: `.github/instructions/automation-metrics-tracking.instructions.md`

**Status**: ✅ Anchor 4 complete (all 4 files done)

---

## Post-Implementation: Validation & Team Communication

### Validation Checklist

**All 4 Files**:

- [ ] Files exist in `.github/instructions/` folder
- [ ] YAML frontmatter is valid (no parse errors)
- [ ] Markdown syntax is correct
- [ ] All principle links work (relative paths valid)
- [ ] All cross-references between files work
- [ ] Total lines across all 4 files ≈ 630 (Anchor 1: 200, Anchor 2: 180, Anchor 3: 150, Anchor 4: 100)

**Content Accuracy**:

- [ ] Examples match your actual practices (branch names, commits, PRs, scripts, decisions, metrics)
- [ ] Terminology matches your Jira and GitHub workflows
- [ ] All references to A1-A10 automation backlog are accurate

**Copilot Integration**:

- [ ] Files follow your established 79-file pattern (YAML + Principles + Content)
- [ ] `applyTo` patterns are precise (not overly broad)
- [ ] Instructions are actionable (no vague guidance)

### Team Communication

**Option 1: Internal Validation First** (Recommended)

1. Review files yourself for accuracy against my-daily-needs.md
2. Test with Copilot (try generating a branch name, commit message, PR, script, decision)
3. Refine based on Copilot responses
4. Share with team after validation

**Option 2: Team-Driven Feedback**

1. Share files with team immediately
2. Ask: "Do these match our actual practices?"
3. Gather feedback on gaps or inaccuracies
4. Refine based on team input
5. Re-share refined version

### Next Steps (Phase 2)

After 4 instruction files are implemented and validated:

1. **Integrate with A1** (Branch naming hook): Reference `automation-workflow-conventions.instructions.md`
2. **Integrate with A2** (Standup generator): Reference `automation-workflow-conventions.instructions.md` and `automation-knowledge-capture.instructions.md`
3. **Use in PR reviews**: Reference `automation-workflow-conventions.instructions.md` when reviewing PRs
4. **Measure adoption**: Track how often Copilot is used for branch naming, commits, PRs

---

## Success Criteria (Completion)

Implementation is complete and successful when:

✅ All 4 instruction files created and committed to `.github/instructions/`
✅ All files follow established pattern (YAML + Principles + Content)
✅ All principle links are valid
✅ All examples are accurate and realistic
✅ Team understands file purpose and can reference them ("See automation-workflow-conventions.instructions.md")
✅ Copilot responses improve in relevance when files are active
✅ Files serve as documentation of your automation engineering standards

---

**Implementation ready**: 2025-01-30
**Estimated completion**: 2025-02-06 (7 days)
**Next review date**: 2025-02-10 (after team uses instructions)
