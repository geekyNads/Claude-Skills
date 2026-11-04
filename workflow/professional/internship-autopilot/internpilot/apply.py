"""Auto-apply to eligible jobs through LinkedIn Easy Apply, in a browser profile you signed into yourself."""
import re
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

from .pipeline import db

PROFILE = Path.home() / ".internpilot" / "chrome-profile"
JOB_URL = "https://www.linkedin.com/jobs/view/{}/"
NEXT = re.compile(r"^(Continue to next step|Next|Review your application|Review)\b", re.I)
SUBMIT = re.compile(r"^Submit application", re.I)


def open_browser(p):
    PROFILE.mkdir(parents=True, exist_ok=True)
    ctx = p.chromium.launch_persistent_context(str(PROFILE), headless=False, viewport={"width": 1280, "height": 900})
    return ctx, (ctx.pages[0] if ctx.pages else ctx.new_page())


def signed_in(page):
    page.goto("https://www.linkedin.com/feed/")
    page.wait_for_load_state("domcontentloaded")
    return not re.search(r"/login|/authwall|/signup|uas/", page.url)


def login():
    """Open the persistent profile so the user signs in by hand. We never see or store the password."""
    with sync_playwright() as p:
        ctx, page = open_browser(p)
        page.goto("https://www.linkedin.com/login")
        input("Sign in to LinkedIn in the browser window, then press Enter here… ")
        ok = signed_in(page)
        ctx.close()
    print("Signed in ✓" if ok else "Still signed out. Run `login` again.")
    return ok


def answer_for(question, cfg):
    q = " ".join(question.split()).lower()
    m = re.search(r"how many years.*?\b(?:with|in|of using|using)\s+(.+?)\s*\??\*?$", q)
    if m:
        skill = m.group(1)
        return str(next((v for k, v in cfg["skill_years"].items() if k in skill), cfg["default_years"]))
    for pat, ans in cfg["answers"].items():
        if re.search(pat, q, re.I):
            return ans
    return None


def _label(dlg, el):
    eid = el.get_attribute("id")
    if eid:
        lab = dlg.locator(f'label[for="{eid}"]')
        text = lab.first.inner_text().strip() if lab.count() else ""
        if text:
            return text
    return (el.get_attribute("aria-label") or "").strip() or _nearby_text(el)


# LinkedIn's newer Easy Apply markup puts the question beside the field, not in a <label>/<legend>:
# climb ancestors until one holds text beyond the field's own (e.g. "Yes No"), and take that.
NEARBY_TEXT = r"""el => {
  const own = (el.innerText || '').trim();
  for (let n = el.parentElement, i = 0; n && i < 6; n = n.parentElement, i++) {
    const t = n.innerText.replace(own, '').replace(/\bRequired\b|\*/g, '').trim();
    if (t) return t.split('\n').map(s => s.trim()).filter(Boolean)[0];
  }
  return '';
}"""


def _nearby_text(el):
    return el.evaluate(NEARBY_TEXT).strip()


def fill_page(dlg, cfg):
    """Fill every empty field on the current Easy Apply page. Returns questions we had no answer for."""
    missing = []
    for el in dlg.locator("input[type=text], input[type=number], input[type=tel], input:not([type]), textarea").all():
        if not el.is_visible() or el.input_value().strip():
            continue
        q = _label(dlg, el)
        ans = answer_for(q, cfg)
        if ans is None:
            missing.append(q)
        else:
            el.fill(ans)
    for sel in dlg.locator("select").all():
        val = sel.input_value()
        if val and not re.match(r"select", val, re.I):
            continue
        q = _label(dlg, sel)
        ans = answer_for(q, cfg)
        opts = [o.strip() for o in sel.locator("option").all_inner_texts()]
        pick = ans and (next((o for o in opts if o.lower() == ans.lower()), None)
                        or next((o for o in opts if ans.lower() in o.lower()), None))
        if pick:
            sel.select_option(label=pick)
        else:
            missing.append(q)
    for fs in dlg.locator("fieldset").all():
        radios = fs.locator("input[type=radio]").all()
        if not radios or any(r.is_checked() for r in radios):
            continue
        legend = fs.locator("legend")
        q = (legend.first.inner_text() if legend.count() else _nearby_text(fs)).strip()
        ans = answer_for(q, cfg)
        exact = re.compile(rf"^\s*{re.escape(ans)}\s*$", re.I) if ans else None
        option = exact and (fs.get_by_role("radio", name=exact).or_(fs.get_by_text(exact))).first
        if option and option.count():
            option.click()
        else:
            missing.append(q)
    return missing


