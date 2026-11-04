---
name: first-tests
description: Add a small number of high-value tests to a project that has none — the logic most likely to break and most costly if it does — set up the test runner, explain each test, and run them. Use when the user says "add tests", "how do I test this", "I keep breaking things", or before refactoring something important.
---

# First Tests

Beginners don't need 80% coverage. They need **5–10 tests that catch the bugs that would actually hurt.**

## 1. Pick what to test

Rank by "breaks often" × "hurts if broken":
1. Money or data logic: prices, totals, discounts, permissions
2. Functions with branches: validation, parsing, date math, formatting
3. The main user flow, end to end (sign up → do the core thing)
4. Any bug you just fixed, so it never comes back

Skip: simple UI with no logic, third-party library behavior, framework internals.

## 2. Set up the runner (use what the project has)

- JS/TS: **Vitest** (Vite/Next), or the existing Jest
- Python: **pytest**
- End to end: **Playwright**, for 1–2 critical flows only

Add a `test` script so `npm test` / `pytest` just works.

## 3. Write tests people can read

```ts
describe("calculateTotal", () => {
  it("applies a 10% discount code", () => {
    expect(calculateTotal([{ price: 100, qty: 2 }], "SAVE10")).toBe(180);
  });
  it("never goes below zero", () => {
    expect(calculateTotal([{ price: 5, qty: 1 }], "FREE100")).toBe(0);
  });
});
```

- The test name says what *should* happen, in plain English
- Cover one happy path and the edge cases: empty, zero, negative, huge, missing
- No mocking of things you could just call directly

## 4. Prove they work

Run them and watch them pass. Then **break the code on purpose** and confirm a test fails, then undo. A test that can't fail is useless.

## 5. Teach the habit

- Run tests before committing
- When you fix a bug, add a test for it first
- Optional: add the tests to CI (a GitHub Action) so every PR runs them
