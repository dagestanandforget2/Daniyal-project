# Trial Reels plan (task uf13ef27e26a6a8293c28d513ae72421b) — Nov 9 2026

## STANDING INSTRUCTION (the owner, Nov 11 1:05 PM ET), read first
Follow the plan doc's format v2 and the four rules at its top: one book per reel, product facts only, no study advice, real book on screen in the first second. Where older notes below mention hooks, bodies, CTAs, scores or a 1-in-5 experiment, use the doc's six openings (O1-O6) and two-day blocks instead. Full working summary in reels/README.md. Doc checked at rev 31: format v2, the rules, six openings, block schedule all present.
Next build (Thu Nov 12) = block 1 day 1: O1 Number fact (champion) vs O2 Title, 5 books, 9 AM champ / 12 chall / 3 champ / 6 chall / 9 champ. Each book must work for both O1 (verified count) and O2 (Arabic title). Needs a proper Arabic font for O2 (raqm works in PIL; only DejaVu/FreeSerif installed).
Today's already-scheduled batch 3 has old-format reels that break the rules: 1111-02 (religious question + content list), 1111-04 (six books), 1111-05 ("for the student of knowledge" line). Asked him whether to pull them from the schedule.


Doc: Claude Doc "Dar Al Athari Trial Reels Plan", https://claude.ai/artifact/2RFhCZ5VRoD5DXF1F4bbKW (doc id 0b7c0b48-b408-4866-834a-dd5a1eb72b39, body node 13a52c7d-fb79). Last rev 16.

Decided (the owner, via coordinator Nov 9 16:25 UTC): Trial Reels run on his MAIN Instagram account. Plan: start 3/day, +2/week, drop back 2 on any block. New account + TikTok carry high volume as normal reels (test lab). Promote main-account winners via Share to everyone; new-account winners are re-made, not re-uploaded.

Facts checked (sources in doc):
- Metricool can schedule TRIAL_REEL (help page updated Nov 9 2026; its scheduling tool also has type TRIAL_REEL). Option always shown; fails at publish if ineligible.
- Eligibility: public professional, 200+ followers per Metricool help (blog says 1,000; conflict). Daily cap unpublished, stricter than reels; exceeding blocks 24h+.
- Auto-share: 72h window (Instagram Dec 2024 post); set in Metricool planner, can't change after. Scheduling tool shows no auto-share field — untested.
- Metricool brand dar.al.athari_ (blogId 7251923) has only TikTok connected as of Nov 9.
- Metricool IG reels metrics: reelsViewRate (3s hold), retention, averageWatchTime, views, reach, shares, saved, comments, likes, reposts. No per-reel follows or link clicks. Blog says trial-reel stats need Advanced plan.
- Duplicate-content warning only from FlowGent (secondhand).

Open (in doc): who schedules; where rendering runs; keep new account; follower count/account type; Metricool plan; sheet location; follows by hand; caption language.
Nothing posted, scheduled or changed in any account.
Next: refine with his answers; then build score sheet + batch 1.

## Nov 9 ~16:45 UTC — batch 1
- the owner said start and "go ahead with everything you need to decide on your own" (decisions recorded in doc section "Decisions made (Nov 9)"). Posting still needs his yes per batch.
- Rendered 3 reels here (Python PIL + ffmpeg, script /mnt/project-files/reels/render_batch1.py, photos from Book Library artifact). Silent audio track. Files in /mnt/project-files/reels/batch-2026-11-10/. Batch sheet /mnt/project-files/reels/batch-sheet.csv; empty score sheet score-sheet.csv.
  - 1110-01 H08 B06 C02 T5 tp+ft+k_tw (stock 27/12/17), 13.5s. Order on screen: Three Principles, Five Treatises, Kitab at-Tawhid — order is my pick, asked him to check.
  - 1110-02 H05 B01 C01 T1 mt (Black 30 in stock), 12.4s. Lines: core texts in one volume; compiled by Dr. Abdul Muhsin al-Qasim, Imam of al-Masjid an-Nabawi; verified against 160 manuscripts (cover says so).
  - 1110-03 H15 B08 C04 T3 zad (3 in stock), 11.2s.
