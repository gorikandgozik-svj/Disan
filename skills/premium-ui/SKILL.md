---
name: premium-ui
description: "Use implicitly when implementing Android, desktop or web UI with premium visuals based on examples, especially glassmorphism, cinematic design, tactile dashboards, microinteraction, or high-fidelity clone/reconstruction."
---

# Premium UI: production procedure

A reference picture is an input; the deliverable is code with working state, semantic structure, responsive layout and real interactions. Analyze a screenshot into regions, layout grid, typography scale, radii, glass material stack, shadows, contrast and color tokens. Use `references/design-dna.md` for the user's palette directions. Preserve actual labels/content of user's application and replace all nonsense AI-looking words with real content.

## Deliverables and stages

- `style-spec.json`: palette, type scale, spacing, elevation, contrast, motion, components, responsive rules, target screenshots.
- A functional project in the user's target framework (Android Compose/Flutter, web React or vanilla, native desktop). Do not relabel HTML mockups as APKs.
- Build native controls and all intended state; loading, error, empty, pressed, focused, disabled and touch input states. Implement interaction and navigation; no fake buttons.
- Use actual image assets or vector/3D resources with appropriate rights; do not simply place a screenshot in a mock device to simulate a UI.
- Render at multiple widths (mobile 360-430, tablet 768, desktop 1280/1440) and test tiny height/landscape if relevant. Maintain safe-area insets and bottom navigation reachability.
- Check text clipping, element overlap, visual hierarchy, tap areas (~44px or appropriate platform guidance), keyboard focus, reduced motion, color contrast, touch target spacing, loading speed and actual events.
- Repeat screenshot comparison against user reference, documenting each significant deviation. Do not report arbitrary quality percentages as verified.

## Design systems

1. Dark luxury: charcoal ink, warm metallic accents, calibrated depth, subtle edges and data-dense grids.
2. Tactile glass: semi-transparent warm glass, carefully bounded backdrop-filter, physical highlights and useful controls.
3. Cinematic photography: full-bleed scenic asset, gradient overlays, readable text, calm information hierarchy.
4. Precision minimal: monochrome, semantic typography, asymmetric but aligned grid, predictable spacing and focus.
5. Illustrated / scenic: actual layered illustration or 3D assets and animatable components, not a flattened single reference graphic.

Use a style only when appropriate. Avoid indiscriminate gloss and excessive animation. 150-300ms UI motion is a design starting point, not a guaranteed target; test on device.

## Optional local tool

`create_ui_prototype` creates a **functional browser prototype**, not a completed Android app. Its premade style profiles provide an execution baseline; generative specificity must be implemented by additional project edits. `audit_ui` checks rendered viewports and obvious overflow, not human aesthetic quality.
