# Dar Al Athari TikTok studio

This branch is the toolkit for the daily Dar Al Athari TikTok video: real motion graphics built as HTML pages, rendered frame by frame with Playwright, never AI-generated footage.

Store: Dar Al Athari LLC, daralathari.com. An online Salafi/Athari Islamic bookstore in Hillsborough, New Jersey that ships internationally. It sells Arabic and English books plus traditional garments (thobes, shemaghs, kufis). TikTok account: dar.al.athari_ (Metricool brand id 7251923).

## Daily workflow

0. Dates are New York dates. Get today's with `TZ=America/New_York date +%F` and use it for the day folder, the video file name and the `log.md` entry. The evening video made at about 8 PM New York time belongs to that same New York day (folder `DATE-pm`), even though the server clock may already show tomorrow.
1. Read `log.md`. Each new video must look clearly different from the last several: a different palette, typefaces, layout idea and motion idea. The owner has rejected videos that "basically made the same ad again".
2. Pick a subject and a format, following "What the numbers say" below: by default ONE book (or one multi-volume set), chosen as the book in `assets/BOOKS.md` that `log.md` shows was featured longest ago. Garments and the store in general are also allowed.
3. Plan the design before coding. Write down 4–6 hex colours, 1–2 fontsource typefaces, the scene list with timings, and the one memorable moment. Then check the plan against `log.md` and the design rules below.
4. Create `days/YYYY-MM-DD/film_src.html` and `days/YYYY-MM-DD/sfx.py`. Copy the structure of an example, not its look.
5. Preview with `python3 tools/build.py days/DATE && python3 tools/shot.py days/DATE 0 1 4 8 12 16`. Look at `chk.jpg` and fix problems: text clipped or off-screen, text outside the safe zone, overlaps, blank frames, ugly 3D angles. The frame at 0 s and the frame at 1 s must already show the real book large and the hook line (see "The first second").
6. Render with `tools/make.sh days/DATE 18 videos/DATE-slug.mp4` (about 4 minutes). Check `days/DATE/sheet.jpg`.
7. Write the caption (rules below), append an entry to `log.md` (date, format, concept, palette, fonts, books used), then commit and push the day folder (without film.html) and log.md to this branch. Do NOT commit the video: `videos/` is git-ignored.
8. Put the video online with `tools/publish.sh videos/DATE-slug.mp4`. It uploads the file to the `video-drop` branch (one video, replaced every time, so the repository stops growing), waits until the address answers, and prints `VIDEO_URL <address>` on its last line. Use exactly that address as the media URL.
9. Schedule the post with Metricool `createScheduledPost`:
   - `blogId` "7251923", network `tiktok`
   - media URL: the `VIDEO_URL` printed by `tools/publish.sh`
   - `publicationDate` 12:00 today, America/New_York (if that has passed, 10 minutes from now); `autoPublish: true`, `draft: false`
   - `tiktokData` is required and must include a `title` (a short hook line): `{"title":"...","privacyOption":"PUBLIC_TO_EVERYONE","isAigc":false,"autoAddMusic":false,"disableComment":false,"disableDuet":false,"disableStitch":false,"commercialContentOwnBrand":false,"commercialContentThirdParty":false}`
   - Metricool copies the file from that address when the post is scheduled, so publish before scheduling. `tools/publish.sh` has already checked that the address returns HTTP 200.

## What the numbers say (reviewed 10 Nov 2026)

These rules come from the account's own results and override older habits in `log.md`.

- About 3 in 4 viewers swipe away within the first three seconds, and the average watch time is about 4 seconds of 18. Videos with a lower skip rate got clearly more views. The first second decides the video.
- The daily videos average about half the views of the owner's own phone videos, which simply show the book straight away.
- Almost every video so far has been "three books plus an object metaphor" using the same 14 books. That format is now the exception.

### The first second

- At 0.0 s the real book photo is already on screen, large (at least half the frame height) and readable. Never open on an empty field, a pattern, a title card alone, or the prop/metaphor object arriving. The prop may arrive with the book or after it, never before it.
- The hook line is fully readable by 0.5 s. No slow letter-by-letter reveal for the hook. Make it a concrete product fact about this book: what it is, how many volumes, the language, the binding, who wrote or explained it. Examples of the kind: "All 7 volumes of Zad al-Ma'ad.", "Fully vocalised Arabic, one volume.", "The Sealed Nectar, in hardcover."
- Something moves in the first second (the book turns, lands, opens, or the camera pushes in). A still opening counts as a failed opening.
- The book's title and author are readable on screen before 3 s.

### One book, different formats

