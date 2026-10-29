---
name: forms-that-work
description: Make forms production-ready — labels, client + server validation, inline errors, loading/disabled submit, success and failure states, no double submits, accessible and mobile-friendly. Use when building any form (signup, contact, checkout, settings) or when the user says "the form doesn't work", "add validation", or "nothing happens when I click submit".
---

# Forms That Work

A form has 5 states: **empty → typing → submitting → success → error.** Beginner forms usually handle only the first one.

## Checklist

**Structure**
- Every input has a visible `<label>` (not just a placeholder)
- The right `type` and `autocomplete` (`email`, `tel`, `new-password`, …) so mobile keyboards and autofill work
- A real `<form>` with `onSubmit`, so Enter submits

**Validation (both sides)**
- Client: instant feedback when a field loses focus or on submit, shown **under the field** in plain words ("Enter a valid email")
- Server: validate again with the same schema. **Client validation is for UX. Server validation is for security.**
- Share one schema where possible (Zod for TypeScript, Pydantic for Python)

**Submitting**
- Disable the button and show a spinner or "Saving…" while the request runs, which prevents double submits
- Keep what the user typed if it fails. Never clear the form on error.

**Results**
- Success: a clear message or redirect, and reset the form if it makes sense
- Error: a human message ("Couldn't send, check your connection and try again"), not `Error: 500`
- Focus moves to the first invalid field

**Accessibility**
- Link errors to fields with `aria-describedby`, set `aria-invalid` on bad fields
- Tap targets of 44px or more, visible focus outline

**Abuse (public forms)**
- Rate-limit the endpoint
- Add a honeypot field or captcha service for contact and signup forms

## Verify

Walk through all 5 states in the browser: submit empty, submit bad data, submit good data, then simulate a failure (offline or a forced error). Screenshot each state for the user.
