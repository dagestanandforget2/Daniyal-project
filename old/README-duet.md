# Dar Al Athari Trial Reels: how a batch gets made and posted

Plan doc: https://claude.ai/artifact/2RFhCZ5VRoD5DXF1F4bbKW (Claude Doc id 0b7c0b48-b408-4866-834a-dd5a1eb72b39). Follow its FORMAT V2 and the four rules at its top (the owner's standing instruction, Nov 11). Hooks H01-H23, bodies B01-B10, CTAs C01-C10, the 60/25/15 mix, the "1 in 5 fresh experiment" and the four-part reel score are retired. Read the doc before every build; it wins over this file.

## The four rules (override everything)
1. No study advice in the store's voice, on screen or in captions ("start with", "begin with", "first... then...", "foundations first", "every student needs this", ranking by level).
2. Product facts only in openings and captions: title, author or explainer, publisher, language, binding, number of volumes, what is on the cover. No religious questions, no summaries of a book's religious content.
3. One book per reel. A multi-volume set of one work counts as one book.
4. The real book is on screen and moving in the first second.

## Making a batch (format v2)
- Every reel: one book, 9 seconds. 0-1 s opening (the only thing that changes). 1-7 s body: front, spine, back (a set lines up its volumes); title and author on screen by 3 s. 7-9 s end card: one more product fact (publisher, binding, language or volumes), then logo and daralathari.com.
- Six openings: O1 Number fact (count from the book, e.g. "All 7 volumes of Zad al-Ma'ad."), O2 Title (Arabic title writes in, English under it), O3 Motion only (no text, title at 1 s), O4 Author or explainer, O5 Edition fact (language, binding, publisher), O6 Spine first. O1 is champion to start. A book goes in a test only if both openings in it work for it.
- Templates: T1 Cover turn (single books), T3 Set and spines (sets). T2 and T5 retired, T4 parked.
- Two-day blocks: champion vs one challenger, same 5 books, same 5 slots. Day 1: 9 AM champ, 12 chall, 3 champ, 6 chall, 9 champ; day 2 swapped. Block 1 Thu Nov 12 + Fri Nov 13 = O1 vs O2; then O3, O4, O5, O6 (one block each), then any rematch. A missed day moves the rest back. Same book at most once a day; no book in two blocks in a row.
- Calling a block (morning after day 2): each opening needs 500+ views in the block, else add a day 3 (repeat of day 1). Gap of 8+ points in pooled 3-second hold = new champion; under 8 = champion stays; lost by 4-8 = one rematch later. Recheck at 72 h. Stop early if a champion holds 40%.
- Score: only the pooled 3-second hold per opening (Metricool IGRE28, weighted by views). Body/CTA/reel scores off until an opening wins. Standings table in the doc, updated each morning; batch message says which block and day it is and the standings.
- Repeat penalty: if day-2 reels get under half of day 1's views across a block, day 2 switches to 5 different books and each test runs two blocks.
- Captions: one product-fact line, then "Available at daralathari.com, link in bio", then 3-5 hashtags.
- Reel ID: MMDD-NN_Ox_book (e.g. 1112-03_O2_zad), in file name and batch sheet, never on screen. Files in batch-YYYY-MM-DD/, captions.md there, a row per reel in batch-sheet.csv (status "awaiting yes", no comma in status).
- Renderer for v2: render_v2.py (O1 and O2 built; add O3-O6 before their blocks). Usage: python3 -I render_v2.py books <out_dir> 1113-01:O2:zad ... Book facts live in its BOOKS_V2 table. Arabic font: reels/fonts/Amiri-Bold.ttf (raqm shaping works). cdn.shopify.com downloads are refused here, so only reels/books photos are usable.
- Shared helpers: reelkit.py (PIL frames piped to ffmpeg, 1080x1920, 30 fps, Inter fonts). render_1110b.py and render_1111.py are old-format; reuse turn_box() and the Zad set code, not their hook/CTA text. Arabic (O2): PIL has raqm shaping; needs a proper Naskh font with harakat (only DejaVu/FreeSerif here), check right-to-left rendering against the cover before use.
- Book photos: reels/books/ (tp, ft, k_tw, mt, sth, zad set and spines). Every fact from the product page or the cover; check stock in Shopify.
- Real motion graphics only, no AI footage. Scholar claims only from binbaz.org.sa, binothaimeen.net or rabee.net. Never the owner's personal name in customer-facing content.
- Daily amount: 5 Trial Reels a day (9 AM, 12, 3, 6, 9 PM ET), 7 from Tue Nov 17 if nothing blocked, then 9, max 10. Late yes: spread the rest evenly, ending by 9 PM ET. If blocked: stop that day, then 2 below that level for a week. Nothing posts without his yes to that day's batch.

## Posting (after his yes)
1. Shopify GraphQL stagedUploadsCreate, resource FILE (not VIDEO: VIDEO transcodes down to 606x1080), mimeType video/mp4, fileSize = exact bytes from stat -c %s.
2. curl POST each file to the staged url with every returned parameter, file last (expect 201).
3. fileCreate contentType FILE with originalSource = resourceUrl; query the GenericFile until READY and use its cdn.shopify.com url.
4. Metricool createScheduledPost, blogId 7251923, providers [{"network":"instagram"}], instagramData {"type":"TRIAL_REEL","isAiGenerated":false}, autoPublish true, timezone America/New_York, at the day's slots (see Daily amount). Metricool's reply shows shareTrialAutomatically false (auto-share off).
5. Check getScheduledPosts after the last slot; a post leaves the list once published. Update batch-sheet.csv status and metricool_id.
