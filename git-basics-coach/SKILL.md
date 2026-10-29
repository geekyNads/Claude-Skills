---
name: git-basics-coach
description: Teach git and GitHub by doing it on the user's real project — init, commit, branch, push, pull request — explaining each command in one line the first time, with safe habits and no scary operations. Use when the user is new to git, says "how do I save my code", "push to GitHub", "what is a branch/commit/PR", "make a repo", or hasn't committed in a long time.
---

# Git Basics Coach

Teach through the project in front of you, not theory. Explain each new command once, in one line, then just use it.

## The mental model (say it once)

- **Commit** = a save point with a note. You can always go back to it.
- **Branch** = a parallel copy to try something without touching the working version.
- **Push** = upload your commits to GitHub.
- **Pull request (PR)** = "please review and merge my branch into main".

## First time on a project

```bash
git init
```
```bash
git add .
```
```bash
git commit -m "Initial commit"
```
Before the first `git add`, check that `.gitignore` covers `node_modules`, `.env*`, and build folders (`secrets-guard`).

Put it on GitHub. The user creates the repo, or with the GitHub CLI and their OK:
```bash
gh repo create my-app --private --source=. --push
```

## The everyday loop

1. `git switch -c feat/contact-form`: new branch for the feature
2. Build a working slice (`build-in-slices`)
3. `git add -A && git commit -m "Add contact form with validation"`: save point
4. `git push -u origin feat/contact-form`: upload
5. `gh pr create --fill`: open a PR, review it, merge on GitHub
6. `git switch main && git pull`: get the merged result

## Good commit messages

Imperative and specific: "Add dark mode toggle", "Fix crash when cart is empty". Not "stuff", "fix", or "update".

## Safe habits

- Commit every time something works
- Check `git status` before and after, so you know what's going on
- Never commit secrets. Never force-push to `main`.
- Stuck or messed up? Use `safe-undo`, and don't panic-delete the folder.

## Common confusions

- "Changes not staged" = edited but not added yet
- "Your branch is behind" = run `git pull`
- Merge conflict = two edits to the same lines. Open the file, keep the right parts, remove the `<<<<<<<` markers, then commit. Offer to walk through it.
