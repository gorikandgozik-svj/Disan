# VIBE VISUAL FORGE 1.2.2 — cross-platform studio and remote MCP

## Implemented

- New installable responsive PWA that runs in mobile/desktop browsers, with offline caching of static assets after initial load.
- Actual interactive browser UI creator with four design themes and standalone HTML export.
- Canvas 3D blockout preview and real GLB 2.0 export for four deterministic scene presets.
- Quality Lab WCAG color contrast checker; browser-local saved project settings.
- New bounded, stateless HTTPS Streamable HTTP MCP endpoint with five read-only/safe generation tools.
- Added Node tests for protocol, security/validation, template safety and geometry; added responsive browser tests; retained Python desktop tools and test suite.

## Unimplemented or unverified

- Photorealistic 3D, licensed professional asset generation, complex rigs, physically accurate vehicles, advanced shaders, native Android APK and Windows EXE.
- Cloud project sync, autonomous never-ending background jobs, guaranteed 24/7 uptime.
- Automatic invocation of private ChatGPT plugin on all mobile/desktop clients (controlled by host availability/installation).
- Real device 60 FPS performance, battery use and full WCAG accessibility audit.

**Honest classification:** working cross-platform prototype/toolkit, not the complete originally requested studio-quality visual engine.

## Cloud deployment status

The Vercel project `vibe-visual-forge-cloud` reported a production deployment as READY with its Vercel Authentication protection turned off. The actual public hostname is https://vibe-visual-forge-cloud.vercel.app. The ChatGPT plugin MCP source was updated to the production HTTPS endpoint. Real-world Android/PC use, independent HTTP round-trip and plugin activation remain to be verified from client devices.

## v1.2.2 CI fix

Declared SciPy as a 3D exporter dependency after GitHub-hosted Python tests failed with `ModuleNotFoundError: No module named scipy`. This is a dependency fix, not a photorealism enhancement.
