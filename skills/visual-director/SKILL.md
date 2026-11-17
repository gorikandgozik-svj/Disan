---
name: visual-director
description: "Automatically use when a user requests a new or improved project whose UI, visual style, 3D objects, game graphics, landscapes or reference fidelity materially matters. Route actual building and visual QA; never substitute a picture for running software."
---

# VIBE VISUAL FORGE / Director

Implicit activation: on relevant creative/product/build tasks without requiring an @-mention. `agents/openai.yaml` explicitly allows implicit invocation. **Do not falsely imply constant execution or that a trigger-free background process has been installed.** If not invoked, the plugin cannot act.

1. Extract the visual target from current prompt / uploaded screenshots. The `references/design-dna.md` file contains abstract art direction; no user-provided photographs are bundled in public releases. Distinguish still-photo realism from a real-time scene budget and UI concept art from functional product screenshots.
2. Set the output contract: target platform (PC/Android/web), real project format, visual-reference IDs, functionality, performance budget and evidence of working output. Infer from conversation; do not ask repeat questions.
3. Route: `premium-ui` for interfaces; `production-3d` for geometry, architecture, cars, planes, engines or game graphics; `visual-qa` to inspect implementation. Do not use presentation mockups as final products. Combine them if appropriate.
4. When available, use actual rendering/build systems: design tools for editable layouts, web/Android frameworks for UI, Blender/Godot/Unreal and asset pipelines for meshes, shading, animation. The plugin's optional MCP local runtime supports deterministic starter assets and quality checks, **not automatic high-end photoreal generation**.
5. Work end-to-end in current task: create code and assets, run or build, screenshot, inspect, fix, repeat. Do not say it ran if there is no execution evidence. Prefer finishing a scoped working slice over a large fictitious project.
6. Add quality gates: correct object silhouette, material fidelity, color/light, component hierarchy, text legibility, responsiveness, click/touch operation, perf and crash check. Track known gaps explicitly.
7. Model confidentiality: use only available tools, do not download paid assets without licenses, do not fabricate API keys, avoid overwriting the user's existing assets without backup.

## Tool use

For mobile and desktop, prefer the verified remote `forge_design_spec`, `forge_ui_html`, `forge_3d_scene_plan`, `forge_contrast` and `forge_capabilities` when the cloud service is connected. For optional desktop local MCP tools: `toolchain_probe`, `create_ui_prototype`, `audit_ui`, `analyze_reference`, `create_city_blockout`, `create_vehicle_blockout`, `create_winter_environment`, `audit_3d`, `compare_screenshots`, `create_blender_recipe`. If a tool is unavailable, state that and proceed with actually available build tools. Do not claim that tools exist merely because this SKILL lists them.

## Reality check

The bundled reference shots show photographic quality. To achieve that as an *interactive* real-time game, use detailed licensed assets, multi-view sources, optimized texture/PBR workflow, dynamic lighting and GPU-specific profiles. A screenshot alone is not sufficient to reconstruct accurate geometry or prove a 60fps target.
