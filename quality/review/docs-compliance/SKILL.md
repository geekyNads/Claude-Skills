---
name: docs-compliance
description: Read every project doc (design.md, technical docs, CONTRIBUTING, ADRs, numbered docs folders), turn them into a checklist of concrete rules, then either implement to spec or audit the code against it with doc citations. Use when the user says "check the docs", "read the docs and implement", "follow the docs", "cross check the code against the docs", or drops a new design/technical doc into the repo.
---

# Docs Compliance

The user's projects run on docs written by them or their team: `design.md`, technical specs, numbered docs like `00–12`, and `ASSETS.md`. The code has to match those docs, so this skill checks the code against them instead of guessing.

## 1. Find every doc

Glob for `**/*.md`, `docs/**`, `reference/**`, `design*`, `*SPEC*`, `CONTRIBUTING*`, `.github/*.md`, `*.mdx`. Skip `node_modules`, `CHANGELOG`, and vendored folders. Read them **in full**, in the order they're numbered or linked. Read images referenced as specs too (logos, favicons, mockups).

## 2. Extract the rules

Build a checklist where each line has a rule ID, the rule, its source `doc:line`, and whether it is testable:

```
R-07  Header and footer share one nav list (src/lib/navigation.ts)   docs/04-nav.md:12   testable
R-12  Primary brand green #1FAF5A, radius 16px on cards              design.md:30         testable
R-19  Copy tone: friendly, no exclamation marks                      design.md:88         judgement
```

Keep only concrete, checkable rules (colors, spacing, file locations, naming, API shapes, required states, accessibility, folder structure). Drop vague aspirations.

Also list:
- **TODOs or gaps:** things the docs mark as undecided.
- **Contradictions:** where two docs disagree. **Don't resolve these yourself.** Collect them as questions for the user or their lead.

## 3. Then act on the mode

- **Implement mode** ("implement the docs", "proceed accordingly"): build to the checklist. Where something isn't decided yet, use an obvious placeholder (`/* TODO(docs): ... */`) and list **every file:line** where a placeholder appears, so the user can fill them in.
- **Audit mode** ("cross check", "does it follow the docs"): don't edit. For each rule, give one of:
  `PASS` · `FAIL file:line — what's wrong` · `N/A` · `CAN'T VERIFY — why`

## 4. Report

1. A compliance table: rule, status, location.
2. Failures, ordered by how visible or user-facing they are.
3. Placeholders and their locations.
4. Open questions (contradictions and gaps). **Keep these out of committed files**, because the user prefers to raise them politely in a message to their lead, not in the repo.

Run the repo's lint, typecheck, and build at the end, and report the results verbatim. "Follows the docs" also means it builds without errors.

If the user wants a PR afterwards, hand over to the `ship-pr` skill.
