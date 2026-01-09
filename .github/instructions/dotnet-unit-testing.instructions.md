---
description: 'Unit testing standards and best practices for .NET projects across MSTest, NUnit, xUnit, and TUnit frameworks'
applies_to: '**/*.cs, **/*.csproj, **/Tests/**, **/test/**'
---

# .NET Unit Testing Standards

Comprehensive unit testing standards and best practices for .NET projects using MSTest, NUnit, xUnit, or TUnit frameworks.

## Core Principles

This content applies the following foundational principles:

- [Testing Standards](../core/principles/testing-standards.md) - TDD, AAA pattern, coverage targets
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Testability as quality metric
- [SOLID Principles](../core/principles/principles-solid.md) - Testability through proper architecture

---

## Framework Selection

### When to Use Each Framework

#### **MSTest** (Microsoft Test Framework)
- **Best for**: Enterprise projects using Visual Studio
- **Advantage**: Native integration with Visual Studio, Azure DevOps
- **When to choose**: Team already invested in Microsoft ecosystem
- **Drawback**: Less community support, older patterns
- **Attributes**: `[TestClass]`, `[TestMethod]`, `[DataTestMethod]`

#### **NUnit** (Most Flexible)
- **Best for**: Complex testing scenarios, maximum flexibility
- **Advantage**: Rich assertion library, extensive customization
- **When to choose**: Need advanced features (parameterized tests, data-driven)
- **Drawback**: Slightly more verbose syntax
- **Attributes**: `[TestFixture]`, `[Test]`, `[TestCase]`

#### **xUnit** (Modern, Recommended)
- **Best for**: New projects, modern architecture
- **Advantage**: Clean API, best-in-class design, active community
- **When to choose**: Starting new project, want industry best practice
- **Drawback**: Less legacy support
- **Attributes**: Constructor injection, `[Fact]`, `[Theory]`

#### **TUnit** (Latest, Cutting-Edge)
- **Best for**: Performance-critical testing, modern async patterns
- **Advantage**: Parallel execution, fast, advanced async support
- **When to choose**: High volume of tests, async-heavy codebase
- **Drawback**: Newest, smaller ecosystem
- **Attributes**: Source generators, modern C# features

### Framework Feature Comparison

| Feature | MSTest | NUnit | xUnit | TUnit |
|---------|--------|-------|-------|-------|
| **Attributes** | `[TestMethod]` | `[Test]` | `[Fact]` | `[Test]` |
| **Parameterized** | `[DataTestMethod]` | `[TestCase]` | `[Theory]` | `[Theory]` |
| **Async Support** | Good | Good | Excellent | Excellent |
| **Parallel Execution** | Yes | Yes | Yes | Yes (Default) |
| **Dependency Injection** | Manual | Constructor | Constructor | Constructor |
| **Community Size** | Medium | Large | Very Large | Growing |
| **Modern C# Support** | Good | Good | Excellent | Excellent |

---

## Standard Test Structure (AAA Pattern)

All tests follow the **Arrange-Act-Assert** pattern:

```csharp
[Fact]  // xUnit
public void MethodName_Scenario_ExpectedResult()
{
    // ARRANGE - Set up test conditions
    var sut = new SystemUnderTest();
    var input = new TestData();
    var expected = new Expected();

    // ACT - Execute the method
    var actual = sut.MethodBeingTested(input);

    // ASSERT - Verify the result
    Assert.Equal(expected, actual);
}
```

### Naming Convention

**Pattern**: `MethodName_Scenario_ExpectedResult`

```csharp
// ✅ Clear, specific
public void CalculateDiscount_CustomerIsGold_ReturnsPercentDiscount()
public void Transfer_InsufficientFunds_ThrowsInvalidOperationException()
public void GetUser_UserNotFound_ReturnsNull()

// ❌ Vague, unclear
public void TestDiscount()
public void TransferTest()
public void GetUserTest()
```

### When Naming Gets Long