- Proposed slots Tue Nov 10, 11 AM / 4 PM / 9 PM ET, Trial Reel, auto-share off. Needs: Instagram main connected to Metricool by ~10 AM Tue; his yes; then upload to Shopify Files for public URL and schedule.

## Nov 9 ~19:47 UTC
- the owner connected Instagram (daralathari) + Facebook page to Metricool brand 7251923.
- Metricool: 4,740 followers (Nov 8). Main already posts 2-5 normal reels/day; Nov 1-9 reel views per reel roughly 350-1,500, ~1,000 typical; avg reach per reel 832 (Nov 9). Eligible on followers; connected via Facebook so it's a professional account.
- Still no yes to schedule batch 1. On yes: upload 3 mp4s to Shopify Files (upload_file), then createScheduledPost type TRIAL_REEL, Tue Nov 10 11:00/16:00/21:00 America/New_York, captions in batch notes below.
- Captions saved: /mnt/project-files/reels/batch-2026-11-10/captions.md (shown to the owner Nov 9 ~19:48 UTC)

## Nov 9, 2:53 PM ET: batch 1 posting (his yes: "post them all now as trials")
- Hosting: Shopify Video upload transcodes to 606x1080, so used plain-file upload (stagedUploadsCreate resource FILE, then fileCreate contentType FILE) to keep 1080x1920 originals. Files: dar-trial-1110-01/02/03.mp4 in Shopify Files. (3 Video copies also exist in Files from the first try; harmless.)
- staged upload fileSize must be exact bytes (stat -c %s).
- Metricool posts 422325150 (2:58), 422325439 (3:05), 422325485 (3:12) PM ET Nov 9; Metricool echoes shareTrialAutomatically=false (auto-share off).
- Next: confirm published status after 3:12; metrics ~24h later (Tue ~3 PM).

## Nov 9, 2:57 PM ET: he asked for 5 Trial Reels a day
- Plan doc updated (rev 22): week 1 = 5/day at 9 AM, 12 PM, 3 PM, 6 PM, 9 PM ET from Tue Nov 10; week 2 = 7; week 3 = 9; then 10 ceiling. Week 1 total 33 Trial Reels.
- Future batches = 5 reels. Each batch still needs his yes before posting (no daily routine agreed yet).
- 3:00 PM: he wants each day's batch posted all at once after his yes, ~7 min apart (doc rev 23). At 7+/day, if any block, spread 9 AM-9 PM again before cutting count.
- 2:59 PM: 1110-01 status PUBLISHING; 02 and 03 PENDING.
- 3:01 PM: main chat set a daily routine (7:13 AM ET) that scores, renders the day's batch "awaiting yes" and posts it to main chat; it never posts. On his yes (relayed here) I post that batch ~7 min apart, auto-share off. Wrote reels/README.md with the full procedure for it.
- Book photos copied to reels/books/ (6 titles). More titles need Shopify product images or his photos.
- 3:04 PM: he changed his mind: spread each batch through the day (9/12/3/6/9 ET at 5/day); late yes = spread remaining over rest of day. Doc rev 24, README updated.
- 3:16 PM: all 3 PUBLISHED per Metricool (DfiJAaSDddu, DfiJo6qklkx, DfiKY1BCFFS). First 24h read Tue Nov 10 ~3:15 PM ET.

## Tue Nov 10, 7:20 AM ET: "Make today's batch now" (daily routine failed: couldn't reach the reels folder)
- Early read (16 h, Metricool 7:20 AM): 01 creed path 123 views, 23.6% 3s view rate, 4 saves; 02 Mutoon 266 views, 24.6%, 5 saves; 03 Zad 337 views, 29.3%, 1 share, 1 save. Skip ~75% on all, avg watch 3-4 s. Retention metric null, so p_retention uses avg watch / length. Rows in score-sheet.csv are this 16 h read (views_24h column); overwrite with the true 24 h read after 3:15 PM.
- Today's batch: 1110-04..08 in batch-2026-11-10/ (same folder as batch 1). Renderer render_1110b.py + shared reelkit.py. Changes: book on screen from frame 1, hook text instant, 8-10 s.
- No Arabic font installed, so on-screen text is English only (no ﷺ glyph); Arabic stays in captions.
- New hook H21 (List): "5 core treatises of creed, explained in one book" (ft). Add to doc.

