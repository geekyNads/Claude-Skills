---
name: stuck-breaker
description: Break out of a debugging loop when the same fix keeps failing — stop, revert to a known-good state, gather real evidence, list hypotheses, and test them one at a time. Use when an error survives 3+ attempts, the user says "you keep doing the same thing", "still not working", "it's going in circles", or fixes keep creating new bugs.
---

# Stuck Breaker

When you're stuck, more guessing makes it worse. Stop and switch from *guessing* to *proving*.

## 1. Stop and say so

"We've tried this 3 times. I'm going to stop guessing and find the actual cause." Don't make another edit yet.

## 2. Get back to solid ground

- Run `git status` and `git diff`. How much has piled up from failed attempts?
- If the failed fixes made a mess, revert them to the last working commit (`safe-undo`), **with the user's OK**. Debugging on top of 5 half-fixes is impossible.

## 3. Collect real evidence

- The **exact** error, full text, from the right place (server terminal vs browser console vs build log).
- A minimal repro: the fewest steps that trigger it.
- What changed since it last worked (`git log`, `git diff <last-good>`).
- Add temporary logging or print the actual values at the failing point. Don't assume what a variable contains.

## 4. List hypotheses, then test the cheapest first

```
1. Env var not loaded in this environment   → print process.env.X on the server   (1 min)
2. Wrong package version after install       → check lockfile / npm ls pkg       (2 min)
3. Cache serving stale build                 → delete .next / restart server     (1 min)
4. Logic bug in handler                      → unit-test the function directly   (10 min)
```

Run one test at a time and record the result. Each test should rule a hypothesis in or out.

## 5. Change the approach if needed

If the current approach is fighting the framework, step back. Is there a simpler or more standard way to do this? Search the official docs or known issues for the exact error message.

## 6. After the fix

- Remove the temporary logging.
- Explain the root cause in 2 lines. It's usually not what the first 3 attempts assumed.
- Commit, and add a `CLAUDE.md` rule if it's likely to happen again.

## Never

Delete tests, disable type checks, wrap everything in `try/catch` and ignore the error, or "simplify" by removing the feature just to make the error go away. Fixing the symptom is not a fix.