For complex scenarios, use nested test classes for organization:

```csharp
public class OrderServiceTests
{
    public class CalculateTotalTests
    {
        [Fact]
        public void WithRegularCustomer_NoDiscount_ReturnsSumPrice()
        {
            // Test
        }

        [Fact]
        public void WithGoldCustomer_AppliesDiscount_ReturnsDiscountedPrice()
        {
            // Test
        }
    }

    public class ProcessPaymentTests
    {
        [Fact]
        public void WithValidCard_UpdatesInventory_ReturnsConfirmation()
        {
            // Test
        }
    }
}
```

---

## Test Project Organization

### Project Structure

```
MyProject/
├── src/
│   └── MyProject/
│       ├── Services/
│       │   ├── UserService.cs
│       │   └── OrderService.cs
│       └── Models/
│           └── User.cs
│
└── tests/
    └── MyProject.Tests/
        ├── Services/
        │   ├── UserServiceTests.cs
        │   └── OrderServiceTests.cs
        └── Models/
            └── UserTests.cs
```

### File Naming

- **Test files**: `ClassNameTests.cs` (one test class per class tested)
- **Fixtures**: `SharedFixture.cs`, `DatabaseFixture.cs`
- **Builders**: `UserBuilder.cs` (test data builders)
- **Fakes**: `FakeUserRepository.cs` (test doubles)

### Project File (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.6.1" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="Moq" Version="4.20.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="../src/MyProject/MyProject.csproj" />
  </ItemGroup>
</Project>
```

---

## Framework-Specific Patterns

### MSTest Pattern

```csharp
[TestClass]
public class CalculatorTests
{
    private Calculator _calculator;

    [TestInitialize]
    public void Setup()
    {
        _calculator = new Calculator();
    }

    [TestMethod]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var a = 2;
        var b = 3;

        // Act
        var result = _calculator.Add(a, b);

        // Assert
        Assert.AreEqual(5, result);
    }

    [DataTestMethod]
    [DataRow(2, 3, 5)]
    [DataRow(0, 0, 0)]
    [DataRow(-1, 1, 0)]
    public void Add_VariousInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        var result = _calculator.Add(a, b);
        Assert.AreEqual(expected, result);
    }
}
```

### NUnit Pattern

```csharp
[TestFixture]
public class CalculatorTests
{
    private Calculator _calculator;

    [SetUp]
    public void Setup()
    {
        _calculator = new Calculator();
    }

    [Test]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var a = 2;
        var b = 3;

        // Act
        var result = _calculator.Add(a, b);

        // Assert
        Assert.That(result, Is.EqualTo(5));
    }

    [TestCase(2, 3, 5)]
    [TestCase(0, 0, 0)]
    [TestCase(-1, 1, 0)]
    public void Add_VariousInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        var result = _calculator.Add(a, b);
        Assert.That(result, Is.EqualTo(expected));
    }
}
```

### xUnit Pattern (Recommended)

```csharp
public class CalculatorTests
{
    [Fact]
    public void Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();
        var a = 2;
        var b = 3;

        // Act
        var result = calculator.Add(a, b);

        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(0, 0, 0)]
    [InlineData(-1, 1, 0)]
    public void Add_VariousInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        var calculator = new Calculator();
        var result = calculator.Add(a, b);
        Assert.Equal(expected, result);
    }

    // With MemberData
    [Theory]
    [MemberData(nameof(GetTestData))]
    public void Add_WithTestData_ReturnsCorrectSum(int a, int b, int expected)
    {
        var calculator = new Calculator();
        var result = calculator.Add(a, b);
        Assert.Equal(expected, result);
    }

    public static IEnumerable<object[]> GetTestData()
    {
        yield return new object[] { 2, 3, 5 };
        yield return new object[] { 0, 0, 0 };
        yield return new object[] { -1, 1, 0 };
    }
}
```

### TUnit Pattern (Modern Async)

```csharp
public class CalculatorTests
{
    [Test]
    public async Task Add_TwoPositiveNumbers_ReturnsSum()
    {
        // Arrange
        var calculator = new Calculator();
        var a = 2;
        var b = 3;

        // Act
        var result = await calculator.AddAsync(a, b);

        // Assert
        Assert.That(result).IsEqualTo(5);
    }

