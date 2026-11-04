---
name: error-explainer
description: Turn a scary error message or stack trace into plain English — what it means, the exact line causing it, the fix, and how to avoid it next time — then apply the fix. Use when the user pastes an error, a red terminal/console screenshot, "it's broken", "what does this mean", or a stack trace.
---

# Error Explainer

## 1. Find the line that matters

Stack traces are long, but the useful part is usually:
- the **first line**: the error type and message,
- the **first frame in the user's own code**: skip `node_modules`, `site-packages`, and framework internals.

Open that file at that line before explaining anything.

## 2. Explain in this format

```
What happened: <one plain sentence, no jargon>
Where: src/app/page.tsx:42 — <the line>
Why: <the actual cause in this code, not a generic definition>
Fix: <what you'll change>
Avoid next time: <one habit or check>
```

Example:
```
What happened: The page tried to read the name of a user that doesn't exist yet.
Where: app/profile/page.tsx:18 — user.name
Why: The data is still loading the first time the page draws, so user is undefined.
Fix: Show a loading state until user exists (user?.name, plus a skeleton).
Avoid next time: Always handle the "loading" and "not found" cases when fetching data.
```

## 3. Then fix it

Apply the fix and **re-run the exact thing that failed** to confirm it's gone. If there's a new error, repeat. After 3 rounds on the same problem, switch to `stuck-breaker`.

## Common translations (only when relevant)

- `undefined is not a function` / `Cannot read properties of undefined`: something you expected to exist doesn't, yet
- `Module not found`: wrong import path, or the package isn't installed
- `CORS`: the browser blocked a request to another site. Call it from your server instead.
- `Hydration mismatch`: the server and the browser drew different HTML (dates, random numbers, `window` during render)
- `EADDRINUSE`: something is already running on that port
- `401` / `403`: not logged in / not allowed
- `500`: the server crashed. Check the **server** terminal, not the browser.

Ask for the full error text if they only sent part of it. A screenshot of half an error wastes a round trip.
