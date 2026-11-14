# Dar Al Athari – Daily Trial Reels: handover

Everything the daily Trial Reels batch needs, exported from Claude Duet on Nov 14, 2026.
Rendered videos are left out. README.md (the original procedure) and notes/working-notes.md
(the running log, with past Metricool ids and Instagram links) are included as they were.

## Contents
- render_v2.py: renders the format v2 reels (the Nov 12–14 batches). Use this one.
- reelkit.py: shared helpers (fonts, easing, end card). render_v2.py imports it.
- render_batch1.py, render_1110b.py, render_1111.py: older format renderers (Nov 9–11), kept for reference.
- books/: book photos (front, spine, back, set shots).
- fonts/Amiri-*.ttf: Arabic titles. fonts/inter/*.otf: Latin text (Inter, SIL Open Font License).
- batch-sheet.csv: every reel planned or posted (reel_id, date, time, opening, book, file, status, metricool_id, instagram_url).
- score-sheet.csv: per-reel performance scores used to pick the winning opening in each two-day block.
- batches/batch-YYYY-MM-DD/captions.md: captions for each batch.
- notes/working-notes.md: the task's working notes.

## Logo
There is no logo image file. The end card draws the words "DAR AL ATHARI" as text, in
reelkit.end_card().

## Setup
- Python 3 with Pillow built with libraqm (Arabic shaping): `python3 -c "from PIL import features; print(features.check('raqm'))"` must print True.
- ffmpeg on PATH (frames are piped to it; output is 1080x1920, 30 fps, H.264 mp4).
- Inter fonts: reelkit.py and render_batch1.py read them from `FD = '/usr/share/fonts/opentype/inter/'`.
  Either install Inter there, or change FD to the full path of this folder's fonts/inter/ (keep the trailing slash).
- Amiri is found automatically next to render_v2.py in fonts/.

## Render one reel
From this folder:

    python3 -I render_v2.py books out 1115-01:O3:mt

- `books` is the photo folder, `out` the output folder.
- Each job is `<reel_id>:<opening>:<book code>`. Openings built: O1, O2, O3. Book codes and their facts are in the BOOKS_V2 table in render_v2.py (zad, mt, k_tw, tp, ft, sth).
- Several jobs can follow in one command. The next planned batch was:
  `python3 -I render_v2.py books out 1115-01:O3:mt 1115-02:O1:zad 1115-03:O3:k_tw 1115-04:O1:tp 1115-05:O3:ft`
- Output: out/<reel_id>.mp4.

## Where the book photos come from
The photos in books/ were copied from the store's "Book Library" artifact in Claude
(product photos of the store's own books). Downloading straight from cdn.shopify.com didn't
work from Duet's sandbox, so new photos were added by hand to books/ with the same naming
(`<code>_front.jpg`, `<code>_spine.jpg`, ...). A new book also needs a row in BOOKS_V2.

## Uploading a video so Metricool can fetch it
Metricool needs a public URL. Videos are hosted as Shopify Files (Shopify Admin GraphQL):

1. `stagedUploadsCreate` with
   `{resource: FILE, filename: "<reel_id>.mp4", mimeType: "video/mp4", fileSize: "<exact bytes>", httpMethod: POST}`.
   Use resource FILE, not VIDEO: VIDEO makes Shopify transcode it down to 606x1080.
   Get the byte count with `stat -c %s <file>`.
2. POST the file to the returned `url` as multipart form data: every returned parameter first, the file last:
   `curl -sS -o /dev/null -w '%{http_code}' -F key=... -F ... -F file=@<reel_id>.mp4 <url>`. Expect 201.
3. `fileCreate` with `{originalSource: "<resourceUrl>", contentType: FILE}`.
4. Query the GenericFile by id until `fileStatus` is READY, then take its `url` (a cdn.shopify.com address).
   That URL goes in Metricool's `media`.

Upload the original rendered file. A copy that's been passed through another app can change size.

## Scheduling a Trial Reel in Metricool
Tool: Metricool MCP `createScheduledPost`, brand blogId `7251923` (Instagram @daralathari).

    blogId: "7251923"
    date:   "2026-11-15T09:00:00-05:00"
    info:
    {
      "autoPublish": true,
      "draft": false,
      "text": "<caption from captions.md>",
      "media": ["<cdn.shopify.com url>"],
      "providers": [{"network": "instagram"}],
      "publicationDate": {"dateTime": "2026-11-15T09:00:00", "timezone": "America/New_York"},
      "instagramData": {"type": "TRIAL_REEL", "isAiGenerated": false},
      "firstCommentText": "",
      "descendants": [],
      "shortener": false,
      "smartLinkData": {"ids": []},
      "hasNotReadNotes": false,
      "mediaAltText": []
    }

- `instagramData.type` must be `TRIAL_REEL`, every time.
- The response should show `shareTrialAutomatically: false` (auto-share to followers off).
- Daily slots: 9 AM, 12 PM, 3 PM, 6 PM and 9 PM ET. Each batch is shown to the owner and posted only on his yes.
- After the last slot, `getScheduledPosts` shows which are still pending (a post drops off once published).
  Then fill status and metricool_id (and instagram_url) in batch-sheet.csv.

## Format v2 rules
From the plan doc (https://claude.ai/artifact/2RFhCZ5VRoD5DXF1F4bbKW): one book per reel, product facts
only, no study advice, the real book on screen in the first second. Use the doc's six openings in two-day
blocks; the block winner is picked from score-sheet.csv. State on Nov 14: the number-fact opening won
block 1 (18.0% vs 15.3%).
