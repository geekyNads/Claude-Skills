"""Run: uv run python test_pipeline.py"""
from internpilot.apply import answer_for
import json, pathlib
from internpilot import pipeline
from internpilot.pipeline import evaluate, parse_pay

cfg = json.loads((pathlib.Path(__file__).parent / "config.example.json").read_text())

# pay parsing: ranges, k, yearly → monthly, LPA, ignore tiny plan prices
assert parse_pay("Stipend: ₹15,000–₹20,000/month") == (15000, 20000)
assert parse_pay("₹60,000 per month for 3 months. Paid plans start at ₹399 a month") == (60000, 60000)
assert parse_pay("Base pay ₹300,000.00/yr - ₹600,000.00/yr") == (25000, 50000)
assert parse_pay("stipend of INR 15,500 to INR 16,500 per month") == (15500, 16500)
assert parse_pay("CTC 6 LPA after conversion") == (50000, 50000)
assert parse_pay("Stipend: up to Rs 10k") == (10000, 10000)
assert parse_pay("Competitive stipend") == (None, None)


def job(desc, company="Acme", pay=(None, None), title="SWE Intern", location="India"):
    return {"description": desc, "company": company, "title": title, "location": location, "pay_min": pay[0], "pay_max": pay[1]}


score, flags, ok = evaluate(job("Remote. Python, React, TypeScript, Next.js", pay=(30000, 50000)), cfg, {})
assert ok and score > 30, (score, flags)
assert "not remote" in evaluate(job("Bengaluru office. Python"), cfg, {})[1]
assert "needs 2+ yrs experience" in evaluate(job("Remote. 2+ years of practical experience"), cfg, {})[1]
assert "graduation-year restricted" in evaluate(job("Remote. 2025 and 2026 graduates only"), cfg, {})[1]
assert "blocklisted" in evaluate(job("Remote", company="QSkill"), cfg, {})[1]
assert any(f.startswith("pay ≤") for f in evaluate(job("Remote", pay=(5000, 10000)), cfg, {})[1])
assert "mass poster" in evaluate(job("Remote", company="Mill"), cfg, {"mill": 5})[1]

# screening answers: years-of-experience by skill, regex answers, unknown → None
assert answer_for("How many years of work experience do you have with React Native?", cfg) == "0"
assert answer_for("How many years of work experience do you have with TypeScript?", cfg) == "1"
assert answer_for("How many years of work experience do you have with Rust?", cfg) == "0"
assert answer_for("Do you have a valid driver's license?", cfg) == "Yes"
assert answer_for("Are you comfortable working in a remote setting?", cfg) == "Yes"
assert answer_for("What is your favourite colour?", cfg) is None
print("all checks passed")

# refinements: singular "graduate", company-name variants hit the blocklist
assert "graduation-year restricted" in evaluate(job("Remote. Ideal candidate is either 2026/2027 graduate"), cfg, {})[1]
assert "blocklisted" in evaluate(job("Remote", company="Medi Nex Workforce"), cfg, {})[1]
assert "mass poster" in evaluate(job("Remote", company="Mill Co"), cfg, {"millco": 4})[1]
print("refinement checks passed")
