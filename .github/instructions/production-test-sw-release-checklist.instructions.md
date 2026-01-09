---
description: Production Test Software Release Checklist – Copilot enforcement & guidance for preparing,
applyTo: '**'
---

# Production Test SW Release Checklist Instructions

Purpose: Guide GitHub Copilot to proactively enforce the Production Test Software Release Checklist during planning, coding, validation, and deployment steps. When the user indicates a release is being prepared (keywords: "release", "tag", "prod test", "handoff", "GA", "cut a build"), Copilot MUST surface this checklist, identify gaps, and assist in remedying them.

## Scope & Triggers

- Trigger phrases: release, RTM, GA, production test, handoff, deployment readiness, cut tag, ship build
- Applies to: version bumps, changelog edits, CI/CD adjustments, test stabilization, artifact promotion, rollback preparation
- Non-trigger context: If not in a release context, do not inject checklist unless user explicitly requests it.

## Release Readiness Categories

Copilot must structure guidance under these categories and confirm each is satisfied or call out deficiencies.

1. Planning & Governance
2. Versioning & Tagging
3. Code Quality & Static Analysis
4. Security & Compliance
5. Test Validation (Unit / Integration / System / Regression)
6. Performance & Resource Verification
7. Documentation & Change Communication
8. Packaging & Artifact Integrity
9. Environment & Configuration Readiness
10. Deployment & Rollback Strategy
11. Post-Release Monitoring Plan

## Detailed Checklist

### 1. Planning & Governance

- Release scope finalized & frozen (no unapproved feature creep)
- JIRA / issue tracker: all tickets in release milestone are Closed or explicitly deferred
- Stakeholder sign-off captured (product / QA / operations)
- Risk assessment logged with mitigation steps
- Release window scheduled & communicated

### 2. Versioning & Tagging

- Semantic version increment correct (MAJOR / MINOR / PATCH rationale documented)
- Version constant updated (e.g. `pyproject.toml`, `package.json`, assembly info, Docker labels)
- Pre-release identifiers removed (e.g. -rc, -beta) for GA
- Git tag naming convention validated (`vX.Y.Z`)
- Changelog entry added with date, version, concise highlights, breaking changes flagged

### 3. Code Quality & Static Analysis

- Linting passes (ESLint / Flake8 / Pylint / style tools)
- Formatting tasks completed (Black, Prettier, isort)
- Type checks clean (MyPy / tsc no errors)
- SonarQube / CodeQL / SAST: no new critical or blocker issues
- Cyclomatic complexity hotspots reviewed or ticketed
- No TODO / FIXME / HACK left untriaged

### 4. Security & Compliance

- Dependency scan (e.g. `npm audit`, `pip-audit`, SCA) – no HIGH/CRITICAL vulns unaddressed
- Secrets not embedded in code / configs (verified via scanning)
- TLS / cert renewals within validity window
- Authentication / authorization changes documented & tested
- Security-related configuration diffs reviewed (headers, CSP, CORS)

### 5. Test Validation

- Unit test coverage meets threshold (report attached)
- Integration tests pass in clean environment
- Regression suite green (no flaky tests ignored without justification)
- New features include test cases linked to requirements
- Manual exploratory QA sign-off (if applicable)

### 6. Performance & Resource Verification

- Baseline performance benchmarks unchanged or improved
- Load / stress test executed for critical paths (results archived)
- Memory / CPU / latency budgets respected
- No new resource leaks (profiling or tooling confirmation)

### 7. Documentation & Change Communication

- README / install / upgrade / ops runbooks updated
- Breaking change migration steps documented
- Feature flags & default states described
- API changes: added, deprecated, removed endpoints listed
- Internal release note prepared (high-level summary + risk notes)

### 8. Packaging & Artifact Integrity

- Build reproducible (clean environment rebuild matches checksum/signature)
- Artifact signed (if applicable) & signature validated
- SBOM generated & stored
- Docker image scanned (no critical CVEs) & tagged immutably
- Asset version embedded (e.g. `--version` returns correct value)

### 9. Environment & Configuration Readiness

- Config diffs between staging and production reviewed
- Feature flags & toggles staged correctly for release state
- Secrets / keys / credentials validated & rotated if scheduled
- Database migrations: forward + rollback tested, idempotency confirmed
- External dependencies (APIs, queues, storage) healthy & quota within limits

### 10. Deployment & Rollback Strategy

