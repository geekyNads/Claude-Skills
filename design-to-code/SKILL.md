---
name: design-to-code
description: Turn a screenshot, Figma export, reference website, or design.md into a faithful, responsive UI — extracting colors, type, spacing, and components first, then building and visually comparing. Use when the user shares an image/mockup/link and says "make it look like this", "build this design", "copy this layout", or provides brand files (logo, colors, fonts).
---

# Design to Code

Match the design closely. Don't "interpret" it. Extract the system first, then build, then compare.

## 1. Extract the design tokens

From the image, link, or design doc, write down:
- **Colors:** background, surface, text, muted text, primary, accent, border (as hex)
- **Type:** font families (match the closest Google Font if unknown), sizes for h1/h2/body/small, weights
- **Spacing and shape:** base spacing unit, corner radius, shadow style
- **Components:** buttons, cards, nav, inputs, and each one's states

Put them in one place: CSS variables or the Tailwind theme. Never scatter hex codes through components.

## 2. Build the structure

- Go top to bottom: nav → hero → sections → footer.
- Use semantic HTML (`header`, `main`, `section`, `footer`, real `button`s).
- Mobile-first. If the design only shows desktop, make a sensible mobile version and say what you decided.
- Use real images and logos if the user provided them. Otherwise use clearly marked placeholders.

## 3. Compare (this step is required)

Open the result in the browser tool at the design's width. Put the screenshot next to the reference and list the differences: spacing, sizes, colors, alignment. Fix them, then check again. Two passes is usually enough.

## 4. Report

- What matches, and what you approximated (e.g. "used Inter instead of the custom font")
- Screenshots at desktop and mobile widths
- Where the tokens live, so the user can tweak colors in one place

## Rules

- Don't copy another company's logo, brand name, or copyrighted images into the user's product. Use the *style*, not the brand.
- If the user gave a `design.md` or brand kit, it wins over the screenshot when they conflict. Mention the conflict.
