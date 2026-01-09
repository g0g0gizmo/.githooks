---
description: 'Secrets management guidelines across languages and environments'
applyTo: '**/*'
---

# Secrets Management

- Never hardcode secrets (API keys, tokens, passwords) in code or configs.
- Use environment variables or a secrets manager (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault).
- Local dev: `.env` files allowed; never commit; add to `.gitignore`.
- Rotation: Document rotation cadence and procedures; avoid long-lived tokens.
- Access: Principle of least privilege; scoped keys; separate dev/stage/prod.
- Transport: Always use HTTPS/TLS for secret retrieval; validate host allow-lists.
- Logging: Do not log secrets; scrub sensitive values in error paths.
- CI/CD: Store secrets in pipeline secret stores; map as env vars at runtime only.

See also: `security-and-owasp.instructions.md`, `production-test-sw-release-checklist.instructions.md`.
