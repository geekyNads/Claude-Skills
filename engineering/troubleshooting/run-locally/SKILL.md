---
name: run-locally
description: Get any cloned or downloaded project running on the user's machine — detect the stack, install the right runtime and dependencies, set up env vars from .env.example, start the dev server, and open it. Use when the user says "run this", "how do I start this project", "I cloned it, now what", "show me on localhost", or a setup step fails.
---

# Run Locally

## 1. Detect

Read the README's setup section first, since it often has the exact steps. Then look at the files to identify the stack:
- `package.json` → Node. Look for a lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lockb` → bun, otherwise npm.
- `pyproject.toml` / `requirements.txt` → Python
- `Cargo.toml` → Rust, `go.mod` → Go, `Gemfile` → Ruby
- `docker-compose.yml` → may need Docker for the database or services
- `.nvmrc` / `engines` / `.python-version` → the required runtime version

## 2. Runtime

Check `node -v` / `python3 --version` against what's required. If it's wrong, suggest a version manager (`nvm`, `fnm`, `pyenv`, `uv`) instead of reinstalling globally.

## 3. Install

- Use the project's package manager (a mismatched one causes weird bugs).
- Python: create a virtualenv first (`python3 -m venv .venv && source .venv/bin/activate`, or `uv sync`).
- If install fails, hand off to `dependency-doctor`.

## 4. Env vars

- Copy `.env.example` to `.env.local` (or `.env`).
- List every variable it needs and where to get each one. The user fills in real keys themselves.
- Never invent real-looking secrets. Leave placeholders and explain which features won't work without them.

## 5. Database and services

Start what's needed (`docker compose up -d`, run migrations, seed). Explain each command in one line.

## 6. Start and open

Run the dev script (`npm run dev`, etc.). Find the actual port in the output and open it with the browser tool. Check the browser console and the server terminal for errors.

## 7. Report

```
Running at http://localhost:3000
Start it again with: npm run dev
Stop it with: Ctrl+C
Missing for full functionality: STRIPE_SECRET_KEY (payments won't work)
```

Common snag: if the port is already in use, find the process with `lsof -i :3000` and ask before killing it, or use another port.
