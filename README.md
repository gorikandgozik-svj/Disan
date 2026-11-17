# VIBE VISUAL FORGE

**Reference-driven UI / 3D production tools for ChatGPT and supported local MCP hosts.**

[![Tests](https://img.shields.io/badge/local%20tests-25%20passed-35b779)](#verification) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **Status: development toolkit, not an AAA art generator.** It builds real responsive web prototypes and GLB **blockouts**, produces limited structural audits, and helps organize visual-engineering work. It does **not** include a proprietary photorealistic 3D model, render farm, Blender, GPU engine, cloud inference, Android APK compiler, or always-on ChatGPT executor. No claim of visual parity with cinematic automotive and aircraft photographs is made.

## Capabilities

| Category | What actually runs | Not yet provided |
| --- | --- | --- |
| UI | Five style token sets, browser-based functional UI demo, buttons, controls, charts | arbitrary prompt-to-app, production-ready application backend |
| Responsive QA | Chromium/Playwright screenshot checks at 320 / 390 / 768 / 832-landscape / 1440px, slider/mood/navigation/reset checks | independent accessibility audit, detailed manual visual review |
| References | Pillow palette and dimensions; equal-size screenshot pixel diff | full multimodal understanding or photo-to-geometry generation |
| 3D city | procedural GLB city blockout with actual geometry | detailed photogrammetric buildings, materials library, game-world streaming |
| 3D vehicles | GLB car and four-engine airliner **silhouette blockouts**, named parts | true-to-model blueprints, rigged animations, real CAD, manufacturer geometry |
| 3D nature | procedural snow-and-conifers GLB environment blockout | photoreal vegetation, wind simulation, GPU lighting/weather system |
| 3D QA | GLB geometry/bounds/degeneracy and triangle counts | visual quality, collisions, GPU FPS, device profiling |
| Rendering | Blender 4.x Cycles studio *script* for externally supplied GLB | Blender bundling or verified rendered final asset |
| Automation | allow-listed local queue with bounded tasks and failure logs | work while host is closed, self-activation in every ChatGPT message |

## Quick start

Install **Python 3.11+**, then in the project directory:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python server/mcp_server.py
```

The third command starts an MCP stdio server; a compatible desktop host can configure it with the `mcp.json` command. The server expects newline-delimited JSON-RPC over stdin. **Do not paste JSON messages into an active ordinary terminal without the server process.**

Example request (when connected to the MCP host):

```json
{"name":"create_ui_prototype","arguments":{"project_name":"My Design","style":"dark-luxury"}}
```

Tools: `toolchain_probe`, `analyze_reference`, `generate_design_spec`, `create_ui_prototype`, `audit_ui`, `create_city_blockout`, `create_vehicle_blockout`, `create_winter_environment`, `audit_3d`, `compare_screenshots`, `create_blender_recipe`.

### Browser QA (optional)

```bash
python -m pip install playwright
python -m playwright install chromium
VF_RUN_BROWSER_TESTS=1 python -m unittest discover -s tests -v   # Linux / macOS
```

Windows PowerShell:

```powershell
$env:VF_RUN_BROWSER_TESTS = '1'
python -m unittest discover -s tests -v
```

### Local queue (optional; NOT self-installing)

```bash
python server/watch.py --once  # execute pending jobs once
python server/watch.py         # poll until stopped; only if you explicitly start it
```

Create `~/VisualForgeProjects/queue/inbox/job1.json` (or set `VF_WORKSPACE_DIR`) with:

```json
{"tool":"create_ui_prototype","arguments":{"project_name":"My Demo","style":"cinematic"}}
```

Reports appear under `queue/done` or `queue/failed`. The watcher never runs arbitrary shell snippets, does not retry failed jobs, has a 64-KiB task limit, and checks abandoned jobs. It is **not** a continuously running autonomous AI and does not connect to ChatGPT via itself. Set a process manager up explicitly if required.

## Plugin packaging and limitations

- `plugin.json`: portable Agent Plugins 1.0 manifest, plugin name `vibe-visual-forge`, version 1.1.0.
- `skills/*/SKILL.md`: five optional auto-eligible skills. Their invocation is controlled by ChatGPT's host; installing a private plugin does not prove invocation in each chat.
- `mcp.json`: local stdio MCP process. It cannot automatically connect to mobile ChatGPT or a cloud account without a separate supported runtime.
- `server/`: lightweight Python implementation and procedural assets. Core MCP server uses stdlib; the generation/test tools require the dependencies in `requirements.txt`.

**Hardware:** interactive graphics performance must be measured on the target phone or PC. Offline screenshot speed or triangle count never proves 60 FPS.

## Verification

See [`docs/TEST_REPORT.md`](docs/TEST_REPORT.md) for reproducible evidence, tested Python/browser environment and remaining gaps. Do not confuse test-suite pass rate with production quality or visual fidelity.

## Open source, privacy and references

The MIT license covers the code and bundled original icon only. **The 23 user-supplied photographic/UI references are excluded** because redistribution rights have not been verified. If you have lawful visual references, provide them privately to your own workflow. Do not place private photographs, API keys, accounts or other third-party proprietary assets in a public repository.

## Contributing

Contributions welcome: improve real geometry, tested shaders/materials, Blender integration, screenshot comparison, accessibility, Android builds and measurable performance. Include deterministic tests and explicit truth labels. See [`SECURITY.md`](SECURITY.md) before reporting vulnerabilities.
