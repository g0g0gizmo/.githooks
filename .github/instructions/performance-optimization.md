# Performance Optimization

## Overview

Performance optimization ensures that software systems respond quickly to user interactions and handle computational workloads efficiently. This principle balances feature richness with execution speed, memory efficiency, and resource utilization.

Performance Optimization guides developers to:
- **Measure First**: Profile before optimizing
- **Optimize Bottlenecks**: Fix actual problems, not presumed ones
- **Cache Strategically**: Reduce redundant computation
- **Async Patterns**: Don't block on I/O operations
- **Database Efficiency**: Query optimization and indexing
- **Memory Management**: Avoid leaks and excessive allocations
- **Batch Operations**: Reduce per-item overhead
- **Algorithm Selection**: Big-O complexity matters

## Core Concepts

### 1. Profiling & Measurement

Never optimize without data. Profile first to identify actual bottlenecks.

```python
# Good: Use profiling tools to measure
import cProfile
import pstats

def slow_function():
    result = []
    for i in range(1000000):
        result.append(i * 2)
    return result

profiler = cProfile.Profile()
profiler.enable()

slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Print top 10
```

**Key Metrics**:
- **Response Time**: How fast users see results
- **Throughput**: Requests processed per second
- **CPU Usage**: Processor utilization percentage
- **Memory Usage**: RAM consumption
- **I/O Wait**: Time blocked on disk/network

### 2. Caching Strategies

Cache reduces repeated computation at the cost of storage and invalidation complexity.

#### HTTP Caching
```csharp
// Good: Configure HTTP cache headers
public class CacheController : ControllerBase {
    [HttpGet("data/{id}")]
    public IActionResult GetData(int id) {
        var data = _service.GetData(id);

        Response.Headers["Cache-Control"] = "public, max-age=3600";  // 1 hour
        Response.Headers["ETag"] = GenerateETag(data);

        return Ok(data);
    }
}
```

#### In-Memory Caching
```csharp
// Good: Cache expensive computations
public class ProductService {
    private readonly IMemoryCache _cache;

    public Product GetProduct(int id) {
        const string cacheKey = $"product-{id}";

        if (!_cache.TryGetValue(cacheKey, out Product product)) {
            // Cache miss: fetch from database
            product = _repository.GetProduct(id);

            var cacheOptions = new MemoryCacheEntryOptions()
                .SetAbsoluteExpiration(TimeSpan.FromMinutes(30));

            _cache.Set(cacheKey, product, cacheOptions);
        }

        return product;
    }
}
```

#### Distributed Caching (Redis)
```python
# Good: Cache across distributed systems
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_user(user_id):
    cache_key = f"user:{user_id}"

    # Try cache first
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss: fetch and cache
    user = database.fetch_user(user_id)
    cache.setex(cache_key, 3600, json.dumps(user))  # 1 hour TTL

    return user
```

**Cache Invalidation**:
```typescript
// Good: Invalidate cache when data changes
async updateUser(userId: string, updates: Partial<User>): Promise<User> {
    const user = await this.repo.update(userId, updates);

    // Invalidate cache for this user
    await this.cache.del(`user:${userId}`);

    // Also invalidate related queries
    await this.cache.del(`user-posts:${userId}`);

    return user;
}
```

### 3. Async & Non-Blocking I/O

Never block threads on I/O operations. Use async patterns to handle multiple requests efficiently.

```csharp
// ✗ Bad: Synchronous I/O blocks thread
public ActionResult GetUserData(int userId) {
    var user = _db.Users.FirstOrDefault(u => u.Id == userId);  // Blocking
    var posts = _db.Posts.Where(p => p.UserId == userId).ToList();  // Blocking
    return Ok(new { user, posts });
}

// ✓ Good: Async I/O frees threads
public async Task<ActionResult> GetUserData(int userId) {
    var user = await _db.Users.FirstOrDefaultAsync(u => u.Id == userId);
    var posts = await _db.Posts.Where(p => p.UserId == userId).ToListAsync();
    return Ok(new { user, posts });
}

// ✓ Good: Parallel async operations
public async Task<ActionResult> GetUserData(int userId) {
    var userTask = _db.Users.FirstOrDefaultAsync(u => u.Id == userId);
    var postsTask = _db.Posts.Where(p => p.UserId == userId).ToListAsync();

    await Task.WhenAll(userTask, postsTask);

    return Ok(new { user: userTask.Result, posts: postsTask.Result });
}
```

### 4. Database Optimization

Database queries often account for 70%+ of performance issues.

#### Query Optimization
```sql
-- ✗ Bad: N+1 queries problem
SELECT * FROM Orders;  -- 1st query
-- Then loop and execute: SELECT * FROM OrderItems WHERE OrderId = {id}  -- N queries

-- ✓ Good: Single query with JOIN
SELECT o.*, oi.*
FROM Orders o
LEFT JOIN OrderItems oi ON o.Id = oi.OrderId
WHERE o.CustomerId = 123;

-- ✓ Good: Include in ORM
var orders = await _context.Orders
    .Where(o => o.CustomerId == 123)
    .Include(o => o.Items)  // Avoid N+1
    .ToListAsync();
```

