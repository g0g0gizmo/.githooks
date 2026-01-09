---
name: python2-to-3-conversion
description: Migrate Python 2 code to Python 3 with f-strings, lazy logging, and Pyright/Pylance best practices.
argument-hint: ConversionScope=<files/dirs/modules>
agent: python2-to-3-conversion
tools:
  - search
  - fileSearch
  - textSearch
  - readFile
  - edit
  - terminal
  - problems
  - runCommands
  - getTerminalOutput
  - vscode
  - execute
  - read
  - edit
  - search
  - web
  - agent
  - github.vscode-pull-request-github/copilotCodingAgent
  - ms-python.python/getPythonEnvironmentInfo
  - ms-python.python/getPythonExecutableCommand
  - ms-python.python/installPythonPackage
  - ms-python.python/configurePythonEnvironment
  - todo
---

# Python 2 → 3 Conversion (Best Practices)

**Related Files:**

- Agent: `./agents/python2-to-3-conversion.agent.md`

Convert Python 2 code to idiomatic Python 3 while improving type safety and logging quality.

**Conversion Scope**: ${input:ConversionScope}

Focus conversion efforts on the specified scope (e.g., specific files, directories, modules, or code sections provided above).

### Scope Determination Strategy

- **Always use editor context**: Determine scope from the currently open file or user-specified path
- **Work iteratively**: Convert in isolated, testable chunks rather than attempting full codebase conversion
- **Prefer single-file conversions**: Start with one file, validate, then move to the next
- **Expand cautiously**: Only expand scope to related files when dependencies require it (e.g., shared utilities, type definitions)
- **Validate after each iteration**: Run smoke tests after each file/module conversion before proceeding

## Inputs To Confirm

- Target minimum Python version (default assumption: 3.8+ unless project says otherwise)
- Packaging/entry points (CLI, scripts, importable packages)
- Whether side effects on import exist (affects smoke test strategy)

## Conversion Goals

- Python 3 syntax and stdlib usage
- Use f-strings for *general string formatting* (user-facing text, exceptions, paths, etc.)
- Use **lazy logging** (defer formatting until log emission)
- Improve Pyright/Pylance signal-to-noise (types, nullability, imports)

## Workflow (Recommended)

**Important**: Work iteratively on isolated files or modules. Do not attempt to convert entire codebases in a single pass.

1. **Determine scope from context**
   - Use the currently open file in the editor as the primary conversion target
   - Only expand to related files if they are direct dependencies (imported by the target file)
   - Ask user for confirmation before expanding scope beyond the current file

2. **Baseline & safety net**
   - Run existing tests for the target file/module (if any)
   - Run a smoke compile pass on the target scope to catch syntax errors early (see "Smoke test" below)
   - Document current behavior before making changes

3. **Automated modernization pass (target file only)**
   - Prefer automated tools to remove mechanical work:
     - `2to3` (or `python -m lib2to3`) for broad Py2→Py3 syntax transforms
     - `pyupgrade` for modernizing syntax once on Py3
   - Apply tools to the target file only
   - Keep changes small and reviewable; avoid "format+refactor+behavior" in one pass

4. **Fix semantic differences (Py2→Py3)**
   - Text/bytes boundaries:
     - Ensure explicit encoding/decoding around file IO, sockets, subprocess, hashing.
     - Prefer `pathlib.Path` for filesystem paths.
   - Iterators/views:
     - `dict.keys()/items()/values()` are views; wrap with `list(...)` only when needed.
     - `range` is lazy; don’t assume list semantics.
   - Exceptions:
     - Use `except Exception as exc:`
     - Re-raise with `raise` (preserves traceback).

5. **String formatting rules (f-strings vs logging)**

   - Use **f-strings** for:
     - User-facing strings (errors, UI/CLI output)
     - Building values you will actually use immediately
     - Simple conversions where readability improves

   - Use **lazy logging** for:
     - `logger.debug/info/warning/error(...)` messages
     - Any logging in hot paths or loops

   Example:
   - ✅ Good (lazy): `logger.info("Loaded %s records from %s", count, path)`
   - ❌ Avoid (eager): `logger.info(f"Loaded {count} records from {path}")`

   Exception logging:
   - Prefer `logger.exception("Failed to ...")` inside `except` blocks.

6. **Pyright/Pylance best practices (practical)**

   - Add type hints for public APIs first (then internal helpers).
   - Prefer precise standard types:
     - `from collections.abc import Iterable, Mapping, Sequence`
     - `pathlib.Path` over `str` paths when possible
   - Avoid implicit `Any` in new/modified code.
   - Handle optional values explicitly:
     - `if value is None: ...` rather than relying on truthiness
   - Prefer explicit returns and narrow exception handling.

7. **Validate and iterate**
   - Run smoke test on converted file(s)
   - Fix any compilation errors
   - Run existing unit tests (if applicable)
   - Commit/checkpoint before moving to next file

