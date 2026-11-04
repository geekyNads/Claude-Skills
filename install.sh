#!/bin/sh
# Link every skill into ~/.claude/skills. Claude Code only looks one level deep there,
# so nested skills in this repo get flat links. Safe to re-run after every pull.
set -eu
repo=$(cd "$(dirname "$0")" && pwd)
dest=${SKILLS_DIR:-$HOME/.claude/skills}
mkdir -p "$dest"
find "$repo" -name SKILL.md -not -path '*/.git/*' | while read -r file; do
  skill=$(dirname "$file")
  link="$dest/$(basename "$skill")"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "skipped $(basename "$skill"): $link is a real folder, not a link" >&2
    continue
  fi
  ln -sfn "$skill" "$link"
  echo "linked ${skill#"$repo"/}"
done
