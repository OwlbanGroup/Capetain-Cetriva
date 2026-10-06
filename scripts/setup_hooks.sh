#!/usr/bin/env bash
# Install git pre-commit hooks
set -euo pipefail

HOOKS_DIR="$(pwd)/hooks"
TARGET_DIR=".git/hooks"

echo "Installing git hooks from $HOOKS_DIR to $TARGET_DIR..."

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "No .git/hooks directory found. Are you in a git repo?"
    exit 1
fi

cp -f "$HOOKS_DIR/pre-commit" "$TARGET_DIR/pre-commit"
chmod +x "$TARGET_DIR/pre-commit"

echo "Git hooks installed successfully."
echo "Run git commit --no-verify to bypass in emergencies."
