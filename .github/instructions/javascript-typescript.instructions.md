---
description: General JavaScript/TypeScript coding standards beyond React/Playwright; linting, formatting,
applyTo: '**/*.js, **/*.ts'
---

# JavaScript/TypeScript Standards

- Language level: Target ES2022; TypeScript 5.x recommended. Use `tsconfig` strict mode.
- Modules: Prefer ES modules; avoid default exports for utilities; use named exports.
- Linting: Use ESLint with TypeScript plugin; fix warnings; no `any` unless justified.
- Formatting: Use Prettier; respect project print width; avoid mixing formatters.
- Error handling: Throw typed errors; avoid silent catches; log with structured context.
- Async: Prefer `async/await`; avoid unhandled promises; use `Promise.allSettled` for bulk.
- State: Avoid globals; prefer DI/config objects; keep functions pure where possible.
- Testing: Use Jest or Vitest for unit tests; colocate tests with code or under `tests/`.
- Security: Sanitize user input; avoid `innerHTML`; use parameterized queries for any DB.
- Performance: Debounce/throttle hot events; avoid blocking main thread; use workers.

See also: `reactjs.instructions.md`, `playwright-typescript.instructions.md`, `security-and-owasp.instructions.md`.
