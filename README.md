# Claude Skills

Custom Claude Code skills, organized as `domain/subdomain/skill/SKILL.md`.

## Install

```bash
git clone https://github.com/geekyNads/Claude-Skills.git ~/Desktop/skills
~/Desktop/skills/install.sh
```

Restart Claude Code (or start a new session) and the skills appear in the list. Skill names don't include the folders, so you still call them as `/ship-pr`.

After every `git pull` that adds or moves a skill, run `install.sh` again. It links each skill flat into `~/.claude/skills`, because Claude Code only looks one level deep there.

## Folder map

| Domain | Subdomain | Skills |
|---|---|---|
| `foundations` | `onboarding` | `claude-onboarding`, `prompt-coach`, `claude-md-builder`, `codebase-tour` |
| | `planning` | `idea-to-plan`, `stack-picker`, `build-in-slices` |
| `engineering` | `frontend` | `landing-page-starter`, `design-to-code`, `premium-ui-pass`, `forms-that-work`, `accessibility-basics` |
| | `backend` | `add-auth`, `add-database`, `connect-api`, `ai-feature-starter` |
| | `troubleshooting` | `error-explainer`, `stuck-breaker`, `safe-undo`, `run-locally`, `dependency-doctor` |
| `quality` | `review` | `vibe-check-review`, `first-tests`, `cleanup-pass`, `docs-compliance` |
| | `security` | `secrets-guard`, `security-war-room` |
| `delivery` | `git` | `git-basics-coach`, `ship-pr` |
| | `release` | `deploy-first-app`, `launch-checklist`, `readme-writer` |
| `workflow` | `sessions` | `token-saver`, `session-handoff` |
| | `professional` | `work-mail`, `internship-autopilot` |

New skill? Put it in the subdomain it fits, add it to this table, and run `install.sh`.

## New to Claude? Follow this path

Each skill kicks in automatically when you ask for what it covers, or call it by name (`/claude-onboarding`).

**1. Getting started**
1. `claude-onboarding`: modes, permissions, and how to ask
2. `idea-to-plan`: turn an idea into a small MVP plan
3. `claude-md-builder`: give Claude your project's rules
4. `prompt-coach`: turn vague asks into clear prompts
5. `stack-picker`: choose a beginner-friendly stack
6. `codebase-tour`: understand an existing repo

**2. Building**
7. `build-in-slices`: one small working step at a time
8. `design-to-code`: turn a screenshot or design into UI
9. `landing-page-starter`: build a landing page from a one-line pitch
10. `add-database`: save real data
11. `add-auth`: add login, safely
12. `connect-api`: use third-party APIs without leaking keys
13. `forms-that-work`: validation and every form state
14. `ai-feature-starter`: add AI with the Claude API

**3. Debugging**
15. `error-explainer`: errors in plain English
16. `stuck-breaker`: escape fix-loops
17. `safe-undo`: go back without losing work
18. `run-locally`: get any project running
19. `dependency-doctor`: fix install hell

**4. Quality and safety**
20. `secrets-guard`: keep keys out of git
21. `vibe-check-review`: can you trust the AI code?
22. `first-tests`: the few tests that matter
23. `cleanup-pass`: remove AI leftovers
24. `accessibility-basics`: usable by everyone

**5. Shipping**
25. `git-basics-coach`: commit, branch, and PR
26. `deploy-first-app`: get a live URL
27. `readme-writer`: make the repo look pro
28. `launch-checklist`: go/no-go before launch

**6. Habits**
29. `token-saver`: stretch your usage limits
30. `session-handoff`: never lose progress between sessions

## Pro skills

- `ship-pr`: branch, verify, and PR, never merged
- `docs-compliance`: make code match the project docs
- `premium-ui-pass`: responsive, polished, SEO-ready UI
- `work-mail`: reports and emails from real repo state
- `security-war-room`: hacker vs white hat vs analyst before production
- `internship-autopilot`: find, filter, auto-apply to LinkedIn internships, and reach out to job posters
