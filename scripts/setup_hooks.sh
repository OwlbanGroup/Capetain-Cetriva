#!/bin/sh
# One-time setup: point git at the repo-managed hooks directory so every
# clone of this repository gets the same quality gates.
set -e
git config core.hooksPath hooks
echo "Hooks enabled: $(git config core.hooksPath)"
