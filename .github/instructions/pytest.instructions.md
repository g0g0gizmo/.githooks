---
description: Pytest usage and best practices for this repository
applyTo: '**/tests/**'
---

# Pytest Instructions

This repository uses `pytest` for Python testing. Follow these guidelines for consistent, reliable, and maintainable tests across any project.

## Why This Style?

These instructions enforce direct, integration-style testing. This means:

- No mocks or monkeypatching: Tests interact with real code and data.
- Real side effects: If your code writes files or updates state, verify those effects directly.
- Minimal abstraction: Tests are easy to follow and debug.

## General Principles

- **No mocks or monkeypatching:** Avoid using `pytest`'s `monkeypatch` or any mocking libraries.
- **Direct functional/integration tests:** Prefer testing actual code paths and outputs, not simulated or stubbed behaviors.
- **Test real side effects:** If your code writes files, updates state, or interacts with the environment, verify those effects directly.
- **Use fixtures for setup/teardown:** Use pytest fixtures for setup and teardown, but keep them minimal and avoid patching.
- **Keep tests readable and maintainable:** Use clear function names, docstrings, and comments to explain intent.

## Test Structure

- Place all test files in the `tests/` directory, mirroring the source structure when possible.
- Name test files as `test_<module>.py` and test functions as `test_<functionality>()`.
- Group related tests in classes only if shared setup/teardown is required.

## Example Test Pattern

```python
# tests/test_example.py

def test_addition():
    assert 1 + 1 == 2
```

## Example Fixture and conftest.py

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4]
```

```python
# tests/test_with_fixture.py

def test_sum(sample_data):
    assert sum(sample_data) == 10
```

## Best Practices

- **Test actual code paths:** Always call real functions/classes, not stubs.
- **Avoid unnecessary abstraction:** Write tests that are easy to follow and debug.
- **Check for side effects:** If your code writes files, check file contents directly.
- **Use parametrization for variations:** Use `@pytest.mark.parametrize` for multiple input/output cases.
- **Fail fast:** Use simple assertions and let pytest handle failures.

## Running Tests

Run all tests:

```sh
pytest tests/ -v --tb=short --color=yes
```

Run with coverage:

```sh
pytest tests/ --cov=src --cov-report=term-missing
```

## What NOT to Do

- Do not use `mock`, `unittest.mock`, or `pytest`'s `monkeypatch`.
- Do not patch environment variables or functions.
- Do not simulate external dependencies; test with real data or skip if unavailable.

---
This file is auto-generated to match a direct, integration-style testing philosophy. For questions, see your project's README or ask the maintainers.
