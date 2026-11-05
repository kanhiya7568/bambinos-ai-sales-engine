# WhatsApp follow-up sequences (generated)


## LEAD-801 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _Before 19:30 IST on call day (father is home at 20:30)_ (53 words)
> Hi Divya ma'am, here's the 60-second note for tonight. Ms. Rhea saw Aarav go from a nervous start to a confident 45-second space-rescue story after learning the 3-step 'Superhero Hook' (Beginning, Problem, Rescue). The program trains speaking confidence, not grammar. Max 6 kids per batch. Roadmap attached. Anything else your husband might ask?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.learning_gaps_observed, transcript [01:55] batch max 6, crm_record.objection_evidence  
_Pre-send checks:_ Attach Stage Showcase roadmap PDF

**T2** · COUNSELLOR_APPROVE · UTILITY · _10:15 IST next day, 45 min before the agreed 11:00 call_ (31 words)
> Good morning ma'am! Quick check before our 11 AM call: did Aarav's dad have any questions after seeing Ms. Rhea's note? I can answer them on the call or right here.

_Grounding:_ transcript [04:15] call booked 11 AM, transcript [03:32] father's question

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after call if no payment and no reply_ (44 words)
> Hi Divya ma'am, no rush at all. If Aarav's dad would like to hear it directly, I can do a 5-minute call with both of you at a time that suits. Or tell me if you'd prefer I pause my messages. Which is easier?

_Grounding:_ crm_record.primary_objection=Spouse_Decision

_Never send:_ Payment link in T1 (link already sent by rep; opened twice); Any 'seat will go' language unless the roster API confirms the seat; Discount (none approved)


## LEAD-802 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _Within 30 min of call end (call ended 19:31 GST, send ~20:00)_ (52 words)
> Hi Amina ma'am, as promised, here's the curriculum outline. You asked what Mr. Vikram noticed about Zoya's word problems: she solved two fraction word puzzles on her own with our Bar-Model method (drawing the story as bars) and said 'that was so easy!' A 1-page note on how it works is attached.

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.learning_gaps_observed, transcript [02:06] parent's unanswered question  
_Pre-send checks:_ Attach curriculum PDF and 1-page Bar-Model note (assets must exist)

**T2** · COUNSELLOR_APPROVE · MARKETING · _36 h after T1 (Wed 10:00 GST)_ (54 words)
> Hi Amina ma'am, thinking about your comparison with the local tutor: worksheets give practice, while the Bar-Model teaches Zoya to turn a 4-line story into a picture so she stops guessing + or x. Would it help if I asked Mr. Vikram to write 3 lines on how he would tackle her word-problem gap?

_Grounding:_ demo_eval.learning_gaps_observed, transcript [00:50] local tuition AED 350

**T3** · COUNSELLOR_APPROVE · MARKETING · _4 days after call (Sat 11:00 GST)_ (46 words)
> Hi Amina ma'am, no pressure from our side. If Zoya stays with her local tutor for now, that's completely fine. If word problems are still the hurdle after her exams, Mr. Vikram's note is yours anyway. Shall I check in after her exams, or pause messages?

_Grounding:_ transcript [03:08] 'I'll discuss with her local tutor'

