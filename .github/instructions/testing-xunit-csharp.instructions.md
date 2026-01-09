---
description: 'xUnit.net testing framework best practices for C# and .NET applications'
applyTo: '**/*.Tests.cs,**/*Test.cs'
---

## Core Engineering Principles

This instruction set applies the following foundational principles:

- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Use fixtures and shared context to eliminate duplication
- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain clarity and comprehensive assertion patterns
- [Testing Standards](../core/principles/testing-standards.md) - Follow AAA pattern and organize tests by behavior

When writing xUnit tests, always consider how they reinforce these core principles and create maintainable test suites.

---

# xUnit.net + C# Testing

## Overview

xUnit.net is the most modern testing framework for .NET, built by the original creator of NUnit. It emphasizes clean code organization, proper fixture usage, and clear assertions through strong typing and extension points.

## xUnit Setup and Configuration

### NuGet Installation
```bash
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
dotnet add package Moq
dotnet add package FluentAssertions
```

### Project File Configuration (.csproj)
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="xunit" Version="2.6.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.1">
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\YourProject\YourProject.csproj" />
  </ItemGroup>
</Project>
```

### xunit.runner.json Configuration
```json
{
  "$schema": "https://xunit.net/schema/current/xunit.runner.schema.json",
  "diagnosticMessages": false,
  "methodDisplay": "method",
  "methodDisplayOptions": "all",
  "shadowCopy": false
}
```

## Test File Organization

### Directory Structure
```
YourProject/
├── src/
│   ├── Services/
│   │   ├── AuthService.cs
│   │   └── PaymentService.cs
│   ├── Models/
│   │   └── User.cs
│   └── Utils/
│       └── Helpers.cs
├── tests/
│   ├── YourProject.Tests.csproj
│   ├── Unit/
│   │   ├── Services/
│   │   │   ├── AuthServiceTests.cs
│   │   │   └── PaymentServiceTests.cs
│   │   └── Utils/
│   │       └── HelpersTests.cs
│   ├── Integration/
│   │   └── ApiTests.cs
│   └── Fixtures/
│       ├── DatabaseFixture.cs
│       └── TestDataBuilder.cs
```

### Naming Convention
- Test classes: `[Class]Tests` (e.g., `UserServiceTests`)
- Test methods: `[Method]_[Scenario]_[Expected]`
  - Example: `Login_WithValidCredentials_ReturnsAuthToken`
- Fixtures: `[Resource]Fixture` (e.g., `DatabaseFixture`)

## Test Structure (AAA Pattern)

All tests must follow **Arrange-Act-Assert** pattern:

```csharp
public class UserServiceTests
{
    private readonly UserService _userService;
    private readonly Mock<IUserRepository> _mockRepository;

    public UserServiceTests()
    {
        _mockRepository = new Mock<IUserRepository>();
        _userService = new UserService(_mockRepository.Object);
    }

    [Fact]
    public void CreateUser_WithValidInput_ReturnsUserWithId()
    {
        // Arrange: Set up test data and dependencies
        var userData = new CreateUserRequest
        {
            Name = "John Doe",
            Email = "john@example.com"
        };

        // Act: Execute the code under test
        var result = _userService.CreateUser(userData);

        // Assert: Verify the expected outcome
        Assert.NotNull(result.Id);
        Assert.Equal("John Doe", result.Name);
        Assert.Equal("john@example.com", result.Email);
    }

    [Fact]
    public void CreateUser_WithInvalidEmail_ThrowsValidationException()
    {
        // Arrange
        var userData = new CreateUserRequest
        {
            Name = "John",
            Email = "invalid-email"
        };

        // Act & Assert
        var exception = Assert.Throws<ValidationException>(
            () => _userService.CreateUser(userData)
        );
        Assert.Contains("Invalid email", exception.Message);
    }
}
```

## Fixtures and Setup/Teardown

### Class Fixtures
```csharp
public class DatabaseFixture : IAsyncLifetime
{
    private readonly IContainer _container;
    public IUserRepository Repository { get; private set; }