    [Test]
    [Arguments(2, 3, 5)]
    [Arguments(0, 0, 0)]
    [Arguments(-1, 1, 0)]
    public async Task Add_VariousInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        var calculator = new Calculator();
        var result = await calculator.AddAsync(a, b);
        Assert.That(result).IsEqualTo(expected);
    }
}
```

---

## Assertions Across Frameworks

### Common Assertions

#### MSTest
```csharp
Assert.AreEqual(expected, actual);
Assert.IsTrue(condition);
Assert.IsFalse(condition);
Assert.IsNull(value);
Assert.IsNotNull(value);
Assert.ThrowsException<Exception>(() => method());
Assert.IsInstanceOfType(value, typeof(Type));
```

#### NUnit
```csharp
Assert.That(actual, Is.EqualTo(expected));
Assert.That(condition, Is.True);
Assert.That(condition, Is.False);
Assert.That(value, Is.Null);
Assert.That(value, Is.Not.Null);
Assert.Throws<Exception>(() => method());
Assert.That(value, Is.InstanceOf<Type>());
Assert.That(items, Has.Length.EqualTo(5));
```

#### xUnit
```csharp
Assert.Equal(expected, actual);
Assert.True(condition);
Assert.False(condition);
Assert.Null(value);
Assert.NotNull(value);
Assert.Throws<Exception>(() => method());
Assert.IsType<Type>(value);
Assert.NotStrictEqual(expected, actual);
Assert.Contains(expected, collection);
Assert.DoesNotContain(expected, collection);
```

### Advanced Assertions

**Collection Assertions**:
```csharp
// xUnit
Assert.Equal(new[] { 1, 2, 3 }, list);
Assert.Contains(item, list);
Assert.All(list, item => Assert.NotNull(item));

// NUnit
Assert.That(list, Has.Exactly(3).Items);
Assert.That(list, Contains.Item(item));
```

**String Assertions**:
```csharp
// xUnit
Assert.StartsWith("prefix", text);
Assert.EndsWith("suffix", text);
Assert.Contains("substring", text);
Assert.Matches(pattern, text);

// NUnit
Assert.That(text, Does.StartWith("prefix"));
Assert.That(text, Does.EndWith("suffix"));
Assert.That(text, Does.Contain("substring"));
Assert.That(text, Does.Match(pattern));
```

---

## Test Doubles (Mocks, Stubs, Fakes)

### Using Moq Library

```csharp
[Fact]
public void ProcessOrder_ValidOrder_CallsPaymentService()
{
    // Arrange
    var mockPaymentService = new Mock<IPaymentService>();
    mockPaymentService
        .Setup(x => x.Charge(It.IsAny<decimal>()))
        .ReturnsAsync(true);

    var orderService = new OrderService(mockPaymentService.Object);

    // Act
    var order = new Order { Total = 100m };
    var result = orderService.ProcessOrder(order);

    // Assert
    Assert.True(result);
    mockPaymentService.Verify(
        x => x.Charge(It.IsAny<decimal>()),
        Times.Once);
}
```

### Creating Fakes for Complex Tests

```csharp
public class FakeUserRepository : IUserRepository
{
    private readonly List<User> _users = new();

    public async Task<User> GetByIdAsync(int id)
    {
        return _users.FirstOrDefault(u => u.Id == id);
    }

    public async Task SaveAsync(User user)
    {
        _users.Add(user);
    }

    public void AddTestData(User user)
    {
        _users.Add(user);
    }
}

