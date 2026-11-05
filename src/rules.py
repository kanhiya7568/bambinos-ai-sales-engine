"""Deterministic rule layer: no LLM. Payment, discount math, duplicates, data quality, SLA clocks.

These checks run BEFORE and AFTER the LLM so that money, identity and policy facts are never
left to model judgement.
"""
import re
from collections import defaultdict
from datetime import timedelta

from common import non_ascii_lookalikes, tz_of, to_utc

SLA_FIRST_CALL_HOURS = 2.0
LAZY_DISPOSITIONS = {"Call back tomorrow", "Call back", "Interested", "Thinking", "Busy", "Price issue"}
OPEN_STAGES = {"Follow_Up_Hot", "Follow_Up_Warm", "Follow_Up_Cold", "Payment_Link_Sent", "Demo_Completed_Uncalled"}
FEE_COL = {"INR": "standard_fee_india_inr", "AED": "standard_fee_gcc_aed", "USD": "standard_fee_usa_usd"}


def cap_pct(policy_row) -> float:
    m = re.match(r"\s*(\d+)%", policy_row["max_rep_discount_allowed_pct"])
    return float(m.group(1)) if m else 10.0


def catalog_fee(policy_row, currency):
    col = FEE_COL.get(currency)
    return float(policy_row[col]) if col and policy_row.get(col) else None


def order_flags(order, policy_row):
    """Independent arithmetic on a payment-gateway row vs the official catalog."""
    out = []
    cur = order["currency"]
    std, disc, net = float(order["standard_amount"]), float(order["discount_applied"]), float(order["net_payable_amount"])
    fee = catalog_fee(policy_row, cur) if policy_row else None
    cap = cap_pct(policy_row) if policy_row else 10.0
    if fee is None:
        out.append(("CATALOG_GAP", f"No {cur} fee for class {order['class_id']} in the catalog; amount {net:g} {cur} cannot be verified"))
    elif abs(std - fee) > 0.5:
        out.append(("PRICE_MISMATCH_VS_CATALOG", f"order standard_amount {std:g} {cur} vs catalog {fee:g} {cur} ({std / fee:.0f}x)"))
    base = fee or std
    pct = disc / base * 100 if base else 0.0
    if pct > cap + 0.01:
        out.append(("DISCOUNT_ANOMALY", f"discount {disc:g} {cur} = {pct:.1f}% of catalog fee vs cap {cap:g}% (limit {base * cap / 100:g} {cur})"))
    plan = order["payment_plan_type"]
    expected = (base - disc) / 2 if plan.startswith("Installment_1_of_2") else base - disc
    if abs(net - expected) > 0.5:
        out.append(("NET_AMOUNT_MISMATCH", f"net {net:g} vs expected {expected:g}"))
    if "Unauthorized_Custom_Link" in plan:
        out.append(("UNAUTHORIZED_LINK", f"payment plan type is '{plan}'"))
    reason = order.get("gateway_error_reason") or ""
    m = re.search(r"(\d+)%\s*Max Cap", reason)
    if m and float(m.group(1)) != cap:
        out.append(("POLICY_RULE_MISMATCH", f"gateway rule says {m.group(1)}% cap, catalog policy says {cap:g}%"))
    return out


def hours_between(a, b):
    return (b - a).total_seconds() / 3600.0