    public DatabaseFixture()
    {
        _container = new TestDatabaseContainer();
    }

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
        Repository = new UserRepository(_container.ConnectionString);
        await Repository.CreateSchemaAsync();
    }

    public async Task DisposeAsync()
    {
        await _container.StopAsync();
    }
}

public class UserServiceIntegrationTests : IAsyncLifetime
{
    private readonly DatabaseFixture _fixture = new();

    public async Task InitializeAsync() => await _fixture.InitializeAsync();
    public async Task DisposeAsync() => await _fixture.DisposeAsync();

    [Fact]
    public async Task GetUser_WithExistingId_ReturnsUser()
    {
        // Use _fixture.Repository in test
        var user = await _fixture.Repository.GetUserAsync(1);
        Assert.NotNull(user);
    }
}
```

### Collection Fixtures for Shared Resources
```csharp
[CollectionDefinition("Database collection")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture>
{
    // This class defines the collection
    // No code needed here
}

[Collection("Database collection")]
public class UserServiceTests
{
    private readonly DatabaseFixture _fixture;

    public UserServiceTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task GetUser_ReturnsUserFromDatabase()
    {
        var user = await _fixture.Repository.GetUserAsync(1);
        Assert.NotNull(user);
    }
}

[Collection("Database collection")]
public class OrderServiceTests
{
    private readonly DatabaseFixture _fixture;

    public OrderServiceTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public async Task CreateOrder_SavesToDatabase()
    {
        // Uses same database fixture as UserServiceTests
    }
}
```

### Constructor Dependency Injection
```csharp
public class PaymentServiceTests
{
    private readonly Mock<IPaymentGateway> _mockGateway;
    private readonly Mock<ILogger> _mockLogger;
    private readonly PaymentService _service;

    public PaymentServiceTests()
    {
        _mockGateway = new Mock<IPaymentGateway>();
        _mockLogger = new Mock<ILogger>();
        _service = new PaymentService(_mockGateway.Object, _mockLogger.Object);
    }

    [Fact]
    public void ProcessPayment_WithValidAmount_CallsGateway()
    {
        _mockGateway
            .Setup(g => g.Charge(It.IsAny<decimal>()))
            .ReturnsAsync(new { TransactionId = "123" });

        var result = _service.ProcessPayment(100);

        _mockGateway.Verify(g => g.Charge(100), Times.Once);
    }
}
```

## Theory and Parametrized Tests

### InlineData Attribute
```csharp
public class EmailValidationTests
{
    [Theory]
    [InlineData("user@example.com", true)]
    [InlineData("invalid.email", false)]
    [InlineData("test@domain.co.uk", true)]
    [InlineData("", false)]
    public void ValidateEmail_WithVariousInputs_ReturnsExpected(string email, bool expected)
    {
        var result = EmailValidator.IsValid(email);
        Assert.Equal(expected, result);
    }
}
```

### MemberData Attribute
```csharp
public class MathOperationTests
{
    public static TheoryData<int, string, int> OperationData => new TheoryData<int, string, int>
    {
        { 10, "square", 100 },
        { 5, "double", 10 },
        { 0, "square", 0 },
        { -5, "double", -10 }
    };

    [Theory]
    [MemberData(nameof(OperationData))]
    public void PerformOperation_WithVariousInputs_ReturnsExpected(int input, string op, int expected)
    {
        var result = MathHelper.Perform(input, op);
        Assert.Equal(expected, result);
    }
}
```

### ClassData Attribute
```csharp
public class TestDataGenerator : TheoryData<string, bool>
{
    public TestDataGenerator()
    {
        Add("valid@example.com", true);
        Add("invalid-email", false);
        Add("user@domain.co.uk", true);
    }
}

public class EmailValidationTheoryTests
{
    [Theory]
    [ClassData(typeof(TestDataGenerator))]
    public void ValidateEmail_WithGeneratedData_ReturnsExpected(string email, bool expected)
    {
        var result = EmailValidator.IsValid(email);
        Assert.Equal(expected, result);
    }
}
```

## Mocking with Moq

### Basic Mocking
```csharp
public class UserServiceTests
{
    [Fact]
    public void GetUser_WithValidId_ReturnsUser()
    {
        // Arrange
        var mockRepository = new Mock<IUserRepository>();
        var user = new User { Id = 1, Name = "Test User", Email = "test@example.com" };

        mockRepository
            .Setup(r => r.GetUserAsync(1))
            .ReturnsAsync(user);

        var service = new UserService(mockRepository.Object);

        // Act
        var result = service.GetUser(1);

        // Assert
        Assert.Equal(user.Name, result.Name);
        mockRepository.Verify(r => r.GetUserAsync(1), Times.Once);
    }
}
```

### Advanced Mocking Patterns
```csharp
// Setup multiple calls
mockRepository
    .SetupSequence(r => r.GetCount())
    .Returns(0)
    .Returns(1)
    .Returns(2);

// Setup with callback
mockRepository
    .Setup(r => r.SaveUser(It.IsAny<User>()))
    .Callback<User>(u => u.Id = Guid.NewGuid());

// Setup with parameter matching
mockRepository
    .Setup(r => r.FindUsers(It.Is<UserFilter>(f => f.Active)))
    .ReturnsAsync(new[] { activeUser });

// Setup to throw exception
mockRepository
    .Setup(r => r.DeleteUser(0))
    .Throws<ArgumentException>();
```

### Verification Patterns
```csharp
// Verify call was made
mockRepository.Verify(r => r.SaveUser(It.IsAny<User>()), Times.Once);

// Verify call was not made
mockRepository.Verify(r => r.DeleteUser(It.IsAny<int>()), Times.Never);

// Verify exact number of calls
mockRepository.Verify(r => r.UpdateUser(It.IsAny<User>()), Times.Exactly(2));

// Verify no other calls
mockRepository.VerifyNoOtherCalls();
```

## FluentAssertions

### Basic Assertions
```csharp
public class UserTests
{
    [Fact]
    public void User_WithValidData_CreatesSuccessfully()
    {
        // Arrange
        var user = new User { Id = 1, Name = "John", Email = "john@example.com" };

        // Act & Assert - FluentAssertions
        user.Id.Should().Be(1);
        user.Name.Should().NotBeNullOrEmpty();
        user.Email.Should().Contain("@");
    }
}
```

### Collection Assertions
```csharp
[Fact]
public void GetActiveUsers_ReturnsExpectedUsers()
{
    // Arrange
    var users = new[]
    {
        new User { Id = 1, Name = "John", Active = true },
        new User { Id = 2, Name = "Jane", Active = true },
        new User { Id = 3, Name = "Bob", Active = false }
    };

    // Act
    var activeUsers = users.Where(u => u.Active).ToList();

    // Assert
    activeUsers
        .Should()
        .HaveCount(2)
        .And.AllSatisfy(u => u.Active.Should().BeTrue())
        .And.Contain(u => u.Name == "John")
        .And.NotContain(u => u.Name == "Bob");
}
```

### Exception Assertions
```csharp
[Fact]
public void CreateUser_WithInvalidEmail_ThrowsValidationException()
{
    // Arrange
    var userData = new CreateUserRequest { Email = "invalid" };

    // Act & Assert
    var act = () => new UserValidator().ValidateAndThrow(userData);

    act
        .Should()
        .Throw<ValidationException>()
        .WithMessage("*Invalid email*")
        .And.Subject.Should().NotBeNull();
}
```

### Async Assertions
```csharp
[Fact]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var service = new UserService(mockRepository.Object);

    // Act & Assert
    var act = async () => await service.GetUserAsync(1);

    await act
        .Should()
        .NotThrowAsync()
        .And.CompleteWithinAsync(TimeSpan.FromSeconds(1));
}
```

## Test Data Builders

### Builder Pattern
```csharp
public class UserBuilder
{
    private string _name = "Test User";
    private string _email = "test@example.com";
    private int _age = 25;
    private bool _active = true;

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