[Fact]
public async Task GetUser_UserExists_ReturnsUser()
{
    // Arrange
    var repository = new FakeUserRepository();
    var user = new User { Id = 1, Name = "John" };
    repository.AddTestData(user);

    // Act
    var result = await repository.GetByIdAsync(1);

    // Assert
    Assert.NotNull(result);
    Assert.Equal("John", result.Name);
}
```

### Test Builders for Complex Objects

```csharp
public class UserBuilder
{
    private int _id = 1;
    private string _name = "Test User";
    private string _email = "test@example.com";
    private bool _isActive = true;

    public UserBuilder WithId(int id)
    {
        _id = id;
        return this;
    }

    public UserBuilder WithName(string name)
    {
        _name = name;
        return this;
    }

    public UserBuilder WithEmail(string email)
    {
        _email = email;
        return this;
    }

    public UserBuilder Inactive()
    {
        _isActive = false;
        return this;
    }

    public User Build()
    {
        return new User
        {
            Id = _id,
            Name = _name,
            Email = _email,
            IsActive = _isActive
        };
    }
}

[Fact]
public void UpdateUser_InactiveUser_DoesNotUpdate()
{
    // Arrange
    var user = new UserBuilder()
        .WithName("John")
        .Inactive()
        .Build();

    var service = new UserService();

    // Act
    var result = service.UpdateUser(user);

    // Assert
    Assert.False(result);
}
```

---

## Async Testing

### Testing Async Methods

```csharp
[Fact]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var service = new UserService();
    var userId = 1;

    // Act
    var user = await service.GetUserAsync(userId);

    // Assert
    Assert.NotNull(user);
}

// Do NOT use .Result or .Wait()
[Fact]
public async Task MethodAsync_ShouldTest_Result()
{
    var result = await service.MethodAsync(); // ✅ Correct
    // var result = service.MethodAsync().Result; // ❌ Can deadlock
}
```

### Testing Exception Handling in Async

```csharp
[Fact]
public async Task GetUserAsync_InvalidId_ThrowsArgumentException()
{
    // Arrange
    var service = new UserService();

    // Act & Assert
    await Assert.ThrowsAsync<ArgumentException>(
        () => service.GetUserAsync(-1)
    );
}
```

---

## Coverage Requirements

### Minimum Coverage Standards

- **Overall Coverage**: 80% minimum
- **Critical Paths**: 100% coverage required
- **Edge Cases**: 90% coverage recommended
- **Error Handling**: 100% coverage required

### Coverage Metrics

```csharp
// Coverage types:
// - Line Coverage: % of lines executed
// - Branch Coverage: % of if/else paths taken
// - Method Coverage: % of methods called

// Measure with:
// - OpenCover (MSTest, NUnit)
// - coverlet (any framework)
// - Codecov integration
```

### Calculating Coverage

```bash
# Using coverlet with xUnit
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=opencover

# View coverage report
# Reports generated in: TestResults/coverage.opencover.xml
```

---

## Best Practices

### ✅ Do's

- **Arrange-Act-Assert pattern**: Always follow AAA structure
- **One assertion per test (ideally)**: Or logically related assertions
- **Clear naming**: Test name describes what is being tested
- **Test behavior, not implementation**: Don't test private methods
- **Use builders for complex objects**: Keep test setup readable
- **Test edge cases**: Null, empty, negative, boundary values
- **Isolate tests**: Each test independent, no test order dependency
- **Mock external dependencies**: Database, API, file system
- **Fast execution**: Tests should complete in milliseconds
- **Deterministic results**: Same input always produces same result

### ❌ Don'ts

- **Don't test multiple behaviors**: One test, one behavior
- **Don't use Thread.Sleep()**: Use async/await or dedicated timing
- **Don't hardcode test data**: Use builders or fixtures
- **Don't test private methods**: Test through public API
- **Don't test framework code**: Trust the framework
- **Don't create test interdependencies**: Tests should run in any order
- **Don't share mutable state**: Each test gets clean state
- **Don't catch exceptions**: Let them bubble up to see failures
- **Don't use real external services**: Mock them
- **Don't skip tests**: Mark with `[Fact(Skip = "reason")]` if needed

---

## Configuration and Execution

### Running Tests

```bash
# Run all tests
dotnet test

