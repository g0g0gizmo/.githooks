---
description: 'C# and .NET best practices standards for code quality, architecture, and design patterns'
applies_to: '**/*.cs, **/*.csproj, **/*.sln'
---

# .NET/C# Best Practices

Comprehensive best practices and coding standards for .NET and C# development, covering architecture, design patterns, code quality, and language features.

## Core Principles

This content applies the following foundational principles:

- [Code Quality Goals](../core/principles/code-quality-goals.md) - Maintain high standards for clarity and quality
- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Promote reusability and efficiency
- [SOLID Principles](../core/principles/principles-solid.md) - Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion

---

## Naming Conventions

### Classes and Types
```csharp
// ✅ Use PascalCase for class names
public class UserService { }
public interface IUserRepository { }
public enum UserRole { }
public record UserData { }

// ❌ Don't use underscores or camelCase for type names
public class user_service { }
public class userService { }
```

### Methods and Properties
```csharp
// ✅ Use PascalCase for public members
public void ProcessOrder() { }
public string UserName { get; set; }
public bool IsActive { get; set; }

// ❌ Don't use camelCase for public members
public void processOrder() { }
public string userName { get; set; }
```

### Private Fields and Local Variables
```csharp
// ✅ Use camelCase for local variables and private fields
private string _userName;
public UserService(string userName)
{
    var localVariable = userName;
}

// Modern C# - use _field for backing fields
private string _userEmail;
public string UserEmail => _userEmail;

// Or use records with automatic properties
public record UserInfo(string Name, string Email);
```

### Constants
```csharp
// ✅ Use UPPER_SNAKE_CASE for constants
private const string DEFAULT_USER_NAME = "Guest";
private const int MAX_RETRY_COUNT = 3;

// ❌ Don't use PascalCase for constants (it looks like a class)
private const string DefaultUserName = "Guest"; // Confusing!
```

### Async Methods
```csharp
// ✅ Use Async suffix for async methods
public async Task<User> GetUserAsync(int id) { }
public async Task SaveUserAsync(User user) { }

// ❌ Don't omit Async suffix
public async Task GetUser(int id) { }
```

### Interfaces
```csharp
// ✅ Always prefix interfaces with 'I'
public interface IUserRepository { }
public interface INotificationService { }

// ❌ Don't use interface names without 'I'
public interface UserRepository { }
```

### Properties for Booleans
```csharp
// ✅ Use affirmative form (Is, Has, Can, Should)
public bool IsActive { get; set; }
public bool HasPermission { get; set; }
public bool CanDelete { get; set; }

// ❌ Avoid negative forms
public bool IsNotActive { get; set; }
public bool NoPermission { get; set; }
```

---

## Project and File Organization

### Namespace Structure
```
Core
  ├── Services          // Business logic services
  ├── Repositories      // Data access abstractions
  ├── Models           // Domain entities
  └── Exceptions       // Custom exceptions

MyApp
  ├── ConsoleApp       // Console applications
  ├── WebApp           // Web applications
  └── Services         // App-specific services

Infrastructure
  ├── Persistence      // EF Core contexts and migrations
  ├── Http             // HTTP client implementations
  └── Caching          // Caching implementations
```

### Namespace Naming
```csharp
// ✅ Clear, hierarchical namespaces
namespace MyCompany.ProductName.Core.Services { }
namespace MyCompany.ProductName.Infrastructure.Persistence { }

// ❌ Don't use overly deep or single-letter namespaces
namespace M.P.C.S { }
namespace MyCompany.ProductName.Core.Services.Implementations.Utils.Helpers { }
```

---

## Dependency Injection

### Constructor Injection with Null Checks
```csharp
// ✅ Use primary constructor syntax (C# 12+)
public class UserService(IUserRepository repository, ILogger<UserService> logger)
{
    private readonly IUserRepository _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    private readonly ILogger<UserService> _logger = logger ?? throw new ArgumentNullException(nameof(logger));

    public async Task<User> GetUserAsync(int id)
    {
        return await _repository.GetByIdAsync(id);
    }
}

// ✅ Or traditional syntax with guard clauses
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly ILogger<UserService> _logger;

    public UserService(IUserRepository repository, ILogger<UserService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
}
```

