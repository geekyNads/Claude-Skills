---
name: vibe-check-review
description: Beginner-friendly review of AI-written code before trusting it — does it actually work, is anything dangerous (security, data loss, cost), what's fragile, what's unnecessary — explained in plain words with a traffic-light summary. Use when the user says "is this code good", "review what you built", "can I trust this", "check before I ship", or after a big AI-generated change.
---

# Vibe Check Review

AI code often *looks* right. This review checks whether it **is** right, explained so a beginner learns what to look for.

## Run it first

Run the build, lint, typecheck, and tests, then click through the main flow. Code that doesn't run fails the review immediately.

## Check, in priority order

**🔴 Dangerous (must fix)**
- Secrets in code or frontend (`secrets-guard`)
- Data that isn't scoped per user: can user A see or edit user B's stuff?
- Server endpoints with no auth check
- User input going straight into SQL, HTML (`dangerouslySetInnerHTML`, `innerHTML`), shell commands, or file paths
- Anything that deletes data without confirmation
- Unbounded loops or API calls that could run up a bill (AI, SMS, email)

**🟡 Fragile (should fix)**
- No error handling on network or database calls
- Missing loading, empty, and error states
- Hardcoded values that should be config (URLs, prices)
- Copy-pasted logic in 3+ places
- Packages added that aren't used, or are huge for a tiny job

**🟢 Fine / nitpicks (optional)**
- Naming, formatting, small refactors

## Output

```
Overall: 🟡 Works, 2 things to fix before shipping

🔴 app/api/notes/route.ts:14 — anyone can delete any note by id.
   Why it matters: a stranger could wipe your users' data.
   Fix: check note.userId === currentUser.id before deleting.

🟡 components/Upload.tsx:30 — no error shown if upload fails; user sees nothing.
   Fix: catch the error, show "Upload failed, try again".

🟢 Looks good: clear structure, env vars used correctly, forms validated.
```

Rules: point to `file:line`, explain *why it matters* in one human sentence, and offer to fix the 🔴/🟡 items. Don't pad with nitpicks. For a deep security pass before production, suggest `security-war-room`.