# Run specific project
dotnet test ./tests/MyProject.Tests.csproj

# Run specific test class
dotnet test --filter ClassName=UserServiceTests

# Run specific test
dotnet test --filter FullyQualifiedName=MyProject.Tests.UserServiceTests.GetUser

# Run with verbose output
dotnet test --verbosity detailed

# Run in parallel
dotnet test --parallel

# Generate coverage report
dotnet test /p:CollectCoverage=true
```

### Test Configuration (xunit.runner.json)

```json
{
  "diagnosticMessages": false,
  "maxParallelThreads": 4,
  "methodDisplay": "method",
  "parallelizeAssembly": true,
  "parallelizeTestCollections": true,
  "preEnumerateTheories": true,
  "shadowCopy": false,
  "longRunningTestSeconds": 10
}
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run tests
  run: dotnet test --configuration Release --no-build --verbosity normal

- name: Publish coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.opencover.xml
```

---

## Common Testing Scenarios

### Testing Exceptions

```csharp
[Fact]
public void Divide_ByZero_ThrowsDivideByZeroException()
{
    // Arrange
    var calculator = new Calculator();

    // Act & Assert
    Assert.Throws<DivideByZeroException>(() => calculator.Divide(10, 0));
}

[Fact]
public void ValidateEmail_InvalidEmail_ThrowsArgumentException()
{
    var validator = new EmailValidator();
    var ex = Assert.Throws<ArgumentException>(() => validator.Validate("invalid"));
    Assert.Equal("Invalid email format", ex.Message);
}
```

### Testing Collections

```csharp
[Fact]
public void FilterUsers_WithMinimumAge_ReturnsFilteredList()
{
    // Arrange
    var users = new[]
    {
        new User { Name = "John", Age = 30 },
        new User { Name = "Jane", Age = 25 },
        new User { Name = "Bob", Age = 20 }
    };
    var service = new UserService();

    // Act
    var result = service.FilterByMinimumAge(users, 25).ToList();

    // Assert
    Assert.Equal(2, result.Count);
    Assert.Contains(result, u => u.Name == "John");
    Assert.Contains(result, u => u.Name == "Jane");
    Assert.DoesNotContain(result, u => u.Name == "Bob");
}
```

### Testing with Timestamps

```csharp
[Fact]
public void CreateUser_SetsCreatedAtToNow()
{
    // Arrange
    var beforeCreation = DateTime.UtcNow;
    var service = new UserService();

    // Act
    var user = service.CreateUser("John");
    var afterCreation = DateTime.UtcNow;

    // Assert
    Assert.True(user.CreatedAt >= beforeCreation);
    Assert.True(user.CreatedAt <= afterCreation);
}
```

---

## Quality Checklist

- [ ] Tests follow AAA pattern consistently
- [ ] Test names clearly describe behavior being tested
- [ ] No test dependencies or test order requirements
- [ ] All external dependencies mocked
- [ ] Tests are fast (complete in < 100ms ideally)
- [ ] Edge cases and error conditions tested
- [ ] No hardcoded test data (use builders/fixtures)
- [ ] Coverage meets minimum standards (80%+)
- [ ] Critical paths have 100% coverage
- [ ] Error handling fully tested
- [ ] Tests are deterministic (no timing issues)
- [ ] Async tests properly await results
- [ ] Test doubles appropriate for scenario
- [ ] No secrets or sensitive data in tests
- [ ] Tests pass consistently

---

## Related Content

- For test architecture: Review SOLID principles
- For mocking strategies: Moq documentation
- For async patterns: Microsoft async best practices
- For CI/CD: GitHub Actions or Azure DevOps documentation
- For profiling test performance: dotTrace or dotMemory
