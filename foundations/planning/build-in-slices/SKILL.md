---
name: build-in-slices
description: Build features as thin, runnable vertical slices — one small change, run it, check it, commit it, then the next — so a beginner never ends up with 40 broken files. Use when building any feature or milestone, when the user says "build X", "add Y", "let's start", or when a request is big enough that doing it in one go is risky.
---

# Build in Slices

The number one vibecoding failure is "Claude wrote 2,000 lines and nothing works". The fix is small steps that each end in something working.

## The loop (repeat per slice)

1. **Name the slice.** Each slice is a single thing the user can see or click. "Show the list of tasks (fake data)" is a slice. "Set up the backend" is not.
2. **Say the plan in 2–4 lines** before writing code: files touched and what will be visible afterward.
3. **Build only that.** No "while I'm here" extras.
4. **Run it.** Start the dev server, open the page, and check the console. Use the browser tool to look if one is available.
5. **Show the user** what changed, with a screenshot or exact steps to see it.
6. **Commit** with a clear message (`git-basics-coach`). Now there's a safe point to return to.
7. **Next slice.**

## Slicing a feature: example "task app"

1. Static page with 3 hard-coded tasks
2. Add-task input that adds to the list (in memory)
3. Tasks persist after refresh (localStorage or DB)
4. Mark done / delete
5. Empty state + loading state
6. Style polish

Each one is runnable. If slice 4 breaks, slices 1–3 still work.

## Rules

- **At most around 150 lines changed per slice.** If a slice needs more, split it.
- **Fake data first, real data second.** UI with hard-coded data makes it obvious what the backend needs.
- **Never move on while broken.** If a slice fails, fix it or revert to the last commit (`safe-undo`). Don't stack fixes on a broken base.
- After 3 failed attempts on the same thing, switch to `stuck-breaker`.

## Report per slice

```
✅ Slice 2: Add-task input works
Changed: components/AddTask.tsx (new), app/page.tsx
Try it: type a task, press Enter, and it appears at the top
Next: make tasks survive refresh
```
