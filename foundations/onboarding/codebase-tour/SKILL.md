---
name: codebase-tour
description: Explain an unfamiliar codebase in plain English — what the app does, how a request flows, what each folder is for, where to make common changes — without overwhelming a beginner. Use when the user says "explain this project", "what does this code do", "I cloned this, where do I start", "walk me through the code", or joins an existing repo.
---

# Codebase Tour

Explain the project like giving a tour of a house: the rooms first, then how people move through them, then where the light switches are.

## 1. Explore quickly

Read the README, the package/dependency file, the entry points (`app/`, `src/main`, `index`, `manage.py`), the routing, and the config. Skim, don't read every file. For big repos, use an Explore subagent.

## 2. Deliver the tour in this order

**What it is** (2 lines): what the app does and who uses it.

**Tech stack** (one line each, with plain-English roles):
- Next.js: builds the pages and the server
- Prisma: talks to the database

**Map** (only folders that matter):
```
app/          → pages users see (each folder = a URL)
app/api/      → backend endpoints
components/   → reusable UI pieces
lib/          → helper code (database, auth, utils)
prisma/       → database structure
```

**One journey traced end to end.** Pick the main action (e.g. "user signs up"): which file shows the form, then where it's sent, then what saves it, then what the user sees next. Give `file:line` for each hop.

**Where to change common things:**
- Colors/fonts → `tailwind.config.ts` / `globals.css`
- Add a page → new folder in `app/`
- Env vars → `.env.local` (copy from `.env.example`)

**How to run it:** the exact commands, or hand off to `run-locally`.

## Rules

- Define every term the first time you use it, in one short clause.
- Use 5–8 folders at most in the map. Hide the noise.
- End with: "Want me to go deeper on any part?"
