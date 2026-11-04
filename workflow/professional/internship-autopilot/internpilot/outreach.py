"""Send a connection request (with a short note) to the job poster of each job you applied to."""
import re
import time

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

from .apply import JOB_URL, open_browser, signed_in
from .pipeline import db

FIND_POSTER = """() => {
  const re = /Meet the hiring team|Job poster/i;
  const h = [...document.querySelectorAll('body *')]
    .find(e => re.test(e.textContent) && ![...e.children].some(c => re.test(c.textContent)));
  let n = h;
  for (let i = 0; i < 8 && n && !n.querySelector('a[href*="/in/"]'); i++) n = n.parentElement;
  const a = n && n.querySelector('a[href*="/in/"]');
  return a ? a.href.split('?')[0] : null;
}"""


def note_for(cfg, first, job):
    return cfg["outreach_note"].format(first=first, title=job["title"], company=job["company"])[:200]


def connect(page, profile, note, dry):
    page.goto(profile)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(4)
    # Newer profile pages have no <h1>; the title is "(3) Jane Doe | LinkedIn".
    name = re.sub(r"^\(\d+\)\s*|\s*\|\s*LinkedIn$", "", page.title()).strip()
    first = name.split()[0] if name else "there"
    # Match the poster's full name: the sidebar has "Invite <someone else> to connect" buttons too.
    invite = page.locator(f'[aria-label="Invite {name} to connect"]')
    if not invite.count():
        more = page.get_by_role("button", name=re.compile(r"^More( actions)?$", re.I))
        if more.count():
            more.first.click()
            time.sleep(1.5)
    if not invite.count():
        page.keyboard.press("Escape")
        return "skipped", first, "no Connect button (pending, 1st-degree, or follow-only)"
    if dry:
        return "dry_run", first, "would connect"
    invite.first.click()
    time.sleep(1.5)
    add = page.get_by_role("button", name=re.compile(r"^Add a note", re.I))
    if add.count():
        add.first.click()
        try:
            box = page.locator("textarea[name=message], textarea#custom-message").first
            box.wait_for(timeout=4000)
            box.fill(note.replace("{first}", first))
        except PWTimeout:
            pass  # free accounts may hit the monthly note limit; fall through to sending without one
    send = page.get_by_role("button", name=re.compile(r"^Send( invitation| now)?$|^Send without a note", re.I))
    if not send.count():
        page.keyboard.press("Escape")
        return "failed", first, "no Send button"
    send.first.click()
    time.sleep(2)
    return "sent", first, "invitation sent"


def sent_today(con):
    return con.execute("select count(*) from outreach where status='sent' and date(sent)=date('now')").fetchone()[0]


def run(cfg, dry=False, limit=None):
    con = db()
    budget = cfg["daily_outreach_cap"] - (0 if dry else sent_today(con))
    if limit is not None:
        budget = min(budget, limit)
    jobs = con.execute("select j.id, j.title, j.company from jobs j left join outreach o on o.job_id=j.id "
                       "where j.status='applied' and o.job_id is null order by j.updated desc limit ?",
                       (max(budget, 0),)).fetchall()
    if not jobs:
        print("No applied jobs waiting for outreach (or today's cap is used up).")
        return
    with sync_playwright() as p:
        ctx, page = open_browser(p)
        if not signed_in(page):
            ctx.close()
            print("Not signed in. Run: uv run python -m internpilot login")
            return
        for j in jobs:
            page.goto(JOB_URL.format(j["id"]))
            page.wait_for_load_state("domcontentloaded")
            time.sleep(3)
            profile = page.evaluate(FIND_POSTER)
            if not profile:
                status, detail = "skipped", "no hiring team listed"
            else:
                try:
                    status, first, detail = connect(page, profile, note_for(cfg, "{first}", j), dry)
                except Exception as e:
                    status, detail = "failed", f"{type(e).__name__}: {e}"[:200]
            print(f"[{status:8}] {j['company']} · {profile or '-'}  ({detail})")
            if not dry:
                con.execute("insert or replace into outreach(job_id, profile, status) values(?,?,?)", (j["id"], profile, status))
                con.commit()
            time.sleep(cfg["delay_s"] * 2)
        ctx.close()