## Nov 10, 7:30 AM ET: batch 2 rendered, awaiting his yes
- 5 reels in reels/batch-2026-11-10/ (1110-04..08), rows in batch-sheet.csv with status "awaiting yes" at 09/12/15/18/21 ET.
- Checked contact sheets; fixed a text overlap in 1110-04 (questions now fade out 4.55-4.85 s, title in at 4.95 s). Others clean.
- Captions in captions.md under "Batch 2". H21 added to the doc hook table (rev 25).
- On his yes: staged FILE upload each mp4 (exact stat sizes) -> fileCreate -> READY -> Metricool TRIAL_REEL, autoPublish, isAiGenerated false, at remaining slots (spread if a slot passed; end by 21:00 ET). Then set sheet rows to scheduled + metricool ids.
- Still to do: 24h score read of 1110-01..03 (after ~3:15 PM ET Nov 10; can be done at the next batch build).
- Routine failure: its run had no /mnt/project-files. Told the coordinator: either have the 7:13 routine only nudge this task's thread to build the batch, or run it where the project's shared files are mounted.
- 7:29 AM ET: his yes ("yes when u say publicly u still mean as a trial reel correct?", relayed). Uploaded from scratchpad originals (shared copies had grown ~5.9 KB after being attached; md5 differed). Scheduled in Metricool as TRIAL_REEL, shareTrialAutomatically false: 423090317 (9 AM), 423090340 (12), 423090367 (3 PM), 423090400 (6 PM), 423090426 (9 PM). Next: confirm each published, then score.

## Nov 10, 8:55 AM ET refresh: feed vs simple vs Trial comparison (Metricool reels, Oct 27 to Nov 10)
- Asked by a morning brief note (not him); his question was in the main chat last night: stop the daily scheduled feed videos and do more Trial Reels?
- "Formula" feed reels = caption ends "Shop at daralathari.com / Link in bio / Shipped from New Jersey", 2 a day (~1 PM and ~9-10 PM ET), made by another automation, not queued in Metricool ahead.
- Formula: Oct 27-Nov 2 median 1,215 views (n=15); Nov 3-7 median 630 (n=10); Nov 8-10 median 407 (n=5, younger posts). Hold 25%, watch 4.3 s.
- Simple hand-made (short captions): n=9, median 1,081, mean 1,805, hold 32%, watch 5.0 s. Hits: Nov 3 no-caption reel 4,558; Mutoon Nov 1 3,696; I'anatul Nov 7 2,521; Mutoon Nov 7 1,872.
- Trial Reels batch 1 at 16 h: 123-337 views, 14 saves per 1k views (highest), similar to formula reels of the same age.
- Recommendation sent: stop the twice-daily formula reels, keep 5 Trial Reels a day, feed = his own simple single-book clips plus Trial winners shared to the feed. Stopping the formula automation is a main-chat routine change, waits on his yes.

