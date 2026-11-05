# Bambinos.live - AI Post-Demo Conversion & Call Intelligence Engine

AI Program Manager (Sales) take-home case. **Call audit + CRM structuring + personalised WhatsApp follow-up**, run on all 6 recorded calls and the 12-lead CRM table.

> Report (Deliverables A, B, D): [`docs/Bambinos_AI_PM_Sales_Case_Report.pdf`](docs/Bambinos_AI_PM_Sales_Case_Report.pdf)

## What is in this repo
| Path | What it is |
|---|---|
| `prompts/01_call_audit_and_compliance.md` | 7-dimension scorecard, anti-gaming rule, compliance catalog (CR/HR/MR/LR) |
| `prompts/02_crm_extraction.md` | CRM taxonomy, anchored 1-10 intent score, objection buckets, next-best-action, deterministic post-rules |
| `prompts/03_whatsapp_followup.md` | 3-touch WhatsApp generator with STOP-mode logic and 11 writing rules |
| `prompts/04_rep_coaching_and_judge.md` | Rep coaching note + grounding-judge verifier |
| `outputs/call_audit_scorecards.md` and `outputs/call_audits/*.json` | Score, evidence quotes, compliance flags, coaching, escalation for each of the 6 calls |
| `outputs/crm_cleaned.csv` / `.json` | Cleaned CRM row for all 12 leads (intent, objection, highlight, next action, AI note) |
| `outputs/whatsapp_sequences.md` / `.json` | 3-touch sequence or STOP alert for all 12 leads |
| `outputs/pipeline_leak_audit.md` / `.json` | 31 pipeline leaks found (unrecovered payments, paid-but-open, uncalled demos, duplicate, discount anomaly, catalog gaps) |
| `src/` | `rules.py` (deterministic checks), `run.py` (quote verification, weighted scoring, rendering), `common.py` |
| `schemas/` | JSON-schema skeletons for the three LLM outputs |
| `inputs/` | Official transcripts and CSVs copied unchanged from the assessment repo |

## How the outputs were produced (honest note)
The LLM step (audit, CRM extraction, WhatsApp drafts) was executed by an LLM following the prompts in `prompts/`, given each call's packet (transcript + demo evaluation + policy row + order row). No live n8n/Make instance or WhatsApp account was connected. Everything the LLM produced is then **checked by code** (`python src/run.py`):

1. every evidence quote must be a verbatim substring of the transcript at the stated timestamp (all pass);
2. the total score is computed in code from integer dimension scores and fixed weights; a CRITICAL flag caps it at 40;
3. payment status overrides conversation (LEAD-804 must be `Enrolled_Paid`, intent 10, STOP);
4. discount maths, price-vs-catalog, duplicates, name hygiene, stale follow-ups and SLA clocks are rule-based;
5. every WhatsApp text is checked for <=70 words, <=1 question and banned phrases.

Run it: `python3 -I src/run.py` (Python 3.10+, standard library only). It re-validates and regenerates the Markdown/CSV files.

## Headline results
| Call | Lead | Score | Gate | Why |
|---|---|---|---|---|
| 7001 | LEAD-801 | 91 | Clear | Consultative benchmark; spouse objection turned into a forwardable proof pack |
| 7002 | LEAD-802 | 24 | Review | Price at 00:30, fake 30-min expiry, parent's word-problem question unanswered |
| 7003 | LEAD-803 | 2 | **Critical hold** | Rank-1 guarantee, 42.1% discount (cap 10%), 6-month refund, blacklist threat |
| 7004 | LEAD-804 | 93 | Clear | Schedule solved live; parent **already paid**, CRM stale -> STOP cadence |
| 7005 | LEAD-805 | 73 | Clear | Good Hinglish call; UPI mandate failed, needs same-day recovery |
| 7006 | LEAD-806 | 7 | Review | Rubric gaming detected; micro-batch remedy denied; recoverable via Ops |

## Assumptions
CRM/order timestamps are lead-local and normalised to UTC (offsets for Nov 2026). Snapshot clock for SLA maths: 2026-11-03 20:00 UTC. Seat counts, the "Exam Pause" feature and the 96-class AED 2,100 package are not in the data and are flagged as unverified, not accepted as fact.