_Never send:_ Payment link or 'link expires' wording (she said 'please don't rush me'); The AED 100 discount as a pay-now lever; The 96-class AED 2,100 package (not in catalog); Any criticism of local tuition


## LEAD-803 - mode **STOP** (English)

**STOP ALERT (COMPLIANCE)** -> notify: Head of Sales, Team Lead (Mumbai), Compliance
- Void order 99403 (Rs. 5,500 custom link) so no payment is taken under false terms
- Set phone DNC on the parent (explicit 'Do not call me again')
- Block all automated cadences for this lead
- Pause new outbound from the rep until the manager review is done
- Manager decides whether to send ONE written correction (draft below); no sales content
- Search WhatsApp chat for the rep's 'written' guarantee and preserve it for review
- Review the rep's other leads (LEAD-808) and recent calls

**Manager-only draft (MANAGER_ONLY)** - Only if the Head of Sales approves. Written, one time, no sales content, signed by a manager.
> Dear Mr. Desai, I'm [name], Head of Sales at Bambinos.live. I'm sorry about your call. The guarantee, the Rs. 5,500 price and the refund terms you were given are not our policy, and the payment link has been cancelled. Our actual policy is a 14-day refund (up to 4 classes). We won't contact you again unless you ask. Ms. Simran's feedback on Vihaan is available if you want it.

_Never send:_ Any selling message; Any phone call; The rep's payment link; Any message citing Vihaan's performance unless the manager approves the draft


## LEAD-804 - mode **STOP** (English)

**STOP ALERT (PAID)** -> notify: Rohan S***, Student Success
- Move CRM stage Payment_Link_Sent -> Enrolled_Paid (order 99404, USD 265, paid 11:40:12 PST)
- Cancel the sales follow-up scheduled 2026-11-03 20:00
- Create onboarding task: confirm first-class date, teacher welcome, parent guide
- Schedule a referral ask for day 14 (separate, non-sales message)

**T1** · AUTO · UTILITY · _Within 5 min of payment webhook_ (40 words)
> Welcome to Bambinos, Neha! Meera's seat is confirmed: Little Yogi with Acharya Aditi, Saturdays and Sundays at 9:30 AM PST. Her first class is on {{first_class_date}} and the class link will arrive before then. We can't wait to welcome her!

_Grounding:_ order_row.payment_link_status=Paid, transcript [02:00] batch

_Never send:_ Any payment or discount reminder; Referral ask before day 14; Upsell in the first week


## LEAD-805 - mode **SEQUENCE** (Hinglish (Roman script))

**T1** · AUTO · UTILITY · _30 min after payment failure (20:45 -> 21:15 IST); payment-recovery utility messages allowed until 22:00_ (40 words)
> Namaste Rajesh sir! Aapka Rs. 5,400 ka payment bank OTP timeout ki wajah se complete nahi ho paya. Naya link: {{fresh_payment_link}} Ek baar ka normal UPI/card payment, mandate nahi. Koi dikkat aaye toh bas reply kar dijiye, main help karungi.

_Grounding:_ order_row.payment_link_status=Payment_Failed, order_row.gateway_error_reason, order_row.net_payable_amount=5400

**T2** · COUNSELLOR_APPROVE · MARKETING · _Next day 10:30 IST_ (48 words)
> Namaste sir! Kabir ne PEEL method se 'Should homework be banned' topic par poore 60 seconds bina ek bhi 'umm' ke bola tha. Mummy ko dikhane ke liye 1-minute ka note attach hai. Exam week mein class pause/reschedule ho sakti hai. Mummy ka koi sawal ho toh bataiye?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, transcript [01:14] 'mummy bol rahi hain', transcript [02:20] exam pause claim  
_Pre-send checks:_ VERIFY the 'Exam Pause / Reschedule' feature exists before sending; Attach 1-minute note

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (46 words)
> Namaste sir, agar exams ke baad start karna better lage toh koi baat nahi. Exams khatam hone par aap jab bolen, main ek chhota call fix kar dungi. Tab tak messages pause kar doon? Kabir ka PEEL wala 60-second speech dobara dekhna ho toh bata dijiye.

_Grounding:_ transcript [01:14] exams from the 15th, demo_eval.demo_magic_moment_for_parent

_Never send:_ Auto-debit mandate link (it just failed); Extra discount (10% already used); PlanetSpark criticism; 'Seats are filling' (not verified)


## LEAD-806 - mode **SEQUENCE** (English)

**T1** · MANAGER_ONLY · MARKETING · _After Academic Ops confirms the micro-batch or 1-on-1 bridge; within 24 h of the call; Team Lead sends_ (48 words)
> Hi Swathi ma'am, I'm [Team Lead] from Bambinos. You were right about Ananya: she loved the Knight and Dragon puzzle with Coach Arvind, and a mixed-age room wasn't ideal for a 6-year-old. We can offer a complimentary 1-on-1 bridge session or an age 5-6 micro-batch. Which feels better?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.recommended_batch_type, policy_row[401].forbidden_compliance_red_flags, transcript [01:32]  
_Pre-send checks:_ Academic Ops confirms micro-batch (max 3) or 1-on-1 bridge is available; Reassign owner from Karan

**T2** · COUNSELLOR_APPROVE · MARKETING · _36 h after T1_ (37 words)
> Hi Swathi ma'am, the 1-on-1 bridge is a calm session just for Ananya with a coach, starting from the Knight puzzle she enjoyed. No other kids. Would a weekday evening or a weekend morning suit her better?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.recommended_batch_type  
_Pre-send checks:_ Bridge-session format confirmed by Ops

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (31 words)
> Hi Swathi ma'am, no pressure at all. When Ananya is ready, the offer of a calm 1-on-1 starter session stands. Shall I check in next week, or pause messages for now?

_Grounding:_ transcript [02:46] mother's condition

_Never send:_ Any payment link; Any urgency or deadline; The 10% discount; Message from Karan (trust damaged); Chess benefit statistics


## LEAD-807 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _Immediately (already overdue); next 09:00 local if outside the window_ (38 words)
> Hi {{parent_first_name}}, this is {{rep_first_name}} from Bambinos. {{student_first_name}} scored 5/5 on Ms. Rhea's live Olympiad inference challenge and asked when the regular batch starts. Great sign! Can I call you today at {{slot_1}} or {{slot_2}} with batch timings?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.child_engagement_score_1_to_5

**T2** · COUNSELLOR_APPROVE · MARKETING · _24 h after T1 if no reply_ (43 words)
> Hi {{parent_first_name}}, Ms. Rhea noted that {{student_first_name}} reads widely and has a strong vocabulary. The area to build is structuring persuasive essays and inference answers, which is what the Olympiad & Creative Writing track focuses on. Shall I send the batch timings here?

_Grounding:_ demo_eval.skill_strengths_observed, demo_eval.learning_gaps_observed

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (34 words)
> Hi {{parent_first_name}}, no rush. If the timing isn't right this month, I'm happy to wait. If it helps, I can send two or three batch options to look at at your pace. Shall I?

_Grounding:_ crm_record.lead_stage

_Never send:_ Any Olympiad medal or selection promise (policy); Discount before the parent asks; Urgency


## LEAD-808 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _After the rep's 11/02 call recording is reviewed; reassign owner_ (43 words)
> Hi {{parent_first_name}}, {{student_first_name}} loved the 'Mystery Box' game in Ms. Simran's class and asked for two extra rounds! Ms. Simran also noted a confident voice and clear pronunciation. When would be a good 10 minutes this week to talk about the right batch?

_Grounding:_ demo_eval.demo_magic_moment_for_parent, demo_eval.skill_strengths_observed  
_Pre-send checks:_ Do not quote a price: class 108 is missing from the catalog

**T2** · COUNSELLOR_APPROVE · MARKETING · _36 h after T1_ (43 words)
> Hi {{parent_first_name}}, Ms. Simran suggests the next step is impromptu storytelling and vocabulary, like the Mystery Box game, but every week. In a small group of up to 6, every child gets plenty of turns. Shall I share batch timings that suit Doha?

_Grounding:_ demo_eval.learning_gaps_observed, demo_eval.recommended_batch_type

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (30 words)
> Hi {{parent_first_name}}, no pressure. If now isn't the right time, tell me when to check back and I'll leave it until then. Or I can pause messages. Whatever is easiest.

_Grounding:_ 

_Never send:_ Price (catalog gap); Anything referencing the earlier 'Busy / ok' call


## LEAD-809 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · UTILITY · _30 min after the failure (14:15 -> 14:45 GMT)_ (46 words)
> Hi {{parent_first_name}}, your payment of GBP 210 for {{student_first_name}}'s Maths place didn't go through because the card's extra security check wasn't completed. Fresh link: {{fresh_payment_link}} If your bank app asks you to approve, please tap approve, or try another card. Reply if you'd like a hand.

_Grounding:_ order_row.payment_link_status=Payment_Failed, order_row.gateway_error_reason, order_row.net_payable_amount=210  
_Pre-send checks:_ Confirm GBP 210 price (GBP missing from catalog) before approving

**T2** · COUNSELLOR_APPROVE · MARKETING · _24 h after T1 if unpaid_ (42 words)
> Hi {{parent_first_name}}, {{student_first_name}} solved the 4-disc Tower of Hanoi challenge on the first attempt in Mr. Vikram's class. A great sign for the Brainiac track. If the card still gives trouble, I can send a link for another payment method. Shall I?

_Grounding:_ demo_eval.demo_magic_moment_for_parent

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (32 words)
> Hi {{parent_first_name}}, no rush. If it's easier to talk it through, I can call at a time that suits you. Or I'll pause my messages if you'd rather. Which would you prefer?

_Grounding:_ 

_Never send:_ A repeat of the same failing link; Discount; Urgency


## LEAD-810 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _Immediately (follow-up date 11/01 is stale)_ (49 words)
> Hi {{parent_first_name}}, {{student_first_name}} learned the 'thumbs-up b and d' trick in just 5 minutes in Ms. Simran's class and then read 4 sentences aloud. Lovely progress! You'd asked for a call back. What would you like to think over? I can answer here or on a quick 5-minute call.

_Grounding:_ demo_eval.demo_magic_moment_for_parent, crm_row.manual_rep_disposition=Call back

**T2** · COUNSELLOR_APPROVE · MARKETING · _36 h after T1_ (36 words)
> Hi {{parent_first_name}}, Ms. Simran noted two things to build next: b/d reversals and long vowel sounds. That is what the Phonics & Early Reading Champions small group (max 6) practises. Would you like the batch timings?

_Grounding:_ demo_eval.learning_gaps_observed, demo_eval.recommended_batch_type

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (24 words)
> Hi {{parent_first_name}}, no pressure at all. If the timing isn't right, tell me when to check back. I can also pause messages until then.

_Grounding:_ 

_Never send:_ Reference to the vague 'cb' note; Discount; Urgency


## LEAD-811 - mode **STOP** (English)

**STOP ALERT (MERGE)** -> notify: Sales Ops, Rohan S***, Pooja M***
- Merge LEAD-811 into LEAD-801 (same user_id 51001, student_id 78001, mobile)
- Remove Pooja M***'s assignment; Rohan S*** remains the single owner
- Log 'website brochure download 2026-11-03 08:10' as an intent signal on LEAD-801
- No new outreach from this record

_Never send:_ Any message from a second counsellor to this family


## LEAD-812 - mode **SEQUENCE** (English)

**T1** · COUNSELLOR_APPROVE · MARKETING · _Immediately (already overdue); next 09:00 Texas time if outside the window_ (52 words)
> Hi {{parent_first_name}}, this is {{rep_first_name}} from Bambinos. {{student_first_name}} asked a thoughtful question in Acharya Aditi's class: how Karma Yoga applies to school grades and sport. It was lovely to see you cheering her on! Could we talk for 10 minutes this week about weekend batch options, at a time that suits you?

_Grounding:_ demo_eval.demo_magic_moment_for_parent

**T2** · COUNSELLOR_APPROVE · MARKETING · _24-36 h after T1_ (37 words)
> Hi {{parent_first_name}}, our US weekend small group fits around school and swim. Acharya Aditi keeps it practical: tools for staying steady under pressure, using real examples from school and sport. Want me to send the weekend timings?

_Grounding:_ demo_eval.recommended_batch_type=US_Weekend_Small_Group, demo_eval.learning_gaps_observed

**T3** · COUNSELLOR_APPROVE · MARKETING · _72 h after T1_ (29 words)
> Hi {{parent_first_name}}, no rush at all. If the timing isn't right, tell me when to check back, or I can pause messages. Happy to answer any questions before then.

_Grounding:_ 

_Never send:_ Any statement about the child's anxiety or health; Price before she asks; Urgency
