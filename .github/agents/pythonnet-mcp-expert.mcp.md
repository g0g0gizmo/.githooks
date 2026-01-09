# Pythonnet Wrapper Generator MCP Server Specification

## Overview

The **Pythonnet Wrapper Generator MCP Server** is a specialized Model Context Protocol server designed to automate and assist in creating Python wrappers for .NET libraries using pythonnet (Python.NET) CLR interoperability.

**Status**: Specification
**Version**: 1.0
**Type**: stdio
**Language**: Python 3.10+
**Dependencies**: pythonnet 3.0+, clr, System libraries

---

## Core Purpose

This MCP server bridges the gap between Python and .NET ecosystems by:

1. **Analyzing .NET Assemblies** — Reflect on .NET DLLs to extract type information
2. **Generating Wrapper Stubs** — Automatically create Python wrapper class templates
3. **Type Mapping** — Generate type conversion utilities for Python ↔ .NET boundaries
4. **Test Generation** — Create unit test templates for wrapper functionality
5. **Documentation** — Generate docstrings and API reference documentation
6. **Validation** — Verify wrapper correctness and identify issues

---

## Implementation Architecture

### Server Component Structure

```
pythonnet-wrapper-generator-mcp/
├── server.py                    # MCP server main entry point
├── tools/
│   ├── assembly_analyzer.py     # CLR reflection and analysis
│   ├── wrapper_generator.py     # Code generation utilities
│   ├── type_converter.py        # Type mapping and conversion
│   ├── test_generator.py        # Unit test template generation
│   ├── documentation.py         # Docstring and docs generation
│   └── validator.py             # Wrapper validation and linting
├── templates/
│   ├── wrapper_class.jinja2     # Base wrapper template
│   ├── type_converter.jinja2    # Type conversion utilities
│   ├── test_template.jinja2     # Unit test template
│   ├── readme.jinja.2           # Documentation template
│   └── docstring.jinja2         # Docstring template
├── models/
│   ├── dotnet_type.py           # .NET type representation
│   ├── method_signature.py      # Method metadata
│   └── conversion_rule.py       # Type conversion rules
└── requirements.txt             # MCP server dependencies
```

---

## Available Tools

### 1. `analyze_assembly`

**Purpose**: Extract type information from .NET assemblies via CLR reflection

**Input Parameters**:

```json
{
  "assembly_path": "/path/to/Assembly.dll",
  "assembly_name": "YourNamespace.YourAssembly",
  "public_only": true,
  "include_events": true,
  "include_properties": true
}
```

**Output**:

```json
{
  "assembly_name": "YourNamespace.YourAssembly",
  "namespaces": [
    {
      "name": "YourNamespace",
      "types": [
        {
          "name": "YourClass",
          "kind": "class",
          "base_types": ["IDisposable"],
          "methods": [
            {
              "name": "DoWork",
              "parameters": [
                {"name": "param1", "type": "System.String"}
              ],
              "return_type": "System.Int32",
              "is_async": false
            }
          ],
          "properties": [
            {
              "name": "Configuration",
              "type": "System.Object",
              "can_read": true,
              "can_write": true
            }
          ],
          "events": [
            {
              "name": "OnComplete",
              "delegate_type": "EventHandler"
            }
          ]
        }
      ]
    }
  ],
  "dependencies": ["System", "System.Collections"]
}
```

**Use Cases**:

- Understand the structure of a .NET library before creating wrappers
- Identify all public API surface
- Determine type conversion requirements

---

### 2. `generate_wrapper_class`

**Purpose**: Generate Python wrapper class for a .NET class

**Input Parameters**:

```json
{
  "assembly_path": "/path/to/Assembly.dll",
  "namespace": "YourNamespace",
  "class_name": "YourClass",
  "pythonic_naming": true,
  "include_docstrings": true,
  "include_type_hints": true,
  "implement_context_manager": true
}
```

**Output**:

