"""Shared helpers: paths, CSV loading, timezone-safe timestamps, transcript parsing."""
import csv
import json
import pathlib
import re
import unicodedata
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"
OUT = ROOT / "outputs"
FMT = "%Y-%m-%d %H:%M:%S"

# CRM / call / order timestamps are stored in the LEAD's local time (not UTC).
# Offsets for Nov 2026 (UK back on GMT since 25 Oct; US back on standard time since 1 Nov).
TZ_OFFSET_H = {"IST": 5.5, "GST": 4.0, "AST": 3.0, "GMT": 0.0, "PST": -8.0, "CST": -6.0}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tz_of(city_timezone: str) -> str:
    m = re.search(r"\((\w+)\)", city_timezone or "")
    return m.group(1) if m else "IST"


def to_utc(ts, tz):
    """Local timestamp string -> aware UTC datetime. Returns None for NULL/empty."""
    if ts in (None, "", "NULL"):
        return None
    dt = datetime.strptime(ts, FMT) - timedelta(hours=TZ_OFFSET_H[tz])
    return dt.replace(tzinfo=timezone.utc)


def fmt_utc(dt):
    return dt.strftime("%Y-%m-%d %H:%M UTC") if dt else None


def norm(s: str) -> str:
    """Normalise quotes/whitespace so verbatim matching is robust to typography only."""
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


LINE_RE = re.compile(r"^\[(\d{2}:\d{2})\]\s+(COUNSELLOR|PARENT)(?:\s*\([^)]*\))?:\s*(.*)$")


def parse_transcript(path):
    """Return {ts: (speaker, text)} for every timestamped utterance."""
    lines = {}
    for raw in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(raw.strip())
        if m:
            lines["[" + m.group(1) + "]"] = (m.group(2), m.group(3))
    return lines


def non_ascii_lookalikes(text: str):
    return [(c, unicodedata.name(c, "?")) for c in text if ord(c) > 127]


def load_all():
    d = INPUTS / "data"
    leads = read_csv(d / "1_crm_leads.csv")
    demos = {int(r["lead_id"]): r for r in read_csv(d / "2_demo_class_evaluations.csv")}
    calls = {int(r["lead_id"]): r for r in read_csv(d / "3_sales_call_logs.csv")}
    orders = {int(r["lead_id"]): r for r in read_csv(d / "4_live_orders_and_invoices.csv")}
    policy = {int(r["class_id"]): r for r in read_csv(d / "reference_courses_pricing_and_compliance_policy.csv")}
    by_code = {r["lead_code"]: r for r in leads}
    return dict(leads=leads, by_code=by_code, demos=demos, calls=calls, orders=orders, policy=policy)


def lead_id(code: str) -> int:
    return int(code.split("-")[1])


def dump(path, obj):
    pathlib.Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
