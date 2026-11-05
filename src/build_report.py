import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; A = ROOT / "assets"; A.mkdir(exist_ok=True)

# ---------- pipeline diagram
fig, ax = plt.subplots(figsize=(11, 4.6)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(0, 4.6)
def box(x, y, w, h, t, fc, ec="#1F2A44", fs=7.6, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", wrap=True)
def arr(x1, y1, x2, y2): ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", color="#1F2A44", lw=1.2))
row = [("1 Call ends\n(Zoom/telephony\nwebhook)", "#E8EEF9"), ("2 Transcribe\n+ diarise\n(Hindi/English)", "#E8EEF9"), ("3 Build context\npacket: transcript,\ndemo eval, policy,\norder, CRM row", "#E8EEF9"),
       ("4 AI analysis\n(parallel)\nA Audit+Compliance\nB CRM extract", "#FFF3D6"), ("5 Validate\nquotes, maths,\npayment override,\njudge pass", "#DDF3E4")]
for i, (t, c) in enumerate(row):
    box(0.2 + i * 2.1, 3.0, 1.8, 1.3, t, c); 
    if i: arr(0.2 + i * 2.1 - 0.3, 3.65, 0.2 + i * 2.1, 3.65)
arr(10.4, 3.65, 10.6, 3.65) if False else None
arr(9.5, 3.0, 9.5, 2.55)
box(0.2, 1.35, 3.3, 1.15, "6a Auto-CRM update (stage, intent 1-10,\nobjection, highlight, next action, AI note)\nPayment status always wins", "#DDF3E4", fs=7.4)
box(3.8, 1.35, 3.3, 1.15, "6b Coaching alert to REP first (5 min)\nCritical compliance: Manager alert,\n5-min SLA, no rep coaching note", "#FDE4E1", fs=7.4)
box(7.4, 1.35, 3.4, 1.15, "6c C WhatsApp 3-touch drafts\nAUTO: payment retry/onboarding only\nAPPROVE: persuasion  |  MANAGER: damaged trust", "#FFF3D6", fs=7.4)
for x in (1.85, 5.45): arr(9.5, 2.55, x, 2.5)
arr(9.5, 2.55, 9.1, 2.5)
box(0.2, 0.15, 10.6, 0.8, "7 Feedback loop: reply / payment webhook / opt-out stop the cadence | manager disputes recalibrate rubric | weekly metrics: speed-to-lead, recovery rate, flags, conversion", "#E8EEF9", fs=7.6)
for x in (1.85, 5.45, 9.1): arr(x, 1.35, x, 0.95)
fig.savefig(A / "pipeline.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# ---------- styles
NAVY = colors.HexColor("#1F2A44"); TEAL = colors.HexColor("#0F766E"); LIGHT = colors.HexColor("#F1F5F9")
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY, spaceBefore=6, spaceAfter=5)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.6, textColor=TEAL, spaceBefore=7, spaceAfter=3)
B = ParagraphStyle("b", fontName="Helvetica", fontSize=8.6, leading=11.4, spaceAfter=3)
BL = ParagraphStyle("bl", parent=B, leftIndent=9, bulletIndent=0, spaceAfter=1.5)
C = ParagraphStyle("c", fontName="Helvetica", fontSize=7.4, leading=9.2)
CH = ParagraphStyle("ch", parent=C, fontName="Helvetica-Bold", textColor=colors.white)
def P(t, s=B): return Paragraph(t, s)
def bl(items): return [Paragraph(i, BL, bulletText="•") for i in items]
def tbl(rows, widths, head=True, zebra=True):
    data = [[Paragraph(str(c), CH if (head and r == 0) else C) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if head else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    if zebra: st += [("BACKGROUND", (0, r), (-1, r), LIGHT) for r in range(2, len(rows), 2)]
    t.setStyle(TableStyle(st)); return t
def footer(c, d):
    c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.grey)
    c.drawString(15 * mm, 8 * mm, "Bambinos.live | AI Program Manager (Sales) take-home | Kanhiya Singh"); c.drawRightString(195 * mm, 8 * mm, f"Page {d.page}"); c.restoreState()

S = []
# ---------- cover + exec summary
S += [P("AI Post-Demo Conversion &amp; Call Intelligence Engine", ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY, leading=24)),
      P("Case report for the AI Program Manager (Sales) take-home | Deliverables A, B, D (C is in the GitHub repo) | Candidate: Kanhiya Singh", ParagraphStyle("s", parent=B, textColor=colors.grey, spaceAfter=8)),
      P("1. Executive summary", H1),
      P("Bambinos loses revenue at three points after a demo: calls nobody reviews, CRM notes nobody can use, and follow-ups parents ignore. I designed one pipeline that audits every counselling call, writes the CRM row, and drafts a child-specific WhatsApp sequence, and I ran it on the 6 supplied calls and 12 CRM leads. <b>The data showed the leaks are real and mostly mechanical</b>, which is why the design leans on deterministic rules around the LLM."),
      tbl([["Finding from the supplied data", "Evidence"],
           ["Call quality spans 2 to 93 out of 100 within one team", "Scores 91, 24, 2, 93, 73, 7. Benchmark calls (801, 804) sell by solving the parent's real problem; weak calls quote price within 30-45 seconds"],
           ["One call is a legal and brand risk", "Call 3 (LEAD-803): 6 critical flags in 12 minutes: Rank-1 guarantee in writing, 42.1% discount (cap 10%), 6-month refund, blacklist threat on a 7-year-old, 1-on-1 claimed at group price, 'hacked my manager's quota'. Paid link 99403 is live"],
           ["A paying parent is about to be nagged", "LEAD-804 paid USD 265 at 11:40 PST; CRM still says Payment_Link_Sent with a 20:00 follow-up scheduled"],
           ["Two failed payments sit unrecovered 5-6 hours", "LEAD-805 (UPI mandate OTP timeout) and LEAD-809 (3DS declined): parents said yes and tried to pay"],
           ["High-intent demos never called", "LEAD-807 (5/5 on challenge, asked when the batch starts): 34 h; LEAD-812: 7.5 h. SLA is 2 h"],
           ["Reps log vague, wrong dispositions", "6 of 9 called leads: e.g. 803 logged 'Interested, will pay today' while the parent said 'Do not call me again'; 806 logged 'child not interested' but the cause was a demo placement error"],
           ["Rubric gaming is a real attack", "Call 6: rep reads 'Discovery Question 1, 2, 3' in 30 seconds. Parent responses must confirm that a behaviour landed before it earns credit"]],
          [58, 122]),
      Spacer(1, 4), P("<b>Business case (Section 5):</b> +2 to +3 percentage points of demo-to-paid is +20 to +30 enrolments per week, about Rs. 2.1-3.2 lakh per week or Rs. 1.0-1.5 crore per year, against an estimated Rs. 43,000 per week to run. Break-even is 4 extra enrolments a week (0.41 pp). Manager review coverage goes from 2% to 100% of calls for about 25 manager hours per week."),
      P("<b>What I did not do:</b> I did not connect live n8n, a CRM or WhatsApp. The LLM step was run by an LLM following the published prompts and every output was then verified by code (all evidence quotes verbatim, scores computed in code). The repo documents this plainly.", B)]
S.append(PageBreak())

# ---------- A
S += [P("2. Deliverable A: Sales discovery and call evaluation framework", H1), P("2.1 Why parents buy kids' courses (hypotheses grounded in the 12 supplied leads)", H2),
      P("Across markets the parent is buying <b>proof that their child's specific problem gets fixed</b>, from a teacher they trust, at a price that feels fair against the alternative they already know. Markets differ in who decides and what the 'alternative' is. These are working hypotheses drawn from the supplied calls and general sector experience; the 30-day pilot validates them with real conversion data."),
      tbl([["Market", "Who decides / pays", "What they are really buying", "Typical objection (in data)", "What the call must do"],
           ["India (801, 803, 805, 806)", "Joint decision; one parent often evaluates, the other pays (801: father holds the card; 805: 'mummy bol rahi hain')", "Confidence in speaking/reading, exam results, a gentle teacher; value vs 1-on-1 competitors", "Spouse approval, exam season, instalments, PlanetSpark comparison", "Find the absent decision-maker and give a forwardable proof; offer instalments; reply in the parent's language"],
           ["GCC (802, 808)", "Expat parent; benchmarks against local tuition and the school's curriculum (British)", "Fix a named curriculum gap (word problems) with a visible method", "'Why pay AED 1,200 vs AED 350 local tutor?'", "Explain the method vs rote worksheets before any price; show what the teacher saw"],
           ["USA/UK (804, 809, 812)", "One parent, busy, schedule-driven; pays instantly if fit is clear", "Values/character and focus without 'lectures'; flexible slots around sport", "Schedule clash; card friction (3DS)", "Solve the schedule live; send the link at once; recover payment failures fast"]], [24, 38, 40, 36, 42]),
      P("2.2 Seven-point call quality scorecard (weights sum to 100)", H2),
      tbl([["Dimension", "Wt", "A 5/5 call looks like", "Auto-fail signals", "Evidence rule"],
           ["D1 Rapport and child-specific praise", "10", "Names a real demo moment that matches the teacher's note; parent warms", "Generic or contradicted praise ('natural Grandmaster' for a 2/5 demo)", "Quote the rep line and the parent's reaction"],
           ["D2 Diagnosing the learning pain", "20", "Pain surfaced, linked to a demo observation, decision-maker/timeline known and reused", "3+ questions in one turn; reading 'Discovery Question 1...'", "Question counts only if the rep later uses the answer"],
           ["D3 Curriculum pitch before price", "15", "Pain, then method seen in demo, then structure (batch size, showcase), price only after fit", "Price in first 2 minutes; company monologue", "Timestamp of first price vs first value statement"],
           ["D4 Objection handling", "20", "Acknowledge, isolate, answer with the child's own evidence, create a next step that removes the blocker", "Brand claims, discount as deflection, dismissing the child", "Parent's next turn must show it landed"],
           ["D5 Honest urgency and trial close", "15", "Dated next step agreed by parent; scarcity only if verified", "Fake expiry, '5 minutes', pay after 'let me think'", "Next step with date/time in transcript"],
           ["D6 Listening and talk balance", "10", "Rep talk about 40-55%; every parent question answered", "Rep over 70%; parent says 'are you listening?'", "Talk ratio plus unanswered-question count"],
           ["D7 Compliance and accuracy", "10", "Price, refund, discount, batch size match the catalog", "Any CRITICAL flag sets total cap at 40", "Compare claim to the policy row"]], [32, 8, 50, 44, 46]),
      P("Scoring is deterministic: the model returns integer 0-5 anchors; <b>code</b> computes the weighted total. A CRITICAL compliance flag caps the score at 40 and escalates in 5 minutes. Every score of 3 or higher requires a verbatim, timestamped quote, which the pipeline verifies character-for-character against the transcript.", B)]
S.append(PageBreak())
S += [P("2.3 Structured CRM taxonomy (what the AI must write)", H2),
      tbl([["Field", "Allowed values and rules"],
           ["Intent score (Hot/Warm/Cold + 1-10)", "Hot 8-10, Warm 4-7, Cold 1-3. Anchored: 10 paid (from order row only); 9 verbal yes + payment attempted/failed or 'will pay at time'; 8 fee and batch accepted, one resolvable blocker with dated next step; 7 start-intent signal or fee accepted without a date; 6 strong fit, key question unanswered; 5 engaged with a specific pain, alternative in play; 4 open to an alternative not yet offered; 3 indefinite deferral; 2 refusal or negative child with no remedy; 1 explicit refusal or trust broken"],
           ["Primary objection (exactly one)", "Price | Spouse_Decision | Schedule_Conflict | Child_Not_Interested | Competitor_Comparison | None_Identified, plus Other_Trust_Or_Compliance for rep-caused trust breaks. The parent's words decide it, not the rep's note (802: logged 'Price', actually Competitor_Comparison). Status: Resolved, Open or Latent; up to 3 secondary objections; mandatory sub_reason"],
           ["Child's demo highlight", "Verbatim demo_magic_moment_for_parent plus a parent-safe line of 20 words or fewer. Never invented"],
           ["Lead stage", "Needs_First_Call, Hot_Closing, Payment_Recovery, Warm_Nurturing, Cold_Reengage, Enrolled_Paid, Compliance_Hold, Duplicate_Merged. Payment webhook overrides conversation"],
           ["Next best action + due time", "ACT-01 forwardable proof for absent decision-maker; 02 fresh payment link with another method; 03 schedule alternative; 04 manager escalation; 05 Ops confirms micro-batch/1-on-1; 06 first call in SLA; 07 stop selling and onboard; 08 merge duplicate; 09 value-proof follow-up; 10 dated nurture; 11 fix missing data; 12 re-engage unclear callback. Due times follow rules (e.g. payment failure + 30 min; marketing messages inside 09:00-20:30 local)"],
           ["Hygiene fields", "AI note of 40 words or fewer for the next person; crm_changes (old to new); discrepancy_with_rep_log flag; priority P0-P3; follow_up_mode AUTO | COUNSELLOR_APPROVE | MANAGER_ONLY | STOP"]], [42, 138]),
      P("Example (LEAD-801): rep logged 'Call back tomorrow / will ask husband'. The AI writes Hot (8), Spouse_Decision (Open), 'father missed demo, will ask: is this just grammar tuition?', action ACT-01 send the 60-second proof pack before 19:30, call at 11:00. Full rows for all 12 leads are in <font name='Courier'>outputs/crm_cleaned.csv</font>.", B),
      P("3. Deliverable B: End-to-end workflow and guardrails", H1), Image(str(A / "pipeline.png"), width=178 * mm, height=178 * mm * 4.6 / 11 * 0.93),
      P("3.1 No-code build (n8n or Make + Google Sheets/CRM + WhatsApp Cloud API)", H2)] + bl([
    "<b>Trigger:</b> Zoom/telephony 'recording completed' webhook into n8n. <b>Transcription:</b> a speech-to-text API with diarisation and Hindi-English support; store transcript with timestamps.",
    "<b>Context packet:</b> Sheets/CRM lookups by lead ID: demo evaluation, catalog policy row, live order row. Mask PII (name, phone, email) before it reaches the LLM and restore by lead ID afterwards.",
    "<b>AI calls (parallel):</b> Prompt 01 (audit + compliance) and Prompt 02 (CRM). Then Prompt 03 (WhatsApp) only after validation. Temperature 0, JSON-schema constrained, one retry, then human QA.",
    "<b>Code node:</b> verbatim quote check, weighted score, discount maths, payment override, duplicate check, 70-word and banned-phrase checks. <b>Judge pass:</b> a second cheap model verifies each claim against the packet.",
    "<b>Write-back:</b> CRM update (old to new logged), Slack/WhatsApp coaching note to the rep, manager digest, WhatsApp scheduled via approved templates. Payment webhooks (Razorpay/Stripe) and parent replies stop the cadence in real time."])
S.append(PageBreak())
S += [P("3.2 Guardrails and human-in-the-loop", H2),
      tbl([["Action", "Mode", "Reason"],
           ["CRM field updates (stage, intent, objection, notes)", "Auto, with old/new log and rep dispute button", "Low risk, reversible, saves 2-3 rep hours per week"],
           ["Payment failure retry, payment-received onboarding, reminder of an already agreed call", "<b>Auto</b>", "Adds no new commercial term and no claim about the child"],
           ["Anything that recaps the child's performance, explains the programme, or mentions a plan", "<b>Counsellor clicks Approve</b>", "Persuasion; one wrong claim harms trust. Approval takes one tap and the draft is already personalised"],
           ["Discounts, off-catalog links, refunds, damaged-trust leads (803, 806), compliance holds", "<b>Manager only</b>", "Money, legal and brand risk; AI never offers a discount that is not in an approved_offer field"],
           ["Opt-out word, DNC, reply from parent, payment received, duplicate lead", "Hard stop of the cadence", "Respect for the parent; avoid nagging a paying family"]], [78, 42, 60]),
      P("3.3 Compliance red flags the AI must catch (fixed IDs; severity decides routing)", H2),
      tbl([["Severity", "Flags", "Routing"],
           ["CRITICAL (cap score 40, manager in 5 min)", "CR-01 outcome guarantees (rank, marks, reading level in N days, Olympiad medal); CR-02 unauthorised discount or off-catalog link; CR-03 off-policy refund promise or 'off the record'; CR-04 coercion or threats (blacklist, 5-minute deadline); CR-05 product misrepresentation (1-on-1 at group price, fake 'Elite batch'); CR-06 rude or abusive language; CR-07 admission of bypassing controls", "Manager and compliance review; payment link voided; rep coaching note not sent (handled in person)"],
           ["HIGH (manager digest in 24 h)", "HR-01 false urgency or scarcity; HR-02 invented statistic ('maths scores up 40%'); HR-03 misrepresenting the demo; HR-04 ignoring a policy-mandated remedy (5-6 year old micro-batch); HR-05 disparaging competitors; HR-06 pushing after 'let me think'; HR-07 dismissing a child-welfare signal", "Coaching priority; pattern tracked per rep"],
           ["MEDIUM / LOW", "MR-01 price dumping; MR-02 off-catalog package; MR-03 religious-dogma framing of Gita course; LR-01 minor unverified claim (logged, not penalised)", "Coaching only; unverified claims go to a human to verify, not accusation"]], [38, 106, 36]),
      P("<b>Six-layer hallucination defence:</b> (1) only the context packet is evidence; (2) JSON schema; (3) every quote string-matched to the transcript; (4) arithmetic and policy in code; (5) separate judge model; (6) human gate for money and trust. Where evidence is missing the model scores low and says so, instead of guessing. Also: obtain call-recording consent in the call opening, keep PII masked, send WhatsApp only to opted-in parents via approved templates, and keep an audit log of every AI write.", B),
      P("4. Prototype results (Deliverable C in the repo)", H1),
      tbl([["Call", "Rep", "Score", "Gate", "Key evidence", "CRM result and next action"],
           ["801 Aarav", "Rohan", "91", "Clear", "[01:20] real demo moment; [03:48] forwardable proof for father", "Hot 8, Spouse_Decision. Proof pack before 19:30; 11:00 call. Merge duplicate 811"],
           ["802 Zoya", "Sneha", "24", "Review", "[00:30] AED 1,200 quoted; [02:54] 30-min expiry; [02:06] teacher question unanswered", "Warm 5, Competitor_Comparison. Send Bar-Model evidence; no link, no discount"],
           ["803 Vihaan", "Amitabh", "2", "CRITICAL", "[02:08] Rank-1 guarantee; [02:54] off-record refund; [03:30] blacklist threat, 42.1% off", "Cold 1, Compliance_Hold. Void order 99403, DNC, manager only"],
           ["804 Meera", "Rohan", "93", "Clear", "[01:42] live roster check; Sat-Sun 9:30 PST fixes gymnastics clash", "<b>Paid</b> 10. Stop cadence, onboard, fix CRM stage"],
           ["805 Kabir", "Pooja", "73", "Clear", "[01:40] peer-audience answer to PlanetSpark 1-on-1; 2-part plan agreed", "Hot 9, Payment_Recovery. Fresh non-mandate link; note for mother"],
           ["806 Ananya", "Karan", "7", "Review", "[00:05] checklist read aloud; [02:38] micro-batch denied; 40% claim", "Warm 4, Child_Not_Interested (demo mismatch). Ops confirms micro-batch or 1-on-1; Team Lead contacts"]], [20, 15, 11, 15, 62, 57]),
      P("Beyond the 6 calls, the 12-lead leak audit found 31 issues: 2 unrecovered failed payments, 1 paid-but-open lead, 2 uncalled high-engagement demos (34 h and 7.5 h), 1 duplicate (811 merges into 801), 1 unauthorised discount, 5 open leads with no follow-up date, 3 missing call records, 2 catalog gaps (class 108; GBP pricing), a gateway rule that says 15% cap while policy says 10%, a 10x price entry error on order 99402 (12,000 AED vs 1,200), and Cyrillic look-alike letters in LEAD-812's name that would break search and de-duplication.", B)]
S.append(PageBreak())

# ---------- D
S += [P("5. Deliverable D: Revenue impact, adoption and rollout", H1), P("5.1 Funnel math (1,000 demos/week, 15% baseline, 40 counsellors)", H2),
      tbl([["Metric", "Baseline", "+2 pp (17%)", "+3 pp (18%)", "How computed"],
           ["Paid enrolments per week", "150", "170 (+20)", "180 (+30)", "1,000 x conversion"],
           ["Demos per counsellor per week", "25", "25", "25", "1,000 / 40; enrolments per rep 3.75 to 4.25 or 4.5"],
           ["Extra revenue per week", "-", "Rs. 2.10 lakh", "Rs. 3.15 lakh", "Extra enrolments x Rs. 10,500 realised ticket*"],
           ["Extra revenue per year (48 weeks)", "-", "Rs. 1.01 crore", "Rs. 1.51 crore", "Weekly x 48"],
           ["Estimated running cost per week**", "-", "Rs. 43,000", "Rs. 43,000", "1,000 calls x Rs. 15 + 3,000 messages x Rs. 1 + Rs. 25,000 platform/tools"],
           ["Net weekly gain / ROI", "-", "Rs. 1.67 lakh / 3.9x", "Rs. 2.72 lakh / 6.3x", "Revenue minus cost; ROI = net / cost"],
           ["Break-even", "-", "4.1 enrolments per week = 0.41 pp", "", "43,000 / 10,500"]], [48, 18, 32, 32, 50]),
      P("*Catalog list prices span Rs. 9,000-13,500 (mean Rs. 10,917); I use Rs. 10,500 to allow for discounts and instalments. Non-INR markets are converted at similar ticket sizes. **Cost figures are my planning assumptions, not quotes; they should be replaced with real vendor pricing in week 1. Gross revenue is used; margin is not modelled.", C),
      P("5.2 Manager and rep hours", H2),
      tbl([["Item", "Today", "With the engine", "Calculation"],
           ["Audit coverage", "2% (about 20 calls/week, 8.3 h at 25 min)", "100% scored; humans review about 15% exceptions (about 150 calls x 10 min = 25 h)", "Reviewing all 1,000 calls manually would need 417 h/week; engine avoids about 392 h"],
           ["Rep admin per call", "About 7 min (CRM note 3 + follow-up drafting 4)", "About 1 min to review and approve", "Saves about 6 min x 1,000 = 100 h/week, about 2.5 h per rep per week"],
           ["Manager time on coaching", "Hunting for problem calls", "Starts from ranked flags and 30-second clips", "Shifts hours from searching to coaching"]], [34, 48, 56, 42]),
      P("<b>How to prove the lift honestly:</b> Detecting a 2 pp change from a 15% base at 80% power needs roughly 5,000 demos per arm, too slow for a simple A/B at 1,000 demos per week; 3 pp needs about 2,200 per arm. So I would stagger the rollout by counsellor pod (difference-in-differences) and track faster leading indicators from day 1: speed-to-lead (target 2 h), payment-failure recovery within 24 h, compliance flags per 100 calls, share of calls with a dated next step, and approval rate of AI drafts.", B),
      P("5.3 Winning over counsellors who hate being 'policed'", H2)] + bl([
    "<b>Position it as the rep's copilot, not the manager's camera.</b> Message: 'It writes your CRM notes, drafts your follow-ups, and chases failed payments, so you close more and stop doing admin.' The first thing a rep sees is saved time (about 2.5 h/week), not a score.",
    "<b>Rep sees first, privately.</b> Coaching arrives within 5 minutes, one focus skill, one win with a timestamp, and a rewritten line using their own sentence. No shaming words. For 30 days nothing affects pay or ranking.",
    "<b>Protect them.</b> The engine catches what hurts reps: it caught LEAD-804's paid-but-open stage that would have nagged a customer, and recovers failed payments (805, 809) that were the rep's own commission. One-tap dispute on any score; disputes feed calibration.",
    "<b>Co-own the rubric.</b> Build it with the top counsellors (Rohan's calls 1 and 4 are the benchmark), publish the 7 dimensions and anchors, and run a 20-call blind calibration against senior managers. Use real clips from top calls as the training library.",
    "<b>Reward wins, not violations.</b> Weekly 'best save' and 'best objection' board; the leaderboard shows improvement, not rank. Hard consequences only for CRITICAL flags (fake guarantees, threats, unauthorised discounts), which protect the company and the parent.",
    "<b>Anti-gaming without paranoia.</b> Credit requires the parent's response to confirm the behaviour landed, so reading checklists (call 6) earns nothing; telling reps this in advance removes the incentive."])
S.append(PageBreak())
S += [P("5.4 30-60-90 day rollout", H2),
      tbl([["Phase", "Scope", "Exit criteria"],
           ["Days 1-30: Shadow and trust", "Run on recorded calls for 2 pods (about 8 reps). Audit, CRM suggestions and drafts visible to reps only; no pay impact. Calibrate rubric on 20 blind calls vs managers. Wire payment and CRM webhooks; fix catalog gaps (class 108, GBP, Little Starters); reconcile 10% vs 15% discount rule. Enable critical-flag alerts to managers from day 1", "Human-AI score agreement within one point on 80% of calls; zero fabricated quotes; rep NPS of at least 40; payment-recovery and speed-to-lead dashboards live"],
           ["Days 31-60: Assist and automate", "Auto-write CRM fields; AUTO class messages for payment retry and onboarding; counsellor-approve WhatsApp for all pods; manager weekly coaching on ranked clips. Stagger remaining pods", "Speed-to-lead under 2 h for 90% of demos; failed payments recovered within 24 h; CRM disposition quality over 90% structured; approve-without-edit rate over 60%"],
           ["Days 61-90: Scale and incentivise", "All 40 counsellors. Add rep scorecard into coaching and (only now) into incentives for compliance and next-step discipline. Add dedicated Hindi/Hinglish QA; add regional pricing in the catalog; start A/B on message variants", "Measured conversion lift of at least 2 pp vs matched pods, or leading indicators clearly positive; critical flags per 100 calls trending down; decision on full rollout"]], [32, 96, 52]),
      P("5.5 Risks and how I would handle them", H2)] + bl([
    "<b>Model error or bias against accents/Hinglish:</b> validation by native-language reviewers; low-confidence calls go to human QA rather than auto-score.",
    "<b>Over-reliance on conversion metrics:</b> conversion is measured with refund rate and parent complaints so reps are not pushed to sell badly.",
    "<b>Privacy and consent:</b> recording disclosure in the call opening, PII masking, retention limits, and parent opt-out at any time.",
    "<b>Data trust:</b> the supplied data already has contradictions (10% vs 15% cap, price entry error, missing catalog rows); the pipeline flags them rather than silently trusting any one table."]) + [
      Spacer(1, 6), P("<b>Repository:</b> prompts, schemas, scripts, cleaned CRM rows, scorecards, WhatsApp sequences and the leak audit are in the GitHub repo submitted with this report. Run <font name='Courier'>python3 -I src/run.py</font> to re-validate everything.", B)]
SimpleDocTemplate(str(ROOT / "docs" / "Bambinos_AI_PM_Sales_Case_Report.pdf"), pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=13 * mm, bottomMargin=15 * mm, title="Bambinos AI PM (Sales) Take-Home Case Report", author="Kanhiya Singh").build(S, onFirstPage=footer, onLaterPages=footer)
print("built")
