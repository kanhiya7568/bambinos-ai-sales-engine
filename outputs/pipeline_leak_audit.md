# CRM pipeline leak audit (12 leads)

Snapshot: 2026-11-03 20:00 UTC. All CRM timestamps normalised from lead-local time to UTC.

| Lead | Owner | Type | Sev | Detail |
|---|---|---|---|---|
| LEAD-803 | Amitabh R*** | DISCOUNT_ANOMALY | P0 | order 99403: discount 4000 INR = 42.1% of catalog fee vs cap 10% (limit 950 INR) |
| LEAD-803 | Amitabh R*** | UNAUTHORIZED_LINK | P0 | order 99403: payment plan type is 'Unauthorized_Custom_Link' |
| LEAD-804 | Rohan S*** | PAID_BUT_CRM_OPEN | P0 | order 99404 paid 2026-11-03 11:40:12; CRM stage still 'Payment_Link_Sent', next follow-up 2026-11-03 20:00:00 would nag a paying parent |
| LEAD-805 | Pooja M*** | PAYMENT_FAILED_UNRECOVERED | P0 | order 99405 Bank_OTP_Timeout_On_UPI_Mandate; no recovery logged 5 h later |
| LEAD-809 | Rohan S*** | PAYMENT_FAILED_UNRECOVERED | P0 | order 99409 3DS_Authentication_Declined_By_Issuer; no recovery logged 6 h later |
| LEAD-801 | Rohan S*** | LINK_OPENED_NOT_PAID | P1 | order 99401: link opened twice, unpaid; strong buying signal |
| LEAD-801 | Rohan S*** | FOLLOWUP_OVERDUE | P1 | follow-up due 2026-11-03 11:00:00 IST; no activity logged since |
| LEAD-802 | Sneha V*** | NO_FOLLOWUP_SCHEDULED | P1 | open stage 'Follow_Up_Cold' with next_followup_at NULL |
| LEAD-803 | Amitabh R*** | FOLLOWUP_OVERDUE | P1 | follow-up due 2026-11-03 18:00:00 IST; no activity logged since |
| LEAD-806 | Karan K*** | NO_FOLLOWUP_SCHEDULED | P1 | open stage 'Follow_Up_Cold' with next_followup_at NULL |
| LEAD-807 | Sneha V*** | UNCALLED_DEMO | P1 | demo ended 2026-11-02 15:30:00 IST; engagement 5/5; no call after 34 h (SLA 2 h) |
| LEAD-807 | Sneha V*** | NO_FOLLOWUP_SCHEDULED | P1 | open stage 'Demo_Completed_Uncalled' with next_followup_at NULL |
| LEAD-808 | Amitabh R*** | NO_FOLLOWUP_SCHEDULED | P1 | open stage 'Follow_Up_Warm' with next_followup_at NULL |
| LEAD-808 | Amitabh R*** | CATALOG_GAP | P1 | class_id 108 ('Young Communicators GCC Track') is not in the reference pricing/policy table |
| LEAD-809 | Rohan S*** | FOLLOWUP_OVERDUE | P1 | follow-up due 2026-11-03 19:00:00 GMT; no activity logged since |
| LEAD-812 | Sneha V*** | UNCALLED_DEMO | P1 | demo ended 2026-11-03 06:30:00 CST; engagement 5/5; no call after 8 h (SLA 2 h) |
| LEAD-812 | Sneha V*** | NO_FOLLOWUP_SCHEDULED | P1 | open stage 'Demo_Completed_Uncalled' with next_followup_at NULL |
| LEAD-801 | Rohan S*** | LAZY_DISPOSITION | P2 | disposition 'Call back tomorrow' / note 'will ask husband and tell tomorrow' carries no usable intent or next step |
| LEAD-802 | Sneha V*** | PRICE_MISMATCH_VS_CATALOG | P2 | order 99402: order standard_amount 12000 AED vs catalog 1200 AED (10x) |
| LEAD-802 | Sneha V*** | LAZY_DISPOSITION | P2 | disposition 'Price issue' / note 'price high thinking' carries no usable intent or next step |
| LEAD-803 | Amitabh R*** | POLICY_RULE_MISMATCH | P2 | order 99403: gateway rule says 15% cap, catalog policy says 10% |
| LEAD-803 | Amitabh R*** | LAZY_DISPOSITION | P2 | disposition 'Interested' / note 'good call sent payment link will pay today' carries no usable intent or next step |
| LEAD-805 | Pooja M*** | LAZY_DISPOSITION | P2 | disposition 'Thinking' / note 'comparing with planetspark and school exam going on' carries no usable intent or next step |
| LEAD-808 | Amitabh R*** | LAZY_DISPOSITION | P2 | disposition 'Busy' / note 'ok' carries no usable intent or next step |
| LEAD-808 | Amitabh R*** | CALL_RECORD_MISSING | P2 | CRM shows a call at 2026-11-02 20:10:00 but no recording/transcript is in the call log |
| LEAD-809 | Rohan S*** | CATALOG_GAP | P2 | order 99409: No GBP fee for class 205 in the catalog; amount 210 GBP cannot be verified |
| LEAD-809 | Rohan S*** | CALL_RECORD_MISSING | P2 | CRM shows a call at 2026-11-03 14:00:00 but no recording/transcript is in the call log |
| LEAD-810 | Karan K*** | FOLLOWUP_BEFORE_LAST_CALL | P2 | next_followup_at 2026-11-01 10:00:00 is earlier than last_call_at 2026-11-02 12:30:00: stale/invalid |
| LEAD-810 | Karan K*** | LAZY_DISPOSITION | P2 | disposition 'Call back' / note 'cb' carries no usable intent or next step |
| LEAD-810 | Karan K*** | CALL_RECORD_MISSING | P2 | CRM shows a call at 2026-11-02 12:30:00 but no recording/transcript is in the call log |
| LEAD-811 | Pooja M*** | DUPLICATE_LEAD | P2 | duplicates LEAD-801 (same user_id/student_id/mobile); owners Rohan S*** vs Pooja M*** |
| LEAD-812 | Sneha V*** | DATA_QUALITY_NON_ASCII | P2 | look-alike letters in name 'Ri***i Ме***a': CYRILLIC CAPITAL LETTER EM, CYRILLIC SMALL LETTER IE |

**Speed-to-lead (demo end to call, minutes):** LEAD-801 45, LEAD-802 45, LEAD-803 45, LEAD-804 45, LEAD-805 45, LEAD-806 40, LEAD-808 70, LEAD-809 60, LEAD-810 60

**Uncalled demos (hours since demo, SLA 2 h):** LEAD-807 34.0 h, LEAD-812 7.5 h