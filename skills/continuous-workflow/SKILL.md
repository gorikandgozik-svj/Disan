---
name: continuous-workflow
description: "Use implicitly when the user asks for automated visual project improvement, continuous monitoring, iterative QA, build loops or a no-@ assistant for visual development."
---

# Continuous workflow (accurate autonomy)

On an active user task, orchestrate: inspect -> spec -> build -> render -> compare -> repair -> test -> deliver. Repeat while there are feasible actionable steps and an available runtime/time budget. The plugin cannot by itself wake ChatGPT in the background, grant permanent access to a PC, change product-wide auto-activation, or guarantee availability across every chat/client. `allow_implicit_invocation: true` allows relevant automatic skill selection **when the host selects it**; it does not run tools unprompted forever. Do not claim a 24/7 service has been installed.

In a supported desktop host, the bundled local MCP `visual-forge-local` provides design-spec/prototype/blockout/render-recipe/QA tools. These only run when the host supports stdio/local Python and has access to the filesystem. Mobile ChatGPT cannot start this stdio server. For truly always-on local execution, explicitly install a separate supervised service with scoped permissions, crash-restart, progress state, human approval for installations/deletions/cloud costs, and stop/pause controls; that daemon is not provisioned by uploading this plugin.

A robust improvement loop must have a target (reference or acceptance criteria), observable changes, tests and a maximum attempts/time budget to prevent uncontrolled cost, accidental file corruption or infinite spin. Preserve project backups; log changes and test results. A test failure must result in a concrete remediation or a transparent limitation.

## Cross-platform 1.2.0 clarification

The public HTTPS MCP tools are stateless. Local PWA storage does not sync across devices. The background Python queue operates only while the PC worker is running. No durable 24/7 cloud queue, host-wide automatic execution or guaranteed uptime exists. For mobile and desktop tools use the `cross-platform` skill; never imply a remote GPU or autonomous background run was provisioned.
