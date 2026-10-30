---
name: internship-autopilot
description: Find, score, and auto-apply to remote internships on LinkedIn, then connect with each job's poster, using the bundled `internpilot` CLI (scrape → filter → Easy Apply → outreach) with daily caps and dry runs. Use when the user says "find me internships", "apply to internships for me", "auto-apply on LinkedIn", "internships that pay more than X", "reach out to the recruiters", or wants the job hunt to keep running on its own.
---

# Internship Autopilot

A local pipeline (Python + Playwright + SQLite) that does the internship hunt end to end:

1. **scrape**: LinkedIn's logged-out job endpoints → listings + full descriptions
2. **filter + score**: remote only, monthly pay above a threshold, resume-skill match, mills and impossible roles dropped
3. **apply**: walks LinkedIn Easy Apply, answers screening questions from `config.json`, submits
4. **outreach**: sends a connection request (with a short note) to the "Meet the hiring team" poster

The code lives next to this file in `internpilot/`. Copy the folder into the user's projects (e.g. `~/code/internpilot`) and run it there.

## Before anything: say the risk out loud

Automated applying and connection requests break LinkedIn's User Agreement and can get the account restricted. Tell the user once, plainly, and recommend dry runs plus the daily caps (15 applies, 10 invites). If they still want full automation, that's their call.

Never type the user's password. Never bypass bot checks (CAPTCHAs, Google's "browser may not be secure" block). The user signs in by hand once in the app's own browser profile.

## Setup

```bash
cp -r <this skill>/ ~/code/internpilot && cd ~/code/internpilot
cp config.example.json config.json   # then fill in YOUR-… placeholders from the resume
uv sync && uv run playwright install chromium
uv run python test_pipeline.py      # must print "all checks passed"
uv run python -m internpilot login  # user signs in, then presses Enter in that terminal
```

**Fill `config.json` from the resume, not from guesses:** skill keywords, `skill_years` (honest numbers, 0 for skills not on the resume), graduation year, city, links. Remove any answer you can't back with a fact.

**Login gotchas:**
- "Continue with Google" fails in Playwright's Chromium ("Couldn't sign you in"). Have the user sign in with LinkedIn email + password. If they've only used Google, they set a password with "Forgot password?" first.
- If the `login` prompt never gets the Enter (it went to another window), the session is usually saved anyway: check `~/.internpilot/chrome-profile/Default/Cookies` was just modified, stop the process with SIGINT, and continue.

## Running it

```bash
uv run python -m internpilot scrape            # fetch + score; prints eligible/ineligible counts
uv run python -m internpilot list              # ranked queue with pay, flags, links
uv run python -m internpilot apply --dry-run   # goes to the Submit button, then discards
uv run python -m internpilot apply             # real submissions (daily cap applies)
uv run python -m internpilot outreach --dry-run
uv run python -m internpilot run               # scrape + apply + outreach
uv run python -m internpilot status            # counts + screening questions it couldn't answer
uv run python -m internpilot answer "<regex>" "<value>"   # teach an answer, re-queue blocked jobs
```

Always dry-run first on a new machine or after LinkedIn changes its UI. Run long jobs in a visible terminal tab so the user can watch and Ctrl-C.

## Rules while applying

- **Unknown screening question → stop, don't guess.** The app discards the application and logs the question. Ask the user, save it with `answer`, re-run. Personal facts (license, degree completed, location, interest in X) always come from the user.
- **Honest answers beat passing filters.** "Bachelor's completed?" is No for a current student, even if it screens them out.
- **Untick "Follow <company>"** on the review page. The app does this; check it if you ever submit by hand.
- **Check before reporting.** Only report "applied" when LinkedIn shows "Application submitted", and "sent" when the profile shows "Pending".
- **The outreach note is text you wrote, so get the user's OK** before the first real send. Show the exact rendered note (max 200 chars). Once they approve the template, later runs may use it.
- Already-applied jobs are detected and skipped. Non-Easy-Apply jobs are marked `external`. Point the user to the company site, or draft an email if the company's form fails.

## Refining the filters (do this after every scrape)

Read the descriptions of anything borderline before applying:
```bash
sqlite3 internpilot.db "select company, substr(description,1,600) from jobs where status='eligible'"
```
Watch for, and encode in `config.json`:
- **Mills:** many near-identical posts, "Up to ₹X performance-based", 1–3 months, same template across company names. Add to `blocklist` (names are normalized, so "Medi Nex" = "MediNex").
- **Graduation-year limits** ("2026/2027 graduate", "2025 and 2026 batch only"): `disqualifiers` drops them.
- **Experience floors** ("2+ years"), unpaid, in-office.

Then `rescore` and re-check `list`. Add a test line to `test_pipeline.py` for every filter you change.

## LinkedIn quirks the code already handles (check here first when something breaks)

- **Guest API rate limits (HTTP 429):** sequential requests with a delay, backoff on 429. Never fire dozens in parallel.
- **The `f_WT=2` remote filter is ignored for guests:** remote is detected from the description text instead.
- **Pay:** monthly ₹ from ranges, `k`, `/yr` (÷12), `LPA`. Amounts under ₹1,000 are ignored (plan prices). Unknown pay is allowed by default (`allow_unknown_pay`).
- **Easy Apply question text isn't in a `<label>`/`<legend>`:** radio groups contain only "Yes No", and the question sits in a parent element. `_nearby_text` climbs ancestors to find it. If missing questions come back as "Yes", this broke.
- **The resume picker is also a radio group:** it's pre-checked, so it's skipped.
- **"Meet the hiring team" is a `<p>`**, and profile pages have no `<h1>`. The name comes from the page title "(3) Jane Doe | LinkedIn".
- **Connect is often under "More"**, and the sidebar has "Invite <someone else> to connect". Only click `[aria-label="Invite <full name> to connect"]`.

When a selector breaks, don't guess: write a 20-line Playwright script that opens the page in the same profile (`open_browser`) and prints the relevant DOM, then fix from what it shows.

## Report back

After each run, give a table: company · role · status · the screening answers it gave. Then list unanswered questions, external roles, and any invites sent. Keep `config.json` and the DB local (`.gitignore` covers `internpilot.db`). Never commit the user's phone number or answers to a public repo.
