---
name: premium-ui-pass
description: Take a working website to "premium / top-tier" — responsive at every width, nothing clipped, smooth scroll-driven motion, polished footer, full SEO + favicon set — and verify it in a real browser before calling it done. Use when the user says "make it premium", "top tier ui/ux", "smooth transitions", "make it responsive", "buttons are being cut", "add SEO", "add a favicon", or "make it show up on Google".
---

# Premium UI Pass

Polish a site so it looks finished on every screen, then prove it by checking in a browser. Keep the existing design language. Polish what's there instead of redesigning it, unless the user asks for a redesign. Respect `design.md` or brand files if they exist.

## 1. Layout and responsiveness (fix these first)

Check widths **390, 768, 1024, 1440, and 1920**. At each width:
- Nothing is clipped: no cut-off names, buttons, or headings. Look for `overflow:hidden` combined with fixed heights, `white-space:nowrap`, fixed `width`s, and tight `line-height` on large type.
- There is no horizontal scroll (`document.documentElement.scrollWidth > innerWidth`).
- Desktop isn't stuck in a mobile layout. Content uses the full width with a sensible `max-width` and fluid gutters (`clamp()`).
- There are no huge accidental gaps between sections.
- Tap targets are at least 44px, and the focus outline is visible.

## 2. Motion (premium means restrained)

- Scroll reveal: sections fade/slide in as they enter the viewport and out as they leave. Use `IntersectionObserver` or CSS `animation-timeline: view()`; reach for GSAP/ScrollTrigger only if the repo already uses it.
- Heavy background animations (SVG paths, canvas) run **only while their section is in view**. Pause them offscreen.
- SVG path gotcha: `view()` timelines don't attach to `<path>`. Put a named `view-timeline` on a wrapper element, and use `vector-effect: non-scaling-stroke` for consistent stroke width.
- Durations are 200–600ms, eased (`cubic-bezier(.2,.8,.2,1)`), animating only `transform` and `opacity`.
- **Always** honor `@media (prefers-reduced-motion: reduce)`.
- Hover and press states go on every interactive element.

## 3. Finish details

- The footer is distinct: a contrasting surface, clear grouping, social links, and ©year. It shouldn't look like an afterthought.
- Typography follows a consistent scale, with no orphaned single words in hero headings (`text-wrap: balance`).
- Images use explicit `width`/`height`, `loading="lazy"` below the fold, and modern formats.

## 4. SEO and discoverability

- Every page has a unique `<title>`, a meta description, and a canonical URL. Next.js gets the `metadata` export.
- Add Open Graph and Twitter card tags with a 1200×630 OG image.
- Generate `robots.txt` and `sitemap.xml`. Next.js can do this with `app/robots.ts` and `app/sitemap.ts`.
- Add JSON-LD: `Person` for portfolios (`name`, `alternateName` such as their handle, `sameAs` with GitHub/LinkedIn/Instagram, `url`), and `Organization` or `WebSite` for products.
- Favicon set: `favicon.ico`, `icon.svg`, a 180px `apple-icon.png`, and `manifest.webmanifest` with 192/512 icons. Generate them from the user's logo/PNG when one is provided.
- **To rank for a name:** the content has to include the exact name and handle in the H1/title. A `*.vercel.app` domain can rank, but a custom domain helps a lot. Tell the user to submit the sitemap in Google Search Console, which needs their action and can't be done from code, and to link the site from their GitHub, LinkedIn, and Instagram profiles.

## 5. Verify (required before you say "done")

Run the dev server and open it with the browser tool. Screenshot the page at 390 and 1440, scroll the full page, and check the console for errors. Run Lighthouse if available, aiming for Performance, Accessibility, Best Practices, and SEO scores of 90 or higher. Report the scores and anything below 90.

Report what changed in one short list, and attach the before/after screenshots. If the user wants a PR, hand over to the `ship-pr` skill.
