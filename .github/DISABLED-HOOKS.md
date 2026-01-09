# Disabled Git Hooks

This directory contains hooks that have been disabled for performance or compatibility reasons.

## Performance Optimization (2025-12-11)

These hooks were disabled to improve commit performance from **1.05s to 0.52s** (50% faster).

### Disabled Hooks

#### `format-code.hook.disabled`

- **Original:** `pre-commit/format-code.hook`
- **Purpose:** Runs Maven (`mvn fmt:format`) to format Java code
- **Why Disabled:**
  - No Java code in this repository
  - Maven JVM startup overhead (~2-5 seconds)
  - Formats entire codebase instead of staged files only
- **Alternative:** Add Java formatting to CI/CD pipeline if Java code is added
- **Re-enable:** `mv format-code.hook.disabled format-code.hook`

#### `spell-check-md-files.hook.disabled`

- **Original:** `pre-commit/spell-check-md-files.hook`
- **Purpose:** Spell-checks markdown files using `aspell`
- **Why Disabled:**
  - Searches hardcoded "content" directory that doesn't exist
  - Causes errors and delays (100-500ms)
  - `find` command overhead on large directory trees
- **Alternative:** Use VS Code spell-checker or CI/CD markdown linter
- **Fix Before Re-enabling:** Change hardcoded directory to `git diff --cached --name-only '*.md'`
- **Re-enable:** Fix directory path, then `mv spell-check-md-files.hook.disabled spell-check-md-files.hook`

#### `autoversion-conventional-commit.hook.disabled`

- **Original:** `post-commit/autoversion-conventional-commit.hook`
- **Purpose:** Runs `npx standard-version` to auto-bump version on conventional commits
- **Why Disabled:**
  - npm/npx startup overhead (~300-1000ms) on every commit
  - Version bumping should be manual or part of release workflow
  - Runs on every commit, not just release commits
- **Alternative:** Manual versioning or GitHub Actions workflow on release branches
- **Re-enable:** `mv autoversion-conventional-commit.hook.disabled autoversion-conventional-commit.hook`

## Performance Baseline

### Before Optimization

```
Total hooks: 9
Total time: 1054.26ms (1.05s)
Status: ✓ ACCEPTABLE
```

### After Optimization

```
Total hooks: 6
Total time: 519.39ms (0.52s)
Status: ✓ FAST
Improvement: 50.7% faster (534ms saved)
```

## Re-enabling Hooks

To re-enable a hook:

```powershell
# Remove .disabled extension
mv <hook-name>.hook.disabled <hook-name>.hook

# Example:
mv pre-commit/format-code.hook.disabled pre-commit/format-code.hook
```

To disable a hook:

```powershell
# Add .disabled extension
mv <hook-name>.hook <hook-name>.hook.disabled

# Example:
mv pre-commit/search-term.hook pre-commit/search-term.hook.disabled
```

## Profiling Performance

Run the profiler to measure current hook performance:

```powershell
python tools/profile-hooks.py
```

Target performance: **< 1 second for typical commit workflow**

## See Also

- `.github/plans/FASTER.IMPLEMENTATION.md` - Full optimization plan and analysis
- `tools/profile-hooks.py` - Performance profiling tool
- `.github/performance-baseline-*.txt` - Historical performance measurements
