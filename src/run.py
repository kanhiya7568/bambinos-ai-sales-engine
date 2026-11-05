"""Pipeline runner: validate LLM outputs -> deterministic rules -> render CRM/scorecards/WhatsApp.
Usage: python src/run.py   (offline; reads outputs/*.json produced by the prompts, see README)"""
import csv, glob, json, re, sys
from datetime import datetime, timezone
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import *
from rules import *

W = {"D1_rapport": 10, "D2_discovery": 20, "D3_pitch_before_price": 15, "D4_objection_handling": 20,
     "D5_honest_urgency_close": 15, "D6_listening_balance": 10, "D7_compliance_accuracy": 10}
AS_OF = datetime(2026, 11, 3, 20, 0, tzinfo=timezone.utc)   # snapshot time used for SLA clocks
BANNED = ["kindly confirm", "last chance", "act now", "100% guarantee", "limited seats"]
data = load_all(); problems = []

# ---- 1. audits: validate quotes verbatim, compute weighted score in code
audits = []
for f in sorted(glob.glob(str(OUT / "call_audits" / "*.json"))):
    a = json.load(open(f, encoding="utf-8"))
    tr = parse_transcript(INPUTS / "call_transcripts" / data["calls"][lead_id(a["lead_code"])]["transcript_filename"])
    quotes = [e for d in a["scorecard"].values() for e in d["evidence"]] + [e for fl in a["compliance_flags"] for e in fl["evidence"]]
    for e in quotes:
        spk_txt = tr.get(e["ts"])
        if not spk_txt or norm(e["quote"]) not in norm(spk_txt[1]):
            problems.append(f"{a['lead_code']} quote not found at {e['ts']}: {e['quote'][:50]}")
    for k, d in a["scorecard"].items():
        if d["score"] >= 3 and not d["evidence"]: problems.append(f"{a['lead_code']} {k} score>=3 without evidence")
    raw = sum(d["score"] / 5 * W[k] for k, d in a["scorecard"].items())
    crit = any(fl["severity"] == "CRITICAL" for fl in a["compliance_flags"])
    a["raw_score"] = round(raw, 1); a["total_score"] = min(raw, 40) if crit else round(raw, 1)
    a["capped"] = crit and raw > 40
    audits.append(a)
    json.dump(a, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ---- 2. CRM: rules override model
crm = json.load(open(OUT / "crm_cleaned_raw.json", encoding="utf-8")); final = []
for r in crm:
    lead = data["by_code"][r["lead_code"]]; o = data["orders"].get(lead_id(r["lead_code"]))
    if o and o["payment_link_status"] == "Paid":
        assert r["lead_stage"] == "Enrolled_Paid" and r["intent"]["score"] == 10 and r["follow_up_mode"] == "STOP", "payment override"
    r["rule_flags"] = [f"{t}: {d}" for t, d in order_flags(o, data["policy"].get(int(lead["class_id"]))) ] if o else []
    r["crm_changes"] = [{"field": "crm_lead_stage", "old": lead["crm_lead_stage"], "new": r["lead_stage"]},
                        {"field": "manual_rep_disposition", "old": lead["manual_rep_disposition"], "new": f'{r["primary_objection"]} ({r["objection_status"]})'},
                        {"field": "manual_rep_notes", "old": lead["manual_rep_notes"], "new": r["ai_note"]},
                        {"field": "next_followup_at", "old": lead["next_followup_at"], "new": r["nba"]["due_local"]}]
    final.append(r)
dump(OUT / "crm_cleaned.json", final)
cols = ["lead_code","owner","priority","lead_stage","intent_band","intent_score","primary_objection","objection_status","secondary_objections","sub_reason","blocker_now","child_demo_highlight","next_best_action","nba_owner","due_local","follow_up_mode","ai_note","rep_logged_disposition","rep_logged_note","discrepancy_with_rep_log","rule_flags"]
with open(OUT / "crm_cleaned.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols)
    for r in final:
        L = data["by_code"][r["lead_code"]]
        w.writerow([r["lead_code"], r["owner"], r["priority"], r["lead_stage"], r["intent"]["band"], r["intent"]["score"], r["primary_objection"], r["objection_status"],
                    "; ".join(s["type"] if isinstance(s, dict) else s for s in r["secondary_objections"]), r["sub_reason"], r["blocker_now"] or "",
                    r["demo_highlight"]["parent_safe_line"], f'{r["nba"]["type"]}: {r["nba"]["action"]}', r["nba"]["owner"], r["nba"]["due_local"], r["follow_up_mode"],
                    r["ai_note"], L["manual_rep_disposition"], L["manual_rep_notes"], r["discrepancy"]["explanation"] or "", " | ".join(r["rule_flags"])])

# ---- 3. WhatsApp validation + markdown
wa = json.load(open(OUT / "whatsapp_sequences.json", encoding="utf-8")); md = ["# WhatsApp follow-up sequences (generated)\n"]
for s in wa:
    md.append(f"\n## {s['lead_code']} - mode **{s['mode']}** ({s['language']})\n")
    if s.get("stop_alert"):
        a = s["stop_alert"]; md.append(f"**STOP ALERT ({a['reason']})** -> notify: {', '.join(a['notify'])}\n" + "\n".join(f"- {x}" for x in a["actions"]) + "\n")
    for t in s["touches"]:
        words = len(re.sub(r"\{\{.*?\}\}", "x", t["text"]).split())
        if words > 70: problems.append(f"{s['lead_code']} T{t['n']} {words} words")
        if t["text"].count("?") > 1 and t["n"] > 0: problems.append(f"{s['lead_code']} T{t['n']} multiple questions")
        for b in BANNED:
            if b in t["text"].lower(): problems.append(f"{s['lead_code']} T{t['n']} banned phrase {b}")
        md.append(f"**T{t['n']}** · {t['class']} · {t['template_category']} · _{t['send_rule']}_ ({words} words)\n> {t['text']}\n\n_Grounding:_ {', '.join(t['grounding'])}" + (f"  \n_Pre-send checks:_ {'; '.join(t['pre_send_checks'])}" if t.get("pre_send_checks") else "") + "\n")
    if s.get("manager_draft"): md.append(f"**Manager-only draft ({s['manager_draft']['class']})** - {s['manager_draft']['note']}\n> {s['manager_draft']['text']}\n")
    md.append("_Never send:_ " + "; ".join(s["never_send"]) + "\n")
(OUT / "whatsapp_sequences.md").write_text("\n".join(md), encoding="utf-8")

# ---- 4. scorecards + leak audit
sc = ["# Call audit scorecards\n", "| Call | Lead | Rep | D1 | D2 | D3 | D4 | D5 | D6 | D7 | Score /100 | Gate | Flags |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for a in audits:
    d = a["scorecard"]; sc.append(f"| {a['call_id']} | {a['lead_code']} | {a['counsellor']} | " + " | ".join(str(d[k]["score"]) for k in W) + f" | **{a['total_score']:g}**{' (capped from '+str(a['raw_score'])+')' if a['capped'] else ''} | {a['compliance_gate']} | {', '.join(f['id'] for f in a['compliance_flags']) or '-'} |")
sc.append("\nScore = sum(dimension/5 x weight); weights D1 10, D2 20, D3 15, D4 20, D5 15, D6 10, D7 10. A CRITICAL flag caps the total at 40.\n")
for a in audits:
    sc.append(f"\n## {a['lead_code']} - {a['counsellor']} - {a['total_score']:g}/100\n**{a['headline']}**\n")
    for k, d in a["scorecard"].items(): sc.append(f"- {k} **{d['score']}/5**: {d['why']}" + (f" _[{d['evidence'][0]['ts']}] \"{d['evidence'][0]['quote'][:90]}\"_" if d["evidence"] else ""))
    for fl in a["compliance_flags"]: sc.append(f"- **{fl['id']} ({fl['severity']})** {fl['why']} _Policy: {fl['policy_reference']}_")
    c = a["coaching"]; sc.append(f"\n**Coaching ({c['route']}):** {c['note'] or 'Not sent to rep; routed to manager.'}\n\n_Manager summary:_ {c['manager_summary']}")
    if a["escalation"]["required"]: sc.append(f"\n**Escalation:** {a['escalation']['route_to']} within {a['escalation']['sla_minutes']} min. {a['escalation']['reason']}")
    sc.append("\n_CRM hygiene:_ " + " / ".join(a["post_call_hygiene"]))
(OUT / "call_audit_scorecards.md").write_text("\n".join(sc), encoding="utf-8")

leaks = leak_audit(data, AS_OF); dump(OUT / "pipeline_leak_audit.json", leaks)
lk = ["# CRM pipeline leak audit (12 leads)\n", f"Snapshot: {fmt_utc(AS_OF)}. All CRM timestamps normalised from lead-local time to UTC.\n", "| Lead | Owner | Type | Sev | Detail |", "|---|---|---|---|---|"]
for x in sorted(leaks, key=lambda x: (x["severity"], x["lead"])): lk.append(f"| {x['lead']} | {x['owner']} | {x['type']} | {x['severity']} | {x['detail']} |")
called, unc = speed_to_lead(data, AS_OF)
lk.append("\n**Speed-to-lead (demo end to call, minutes):** " + ", ".join(f"{c} {m:.0f}" for c, m in called) + "\n\n**Uncalled demos (hours since demo, SLA 2 h):** " + ", ".join(f"{c} {h:.1f} h" for c, h in unc))
(OUT / "pipeline_leak_audit.md").write_text("\n".join(lk), encoding="utf-8")

print("audits", len(audits), "crm", len(final), "wa", len(wa), "leaks", len(leaks))
print("scores", {a["lead_code"]: a["total_score"] for a in audits})
print("PROBLEMS:", *problems, sep="\n  ") if problems else print("validation: all quotes verbatim, all WhatsApp checks pass")
