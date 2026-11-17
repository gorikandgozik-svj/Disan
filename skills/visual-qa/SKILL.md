---
name: visual-qa
description: "Use implicitly after UI, game graphics or 3D implementation, and when a user reports ugly or broken visuals, layout overlap, unresponsive controls, missing 3D detail, bad physics, APK/EXE build failures or visual mismatch."
---

# Visual QA / verification before release

Never accept user-visible screenshots, videos, product promotional renders, or assistant-generated mockups as proof that actual software works.

## Visual checks

- UI: launch real implementation, screenshot desktop and mobile, check viewport overflow, clipping, z-index, keyboard and touch, button effects, states, safe-area and color contrast. Compare directly to references; palette consistency alone does not establish fidelity.
- 3D: verify GLB/BLEND import, nondegenerate bounds/scale, material assignments, camera movement, normal orientation, silhouette in multiple views, weather effects, collisions, temporal stability and naming for animation rig.
- FPS: measure runtime frame time distribution on target device (median and p95/p99). A local fast PC render cannot certify Android 60fps; no GPU run means **performance not verified**.
- Build: run compile, unit tests and smoke tests; capture errors and reproduce. An APK or EXE that was not generated or tested must not be described as ready or fully functional.

Use `audit_ui` tool for Chrome/Chromium screenshots (if Playwright/browser present). The tool assesses mechanical layout and captures screenshot paths, not aesthetic similarity. `analyze_reference` returns palette/image metrics, not an actual multimodal understanding of object geometry. After automated checks, do manual reference review when possible.

Use a short end-state table or concise summary with **Pass / Fail / Not tested** and concrete artifacts. No fabricated scores and no claiming all defects fixed if untested.
