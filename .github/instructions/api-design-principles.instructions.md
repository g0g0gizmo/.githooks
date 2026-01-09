# API Design Principles

## Overview

Well-designed APIs are the backbone of modern distributed systems. This principle ensures that APIs are intuitive, consistent, maintainable, and future-proof. Good API design reduces client development effort, minimizes integration costs, and prevents versioning nightmares.

API Design Principles guide developers to:

- **Consistency**: Predictable patterns across all endpoints
- **Clarity**: Obvious intent from resource URIs and methods
- **Compatibility**: Support evolution without breaking clients
- **Resilience**: Handle failures gracefully
- **Documentation**: Clear contracts for clients
- **Standards**: Follow HTTP semantics and conventions
- **Discoverability**: Clients can navigate API capabilities
- **Versioning**: Strategy for managing API evolution

## Core Concepts

### 1. RESTful Design

REST (Representational State Transfer) principles create intuitive, web-native APIs.

#### Resource-Oriented Design

```
✗ Bad: Action-oriented (verb-heavy)
GET /api/getUsers
POST /api/createUser
PUT /api/updateUser?id=123
DELETE /api/removeUser?id=123

✓ Good: Resource-oriented (noun-focused)
GET    /api/users          # List users
POST   /api/users          # Create user
GET    /api/users/{id}     # Get specific user
PUT    /api/users/{id}     # Update user
DELETE /api/users/{id}     # Delete user
```

#### HTTP Method Semantics

```
GET     - Safe, idempotent. Retrieve resource without side effects
HEAD    - Like GET but without response body
POST    - Create new resource or perform actions
PUT     - Replace entire resource (idempotent)
PATCH   - Partial update (may not be idempotent)
DELETE  - Remove resource (idempotent)
OPTIONS - Describe available methods
```

**Idempotency Rule**:

```csharp
// ✓ Good: PUT is idempotent (same request = same result)
PUT /api/users/123
{
  "name": "John",
  "email": "john@example.com"
}

// Call multiple times → same result

// ✓ Good: POST for non-idempotent operations
POST /api/users
{
  "name": "John"
}

// Call multiple times → creates multiple users (non-idempotent)
```

#### Nested Resources

```
GET  /api/users/123/orders              # Get user's orders
GET  /api/users/123/orders/456          # Get specific order
POST /api/users/123/orders/456/items    # Add item to order

# Avoid excessive nesting (hard to navigate, test)
✗ Avoid: /api/users/123/orders/456/items/789/notes/321
✓ Better: /api/items/789?_expand=notes  # Expand on demand
```

### 2. Request & Response Design

#### Consistent Naming

```json
{
  "✓ Good: camelCase for JSON fields":
  {
    "userId": 123,
    "userName": "john_doe",
    "createdAt": "2024-01-15T10:30:00Z",
    "isActive": true,
    "orderItems": [...]
  }
}

{
  "✓ Also acceptable: snake_case (common in APIs)":
  {
    "user_id": 123,
    "user_name": "john_doe",
    "created_at": "2024-01-15T10:30:00Z",
    "is_active": true,
    "order_items": [...]
  }
}
```

#### Error Responses

```json
{
  "✗ Bad: Inconsistent error format":
  "error": "User not found"
}

{
  "✓ Good: Structured error response":
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "The requested user was not found",
    "statusCode": 404,
    "timestamp": "2024-01-15T10:30:00Z",
    "details": {
      "userId": "123"
    }
  }
}
```

#### Pagination

```json
{
  "✓ Good: Consistent pagination":
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalPages": 50,
    "totalCount": 1000,
    "hasNext": true,
    "hasPrev": false,
    "nextUrl": "/api/users?page=2&pageSize=20",
    "prevUrl": null
  }
}
```

### 3. HTTP Status Codes

Use correct status codes for API contract clarity:

```
2xx Success
  200 OK              - Successful GET, PUT, PATCH
  201 Created         - Successful POST (resource created)
  204 No Content      - Successful DELETE or PUT with no body

3xx Redirection
  301 Moved Permanently - Resource moved, update URLs
  304 Not Modified       - Cached response still valid

4xx Client Error
  400 Bad Request         - Malformed request, validation failed
  401 Unauthorized        - Authentication required
  403 Forbidden           - Authenticated but not authorized
  404 Not Found           - Resource doesn't exist
  409 Conflict            - Request conflicts with current state
  422 Unprocessable Entity - Request understood but semantically invalid
  429 Too Many Requests   - Rate limiting in effect

5xx Server Error
  500 Internal Server Error  - Unexpected server error
  502 Bad Gateway            - Upstream service unavailable
  503 Service Unavailable    - Maintenance or overload
```

**Good Practice**:

```csharp
public class UserController : ControllerBase {
    [HttpPost]
    public IActionResult CreateUser(CreateUserRequest request) {
        if (!ModelState.IsValid) {
            return BadRequest(ModelState);  // 400
        }

        var user = _service.CreateUser(request);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);  // 201
    }

    [HttpGet("{id}")]
    public IActionResult GetUser(int id) {
        var user = _service.GetUser(id);
        if (user == null) {
            return NotFound();  // 404
        }
        return Ok(user);  // 200
    }

    [HttpDelete("{id}")]
    public IActionResult DeleteUser(int id) {
        _service.DeleteUser(id);
        return NoContent();  // 204
    }
}
```

### 4. Versioning Strategy

Plan for API evolution from the start.

#### URL Path Versioning

