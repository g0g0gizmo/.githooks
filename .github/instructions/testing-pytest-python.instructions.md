---
description: 'Pytest framework best practices for Python applications and data science'
applyTo: '**/*_test.py,**/test_*.py'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Use fixtures and parametrization to eliminate test duplication
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain readability and comprehensive test coverage
- [Testing Standards](../core/principles/testing-standards.md) - Follow AAA pattern and clear test organization

When writing tests with pytest, always consider how they reinforce these core principles and create sustainable, maintainable test suites.

---

# Pytest + Python Testing

## Overview

Pytest is the most popular testing framework for Python, offering powerful features including fixtures, parametrization, plugins, and clear assertion syntax. It works seamlessly with data science libraries and production Python applications.

## Pytest Installation and Configuration

### Installation
```bash
pip install pytest pytest-cov pytest-asyncio pytest-mock
```

### pytest.ini Configuration
```ini
[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --cov=src --cov-report=html
markers =
    unit: unit tests
    integration: integration tests
    slow: slow running tests
    asyncio: async tests
```

### pyproject.toml Configuration
```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = ["-v", "--strict-markers", "--cov=src"]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning"
]

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

## Test File Organization

### Directory Structure
```
project/
├── src/
│   ├── services/
│   │   ├── auth.py
│   │   └── payment.py
│   ├── utils/
│   │   └── helpers.py
│   └── models/
│       └── user.py
├── tests/
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_payment.py
│   │   └── test_helpers.py
│   ├── integration/
│   │   └── test_api.py
│   ├── fixtures.py
│   └── conftest.py
└── pyproject.toml
```

### File Naming Convention
- Test files: `test_*.py` or `*_test.py`
- Fixtures: Defined in `conftest.py` for sharing across tests
- Test utilities: `test_utils.py` or `testing_helpers.py`

## Test Structure (AAA Pattern)

All tests must follow the **Arrange-Act-Assert** pattern:

```python
import pytest
from src.services.user import UserService
from src.models.user import User

class TestUserService:
    """Test suite for UserService class."""

    def test_create_user_with_valid_input(self, user_service):
        """Should create a new user with valid input."""
        # Arrange: Prepare test data and dependencies
        user_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }

        # Act: Execute the code under test
        user = user_service.create_user(user_data)

        # Assert: Verify the expected outcome
        assert user.id is not None
        assert user.name == 'John Doe'
        assert user.email == 'john@example.com'

    def test_create_user_raises_validation_error_with_invalid_email(self, user_service):
        """Should raise ValidationError when email is invalid."""
        # Arrange
        invalid_data = {'name': 'John', 'email': 'not-an-email'}

        # Act & Assert
        with pytest.raises(ValueError, match='Invalid email format'):
            user_service.create_user(invalid_data)
```

## Fixtures and Setup/Teardown

### Basic Fixtures
```python
# conftest.py - shared across all tests
import pytest
from src.services.user import UserService
from src.database import Database

@pytest.fixture
def database():
    """Create an in-memory test database."""
    db = Database(":memory:")
    db.connect()
    yield db  # Test runs here
    db.close()

@pytest.fixture
def user_service(database):
    """Create UserService with test database."""
    return UserService(database)

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'age': 30
    }
```

### Fixture Scopes
```python
@pytest.fixture(scope="function")  # Default: new instance per test
def function_scoped():
    return setup()

@pytest.fixture(scope="class")     # Shared within test class
def class_scoped():
    return setup()

@pytest.fixture(scope="module")    # Shared within module
def module_scoped():
    return setup()

@pytest.fixture(scope="session")   # Shared across all tests
def session_scoped():
    return setup()
```

### Fixture Cleanup
```python
@pytest.fixture
def temporary_directory():
    """Create and clean up temporary directory."""
    import tempfile
    import shutil

    tmpdir = tempfile.mkdtemp()
    yield tmpdir  # Test runs here
    shutil.rmtree(tmpdir)  # Cleanup