    public UserBuilder AsInactive()
    {
        _active = false;
        return this;
    }

    public User Build()
    {
        return new User
        {
            Name = _name,
            Email = _email,
            Age = _age,
            Active = _active
        };
    }
}

// Usage in tests
public class UserServiceTests
{
    [Fact]
    public void ProcessUser_WithInactiveUser_DoesNotProcess()
    {
        var inactiveUser = new UserBuilder().AsInactive().Build();
        // Use inactiveUser in test
    }
}
```

## Async Testing

### Testing Async Methods
```csharp
public class AsyncServiceTests
{
    [Fact]
    public async Task FetchDataAsync_WithValidId_ReturnsData()
    {
        // Arrange
        var service = new AsyncService();

        // Act
        var result = await service.FetchDataAsync(1);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(1);
    }

    [Fact]
    public async Task FetchDataAsync_WithInvalidId_ThrowsException()
    {
        // Arrange
        var service = new AsyncService();

        // Act & Assert
        await FluentActions
            .Invoking(() => service.FetchDataAsync(-1))
            .Should()
            .ThrowAsync<ArgumentException>();
    }
}
```

## Best Practices

### ✓ Good Patterns

**1. Clear, Descriptive Test Names**
```csharp
[Fact]
public void CreateUser_WithValidEmailAndName_ReturnsUserWithGeneratedId()
{
    // Test logic
}
```

**2. One Logical Assertion per Test**
```csharp
[Fact]
public void User_WithValidAge_IsConsideredAdult()
{
    var user = new User { Age = 25 };
    user.IsAdult().Should().BeTrue();
}
```

**3. Use Test Fixtures to Avoid Duplication**
```csharp
public class UserServiceTests
{
    private readonly UserService _service;
    private readonly Mock<IRepository> _mockRepository;

