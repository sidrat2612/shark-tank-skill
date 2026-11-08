#!/usr/bin/env bash
# Install the shark-tank skill by copying files, for people who do not use the plugin marketplace.
#
#   curl -fsSL https://raw.githubusercontent.com/sidrat2612/shark-tank-skill/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/sidrat2612/shark-tank-skill/main/install.sh | bash -s -- --project
#
# Default target is ~/.claude (all projects). --project installs into ./.claude (this project only).
set -euo pipefail

REPO="https://github.com/sidrat2612/shark-tank-skill.git"
TARGET="$HOME/.claude"
if [[ "${1:-}" == "--project" ]]; then
  TARGET="$(pwd)/.claude"
fi

command -v git >/dev/null || { echo "git is required" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --depth 1 --quiet "$REPO" "$TMP/shark-tank-skill"
SRC="$TMP/shark-tank-skill"

mkdir -p "$TARGET/skills" "$TARGET/agents"
for skill in shark-tank newshark; do
  rm -rf "$TARGET/skills/$skill"
  cp -R "$SRC/skills/$skill" "$TARGET/skills/$skill"
done
cp "$SRC"/agents/shark-*.md "$TARGET/agents/"

echo "Installed shark-tank into $TARGET"
echo "Restart Claude Code, then try:  /shark-tank I'm asking 100k for 10% of my coffee subscription"