```python
"""
Python wrapper for YourNamespace.YourClass
Provides Pythonic interface to .NET functionality via pythonnet CLR
"""

import clr
from typing import Optional, Any
from System import Exception as DotNetException

clr.AddReference("YourAssembly")
from YourNamespace import YourClass as DotNetYourClass


class YourClassWrapper:
    """
    Python wrapper for YourNamespace.YourClass.

    This wrapper provides a Pythonic interface to the .NET class,
    handling type conversions and exception handling automatically.
    """

    def __init__(self):
        """Initialize wrapper with .NET object."""
        try:
            self._dotnet_obj = DotNetYourClass()
        except DotNetException as e:
            raise RuntimeError(f"Failed to create .NET object: {e.Message}")

    # ... generated methods, properties, and helpers
```

**Use Cases**:

- Quickly scaffold wrapper classes for .NET types
- Ensure consistent wrapper structure across multiple classes
- Generate boilerplate code

---

### 3. `generate_type_converters`

**Purpose**: Create type conversion utilities for Python ↔ .NET boundaries

**Input Parameters**:

```json
{
  "assembly_path": "/path/to/Assembly.dll",
  "types_to_convert": [
    "System.DateTime",
    "System.Collections.Generic.List<System.String>",
    "CustomNamespace.CustomType"
  ],
  "conversion_direction": "both"
}
```

**Output**:

```python
from typing import List, Dict, Any
from System import DateTime
from System.Collections.Generic import List as DotNetList
from datetime import datetime as py_datetime

class TypeConverters:
    """Utilities for converting between Python and .NET types."""

    @staticmethod
    def datetime_to_python(dotnet_datetime: DateTime) -> py_datetime:
        """Convert System.DateTime to Python datetime."""
        return py_datetime(
            dotnet_datetime.Year,
            dotnet_datetime.Month,
            dotnet_datetime.Day,
            dotnet_datetime.Hour,
            dotnet_datetime.Minute,
            dotnet_datetime.Second,
            dotnet_datetime.Millisecond * 1000
        )

    @staticmethod
    def datetime_from_python(py_dt: py_datetime) -> DateTime:
        """Convert Python datetime to System.DateTime."""
        return DateTime(
            py_dt.year, py_dt.month, py_dt.day,
            py_dt.hour, py_dt.minute, py_dt.second,
            py_dt.microsecond // 1000
        )

    @staticmethod
    def list_to_dotnet(python_list: list, item_type) -> DotNetList:
        """Convert Python list to .NET List<T>."""
        dotnet_list = DotNetList[item_type]()
        for item in python_list:
            dotnet_list.Add(item)
        return dotnet_list

    # ... additional conversion methods
```

**Use Cases**:

- Automate generation of type conversion utilities
- Ensure type safety at Python-NET boundaries
- Support complex generic types

---

### 4. `generate_tests`

**Purpose**: Create unit test templates for wrapper classes

**Input Parameters**:

```json
{
  "wrapper_class_name": "YourClassWrapper",
  "assembly_path": "/path/to/Assembly.dll",
  "namespace": "YourNamespace",
  "class_name": "YourClass",
  "test_framework": "pytest",
  "include_mock_patterns": true
}
```

**Output**:

```python
import unittest
import pytest
from your_module import YourClassWrapper
from System import Exception as DotNetException


class TestYourClassWrapper:
    """Test suite for YourClassWrapper."""

    @pytest.fixture
    def wrapper(self):
        """Create wrapper instance for each test."""
        w = YourClassWrapper()
        yield w
        if hasattr(w, 'dispose'):
            w.dispose()

    def test_initialization(self, wrapper):
        """Test wrapper initializes correctly."""
        assert wrapper is not None
        assert hasattr(wrapper, '_dotnet_obj')

    def test_do_work_method(self, wrapper):
        """Test DoWork method with valid input."""
        result = wrapper.do_work("test")
        assert result is not None

    def test_do_work_with_invalid_input(self, wrapper):
        """Test DoWork raises ValueError with invalid input."""
        with pytest.raises(ValueError):
            wrapper.do_work(None)

    def test_context_manager(self):
        """Test wrapper can be used as context manager."""
        with YourClassWrapper() as wrapper:
            result = wrapper.do_work()
        # Verify resources were cleaned up

    # ... additional test methods
```