    public UserServiceTests()
    {
        // Common setup
        _mockRepository = new Mock<IRepository>();
        _service = new UserService(_mockRepository.Object);
    }
}
```

**4. Private Test Helpers**
```csharp
private User CreateTestUser(string name = "Test", string email = "test@example.com")
{
    return new User { Name = name, Email = email };
}
```

### ✗ Anti-Patterns to Avoid

**1. Testing Implementation Details**
```csharp
// ✗ Bad: Testing private methods
var result = user.PrivateCalculateAge();

// ✓ Good: Test observable behavior
var age = user.GetAge();
```

**2. Coupled Tests**
```csharp
// ✗ Bad: Tests depend on execution order
[Fact]
public void Step1_CreateUser() { }

[Fact]
public void Step2_UpdateUser() { } // Depends on Step1
```

**3. Over-Mocking**
```csharp
// ✗ Bad: Mocking simple dependencies
var mockString = new Mock<string>();

// ✓ Good: Test with real simple objects
var actualString = "test";
```

**4. Assertion Overload**
```csharp
// ✗ Bad: Too many assertions
[Fact]
public void Service_DoesEverything()
{
    // 20+ assertions on different concerns
}

// ✓ Good: Focused test
[Fact]
public void UpdateUser_WithValidData_UpdatesName()
{
    user.Update(new { Name = "New Name" });
    user.Name.Should().Be("New Name");
}
```

## Running Tests

### Command Line
```bash
# Run all tests
dotnet test

# Run with verbose output
dotnet test --verbosity detailed

# Run specific test class
dotnet test --filter "ClassName=UserServiceTests"

# Run specific test
dotnet test --filter "FullyQualifiedName~UserServiceTests.CreateUser"

# Generate code coverage report
dotnet test /p:CollectCoverage=true /p:CoverageFormat=opencover
```

### Test Explorer Integration
xUnit tests appear in Visual Studio Test Explorer and VS Code Test Explorer for easy navigation and execution.

## Code Coverage

### Configuration in .csproj
```xml
<PropertyGroup>
  <GenerateDocumentationFile>true</GenerateDocumentationFile>
</PropertyGroup>

<ItemGroup>
  <PackageReference Include="coverlet.collector" Version="6.0.0">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
</ItemGroup>
```

### Coverage Standards
- **Statements**: Minimum 75%, target 85%+
- **Branches**: Minimum 70%, target 80%+
- **Methods**: Minimum 80%, target 90%+
- **Lines**: Minimum 75%, target 85%+

---

## Related Instructions

- [C# Development Guidelines](./csharp.instructions.md)
- [.NET Architecture Patterns](./dotnet-architecture-good-practices.instructions.md)
