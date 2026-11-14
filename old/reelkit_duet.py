"""Shared helpers for Dar Al Athari motion-graphic reels. Scripts set sys.argv: <books_dir> <out_dir> [only]."""
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

