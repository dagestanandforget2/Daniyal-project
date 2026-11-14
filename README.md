# Dar Al Athari Trial Reels kit

Everything the daily "Trial Reels batch" task needs to make, score and post Instagram Trial Reels
for @daralathari. The plan itself (rules, openings, standings, schedule, change log) lives in the
plan doc: https://claude.ai/artifact/2RFhCZ5VRoD5DXF1F4bbKW (Claude Doc id
0b7c0b48-b408-4866-834a-dd5a1eb72b39). Read the doc before every batch. Where the doc and this file
disagree, the doc wins, except that nothing may break the rules below.

This repository is public. Never commit tokens, passwords, emails, customer data or the owner's
personal name. Commit as `dar-al-athari-tasks <autopost-bot@users.noreply.github.com>`.

## Rules that override everything
1. No study advice in the store's voice, on screen or in captions: no "start with", "begin with",
   "first... then...", "a simple path", "foundations first", "every student needs this", no ranking
   books by level.
2. Openings and captions state product facts only: title, author or explainer, publisher, language,
   binding, number of volumes, what is printed on the cover. No religious questions, rulings or
   summaries of a book's religious content. No Qur'an or hadith text beyond a title. Never call a
   book "new". Invent nothing.
3. One book per reel. A multi-volume set of one work counts as one book.
4. The real book is on screen in the first second. Skip rate and 3-second hold are the top things
   to improve.
5. Nothing is posted or scheduled without the owner's yes to that day's batch.

## Frame rules (built into render_v3.py)
- The book is at least half the frame tall and is turning or pushing in for the whole first second.
- An opening line stays on screen for 2 seconds, large, written in word by word.
- No text in the top 15% or the bottom 25% of the frame. The renderer stops with an error if any
  text leaves that band.
- O1 (number fact) only for books with a real count on them (volumes, texts, treatises). Never a
  page count.

## Files
- `render_v3.py`  the renderer and the book table `BOOKS_T` (one entry per book: title, author
  line, Arabic title, the O1/O4/O5 lines and the end-card fact). `python3 render_v3.py --list`
  shows every book and the openings it can use.
- `reelkit.py`  shared drawing helpers (PIL frames piped to ffmpeg, 1080x1920, 30 fps, silent
  audio track).
- `books/`  real photos of each book: `<code>_front.jpg`, `_spine.jpg`, `_back.jpg`, or one
  `<code>_set.jpg` for a set.
- `fonts/`  Inter and Amiri (Arabic, shaped with raqm).
- `tools/publish.sh`  puts a batch's videos online for Metricool (branch `reels-drop`).
- `batch-sheet.csv`  one row per reel made: id, date, slot, opening, book, status, Metricool id.
- `score-sheet.csv`  one row per reel read: views, 3-second hold, average watch, shares, saves.
- `batches/batch-YYYY-MM-DD/captions.md`  that day's captions.
- `notes/`  working notes. `old/`  the earlier renderers and the Claude Duet handover, for
  reference only. Do not render with them.

## Rendering
```
python3 render_v3.py --list
python3 render_v3.py /tmp/out 1115-01:O1:zad 1115-02:O2:mt 1115-03:O1:ks 1115-04:O2:ts 1115-05:O1:sb
```
Each job writes `<id>_<opening>_<book>.mp4` (9 s, about 2 to 6 MB) and `<id>_<opening>_<book>_check.jpg`,
a strip of the frames at 0, 0.5, 1.5, 4 and 8 s with the two no-text lines drawn in red. Look at
every check strip before sending a batch: the book must be large and readable at 0 s, the opening
line fully legible at 0.5 s and still there at 1.5 s, and the Arabic must match the cover.

Openings: O1 number fact, O2 title (Arabic title writes in, English under it), O3 motion only (no
line, title at 1 s), O4 author or explainer, O5 edition fact (language, binding, publisher), O6
spine first (opens on the spine, turns to the cover; needs a spine photo).

## Adding a book
Put straightened photos in `books/`, add an entry to `BOOKS_T`, render one test and look at the
check strip. Every line must come from the cover or the live Shopify product page. If no verified
count exists, leave `o1=None`.

## The morning procedure
1. `git clone --depth 1 -b trial-reels https://github.com/dagestanandforget2/Daniyal-project trialreels`
2. Read the plan doc: which block and day it is, the champion, the challenger, the standings.
3. Score. In Metricool (blogId 7251923) read the Instagram reels of the last 10 days: date,
   caption, views (IGRE23), 3-second hold (IGRE28, "reel view rate"), average watch (IGRE24),
   saves (IGRE12), shares (IGRE21). Match each to its row in `batch-sheet.csv` by date, slot and
   caption, and write or update its row in `score-sheet.csv`. Pooled hold for an opening =
   sum(views x hold) / sum(views) over that opening's reels in the block.
4. If a block finished yesterday, call it by the doc's rules (500-view floor per opening, 8-point
   gap to win, 4 to 8 points behind = one rematch later, calls are provisional until the 72-hour
   read, repeat-penalty check). Update the standings table, the batch log and the change log in
   the doc.
5. Pick five books for today. Each must be active and in stock in Shopify, usable with both
   openings in the block, not used yesterday unless it is day 2 of a block (day 2 repeats day 1's
   books with the openings swapped), and its on-screen lines must agree with the live product page.
6. Slots (ET): 9 AM, 12 PM, 3 PM, 6 PM, 9 PM. Day 1: champion at 9, 3 and 9; challenger at 12 and 6.
   Day 2: swapped.
7. Render, look at all five check strips, fix anything wrong and render again.
8. Captions, one per reel, in `batches/batch-YYYY-MM-DD/captions.md`: one product-fact line, then
   "Available at daralathari.com, link in bio.", then hashtags. The hashtag count marks the arm:
   champion reels carry exactly 4 hashtags, challenger reels exactly 5.
9. `tools/publish.sh /tmp/out` and keep the VIDEO_URL lines.
10. Add the five rows to `batch-sheet.csv` (status `awaiting yes`), commit sheets and captions to
    `trial-reels` and push. Never commit videos.
11. Send the owner the batch: the five videos, the captions, the slots, and three lines on what
    was scored and decided. Then wait for his yes.
12. After his yes, schedule each reel with Metricool `createScheduledPost`:
    blogId "7251923", date "YYYY-MM-DDTHH:MM:SS-05:00" (use -04:00 during daylight time), info
    {autoPublish true, draft false, text <caption>, media [<VIDEO_URL>], providers
    [{"network":"instagram"}], publicationDate {dateTime "YYYY-MM-DDTHH:MM:SS", timezone
    "America/New_York"}, instagramData {"type":"TRIAL_REEL","isAiGenerated":false},
    firstCommentText "", descendants [], shortener false, smartLinkData {"ids":[]},
    hasNotReadNotes false, mediaAltText []}. The reply must show shareTrialAutomatically false and
    a static.metricool.com media address. A slot already past when the yes arrives: spread the
    remaining reels evenly between now + 20 minutes and 9 PM ET.
13. Confirm with getScheduledPosts, write the Metricool ids and status `scheduled` into
    `batch-sheet.csv`, commit and push.
