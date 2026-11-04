---
name: claude-onboarding
description: First-15-minutes guide for someone new to Claude Code — what it is, how permissions and modes work, plan mode, how to phrase requests, and the five habits that separate good vibecoding from chaos. Use when the user says they're new, "how do I use Claude", "teach me Claude Code", "where do I start", or seems unsure how to work with you.
---

# Claude Onboarding

Teach by doing. Keep each step short, run something real, and stop after each step to check that it made sense. Use no jargon without a one-line definition.

## Step 1: What Claude Code is (30 seconds)

Claude can read your files, run commands, and edit code in the folder you opened. It **asks before** risky actions, depending on the permission mode. Your job is to describe what you want and review what it did.

## Step 2: Permission modes

- **Default:** asks before edits and commands. Best for learning.
- **Accept edits:** edits files without asking, but still asks before running commands.
- **Plan mode:** reads and plans only, with no changes. Use it before any big feature.
- **Auto:** works mostly on its own. Use it once you trust the flow.

In the terminal, `Shift+Tab` cycles through the modes. In the desktop app, the mode picker is by the input box.

## Step 3: Your first real task

Pick something tiny in their project (or a fresh folder): "Create an index.html that says hello with a nice gradient background, then open it." Show them how to:
1. read the plan or diff before approving,
2. approve or reject a step,
3. ask for a change in plain words ("make the text bigger").

## Step 4: How to ask well

| Weak | Strong |
|---|---|
| "make a website" | "Make a one-page site for my bakery: hero with name + tagline, menu section with 6 items, contact form. Mobile-first, warm colors." |
| "fix it" | "Clicking Submit shows a blank page. Expected: success message. Here's the console error: …" |

The formula: **goal + context + constraints + what done looks like.** For more practice, point them to the `prompt-coach` skill.

## Step 5: Five habits

1. **Plan before big changes.** Use plan mode or "give me a plan first".
2. **Work in small slices.** Make one feature, run it, check it, then do the next (`build-in-slices`).
3. **Commit often.** Git is your undo button (`git-basics-coach`, `safe-undo`).
4. **Read what Claude changed.** You're the reviewer, not a passenger.
5. **Start fresh for new tasks.** `/clear` keeps answers sharp and saves usage (`token-saver`).

## Useful commands

- `/init`: create a `CLAUDE.md` for the project (`claude-md-builder`).
- `/clear`: start a fresh conversation.
- `/compact`: shrink a long conversation.
- `Esc` stops Claude mid-action. `Esc Esc` rewinds to an earlier point.
- `@path/to/file` points Claude at a specific file.

## What next

Once the first task works, suggest `idea-to-plan` to scope their actual project.
