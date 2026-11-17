# VIBE VISUAL FORGE v1.2.2 verification

## Local tests (2026-11-17)

- Node: `npm test` — 20 passed, 0 failed, 0 skipped.
- Python: `VF_RUN_BROWSER_TESTS=1 VF_BROWSER_EXECUTABLE=/usr/bin/chromium python -m unittest discover -s tests -v` — 28 passed.
- Node syntax check: `npm run check` — passed.
- Browser responsive PWA screenshots and interaction smoke checks at 390×844, 832×384 and 1440×900: 0 uncaught JS errors, 0 horizontal overflow after fixed mobile navigation, JSON contrast 16.60:1, 3D preview renders, project saving works in browser-local storage.
- GLB outputs validated by Node checks for glTF magic (`glTF`), version 2, chunk length and declared meshes; **not** audited in a game engine or GPU benchmark.

## What these tests do not prove

- No Android physical device or Windows physical PC install has been exercised from this environment.
- No hosted MCP endpoint is certified until production deployment and protocol smoke tests complete.
- App quality does not match cinematic 3D reference photography or AAA game requirements; procedural geometry is illustrative blockout-tier.
- No 24/7 uninterrupted cloud worker or automatic task queue, cross-device account sync, persistent cloud projects, paid AI inference, or guaranteed uptime.
- Offline service-worker installation and battery consumption on real devices not tested.

These are claims about specific tested code paths, not a claim of an ideal/perfect product.

## Hosting evidence

Vercel production deployment: READY, production alias `vibe-visual-forge-cloud.vercel.app`, no password and no Vercel SSO protection. The deployment was created via inline file upload, not a live GitHub integration. A direct external HTTP GET/POST smoke test of the published domain could not be executed from this environment; the endpoint should be verified from a browser and remote MCP client before claiming complete cross-device availability.

## GitHub Actions initial failure resolved in sources

The first GitHub-hosted Python jobs for v1.2.0 failed because `trimesh` needs `scipy.sparse` to convert face colors to vertex colors while exporting GLB. Version 1.2.2 adds an explicit compatible `scipy` requirement. This fix is only confirmed in GitHub after a subsequent workflow run is green; local reruns alone are insufficient.
