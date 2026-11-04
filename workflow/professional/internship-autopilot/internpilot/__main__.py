"""internpilot: find → score → apply → reach out.  Usage: uv run python -m internpilot <command>"""
import argparse
import json

from . import pipeline


def cmd_list(args, cfg):
    con = pipeline.db()
    where = "" if args.all else "where status not in ('ineligible')"
    rows = con.execute(f"select * from jobs {where} order by status='eligible' desc, score desc limit ?", (args.n,)).fetchall()
    for r in rows:
        pay = f"₹{r['pay_min']:,}–{r['pay_max']:,}" if r["pay_max"] else "pay ?"
        print(f"{r['status']:11} {r['score'] or 0:>4}  {pay:>17}  {r['company'][:22]:22}  {r['title'][:45]:45}  "
              f"https://www.linkedin.com/jobs/view/{r['id']}/  {r['flags'] or ''}")


def cmd_status(args, cfg):
    con = pipeline.db()
    for status, n in con.execute("select status, count(*) from jobs group by status order by 2 desc"):
        print(f"{status:12} {n}")
    for status, n in con.execute("select status, count(*) from outreach group by status"):
        print(f"outreach {status:8} {n}")
    qs = [r[0] for r in con.execute("select question from questions order by seen desc")]
    if qs:
        print("\nUnanswered screening questions (add with `answer`):")
        print("\n".join(f"  - {q}" for q in qs))


def cmd_answer(args, cfg):
    """Teach a new screening answer, then re-queue jobs that were waiting on it."""
    cfg["answers"][args.pattern] = args.value
    pipeline.CONFIG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
    con = pipeline.db()
    con.execute("delete from questions where question like ?", (f"%{args.pattern}%",))
    n = con.execute("update jobs set status='eligible', note=null where status='needs_input'").rowcount
    con.commit()
    print(f"Saved. {n} job(s) re-queued for the next apply run.")


def main():
    ap = argparse.ArgumentParser(prog="internpilot", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("login", help="sign in to LinkedIn once in the app's browser profile")
    sub.add_parser("scrape", help="fetch new listings, parse pay, score fit")
    sub.add_parser("rescore", help="re-apply config filters to stored jobs")
    p = sub.add_parser("list", help="show jobs")
    p.add_argument("--all", action="store_true")
    p.add_argument("-n", type=int, default=40)
    for name in ("apply", "outreach", "run"):
        p = sub.add_parser(name, help={"apply": "Easy Apply to eligible jobs", "outreach": "connect with job posters",
                                       "run": "scrape + apply + outreach"}[name])
        p.add_argument("--dry-run", action="store_true", help="go up to the final click, then stop")
        p.add_argument("--limit", type=int)
    sub.add_parser("status", help="pipeline counts + unanswered questions")
    p = sub.add_parser("answer", help="add a screening answer: answer '<regex>' '<value>'")
    p.add_argument("pattern")
    p.add_argument("value")
    args = ap.parse_args()
    cfg = pipeline.load_config()

    if args.cmd == "login":
        from .apply import login
        login()
    elif args.cmd == "scrape":
        pipeline.scrape(cfg)
        cmd_status(args, cfg)
    elif args.cmd == "rescore":
        pipeline.rescore(pipeline.db(), cfg)
    elif args.cmd in ("apply", "outreach", "run"):
        from . import apply, outreach
        if args.cmd == "run":
            pipeline.scrape(cfg)
        if args.cmd in ("apply", "run"):
            apply.run(cfg, args.dry_run, args.limit)
        if args.cmd in ("outreach", "run"):
            outreach.run(cfg, args.dry_run, args.limit)
    else:
        {"list": cmd_list, "status": cmd_status, "answer": cmd_answer}[args.cmd](args, cfg)


if __name__ == "__main__":
    main()
