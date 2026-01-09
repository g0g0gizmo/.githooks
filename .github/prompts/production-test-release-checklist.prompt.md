---
description: 'Prompt: Enforce Production Test Software Release Checklist readiness and gating'
mode: 'agent'
tools:
  - run_in_terminal
  - get_terminal_output
  - todos
  - manage_todo_list
  - file_search
  - read_file
---

# Production Test Release Readiness

Drive an end‑to‑end gated release readiness assessment using the authoritative checklist in `instructions/production-test-sw-release-checklist.instructions.md`.


## Mission

Assess and enforce production test software release readiness. Provide explicit status for every category; block sign‑off until all MUST items are satisfied or explicitly waived with rationale.

## Trigger Detection

If user input contains any release keywords (release, tag, GA, prod test, RTM, handoff, cut build, deployment readiness): start the workflow automatically. Otherwise wait for explicit invocation.

## Workflow Overview

1. Collect Context Inputs
2. Enumerate Categories & MUST Items
3. Gather Evidence Commands / Artifacts
4. Compute Status Matrix
5. Surface Risks & Missing Data
6. Assist Remediation (generate commands/templates)
7. Confirm Waivers (if requested)
8. Final Readiness Summary (only when zero unaddressed MUST)

## Step 1: Collect Context Inputs

Prompt the user (batch single message) for any missing:

- [ ] Target version (semantic X.Y.Z)
- [ ] Intended tag name (default `vX.Y.Z`)
- [ ] Changelog path (default `CHANGELOG.md` or auto-create if absent)
- [ ] CI status reference (link or pipeline id)
- [ ] Test coverage threshold / actual
- [ ] Artifact type(s): Python package, Node package, Docker image, other
- [ ] Database migration scripts location
- [ ] SBOM requirement (yes/no)
- [ ] Performance baseline location
Store answers in a transient in‑memory structure.

## Step 2: Enumerate Categories

Use the eleven categories from the instructions file. For each produce an entry:
`Category: <name> | MUST: [list] | SHOULD: [list]`

## Step 3: Evidence Gathering

Offer or execute (if user consents) commands:

```bash
# Quality & static analysis
pytest -v --maxfail=1
pytest -v --cov=src --cov-report=term-missing  # if coverage needed
mypy src/
flake8 .
pip-audit --strict
npm audit --production  # if Node component
sonar-scanner -Dsonar.projectVersion=X.Y.Z

# Build / artifact
python -m build
npm run build
docker build -t org/app:vX.Y.Z .

# SBOM examples
cyclonedx-py -o sbom-python.json
cyclonedx-npm -o sbom-node.json
```

Do NOT assume success—capture output and mark evidence.

## Step 4: Status Matrix

Create a table with columns:
`Item | Category | Status | Evidence | Notes`
Status values: `[OK]`, `[MISSING]`, `[RISK]`, `[WAIVED]`.
Use `[MISSING]` if no evidence or user confirmation; `[RISK]` if partial / failing metrics; `[WAIVED]` only after explicit user waiver of a MUST with rationale.

## Step 5: Risks & Missing Data

List every `[MISSING]` or `[RISK]` item under headers:

- [ ] Missing Evidence
- [ ] Active Risks
Provide concise remediation suggestions (command, file to edit, test to add).

## Step 6: Remediation Assistance

Auto‑generate where requested:

- [ ] Changelog template (inject section if absent)
- [ ] Migration verification script skeleton (forward + rollback test)
- [ ] Coverage delta summary placeholder
- [ ] Risk matrix table (if >3 risks) using provided format
- [ ] Canary rollout plan draft for blue/green or canary strategy

## Step 7: Waiver Handling

If user insists on skipping a MUST:

1. Warn about consequence.
2. Require explicit waiver text: `WAIVE <item> BECAUSE <reason>`.
3. Mark status `[WAIVED]` and keep in final summary.
Never auto‑waive.

## Step 8: Final Readiness Summary

Only emit when no `[MISSING]` and no un-waived MUST items.
Format:

```
Release Readiness: APPROVED
Version: vX.Y.Z
MUST Items: 100% satisfied (waived: N)
Risks: <none|list>
Next Actions: tag + deploy commands
```

If not ready, output:

```
Release Readiness: BLOCKED
Unmet MUST:
- <item> (reason)
Remediation Suggestions Provided Above.
```

## MUST Items (Authoritative)

- [ ] Semantic version bump committed.
- [ ] Changelog updated with date, version, highlights, breaking changes.
- [ ] Tests all pass; coverage threshold met (if defined).
- [ ] No critical security vulnerabilities outstanding.
- [ ] Rollback plan documented with tag + DB backup reference.
- [ ] Artifact built, integrity (checksum/signature) verified.
- [ ] Database migrations forward & rollback tested.
- [ ] Git tag prepared (not yet pushed if blocking items remain).

## Output Requirements

- [ ] Always first produce or update Status Matrix before declaring readiness.
- [ ] Never claim readiness with any `[MISSING]` or `[RISK]` in MUST items.
- [ ] Keep answers concise: bullet lists, tables, fenced commands.
- [ ] Avoid reprinting unchanged large sections; show deltas on iterative passes.

