---
name: stack-picker
description: Recommend a beginner-friendly tech stack for a specific project — frontend, backend, database, auth, hosting — with one-line reasons and an honest note on what's hard. Use when the user asks "what should I build this with", "which framework", "React or Next", "what database", or is starting a project without a stack.
---

# Stack Picker

Pick **one** stack and commit to it. Beginners lose weeks comparing frameworks. Optimize for: lots of tutorials and examples, a generous free tier, deploying in one command, and Claude knowing it well.

## Defaults (change one only when there's a reason)

| Need | Default | Why |
|---|---|---|
| Website / web app | **Next.js + TypeScript + Tailwind** | One framework for pages and API, huge ecosystem, deploys to Vercel instantly |
| Simple static site | **Plain HTML/CSS** or **Astro** | No build complexity |
| Database | **Postgres via Supabase or Neon** | Free tier, real SQL, dashboard to see your data |
| Auth | **Clerk** or **Supabase Auth** | Login without writing password code |
| File uploads | **Vercel Blob** or **Supabase Storage** | Simple API |
| Payments | **Stripe** | The standard, great test mode |
| AI features | **Claude API** (via AI SDK or the Anthropic SDK) | See `ai-feature-starter` |
| Hosting | **Vercel** | Push to GitHub and get a live URL |
| Mobile app | **Expo (React Native)** | One codebase for iOS and Android, test on your phone instantly |
| Python / data / ML | **FastAPI** + **Streamlit** for quick UIs | Simple, fast to ship |
| Chrome extension | Plain JS + Manifest V3 | No framework needed |

## Output

```
For <project>:
- Frontend: … because …
- Backend: … because …
- Data: … because …
- Auth: … (or "not needed for v1")
- Hosting: …
Hardest part for a beginner: <one honest sentence>
Free to start: yes/no (what costs money later)
```

## Rules

- If the user already knows a stack, use it unless it's a terrible fit. Familiarity beats "best".
- Don't add services the MVP doesn't need (no Redis, queues, or microservices for v1).
- Mention cost honestly: what's free now and what costs money at scale.
