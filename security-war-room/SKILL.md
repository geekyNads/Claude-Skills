---
name: security-war-room
description: Pre-production security gauntlet. Splits into three adversarial subagents — Hacker (finds every vulnerability), White Hat (patches what it can without touching the core architecture), Analyst (rules which findings need real changes to the main code). Use before shipping to production, before merging a release branch, or when the user says "war room", "attack my code", "pentest the codebase", or "is this safe to ship".
---

# Security War Room

Three subagents fight over the codebase. The Hacker attacks, the White Hat defends, and the Analyst referees. Nothing ships until the Analyst signs off.

Only run this against code the user owns or is authorized to test. All attacks are **static and local**: read the code, run the project's own tests, and run local scanners. Never attack live production hosts or third-party services, and never exfiltrate real secrets. If you find a secret, report its location in redacted form.

## 0. Recon (you, before spawning)

Map the target in a few tool calls. Collect:
- the languages, frameworks, and package managers in use
- entry points: HTTP routes, CLI args, queue consumers, webhooks, file uploads, cron jobs
- trust boundaries: user input, auth/session layer, database, external APIs, LLM/tool calls
- deploy surface: Dockerfiles, IaC, CI workflows, `.env*` files, `vercel.json`/`vercel.ts`
- the **core frame**, meaning the files that define the architecture: data models/schema, the auth flow, the routing skeleton, and the public API contracts. Write this list down, because it is the line the White Hat may not cross.

Put all of this in a short `RECON` block, which gets passed to every agent.

## 1. Hacker (round 1)

Spawn with `Agent` (subagent_type `general-purpose`, or `ecc:security-reviewer` if available). The agent is **read-only and may not edit files.** Use this prompt:

> You are an attacker preparing to breach this codebase before it reaches production. RECON: <paste>.
> Find every exploitable weakness. Cover the known classes **and** reason from first principles about novel ones specific to this app's logic.
>
> Known classes to sweep at minimum:
> - Injection: SQL/NoSQL, command, LDAP, XPath, template (SSTI), header/CRLF, log injection, prompt injection into LLM calls
> - XSS (stored, reflected, DOM), CSRF, clickjacking, open redirect
> - AuthN/AuthZ: broken auth, IDOR/BOLA, privilege escalation, missing auth on routes, JWT flaws (alg none, weak secret, no expiry), session fixation
> - SSRF, path traversal, unsafe file upload, zip slip, XXE
> - Insecure deserialization, prototype pollution, mass assignment
> - Secrets in code, git history, logs, client bundles, or error messages
> - Crypto: weak hashing, hardcoded keys/IVs, `Math.random` for tokens, missing TLS verification
> - Race conditions/TOCTOU, double-spend, missing idempotency
> - Business-logic abuse: negative quantities, skipped workflow steps, replay, coupon/limit bypass
> - DoS: ReDoS, unbounded queries/uploads, missing rate limits, N+1 amplification
> - Supply chain: vulnerable/typosquatted deps, unpinned versions, postinstall scripts, risky CI (`pull_request_target`, secret exposure)
> - Misconfig: CORS `*` with credentials, debug mode, verbose errors, missing security headers, permissive IAM/IaC, exposed admin panels
> - Data exposure: PII in logs, over-fetching APIs, missing field-level filtering
>
> "Unknown" hunting: for each trust boundary, ask "what does the developer *assume* here that an attacker controls?" Chain low-severity bugs into high-impact paths.
>
> Run available local tooling where it exists, and do not fail if it's missing: `npm audit`/`pnpm audit`, `pip-audit`, `cargo audit`, `govulncheck`, `semgrep --config auto`, `gitleaks detect`, `trivy fs .`.
>
> Output a list of findings. Each one has: `ID`, `title`, `class`, `severity` (Critical/High/Medium/Low, CVSS-style reasoning), `file:line`, `attack path` (concrete steps/payload an attacker would use), and `confidence` (confirmed/likely/speculative). Do not propose fixes.

