# Example workflow

1. `toolchain_probe` to inspect local dependencies.
2. `generate_design_spec({"project_name":"My visual studio","style":"dark-luxury","target":"web"})`.
3. `create_ui_prototype({"project_name":"My visual studio","style":"dark-luxury"})` to produce HTML/CSS/JS.
4. `audit_ui({"index_path":"<path returned in step 3>"})`: real desktop/tablet/mobile screenshots, basic controls and layout checks (requires Playwright + Chromium).
5. Optional: `compare_screenshots` using screenshot and a **same-dimension**, privately supplied reference; numbers measure pixels only.
6. `create_vehicle_blockout` or `create_city_blockout` or `create_winter_environment` for an actual GLB **blockout**.
7. `audit_3d({"glb_path":"<path returned in step 6>"})`: check geometry count and bounds; not an FPS or photoreal quality check.
8. `create_blender_recipe` makes a Cycles rendering script for an *existing* GLB. Requires a separately installed Blender executable.

All assets are intentionally starter-tier, not production-asset replacements.
