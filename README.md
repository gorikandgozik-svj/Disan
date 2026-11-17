# VIBE VISUAL FORGE 1.2.0

**Cross-platform PWA + HTTPS MCP design/3D toolkit.** Open the same web studio on Android and Windows, export editable HTML interfaces and genuine GLB geometry files, or use safe stateless tools in any remote MCP-compatible host.

> **Actual quality:** UI prototypes and low-poly procedural **blockouts**. This is neither a photoreal AI image/3D model nor an AAA game engine. Background autonomous work, cross-device cloud sync, native APK/EXE, and guaranteed 24/7 uptime have **not** been implemented.

## 1. Use on phone and PC

Once deployed, open the hosted HTTPS studio from your mobile or desktop browser. Install it from the browser's **Add to Home screen / Install app** if that browser supports PWA installation. The responsive app is the same on both platforms, does not require Python on Android, and works with previously cached assets offline after first load. Exports are downloaded onto the current device.

UI Studio: editable design system + live interactive HTML preview + standalone HTML export. 3D Workshop: a rotatable genuine 3D blockout viewer for city, winter forest, sports car and airliner, plus GLB 2.0 export. Quality Lab: color contrast check. Projects: **local browser storage only**; there is no cloud sync. No third-party photographs are bundled.

## 2. Remote MCP (ChatGPT or another compatible client)

Host `/mcp` using Vercel or a Node.js-compatible HTTPS environment. Connect the deployed endpoint as a *remote* Streamable HTTP MCP server where the host allows that capability. It supports stateless `POST` JSON-RPC with `Accept: application/json, text/event-stream`. Calls cannot access a user's filesystem, private account, arbitrary URLs, or shell. Tool list:

- `forge_capabilities` — honest features and unsupported claims.
- `forge_design_spec` — palette/layout/typography with testable design contract.
- `forge_ui_html` — standalone interactive HTML from a project name/theme.
- `forge_3d_scene_plan` — deterministic scene-geometry parameters.
- `forge_contrast` — WCAG contrast ratio.

Remote MCP is intentionally stateless and public **without authentication**. Do not send secrets or personal data in tool arguments. No external AI provider, GPU backend, image-to-3D model or durable task queue is included.

### Request example

```sh
curl -sS https://YOUR-DEPLOYMENT.example/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 3. Source development and tests

```sh
npm test                # Node: GLB, HTML, security, HTTP/MCP protocol
npm run check           # JS syntax
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Browser tests require Playwright with Chromium; set `VF_RUN_BROWSER_TESTS=1` and see `docs/TEST_REPORT.md`. The optional Python **desktop** MCP still exists at `server/mcp_server.py`; its portable configuration is `mcp.local.json`, installed separately from the cloud service.

## 4. Deploy

Connect this GitHub repository to Vercel, configure the project root at the repository root, use the default Node runtime, and deploy. The `/` route serves the PWA, `/api/health` is a non-secret status endpoint, `/mcp` routes to the stateless MCP endpoint. `vercel.json` defines the rewrite. Production HTTPS is necessary for installable PWA support.

The `mcp.json` for the ChatGPT plugin is updated to the **verified** deployed endpoint only after it is live. If the host does not enable personal plugins or remote connectors on Android, this package alone cannot change ChatGPT app entitlement. The PWA remains usable in the browser.

## 5. Availability limitations

Vercel's serverless functions respond when invoked; they do not run an autonomous daemon continuously. Free hosting has usage limits, possible outages and rate limits. A true durable background processing service requires a job queue, database, worker and operational monitoring. Offline PWA assets allow local editing but do not process remote AI tasks while devices are asleep.

## 6. Ethical licensing and security

MIT license covers the code and original icon. User-submitted photographic references are not included in the public distribution. Never embed third-party API keys into the public PWA or repository. See `SECURITY.md`.