### Service Lifetimes
```csharp
// Register services with appropriate lifetimes
services.AddSingleton<IGlobalConfig, GlobalConfig>();        // Single instance for app lifetime
services.AddScoped<IUserService, UserService>();             // One per request/scope
services.AddTransient<IEmailSender, EmailSender>();          // New instance each time

// Guidelines:
// - Singleton: Stateless, thread-safe, shared config
// - Scoped: Request-specific (DbContext, repositories)
// - Transient: Lightweight, stateless operations
```

---

## Design Patterns

### Factory Pattern
```csharp
// ✅ Use Factory for complex object creation
public interface IPaymentProcessorFactory
{
    IPaymentProcessor CreateProcessor(PaymentMethod method);
}

public class PaymentProcessorFactory : IPaymentProcessorFactory
{
    public IPaymentProcessor CreateProcessor(PaymentMethod method)
    {
        return method switch
        {
            PaymentMethod.CreditCard => new CreditCardProcessor(),
            PaymentMethod.PayPal => new PayPalProcessor(),
            PaymentMethod.Bank => new BankTransferProcessor(),
            _ => throw new InvalidOperationException($"Unknown method: {method}")
        };
    }
}
```

### Command Handler Pattern
```csharp
// ✅ Generic command handler base class
public abstract class CommandHandler<TCommand>
{
    public virtual async Task HandleAsync(TCommand command)
    {
        ValidateCommand(command);
        await ExecuteAsync(command);
    }

    protected abstract void ValidateCommand(TCommand command);
    protected abstract Task ExecuteAsync(TCommand command);
}

// Usage
public class CreateUserCommand
{
    public string Name { get; set; }
    public string Email { get; set; }
}

public class CreateUserCommandHandler : CommandHandler<CreateUserCommand>
{
    private readonly IUserRepository _repository;

    public CreateUserCommandHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    protected override void ValidateCommand(CreateUserCommand command)
    {
        if (string.IsNullOrWhiteSpace(command.Name))
            throw new InvalidOperationException("Name is required");
    }

    protected override async Task ExecuteAsync(CreateUserCommand command)
    {
        var user = new User { Name = command.Name, Email = command.Email };
        await _repository.AddAsync(user);
    }
}
```

### Repository Pattern
```csharp
// ✅ Interface-based repository with generic base
public interface IRepository<T> where T : class
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}

public abstract class Repository<T> : IRepository<T> where T : class
{
    protected readonly DbContext _context;

    public Repository(DbContext context)
    {
        _context = context ?? throw new ArgumentNullException(nameof(context));
    }

    public virtual async Task<T> GetByIdAsync(int id)
    {
        return await _context.Set<T>().FindAsync(id);
    }

    // ... other methods
}
```

---

## Code Quality Standards

### Method Size and Complexity
```csharp
// ✅ Small, focused methods (8-12 lines ideal)
public bool ValidateEmail(string email)
{
    if (string.IsNullOrWhiteSpace(email))
        return false;

    var emailPattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$";
    return Regex.IsMatch(email, emailPattern);
}

// ❌ Large, complex methods (hard to test, maintain)
public bool ProcessOrder(Order order) // 100+ lines of logic
{
    // ... too much responsibility
}
```

### Cohesion and Single Responsibility
```csharp
// ✅ Single responsibility - repository only handles persistence
public class UserRepository : IUserRepository
{
    private readonly DbContext _context;

    public async Task<User> GetByIdAsync(int id) => await _context.Users.FindAsync(id);
    public async Task AddAsync(User user) => await _context.Users.AddAsync(user);
}

// ✅ Separate service handles business logic
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly IEmailSender _emailSender;

    public async Task RegisterUserAsync(UserRegistration registration)
    {
        var user = new User { Name = registration.Name, Email = registration.Email };
        await _repository.AddAsync(user);
        await _emailSender.SendWelcomeEmailAsync(registration.Email);
    }
}
```