```

## Parametrized Tests

### Simple Parametrization
```python
import pytest

@pytest.mark.parametrize('email,expected', [
    ('user@example.com', True),
    ('invalid.email', False),
    ('test@domain.co.uk', True),
    ('', False),
])
def test_email_validation(email, expected):
    """Test email validation with multiple inputs."""
    result = validate_email(email)
    assert result == expected
```

### Multiple Parameters
```python
@pytest.mark.parametrize('input_value,operation,expected', [
    (10, 'square', 100),
    (5, 'double', 10),
    (0, 'square', 0),
    (-5, 'double', -10),
])
def test_math_operations(input_value, operation, expected):
    """Test various math operations."""
    result = perform_operation(input_value, operation)
    assert result == expected
```

### Indirect Parametrization
```python
@pytest.fixture
def user_fixture(request):
    """Create user based on parameter."""
    user_data = request.param
    return User(**user_data)

@pytest.mark.parametrize('user_fixture', [
    {'name': 'Admin', 'role': 'admin'},
    {'name': 'User', 'role': 'user'},
], indirect=True)
def test_user_permissions(user_fixture):
    """Test permissions for different user roles."""
    assert user_fixture.can_create_content == (user_fixture.role == 'admin')
```

## Mocking and Patching

### Using pytest-mock
```python
def test_payment_processing(mocker, payment_service):
    """Test payment processing with mocked gateway."""
    # Arrange: Create mock
    mock_gateway = mocker.patch('src.services.payment.PaymentGateway')
    mock_gateway.charge.return_value = {'status': 'success', 'txn_id': '123'}

    # Act
    result = payment_service.process_payment(100)

    # Assert
    assert result['status'] == 'success'
    mock_gateway.charge.assert_called_once_with(100)
```

### Mocking with Context Manager
```python
from unittest.mock import patch, MagicMock

def test_api_call():
    """Test function that calls external API."""
    with patch('src.api.requests.get') as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'data': 'value'})

        result = fetch_data('http://api.example.com')
        assert result == {'data': 'value'}
```

### Mocking File Operations
```python
def test_file_processing(mocker):
    """Test file processing without actual file I/O."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data='file content'))

    content = read_file('path/to/file.txt')

    assert content == 'file content'
    mock_open.assert_called_once_with('path/to/file.txt', 'r')
```

## Async Testing

### Testing Async Functions
```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await async_fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_async_with_timeout():
    """Test async function with timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(long_running_async_task(), timeout=1.0)
```

### Async Fixtures
```python
@pytest.fixture
async def async_database():
    """Create async database connection."""
    db = AsyncDatabase()
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_async_query(async_database):
    """Test async database query."""
    result = await async_database.query('SELECT * FROM users')
    assert len(result) > 0
