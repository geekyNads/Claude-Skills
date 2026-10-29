---
name: landing-page-starter
description: Build a clean, responsive, conversion-focused landing page from a one-line pitch — hero, problem, features, social proof, CTA, footer — with real copy, SEO basics, and a working signup/contact form. Use when the user says "make a landing page", "I need a website for my product/startup/portfolio", "waitlist page", or "coming soon page".
---

# Landing Page Starter

A landing page has one job: get the visitor to take **one** action (sign up, join the waitlist, book a call, download).

## 1. Get the inputs (ask only for what's missing)

- Product name + one-line pitch
- Who it's for
- The ONE call to action
- Brand colors or logo (optional; otherwise pick a tasteful palette)

## 2. Sections (in this order; skip what doesn't apply)

1. **Nav:** logo, 2–3 links, CTA button
2. **Hero:** headline (benefit, under 10 words), subheadline (how, 1–2 lines), primary CTA, visual (product shot, illustration, or gradient)
3. **Problem:** 3 pains the audience feels
4. **How it works / Features:** 3–4 items, each with an icon + short title + one line
5. **Social proof:** testimonials, logos, numbers. **Use clearly marked placeholders**, never fake quotes presented as real.
6. **FAQ:** 4–6 real objections answered
7. **Final CTA:** repeat the action
8. **Footer:** links, socials, ©year, privacy/terms links

## 3. Copy rules

- Talk about benefits, not features: "Get paid in 2 days", not "Automated invoicing engine".
- Use "you" more than "we".
- Use one CTA label everywhere ("Join the waitlist").

## 4. Technical baseline

- Fully responsive (check 390 and 1440), fast, with no layout shift
- Title, meta description, OG image tags, favicon
- A form that actually works. Use the stack's form handling, or a simple serverless route that stores emails (`connect-api` / `add-database`), with success and error states (`forms-that-work`).
- Subtle scroll animations only, respecting reduced-motion

## 5. Finish

Run it, screenshot desktop and mobile, and list the placeholders the user must replace. For more polish, hand off to `premium-ui-pass`. To put it live, use `deploy-first-app`.
