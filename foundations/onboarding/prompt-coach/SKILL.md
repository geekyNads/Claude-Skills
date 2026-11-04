---
name: prompt-coach
description: Rewrite a vague request into a strong prompt and teach why — goal, context, constraints, definition of done, examples. Use when the user says "how should I ask this", "improve my prompt", "Claude isn't getting what I want", or sends a very short/ambiguous request and is learning.
---

# Prompt Coach

Show the before and the after, explain the difference in one line per change, then offer to run the improved prompt.

## The formula

1. **Goal:** what you want, in one sentence.
2. **Context:** which files, what exists already, who it's for.
3. **Constraints:** stack, style, what not to touch, limits.
4. **Done looks like:** how you'll know it worked (what you see, a test passing).
5. **Examples (optional):** a screenshot, a link, sample input and output.

## Output format

```
Your prompt:
> make the login better

Stronger:
> On the login page (app/login/page.tsx), add: show/hide password toggle,
> inline error under each field, a loading spinner on the button while
> submitting, and a "Forgot password?" link (can be a placeholder for now).
> Keep the current colors. Done = I can see each state on mobile and desktop.

Why it's better:
- Names the file, so there's no searching or guessing
- Lists exact changes instead of "better"
- Says what NOT to change (colors)
- Defines done, so you both know when to stop
```

## Teaching tips (mention once, briefly)

- One task per message. Split "build login AND dashboard AND emails".
- For bugs: what you did, what you expected, what happened, and the exact error text.
- For UI: attach a screenshot or reference site.
- For big things: ask for a plan first ("don't code yet, plan it").
- If Claude gets it wrong, say **what** was wrong, not just "no".

Don't lecture. If the original prompt was already good, say so and run it.
