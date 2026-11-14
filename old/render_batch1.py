"""Batch 1 motion-graphic reels for Dar Al Athari. Usage: python3 -I reels.py <books_dir> <out_dir> [reel_id]"""
import sys, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 30
BOOKS, OUT = sys.argv[1], sys.argv[2]
ONLY = sys.argv[3] if len(sys.argv) > 3 else None
FD = '/usr/share/fonts/opentype/inter/'
GOLD = (214, 178, 106)
CREAM = (244, 238, 226)
MUTE = (176, 168, 152)
BG1, BG2 = (14, 14, 16), (34, 27, 20)

_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + name, size)
    return _fc[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)
def ease_out(x): return 1 - (1 - x) ** 3
def ease_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def lerp(a, b, x): return a + (b - a) * x

def load(name):
    return Image.open(os.path.join(BOOKS, name)).convert('RGB')

def fit_h(img, h):
    return img.resize((max(1, round(img.width * h / img.height)), h), Image.LANCZOS)

# ---------- background ----------
def make_bg():
    bg = Image.new('RGB', (W, H), BG1)
    g = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(g)
    for r in range(900, 0, -12):
        v = int(255 * (1 - r / 900) ** 1.6)
        d.ellipse([W / 2 - r * 1.1, H * 0.42 - r, W / 2 + r * 1.1, H * 0.42 + r], fill=v)
    g = g.filter(ImageFilter.GaussianBlur(40))
    warm = Image.new('RGB', (W, H), BG2)
    return Image.composite(warm, bg, g)
BG = make_bg()

