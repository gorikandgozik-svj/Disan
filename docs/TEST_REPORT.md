# Test report — VIBE VISUAL FORGE 1.1.0

Date: **2026-11-17**. Verified locally in the task runtime with **Python 3.13.5**, `trimesh 4.11.1`, `numpy 2.3.5`, `Pillow 12.3.0`, Playwright and Chromium. These are **local execution results**, not GitHub Actions logs and not device-level Android certification.

## Reproduction

```bash
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
VF_RUN_BROWSER_TESTS=1 python -m unittest discover -s tests -v
```

**Final local result: 25 tests, 25 passed, 0 failed, 0 skipped** using `VF_RUN_BROWSER_TESTS=1`. The test suite covers:

- Python unit and negative-path tests for style specifications, project name validation, HTML escaping, reference handling and error reporting.
- Serialized MCP/JSON-RPC stdio round trip (`initialize`, `tools/list`, successful tool call, tool failure, malformed JSON, notification).
- Local queue allow-list, bounded inputs, symlink rejection and result creation.
- Structural validation for four real GLB exports: city, sports car, generic four-engine airliner and winter forest.
- Pixel comparison, equal/different screenshots, size mismatch rejection.
- Playwright/Chromium UI interactions: light slider, mood switch, navigation state and reset.
- Browser rendering at 320 × 568, 390 × 844, 768 × 1024, 832 × 384 and 1440 × 900.

## Actual UI and 3D audit

| Target | Result | Evidence |
| --- | --- | --- |
| UI @ 320 × 568 | Pass: no horizontal overflow, no uncaught JS errors, basic structural checks | local Chromium screenshot (reproduce using browser QA) |
| UI @ 390 × 844 | Pass: same, plus interaction smoke test | local Chromium screenshot (reproduce using browser QA) |
| UI @ 768 × 1024 | Pass: same | local Chromium screenshot (reproduce using browser QA) |
| UI @ 832 × 384 landscape | Pass: same | local Chromium screenshot (reproduce using browser QA) |
| UI @ 1440 × 900 | Pass: same | local Chromium screenshot (reproduce using browser QA) |
| City blockout | 96 meshes, 1,152 triangles, structural audit passed | locally generated GLB (run the corresponding tool) |
| Sports car blockout | 13 meshes, 996 triangles, structural audit passed | locally generated GLB (run the corresponding tool) |
| Airliner blockout | 14 meshes, 1,068 triangles, structural audit passed | locally generated GLB (run the corresponding tool) |
| Winter forest blockout | 129 meshes, 4,112 triangles, structural audit passed | locally generated GLB (run the corresponding tool) |
| Screenshot difference | Identical screenshots compare to 0.0 normalized MAE | [`test_pipeline.py`](../tests/test_pipeline.py) |

## Issues found and fixed

1. **Mobile reset button hidden by CSS**: browser test originally failed; control is now visible and works at 390px.
2. **Unicode project directory collisions**: distinct Cyrillic names now have unique stable IDs.
3. **Incomplete plugin tool registry**: the saved 1.0.0 plugin had seven tools; this release declares eleven, including structural GLB and pixel audits.
4. **Queue input hardening**: limit task payload, block symlink jobs, bounded number processed, explicit errors for abandoned jobs, atomic report writing.
5. **JSON-RPC robustness**: consistent error responses for parse errors, unknown methods and invalid tool arguments.
6. **Reference redistribution risk**: source bundle no longer includes the 23 supplied photographic reference images.

## What was not verified

- Visual match with the user's premium UI/photographic references: **NOT VERIFIED** (we do not redistribute those references; pixel comparison is not semantic fidelity).
- AAA-quality assets, functioning rigs, procedural PBR texture authoring, physically accurate engines/airframes: **NOT IMPLEMENTED**.
- GPU shaders, actual game engine import, collisions, network, 60 FPS/120 FPS, Android APK/Windows EXE, mobile battery drain: **NOT TESTED**.
- Blender 4.x actual Cycles render: **NOT TESTED**; only Python script compilation is checked.
- Sustained operation of an OS service or automatic ChatGPT host invocation: **NOT TESTED**; only local single-run queue behavior is covered.
- GitHub Actions CI result: **NOT VERIFIED**, pending the hosted workflow run. A separate GitHub Release has not been created.

**Conclusion:** executable development utilities pass their defined local tests. They do **not** meet the original goal of studio-grade visual fidelity or a complete unattended mobile/desktop production pipeline.