```
GET /api/v1/users
GET /api/v2/users

Pros: Clear in URLs, easy to deprecate
Cons: More deployment complexity, URL duplication
```

#### Header Versioning

```
GET /api/users
Accept: application/vnd.myapi.v2+json

Pros: Cleaner URLs, negotiation standard
Cons: Less obvious in browser, harder to test
```

#### Backwards Compatibility (Recommended)

```csharp
// ✓ Good: Support multiple versions without separate endpoints
[HttpGet("/api/users/{id}")]
public IActionResult GetUser(int id, [FromQuery] string? apiVersion = "1") {
    var user = _service.GetUser(id);

    if (apiVersion == "2") {
        return Ok(new UserResponseV2 {
            Id = user.Id,
            Name = user.Name,
            Email = user.Email,
            Roles = user.Roles  // New in V2
        });
    }

    return Ok(new UserResponse {
        Id = user.Id,
        Name = user.Name,
        Email = user.Email
    });
}
```

#### Deprecation Strategy

```json
{
  "Deprecation": "Sat, 30 Jun 2025 23:59:59 GMT",
  "Sunset": "Sun, 01 Jan 2026 00:00:00 GMT",
  "Link": "</api/v2/users>; rel=\"successor-version\""
}
```

### 5. Authentication & Authorization

```typescript
// ✓ Good: JWT Bearer token
GET /api/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

// ✓ Good: API Key (for service-to-service)
GET /api/users
X-API-Key: sk_prod_abc123def456

// ✗ Bad: Credentials in URL
GET /api/users?username=john&password=secret
```

### 6. Rate Limiting & Throttling

```http
✓ Good: Advertise limits in response headers
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642351200

✓ Good: Return 429 when limit exceeded
HTTP/1.1 429 Too Many Requests
Retry-After: 60

{
  "error": "Rate limit exceeded",
  "retryAfter": 60
}
```

### 7. Filtering, Sorting, Searching

```
GET /api/users?status=active&sort=-createdAt&search=john

Parsing:
- status=active          # Filter by status
- sort=-createdAt        # Sort by createdAt descending (- prefix)
- search=john            # Full-text search

✓ Good implementation with validation
var query = dbContext.Users
    .Where(u => u.Status == request.Status)
    .OrderByDescending(u => u.CreatedAt)
    .Where(u => EF.Functions.Like(u.Name, $"%{request.Search}%"))
    .ToListAsync();
```

### 8. API Documentation

Every endpoint needs clear documentation:

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List all users
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '400':
          description: Invalid parameters
        '401':
          description: Unauthorized

    post:
      summary: Create new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Validation error

components:
  schemas:
    User:
      type: object
      required: [id, name, email]
      properties:
        id:
          type: integer
          example: 123
        name:
          type: string
          example: "John Doe"
        email:
          type: string
          format: email
          example: "john@example.com"
        createdAt:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"

    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 255
        email:
          type: string
          format: email
```

### 9. CORS & Security Headers

```csharp
// ✓ Good: Configure CORS properly
services.AddCors(options => {
    options.AddPolicy("AllowFrontend", policy => {
        policy.WithOrigins("https://app.example.com")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });
});

// ✓ Good: Security headers
app.Use(async (context, next) => {
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    await next();
});
```

## Application Checklist

- [ ] Resources identified and URIs designed consistently
- [ ] HTTP methods used according to semantics (GET, POST, PUT, DELETE)
- [ ] Appropriate HTTP status codes for all responses
- [ ] Error responses follow consistent structure
- [ ] Pagination implemented for list endpoints
- [ ] Filtering and sorting supported
- [ ] API versioning strategy defined
- [ ] Backwards compatibility maintained or deprecation path clear
- [ ] Authentication/authorization implemented
- [ ] Rate limiting configured
- [ ] CORS properly configured
- [ ] Security headers set
- [ ] OpenAPI/Swagger documentation complete
- [ ] Request/response examples provided
- [ ] Load tested and performance verified
- [ ] Monitoring and logging in place

## Related Principles

- [Code Quality Goals](../../.github/copilot/code-quality-goals.md) - API usability is a quality concern
- [Design by Contract](../../.github/copilot/design-by-contract.md) - API contract clarity
- [DRY Principle](../../.github/copilot/dry-principle.md) - Avoid duplicating API patterns

## Anti-Patterns

**1. Inconsistent Naming**

```
✗ Bad: Mix of conventions
GET /api/getAllUsers
GET /api/user/{id}
GET /api/fetch_posts

✓ Good: Consistent naming
GET /api/users
GET /api/users/{id}
GET /api/posts
```

**2. Over-Engineering Responses**

```json
{
  "✗ Bad: Deeply nested, unclear structure":
  "response": {
    "data": {
      "payload": {
        "results": {
          "users": [...]
        }
      }
    }
  }
}

{
  "✓ Good: Flat, clear structure":
  "data": [...],
  "pagination": {...}
}
```

**3. Ignoring HTTP Semantics**

```
✗ Bad: Everything is POST
POST /api/getUsers
POST /api/getUserById?id=123
POST /api/deleteUser?id=456

✓ Good: Proper HTTP methods
GET    /api/users
GET    /api/users/123
DELETE /api/users/456
```

## API Testing Tools

- **Documentation**: Swagger/OpenAPI, Postman, Insomnia
- **Testing**: REST Assured, Postman, Thunder Client
- **Monitoring**: New Relic, Datadog, API Gateway Analytics
- **Load Testing**: Apache JMeter, k6, Artillery