### Avoiding Code Duplication (DRY)
```csharp
// ❌ Duplicate code - violates DRY
public class UserService
{
    public User GetActiveUser(int id)
    {
        var user = _repository.GetById(id);
        if (user == null || !user.IsActive)
            throw new InvalidOperationException("User not found or inactive");
        return user;
    }

    public async Task<User> UpdateActiveUserAsync(int id, UserUpdate update)
    {
        var user = _repository.GetById(id);
        if (user == null || !user.IsActive)
            throw new InvalidOperationException("User not found or inactive");
        // ... update logic
    }
}

// ✅ Extract common logic
public class UserService
{
    private User GetActiveUserOrThrow(int id)
    {
        var user = _repository.GetById(id);
        if (user == null || !user.IsActive)
            throw new InvalidOperationException("User not found or inactive");
        return user;
    }

    public User GetActiveUser(int id) => GetActiveUserOrThrow(id);

    public async Task<User> UpdateActiveUserAsync(int id, UserUpdate update)
    {
        var user = GetActiveUserOrThrow(id);
        // ... update logic
    }
}
```

---

## SOLID Principles

### Single Responsibility Principle
Each class should have one reason to change:

```csharp
// ❌ Violates SRP - class has multiple reasons to change
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }

    public void SendWelcomeEmail() { }        // Reason 1: Email sending changes
    public void ValidateEmail() { }            // Reason 2: Email validation changes
    public void SaveToDatabase() { }           // Reason 3: Persistence changes
}

// ✅ Follows SRP - each class has single reason to change
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }
}

public class EmailValidator
{
    public bool IsValid(string email) => /* validation logic */;
}

public class EmailService
{
    public async Task SendWelcomeEmailAsync(User user) { }
}

public class UserRepository
{
    public async Task SaveAsync(User user) { }
}
```

### Open/Closed Principle
Open for extension, closed for modification:

```csharp
// ✅ Extensible design - add new payment methods without modifying existing code
public interface IPaymentProcessor
{
    Task ProcessPaymentAsync(decimal amount);
}

public class CreditCardProcessor : IPaymentProcessor
{
    public async Task ProcessPaymentAsync(decimal amount) { }
}

public class PayPalProcessor : IPaymentProcessor
{
    public async Task ProcessPaymentAsync(decimal amount) { }
}

public class OrderService
{
    private readonly IPaymentProcessor _paymentProcessor;

    public async Task ProcessOrderAsync(Order order)
    {
        await _paymentProcessor.ProcessPaymentAsync(order.Total);
    }
}
```

### Interface Segregation Principle
Clients should not depend on interfaces they don't use:

```csharp
// ❌ Fat interface - forces implementing unused methods
public interface IService
{
    Task<User> GetUserAsync(int id);
    Task<IEnumerable<Order>> GetOrdersAsync(int userId);
    Task SendEmailAsync(string to, string body);
    Task GenerateReportAsync();
}

// ✅ Segregated interfaces - clients depend only on what they need
public interface IUserRepository
{
    Task<User> GetUserAsync(int id);
}

public interface IOrderRepository
{
    Task<IEnumerable<Order>> GetOrdersAsync(int userId);
}

public interface IEmailService
{
    Task SendEmailAsync(string to, string body);
}

public interface IReportGenerator
{
    Task GenerateReportAsync();
}
```

---

## Error Handling and Validation

### Input Validation
```csharp
// ✅ Validate inputs early, use ArgumentException family
public class UserService
{
    public async Task<User> CreateUserAsync(string name, string email)
    {
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Name cannot be empty", nameof(name));

        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email cannot be empty", nameof(email));

        if (!IsValidEmail(email))
            throw new ArgumentException("Email format is invalid", nameof(email));

        // ... proceed with creation
    }

    private bool IsValidEmail(string email)
    {
        var emailPattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$";
        return Regex.IsMatch(email, emailPattern);
    }
}

// ✅ Use data annotations for model validation
public class UserRegistration
{
    [Required(ErrorMessage = "Name is required")]
    [StringLength(100, MinimumLength = 3)]
    public string Name { get; set; }

    [Required]
    [EmailAddress]
    public string Email { get; set; }

    [MinLength(8, ErrorMessage = "Password must be at least 8 characters")]
    public string Password { get; set; }
}
```

