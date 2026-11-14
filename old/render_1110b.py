"""Tue Nov 10 batch: 5 Trial Reels (1110-04 to 1110-08).
Usage: python3 -I render_1110b.py <books_dir> <out_dir> [4|5|6|7|8]
Changes from batch 1, from its first read (skip rate ~75%, avg watch 3-4 s):
the book is on screen from the first frame, the hook text shows at once (no word-by-word build),
and every reel is 8-10 s instead of 11-13.5 s."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import *  # noqa: F401,F403  (W, H, fonts, helpers, render, BOOKS, OUT, ONLY)

def hook(fr, t, text, t_out, size=84, y=230):
    a = (1 - prog(t, t_out, t_out + .3)) * ease_out(prog(t, 0, .12))
    if a > 0:
        text_block(fr, text, 'InterDisplay-ExtraBold.otf', size, y, alpha=a, maxw=940)

def book_box(front, spine, FH):
    """Returns draw(fr, ang, cx, cy, scale) that turns a book; negative ang shows the spine on the right."""
    front = fit_h(front, FH)
    SW = round(front.width * 0.16)
    spine = spine.resize((SW, FH), Image.LANCZOS)
    def box(fr, ang, cx, cy, scale):
        r = math.radians(abs(ang))
        fw, sw = math.cos(r) * front.width, math.sin(r) * SW
        parts = [(front, fw), (spine, sw)] if ang < 0 else [(spine, sw), (front, fw)]
        tot = (fw + sw) * scale
        hh = round(FH * scale)
        x = cx - tot / 2
        s, pad = shadow_for((max(1, round(tot)), hh))
        fr.paste((0, 0, 0), (round(x) - pad, round(cy - hh / 2) - pad), s)
        for img, w_ in parts:
            ww = round(w_ * scale)
            if ww >= 1:
                im = img.resize((ww, hh), Image.BILINEAR)
                k = .55 if img is spine else lerp(.6, 1, w_ / front.width)
                if k < .999:
                    im = ImageEnhance.Brightness(im).enhance(k)
                fr.paste(im, (round(x), round(cy - hh / 2)))
            x += w_ * scale
    return box

# ---------- 1110-04: H01 B01 C03 T1 (sth) ----------
def reel4():
    box = book_box(load('sth_front.jpg'), load('sth_spine.jpg'), 1000)
    qs = ['Who is your Lord?', 'What is your religion?', 'Who is your Prophet?']
    def draw(fr, t):
        wordmark(fr)
        ang = -lerp(0, 50, ease_io(prog(t, 5.0, 5.8))) + lerp(0, 50, ease_io(prog(t, 6.4, 7.1)))
        box(fr, ang, W / 2, lerp(1120, 1080, prog(t, 0, 7.4)), .6 + .04 * prog(t, 0, 7.4))
        hook(fr, t, "Do you know the three questions you'll be asked in the grave?", 2.2)
        for i, q in enumerate(qs):
            s0 = 2.4 + i * .75
            a = ease_out(prog(t, s0, s0 + .35)) * (1 - prog(t, 4.55, 4.85))
            if a > 0:
                text_block(fr, q, 'InterDisplay-ExtraBold.otf', 76, 220 + i * 120, color=GOLD if i == 2 else CREAM,
                           alpha=a, rise=(1 - a) * 24)
        la = ease_out(prog(t, 4.95, 5.35)) * (1 - prog(t, 7.2, 7.4))
        if la > 0:
            yy = text_block(fr, 'Sharh Thalathat al-Usul', 'InterDisplay-ExtraBold.otf', 80, 260, alpha=la, rise=(1 - la) * 24)
            text_block(fr, 'Shaykh Muhammad ibn Salih al-Uthaymeen', 'Inter-Medium.otf', 40, yy + 8, color=MUTE, alpha=la)
        end_card(fr, t, 7.3, 'Send this to someone starting to seek knowledge', 'Dar Al Athari · daralathari.com')
    render('1110-04_H01-B01-C03-T1-sth', 9.6, draw)

# ---------- 1110-05: H02 B01 C02 T1-flat (k_tw) ----------
def reel5():
    cov = fit_h(load('k_tw_front.jpg'), 1000)
    def draw(fr, t):
        wordmark(fr)
        z = .64 + .06 * prog(t, 0, 7)
        im = cov.resize((round(cov.width * z), round(cov.height * z)), Image.BILINEAR)
        paste_book(fr, im, W / 2, 1080 + 14 * math.sin(t * 1.6))
        hook(fr, t, 'Can you explain Tawhid in one sentence?', 2.3, size=92)
        a = ease_out(prog(t, 2.5, 2.9)) * (1 - prog(t, 4.6, 4.9))
        if a > 0:
            yy = text_block(fr, 'Kitab at-Tawhid', 'InterDisplay-ExtraBold.otf', 92, 250, alpha=a, rise=(1 - a) * 24)
            text_block(fr, 'Imam Muhammad ibn Abd al-Wahhab', 'Inter-Medium.otf', 42, yy + 8, color=MUTE, alpha=a)
        b = ease_out(prog(t, 4.9, 5.3)) * (1 - prog(t, 6.7, 6.9))
        if b > 0:
            text_block(fr, 'Chapter by chapter, with the evidence from the Qur’an and Sunnah', 'InterDisplay-Bold.otf', 60, 230,
                       alpha=b, rise=(1 - b) * 24, maxw=900)
        end_card(fr, t, 6.8, 'Save this for your reading list', 'Kitab at-Tawhid · daralathari.com')
    render('1110-05_H02-B01-C02-T1-ktw', 9.0, draw)

# ---------- 1110-06: H16 B08 C01 T3 (zad stack) ----------
def reel6():
    vols = [fit_h(load(f'zad_v{n}_spine.jpg'), 900) for n in range(1, 8)]
    total = sum(v.width for v in vols)
    # vol 1 on the right, vol 7 on the left
    xs, x = [], W / 2 + total / 2
    for v in vols:
        xs.append(x - v.width / 2); x -= v.width
    def draw(fr, t):
        wordmark(fr)
        z = 1 + .05 * prog(t, 2.8, 6.2)
        for i, v in enumerate(vols):
            s0 = .15 + i * .36
            e = ease_out(prog(t, s0, s0 + .42))
            if e <= 0: continue
            cy = lerp(-500, 1000, e)
            im = v if z == 1 else v.resize((round(v.width * z), round(v.height * z)), Image.BILINEAR)
            cx = W / 2 + (xs[i] - W / 2) * z
            paste_book(fr, im, cx, cy, shadow=(i == 0 or e < 1))
        n = sum(1 for i in range(7) if t >= .15 + i * .36 + .3)
        ca = 1 - prog(t, 3.0, 3.3)
        if n and ca > 0:
            text_block(fr, f'{n}', 'InterDisplay-Black.otf', 150, 230, color=GOLD, alpha=ca)
        ta = ease_out(prog(t, 3.2, 3.6)) * (1 - prog(t, 6.0, 6.2))
        if ta > 0:
            yy = text_block(fr, "Zad al-Ma’ad", 'InterDisplay-ExtraBold.otf', 96, 230, alpha=ta, rise=(1 - ta) * 24)
            text_block(fr, 'Imam Ibn al-Qayyim  ·  all 7 volumes', 'Inter-Medium.otf', 42, yy + 8, color=MUTE, alpha=ta)
        end_card(fr, t, 6.1, 'Zad al-Ma’ad, all 7 volumes', 'Available at daralathari.com, link in bio')
    render('1110-06_H16-B08-C01-T3-zad', 8.6, draw)

# ---------- 1110-07: H18 B06 C05 T5-shelf (tp, ft, k_tw, sth, mt, zad) ----------
def reel7():
    names = ['tp_front.jpg', 'ft_front.jpg', 'k_tw_front.jpg', 'sth_front.jpg', 'mt_front.jpg', 'zad_front.jpg']
    covers = [fit_h(load(n), 430) for n in names]
    pos = [(W / 2 - 330, 820), (W / 2, 820), (W / 2 + 330, 820), (W / 2 - 330, 1360), (W / 2, 1360), (W / 2 + 330, 1360)]
    def draw(fr, t):
        wordmark(fr)
        for row_y in (1050, 1590):
            a = ease_out(prog(t, 0, .4))
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle([90, row_y, W - 90, row_y + 10], fill=GOLD + (int(150 * a),))
            fr.paste(lay, (0, 0), lay)
        for i, c in enumerate(covers):
            s0 = .2 + i * .42
            e = ease_out(prog(t, s0, s0 + .4))
            if e <= 0: continue
            cx, cy = pos[i]
            paste_book(fr, c, cx, lerp(cy - 160, cy, e), alpha=e)
        hook(fr, t, 'POV: your first serious Islamic bookshelf', 4.3, size=88, y=250)
        end_card(fr, t, 5.4, 'Which of these have you read?', 'Tell us in the comments')
    render('1110-07_H18-B06-C05-T5-shelf', 8.2, draw)

# ---------- 1110-08: H21 B03 C10 T1-flat (ft) ----------
def reel8():
    cov = fit_h(load('ft_front.jpg'), 1000)
    items = ['The Three Fundamental Principles', 'The Six Fundamental Principles', 'The Four Foundational Rules',
             'The Nullifiers of Islam', 'Removal of the Doubts']
    def draw(fr, t):
        wordmark(fr)
        m = ease_io(prog(t, 2.2, 2.9))
        z = lerp(.66, .44, m)
        im = cov.resize((round(cov.width * z), round(cov.height * z)), Image.BILINEAR)
        paste_book(fr, im, W / 2, lerp(1100, 560, m))
        hook(fr, t, '5 core treatises of creed, explained in one book', 2.1, size=88)
        for i, it in enumerate(items):
            s0 = 2.8 + i * .55
            a = ease_out(prog(t, s0, s0 + .35)) * (1 - prog(t, 7.4, 7.6))
            if a > 0:
                y = 920 + i * 112
                f = font('InterDisplay-Black.otf', 56)
                lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((120, y + (1 - a) * 18), str(i + 1), font=f, fill=GOLD + (int(255 * a),))
                fr.paste(lay, (0, 0), lay)
                text_block(fr, it, 'InterDisplay-Bold.otf', 52, y + 4, alpha=a, rise=(1 - a) * 18, align='left', x=200)
        la = ease_out(prog(t, 5.8, 6.2)) * (1 - prog(t, 7.4, 7.6))
        if la > 0:
            text_block(fr, 'Explained by Shaykh Ahmad ibn Yahya an-Najmi', 'Inter-Medium.otf', 40, 1520, color=MUTE, alpha=la)
        end_card(fr, t, 7.5, '', '')
    render('1110-08_H21-B03-C10-T1-ft', 9.2, draw)

for rid, fn in (('4', reel4), ('5', reel5), ('6', reel6), ('7', reel7), ('8', reel8)):
    if ONLY in (None, rid): fn()
