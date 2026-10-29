---
name: session-handoff
description: Write a short handoff note so the next session (or the work after a usage-limit reset, or a teammate) continues instantly — goal, what's done, what's in progress, exact next steps, decisions, gotchas, how to run. Use when the user says "save progress", "I'm about to hit my limit", "continue tomorrow", "hand this off", "summarize where we are", or a long session is ending mid-task.
---

# Session Handoff

## 1. Gather the truth

Run `git status`, `git log --oneline -10`, and `git branch --show-current`, and check open PRs (`gh pr list`). Re-check the last thing you ran (does it build? are tests passing?). Don't write from memory alone.

## 2. Write `HANDOFF.md` in the project root

```markdown
# Handoff — <date>

## Goal
<What we're building and why, 1–2 lines.>

## Done
- ✅ <feature> (commit abc123 / PR #4)

## In progress
- 🔨 <task> — <exact state: "form UI done, API route returns 500 on submit">
  Files: app/api/contact/route.ts, components/ContactForm.tsx

## Next steps (in order)
1. <specific, actionable — "Fix 500: RESEND_API_KEY missing from .env.local">
2. …

## Decisions made (don't revisit)
- Using Supabase, not Firebase, for auth + DB (free tier, SQL)

## Gotchas
- Dev server must run on port 5173 (CORS allowlist)

## How to run
`npm install && npm run dev`, then open http://localhost:5173
Branch: feat/contact-form
```

## 3. Rules

- Make next steps concrete enough that someone with **no context** could start in 1 minute.
- Record the *why* of decisions, so the next session doesn't redo them.
- Never put secrets in the handoff. Name the env var, not its value.
- Ask the user before committing it. Add it to `.gitignore` if they don't want it in the repo.

## 4. Resuming

Tell the user: start a new session and say **"Read HANDOFF.md and continue from Next steps."** When resuming, verify the state first (git, build) before continuing, then update or delete the file once it's done.