### Exception Handling
```csharp
// ✅ Throw specific exceptions with descriptive messages
public async Task<User> GetUserAsync(int id)
{
    if (id <= 0)
        throw new ArgumentException("User ID must be positive", nameof(id));

    var user = await _repository.GetByIdAsync(id);
    if (user == null)
        throw new KeyNotFoundException($"User with ID {id} not found");

    return user;
}

// ✅ Log exceptions with context
public async Task ProcessOrderAsync(int orderId)
{
    try
    {
        var order = await _repository.GetOrderAsync(orderId);
        await _paymentService.ProcessAsync(order);
    }
    catch (InvalidOperationException ex)
    {
        _logger.LogError(ex, "Failed to process order {OrderId}", orderId);
        throw;
    }
}
```

---

## Async/Await Patterns

See `dotnet-async.instructions.md` for comprehensive async programming standards.

Quick reference:
```csharp
// ✅ Always use async/await for I/O operations
public async Task<User> GetUserAsync(int id)
{
    return await _repository.GetByIdAsync(id);
}

// ✅ Use Task.WhenAll for parallel operations
var users = await Task.WhenAll(
    _repository.GetUserAsync(1),
    _repository.GetUserAsync(2),
    _repository.GetUserAsync(3)
);

// ❌ Never use .Result or .Wait() - causes deadlocks
var user = _repository.GetUserAsync(id).Result; // WRONG!
```

---

## Entity Framework Core

See `dotnet-ef-core.instructions.md` for comprehensive EF Core best practices.

Quick reference:
```csharp
// ✅ Use DbContextFactory for clean instances
var context = _factory.CreateDbContext();

// ✅ Use AsNoTracking for read-only queries
var users = await _context.Users.AsNoTracking().ToListAsync();

// ✅ Eager load related entities
var users = await _context.Users
    .Include(u => u.Orders)
    .ThenInclude(o => o.Items)
    .ToListAsync();

// ✅ Use projection for specific fields
var userEmails = await _context.Users
    .Select(u => new { u.Id, u.Email })
    .ToListAsync();
```

---

## Documentation Standards

See `dotnet-documentation.instructions.md` for comprehensive XML documentation standards.

Quick reference:
```csharp
/// <summary>
/// Retrieves a user by their unique identifier.
/// </summary>
/// <param name="id">The user's unique identifier.</param>
/// <returns>The user if found; otherwise, <see langword="null"/>.</returns>
/// <exception cref="ArgumentException">Thrown when <paramref name="id"/> is less than or equal to zero.</exception>
public async Task<User> GetUserAsync(int id)
{
    if (id <= 0)
        throw new ArgumentException("User ID must be positive", nameof(id));

    return await _repository.GetByIdAsync(id);
}
```

---

## Performance Considerations

### Caching
```csharp
// ✅ Cache expensive operations
public class UserService
{
    private readonly IDistributedCache _cache;
    private readonly IUserRepository _repository;
    private const string CACHE_KEY = "user_{0}";
    private const int CACHE_DURATION_MINUTES = 5;

    public async Task<User> GetUserAsync(int id)
    {
        var cacheKey = string.Format(CACHE_KEY, id);
        var cachedUser = await _cache.GetAsync<User>(cacheKey);

        if (cachedUser != null)
            return cachedUser;

        var user = await _repository.GetByIdAsync(id);
        await _cache.SetAsync(cacheKey, user, TimeSpan.FromMinutes(CACHE_DURATION_MINUTES));

        return user;
    }
}
```

### Database Optimization
```csharp
// ✅ Batch operations
public async Task ImportUsersAsync(List<User> users)
{
    const int batchSize = 1000;
    for (int i = 0; i < users.Count; i += batchSize)
    {
        var batch = users.Skip(i).Take(batchSize);
        await _context.Users.AddRangeAsync(batch);
        await _context.SaveChangesAsync();
    }
}

// ✅ Use pagination for large datasets
public async Task<PagedResult<User>> GetUsersAsync(int page, int pageSize)
{
    var total = await _context.Users.CountAsync();
    var users = await _context.Users
        .OrderBy(u => u.Id)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return new PagedResult<User> { Items = users, Total = total };
}
```

