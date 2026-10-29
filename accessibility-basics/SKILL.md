---
name: accessibility-basics
description: Make a site usable by everyone with the high-impact basics — color contrast, keyboard navigation, focus states, labels, alt text, headings, motion preferences — checked in the browser and explained simply. Use when the user says "accessibility", "a11y", "make it accessible", before launch, or when building forms/navigation/modals.
---

# Accessibility Basics

These 8 checks cover most real problems. They also help SEO and mobile users.

## The checklist

1. **Contrast:** body text at least 4.5:1, large text and icons at least 3:1. Watch out for light grey on white and text on images.
2. **Keyboard:** unplug the mouse mentally. `Tab` reaches every link, button, and input in a sensible order. `Enter`/`Space` activates. `Esc` closes modals. Nothing traps focus.
3. **Visible focus:** never `outline: none` without a replacement. Use `:focus-visible` with a clear ring.
4. **Real elements:** use `<button>` for actions and `<a href>` for navigation. A `<div onClick>` is invisible to keyboards and screen readers.
5. **Labels:** every input has a `<label>`. Icon-only buttons get `aria-label="Close"`.
6. **Images:** meaningful images get descriptive `alt`. Decorative ones get `alt=""`.
7. **Headings:** one `<h1>` per page, then `h2`/`h3` in order, so screen-reader users can skim.
8. **Motion:** respect `prefers-reduced-motion`. No auto-playing video with sound. Nothing flashes more than 3 times a second.

Bonus: set `<html lang="en">` (or the right language), make tap targets 44px or more, and never use color alone to convey meaning (add an icon or text to red errors).

## How to check

- Run Lighthouse Accessibility, or axe DevTools if available, and aim for 95+.
- Do the keyboard walk-through yourself in the browser tool: Tab through the page and screenshot the focus states.
- Spot-check contrast on the main colors.

## Report

A list of `file:line → problem → fix`, then apply the fixes. Explain each in one human sentence, like "Keyboard users can't open the menu because it's a div, not a button."
