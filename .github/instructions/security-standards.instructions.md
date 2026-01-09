---
description: 'Incorporate security from the beginning with foundational controls and best practices'
---

# Security Standards

## Overview

Security is a foundational concern in modern software development. This principle ensures that all code, architecture, and infrastructure decisions incorporate security from the beginning (security by design), rather than treating it as an afterthought.

Security Standards ensure:

- Prevention of common vulnerabilities (OWASP Top 10)
- All external inputs are validated and sanitized
- Proper authentication and authorization controls
- Sensitive data is encrypted and protected
- Security events are logged and monitored
- Systems fail securely without exposing details
- Dependencies are regularly updated and scanned
- Defense in depth with multiple security layers

## Core Concepts

### 1. OWASP Top 10 Vulnerabilities (2023)

All applications must address these critical vulnerabilities:

#### A01:2021 – Broken Access Control

Enforce principle of least privilege and verify authorization on every request.

```csharp
// ❌ Bad: No authorization check
public Order GetOrder(int orderId) {
    return _repository.GetOrder(orderId);  // Anyone can access any order
}

// ✅ Good: Verify user owns the resource
public Order GetOrder(int orderId, string userId) {
    var order = _repository.GetOrder(orderId);

    // Verify user owns this order
    if (order.UserId != userId) {
        throw new UnauthorizedAccessException("Not authorized");
    }

    return order;
}
```

**Protections**:
- Enforce principle of least privilege
- Verify authorization on every request
- Use role-based access control (RBAC)
- Implement proper authentication flows
- Disable HTTP method override
- Enforce CORS policy

---

#### A02:2021 – Cryptographic Failures

Use strong encryption and never store sensitive data in plaintext.

```python
# ❌ Bad: Storing plaintext password
user.password = provided_password

# ✅ Good: Use strong password hashing
from werkzeug.security import generate_password_hash, check_password_hash

user.password_hash = generate_password_hash(provided_password)

# Verify password
if check_password_hash(user.password_hash, provided_password):
    authenticate_user()
```

**Protections**:
- Use strong encryption (AES-256, ChaCha20)
- Never hardcode secrets or API keys
- Encrypt sensitive data at rest and in transit
- Use TLS 1.2+ for all network communication
- Never log passwords or sensitive data
- Use password hashing with salts (bcrypt, PBKDF2, Argon2)

---

#### A03:2021 – Injection

Always use parameterized queries and validate inputs.

```csharp
// ❌ Bad: SQL Injection vulnerability
string query = $"SELECT * FROM Users WHERE Email = '{userInput}'";
// If userInput = "'; DROP TABLE Users; --", table is deleted!

// ✅ Good: Parameterized query
var user = _context.Users
    .FromSqlInterpolated($"SELECT * FROM Users WHERE Email = {userInput}")
    .FirstOrDefault();

// ✅ Good: ORM approach (preferred)
var user = _context.Users
    .Where(u => u.Email == userInput)
    .FirstOrDefault();
```

**Protections**:
- Always use parameterized queries/prepared statements
- Validate and sanitize all inputs
- Never concatenate strings into SQL queries
- Use ORM frameworks (Entity Framework, Django ORM)
- Implement input validation on both client and server

---

#### A04:2021 – Insecure Design

Incorporate security requirements from the start.

**Protections**:
- Threat modeling in design phase
- Security requirements before coding
- Secure design patterns and libraries
- Separation of concerns
- Security testing in CI/CD

---

#### A05:2021 – Security Misconfiguration

Minimize deployment surface and remove defaults.

**Protections**:
- Only deploy needed services
- Remove default credentials
- Automated security scanning in pipelines
- Regular dependency updates
- Security headers (CSP, X-Frame-Options, etc.)

---

#### A06:2021 – Vulnerable and Outdated Components

Keep dependencies current and monitored.

**Protections**:
- Regular dependency audits
- Automated vulnerability scanning
- Immediate patching of critical vulnerabilities
- Component version management
- Software composition analysis (SCA)

---

#### A07:2021 – Authentication Failures

Implement robust authentication mechanisms.

