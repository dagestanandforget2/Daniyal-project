# Dar Al Athari TikTok studio

This branch is the toolkit for the daily Dar Al Athari TikTok video: real motion graphics built as HTML pages, rendered frame by frame with Playwright, never AI-generated footage.

Store: Dar Al Athari LLC, daralathari.com. An online Salafi/Athari Islamic bookstore in Hillsborough, New Jersey that ships internationally. It sells Arabic and English books plus traditional garments (thobes, shemaghs, kufis). TikTok account: dar.al.athari_ (Metricool brand id 7251923).

## Daily workflow

1. Read `log.md`. Each new video must look clearly different from the last several: a different palette, typefaces, layout idea and motion idea. The owner has rejected videos that "basically made the same ad again".
2. Pick a subject. It can be one book, a theme (creed, tafsir, fiqh, tazkiyah, Arabic vs English), the garments, or the store in general.
3. Plan the design before coding. Write down 4–6 hex colours, 1–2 fontsource typefaces, the scene list with timings, and the one memorable moment. Then check the plan against `log.md` and the design rules below.
4. Create `days/YYYY-MM-DD/film_src.html` and `days/YYYY-MM-DD/sfx.py`. Copy the structure of an example, not its look.
5. Preview with `python3 tools/build.py days/DATE && python3 tools/shot.py days/DATE 1 4 8 12 16`. Look at `chk.jpg` and fix problems: text clipped or off-screen, text outside the safe zone, overlaps, blank frames, ugly 3D angles.
6. Render with `tools/make.sh days/DATE 18 videos/DATE-slug.mp4` (about 4 minutes). Check `days/DATE/sheet.jpg`.
7. Write the caption (rules below), append an entry to `log.md`, then commit and push the video, the day folder (without film.html) and log.md to this branch.
8. Schedule the post with Metricool `createScheduledPost`:
   - `blogId` "7251923", network `tiktok`
   - media URL: `https://raw.githubusercontent.com/dagestanandforget2/Daniyal-project/tiktok-studio/videos/<file>.mp4`
   - `publicationDate` 12:00 today, America/New_York (if that has passed, 10 minutes from now); `autoPublish: true`, `draft: false`
   - `tiktokData` is required and must include a `title` (a short hook line): `{"title":"...","privacyOption":"PUBLIC_TO_EVERYONE","isAigc":false,"autoAddMusic":false,"disableComment":false,"disableDuet":false,"disableStitch":false,"commercialContentOwnBrand":false,"commercialContentThirdParty":false}`
   - Metricool copies the file from the raw GitHub URL, so push before scheduling and check that the URL returns HTTP 200.

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

## Design rules (from the owner's design skills)

- Take a distinctive point of view every time and put the boldness in one place. Avoid defaults: cream plus serif plus terracotta; near-black with one acid accent; SaaS card grids; tracked-out all-caps eyebrow labels on every heading; "A · B · C" meta strings; arrows tacked onto button text.
- Typography carries the piece. Choose typefaces for this brief, avoid Inter, Roboto and Arial, and set a clear type scale. Don't colour a single word in a headline just to accent it.
- Motion should feel like it has weight: use custom easing (`io`, `oc`, `ob`, exponential), never linear. Build one orchestrated hero moment rather than scattered fade-ups.
- Pull colour from the subject: the gold foil, leather and paper of the actual books, Islamic geometry and architecture.
- End card: logo, daralathari.com, and one clear call to action ("Shop the collection", "Browse the books", and so on).

## Caption format

Hook line, 2–5 short lines naming the real titles and authors shown, "Shop at daralathari.com 🔗 Link in bio", "Shipped from New Jersey.", then 8–12 relevant hashtags (#islamicbooks #salafi #athari #studentofknowledge #islamicbookstore plus topic tags). Keep it under 2,000 characters.