## User Interaction Guardrails

- [ ] If user asks for sign-off prematurely: return BLOCKED summary.
- [ ] If user omits critical inputs: prompt again before proceeding.
- [ ] If evidence commands fail: mark `[RISK]` and capture stderr snippet.

## Anti-Patterns (Reject & Correct)

- [ ] Tag pushed before checklist completion.
- [ ] Skipping security / dependency scan citing time pressure.
- [ ] Ignoring failing migration test.
- [ ] Mixing unrelated changes into version bump commit.

## Example Session Outline

```
User: prepare release 2.4.1
Agent: Collect missing inputs → run quality commands → build matrix → remediation suggestions → final readiness (blocked or approved).
```

## Final Instruction

Run this workflow now upon invocation context; otherwise wait for trigger keywords.

## Checklist Report (Mandatory Output)

Always emit a structured checklist report regardless of readiness outcome. Use these sections and items verbatim, marking each line with one of `[OK]`, `[MISSING]`, `[RISK]`, `[WAIVED]` and include brief evidence or note per item.

### All Releases

- [ ] Build has a unique build ID for traceability (goes along with Semantic Versioning)
- [ ] Revision of software used to create the build is tagged in GitHub/Perforce
- [ ] Binaries are stored and distributed from an archived location (ex. GitHub Release Page, Artifactory, etc)

### Final Release Pre-Deployment (where applicable)

- [ ] No alpha version dependencies shall be referenced.
- [ ] If the Build version is managed manually, ensure it is updated in any/all applicable locations
- [ ] No defaults shall exist in `Configuration\\DUT\\ScanConfig.ini`
  - [ ] Exceptions allowed only if acknowledged and agreed upon by the technical lead.
- [ ] Limit files shall be used (`Configuration\\ModelConfig.ini` → `Use_Sequence_Limits = False`).
- [ ] All limit files checked with TLPM
- [ ] VPNs shall be populated in `config.json`.
- [ ] TestStand Analyzer shall be run and all errors addressed.
- [ ] Model Config Classification shall be set to Conformity.
  - [ ] Anything other than Development may be OK.
- [ ] DUT and Sequence file protection projects shall be updated to include all files that should not be edited once installed.
- [ ] All available file protection manifests (fpman) shall be verified using the auditor tool.
- [ ] Installer shall be verified on vanilla CTA (ideally run a golden DUT on this vanilla setup).
- [ ] Deployment Guide (Setup and Config Document) shall be created.
- [ ] All station hardware shall be added to preflight checks.
- [ ] All keys in the `Operator_UI.ini` shall be configured appropriately
  - [ ] Tree Items visibility
  - [ ] `Window.Title` string (standard: `PLN_COP_NOP_MOT - v<Version>`)
  - [ ] CUI Configuration
- [ ] STE and DUT limit files shall exist for all intended test configurations.
- [ ] No DUT SW shall be bundled with our SW (CMMC paved road will address this)
- [ ] If DUT SW is utilized, ensure Test SW has been tested using the specified version (prefer the latest released in Agile), not a development version
- [ ] Update README in repo root directory.
- [ ] README contains the most up-to-date VSAT Map file.
- [ ] Check all documents for accurate reference tables (e.g., user manual references PTP part number/rev; update after PTP REV changes)
- [ ] Validate a TDR generated by the SW using the Online TDR Validator

### Final Release Post-Deployment (where applicable)

- [ ] An entry was made in Add/Remove Programs for each software component installed (Test SW Installer, Limit Files Installer, etc) with correct version
- [ ] Entries have been made in All Programs and a shortcut placed on the Desktop as appropriate (`<Users>\\Public\\Desktop` preferred)
- [ ] If Limits were changed due to an update, verify that Limits were updated after installation
- [ ] All available file protection manifests (fpman) verified using the auditor tool
- [ ] No errors when opening and closing the Test Application Operator Interface
- [ ] No errors when executing a full test run using a Golden Unit or known-provenance DUT
- [ ] Memory usage is as expected during multiple back-to-back full test runs
- [ ] Correct artifacts created for each test run (at minimum, a TDR)
- [ ] Test artifacts created in the standard directory structure; all expected artifacts present
- [ ] TDR contents are as expected
- [ ] TDRs checked with TDR Validator and SPID Decoder
  - [ ] SPID contains the various flags that are set (Debug, RMA, Golden, etc)
- [ ] All log files created with expected contents and transferred to LOG folder for the test run
- [ ] If necessary, check appropriate DUT SW is present in the proper STE location
  - [ ] If DUT SW should work with latest version, ensure the version present matches latest released in Agile
- [ ] Uninstalling the SW removes all files that were installed

### Checklist Report Output Format

```text
Checklist Report

All Releases
- [OK] Build has a unique build ID – evidence: <id/command/output>
- [MISSING] Revision tagged – note: <branch/tag pending>
...

Final Release Pre-Deployment
- [OK] No alpha dependencies – evidence: <lockfile scan>
...

Final Release Post-Deployment
- [RISK] Memory usage stable – evidence: <metrics>
...
```

Do not omit this report. If an item is not applicable, mark `[WAIVED]` and provide rationale.
