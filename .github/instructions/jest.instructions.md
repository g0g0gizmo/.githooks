---
description: 'Jest unit/integration testing guidelines for JS/TS projects'
applyTo: '**/tests/**/*.ts, **/tests/**/*.js, **/*.spec.ts, **/*.spec.js'
---

# Jest Testing Guidelines

- Imports: `import { describe, it, expect } from '@jest/globals'` or default config.
- Structure: Group with `describe`; use clear test names; AAA pattern (Arrange/Act/Assert).
- Mocks: Use `jest.mock` for modules; prefer dependency injection over global mocks.
- Async: Use `await` with promises; avoid `done` unless necessary.
- Assertions: Prefer specific matchers (`toHaveBeenCalledWith`, `toContainEqual`).
- Coverage: Enable coverage in CI; focus on critical paths; avoid 100% dogma.
- Performance: Avoid hitting real networks/filesystems; use fakes; keep tests fast.
- Snapshots: Use sparingly; prefer explicit assertions; update snapshots intentionally.

See also: `javascript-typescript.instructions.md`, `playwright-typescript.instructions.md`.