def unfollow(dlg):
    for cb in dlg.locator("input[type=checkbox]").all():
        if cb.is_checked() and "follow" in _label(dlg, cb).lower():
            dlg.locator(f'label[for="{cb.get_attribute("id")}"]').first.click()


def discard(page):
    page.keyboard.press("Escape")
    time.sleep(1)
    btn = page.get_by_role("button", name=re.compile(r"^Discard", re.I))
    if btn.count():
        btn.first.click()


def apply_one(page, job_id, cfg, dry):
    """Returns (status, note)."""
    page.goto(JOB_URL.format(job_id))
    page.wait_for_load_state("domcontentloaded")
    time.sleep(3)
    if page.get_by_text(re.compile(r"Application submitted|Applied \d+ \w+ ago", re.I)).count():
        return "applied", "already applied"
    btn = page.locator("main").get_by_role("button", name=re.compile(r"Easy Apply", re.I))
    if not btn.count():
        return "external", "no Easy Apply (apply on company site)"
    btn.first.click()
    dlg = page.get_by_role("dialog").filter(has_text=re.compile(r"Apply to", re.I)).first
    try:
        dlg.wait_for(timeout=10_000)
    except PWTimeout:
        return "failed", "Easy Apply dialog did not open"
    for _ in range(12):
        time.sleep(1.5)
        errors = dlg.locator(".artdeco-inline-feedback--error").all_inner_texts()
        missing = fill_page(dlg, cfg)
        if missing or any(e.strip() for e in errors):
            discard(page)
            return "needs_input", " | ".join(missing or errors)
        unfollow(dlg)
        submit = dlg.get_by_role("button", name=SUBMIT)
        if submit.count():
            if dry:
                discard(page)
                return "eligible", "dry run: reached submit"
            submit.first.click()
            time.sleep(4)
            ok = page.get_by_text(re.compile(r"application was sent|Application submitted", re.I)).count()
            return ("applied", "submitted") if ok else ("failed", "no confirmation after submit")
        nxt = dlg.get_by_role("button", name=NEXT)
        if not nxt.count():
            discard(page)
            return "failed", "no Next/Review button"
        nxt.first.click()
    discard(page)
    return "failed", "too many pages"


def applied_today(con):
    return con.execute("select count(*) from jobs where status='applied' and note='submitted' "
                       "and date(updated)=date('now')").fetchone()[0]


def run(cfg, dry=False, limit=None):
    con = db()
    budget = cfg["daily_apply_cap"] - (0 if dry else applied_today(con))
    if limit is not None:
        budget = min(budget, limit)
    jobs = con.execute("select id, title, company from jobs where status='eligible' order by score desc limit ?",
                       (max(budget, 0),)).fetchall()
    if not jobs:
        print("Nothing to apply to (no eligible jobs, or today's cap is used up).")
        return
    with sync_playwright() as p:
        ctx, page = open_browser(p)
        if not signed_in(page):
            ctx.close()
            print("Not signed in. Run: uv run python -m internpilot login")
            return
        for j in jobs:
            try:
                status, note = apply_one(page, j["id"], cfg, dry)
            except Exception as e:  # one broken page shouldn't stop the batch
                status, note = "failed", f"{type(e).__name__}: {e}"[:200]
                discard(page)
            print(f"[{status:11}] {j['company']} · {j['title']}  ({note})")
            if status == "needs_input":
                for q in note.split(" | "):
                    con.execute("insert or ignore into questions(question, job_id) values(?,?)", (q, j["id"]))
            if not dry or status != "eligible":
                con.execute("update jobs set status=?, note=?, updated=current_timestamp where id=?", (status, note, j["id"]))
            con.commit()
            time.sleep(cfg["delay_s"])
        ctx.close()
