---
description: "Use Jina Reader (r.jina.ai / s.jina.ai) to fetch or search web content for grounding"
applyTo: "**/*"
---

# Jina Reader Usage Instructions

- Prefer Reader for external lookups: prepend `https://s.jina.ai/` for search queries and `https://r.jina.ai/` for direct URL fetches.
- Always URL-encode queries and paths (e.g., spaces to `%20`, question marks to `%3F`).
- For web search tasks:
  - Build `https://s.jina.ai/<encoded query>`; use `site=` query params to scope domains when helpful (e.g., `?site=jina.ai&site=github.com`).
  - Expect top-5 results already expanded by Reader; no extra crawling needed unless deeper follow-up is required.
- For single-page fetch tasks:
  - Build `https://r.jina.ai/<full target URL>`; use POST with `url=<target>` for hash-based SPA routes when `#` content matters.
  - If content loads via JS or is delayed, prefer streaming mode with header `Accept: text/event-stream`; the last chunk is most complete.
  - For SPAs or dynamic pages, use headers:
    - `x-wait-for-selector: <css>` when a specific element must render before capture.
    - `x-target-selector: <css>` to extract a sub-tree when auto-extraction misses the desired content.
    - `x-timeout: <seconds>` to wait longer for network idle on slow pages.
- Control output format based on downstream need:
  - Default is markdown; use `Accept: application/json` when JSON is required (search returns a list of `{title, content, url}`; fetch returns `{url, title, content}`).
  - Use `x-respond-with: markdown|html|text|screenshot` to override readability handling; prefer markdown unless the task explicitly needs raw HTML, plain text, or a screenshot URL.
- Caching and freshness:
  - Responses cache ~1h. Force fresh content with `x-no-cache: true` or `x-cache-tolerance: 0` when time-sensitive.
  - Avoid disabling cache unless necessary to reduce latency and load.
- Images and accessibility:
  - Enable auto alt-text when image context matters via `x-with-generated-alt: true`.
- Cookies and proxies (use sparingly):
  - Forward cookies with `x-set-cookie` only when needed; cached responses are skipped when cookies are sent.
  - Route through a proxy with `x-proxy-url` if required by the target environment.
- Error handling and fallbacks:
  - If Reader returns incomplete content, retry with streaming mode and longer `x-timeout` or a more specific `x-wait-for-selector`.
  - When search results lack the needed detail, drill down by fetching individual result URLs with `r.jina.ai`.
- Include citation-quality links in responses: cite the final `r.jina.ai` or `s.jina.ai` URLs used so readers can reproduce the fetch.
- Security and safety: never send secrets, tokens, or internal-only URLs to Reader; use it only for public web content.
