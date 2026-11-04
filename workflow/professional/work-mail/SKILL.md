---
name: work-mail
description: Draft work reports and emails from the real state of the repo — findings reports after reading docs, "what I did in this PR" notes to a lead, credit-splitting notes when two people shared a task, and polite question emails. Use when the user says "write a mail to <name>", "write a report", "explain what I did", "these are my findings", or "give me the whole explanation in N points".
---

# Work Mail

The user is a developer who also reports to leads and works alongside teammates. This skill turns what actually happened (the docs, diffs, commits, and PR) into messages they can send without editing.

## Ground everything in evidence first

Before writing, gather the facts:
- **For a PR:** `gh pr view`, `git log origin/main..HEAD`, `git diff --stat origin/main`, and the task list or ticket.
- **For a findings report:** the docs you read and what they say.
- **For a shared task:** split commits by author (`git log --format='%an %s'`) so credit is accurate.

Never invent work, numbers, or status. If you don't know something, ask, or leave a `[fill in]` placeholder.

## Formats

**Findings report** (a file, e.g. `<name>.md`):
- A summary of what each doc covers, organized by type or topic in the format the user or team specifies.
- Only what the docs say. **Contradictions and open questions go in the email, not the file.**

**Email to a lead, findings or update:**
```
Subject: <Project> — <what this is about> (<date or task ID>)

Hi <Name>,

<1 line: what I did / where it is>

<3–5 bullets: key points, each one line>

A few questions:
1. <polite, specific question — e.g. "Doc 04 says X while doc 07 says Y; which should I follow?">

<1 line: next step + when>

Thanks,
<User's name>
```

**PR note when work was shared** (short, one per recipient):
- What <teammate> did, then what I did, then where it stands (PR link, what's left).
- Give fair, specific credit, and don't inflate anyone's role.

**"Explain in N points":** exactly N points, one or two sentences each, in plain language.

## Tone

Polite and direct, the way a junior engineer writes to a senior one: not grovelling, no filler ("I hope this email finds you well"), and no exclamation marks. Phrase a contradiction or problem as a question, not an accusation. Keep it short enough to read on a phone.

## Never

- Send anything. Only draft. The user sends.
- Mention AI tools or Claude in the drafts.
- Put internal doubts or contradictions into committed files.

If the user pastes back the version they actually sent, update any related file (report, notes) to match it.