def leak_audit(data, as_of_utc):
    """Audit the 12-lead CRM table for pipeline leaks. Returns list of findings."""
    F = []
    leads, demos, calls, orders, policy = (data[k] for k in ("leads", "demos", "calls", "orders", "policy"))

    def add(lead, typ, sev, detail, hours=None):
        F.append(dict(lead=lead["lead_code"], owner=lead["assigned_counsellor_name"], type=typ, severity=sev,
                      detail=detail, hours=None if hours is None else round(hours, 1)))

    # duplicates
    groups = defaultdict(list)
    for r in leads:
        groups[(r["user_id"], r["student_id"])].append(r)
    dup_of = {}
    for g in groups.values():
        if len(g) > 1:
            g.sort(key=lambda r: r["created_at"])
            for later in g[1:]:
                dup_of[later["lead_code"]] = g[0]["lead_code"]
                add(later, "DUPLICATE_LEAD", "P2",
                    f"duplicates {g[0]['lead_code']} (same user_id/student_id/mobile); owners {g[0]['assigned_counsellor_name']} vs {later['assigned_counsellor_name']}")

    for r in leads:
        code, lid, tz = r["lead_code"], int(r["id"]), tz_of(r["city_timezone"])
        demo, order, call = demos.get(lid), orders.get(lid), calls.get(lid)
        pol = policy.get(int(r["class_id"]))

        # uncalled demos
        if r["crm_lead_stage"] == "Demo_Completed_Uncalled" and demo:
            demo_end = to_utc(demo["demo_completed_at"], tz)
            h = hours_between(demo_end, as_of_utc)
            add(r, "UNCALLED_DEMO", "P1",
                f"demo ended {demo['demo_completed_at']} {tz}; engagement {demo['child_engagement_score_1_to_5']}/5; no call after {h:.0f} h (SLA {SLA_FIRST_CALL_HOURS:g} h)", h)

        # payment states
        if order:
            for typ, detail in order_flags(order, pol):
                sev = "P0" if typ in ("DISCOUNT_ANOMALY", "UNAUTHORIZED_LINK") else "P2"
                add(r, typ, sev, f"order {order['order_id']}: {detail}")
            st = order["payment_link_status"]
            if st == "Paid" and r["crm_lead_stage"] != "Enrolled_Paid":
                add(r, "PAID_BUT_CRM_OPEN", "P0",
                    f"order {order['order_id']} paid {order['paid_at']}; CRM stage still '{r['crm_lead_stage']}', next follow-up {r['next_followup_at']} would nag a paying parent")
            if st == "Payment_Failed":
                fail = to_utc(order["updated_at"], tz)
                add(r, "PAYMENT_FAILED_UNRECOVERED", "P0",
                    f"order {order['order_id']} {order['gateway_error_reason']}; no recovery logged {hours_between(fail, as_of_utc):.0f} h later", hours_between(fail, as_of_utc))
            if st.startswith("Unpaid_Link_Opened"):
                add(r, "LINK_OPENED_NOT_PAID", "P1", f"order {order['order_id']}: link opened twice, unpaid; strong buying signal")

        # follow-up hygiene
        nf, lc = to_utc(r["next_followup_at"], tz), to_utc(r["last_call_at"], tz)
        if nf and lc and nf < lc:
            add(r, "FOLLOWUP_BEFORE_LAST_CALL", "P2", f"next_followup_at {r['next_followup_at']} is earlier than last_call_at {r['last_call_at']}: stale/invalid", hours_between(nf, as_of_utc))
        elif nf and nf < as_of_utc and r["crm_lead_stage"] in OPEN_STAGES:
            add(r, "FOLLOWUP_OVERDUE", "P1", f"follow-up due {r['next_followup_at']} {tz}; no activity logged since", hours_between(nf, as_of_utc))
        if not nf and r["crm_lead_stage"] in OPEN_STAGES and code not in dup_of:
            add(r, "NO_FOLLOWUP_SCHEDULED", "P1", f"open stage '{r['crm_lead_stage']}' with next_followup_at NULL")

        # note quality
        note, disp = (r["manual_rep_notes"] or ""), (r["manual_rep_disposition"] or "")
        if lc and (len(note.split()) <= 4 or disp in LAZY_DISPOSITIONS):
            add(r, "LAZY_DISPOSITION", "P2", f"disposition '{disp}' / note '{note}' carries no usable intent or next step")

        # call record gaps
        if lc and lid not in calls:
            add(r, "CALL_RECORD_MISSING", "P2", f"CRM shows a call at {r['last_call_at']} but no recording/transcript is in the call log")

        # data quality
        bad = non_ascii_lookalikes(r["student_name"] + r["parent_name"])
        if bad:
            add(r, "DATA_QUALITY_NON_ASCII", "P2", f"look-alike letters in name {r['student_name']!r}: " + ", ".join(n for _, n in bad))

        # catalog gap
        if not pol:
            add(r, "CATALOG_GAP", "P1", f"class_id {r['class_id']} ('{r['course_pitched']}') is not in the reference pricing/policy table")

    return F


def speed_to_lead(data, as_of_utc):
    """Minutes from demo end to first call for called leads; hours-without-call for uncalled."""
    called, uncalled = [], []
    for r in data["leads"]:
        lid, tz = int(r["id"]), tz_of(r["city_timezone"])
        demo = data["demos"].get(lid)
        if not demo:
            continue
        end = to_utc(demo["demo_completed_at"], tz)
        lc = to_utc(r["last_call_at"], tz)
        if lc:
            called.append((r["lead_code"], (lc - end).total_seconds() / 60))
        elif r["crm_lead_stage"] == "Demo_Completed_Uncalled":
            uncalled.append((r["lead_code"], hours_between(end, as_of_utc)))
    return called, uncalled