```

## Exceptions and Error Handling

### Testing Exceptions
```python
def test_division_by_zero():
    """Should raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_exception_with_message():
    """Should raise ValueError with specific message."""
    with pytest.raises(ValueError, match='Invalid input'):
        process_data(None)

def test_exception_info():
    """Capture and verify exception details."""
    with pytest.raises(ValueError) as exc_info:
        invalid_operation()

    assert 'specific error' in str(exc_info.value)
```

## Markers and Test Organization

### Built-in Markers
```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_modern_syntax():
    pass

@pytest.mark.xfail(reason="Known issue")
def test_known_bug():
    pass
```

### Custom Markers
```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "db: marks tests that use database")

# In tests
@pytest.mark.slow
def test_long_operation():
    pass

@pytest.mark.db
def test_database_query():
    pass
```

### Running Specific Tests
```bash
# Run only unit tests
pytest -m unit

# Run all except slow tests
pytest -m "not slow"

# Run specific file
pytest tests/unit/test_auth.py

# Run specific test class
pytest tests/unit/test_auth.py::TestAuthService

# Run specific test
pytest tests/unit/test_auth.py::TestAuthService::test_login_valid
```

## Test Coverage

### Generate Coverage Report
```bash
# Terminal report
pytest --cov=src --cov-report=term-missing

# HTML report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

### Coverage Standards
```ini
[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

## Factories and Builders for DRY Tests

### Factory Pattern
```python
from dataclasses import dataclass
from src.models.user import User

@dataclass
class UserFactory:
    """Factory for creating test users."""
    name: str = "Test User"
    email: str = "test@example.com"
    role: str = "user"

    def build(self) -> User:
        """Create User instance."""
        return User(name=self.name, email=self.email, role=self.role)

    def as_admin(self):
        """Create admin user."""
        self.role = "admin"
        return self

# Usage
user = UserFactory().build()
admin = UserFactory().as_admin().build()
```

### Pytest Factory Fixture
```python
@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    def _create_user(name="Test", email="test@example.com", **kwargs):
        return User(name=name, email=email, **kwargs)
    return _create_user

def test_with_factory(user_factory):
    """Test using factory fixture."""
    user = user_factory(name="John")
    assert user.name == "John"
```

## Best Practices

### ✓ Good Patterns

**1. Clear Test Names Describing Behavior**
```python
def test_should_raise_validation_error_when_email_is_invalid():
    """Clearly describes what should happen."""
    pass
```

**2. Use Assertions with Custom Messages**
```python
assert user.age >= 18, f"User age must be 18+, got {user.age}"
```

**3. Extract Common Setup**
```python
@pytest.fixture
def setup_test_user():
    return User(name="Test", email="test@example.com")
```

**4. Isolate External Dependencies**
```python
def test_payment(mocker):
    # Mock external payment service
    mocker.patch('external_service.charge')
```

### ✗ Anti-Patterns to Avoid

**1. Tests That Share State**
```python
# ✗ Bad: Test order dependency
class TestUserSequence:
    user_id = None

    def test_1_create_user(self):
        # Creates global user_id
        pass

    def test_2_use_user(self):
        # Depends on test_1
        pass
```

**2. Testing Implementation Details**
```python
# ✗ Bad: Testing private methods
def test_private_calculation():
    assert obj._internal_calc() == 42
```

**3. Non-Descriptive Assertions**
```python
# ✗ Bad
assert x

# ✓ Good
assert user.is_active, "User should be active after creation"
```

**4. Lack of Isolation**
```python
# ✗ Bad: Tests make real database calls
def test_user_creation():
    # Actually writes to production database
    pass
```

## Data Science Testing

### Testing Pandas DataFrames
```python
import pandas as pd
import pytest

def test_data_transformation(sample_dataframe):
    """Test dataframe transformation."""
    result = transform_data(sample_dataframe)

    assert result.shape[0] > 0
    assert 'processed_column' in result.columns
    assert result['processed_column'].dtype == 'float64'

@pytest.fixture
def sample_dataframe():
    """Create sample dataframe for testing."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30],
        'category': ['A', 'B', 'A']
    })
```

### Testing ML Models
```python
from sklearn.model_selection import train_test_split
import numpy as np

def test_model_prediction():
    """Test ML model prediction."""
    X = np.array([[1, 2], [3, 4], [5, 6]])
    y = np.array([0, 1, 0])

    model = train_model(X, y)
    prediction = model.predict([[2, 3]])

    assert prediction.shape == (1,)
    assert prediction[0] in [0, 1]

def test_model_accuracy():
    """Test model reaches minimum accuracy threshold."""
    model = train_model(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    assert accuracy >= 0.75, f"Model accuracy too low: {accuracy}"
```

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login

# Run with keyword matching
pytest -k "login"

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Generate coverage report
pytest --cov=src --cov-report=html
```

---

## Related Instructions

- [Python Best Practices](./python.instructions.md)
- [General Testing Standards](../core/principles/testing-standards.md)
