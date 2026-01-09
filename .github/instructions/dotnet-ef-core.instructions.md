---
description: 'Entity Framework Core best practices and design patterns'
applies_to: '**/*.cs (DbContext, migrations, queries), **/Migrations/**'
---

# Entity Framework Core Best Practices

Comprehensive standards and patterns for Entity Framework Core development, including context design, queries, migrations, and performance optimization.

## Core Principles

This content applies the following foundational principles:

- [Code Quality Goals](../core/principles/code-quality-goals.md) - Clear, maintainable data access
- [DRY (Don't Repeat Yourself)](../core/principles/dont-repeat-yourself.md) - Reusable query patterns

---

## DbContext Design

### Context Structure
```csharp
// ✅ Keep DbContext focused and cohesive
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }

    // DbSets for each entity
    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Delegate configuration to separate classes
        modelBuilder.ApplyConfigurationsFromAssembly(GetType().Assembly);
    }
}

// ✅ Delegate entity configuration to IEntityTypeConfiguration
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.HasKey(u => u.Id);
        builder.Property(u => u.Email).IsRequired().HasMaxLength(255);
        builder.Property(u => u.Name).IsRequired().HasMaxLength(100);

        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId);
    }
}

// ✅ Avoid mixing configuration concerns
// ❌ Don't put all configuration inline in OnModelCreating
```

### DbContextFactory Pattern
```csharp
// ✅ Use DbContextFactory for clean instances (especially in console apps)
public class UserService
{
    private readonly IDbContextFactory<ApplicationDbContext> _contextFactory;

    public UserService(IDbContextFactory<ApplicationDbContext> contextFactory)
    {
        _contextFactory = contextFactory;
    }

    public async Task<User> GetUserAsync(int id)
    {
        await using var context = _contextFactory.CreateDbContext();
        return await context.Users.FirstOrDefaultAsync(u => u.Id == id);
    }
}

// Configuration (Startup)
services.AddDbContextFactory<ApplicationDbContext>(options =>
    options.UseSqlServer("connection-string")
);
```

### DbContext Lifetime Management
```csharp
// ✅ Use Scoped lifetime for web applications (one per request)
services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer("connection-string"),
    ServiceLifetime.Scoped  // ← One per request/scope
);

// ✅ Use using statements for explicit lifetime control
public async Task ProcessOrderAsync(int orderId)
{
    await using (var context = new ApplicationDbContext(options))
    {
        var order = await context.Orders.FindAsync(orderId);
        // Work with order
    }  // ← Context disposed here
}

// ❌ Don't hold DbContext references too long
public class CachedUserService
{
    private ApplicationDbContext _context;  // ← WRONG! Lifetime unclear

    public void Initialize(ApplicationDbContext context)
    {
        _context = context;  // What's the lifetime?
    }
}
```

---

## Entity Design

### Entity Configuration with Data Annotations
```csharp
// ✅ Entity with appropriate configuration
public class User
{
    public int Id { get; set; }

    [Required]
    [StringLength(100)]
    public string Name { get; set; }

    [Required]
    [EmailAddress]
    [StringLength(255)]
    public string Email { get; set; }

    [Required]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public bool IsActive { get; set; } = true;

    // Navigation properties
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

// ✅ Or use fluent API for complex configuration
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(255)
            .HasConversion(e => e.ToLower(), e => e);  // Store lowercase

        builder.HasIndex(u => u.Email)
            .IsUnique();  // Unique constraint on email

        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);  // Cascade delete
    }
}
```

### Entity Relationships
```csharp
// ✅ One-to-Many relationship
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

public class Order
{
    public int Id { get; set; }
    public int UserId { get; set; }  // Foreign key
    public User User { get; set; }   // Navigation property
}

// ✅ Many-to-Many relationship (EF Core 5+)
public class Student
{
    public int Id { get; set; }
    public string Name { get; set; }
    public ICollection<Course> Courses { get; set; } = new List<Course>();
}

public class Course
{
    public int Id { get; set; }
    public string Title { get; set; }
    public ICollection<Student> Students { get; set; } = new List<Student>();
}

// Configure M2M in OnModelCreating
modelBuilder.Entity<Student>()
    .HasMany(s => s.Courses)
    .WithMany(c => c.Students);

// ✅ Owned entity types for value objects
public class Address
{
    public string Street { get; set; }
    public string City { get; set; }
    public string Country { get; set; }
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public Address Address { get; set; }  // Owned type
}

// Configure owned type
modelBuilder.Entity<User>()
    .OwnsOne(u => u.Address);  // Address stored in User table
```

---

## Querying Best Practices

### LINQ Queries
```csharp
// ✅ Use strongly-typed LINQ queries
public async Task<List<User>> GetActiveUsersAsync()
{
    return await _context.Users
        .Where(u => u.IsActive)
        .OrderBy(u => u.Name)
        .ToListAsync();
}

// ✅ Use Select for projection (fewer fields)
public async Task<List<UserDto>> GetActiveUsersAsync()
{
    return await _context.Users
        .Where(u => u.IsActive)
        .Select(u => new UserDto
        {
            Id = u.Id,
            Name = u.Name,
            Email = u.Email
        })
        .ToListAsync();
}

// ✅ Eager load related entities with Include
public async Task<User> GetUserWithOrdersAsync(int id)
{
    return await _context.Users
        .Include(u => u.Orders)
        .ThenInclude(o => o.Items)
        .FirstOrDefaultAsync(u => u.Id == id);
}

// ❌ Don't fetch all fields if you only need a few
public async Task<string> GetUserEmailAsync(int id)
{
    var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == id);
    return user?.Email;
}

// ✅ Use projection instead
public async Task<string> GetUserEmailAsync(int id)
{
    return await _context.Users
        .Where(u => u.Id == id)
        .Select(u => u.Email)
        .FirstOrDefaultAsync();
}
```

### AsNoTracking for Read-Only Queries
```csharp
// ✅ Use AsNoTracking for read-only queries (better performance)
public async Task<List<User>> GetAllUsersForDisplayAsync()
{
    return await _context.Users
        .AsNoTracking()  // No change tracking overhead
        .ToListAsync();
}

// ✅ Use AsNoTrackingWithIdentityResolution for queries with navigation properties
public async Task<List<User>> GetUsersWithOrdersAsync()
{
    return await _context.Users
        .AsNoTrackingWithIdentityResolution()  // Prevents duplicate objects
        .Include(u => u.Orders)
        .ToListAsync();
}

// ❌ Don't use AsNoTracking when you'll modify entities
public async Task<User> GetAndModifyUserAsync(int id)
{
    var user = await _context.Users
        .AsNoTracking()  // ← Changes won't be saved!
        .FirstOrDefaultAsync(u => u.Id == id);

    user.Name = "Updated";
    await _context.SaveChangesAsync();  // ← Changes lost
}
```

### Pagination
```csharp
// ✅ Implement proper pagination
public async Task<PagedResult<User>> GetUsersAsync(int pageNumber, int pageSize)
{
    var query = _context.Users.AsQueryable();

    var total = await query.CountAsync();

    var items = await query
        .OrderBy(u => u.Id)
        .Skip((pageNumber - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return new PagedResult<User>
    {
        Items = items,
        Total = total,
        PageNumber = pageNumber,
        PageSize = pageSize
    };
}

// ❌ Don't fetch all data and paginate in memory
public async Task<List<User>> GetAllUsersIncorrectlyAsync()
{
    var allUsers = await _context.Users.ToListAsync();  // Fetch all!
    return allUsers.Skip(100).Take(20).ToList();  // Then paginate in memory
}
```

### Compiled Queries
```csharp
// ✅ Use compiled queries for frequently executed queries
public static class UserQueries
{
    private static readonly Func<ApplicationDbContext, int, Task<User>>
        GetUserById = EF.CompileAsyncQuery(
            (ApplicationDbContext context, int id) =>
                context.Users
                    .Include(u => u.Orders)
                    .FirstOrDefault(u => u.Id == id)
        );

    public static Task<User> GetUserByIdAsync(
        ApplicationDbContext context, int id)
    {
        return GetUserById(context, id);
    }
}

// Usage
var user = await UserQueries.GetUserByIdAsync(_context, 1);
```

---

## Performance Optimization

### Avoiding N+1 Queries
```csharp
// ❌ N+1 Problem - 1 query for users + 1 per user for orders
var users = await _context.Users.ToListAsync();
foreach (var user in users)
{
    user.Orders = await _context.Orders
        .Where(o => o.UserId == user.Id)
        .ToListAsync();  // ← Query for each user!
}

// ✅ Solution 1: Eager load with Include
var users = await _context.Users
    .Include(u => u.Orders)
    .ToListAsync();

// ✅ Solution 2: Explicit eager load
var userIds = users.Select(u => u.Id);
var orders = await _context.Orders
    .Where(o => userIds.Contains(o.UserId))
    .ToListAsync();

var ordersLookup = orders.GroupBy(o => o.UserId).ToDictionary(g => g.Key);
foreach (var user in users)
{
    user.Orders = ordersLookup[user.Id].ToList();
}
```

### Batch Operations
```csharp
// ✅ Batch inserts for better performance
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

// ✅ Bulk delete with ExecuteDelete (EF Core 7+)
public async Task DeleteInactiveUsersAsync()
{
    await _context.Users
        .Where(u => !u.IsActive && u.LastLoginDate < DateTime.UtcNow.AddYears(-1))
        .ExecuteDeleteAsync();
}

// ✅ Bulk update with ExecuteUpdate (EF Core 7+)
public async Task ArchiveOldOrdersAsync()
{
    await _context.Orders
        .Where(o => o.CreatedAt < DateTime.UtcNow.AddYears(-1))
        .ExecuteUpdateAsync(s => s.SetProperty(o => o.IsArchived, true));
}
```

### Database Functions
```csharp
// ✅ Use database functions for complex operations
public async Task<List<UserStats>> GetUserStatisticsAsync()
{
    return await _context.UserStats
        .FromSqlInterpolated(@"
            SELECT
                UserId,
                COUNT(DISTINCT OrderId) as OrderCount,
                SUM(OrderTotal) as TotalSpent,
                AVG(OrderTotal) as AvgOrderValue
            FROM Orders
            GROUP BY UserId
        ")
        .ToListAsync();
}

// ✅ Map to stored procedures
public async Task<UserStatistics> GetUserStatsAsync(int userId)
{
    return await _context.UserStatistics
        .FromSqlInterpolated($"EXEC sp_GetUserStats {userId}")
        .AsAsyncEnumerable()
        .FirstOrDefaultAsync();
}
```

---

## Migrations

### Creating Migrations
```bash
# ✅ Add migration with descriptive name
dotnet ef migrations add AddUserPhoneNumber

# ✅ View SQL before applying
dotnet ef migrations script AddUserPhoneNumber

# ✅ Apply migration
dotnet ef database update

# ✅ List migrations
dotnet ef migrations list
```

### Migration Best Practices
```csharp
// ✅ Create focused, incremental migrations
public partial class AddUserPhoneNumber : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<string>(
            name: "PhoneNumber",
            table: "Users",
            type: "nvarchar(20)",
            nullable: true);

        migrationBuilder.CreateIndex(
            name: "IX_Users_PhoneNumber",
            table: "Users",
            column: "PhoneNumber",
            unique: true,
            filter: "[PhoneNumber] IS NOT NULL");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(
            name: "IX_Users_PhoneNumber",
            table: "Users");

        migrationBuilder.DropColumn(
            name: "PhoneNumber",
            table: "Users");
    }
}

// ✅ Add data seeding in migrations if needed
public partial class SeedUserRoles : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.InsertData(
            table: "UserRoles",
            columns: new[] { "Id", "Name" },
            values: new object[,]
            {
                { 1, "Admin" },
                { 2, "User" },
                { 3, "Guest" }
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DeleteData(
            table: "UserRoles",
            keyColumn: "Id",
            keyValue: 1);
        // ... etc
    }
}

// ✅ Verify migration SQL scripts before applying to production
dotnet ef migrations script --from <prev-migration> --to <new-migration> --output script.sql
```

---

## Testing with EF Core

### Testing with In-Memory Database
```csharp
[TestMethod]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var options = new DbContextOptionsBuilder<ApplicationDbContext>()
        .UseInMemoryDatabase(databaseName: "test-db")
        .Options;

    using (var context = new ApplicationDbContext(options))
    {
        context.Users.Add(new User { Id = 1, Name = "John", Email = "john@test.com" });
        await context.SaveChangesAsync();
    }

    // Act
    using (var context = new ApplicationDbContext(options))
    {
        var userService = new UserService(context);
        var user = await userService.GetUserAsync(1);

        // Assert
        Assert.IsNotNull(user);
        Assert.AreEqual("John", user.Name);
    }
}

// ✅ Use SQLite in-memory for closer-to-production testing
var options = new DbContextOptionsBuilder<ApplicationDbContext>()
    .UseSqlite("Data Source=:memory:")
    .Options;
```

### Mocking DbContext
```csharp
// ✅ Mock DbSet for unit tests
var mockUsers = new Mock<DbSet<User>>();
mockUsers.Setup(d => d.FindAsync(1))
    .ReturnsAsync(new User { Id = 1, Name = "John" });

var mockContext = new Mock<ApplicationDbContext>();
mockContext.Setup(c => c.Users).Returns(mockUsers.Object);

var service = new UserService(mockContext.Object);
var user = await service.GetUserAsync(1);

Assert.AreEqual("John", user.Name);
```

---

## Change Tracking and Saving

### Change Tracking Strategies
```csharp
// ✅ Use appropriate change tracking for your scenario
var user = await _context.Users.FindAsync(1);  // Tracked
user.Name = "Updated";

var userNoTrack = await _context.Users
    .AsNoTracking()
    .FirstAsync(u => u.Id == 1);  // Not tracked

// Reattach if needed
_context.Users.Update(userNoTrack);
userNoTrack.Name = "Updated Again";
await _context.SaveChangesAsync();

// ✅ Batch SaveChanges calls
foreach (var user in users)
{
    user.LastLoginDate = DateTime.UtcNow;
}
await _context.SaveChangesAsync();  // One save for all changes
```

### Transactions
```csharp
// ✅ Use transactions for multiple related operations
public async Task TransferFundsAsync(int fromUserId, int toUserId, decimal amount)
{
    using var transaction = await _context.Database.BeginTransactionAsync();

    try
    {
        var fromUser = await _context.Users.FindAsync(fromUserId);
        var toUser = await _context.Users.FindAsync(toUserId);

        fromUser.Balance -= amount;
        toUser.Balance += amount;

        await _context.SaveChangesAsync();
        await transaction.CommitAsync();
    }
    catch
    {
        await transaction.RollbackAsync();
        throw;
    }
}
```

---

## Security Considerations

### SQL Injection Prevention
```csharp
// ✅ Use parameterized queries (automatic with LINQ)
var users = await _context.Users
    .Where(u => u.Email == userInput)  // Parameterized automatically
    .ToListAsync();

// ✅ If using raw SQL, still use parameters
var users = await _context.Users
    .FromSqlInterpolated($"SELECT * FROM Users WHERE Email = {userInput}")
    .ToListAsync();

// ❌ Never concatenate user input
var users = await _context.Users
    .FromSqlRaw($"SELECT * FROM Users WHERE Email = '{userInput}'")
    .ToListAsync();  // Vulnerable to SQL injection!
```

### Data Encryption
```csharp
// ✅ Encrypt sensitive data
public class User
{
    public int Id { get; set; }

    [Encrypted]  // Custom attribute
    public string SocialSecurityNumber { get; set; }

    [Encrypted]
    public string CreditCardNumber { get; set; }
}

// Configuration with value converters
modelBuilder.Entity<User>()
    .Property(u => u.SocialSecurityNumber)
    .HasConversion(new EncryptedConverter());
```

---

## Best Practices Checklist

- [ ] DbContext focused and cohesive (one responsibility)
- [ ] Entity configuration separated into IEntityTypeConfiguration classes
- [ ] Appropriate DbContext lifetime (Scoped for web, Factory for console)
- [ ] Queries use AsNoTracking when appropriate
- [ ] Related entities eagerly loaded to avoid N+1
- [ ] Pagination implemented for large result sets
- [ ] Select projection used to fetch only needed fields
- [ ] Batch operations for bulk inserts/updates
- [ ] Migrations created frequently with descriptive names
- [ ] Migrations tested before applying to production
- [ ] Transactions used for multi-step operations
- [ ] Parameterized queries prevent SQL injection
- [ ] Change tracking appropriate for scenario
- [ ] SaveChanges batched efficiently
- [ ] Tests use in-memory database or SQLite

---

## Related Documentation

- `dotnet.instructions.md` - General .NET best practices
- `dotnet-async.instructions.md` - Async patterns in EF Core
- `dotnet-unit-testing.instructions.md` - Testing data access
