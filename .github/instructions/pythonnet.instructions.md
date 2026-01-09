---
description: 'Pythonnet wrapper development standards and best practices'
applyTo: '**/*wrapper*.py'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [Design by Contract](../core/principles/design-by-contract.md) — Establish clear preconditions, postconditions, and invariants for CLR interop
- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) — Create reusable type conversion utilities and wrapper patterns
- [Code Quality Goals](../core/principles/code-quality-goals.md) — Maintain readability, performance, and security across Python-NET boundaries

When implementing pythonnet wrappers, always reinforce these core principles through your design choices.

---

# Pythonnet Wrapper Development Standards

## 1. Installation & Setup Requirements

### Dependencies
```
pythonnet>=3.0.0
typing-extensions>=4.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

### Assembly References
- Document all required `.NET assemblies` in setup documentation
- Use `clr.AddReference()` for system assemblies in module-level code
- For custom DLLs, add to `sys.path` before reference
- Always catch `System.Runtime.InteropServices.DllNotFoundException` for missing assemblies

---

## 2. Wrapper Class Structure

### Naming Conventions
- Wrapper classes: Use `{OriginalName}Wrapper` or `{OriginalName}` if context is clear
- Methods: Convert `PascalCase` .NET methods to `snake_case` Python methods
- Properties: Use `@property` decorator for .NET properties
- Internal .NET object: Always store as `self._dotnet_obj`

### Mandatory Methods
Every wrapper class must implement:

```python
def __init__(self, *args, **kwargs):
    """Initialize wrapper with .NET object or create new instance."""

@classmethod
def from_dotnet_object(cls, dotnet_obj):
    """Create wrapper from existing .NET object."""

def __repr__(self):
    """Return string representation for debugging."""

def __enter__(self):
    """Support context manager protocol."""

def __exit__(self, exc_type, exc_val, exc_tb):
    """Clean up .NET resources (call Dispose if applicable)."""
```

### Documentation Requirements
- Include docstring for every public method
- Document parameter types (use type hints)
- Explain what .NET method is being called
- Note any type conversions happening
- Include `Raises:` section documenting exceptions

Example:
```python
def get_configuration(self, key: str) -> Any:
    """
    Retrieve configuration value from .NET ConfigurationManager.

    Converts System.String key to Python string and returns
    appropriately typed configuration value.

    Args:
        key: Configuration key (converted to System.String)

    Returns:
        Converted configuration value (type depends on key)

    Raises:
        ValueError: If key is invalid or not found
        RuntimeError: If .NET ConfigurationManager fails
    """
    if not isinstance(key, str):
        raise ValueError(f"Key must be str, got {type(key)}")
    try:
        result = self._dotnet_obj.GetConfiguration(key)
        return self._convert_from_dotnet(result)
    except DotNetException as e:
        raise RuntimeError(f"Configuration retrieval failed: {e.Message}")
```

---

## 3. Type Conversion Patterns

### Conversion Utilities (Required)
Create static methods for converting to/from .NET types:

```python
@staticmethod
def _convert_from_dotnet(value):
    """Convert .NET types to Python equivalents."""
    if value is None:
        return None
    # Handle specific .NET types:
    if isinstance(value, str):  # System.String
        return value
    if isinstance(value, int):  # System.Int32/Int64
        return value
    # TODO: Add more type conversions
    return value

@staticmethod
def _convert_to_dotnet(value):
    """Convert Python types to .NET equivalents."""
    if value is None:
        return None
    # Handle specific Python types:
    if isinstance(value, str):
        return value  # Automatically becomes System.String
    if isinstance(value, int):
        return value  # Automatically becomes System.Int32
    # TODO: Add more type conversions
    return value
```

### Supported Type Mappings

| .NET Type | Python Type | Conversion Required |
|-----------|------------|---------------------|
| `System.String` | `str` | No |
| `System.Int32` | `int` | No |
| `System.Int64` | `int` | No |
| `System.Double` | `float` | No |
| `System.Boolean` | `bool` | No |
| `System.DateTime` | `datetime.datetime` | Yes |
| `System.Guid` | `uuid.UUID` | Yes |
| `List<T>` | `list` | Yes |
| `Dictionary<K,V>` | `dict` | Yes |
| `Byte[]` | `bytes` | Yes |

### Collection Conversion Pattern
```python
from System.Collections.Generic import List

@staticmethod
def _list_to_dotnet(python_list: list, item_type) -> List:
    """Convert Python list to .NET List<T>."""
    dotnet_list = List[item_type]()
    for item in python_list:
        dotnet_list.Add(item)
    return dotnet_list

@staticmethod
def _list_from_dotnet(dotnet_list) -> list:
    """Convert .NET List<T> to Python list."""
    return [item for item in dotnet_list]
```

---

## 4. Exception Handling

### Exception Translation Pattern
Always wrap .NET exceptions in appropriate Python exceptions:

```python
from System import Exception as DotNetException
from System.ArgumentException import ArgumentException

def configure_settings(self, settings: dict):
    """Configure wrapper settings."""
    try:
        for key, value in settings.items():
            self._dotnet_obj.SetSetting(key, value)
    except ArgumentException as e:
        raise ValueError(f"Invalid setting: {e.Message}")
    except DotNetException as e:
        raise RuntimeError(f"Configuration failed: {e.Message}")
