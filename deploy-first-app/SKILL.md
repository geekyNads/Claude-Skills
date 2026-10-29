---
name: deploy-first-app
description: Take a beginner's app from localhost to a live public URL — usually Vercel via GitHub — with env vars, a production build check, database/auth production settings, and an optional custom domain. Use when the user says "deploy", "put it online", "host it", "get a link to share", "go live", or "it works locally but not deployed".
---

# Deploy Your First App

## 1. Pre-flight (local)

- `npm run build` (or the equivalent) **passes locally**. Most deploy failures are just build errors.
- No secrets in code. `.env*` is git-ignored (`secrets-guard`).
- The code is pushed to GitHub (`git-basics-coach`).

## 2. Pick the host

| App | Host |
|---|---|
| Next.js, React, Vite, Astro, static sites, Node/Python APIs | **Vercel** (default) |
| Long-running servers, websockets-heavy, Docker apps | Railway / Render / Fly.io |
| Mobile (Expo) | EAS Build → app stores |

## 3. Deploy on Vercel

**Easiest:** the user imports the GitHub repo at vercel.com/new. After that, every push to `main` deploys automatically, and every PR gets a preview URL.

**From the terminal:**
```bash
npm i -g vercel
```
```bash
vercel
```
```bash
vercel --prod
```

## 4. Environment variables (the number one "works locally, broken live" cause)

Add every variable from `.env.example` in Project → Settings → Environment Variables, or with `vercel env add NAME`. Then **redeploy**, because env changes only apply to new deployments. Use production keys, not test ones, when going truly live.

## 5. Production settings for connected services

- Database: use the provider's pooled or serverless connection string
- Auth: add the live URL to allowed redirect/callback URLs, or login will fail
- Webhooks (Stripe, etc.): point them at the live URL
- CORS / allowed origins: include the live domain

## 6. Check the live site

Open the URL. Click through sign up, the core feature, and forms. Check the browser console and the host's function logs. Check on a phone.

## 7. Custom domain (optional)

The user buys the domain. Add it in Project → Domains and set the DNS records the dashboard shows. HTTPS is automatic.

## Report

The live URL, how future deploys happen ("push to main"), and where to see logs.
