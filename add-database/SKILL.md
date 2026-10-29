---
name: add-database
description: Add a real database to a beginner's app — pick a hosted Postgres, design a minimal schema, set up an ORM/client, migrations, seed data, and CRUD — explaining each concept in one line. Use when the user says "save data", "add a database", "data disappears on refresh", "connect Supabase/Postgres/Mongo", or moves from fake data to real data.
---

# Add a Database

## 1. Choose (default unless there's a reason not to)

- **Supabase** (Postgres + dashboard + auth + storage) or **Neon** (Postgres only), both with free tiers.
- ORM: **Drizzle** or **Prisma** for TypeScript, **SQLAlchemy/SQLModel** for Python. *ORM = write database queries as code instead of raw SQL.*
- If the project already has a database or ORM, use it.

## 2. Design the schema with the user

List the "things" in the app (users, posts, orders) and their fields. Keep it minimal for v1:
- Every table gets `id`, `created_at`
- Relationships: "a post belongs to a user", which means `posts.user_id`
- Show it as a small table before writing code, and confirm with the user.

## 3. Set up

1. Create the DB (guide the user through the provider's dashboard; they create the account themselves).
2. Put the connection string in `.env.local` as `DATABASE_URL`. **Never in code.** Add `.env*` to `.gitignore` and create `.env.example` with placeholder values (`secrets-guard`).
3. Define the schema in the ORM, then generate and run a migration. *Migration = a saved, replayable change to the database's structure.*
4. Write a seed script with a few fake rows so the UI has something to show.

## 4. Wire it into the app

- Do reads and writes on the **server** (API routes, server actions, backend), never directly from browser code with secret keys.
- Implement only the operations the UI needs (list, create, update, delete).
- Validate input before saving (`forms-that-work`).
- Handle "not found" and errors with a friendly message.

## 5. Verify

Create, refresh, see it persist, then check the row in the provider's dashboard. Show the user where to look at their data.

## Watch-outs to explain once

- If you use Supabase from the browser, **Row Level Security** must be on, or anyone can read every row.
- Serverless and too many connections: use the provider's pooled URL in production.
- Back up before destructive migrations (dropping columns or tables).