---

## Security Standards

### Input Validation
```csharp
// ✅ Always validate and sanitize user input
public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
{
    if (string.IsNullOrWhiteSpace(request.CustomerName))
        throw new ArgumentException("Customer name is required");

    // Validate numeric ranges
    if (request.Amount <= 0 || request.Amount > decimal.MaxValue)
        throw new ArgumentException("Invalid amount");

    // Continue with order creation...
}
```

### Database Security
```csharp
// ✅ Use parameterized queries (automatic with Entity Framework LINQ)
var users = await _context.Users
    .Where(u => u.Email == email)  // Parameter automatically
    .ToListAsync();

// ❌ Never use string concatenation in queries
// var users = _context.Users.FromSqlInterpolated($"SELECT * FROM Users WHERE Email = '{email}'");
```

### Secrets Management
```csharp
// ✅ Use configuration and dependency injection
public class EmailService
{
    private readonly string _apiKey;

    public EmailService(IConfiguration configuration)
    {
        _apiKey = configuration["EmailService:ApiKey"];
    }

    // Never hardcode secrets, use appsettings.json or environment variables
}
```

---

## Testing Considerations

- Keep code testable: small methods, loose coupling, dependency injection
- Test behavior, not implementation details
- Mock external dependencies (database, API, file system)
- Use test builders for complex test data
- Achieve 80% minimum code coverage, 100% for critical paths

See `dotnet-unit-testing.instructions.md` for comprehensive testing standards.

---

## Modern C# Features

### Records (C# 9+)
```csharp
// ✅ Use records for data transfer objects and immutable data
public record CreateUserRequest(string Name, string Email);

public record UserDto(int Id, string Name, string Email, DateTime CreatedAt);

// ✅ Records provide value equality and immutability
var dto1 = new UserDto(1, "John", "john@example.com", DateTime.Now);
var dto2 = new UserDto(1, "John", "john@example.com", DateTime.Now);
var areEqual = dto1 == dto2;  // true - value equality
```

### Primary Constructors (C# 12+)
```csharp
// ✅ Use primary constructors for cleaner dependency injection
public class UserService(IUserRepository repository, ILogger<UserService> logger)
{
    public async Task<User> GetUserAsync(int id)
    {
        return await repository.GetByIdAsync(id);
    }
}
```

### Switch Expressions
```csharp
// ✅ Use switch expressions for cleaner branching
public string GetUserStatus(User user) => user.Status switch
{
    UserStatus.Active => "Active",
    UserStatus.Inactive => "Inactive",
    UserStatus.Suspended => "Suspended",
    _ => "Unknown"
};
```

### Null Coalescing and Pattern Matching
```csharp
// ✅ Use modern null handling
public string GetDisplayName(User user)
{
    return user?.FullName ?? user?.Email ?? "Unknown User";
}

// ✅ Use pattern matching
public string GetUserInfo(User user) => user switch
{
    null => "User not found",
    { IsActive: false } => "User is inactive",
    { IsAdmin: true } => "Administrator: " + user.Name,
    _ => "User: " + user.Name
};
```

---

## Code Organization Checklist

- [ ] Namespaces organized hierarchically by feature
- [ ] Classes follow Single Responsibility Principle
- [ ] Constructor dependencies injected, validated
- [ ] Appropriate service lifetimes selected
- [ ] Exceptions specific and descriptive
- [ ] Async methods properly named and implemented
- [ ] Code is DRY (no duplication)
- [ ] SOLID principles applied
- [ ] Methods are small and focused
- [ ] XML documentation complete for public APIs
- [ ] Input validation at boundaries
- [ ] Tests cover core functionality and edge cases

---

## Related Documentation

- `dotnet-async.instructions.md` - Async programming best practices
- `dotnet-ef-core.instructions.md` - Entity Framework Core standards
- `dotnet-documentation.instructions.md` - XML documentation standards
- `dotnet-unit-testing.instructions.md` - Testing frameworks and patterns
- `dotnet-aspnet-api.instructions.md` - ASP.NET Core API standards
- `dotnet-design-patterns.instructions.md` - Design pattern implementations
