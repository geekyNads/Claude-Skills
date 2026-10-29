---
name: connect-api
description: Connect a third-party API (weather, payments, maps, email, AI, any REST service) safely — keys in env vars, calls from the server, typed responses, error/timeout/rate-limit handling, and caching. Use when the user says "use the X API", "fetch data from", "integrate Stripe/Resend/OpenWeather/etc.", or pastes API docs.
---

# Connect an API

## 1. Read the docs first

Use the documentation tool (Context7), the official docs site, or the user's pasted docs. Find: the base URL, how auth works (header, query key, OAuth), the exact endpoint, request and response shape, rate limits, and the free tier. Don't guess endpoints from memory.

## 2. Keys

- The user signs up and gets the key. You never create accounts or enter their credentials.
- Put the key in `.env.local` (e.g. `WEATHER_API_KEY=`) and add the name to `.env.example`.
- **The key is only used on the server.** Browser code calls *your* API route, which calls the third party. A key in frontend code is public to everyone.

## 3. Write one small client

```ts
// lib/weather.ts
export async function getWeather(city: string) {
  const res = await fetch(`https://api.example.com/weather?q=${encodeURIComponent(city)}`, {
    headers: { Authorization: `Bearer ${process.env.WEATHER_API_KEY}` },
    signal: AbortSignal.timeout(8000),
  });
  if (!res.ok) throw new Error(`Weather API ${res.status}`);
  return res.json() as Promise<Weather>;
}
```

- Encode user input (`encodeURIComponent`) and validate it.
- Set a timeout, because a hanging API shouldn't hang your app.
- Type the response with only the fields you use.

## 4. Handle the unhappy paths

- Errors → show a friendly message, log the details on the server
- 429 rate limit → back off, or cache
- Empty results → an empty state, not a crash
- Cache responses that don't change often (minutes or hours) to save quota and speed things up

## 5. Webhooks (if the API calls *you*, e.g. Stripe)

Verify the signature with the provider's secret before trusting the payload, and make the handler safe to run twice.

## 6. Verify

Call it for real from the app, show the result, then break it on purpose (wrong key, offline) and confirm the error state works.