**Use Cases**:

- Create comprehensive test suites faster
- Ensure wrapper testing follows pytest best practices
- Generate tests for newly created wrappers

---

### 5. `generate_documentation`

**Purpose**: Create documentation and API reference for wrappers

**Input Parameters**:

```json
{
  "wrapper_class": "YourClassWrapper",
  "assembly_path": "/path/to/Assembly.dll",
  "doc_format": "sphinx",
  "include_examples": true,
  "include_performance_notes": true
}
```

**Output**:

```markdown
# YourClassWrapper

## Overview

Python wrapper for `YourNamespace.YourClass` using pythonnet CLR interop.
This wrapper provides a Pythonic interface to .NET functionality.

## Installation

```bash
pip install pythonnet
```

## Quick Start

```python
from your_module import YourClassWrapper

# Create wrapper instance
wrapper = YourClassWrapper()

# Call wrapped method
result = wrapper.do_work("test")
```

## API Reference

### `YourClassWrapper`

#### Methods

##### `do_work(param: str) -> Any`

Perform work operation via .NET DoWork method.

**Parameters:**

- `param` (str): Input parameter for work operation

**Returns:**

- Converted result from .NET method

**Raises:**

- `ValueError`: If param is invalid
- `RuntimeError`: If .NET method fails

**Example:**

```python
result = wrapper.do_work("test")
```

## Type Conversions

The wrapper automatically converts between Python and .NET types:

| Python Type | .NET Type                                  |
| ----------- | ------------------------------------------ |
| str         | System.String                              |
| int         | System.Int32                               |
| float       | System.Double                              |
| dict        | System.Collections.Generic.Dictionary<K,V> |

## Performance Considerations

- Interop calls have overhead; cache frequently accessed objects
- Batch operations to minimize round-trips
- Profile hot paths using cProfile or py-spy

## Thread Safety

This wrapper is thread-safe when accessing the underlying .NET object
from multiple Python threads.

## Known Limitations

- Async methods are wrapped as blocking calls
- Events require manual subscription management
- Generic types require explicit type parameters

```

**Use Cases**:
- Generate README files for wrapper packages
- Create API documentation
- Document type conversions and limitations

---

### 6. `validate_wrapper`

**Purpose**: Validate wrapper implementation against standards

**Input Parameters**:
```json
{
  "wrapper_file_path": "/path/to/wrapper.py",
  "check_docstrings": true,
  "check_type_hints": true,
  "check_exception_handling": true,
  "check_context_manager": true,
  "check_test_coverage": true,
  "coverage_threshold": 80
}
```

**Output**:

```json
{
  "status": "pass",
  "issues": [
    {
      "severity": "warning",
      "location": "line 42",
      "code": "missing-docstring",
      "message": "Method 'configure' missing docstring",
      "suggestion": "Add docstring explaining method behavior"
    }
  ],
  "coverage": {
    "overall": 85,
    "status": "pass"
  },
  "checks": {
    "docstrings": { "status": "pass", "count": 12 },
    "type_hints": { "status": "pass", "count": 12 },
    "exception_handling": { "status": "pass", "caught_all_dotnet_exceptions": true },
    "context_manager": { "status": "pass", "implements_enter_exit": true }
  },
  "recommendations": [
    "Consider caching frequently accessed properties",
    "Add performance notes for expensive operations"
  ]
}
```

**Use Cases**:

- Validate wrapper implementation against standards
- Ensure consistent code quality
- Identify issues before deployment

---

## Type Conversion Rules

The MCP server maintains a database of standard type conversions:

