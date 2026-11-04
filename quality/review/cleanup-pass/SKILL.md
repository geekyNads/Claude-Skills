---
name: cleanup-pass
description: Clean up the mess vibecoding leaves behind — unused files, dead code, duplicate components, leftover console.logs, unused packages, commented-out blocks, inconsistent naming — without changing behavior, verified by build and a click-through. Use when the user says "clean up the code", "the project is messy", "remove unused stuff", or after a long build session.
---

# Cleanup Pass

**Rule: behavior must not change.** If you're unsure whether something is used, leave it and list it.

## 1. Safety first

Make sure everything is committed (`git status` clean), or create a branch. Run build and tests to record a baseline.

## 2. Find the junk

- **Unused files and exports:** `npx knip` (JS/TS), or `vulture` (Python). Also grep for each suspicious file's name before deleting.
- **Unused packages:** `npx depcheck` / `knip`. Verify with a grep.
- **Leftover debugging:** `console.log`, `print(`, `debugger`, `TODO remove`
- **Commented-out code blocks:** delete them, since git remembers
- **Duplicates:** two components or functions doing the same thing (`Button.tsx` and `Button2.tsx`, three date formatters). Merge into one.
- **Abandoned attempts:** `page-old.tsx`, `backup/`, `test2.js`, `copy of …`
- **Inconsistent naming:** mixed `camelCase`/`snake_case` file names in the same folder

## 3. Clean in small commits

One kind of cleanup per commit ("remove unused deps", "merge duplicate Button"), so any single one can be reverted.

## 4. Verify

Run the build, lint, and tests, and click through the main pages. Compare with the baseline.

## 5. Report

```
Removed: 9 unused files, 4 unused packages, 23 console.logs
Merged: Button + Button2 → components/ui/Button.tsx
Left alone (unsure, please check): lib/legacy-api.ts — no imports found, but referenced in a comment
Bundle/deps: 4 fewer packages
```

Don't refactor architecture or restyle code in a cleanup pass. That's a separate task.
