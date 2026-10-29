---
name: idea-to-plan
description: Turn a vague app idea into a small, buildable MVP plan — the problem, the user, 3–5 core features, what's explicitly out, a stack, and milestones that each end in something runnable. Use when the user says "I have an idea", "I want to build an app that…", "help me plan", or starts a project with no clear scope.
---

# Idea to Plan

Beginners fail by building too much at once. Your job is to shrink the idea until it can ship in days, not months.

## 1. Interview, at most 5 questions

Ask only what you can't infer:
1. Who is it for? Name one specific person or group.
2. What problem does it solve for them, in one sentence?
3. What is the **one** action they must be able to do?
4. Web, mobile, or both? If they're unsure, default to web.
5. Any deadline, budget, or must-use tool?

## 2. Write the plan as `PLAN.md`

```
# <App name>
**One-liner:** <who> can <do what> so that <benefit>.

## MVP features (max 5)
1. ...
## Not in v1 (on purpose)
- payments, admin panel, notifications, ... (whatever is tempting but not core)

## Screens
- <Screen>: what's on it, what the user can do

## Data
- <Thing>: fields

## Stack
<from stack-picker, with one-line reasons>

## Milestones (each ends runnable)
1. Static UI with fake data, so they can click through it
2. Real data saved and loaded
3. Accounts (only if needed)
4. Deployed live URL
```

## 3. Rules

- If there are more than 5 features, cut. Move the extras to "Not in v1" and say why.
- Every milestone ends with something they can **open and click**.
- If the idea needs something hard (realtime, payments, AI, maps), flag it as the main risk and put it in an early milestone.
- Plain words only. Define any technical term in one short clause.

## 4. Hand-off

Ask: "Want me to start milestone 1?" Then build it with `build-in-slices`. If there's no `CLAUDE.md` yet, suggest `claude-md-builder` first.
