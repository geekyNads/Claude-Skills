"""Find internships via LinkedIn's public (logged-out) job endpoints, parse pay, score fit, store in SQLite."""
import json
import re
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.json"  # copy config.example.json here and fill in your answers
DB = ROOT / "internpilot.db"
GUEST = "https://www.linkedin.com/jobs-guest/jobs/api"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

SCHEMA = """
create table if not exists jobs(
  id text primary key, title text, company text, location text, posted text, description text,
  pay_min integer, pay_max integer, remote integer, score integer, flags text,
  status text default 'new', note text, updated text default current_timestamp);
create table if not exists outreach(job_id text primary key, profile text, status text, sent text default current_timestamp);
create table if not exists questions(question text primary key, job_id text, seen text default current_timestamp);
"""
# Statuses a rescore may overwrite; anything else (applied, needs_input, external, failed) is sticky.
RESCORABLE = ("new", "eligible", "ineligible")


def load_config():
    return json.loads(CONFIG.read_text())


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode()
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == tries - 1:
                raise
            time.sleep(30 * (i + 1))  # LinkedIn rate-limits guest calls; back off and retry


def _text(node, sel):
    el = node.select_one(sel)
    return el.get_text(" ", strip=True) if el else ""


def search(keywords, location, days, start):
    q = urllib.parse.urlencode({"keywords": keywords, "location": location, "f_TPR": f"r{days * 86400}", "f_E": 1, "start": start})
    soup = BeautifulSoup(get(f"{GUEST}/seeMoreJobPostings/search?{q}"), "html.parser")
    for card in soup.select(".base-card"):
        jid = (card.get("data-entity-urn") or "").rsplit(":", 1)[-1]
        if jid.isdigit():
            time_el = card.select_one("time")
            yield {
                "id": jid,
                "title": _text(card, ".base-search-card__title"),
                "company": _text(card, ".base-search-card__subtitle"),
                "location": _text(card, ".job-search-card__location"),
                "posted": time_el.get("datetime", "") if time_el else "",
            }


def description(job_id):
    soup = BeautifulSoup(get(f"{GUEST}/jobPosting/{job_id}"), "html.parser")
    el = soup.select_one(".show-more-less-html__markup")
    return el.get_text("\n", strip=True) if el else ""


AMOUNT = re.compile(r"(?:₹|\bINR|\bRs\.?)\s*([\d,]+(?:\.\d+)?)\s*(k\b|lakhs?\b|lpa\b|l\b)?", re.I)
LPA = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:-|–|to)?\s*(\d+(?:\.\d+)?)?\s*LPA\b", re.I)
YEARLY = re.compile(r"^.{0,40}?(?:/\s*yr|/\s*year|per\s+(?:annum|year)|p\.?a\.?\b|annually|\bctc\b)", re.I)


def parse_pay(text):
    """Monthly INR (min, max) mentioned in text, or (None, None). Ignores amounts under ₹1,000 (plan prices etc.)."""
    vals = []
    for m in AMOUNT.finditer(text):
        n = float(m.group(1).replace(",", ""))
        unit = (m.group(2) or "").lower()
        if unit == "k":
            n *= 1_000
        elif unit:  # lakh / lpa / l
            n = n * 100_000 / 12
        elif YEARLY.match(text[m.end():m.end() + 45]):
            n /= 12
        if n >= 1000:
            vals.append(int(n))
    for m in LPA.finditer(text):
        vals += [int(float(g) * 100_000 / 12) for g in m.groups() if g]
    return (min(vals), max(vals)) if vals else (None, None)


def norm(company):
    """"Medi Nex Workforce" and "MediNex Workforce" are the same poster."""
    return re.sub(r"[^a-z0-9]", "", (company or "").lower())


REMOTE = re.compile(r"\bremote\b|work from home|\bwfh\b", re.I)


def is_remote(job):
    return bool(REMOTE.search(" ".join([job["title"] or "", job["location"] or "", job["description"] or ""])))


def evaluate(job, cfg, company_counts):
    """Return (score, flags, eligible) for a job row with a description."""
    d = job["description"] or ""
    hits = [s for s in cfg["resume_skills"] if re.search(rf"(?<![\w.+]){re.escape(s)}(?![\w+])", d, re.I)]
    flags = [why for pat, why in cfg["disqualifiers"].items() if re.search(pat, d, re.I)]
    if not is_remote(job):
        flags.append("not remote")
    if norm(job["company"]) in {norm(b) for b in cfg["blocklist"]}:
        flags.append("blocklisted")
    elif company_counts.get(norm(job["company"]), 0) >= 4:
        flags.append("mass poster")  # ponytail: count-based mill heuristic; add to blocklist when it misfires
    pay_max = job["pay_max"]
    if pay_max is None and not cfg["allow_unknown_pay"]:
        flags.append("pay not stated")
    elif pay_max is not None and pay_max <= cfg["min_monthly_pay_inr"]:
        flags.append(f"pay ≤ ₹{cfg['min_monthly_pay_inr']:,}")
    score = len(hits) * 10 + (min(pay_max, 60_000) // 2_000 if pay_max else 0)
    return score, flags, not flags


def rescore(con, cfg):
    counts = {}
    for (company,) in con.execute("select company from jobs"):
        counts[norm(company)] = counts.get(norm(company), 0) + 1
    for job in con.execute("select * from jobs where description is not null").fetchall():
        score, flags, ok = evaluate(job, cfg, counts)
        status = job["status"]
        if status in RESCORABLE:
            status = "eligible" if ok else "ineligible"
        con.execute("update jobs set score=?, flags=?, remote=?, status=? where id=?",
                    (score, ", ".join(flags), int(is_remote(job)), status, job["id"]))
    con.commit()


def scrape(cfg, log=print):
    con = db()
    new = 0
    for kw in cfg["searches"]:
        for start in range(0, cfg["pages"] * 25, 25):
            try:
                cards = list(search(kw, cfg["location"], cfg["days"], start))
            except urllib.error.HTTPError as e:
                log(f"  search '{kw}' p{start // 25}: HTTP {e.code}, skipping")
                cards = []
            for c in cards:
                if not re.search(r"\bintern", c["title"], re.I):
                    continue
                cur = con.execute("insert or ignore into jobs(id,title,company,location,posted) values(?,?,?,?,?)",
                                  (c["id"], c["title"], c["company"], c["location"], c["posted"]))
                new += cur.rowcount
            time.sleep(cfg["delay_s"])
            if len(cards) < 25:
                break
    con.commit()
    todo = [r["id"] for r in con.execute("select id from jobs where description is null")]
    log(f"{new} new listings; fetching {len(todo)} descriptions…")
    for jid in todo:
        try:
            d = description(jid)
        except urllib.error.HTTPError as e:
            log(f"  {jid}: HTTP {e.code}, will retry next run")
            continue
        lo, hi = parse_pay(d)
        con.execute("update jobs set description=?, pay_min=?, pay_max=? where id=?", (d, lo, hi, jid))
        con.commit()
        time.sleep(cfg["delay_s"] / 2)
    rescore(con, cfg)
    return new
