#!/usr/bin/env bash
# Release helper for an already published GitHub repository.
set -euo pipefail
command -v gh >/dev/null || { echo 'Install GitHub CLI: https://cli.github.com/'; exit 1; }
gh auth status
gh repo view gorikandgozik-svj/Disan >/dev/null
gh release create v1.1.0 --repo gorikandgozik-svj/Disan --title 'VIBE VISUAL FORGE 1.1.0' --notes-file RELEASE_NOTES.md