| .NET Type             | Python Type       | Conversion Required   |
| --------------------- | ----------------- | --------------------- |
| System.String         | str               | No (automatic)        |
| System.Int32, Int64   | int               | No (automatic)        |
| System.Double, Single | float             | No (automatic)        |
| System.Boolean        | bool              | No (automatic)        |
| System.DateTime       | datetime.datetime | Yes (custom)          |
| System.Guid           | uuid.UUID         | Yes (custom)          |
| List<T>               | list              | Yes (iteration)       |
| Dictionary<K,V>       | dict              | Yes (iteration)       |
| Byte[]                | bytes             | Yes (conversion)      |
| IEnumerable<T>        | Iterator[T]       | Yes (lazy conversion) |

---

## Configuration File Format

MCP servers are configured in VS Code settings:

```json
{
  "modelContextProtocol": {
    "servers": {
      "pythonnet-wrapper-generator": {
        "command": "python",
        "args": [
          "-m",
          "pythonnet_wrapper_generator.server"
        ],
        "env": {
          "PYTHONNET_ENVIRONMENT": "development",
          "CLR_TRACE_ENABLED": "false"
        }
      }
    }
  }
}
```

---

## Error Handling

The MCP server provides detailed error messages for common issues:

### Assembly Not Found

```json
{
  "error": "ASSEMBLY_NOT_FOUND",
  "message": "Cannot locate assembly at path",
  "suggestions": [
    "Verify path is correct",
    "Ensure DLL exists",
    "Check permissions"
  ]
}
```

### Type Not Accessible

```json
{
  "error": "TYPE_NOT_ACCESSIBLE",
  "message": "Type is internal or inaccessible",
  "suggestions": [
    "Check if type is public",
    "Verify namespace is correct",
    "Check version compatibility"
  ]
}
```

### Unsupported Type Conversion

```json
{
  "error": "UNSUPPORTED_TYPE",
  "message": "No conversion rule for type System.CustomType",
  "suggestions": [
    "Create custom conversion method",
    "Check if type has simple representation",
    "Consider if wrapper is needed"
  ]
}
```

---

## Performance Considerations

1. **Reflection Overhead**: Initial assembly analysis may take time for large DLLs
2. **Code Generation**: Large assemblies generate substantial wrapper code
3. **Type Resolution**: Complex generic types require careful analysis

---

## Integration with Claude Code

The MCP server integrates with Claude Code through:

1. **Tool Invocation**: Ask Claude to generate wrappers using tools
2. **Workflow Support**: Automation of repetitive wrapper creation tasks
3. **Validation Pipeline**: Automatic validation of generated code
4. **Documentation**: Integrated documentation generation

---

## Development Roadmap

### Phase 1: MVP (Current)

- Assembly analysis via CLR reflection
- Basic wrapper class generation
- Simple type conversion utilities
- Unit test templates

### Phase 2: Enhanced Generation

- Async/await support
- Event handling utilities
- Generic type support
- Performance optimization hints

### Phase 3: Advanced Features

- Automated test execution
- Performance profiling integration
- Wrapper validation against standards
- Interactive wrapper customization

### Phase 4: Platform Integration

- VSCode Copilot integration
- MCP server auto-configuration
- Real-time wrapper feedback
- Continuous validation

---

## Security Considerations

1. **Assembly Loading**: Only load assemblies from trusted sources
2. **Code Execution**: Generated code executes in isolated test environment
3. **Type Safety**: Validate all type conversions
4. **Exception Handling**: Catch and translate all .NET exceptions

---

## References

- [Python.NET Documentation](https://pythonnet.github.io/)
- [CLR Reflection](https://docs.microsoft.com/en-us/dotnet/framework/reflection-and-codedom/reflection)
- [Type Conversion Guide](../prompts/dotnet-pythonnet-wrapper.prompt.md)
- [Wrapper Standards](pythonnet-wrapper.instructions.md)
