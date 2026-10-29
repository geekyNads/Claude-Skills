---
name: readme-writer
description: Write a README that makes a project instantly understandable and impressive — what it is, a screenshot/demo, features, tech stack, how to run it, env vars, and roadmap — based on the actual code, not guesses. Use when the user says "write a README", "make my repo look professional", "document this project", or before sharing a repo/portfolio piece.
---

# README Writer

A README is the project's landing page. Recruiters, users, and future-you read the top 20 lines, then leave.

## 1. Gather facts from the code

The `package.json`/dependency file (stack, scripts), `.env.example` (setup), routes and pages (features), the deploy config (the live URL), the license file, and any screenshots in the repo. Ask the user for the live URL and the "why" if you can't find them.

## 2. Structure

```markdown
# <Name>
<One line: what it does and for whom.>

<Live demo link> · <screenshot or GIF>

## Features
- <user-facing benefit, not implementation>
- …(3–6)

## Tech stack
Next.js · TypeScript · Tailwind · Supabase · Vercel

## Getting started
### Prerequisites
Node 22+, a Supabase account
### Setup
​```bash
git clone …
cd …
npm install
cp .env.example .env.local   # fill in values (see below)
npm run dev
​```
### Environment variables
| Name | What it's for | Where to get it |
|---|---|---|

## Project structure (optional, 5–8 lines)

## Roadmap
- [ ] …

## License
```

## 3. Rules

- **Every command must actually work.** Run the setup steps yourself if you can.
- Put the screenshot near the top. Take one with the browser tool if there isn't one, and save it as `docs/screenshot.png`.
- Badges are optional. Keep to 3 at most, and only if they're real (build status, license).
- No invented features, stats, or users.
- For a portfolio or founder project, add a short "Why I built this" (2–3 lines) in the user's voice.

Keep it scannable: short sections, real headings, and code blocks for every command.
