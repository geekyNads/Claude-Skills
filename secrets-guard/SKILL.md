---
name: secrets-guard
description: Keep API keys, passwords, and tokens out of code, git, logs, and the browser — env vars, .gitignore, .env.example, server-only usage, scanning for leaks — and walk through what to do if one leaked. Use when adding any API key, creating .env files, before the first push/deploy, or when the user says "I pushed my key", "is my key safe", or "where do I put my API key".
---

# Secrets Guard

A leaked key on GitHub is found by bots within minutes and can cost real money. Prevention takes 2 minutes.

## Setup (do this once per project)

1. `.gitignore` includes:
   ```
   .env
   .env.*
   !.env.example
   ```
2. `.env.example` lists every variable name with a fake value and a comment saying where to get the real one:
   ```
   # https://dashboard.stripe.com/test/apikeys
   STRIPE_SECRET_KEY=sk_test_xxx
   ```
3. Real values go in `.env.local` (local) and the hosting dashboard (production, `deploy-first-app`).

## Rules

- **Never** hardcode keys in source, even "just for testing".
- **Secret keys run on the server only.** Anything prefixed `NEXT_PUBLIC_` / `VITE_` / `EXPO_PUBLIC_` is shipped to every visitor's browser. Only publishable or anon keys go there.
- Don't log secrets or full request headers, and don't put them in error messages or URLs.
- Don't paste real keys into chat. Claude doesn't need the value, only the variable name.

## Scan before pushing

- `git diff --cached` and look for anything key-like (`sk_`, `AKIA`, `ghp_`, `-----BEGIN`, `password=`)
- If available: `gitleaks detect` or `trufflehog git file://.`
- Check that no `.env` file is tracked: `git ls-files | grep -i env`

## If a key leaked

1. **Rotate it first.** Revoke the key in the provider's dashboard and create a new one. The user does this, and it's the only real fix. Deleting the file doesn't help, because it's in git history and bot caches.
2. Update the new key in `.env.local` and the hosting env vars.
3. Remove it from the code, and add the `.gitignore` rule if it was missing.
4. Check the provider's usage and billing for abuse.
5. Optional: scrub history (`git filter-repo`), but only after rotating, and only with the user's OK, since it rewrites history.

Stay calm and explain each step. Rotation matters most; everything else is cleanup.
