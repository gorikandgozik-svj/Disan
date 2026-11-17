---
name: production-3d
description: "Use implicitly for model/scene/game development including realistic cars, aircraft, engines, landscapes, large cities, PBR materials, simulation-grade details, rigging, or optimized 3D exports."
---

# Production 3D: build actual meshes, not images

Classify every requested output as (a) cinematic still, (b) explorable real-time scene, (c) game-ready asset, or (d) engineering/animation-grade mechanical assembly. They are different deliverables. The user expects real spatial geometry, freely movable camera, materials, physics/collisions and interactive control where applicable. Never confuse output of one class with another.

## Production sequence

1. **Reference & truth:** identify object/category and silhouette using all available views; do not claim accurate aircraft or engine geometry from one angle. For branded vehicles use authoritative blueprints/multi-view photos and lawful assets. Engine CAD requires actual dimensions for mechanical accuracy.
2. **Asset sourcing:** choose high-quality legally usable models or create clean topology; classify licensed / procedural / placeholder. Avoid cubes and cylinders as the only final asset detail, except explicitly labelled scene blockouts.
3. **Geometry:** correct scale, normals, smoothing, UV topology and vertex organization; moving parts as separate named objects; LODs and collision proxies; verify imports and exports (GLB, glTF, FBX where supported, source BLEND).
4. **Shading:** PBR metallic-roughness, albedo, normal and roughness maps, clearcoat for vehicles, glass transparency, decals, snow/wetness accumulation and weather-specific roughness, day/night lighting.
5. **Scene:** global terrain and routes; credible zoning and house variation; clustered vegetation; weather; time of day and camera. For urban settings use streaming/chunking, instancing, LOD and distance fog, not a single massive scene draw call.
6. **Animation:** rigged moving wheels/doors/gear/flaps/control surfaces, engine crank/cam motion, camera behavior and mechanical constraints. Create appropriate real-time controls and collision where requested.
7. **Quality:** render multiple cameras (front, rear, top and silhouette-critical angles); verify perspective and collisions; tri counts, material/texture budgets, render frame times **on target hardware**.

## Target tiers

- `blockout` = procedural coarse geometry, routes, collision layout, made for iteration and **not visual fidelity**.
- `game-ready` = detailed sourced/generated geometry, optimized topology, working interactions, stable shader, export QA.
- `simulator-grade` = documented geometric fidelity, organized mechanisms, calibrated motion and behavior, high-detail LOD0 plus low-cost LODs.
- `cinematic` = offline render targeting photographic fidelity; must not be passed off as interactive 60fps.

The local tool `create_city_blockout` genuinely exports a navigable 3D GLB mesh but at blockout tier only. `create_blender_recipe` prepares a Cycles/EEVEE render script with studio lights for user-supplied meshes and does not manufacture detailed aircraft or auto-render without Blender.