## 2. White Hat (round 1)

Spawn after the Hacker returns. This agent **may edit files**, within limits. Use this prompt:

> You are a defender. Here are the Hacker's findings: <paste>. RECON and the CORE FRAME list: <paste>.
> Fix every finding you can **without changing the core frame**. Allowed:
> - input validation/sanitization at the boundary, output encoding, parameterized queries at the call site
> - security headers, CORS, cookie flags, rate limiting via existing middleware
> - config hardening (debug off, error verbosity, TLS verify on)
> - dependency bumps within the same major version, pinning, removing unused deps
> - moving hardcoded secrets to env vars (and flagging the secret for rotation)
> - adding authz checks inside existing handlers using the app's existing auth helpers
> - safer stdlib calls (constant-time compare, `secrets`/`crypto.randomBytes`)
>
> NOT allowed: changing schemas/data models, redesigning the auth flow, altering public API contracts, restructuring modules, adding new frameworks, or bumping a major version. If a fix needs any of these, **do not attempt it** and mark it `ESCALATE`.
>
> Keep each diff minimal. After you patch, run the project's existing tests/lint/build.
> Output one row per finding ID: `FIXED` (with files changed + what you did), `PARTIAL` (with what is mitigated and what remains), or `ESCALATE` (why the core frame blocks it). Also report test/build results verbatim if anything fails.

## 3. Hacker (round 2): the fight

Re-spawn the Hacker (or `SendMessage` the original) with the White Hat's patch report:

> Here are the defender's patches: <paste>. Try to **bypass each FIXED/PARTIAL patch**: encoding tricks, alternate routes to the same sink, case/unicode normalization, race windows, other callers of the same function that weren't patched. Also check that the patches did not introduce new bugs. Output: `ID → HOLDS` or `ID → BYPASSED (how)`, plus any new findings.

If anything is BYPASSED, send it back to the White Hat for one more round. **Cap the fight at 3 rounds.** After that, whatever is still open goes to the Analyst as-is.

## 4. Analyst: the verdict

Spawn this agent read-only, with all findings, patch reports, and bypass results. Use this prompt:

> You are the security analyst and referee. Inputs: <findings, patches, bypass rounds, CORE FRAME>.
> For every finding, decide:
> 1. **Resolved**: the patch held under attack. Verify by reading the diff yourself.
> 2. **Needs core change**: the vulnerability is architectural. Explain *why* a surface patch can't fix it, which core files must change, the recommended redesign, and the estimated blast radius.
> 3. **Accepted risk / false positive**: justify it with a concrete reason, not a vibe.
>
> Also catch White Hat overreach: flag any patch that quietly crossed into the core frame or broke behavior.
> Give a final **SHIP / SHIP WITH CONDITIONS / DO NOT SHIP** verdict. Any open Critical or High that needs a core change means DO NOT SHIP.

## 5. Report to the user

Give the user one table and nothing else noisy:

| ID | Severity | Vulnerability | Location | Status | Needs core change? |
|----|----------|---------------|----------|--------|--------------------|

Then add:
- **Verdict** (from the Analyst)
- **Core changes required**: one short paragraph each, ordered by severity
- **Secrets to rotate**, if any were found
- **What changed**: the files the White Hat touched (the user reviews the diff, and nothing is committed automatically)
- **Not covered**: anything that needs runtime/DAST testing, infra access, or manual review that static analysis can't prove

## Rules

- Never commit, push, or deploy. The user reviews the White Hat's diff first.
- The Hacker and the Analyst never edit files, and only the White Hat writes.
- Severity must come with an attack path. Use "speculative" when one isn't proven, and never inflate.
- No agent can promise zero unknown vulnerabilities. Say what was covered and what wasn't.
- On large repos, split the Hacker by area (e.g. API, frontend, infra) into parallel subagents, then merge their findings before the White Hat runs.
