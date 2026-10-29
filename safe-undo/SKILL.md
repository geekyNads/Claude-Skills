---
name: safe-undo
description: Undo changes without panic — Claude's rewind/checkpoints, git restore for files, git revert for commits, stash for "save for later" — choosing the least destructive option and confirming before anything irreversible. Use when the user says "undo", "go back", "revert", "it was working before", "I broke everything", or "restore the old version".
---

# Safe Undo

Always pick the **least destructive** undo that solves the problem. Before anything that throws work away, show what will be lost and get a yes.

## First, see what you have

Run `git status`, `git log --oneline -10`, and `git stash list`. Tell the user in plain words: "You have 4 changed files that aren't saved in git yet, and your last commit was 'add login page' 20 minutes ago."

## Pick the right tool

| Situation | Do this | Destroys work? |
|---|---|---|
| Undo what Claude just did in this conversation | Claude Code rewind: `Esc Esc`, or `/rewind`, and pick the point | Only edits after that point |
| Undo changes to one file (not committed) | `git restore path/to/file` | Yes, that file's unsaved changes |
| Undo all uncommitted changes | `git stash` (recoverable!) rather than `git restore .` | No, stash keeps them |
| Undo the last commit but keep the changes | `git reset --soft HEAD~1` | No |
| Undo a commit that's already pushed/shared | `git revert <hash>` (adds a new "undo" commit) | No, history kept |
| Get back to how it was at a commit, to compare | `git switch -c test-old <hash>` | No, new branch |
| "I deleted/reset something by mistake" | `git reflog` shows where you were, then `git switch -c rescue <hash>` | No |

## Rules

- **Never run** `git reset --hard`, `git clean -fd`, `git push --force`, or delete branches without showing exactly what will be lost and getting an explicit yes.
- Prefer `stash` and new branches. They're reversible.
- After undoing, run the app to confirm it's actually back to working.

## Teach the habit

"Commit every time something works, even small things. Then undo is always one command away." Point them to `git-basics-coach`.
