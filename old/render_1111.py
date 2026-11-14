"""Wed Nov 11 batch: 5 Trial Reels (1111-01 to 1111-05).
Usage: python3 -I render_1111.py <books_dir> <out_dir> [1|2|3|4|5]
Leans on the winners so far: the question hook (H02, Kitab at-Tawhid, 1,270 views at 19 h),
the lit-up Zad set (H15, 912 views, 35% hold), the shelf POV (H18, 35% hold). One fresh concept (mt, H23)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import *  # noqa: F401,F403


def hook(fr, t, text, t_out, size=84, y=230):
    a = (1 - prog(t, t_out, t_out + .3)) * ease_out(prog(t, 0, .12))
    if a > 0:
        text_block(fr, text, 'InterDisplay-ExtraBold.otf', size, y, alpha=a, maxw=940)


def turn_box(front, spine, back, FH):
    """draw(fr, ang, cx, cy, scale): orthographic turn showing front, spine and (past 90 deg) back."""
    front = fit_h(front, FH)
    SW = round(front.width * 0.16)
    spine = spine.resize((SW, FH), Image.LANCZOS)
    back = back.resize((front.width, FH), Image.LANCZOS) if back is not None else front

    def box(fr, ang, cx, cy, scale):
        a = ang % 360
        r = math.radians(a)
        fw, sw = abs(math.cos(r)) * front.width, abs(math.sin(r)) * SW
        face = front if (a < 90 or a >= 270) else back
        if a < 90 or 180 <= a < 270:
            parts = [(spine, sw), (face, fw)]
        else:
            parts = [(face, fw), (spine, sw)]
        tot = sum(p[1] for p in parts) * scale
        x = cx - tot / 2
        hh = round(FH * scale)
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


# ---------- 1111-01: H02 B01 C03 T1 (k_tw) : winner's hook, CTA swapped to "send" ----------
def reel1():
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
        end_card(fr, t, 6.8, 'Send this to someone starting to seek knowledge', 'Kitab at-Tawhid · daralathari.com')
    render('1111-01_H02-B01-C03-T1-ktw', 9.0, draw)


# ---------- 1111-02: H22 B03 C02 T1 (tp) : the question-hook format on a new book ----------
def reel2():
    box = turn_box(load('tp_front.jpg'), load('tp_spine.jpg'), None, 1000)
    items = ['Knowing your Lord', 'Knowing your religion', 'Knowing your Prophet']

    def draw(fr, t):
        wordmark(fr)
        m = ease_io(prog(t, 2.2, 2.9))
        ang = -lerp(0, 40, ease_io(prog(t, 6.0, 6.6)))
        box(fr, ang, W / 2, lerp(1080, 560, m), lerp(.64, .44, m))
        hook(fr, t, 'Can you name the three fundamental principles?', 2.1, size=88)
        for i, it in enumerate(items):
            s0 = 2.8 + i * .6
            a = ease_out(prog(t, s0, s0 + .35)) * (1 - prog(t, 5.6, 5.8))
            if a > 0:
                y = 960 + i * 130
                f = font('InterDisplay-Black.otf', 64)
                lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).text((170, y + (1 - a) * 18), str(i + 1), font=f, fill=GOLD + (int(255 * a),))
                fr.paste(lay, (0, 0), lay)
                text_block(fr, it, 'InterDisplay-Bold.otf', 62, y + 4, alpha=a, rise=(1 - a) * 18, align='left', x=250,
                           color=GOLD if i == 2 else CREAM)
        la = ease_out(prog(t, 5.8, 6.2)) * (1 - prog(t, 7.4, 7.6))
        if la > 0:
            yy = text_block(fr, 'Commentary on the Three Fundamental Principles', 'InterDisplay-ExtraBold.otf', 64, 1020,
                            alpha=la, rise=(1 - la) * 20, maxw=900)
            text_block(fr, 'Shaykh Muhammad ibn Salih al-Uthaymeen', 'Inter-Medium.otf', 40, yy + 10, color=MUTE, alpha=la)
        end_card(fr, t, 7.5, 'Save this for your reading list', 'Commentary on the Three Fundamental Principles · daralathari.com')
    render('1111-02_H22-B03-C02-T1-tp', 9.6, draw)


# ---------- 1111-03: H15 B08 C01 T3 (zad set) : batch 1's best visual, shorter ----------
def reel3():
    SH = 1000
    st = fit_h(load('zad_set.jpg'), SH)
    sx = st.width / 1160
    bounds = [(935, 1160), (805, 935), (600, 805), (440, 600), (290, 440), (160, 290), (0, 160)]
    dim = ImageEnhance.Brightness(st).enhance(.28)
    step = .38

    def draw(fr, t):
        wordmark(fr)
        z = 1 + 0.06 * prog(t, 0, 8)
        img = dim.copy()
        for i, (x0, x1) in enumerate(bounds):
            k = ease_out(prog(t, .2 + i * step, .2 + i * step + .3))
            if k > 0:
                xa, xb = round(x0 * sx), round(x1 * sx)
                crop = st.crop((xa, 0, xb, SH))
                img.paste(crop, (xa, 0), None if k >= 1 else Image.new('L', crop.size, int(255 * k)))
        g = prog(t, 3.0, 3.9)
        if 0 < g < 1:
            gl = Image.new('L', img.size, 0)
            gx = lerp(img.width + 200, -200, g)
            ImageDraw.Draw(gl).polygon([(gx, 0), (gx + 120, 0), (gx - 80, SH), (gx - 200, SH)], fill=70)
            gl = gl.filter(ImageFilter.GaussianBlur(30))
            img.paste((255, 236, 200), (0, 0), gl)
        if z != 1:
            img = img.resize((round(img.width * z), round(img.height * z)), Image.BILINEAR)
        paste_book(fr, img, W / 2, 860)
        n = min(7, int(max(0, t - .2) / step) + 1) if t >= .2 else 0
        ca = 1 - prog(t, 3.0, 3.3)
        if n and ca > 0:
            text_block(fr, f'Volume {n} of 7', 'Inter-SemiBold.otf', 44, 1430, color=GOLD, alpha=ca)
        ta = ease_out(prog(t, 3.4, 3.9)) * (1 - prog(t, 6.0, 6.2))
        if ta > 0:
            yy = text_block(fr, "Zad al-Ma’ad", 'InterDisplay-ExtraBold.otf', 96, 1380, alpha=ta, rise=(1 - ta) * 30)
            text_block(fr, 'Imam Ibn al-Qayyim  ·  complete in 7 volumes', 'Inter-Medium.otf', 40, yy + 6, color=MUTE, alpha=ta)
        end_card(fr, t, 6.1, 'Zad al-Ma’ad, all 7 volumes', 'Available at daralathari.com, link in bio')
    render('1111-03_H15-B08-C01-T3-zad', 8.6, draw)


# ---------- 1111-04: H18 B06 C02 T5 (shelf) : best hold so far, CTA swapped to "save" ----------
def reel4():
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
            if e <= 0:
                continue
            cx, cy = pos[i]
            paste_book(fr, c, cx, lerp(cy - 160, cy, e), alpha=e)
        hook(fr, t, 'POV: your first serious Islamic bookshelf', 4.3, size=88, y=250)
        end_card(fr, t, 5.4, 'Save this for your reading list', 'All six at daralathari.com')
    render('1111-04_H18-B06-C02-T5-shelf', 8.2, draw)


# ---------- 1111-05: H23 B01 C01 T1 (mt) : fresh, the feed's best-selling title ----------
def reel5():
    box = turn_box(load('mt_front.jpg'), load('mt_spine.jpg'), load('mt_back.jpg'), 1000)

    def draw(fr, t):
        wordmark(fr)
        ang = lerp(0, 180, ease_io(prog(t, 2.6, 3.6))) + lerp(0, 180, ease_io(prog(t, 4.8, 5.8)))
        box(fr, ang, W / 2, 1100, .62 + .04 * prog(t, 0, 7))
        hook(fr, t, 'Every core text for the student of knowledge, in one volume', 2.4, size=84)
        a = ease_out(prog(t, 2.6, 3.0)) * (1 - prog(t, 6.6, 6.8))
        if a > 0:
            yy = text_block(fr, 'Al-Mutoon al-Jami’ah', 'InterDisplay-ExtraBold.otf', 92, 250, alpha=a, rise=(1 - a) * 24)
            text_block(fr, 'Compiled by Dr. Abdul Muhsin al-Qasim', 'Inter-Medium.otf', 42, yy + 8, color=MUTE, alpha=a)
        end_card(fr, t, 6.7, 'Al-Mutoon al-Jami’ah li Talib al-‘Ilm', 'Available at daralathari.com, link in bio')
    render('1111-05_H23-B01-C01-T1-mt', 9.0, draw)


for rid, fn in (('1', reel1), ('2', reel2), ('3', reel3), ('4', reel4), ('5', reel5)):
    if ONLY in (None, rid):
        fn()