#### Indexing
```sql
-- Identify missing indexes
EXPLAIN SELECT * FROM Users WHERE Email = 'user@example.com';

-- Create indexes on frequently queried columns
CREATE INDEX idx_users_email ON Users(Email);
CREATE INDEX idx_posts_user_created ON Posts(UserId, CreatedDate DESC);

-- Composite indexes for filtering + sorting
CREATE INDEX idx_orders_customer_date ON Orders(CustomerId, OrderDate DESC);
```

#### Connection Pooling
```csharp
// Good: Database connection pooling
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.MaxPoolSize(100);  // Limit connections
        sqlOptions.EnableRetryOnFailure();
    }));
```

### 5. Algorithm Selection & Complexity

Choose algorithms appropriate for expected data sizes.

```python
# ✗ Bad: O(n²) algorithm for large lists
def find_duplicates_slow(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):  # Quadratic complexity
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates

# ✓ Good: O(n) algorithm using hash set
def find_duplicates_fast(items):
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)
```

**Complexity Guidelines**:
- O(1): Constant - Best for all sizes
- O(log n): Logarithmic - Acceptable for large datasets
- O(n): Linear - Ok for large datasets
- O(n log n): Linearithmic - Reasonable for sorting
- O(n²): Quadratic - Avoid for large datasets
- O(2ⁿ): Exponential - Only for small inputs

### 6. Memory Efficiency

```csharp
// ✗ Bad: Creating unnecessary allocations
string result = "";
for (int i = 0; i < 10000; i++) {
    result += i.ToString();  // Creates new string each iteration
}

// ✓ Good: Use StringBuilder
var result = new StringBuilder();
for (int i = 0; i < 10000; i++) {
    result.Append(i);  // Efficient appending
}
return result.ToString();
```

```python
# ✗ Bad: Loading entire file into memory
with open('large_file.txt') as f:
    lines = f.readlines()  # Entire file loaded
    for line in lines:
        process(line)

# ✓ Good: Streaming/generator pattern
with open('large_file.txt') as f:
    for line in f:  # Processed line by line
        process(line)
```

### 7. Batch Operations

```java
// ✗ Bad: Individual inserts (many database round-trips)
for (User user : users) {
    userRepository.save(user);  // N database calls
}

// ✓ Good: Batch insert (single database call)
userRepository.saveAll(users);  // Single batch call

// ✓ Good: Bulk API for large batches
try (BulkProcessor bulk = BulkProcessor.builder(client)
    .setBulkActions(5000)
    .setConcurrentRequests(10)
    .build()) {
    for (User user : users) {
        bulk.add(new IndexRequest().source(user));
    }
}
```

### 8. Frontend Performance

```javascript
// Good: Lazy load images
<img src="placeholder.jpg"
     data-src="actual-image.jpg"
     loading="lazy"
     onload="this.src=this.dataset.src" />

// Good: Code splitting in SPA
const Dashboard = React.lazy(() => import('./Dashboard'));

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>

// Good: Debounce expensive operations
const debouncedSearch = debounce((query) => {
    searchAPI(query);
}, 300);  // Wait 300ms after user stops typing

<input onChange={(e) => debouncedSearch(e.target.value)} />
```

## Application Checklist

- [ ] Performance requirements defined and measured
- [ ] Profiling performed to identify bottlenecks
- [ ] Database queries optimized (no N+1 problems)
- [ ] Indexes created on frequently queried columns
- [ ] Async patterns used for I/O operations
- [ ] Caching implemented for expensive computations
- [ ] Connection pooling configured
- [ ] Memory leaks tested and prevented
- [ ] Algorithm complexity appropriate for data size
- [ ] Batch operations used instead of individual inserts
- [ ] Code splitting/lazy loading implemented (frontend)
- [ ] Bundle size optimized (frontend)
- [ ] HTTP caching headers configured
- [ ] Monitoring/alerting for performance degradation
- [ ] Load testing performed under expected traffic
- [ ] Autoscaling configured for peak demand

## Related Principles

- [Code Quality Goals](../../.github/copilot/code-quality-goals.md) - Performance is a quality dimension
- [Problem Decomposition](../../.github/copilot/problem-decomposition.md) - Break complex optimization tasks
- [DRY Principle](../../.github/copilot/dry-principle.md) - Avoid redundant computation through caching

## Anti-Patterns

**1. Premature Optimization**
```python
# ✗ Bad: Optimizing without measurement
def calculate_sum(numbers):
    # Overly complex micro-optimization
    return sum(numbers[i] for i in range(len(numbers)))

# ✓ Good: Simple and clear, profile if needed
def calculate_sum(numbers):
    return sum(numbers)
```

**2. Over-Caching**
```csharp
// ✗ Bad: Caching everything, creating memory pressure
for (int i = 0; i < 1000000; i++) {
    _cache.Set($"item-{i}", ExpensiveComputation(i));  // Memory explosion
}

// ✓ Good: Cache strategically with TTLs
_cache.Set($"item-{i}", result, TimeSpan.FromMinutes(30));
```

## Performance Testing Tools

- **Profilers**: New Relic, Datadog, Jaeger
- **Load Testing**: Apache JMeter, k6, Locust
- **Database Analysis**: EXPLAIN PLAN, SQL Server Execution Plans
- **Frontend**: Lighthouse, WebPageTest, Chrome DevTools
- **APM**: Application Performance Monitoring tools
