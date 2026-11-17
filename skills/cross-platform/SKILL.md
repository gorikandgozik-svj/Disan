---
name: cross-platform
summary: "Cross-platform visual project work on Android and Windows with verified remote MCP when connected, browser PWA for independent use, and optional local Python for heavy PC operations."
description: "Use automatically when a user asks for mobile/desktop visual design, interface creation, 3D geometry, graphics export, or continuity between phone and computer. Distinguish hosted PWA from a native APK and a serverless endpoint from an always-on worker."
---

# VIBE VISUAL FORGE / Cross-platform

Detect platform and prefer the tools actually available in the current ChatGPT host. A saved but disabled plugin is not evidence of installation or callable tools.

**On any device:** The hosted HTTPS PWA (when deployed) supports live responsive HTML template previews, standalone HTML export, a rotatable 3D blockout viewer and GLB export, browser-local projects and contrast checks. This is a website installed as PWA where supported, not a native Android APK or Windows EXE. Cloud project synchronization is not implemented.

**Cloud MCP:** When the remote connection is activated, the safe stateless tools `forge_capabilities`, `forge_design_spec`, `forge_ui_html`, `forge_3d_scene_plan` and `forge_contrast` can be used on mobile or desktop. Do not pretend they are available until discovered and called. No user files, GPU renderer, private credentials or third-party AI inference are exposed by these tools.

**Desktop optional:** The local Python MCP is separate (`mcp.local.json`), can create GLB blockouts, Blender recipes and local QA when installed in a desktop host with permission. Never expose its filesystem tools via the public cloud service.

**Continuous operation:** The live HTTPS service is invoked per request. It is not a worker that autonomously runs projects 24/7. Continuous background tasks require authenticated durable queues and worker infrastructure, which is not part of this release. ChatGPT implicit activation remains host-controlled, even if a skill declares it allowed.

Perform actual tool calls, inspect real artifacts and provide device-specific installation steps when appropriate. Return measured tests and clearly labeled unresolved gaps.