```

### Required Exception Handling
- **Never** let .NET exceptions escape the wrapper
- Always translate to Python exception types:
  - `ArgumentException` → `ValueError`
  - `NullReferenceException` → `AttributeError` or `ValueError`
  - `InvalidOperationException` → `RuntimeError`
  - `TimeoutException` → `TimeoutError`
  - Unexpected exceptions → `RuntimeError`

---

## 5. Resource Management

### IDisposable Pattern
When wrapping .NET classes implementing `IDisposable`:

```python
class ResourceWrapper:
    def __init__(self):
        try:
            self._dotnet_obj = DotNetResource()
        except Exception as e:
            raise RuntimeError(f"Failed to create resource: {e.Message}")
        self._disposed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()

    def dispose(self):
        """Explicitly dispose of .NET resources."""
        if not self._disposed:
            try:
                if hasattr(self._dotnet_obj, 'Dispose'):
                    self._dotnet_obj.Dispose()
            finally:
                self._disposed = True

    def __del__(self):
        """Ensure cleanup even if not explicitly disposed."""
        self.dispose()
```

### Usage Pattern (Context Manager)
```python
with ResourceWrapper() as resource:
    result = resource.do_work()
# Automatically disposed here
```

---

## 6. Testing Requirements

### Test File Naming
- `test_*_wrapper.py` for wrapper unit tests
- One test file per wrapper class minimum

### Test Coverage Requirements
- **Minimum 80%** code coverage for wrapper code
- **All public methods** must have corresponding tests
- **Exception paths** must be tested

### Test Structure
```python
import unittest
from mymodule import YourClassWrapper
from System import Exception as DotNetException

class TestYourClassWrapper(unittest.TestCase):
    def setUp(self):
        """Create wrapper instance for each test."""
        self.wrapper = YourClassWrapper()

    def tearDown(self):
        """Clean up resources."""
        if hasattr(self.wrapper, 'dispose'):
            self.wrapper.dispose()

    def test_initialization(self):
        """Test wrapper initializes correctly."""
        self.assertIsNotNone(self.wrapper._dotnet_obj)

    def test_method_call(self):
        """Test method returns expected type."""
        result = self.wrapper.your_method("test", 42)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, expected_type)

    def test_exception_handling(self):
        """Test that .NET exceptions are translated."""
        with self.assertRaises(ValueError):
            self.wrapper.your_method(None, -1)

    def test_context_manager(self):
        """Test context manager protocol."""
        with YourClassWrapper() as wrapper:
            result = wrapper.your_method()
        # Verify wrapper was properly disposed

    def test_property_access(self):
        """Test property getter/setter."""
        self.wrapper.your_property = "test"
        self.assertEqual(self.wrapper.your_property, "test")
```

### Pytest Configuration
In `conftest.py`:
```python
import pytest
import clr

@pytest.fixture(scope="session", autouse=True)
def load_assemblies():
    """Load required .NET assemblies once per test session."""
    clr.AddReference("System")
    clr.AddReference("YourAssembly")
```

---

## 7. Performance Guidelines

### Interop Call Optimization
- **Cache** frequently accessed .NET objects
- **Batch** multiple operations before returning to Python
- **Minimize** round-trip conversions for large collections
- **Profile** hot paths using `cProfile`

### Caching Pattern
```python
class CachedPropertyWrapper:
    def __init__(self):
        self._dotnet_obj = DotNetObject()
        self._cache = {}

    def get_expensive_property(self):
        """Get property with caching."""
        if 'expensive' not in self._cache:
            self._cache['expensive'] = self._dotnet_obj.ExpensiveProperty
        return self._cache['expensive']

    def invalidate_cache(self):
        """Clear cache when underlying object changes."""
        self._cache.clear()
```

---

## 8. Documentation Requirements

### Docstring Format (NumPy Style)
```python
def method_name(self, param1: str, param2: int) -> dict:
    """
    Brief one-line description.

    Longer description explaining what the method does,
    including reference to underlying .NET behavior.

    Parameters
    ----------
    param1 : str
        Description of parameter 1
    param2 : int
        Description of parameter 2

    Returns
    -------
    dict
        Description of return value structure

    Raises
    ------
    ValueError
        If param1 is empty
    RuntimeError
        If .NET method fails

    Notes
    -----
    Performance consideration: This method calls .NET code
    multiple times. Consider caching results.

    Examples
    --------
    >>> wrapper = MyWrapper()
    >>> result = wrapper.method_name("test", 42)
    """
```

### README Requirements
Create `README_WRAPPER.md` documenting:
1. Installation instructions
2. Quick start example
3. Complete API reference
4. Type conversion guide
5. Known limitations
6. Performance notes
7. Thread safety considerations

---

## 9. Type Hints (Mandatory)

All public methods must include complete type hints:

```python
from typing import List, Dict, Optional, Any, Union

def process_items(self, items: List[str]) -> Dict[str, int]:
    """Process items and return statistics."""
    ...

def optional_operation(self, value: Optional[str] = None) -> Union[int, None]:
    """Operation with optional parameter."""
    ...
```

---

## 10. Quality Checklist

Before submitting wrapper code:

- [ ] All classes implement `__init__`, `__repr__`, `__enter__`, `__exit__`
- [ ] All public methods have complete docstrings
- [ ] All parameters and returns have type hints
- [ ] Type conversion utilities `_convert_to_dotnet` and `_convert_from_dotnet` implemented
- [ ] All .NET exceptions translated to Python exceptions
- [ ] IDisposable pattern implemented (if applicable)
- [ ] Context manager pattern supported
- [ ] Unit tests cover all public methods (80%+ coverage)
- [ ] No .NET exceptions escape to caller
- [ ] Performance-critical code documented with complexity notes
- [ ] README.md includes usage examples and API reference
