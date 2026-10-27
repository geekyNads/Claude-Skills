# Claude Skills

Custom Claude Code skills. Each folder is one skill (`<name>/SKILL.md`).

## Install

```bash
git clone https://github.com/geekyNads/Claude-Skills.git ~/Desktop/skills
for d in ~/Desktop/skills/*/; do ln -sfn "$d" ~/.claude/skills/$(basename "$d"); done
```

Restart Claude Code (or start a new session) and the skills appear in the list.
