---
name: add-auth
description: Add sign-up/login to an app the safe way — using an auth provider instead of hand-rolled passwords — with protected pages, the current user in the UI, and per-user data. Use when the user says "add login", "sign in with Google", "user accounts", "only logged-in users can see this", or "protect this page".
---

# Add Auth

**Rule number one: don't write your own password storage, sessions, or JWT logic.** Use a provider. Hand-rolled auth is the most common way vibecoded apps get hacked.

## 1. Pick a provider

| Stack | Default |
|---|---|
| Next.js | **Clerk** (fastest), or **Auth.js** / **Better Auth** (self-hosted, free) |
| Already on Supabase | **Supabase Auth** |
| Mobile (Expo) | Clerk or Supabase Auth |

If the project already has auth, use it.

## 2. Set up

1. The user creates the provider account and copies the keys. You never enter their credentials.
2. Put the keys in `.env.local` and add placeholders to `.env.example`. The secret key stays server-only. Only `NEXT_PUBLIC_*`/publishable keys may reach the browser.
3. Install the SDK and add the provider wrapper per its current docs (check the docs, not memory).
4. Add sign-in, sign-up, and sign-out UI. Use the provider's prebuilt components first.

## 3. Protect things (the part beginners skip)

- **Pages:** redirect logged-out users using middleware or a server-side check.
- **API routes and server actions:** check the user **on the server** in every handler. Hiding a button is not security.
- **Data:** every query filters by the current user's id (`where user_id = currentUser.id`). Otherwise user A can read user B's data by changing an id in the URL.

## 4. Verify

- Logged out → protected page redirects to login
- Sign up → land on the dashboard with the name/avatar shown
- User A cannot see User B's data. Test with two accounts in two browsers.
- Sign out → can't go back with the browser's back button

## Explain once

*Authentication* = who you are (login). *Authorization* = what you're allowed to do (permissions). You need both.