**Protections**:
- Multi-factor authentication (MFA)
- Strong password policies
- Secure session management
- Account lockout after failed attempts
- Credential exposure prevention

---

#### A08:2021 – Software and Data Integrity Failures

Verify software authenticity and integrity.

**Protections**:
- Verify software signatures
- Secure CI/CD pipelines
- Dependency integrity checks
- Secure update mechanisms

---

#### A09:2021 – Logging and Monitoring Failures

Log security events and monitor for threats.

**Protections**:
- Comprehensive security event logging
- Real-time alerting on suspicious activities
- Log retention and analysis
- Protect logs from unauthorized access

---

#### A10:2021 – Server-Side Request Forgery (SSRF)

Validate and restrict outbound requests.

**Protections**:
- Validate and sanitize URLs
- Whitelist allowed domains
- Disable unused URL schemes
- Implement network segmentation

---

### 2. Input Validation

All external inputs are untrusted until proven otherwise.

```typescript
// Good: Validate inputs at system boundaries
function createUser(email: string, password: string): User {
    // Validate email format
    if (!isValidEmail(email)) {
        throw new ValidationError("Invalid email format");
    }

    // Validate password strength
    if (password.length < 12 || !hasSpecialCharacters(password)) {
        throw new ValidationError("Password does not meet requirements");
    }

    // Check for SQL injection patterns (defense in depth)
    if (containsSqlKeywords(email)) {
        throw new ValidationError("Invalid input detected");
    }

    return _repository.create({ email, password });
}
```

---

### 3. Authentication & Authorization

- **Authentication**: Verify who you are
- **Authorization**: Verify what you can do

```java
@RestController
public class ResourceController {

    @GetMapping("/resource/{id}")
    @PreAuthorize("isAuthenticated()")  // Authentication: require login
    public Resource getResource(@PathVariable int id, @AuthenticationPrincipal User user) {
        Resource resource = repository.findById(id);

        // Authorization: User must own the resource
        if (!resource.getOwnerId().equals(user.getId())) {
            throw new AccessDeniedException("Not authorized");
        }

        return resource;
    }
}
```

---

### 4. Secure Data Management

```python
# Good: Mask sensitive data in logs
import logging

logger = logging.getLogger(__name__)

def process_payment(credit_card: str, amount: float):
    # Mask card number for logging
    masked_card = f"****-****-****-{credit_card[-4:]}"
    logger.info(f"Processing payment: {amount}, card: {masked_card}")

    # Actual processing with full card details
    gateway.charge(credit_card, amount)
```

**Protections**:
- Never log sensitive data (passwords, tokens, credit cards, SSNs)
- Encrypt data at rest (database fields with PII)
- Encrypt data in transit (HTTPS/TLS for all transmission)
- Minimize exposure through least privilege access
- Use tokenization to replace sensitive data with non-sensitive tokens

---

### 5. Error Handling

Fail securely without exposing system details.

```csharp
// ❌ Bad: Exposing system details
catch (Exception ex) {
    return StatusCode(500, ex.Message);  // Reveals internal structure
}

// ✅ Good: Generic user message, log details
catch (Exception ex) {
    _logger.LogError(ex, "Database error occurred");
    return StatusCode(500, "An error occurred. Please try again later.");
}
```

---

## Application Checklist

- [ ] All inputs validated at system boundaries
- [ ] Parameterized queries used for all database access
- [ ] Sensitive data never logged or exposed in errors
- [ ] HTTPS/TLS used for all data transmission
- [ ] Authentication required for protected resources
- [ ] Authorization verified for every operation
- [ ] Secrets managed via environment variables or vaults
- [ ] Dependencies regularly updated and scanned
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] Security events logged and monitored
- [ ] Rate limiting implemented for APIs
- [ ] CORS properly configured
- [ ] File uploads validated and sanitized
- [ ] SQL injection defenses in place (parameterized queries)
- [ ] XSS protections implemented (input sanitization)
- [ ] CSRF tokens used for state-changing operations
- [ ] Passwords hashed with strong algorithms
- [ ] Session timeouts configured
- [ ] Audit trails maintained for sensitive operations
- [ ] Security testing included in CI/CD
- [ ] Penetration testing performed regularly