- Deployment method chosen (rolling, blue/green, canary) with rationale
- Rollback procedure documented (commands, conditions, data impact)
- Monitoring hooks integrated (metrics / logs / traces ready pre-switch)
- Automatic health checks & gating validated
- DR / failover scenarios unchanged or updated documentation

### 11. Post-Release Monitoring Plan

- Alert thresholds reviewed (no noisy or missing critical alerts)
- Dashboard updated with new KPIs
- Log retention & indexing stable
- Post-release validation script prepared (sanity checks)
- 24–48h hypercare assignment & escalation contacts listed

## Copilot Interaction Rules

When release context detected:

1. Summarize current known checklist state: Mark unknowns explicitly.
2. Ask user for missing critical inputs (e.g., target version, tag name, migration scripts).
3. Offer to auto-generate: changelog template, migration verification snippet, SBOM command, performance test harness stub.
4. Refuse to declare readiness until all MUST criteria validated or explicitly waived.
5. Provide risk callouts for skipped items.

## MUST vs SHOULD Classification

- MUST: Version bump, changelog, passing tests, no critical security issues, rollback plan, artifact integrity, tag creation, migration test.
- SHOULD: Performance benchmarking delta, documentation polish, SBOM export, load test, dashboard updates.
- If any MUST missing: Copilot must guide remediation before sign-off.

## Changelog Template (Inject If Missing)

```
## [vX.Y.Z] - YYYY-MM-DD
### Added
-
### Changed
-
### Fixed
-
### Deprecated
-
### Removed
-
### Security
-
### Migration Notes
-
```

## Release Command Patterns (Examples)

```bash
# Git tag
git tag -a vX.Y.Z -m "Release vX.Y.Z" && git push origin vX.Y.Z

# Python build
python -m build && twine upload dist/*

# Node build & publish
npm version X.Y.Z --no-git-tag-version
npm run build
npm publish --tag latest

# Docker image
docker build -t org/app:vX.Y.Z .
docker push org/app:vX.Y.Z

# SBOM (CycloneDX examples)
cyclonedx-py -o sbom-python.json
cyclonedx-npm -o sbom-node.json
```

## Validation Commands (Examples)

```bash
pytest -v --maxfail=1
npm test --silent
sonar-scanner -Dsonar.projectVersion=X.Y.Z
npm audit --production
pip-audit --strict
mypy src/
ts-node scripts/smoke-check.ts
```

## Copilot Auto-Assist Generation Opportunities

- Generate migration dry-run script with rollback verification.
- Produce coverage delta report summary.
- Create risk matrix table if more than 3 high-risk changes detected.
- Suggest canary route rules (Ingress / Load Balancer) if user mentions gradual traffic.

## Risk Matrix Template

| Area                | Risk               | Impact | Likelihood | Mitigation                        |
| ------------------- | ------------------ | ------ | ---------- | --------------------------------- |
| DB Migration        | Data inconsistency | High   | Medium     | Pre-production rehearsal + backup |
| New Auth Flow       | Login failures     | High   | Low        | Canary + enhanced logging         |
| Cache Config Change | Latency spike      | Medium | Medium     | Gradual TTL adjustment            |

## Rollback Essentials (Copilot Must Confirm)

- Last stable tag
- DB backup timestamp
- Config snapshot reference
- Clear reversal commands
- Alert quieting plan during rollback

## Copilot Enforcement Responses

- If user tries to skip a MUST: Respond with required justification request and consequences summary.
- If user requests release sign-off prematurely: Provide list of unmet MUST items.
- If all MUST satisfied: Provide concise readiness summary + optional SHOULD improvements.

## Anti-Patterns to Block

- Tagging before changelog update
- Publishing artifact with pre-release suffix for GA
- Ignoring failing but "non-critical" migration test
- Skipping security scan due to time pressure
- Unverified manual hotfix added post-freeze

## Output Style

- Concise bullet summaries
- Explicit statuses: [OK] / [MISSING] / [RISK] / [WAIVED]
- Never claim release ready without validation evidence

## Maintenance

- Review this instruction file quarterly or upon process changes
- Update command examples as tooling versions evolve
- Add new MUST items if mandated by governance

## References

- Internal Release Policy (link redacted)
- GitHub Copilot Custom Instructions: https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- OWASP Secure Deployment Principles

---
Copilot should treat this checklist as authoritative during release conversations and escalate missing MUST items before approval.
