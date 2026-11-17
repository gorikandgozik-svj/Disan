#!/usr/bin/env bash
# Optional manual release helper for an already prepared repository.
# CI publishes v1.2.2 only after the complete Tests workflow succeeds.
set -euo pipefail
command -v gh >/dev/null || { echo 'Install GitHub CLI: https://cli.github.com/'; exit 1; }
gh auth status
gh repo view gorikandgozik-svj/Disan >/dev/null
if gh release view v1.2.2 --repo gorikandgozik-svj/Disan >/dev/null 2>&1; then
  echo 'v1.2.2 already exists; no duplicate release created.'
  exit 0
fi
echo 'For a public release, verify GitHub Actions Tests are green and run:'
echo 'gh release create v1.2.2 --repo gorikandgozik-svj/Disan --title "VIBE VISUAL FORGE 1.2.2" --notes-file RELEASE_NOTES.md'