- Default: ONE book or one multi-volume set per video, shown properly: front, spine, back, and an inside page when `assets/` has a verified one.
- At most two videos a week may show two or three books. Check `log.md` before choosing.
- Rotate through every entry in `assets/BOOKS.md` before repeating one. Two videos on the same day never share a book.
- Change the format as well as the look. Formats to rotate: a close look at one book (cover, spine, back, page); a set reveal (volumes sliding out of a spine-out row); the same work in Arabic and in English side by side; a look at an inside page; the garments; the store in general. Write the format in the `log.md` entry and do not use the same format two days running.

## Page contract (how the tools expect a film)

- Stage 540×960 CSS px, rendered at 2× to 1080×1920, 30 fps. Videos are 15–20 s, usually 18.
- `window.__seek(t)` must be a pure function of t (seconds). Never use CSS animations, timers or Date.
- Line 1 declares fonts, e.g. `<!--FONTS Big Shoulders Display:big-shoulders-display:latin:500,700,900:normal -->` (Family:fontsource-package:subset:weights:style; separate several with `;`). Put `/*FONTS*/` inside the `<style>`. Missing packages install automatically.
- Put `/*LIB*/` at the top of the script to get `tools/lib.js`: easing helpers (`cl sm oc io ob lerp keyed`), `makeBook(parent,key)` and `pose(book,{x,y,z,rx,ry,rz,s,g,blur,op,hide})` for 3D books built from the real cover photos. The keys and sizes are in `SPEC` at the top of lib.js. See `examples/shelf-3d`.
- Assets are referenced as `assets/<file>`. `build.py` symlinks the folder in.
- Safe zones for TikTok: keep all text out of the top 10% (y < 96), the bottom 20% (y > 768) and the right 12% (x > 475). Images can bleed.
- Logo: `assets/logo.png` is white on transparent black and goes on dark backgrounds with `mix-blend-mode:screen`. `assets/logo_dark.png` is black on white and goes on light backgrounds with `mix-blend-mode:multiply`. Blend modes fail inside transformed or filtered parents, so put the logo directly in `#stage`, or inside a container whose background matches the page.
- Sound: `sfx.py` uses `tools/sfxlib.py` (whoosh, thud, slap, clack, tick, click, scratch, scrape, rumble, flip, shimmer, endcard, master). Use noise-based effects only: **no music, no instruments, no melodic tones.** The owner adds TikTok audio himself.

## Content rules (strict)

- Use only real images: the book photos in `assets/` (the gallery is listed in `assets/BOOKS.md`) and the logo. Draw no people and no faces. There are no garment photos yet, so garments get typographic or abstract treatment, never fake product photos.
- Never invent product facts, prices, discounts, stock levels, quotes or rulings. All the books on file are long-standing stock, so never call them "new" or "just arrived".
- Known garment facts: black thobe $50, white thobe $45, sizes 52–60, extra panels for flexibility, double stitching, cooling fabric. Check Shopify before using any other price.
- Religious text (Qur'an, hadith, scholars' words) must be copied exactly from a page photo in `assets/` or from rabee.net, binbaz.org.sa or binothaimeen.net, with the source. If you are unsure, leave it out.
- Tone: modest and confident. No hype, no fake urgency, and nothing that assumes the viewer's religion.
- No study advice in the store's own voice, on screen or in the caption. The store sells books; it does not tell people what to study or in what order. Do not write "start with", "begin with", "first… then…", "a simple path", "foundations first", "before you study anything", "every student needs this", or rank books by level. Describe each book as a product: title, author or explainer, publisher, language, binding, number of volumes. If a publisher's own description states the intended reader, it may be quoted only with attribution ("the publisher describes it as…").
- Hooks and captions do not ask or answer religious questions and do not summarise a book's religious content. The title, the author and the product facts are enough.

## Design rules (from the owner's design skills)

- Take a distinctive point of view every time and put the boldness in one place. Avoid defaults: cream plus serif plus terracotta; near-black with one acid accent; SaaS card grids; tracked-out all-caps eyebrow labels on every heading; "A · B · C" meta strings; arrows tacked onto button text.
- Typography carries the piece. Choose typefaces for this brief, avoid Inter, Roboto and Arial, and set a clear type scale. Don't colour a single word in a headline just to accent it.
- Motion should feel like it has weight: use custom easing (`io`, `oc`, `ob`, exponential), never linear. Build one orchestrated hero moment rather than scattered fade-ups.
- Pull colour from the subject: the gold foil, leather and paper of the actual books, Islamic geometry and architecture.
- End card: logo, daralathari.com, and one clear call to action ("Shop the collection", "Browse the books", and so on).

## Caption format

Hook line (a product fact, as in "The first second"), 1–4 short lines naming the real titles and authors shown, "Shop at daralathari.com 🔗 Link in bio", "Shipped from New Jersey.", then 8–12 relevant hashtags (#islamicbooks #salafi #athari #studentofknowledge #islamicbookstore plus topic tags). Keep it under 2,000 characters.