## Nov 11, 7:30 AM ET refresh: batch 3 built (routine couldn't reach the folder again, 2nd failure)
- He hasn't answered the feed-reels question (stop the twice-daily formula reels?). Still open on the card until today's batch question replaced it; mention again.
- All 5 of Nov 10 published as Trial Reels (Metricool rows with captions match). Sheet rows 1110-04..08 marked published with URLs.
- Score sheet rewritten (read 7:20 AM ET Nov 11, ages 10-40 h). Top: 1110-05 Tawhid question hook 1,270 views, 14 shares, 13 saves (score 83); 1110-07 shelf POV 35% hold (81); 1110-03 Zad lit-up set 912 views, 35% hold (80). Bottom: 1110-08 "5 treatises" numbers hook 14% hold (0); 1110-06 Zad stack with big counter 122 views (28).
- Batch 3 (render_1111.py, files in batch-2026-11-11/, captions.md there, sheet rows awaiting yes): 01 H02 k_tw C03 (winner hook, CTA swap) 9 AM; 02 H22 tp question hook "Can you name the three fundamental principles?" C02 12 PM; 03 H15 Zad lit-up set shortened to 8.6 s, C01 3 PM; 04 H18 shelf C02 6 PM; 05 H23 fresh mt "Every core text..." C01 9 PM.
- Post the same way as Nov 10, from scratchpad render/out3 originals (shared copies may change after attaching).
- Nov 11 10:53 AM ET: his yes ("yes" to the brief's line, relayed). 9 AM had passed, so spread: 11:15, 1:45, 4:15, 6:45, 9 PM ET. Metricool TRIAL_REEL, auto-share off: 424604639, 424604689, 424604731, 424604772, 424604812. Uploaded from scratchpad out3 originals.
- Nov 11 11:32 AM ET: the owner chose to keep the twice-daily automated feed reels for now. Don't ask again unless their views keep falling.

## Nov 12 (refresh from routine; routine run again couldn't reach the reels folder)
- Nov 11 batch 3: all 5 published as Trial Reels (Metricool, auto-share off). 7:30 AM read: 1111-01 Tawhid question 677 views, 33.8% hold, 47 shares; others 152-430 views, 26-31% hold. Old format, so not in the opening standings. Rows in score-sheet.csv. the owner never answered the "pull 3 reels" question; they posted.
- Block 1 day 1 built (format v2), renderer reels/render_v2.py (O1, O2 built; O3-O6 still to write). Arabic font Amiri installed via apt and copied to reels/fonts/. cdn.shopify.com downloads are refused by the proxy here, so only the 6 photographed books (reels/books) are usable.
- Books chosen (each has a verified count for O1 and an Arabic title on cover/product page for O2): zad (7 volumes), mt (15 texts, 712 pages; mt photo = Al-Mutoon al-Jami'ah black, cover reads متون طالب العلم), ft (5 treatises), tp (260 pages), k_tw (192 pages). sth left out: no verified count.
- Day 1 (Thu): 9 zad O1, 12 mt O2, 3 ft O1, 6 tp O2, 9 k_tw O1. Day 2 (next approved day): 9 zad O2, 12 mt O1, 3 ft O2, 6 tp O1, 9 k_tw O2. Render: python3 -I render_v2.py books <out> 1113-01:O2:zad 1113-02:O1:mt 1113-03:O2:ft 1113-04:O1:tp 1113-05:O2:k_tw
- Files: scratchpad out5 originals (upload these), shared copies in reels/batch-2026-11-12/, captions.md there, sheet rows "awaiting yes". k_tw has no spine photo, so its body is a slow push only; ft and tp turn to the spine; mt turns fully (plain back).
- Nov 12 8:54 AM ET: his yes (Both, via the main chat). Uploaded from out5 originals (Shopify files READY), scheduled in Metricool as TRIAL_REEL, auto-share off: 9:15 AM (425719544), 12 (425719574), 3 PM (425719605), 6 PM (425719627), 9 PM (425719655). Next: confirm they published, then build day 2 (Fri) on the next refresh.

## Nov 13 (refresh from routine; routine still can't reach the reels folder)
- Day 1 (Nov 12) all 5 published as Trial Reels. 7:30 AM read (10-22 h): O1 zad 296 views 21.2%, ft 123 / 8.9%, k_tw 130 / 23.1%; O2 mt 146 / 9.6%, tp 125 / 11.6%. Pooled: O1 18.9% on 549 views, O2 10.5% on 271 views.
- Warning flagged to the owner: format v2 reels hold far worse than everything before (old Trial Reels 26-34%, feed reels 24-35%) and get 120-300 views. Plan rules unchanged; continue block, his call.
- Day 2 rendered (scratchpad out6 originals; shared copies in reels/batch-2026-11-13/, captions.md there): 9 zad O2, 12 mt O1, 3 ft O2, 6 tp O1, 9 k_tw O2. All in stock. Sheet rows awaiting yes.
- Block 1 call is due the morning after day 2 (Sat). O2 will likely need a day 3 (repeat of day 1) to reach 500 views.

## Nov 13, 9:02 AM ET: his yes, but blocked
- the owner said yes (relayed 9:01 AM ET) to scheduling Friday's 5. Coordinator asked: first slot ~9:15 AM, then 12, 3, 6, 9 PM ET.
- Shopify and Metricool MCP servers failed to connect in this session (502), so nothing uploaded or scheduled.
- Next session: if both connect, upload out6 originals (scratchpad may be gone; then use batch-2026-11-13 copies but check byte sizes), schedule remaining slots from the next sensible time, ending 9 PM ET. His yes covers today only.
- 11:36 AM ET refresh: Metricool answers again; no IG Trial Reels scheduled today (only a TikTok post at 12 PM). Refresh can't use his morning yes, so card asks again: schedule all 5 from next free slot through 9 PM ET. On his yes: day-2 order (zad O2, mt O1, ft O2, tp O1, ktw O2) spread to 9 PM.
- 5:18 PM ET: his second yes (relayed). Uploaded out6 originals to Shopify, scheduled all 5 as TRIAL_REEL, shareTrialAutomatically false: 5:45 zad O2 (427531011), 6:30 mt O1 (427531027), 7:15 ft O2 (427531043), 8:05 tp O1 (427531062), 9:00 ktw O2 (427531080).
- Block 1 day 2 ran evening-only, so by Sat morning these have <15 h of data. Saturday call should note that; O2 will very likely need day 3 anyway.

## Nov 14 (refresh from routine; routine still can't reach the reels folder)
- Fri batch published: all 5 as Trial Reels between 5:46 and 9:03 PM ET.
- Read 7:15 AM ET. Block 1 called: O1 18.0% hold on 1,058 views, O2 15.3% on 781; gap 2.7 points, so O1 stays champion, no rematch. Day 2 only ~11 h old, recheck at 72 h. Repeat penalty not hit (day 2 768 views vs day 1 1,071).
- Compare: same-period automated feed reels 419-2,370 views, 23.7-31.4% hold (Bukhari 9 vols 2,370; Aqeedah 1,470; Thalathat 1,341; Mutoon 1,180; Forty Hadith 1,030). v2 Trial Reels 110-445 views.
- Block 2 = O1 vs O3 (motion only). O3 built in render_v2.py (no text 0-1 s, book pushes in from 1.16x, single books turn in 35 deg; title at 1.0 s).
- Problem: doc rule "no book in two blocks in a row" needs 5 new books; only sth has photos and it has no verified count. Rendered block 2 day 1 with the same 5 books anyway so a yes is quick: 9 mt O1, 12 zad O3, 3 k_tw O1, 6 tp O3, 9 ft O1. O1 files are byte-identical to block 1's O1 renders (Instagram may treat exact reposts as unoriginal).
- Files: scratchpad out7 originals (upload these), shared copies reels/batch-2026-11-14/, captions.md there. All 5 in stock (Shopify Nov 14). Sheet rows "awaiting choice".
- Asked him: reuse the books / send photos of 5 other books / skip today. Refresh, so no yes counts; nothing scheduled.
- 10:31 AM ET: the owner picked "Reuse this week's books" (relayed; the option said today's 5 go out 12 PM to 9 PM). Uploaded out7 originals, scheduled TRIAL_REEL, shareTrialAutomatically false: 12:00 mt O1 (428094326), 2:15 zad O3 (428094347), 4:30 k_tw O1 (428094368), 6:45 tp O3 (428094381), 9:00 ft O1 (428094396).
- Next (block 2 day 2, Sun): swap: 9 mt O3, 12 zad O1, 3 k_tw O3, 6 tp O1, 9 ft O3. His pick covers reusing these books for block 2; each day still needs his yes. Render: python3 -I render_v2.py books <out> 1115-01:O3:mt 1115-02:O1:zad 1115-03:O3:k_tw 1115-04:O1:tp 1115-05:O3:ft
