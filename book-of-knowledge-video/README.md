# The Book of Knowledge – promo film (Dar Al Athari)

Pure-function film: `src/film.js` exposes `seek(t)`; `tools/render.mjs` screenshots each frame in headless Chromium and pipes to ffmpeg.

```
python3 -I tools/prep_photos.py                 # perspective-correct + even out the photos -> src/assets/photos
python3 -I tools/make_audio.py                  # synthesised noise-only SFX -> out/sfx.wav
node tools/audit_safe.mjs                       # checks all text stays in the platform safe area
node tools/render.mjs --scale 0.5 --out out/preview_silent.mp4     # fast preview
node tools/render.mjs --scale 2   --out out/final_silent.mp4       # full quality (supersampled)
ffmpeg -i out/final_silent.mp4 -i out/sfx.wav -c:v copy -c:a aac -b:a 192k -shortest out/book-of-knowledge.mp4
node tools/render.mjs --still 10.5,27.8 --scale 1 --out out/stills # stills at given seconds
```
To reuse for another book: change the photo corners in `tools/prep_photos.py`, the `Book({...})` configs, text/quotes and timeline in `src/film.js`.
