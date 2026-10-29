---
name: token-saver
description: Teach habits that stretch Claude usage limits and keep answers sharp — fresh sessions per task, compacting, pointing at exact files, not pasting huge logs, right-sized models, CLAUDE.md instead of repeating yourself. Use when the user says "I hit my limit", "usage ran out", "Claude is getting slow/confused", "how do I save tokens", or a session has become very long.
---

# Token Saver

Everything in the conversation is re-read on every message. Long, messy sessions cost more **and** make Claude worse. Here's how to stay lean.

## The big wins

1. **One task, one session.** Finished a feature? Run `/clear` and start fresh. Carry over only what matters (`session-handoff`).
2. **`/compact` when a session gets long** but you're mid-task. It summarizes the history and keeps going.
3. **Point, don't paste.** Say "fix the bug in `@app/cart/page.tsx`" instead of pasting the whole file. Claude reads only what it needs.
4. **Trim logs.** Paste the error and the relevant 20 lines, not 2,000 lines of build output.
5. **Put repeated instructions in `CLAUDE.md`** ("always use Tailwind", "run lint before done") instead of re-typing them every session (`claude-md-builder`).
6. **Be specific up front.** A clear prompt (`prompt-coach`) avoids 3 rounds of "no, I meant…".
7. **Plan big things first.** A 1-minute plan beats an hour of building the wrong thing.
8. **Right-size the model.** Use a faster or cheaper model for simple edits and questions, and the strongest one for hard design or debugging. Switch with `/model`.

## Smaller wins

- Ask for "just the diff" or "just the fix" when you don't need explanations
- Don't ask Claude to re-read the whole codebase. Name the area.
- Large searches across the repo can go to a subagent, which keeps the main conversation small.
- Check what's using space with `/context`, if available.

## When you hit the limit

- Before it resets, ask Claude to write the `session-handoff` note so nothing is lost.
- After the reset, start a new session, then say "read HANDOFF.md and continue".

Give the user the 3 tips most relevant to how they've been working, not the whole list.
