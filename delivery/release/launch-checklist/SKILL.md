---
name: launch-checklist
description: Pre-launch audit before sharing an app with real users — works on phone and desktop, errors tracked, analytics on, SEO/social previews, privacy/terms pages, backups, cost limits, security basics — producing a go/no-go list. Use when the user says "ready to launch", "going live", "sharing it tomorrow", "Product Hunt", or "what am I missing before launch".
---

# Launch Checklist

Run through it, check each item yourself where possible, and report ✅ / ❌ / ⚠️ with fixes.

## Works
- [ ] Main flow works end to end on the **live** URL (not just localhost)
- [ ] Mobile (390px) and desktop both look right, with nothing clipped
- [ ] Every form, button, and link works, with no 404s
- [ ] Loading, empty, and error states exist (`forms-that-work`)
- [ ] Tested in Chrome and Safari

## Doesn't break silently
- [ ] Error tracking (Sentry, or the host's logs) so you hear about crashes
- [ ] Friendly 404 and error pages
- [ ] Database backups are on (check the provider setting)

## People can find and share it
- [ ] Title, meta description, favicon
- [ ] Open Graph image, so links look good on WhatsApp, X, LinkedIn, and Slack
- [ ] `sitemap.xml` + `robots.txt`
- [ ] Analytics are on (Vercel Analytics, Plausible, PostHog) to see if anyone comes

## Safe
- [ ] No secrets in code or the frontend (`secrets-guard`)
- [ ] Users can only see their own data (`add-auth`)
- [ ] Rate limits on signup, contact, and AI endpoints
- [ ] Spending limits or alerts set on paid APIs (AI, SMS, email, hosting)
- [ ] Production keys used, not test keys (for payments, switch to Stripe live mode deliberately)

## Legal and trust (if collecting any user data)
- [ ] Privacy policy page and terms page. A generated template is fine for v1. Say it's not legal advice.
- [ ] Contact or support email visible
- [ ] Cookie notice if using non-essential cookies or tracking in regions that require it

## Output

```
Verdict: ⚠️ Ready after 3 fixes
❌ No OG image — links will show blank previews (10 min fix)
❌ /api/contact has no rate limit — spam risk
⚠️ No error tracking — you won't know if it breaks
✅ Everything else (14 items)
```

Offer to fix the ❌ items. For a deeper security pass, suggest `security-war-room`. For polish, suggest `premium-ui-pass`.
