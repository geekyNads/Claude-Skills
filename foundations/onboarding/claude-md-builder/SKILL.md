---
name: claude-md-builder
description: Create or improve a project's CLAUDE.md — the file Claude reads every session — with the real run/test/build commands, stack, folder map, conventions, and do/don't rules, kept short. Use when the user says "set up CLAUDE.md", "/init", "Claude keeps forgetting X", "Claude keeps doing Y wrong", or starts a new project.
---

# CLAUDE.md Builder

`CLAUDE.md` is loaded into every session in that folder. A good one stops Claude repeating the same mistakes. A bloated one wastes usage, so keep it **under about 60 lines**.

## 1. Discover, don't guess

Read `package.json` scripts / `pyproject.toml` / `Makefile`, the folder structure, lint configs, README, and the existing `CLAUDE.md`. Run the dev, test, and build commands to confirm they actually work.

## 2. Template

```markdown
# <Project>
<One line: what it is and who it's for.>

## Commands
- Dev: `npm run dev` (http://localhost:3000)
- Test: `npm test`
- Lint/typecheck: `npm run lint && npx tsc --noEmit`
- Build: `npm run build`

## Stack
Next.js (App Router), Tailwind, Supabase, deployed on Vercel.

## Where things live
- `app/`: pages and routes
- `components/`: shared UI
- `lib/`: helpers, API clients

## Rules
- Use existing components in `components/ui` before creating new ones.
- Never commit `.env*`. Secrets come from env vars.
- Run lint + build before saying a task is done.
- <project-specific rule the user cares about>
```

## 3. What belongs and what doesn't

- **In:** commands, non-obvious conventions, gotchas Claude hit before, and the user's strong preferences.
- **Out:** anything Claude can read from the code itself, long docs (link them instead), and generic advice like "write clean code".

## 4. Teaching moment

Tell the user: "When Claude does something you don't like twice, add a one-line rule here." Show them that `#` at the start of a message (in the terminal) or just asking "add this to CLAUDE.md" saves a rule.

If a `CLAUDE.md` already exists, edit it: tighten, dedupe, and fix stale commands. Don't replace it wholesale.