### When Developing

1. **Identify Threats**: What could go wrong?
2. **Apply Controls**: Use security patterns
3. **Validate Inputs**: Trust nothing external
4. **Log Events**: Record security-relevant events
5. **Test Security**: Include security in tests

### When Reviewing Code

- Are all inputs validated?
- Is sensitive data protected?
- Are external dependencies mocked in tests?
- Are error messages generic (not exposing internals)?
- Is authentication enforced?
- Is authorization checked?

---

## Related Principles

- [Design by Contract](../../.github/copilot/instructions/design-by-contract.instructions.md) - Security contracts are explicit
- [SOLID Principles](../../.github/copilot/instructions/solid-principles.instructions.md) - Single Responsibility supports security separation
- [Code Quality Goals](../../.github/copilot/instructions/code-quality-goals.instructions.md) - Security is a quality dimension

---

## Anti-Patterns

### Anti-Pattern 1: Hardcoded Secrets

```python
# ❌ Bad: API key in code
API_KEY = "sk_prod_abc123def456"

# ✅ Good: Load from environment
import os
API_KEY = os.getenv('API_KEY')
```

### Anti-Pattern 2: Logging Sensitive Data

```typescript
// ❌ Bad: Logging password
logger.info(`User login: ${email}:${password}`);

// ✅ Good: Log user, not credentials
logger.info(`User login attempt: ${email}`);
```

### Anti-Pattern 3: No Input Validation

```typescript
// ❌ Bad: No validation
function getUser(userId) {
  return database.findById(userId);  // What if userId is malicious?
}

// ✅ Good: Validate input
function getUser(userId: string) {
  if (!userId || !uuid.validate(userId)) {
    throw new ValidationError("Invalid userId");
  }
  return database.findById(userId);
}
```

### Anti-Pattern 4: Exposing System Details in Errors

```typescript
// ❌ Bad: Revealing internals
catch (err) {
  res.status(500).json({
    error: err.message,  // "Cannot read property 'email' of undefined"
    stack: err.stack     // Full stack trace exposed
  });
}

// ✅ Good: Generic error message
catch (err) {
  logger.error(err);  // Log details internally
  res.status(500).json({
    error: "An error occurred. Please try again later."
  });
}
```

### Anti-Pattern 5: No Authorization Checks

```typescript
// ❌ Bad: Only checking authentication
if (!user) {
  throw new Error("Not authenticated");
}
return userService.getUser(userId);  // But can user access this user?

// ✅ Good: Check both authentication and authorization
if (!user) {
  throw new Error("Not authenticated");
}
if (user.id !== userId) {
  throw new Error("Not authorized");
}
return userService.getUser(userId);
```

---

## Security Layers (Defense in Depth)

1. **Network**: Firewalls, VPNs, network segmentation
2. **Transport**: TLS/HTTPS, secure protocols
3. **Application**: Authentication, authorization, input validation
4. **Data**: Encryption, hashing, masking
5. **Access**: Role-based controls, least privilege
6. **Monitoring**: Logging, alerting, incident response

Multiple layers ensure that if one fails, others provide protection.

---

## Common Security Tools

- **Dependency Scanning**: npm audit, Snyk, OWASP Dependency-Check
- **Static Analysis**: SonarQube, Checkmarx, Veracode
- **Dynamic Testing**: OWASP ZAP, Burp Suite
- **Secret Management**: HashiCorp Vault, AWS Secrets Manager
- **Logging**: ELK Stack, Splunk, CloudWatch
- **Monitoring**: New Relic, Datadog, Prometheus

---

## Why Security Matters

✅ **Protects Data** - Sensitive information stays secure
✅ **Prevents Breaches** - Common attacks are blocked
✅ **Builds Trust** - Users trust secure systems
✅ **Reduces Risk** - Fewer security incidents
✅ **Saves Money** - Breaches are expensive to fix
✅ **Legal Compliance** - Meet regulatory requirements

Master security standards, and your applications become resilient against common attacks while building user trust and compliance.