8. **Formatting, linting, and consistency**

   - Run formatter/import organizer already used by the repo (e.g., Black + isort).
   - Keep logging and typing changes consistent across modules.

## Smoke test (REQUIRED)

Create a file named `test_smoke.py` that verifies *all Python modules compile under Python 3*.

- Prefer compilation (`compileall` / `py_compile`) over importing modules.
  - Importing can execute module-level side effects and may require runtime dependencies.

Suggested pytest-style implementation with subprocess validation:

```python
import compileall
import subprocess
import sys
from pathlib import Path


def test_smoke_compile_all_python_files() -> None:
    """Compile all Python files to detect syntax errors."""
    root = Path(__file__).resolve().parents[0]
    ok = compileall.compile_dir(str(root), quiet=1)
    assert ok, "One or more Python files failed to compile"


def test_smoke_run_compilation_check() -> None:
    """Run compilation check as subprocess to validate syntax errors in converted code."""
    root = Path(__file__).resolve().parents[0]
    result = subprocess.run(
        [sys.executable, "-m", "py_compile"] +
        [str(f) for f in root.rglob("*.py") if "__pycache__" not in str(f)],
        capture_output=True,
        text=True,
        timeout=30
    )
    if result.returncode != 0:
        raise AssertionError(
            f"Python syntax check failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
```

If the repo has non-source folders to exclude (e.g., `History/`, `node_modules/`), implement a file walker and call `py_compile.compile()` per file with exclusions.

## Validation execution (REQUIRED)

After completing conversions:

1. Run the smoke test to verify compilation:

   ```bash
   pytest test_smoke.py -v
   ```

   or directly:

   ```bash
   python test_smoke.py
   ```

2. Review any syntax errors reported and apply targeted fixes.

3. Repeat until all Python files compile without errors.

## Output

- A PR-ready set of changes that:
  - Runs on Python 3
  - Uses f-strings appropriately
  - Uses lazy logging consistently
  - Improves type-checking with Pyright/Pylance
  - Includes `test_smoke.py` compile check

## Agent Mode

For interactive conversion guidance, use the agent mode file:

- `./agents/python2-to-3-conversion.agent.md`


# Python 2 → 3 Migration Standards

**Related Files:**


- Conversion Prompt: `prompts/python2-to-3-conversion.prompt.md`
- Agent Mode: `prompts/python2-to-3-conversion.agent.chatmode.md`

These rules apply when converting Python 2 code to Python 3 and when touching converted files.

## Target

- Default target: Python 3.8+ unless the repository explicitly sets a different minimum.

## Scope

- **IronPython code is out of scope**: Do not attempt to convert IronPython 2.7 code (files that use `import wpf`, `import clr`, or `.NET` interop).
- Only convert standard Python 2 code to Python 3.

## Formatting & Modern Python

- Prefer f-strings for general formatting (exceptions, CLI output, user messages, debug-only strings you will actually use immediately).
- Prefer `pathlib.Path` for filesystem paths.
- Prefer `collections.abc` imports (e.g., `Iterable`, `Mapping`, `Sequence`).

## Logging (Lazy Logging Required)

Python’s logging supports lazy formatting; use it to avoid unnecessary string construction.

- ✅ Use lazy logging:
  - `logger.debug("User id=%s", user_id)`
  - `logger.info("Loaded %s records from %s", count, path)`
- ❌ Avoid eager formatting inside logging calls:
  - `logger.info(f"Loaded {count} records from {path}")`
  - `logger.info("Loaded {} records".format(count))`

Exceptions:

- Use `logger.exception("...")` inside `except` blocks to include traceback.

## Py2 → Py3 Semantic Fixes

- Text vs bytes:
  - Be explicit about encoding/decoding around IO and network boundaries.
  - Prefer opening text files with explicit `encoding=` when appropriate.
- Iteration changes:
  - `dict.items()/keys()/values()` are views; wrap with `list(...)` only when you truly need a list.
- Exceptions:
  - Use `except Exception as exc:` and re-raise with `raise` when preserving context.

## Type Checking (Pyright/Pylance)

- Add type hints for public functions and class APIs you modify.
- Avoid introducing new implicit `Any`.
- Handle `Optional[...]` explicitly (check for `None`);
  avoid relying on truthiness when it changes meaning.

## Smoke Test (REQUIRED)

Add a `test_smoke.py` file that ensures every Python module in the repository compiles under Python 3.

- Prefer compilation (`compileall`/`py_compile`) over importing modules to avoid import-time side effects.

Recommended pytest-style snippet:

```python
import compileall
from pathlib import Path


def test_smoke_compile_all_python_files() -> None:
    root = Path(__file__).resolve().parents[1]
    ok = compileall.compile_dir(str(root), quiet=1)
    assert ok, "One or more Python files failed to compile"
```

If your repo contains large non-source folders, implement exclusions (e.g., skip `History/`, `node_modules/`, virtualenvs).
