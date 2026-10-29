---
name: dependency-doctor
description: Fix package install and version problems — npm ERESOLVE/peer dependency conflicts, pip resolution errors, wrong Node/Python version, broken lockfiles, "module not found" after install, native build failures — without blindly forcing or nuking everything. Use when npm/pnpm/yarn/pip/uv install fails, after upgrading packages, or when the user says "install is broken" or "packages conflict".
---

# Dependency Doctor

## 1. Read the actual error

Install errors name the conflict. Find:
- **Which package** wants **which version** of what
- Whether it's a **peer dependency** conflict, a **runtime version** mismatch, a **network/registry** problem, or a **native build** failure (node-gyp, C compiler, Python headers)

Explain it in one sentence: "`some-ui-lib@2` only supports React 18, but you have React 19."

## 2. Check the basics

- Runtime version vs `engines` / `.nvmrc` / `requires-python`
- Mixing package managers? (`package-lock.json` *and* `pnpm-lock.yaml`.) Pick the one the project uses and remove the stray lockfile, with the user's OK.
- Python: is the virtualenv active? (`which python`)

## 3. Fix, in order of preference

1. **Use a compatible version.** Upgrade the outdated package (`npm i pkg@latest`), or pin the one causing the conflict to a version that fits. Check its changelog or releases for support.
2. **Replace an abandoned package** with a maintained one if it hasn't been updated for the current framework.
3. **Clean reinstall** (it's reversible): delete `node_modules` and reinstall from the lockfile. Python: recreate the venv.
4. **Last resort:** `--legacy-peer-deps` / `overrides`. Explain the risk (it may break at runtime) and add a comment saying why.

## Don't

- Run `npm audit fix --force` (it can jump major versions and break the app)
- Delete the lockfile casually (it changes every dependency at once)
- Use `sudo npm install -g` or `sudo pip install`
- Install packages with typos or unknown publishers. Check the name, weekly downloads, and repo before adding a new one.

## 4. Verify

After install: run the dev server and the build. "Installed without errors" isn't the goal; "the app runs" is. Commit the lockfile change with a clear message.