def shadow_for(size, blur=38, alpha=170):
    w, h = size
    pad = blur * 3
    s = Image.new('L', (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(s).rectangle([pad, pad + 18, pad + w, pad + h + 18], fill=alpha)
    return s.filter(ImageFilter.GaussianBlur(blur)), pad

def paste_book(frame, img, cx, cy, alpha=1.0, shadow=True):
    x, y = round(cx - img.width / 2), round(cy - img.height / 2)
    if shadow and alpha > 0:
        s, pad = shadow_for(img.size)
        if alpha < 1: s = s.point(lambda v: int(v * alpha))
        frame.paste((0, 0, 0), (x - pad, y - pad), s)
    if alpha >= 1:
        frame.paste(img, (x, y))
    elif alpha > 0:
        frame.paste(img, (x, y), Image.new('L', img.size, int(255 * alpha)))

def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def text_block(frame, text, fname, size, y, color=CREAM, alpha=1.0, maxw=900, lh=1.18, rise=0, align='center', x=None, stagger=None):
    """Draw wrapped text. stagger=(t_local, per_word) reveals word by word."""
    if alpha <= 0: return y
    f = font(fname, size)
    lines = wrap(text, f, maxw)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = y + rise
    wi = 0
    for ln in lines:
        lw = f.getlength(ln)
        xx = (W - lw) / 2 if align == 'center' else x
        if stagger is None:
            d.text((xx, yy), ln, font=f, fill=color + (int(255 * alpha),))
        else:
            tl, per = stagger
            for w_ in ln.split(' '):
                a = ease_out(prog(tl, wi * per, wi * per + 0.25)) * alpha
                if a > 0:
                    d.text((xx, yy + (1 - a) * 18), w_, font=f, fill=color + (int(255 * a),))
                xx += f.getlength(w_ + ' ')
                wi += 1
        yy += size * lh
    frame.paste(layer, (0, 0), layer)
    return y + len(lines) * size * lh

def wordmark(frame, alpha=1.0):
    if alpha <= 0: return
    f = font('Inter-SemiBold.otf', 30)
    layer = Image.new('RGBA', (W, 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = 64
    for ch in 'DAR AL ATHARI':
        d.text((x, 92), ch, font=f, fill=GOLD + (int(230 * alpha),))
        x += f.getlength(ch) + 6
    d.line([(64, 136), (64 + 120, 136)], fill=GOLD + (int(160 * alpha),), width=2)
    frame.paste(layer, (0, 0), layer)

def end_card(frame, t, t0, cta, sub):
    a = ease_out(prog(t, t0, t0 + 0.5))
    if a <= 0: return
    ov = Image.new('RGB', (W, H), BG1)
    frame.paste(ov, (0, 0), Image.new('L', (W, H), int(238 * a)))
    f = font('Inter-SemiBold.otf', 44)
    lw = f.getlength('DAR AL ATHARI') + 12 * 12
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = (W - lw) / 2
    for ch in 'DAR AL ATHARI':
        d.text((x, 640), ch, font=f, fill=GOLD + (int(255 * a),))
        x += f.getlength(ch) + 12
    d.line([(W / 2 - 60, 720), (W / 2 + 60, 720)], fill=GOLD + (int(200 * a),), width=2)
    frame.paste(layer, (0, 0), layer)
    b = ease_out(prog(t, t0 + 0.25, t0 + 0.85))
    yb = text_block(frame, cta, 'InterDisplay-Bold.otf', 66, 790, alpha=b, rise=(1 - b) * 30, maxw=960)
    c = ease_out(prog(t, t0 + 0.6, t0 + 1.2))
    text_block(frame, sub, 'Inter-Medium.otf', 38, yb + 30, color=MUTE, alpha=c, maxw=880)

def render(reel_id, dur, draw):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, reel_id + '.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', path], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        frame = BG.copy()
        draw(frame, t)
        p.stdin.write(frame.tobytes())
        if i in (int(n * .1), int(n * .45), int(n * .8)):
            frame.save(os.path.join(OUT, f'{reel_id}_f{i:03d}.jpg'), quality=85)
    p.stdin.close(); p.wait()
    print('wrote', path)

# ---------- Reel 1: H08 B06 C02 T5 (tp, ft, k_tw) ----------
def reel1():
    covers = [fit_h(load('tp_front.jpg'), 860), fit_h(load('ft_front.jpg'), 860), fit_h(load('k_tw_front.jpg'), 860)]
    small = [fit_h(c, 420) for c in covers]
    labels = [('Commentary on the Three Fundamental Principles', 'Shaykh Ibn Uthaymeen'),
              ('Beautiful Commentary on the Five Foundational Treatises of Creed', 'Shaykh Ahmad an-Najmi'),
              ('Kitab at-Tawhid', 'Imam Muhammad ibn Abd al-Wahhab')]
    slots = [W / 2 - 330, W / 2, W / 2 + 330]
    starts = [2.3, 4.4, 6.5]
    def draw(fr, t):
        wordmark(fr, ease_out(prog(t, 0, .4)))
        ha = 1 - prog(t, 2.0, 2.4)
        if ha > 0:
            text_block(fr, '3 books to start learning your creed, in order', 'InterDisplay-ExtraBold.otf', 96, 720,
                       alpha=ha, maxw=900, stagger=(t, 0.11))
        for i in range(3):
            s = starts[i]
            if not (s <= t < s + 2.15): continue
            enter = ease_out(prog(t, s, s + .55))
            leave = ease_io(prog(t, s + 1.75, s + 2.1))
            cx = lerp(W + 520, W / 2, enter) - leave * (W / 2 + 520)
            paste_book(fr, covers[i], cx, 820)
            la = enter * (1 - prog(t, s + 1.6, s + 1.8))
            if la > 0:
                text_block(fr, f'{i + 1}', 'InterDisplay-Black.otf', 120, 190, color=GOLD, alpha=la)
                yy = text_block(fr, labels[i][0], 'InterDisplay-Bold.otf', 54, 1300, alpha=la, maxw=860)
                text_block(fr, labels[i][1], 'Inter-Medium.otf', 38, yy + 10, color=MUTE, alpha=la, maxw=860)
        if t >= 8.6:
            ta = ease_out(prog(t, 8.7, 9.2))
            text_block(fr, 'Start here. Then go deeper.', 'InterDisplay-Bold.otf', 66, 560, alpha=ta, rise=(1 - ta) * 20)
            for i in range(3):
                e = ease_out(prog(t, 8.6 + i * .18, 9.2 + i * .18))
                if e > 0:
                    paste_book(fr, small[i], slots[i], lerp(1300, 1000, e), alpha=e)
                    f = font('InterDisplay-Black.otf', 64)
                    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                    ImageDraw.Draw(lay).text((slots[i] - f.getlength(str(i + 1)) / 2, lerp(1530, 1230, e)), str(i + 1), font=f, fill=GOLD + (int(255 * e),))
                    fr.paste(lay, (0, 0), lay)
        end_card(fr, t, 10.8, 'Save this for your reading list', 'All three at daralathari.com')
    render('1110-01_H08-B06-C02-T5-tp', 13.5, draw)

# ---------- Reel 2: H05 B01 C01 T1 (mt) ----------
def reel2():
    FH = 1000
    front, spine, back = load('mt_front.jpg'), load('mt_spine.jpg'), load('mt_back.jpg')
    front = fit_h(front, FH); spine = fit_h(spine, FH); back = fit_h(back, FH)
    SW = round(front.width * 0.16)  # spine thickness on screen
    spine = spine.resize((SW, FH), Image.LANCZOS)
    back = back.resize((front.width, FH), Image.LANCZOS)
    lines = ['The core texts for the student of knowledge, in one volume',
             'Compiled by Dr. Abdul Muhsin al-Qasim, Imam of al-Masjid an-Nabawi',
             'Verified against 160 manuscripts']
    def box(fr, ang, cx, cy, scale):
        # orthographic rotation: show front (cos) and spine (sin); after 90deg show spine and back
        a = ang % 360
        r = math.radians(a)
        fw, sw = abs(math.cos(r)) * front.width, abs(math.sin(r)) * SW
        face = front if (a < 90 or a >= 270) else back
        parts = []
        if a < 90:   parts = [(spine, sw, .55), (face, fw, 1.0)]       # spine on left turning in
        elif a < 180: parts = [(face, fw, 1.0), (spine, sw, .55)]
        elif a < 270: parts = [(spine, sw, .55), (face, fw, 1.0)]
        else: parts = [(face, fw, 1.0), (spine, sw, .55)]
        tot = sum(p[1] for p in parts) * scale
        x = cx - tot / 2
        hh = round(FH * scale)
        s, pad = shadow_for((max(1, round(tot)), hh))
        fr.paste((0, 0, 0), (round(x) - pad, round(cy - hh / 2) - pad), s)
        for img, w_, light in parts:
            ww = round(w_ * scale)
            if ww >= 1:
                im = img.resize((ww, hh), Image.BILINEAR)
                if light < 1 or (img is face and w_ < front.width * .98):
                    k = light if img is spine else lerp(.6, 1, w_ / front.width)
                    im = ImageEnhance.Brightness(im).enhance(k)
                fr.paste(im, (round(x), round(cy - hh / 2)))
            x += w_ * scale
    def draw(fr, t):
        wordmark(fr, ease_out(prog(t, 0, .4)))
        ha = 1 - prog(t, 2.1, 2.5)
        if ha > 0:
            text_block(fr, "You want to seek knowledge but don't know where to start?", 'InterDisplay-ExtraBold.otf', 92, 640,
                       alpha=ha, maxw=920, stagger=(t, 0.1))
        if t >= 2.35:
            e = ease_out(prog(t, 2.35, 3.05))
            ang = -lerp(0, 58, ease_io(prog(t, 4.6, 5.5))) + lerp(0, 58, ease_io(prog(t, 7.0, 7.9)))
            scale = lerp(.55, .74, e) + 0.03 * prog(t, 2.9, 10)
            box(fr, ang, W / 2, lerp(1300, 760, e), scale)
            for i, ln in enumerate(lines):
                s0 = 3.0 + i * 1.6
                a = ease_out(prog(t, s0, s0 + .45)) * (1 - prog(t, s0 + 1.45, s0 + 1.6)) if i < 2 else ease_out(prog(t, s0, s0 + .45)) * (1 - prog(t, 9.6, 9.8))
                if a > 0:
                    text_block(fr, ln, 'InterDisplay-Bold.otf', 54, 1210, alpha=a, rise=(1 - a) * 24, maxw=880)
        end_card(fr, t, 9.7, 'Al-Mutoon al-Jami’ah li Talib al-‘Ilm', 'Available now at daralathari.com, link in bio')
    render('1110-02_H05-B01-C01-T1-mt', 12.4, draw)

# ---------- Reel 3: H15 B08 C04 T3 (zad) ----------
def reel3():
    SH = 1000
    st = load('zad_set.jpg')
    st = fit_h(st, SH)
    sx = st.width / 1160
    # spine x-ranges in original px, vol 1 on the right
    bounds = [(935, 1160), (805, 935), (600, 805), (440, 600), (290, 440), (160, 290), (0, 160)]
    dim = ImageEnhance.Brightness(st).enhance(.28)
    def draw(fr, t):
        wordmark(fr, ease_out(prog(t, 0, .4)))
        a = ease_out(prog(t, 0, .8))
        z = 1 + 0.06 * prog(t, 0, 11)
        img = dim.copy()
        for i, (x0, x1) in enumerate(bounds):
            k = ease_out(prog(t, 1.0 + i * 0.55, 1.0 + i * 0.55 + .35))
            if k > 0:
                xa, xb = round(x0 * sx), round(x1 * sx)
                crop = st.crop((xa, 0, xb, SH))
                if k < 1:
                    img.paste(crop, (xa, 0), Image.new('L', crop.size, int(255 * k)))
                else:
                    img.paste(crop, (xa, 0))
        # glint sweep after all lit
        g = prog(t, 5.0, 6.0)
        if 0 < g < 1:
            gl = Image.new('L', img.size, 0)
            gx = lerp(img.width + 200, -200, g)
            ImageDraw.Draw(gl).polygon([(gx, 0), (gx + 120, 0), (gx - 80, SH), (gx - 200, SH)], fill=70)
            gl = gl.filter(ImageFilter.GaussianBlur(30))
            img.paste((255, 236, 200), (0, 0), gl)
        if z != 1:
            img = img.resize((round(img.width * z), round(img.height * z)), Image.BILINEAR)
        paste_book(fr, img, W / 2, lerp(900, 820, ease_out(prog(t, 0, 1.2))), alpha=a)
        # volume counter
        n = min(7, int(max(0, t - 1.0) / 0.55) + 1) if t >= 1.0 else 0
        ca = (1 - prog(t, 5.2, 5.5))
        if n and ca > 0:
            text_block(fr, f'Volume {n} of 7', 'Inter-SemiBold.otf', 44, 1430, color=GOLD, alpha=ca)
        ta = ease_out(prog(t, 5.6, 6.1)) * (1 - prog(t, 8.3, 8.5))
        if ta > 0:
            yy = text_block(fr, "Zad al-Ma’ad", 'InterDisplay-ExtraBold.otf', 96, 1380, alpha=ta, rise=(1 - ta) * 30)
            text_block(fr, 'Imam Ibn al-Qayyim  ·  complete in 7 volumes', 'Inter-Medium.otf', 40, yy + 6, color=MUTE, alpha=ta)
        end_card(fr, t, 8.4, 'Follow for one book a day', 'Dar Al Athari · Islamic books, shipped worldwide')
    render('1110-03_H15-B08-C04-T3-zad', 11.2, draw)

for rid, fn in (('1', reel1), ('2', reel2), ('3', reel3)):
    if ONLY in (None, rid): fn()
