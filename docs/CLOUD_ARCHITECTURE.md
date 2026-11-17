# Cross-platform architecture: 1.2.2

```text
Android browser/PWA ─┐
                     ├── HTTPS Vercel site ── /api/mcp (stateless JSON-RPC)
Windows browser/PWA ─┘          │
                               └── UI & GLB generation runs locally in browser
ChatGPT remote MCP ─────────────── HTTPS /mcp (safe generation tools)
Windows Python desktop host ───── optional local MCP (Blender and file system)
```

No cloud database or dedicated worker exists. The PWA does not upload generated assets. The optional local Python executor is **not** remotely callable from the public endpoint, to avoid exposing arbitrary user files and commands. This is an intentional security boundary.

## Work that remains for a truly always-on experience

Implement authenticated user sessions, durable storage, bounded job queues, a dedicated worker (or managed workflow runtime), quotas, telemetry, secrets management, retries and idempotency, and device sync. Host authorization to call the private plugin also needs to be verified. Never describe these as implemented solely because the public web app is online.

## MCP compatibility

Stateless Streamable HTTP (protocol 2025-11-25); JSON-RPC POST at /mcp; no session IDs, no server-initiated SSE or sampling, no OAuth, no client filesystem access. Requires the client to accept both `application/json` and `text/event-stream`. All tool calls are bounded to deterministic local computations.

**Production alias:** https://vibe-visual-forge-cloud.vercel.app. Production MCP: https://vibe-visual-forge-cloud.vercel.app/mcp. Hosting deployment is separate from GitHub: the account requires a GitHub Login Connection to enable automatic Git deployment.
