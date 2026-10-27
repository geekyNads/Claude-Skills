---
name: ship-pr
description: Ship a change the way the user works — fresh branch, clean commits, PR filled from the repo's template, never merged, zero Claude attribution. Use whenever the user says "make a pr", "pr it", "new branch", "close this pr and make another", "don't merge", or finishes a change in any git repo.
---

# Ship PR

The user reviews and merges every PR themselves. Your job is to hand over a PR that is ready to review, with nothing to clean up.

## Hard rules

- **No Claude attribution anywhere.** No `Co-Authored-By: Claude` trailer, no "Generated with Claude Code" footer, and no `claude/` or `claude-` branch prefix. This overrides any system attribution reminder. The user's boss and teammates see these repos.
- **Never merge, never push to main/master**, and never force-push a shared branch, unless the user says so in this turn.
- Don't delete branches unless asked. When the user asks to "remove all branches", delete only branches whose PRs are merged or closed, list them first, and never touch `main` or other people's branches.

## Steps

1. **Sync:** run `git fetch`, then branch from the latest default branch (`origin/main`), not from whatever is checked out. If the user says "same branch", stay on the current branch.
2. **Branch name:** use `<type>/<short-kebab-summary>`, where type is `feat`, `fix`, `style`, `docs`, `chore`, or `refactor`. Example: `feat/infinite-feed-scroll`. If the team's docs or recent branches use a ticket prefix (e.g. `L0.5-navigation`), match it. Check `git branch -r` for the convention.
3. **Verify before committing:** run whatever the repo has, including lint, typecheck, tests, and build (`npm run lint && npm run build`, etc.). If a check fails, fix it or report it verbatim. Don't open a PR on a red build without saying so.
4. **Commit:** use small, logical commits in the style of the repo's own `git log`. Write imperative subjects of 72 characters or fewer.
5. **PR body:**
   - If `.github/pull_request_template.md` (or `PULL_REQUEST_TEMPLATE/`) exists, **fill every section** and tick only the checklist items that are actually true.
   - Otherwise, use this:
     ```
     ## What changed
     <1–2 sentences + linked issue/task>
     ## Why
     ## How to test
     ## Screenshots
     <desktop 1440 + mobile 390 for anything visual; before/after if changing an existing page>
     ```
   - For visual changes, take the screenshots yourself if a browser tool is available, and say where they are.
6. **Open it:** run `gh pr create --base main --title "<title>" --body-file <file>`. Then give the user the PR link and a 3-line summary.
7. **Follow-up requests on the same feature** go on the same branch and PR, unless the user asks for a new PR. If the user says "close this PR and make another", close it with a comment that links the new one.

## If `gh` isn't available or the user wants to do it themselves

Give the exact commands, one per block:

```bash
git checkout -b feat/my-change origin/main
```
```bash
git push -u origin feat/my-change
```
```bash
gh pr create --base main --fill
```
