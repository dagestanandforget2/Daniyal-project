"""Shared helpers for Dar Al Athari Trial Reels (format v3). Everything is local to this folder:
book photos in books/, fonts in fonts/. No network needed to render."""
import sys, math, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
BOOKS = os.path.join(HERE, 'books')
FD = os.path.join(HERE, 'fonts', 'inter', '')
AR_FONT = os.path.join(HERE, 'fonts', 'Amiri-Bold.ttf')
GOLD = (214, 178, 106)
CREAM = (244, 238, 226)
MUTE = (176, 168, 152)
BG1, BG2 = (14, 14, 16), (34, 27, 20)

# Frame rules (plan doc): no text in the top 15% or the bottom 25% of the frame.
SAFE_TOP, SAFE_BOTTOM = round(H * .15), round(H * .75)      # 288 .. 1440
TEXT_SPAN = [H, 0]                                           # lowest / highest y any text touched


def _note(y0, y1):
    TEXT_SPAN[0] = min(TEXT_SPAN[0], y0)
    TEXT_SPAN[1] = max(TEXT_SPAN[1], y1)


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


def make_bg():
    bg = Image.new('RGB', (W, H), BG1)
    g = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(g)
    for r in range(900, 0, -12):
        v = int(255 * (1 - r / 900) ** 1.6)
        d.ellipse([W / 2 - r * 1.1, H * 0.5 - r, W / 2 + r * 1.1, H * 0.5 + r], fill=v)
    g = g.filter(ImageFilter.GaussianBlur(40))
    return Image.composite(Image.new('RGB', (W, H), BG2), bg, g)
BG = make_bg()


def shadow_for(size, blur=38, alpha=170):
    """Soft drop shadow, built at quarter size for speed."""
    w, h = size
    pad = blur * 3
    q = 4
    s = Image.new('L', ((w + pad * 2) // q + 1, (h + pad * 2) // q + 1), 0)
    ImageDraw.Draw(s).rectangle([pad // q, (pad + 18) // q, (pad + w) // q, (pad + h + 18) // q], fill=alpha)
    s = s.filter(ImageFilter.GaussianBlur(blur / q))
    return s.resize((w + pad * 2, h + pad * 2), Image.BILINEAR), pad


def paste_book(frame, img, cx, cy, shadow=True):
    x, y = round(cx - img.width / 2), round(cy - img.height / 2)
    if shadow:
        s, pad = shadow_for(img.size)
        frame.paste((0, 0, 0), (x - pad, y - pad), s)
    frame.paste(img, (x, y))


def wrap(text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if f.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def fit_text(text, fname, sizes, maxw=940, max_lines=3, lh=1.16, max_h=10 ** 6):
    """Largest size from `sizes` that wraps into max_lines and max_h px. Returns (size, n_lines, block_height)."""
    for s in sizes:
        n = len(wrap(text, font(fname, s), maxw))
        if n <= max_lines and n * s * lh <= max_h:
            return s, n, n * s * lh
    s = sizes[-1]
    n = len(wrap(text, font(fname, s), maxw))
    return s, n, n * s * lh


def text_block(frame, text, fname, size, y, color=CREAM, alpha=1.0, maxw=940, lh=1.16, rise=0,
               stagger=None, gold_digits=False):
    """Centered wrapped text. stagger=(t_local, per_word) reveals it word by word.
    gold_digits paints any word that holds a digit in gold."""
    f = font(fname, size)
    lines = wrap(text, f, maxw)
    end = y + len(lines) * size * lh
    if alpha <= 0:
        return end
    _note(y, end)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    yy = y + rise
    wi = 0
    for ln in lines:
        xx = (W - f.getlength(ln)) / 2
        for w_ in ln.split(' '):
            a = alpha
            if stagger is not None:
                tl, per = stagger
                a = ease_out(prog(tl, wi * per, wi * per + 0.22)) * alpha
            col = GOLD if (gold_digits and any(c.isdigit() for c in w_)) else color
            if a > 0:
                d.text((xx, yy + (1 - a / max(alpha, 1e-6)) * 16), w_, font=f, fill=col + (int(255 * a),))
            xx += f.getlength(w_ + ' ')
            wi += 1
        yy += size * lh
    frame.paste(layer, (0, 0), layer)
    return end


def arabic_line(frame, text, y, t, t_out, maxw=980, size=118):
    """Arabic title in gold, written in from right to left, ink top at y. Returns the y under it."""
    while True:
        f = ImageFont.truetype(AR_FONT, size, layout_engine=ImageFont.Layout.RAQM)
        bb = ImageDraw.Draw(Image.new('L', (8, 8))).textbbox((0, 0), text, font=f, direction='rtl', language='ar')
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if tw <= maxw or size <= 60:
            break
        size -= 6
    out_a = 1 - prog(t, t_out, t_out + .25)
    if out_a <= 0:
        return y + th
    _note(y, y + th)
    lay = Image.new('RGBA', (W, th + 20), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text(((W - tw) / 2 - bb[0], 10 - bb[1]), text, font=f, fill=GOLD + (255,),
                             direction='rtl', language='ar')
    k = ease_out(prog(t, -0.12, .45))               # already a third written on the very first frame
    edge = (W - tw) / 2 + tw * (1 - k) - 30
    m = Image.new('L', lay.size, 0)
    md = ImageDraw.Draw(m)
    md.rectangle([edge + 30, 0, W, lay.height], fill=int(255 * out_a))
    for i in range(30):
        md.line([(edge + i, 0), (edge + i, lay.height)], fill=int(255 * out_a * i / 30))
    frame.paste(lay, (0, y - 10), ImageChops.multiply(m, lay.split()[3]))
    return y + th


def end_card(frame, t, t0, cta, sub):
    a = ease_out(prog(t, t0, t0 + 0.5))
    if a <= 0: return
    frame.paste(Image.new('RGB', (W, H), BG1), (0, 0), Image.new('L', (W, H), int(238 * a)))
    f = font('Inter-SemiBold.otf', 44)
    lw = f.getlength('DAR AL ATHARI') + 12 * 12
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x = (W - lw) / 2
    for ch in 'DAR AL ATHARI':
        d.text((x, 700), ch, font=f, fill=GOLD + (int(255 * a),))
        x += f.getlength(ch) + 12
    d.line([(W / 2 - 60, 780), (W / 2 + 60, 780)], fill=GOLD + (int(200 * a),), width=2)
    frame.paste(layer, (0, 0), layer)
    _note(700, 780)
    b = ease_out(prog(t, t0 + 0.25, t0 + 0.85))
    yb = text_block(frame, cta, 'InterDisplay-Bold.otf', 66, 850, alpha=b, rise=(1 - b) * 30, maxw=960)
    c = ease_out(prog(t, t0 + 0.6, t0 + 1.2))
    text_block(frame, sub, 'Inter-Medium.otf', 40, yb + 30, color=MUTE, alpha=c, maxw=880)


CHECK_T = (0.0, 0.5, 1.5, 4.0, 8.0)

def render(out_dir, reel_id, dur, draw):
    """Writes <reel_id>.mp4 and <reel_id>_check.jpg (frames at 0, 0.5, 1.5, 4 and 8 s with the
    no-text lines drawn in red). Stops with an error if any text left the allowed band."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, reel_id + '.mp4')
    TEXT_SPAN[0], TEXT_SPAN[1] = H, 0
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart', path], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    marks = {min(n - 1, round(t * FPS)): t for t in CHECK_T}
    stills = []
    for i in range(n):
        frame = BG.copy()
        draw(frame, i / FPS)
        p.stdin.write(frame.tobytes())
        if i in marks:
            stills.append((marks[i], frame.resize((360, 640), Image.BILINEAR)))
    p.stdin.close(); p.wait()
    sheet = Image.new('RGB', (len(stills) * 368 + 8, 700), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for k, (t, im) in enumerate(stills):
        x = 8 + k * 368
        sheet.paste(im, (x, 52))
        for yy in (SAFE_TOP, SAFE_BOTTOM):
            d.line([(x, 52 + yy / 3), (x + 360, 52 + yy / 3)], fill=(255, 60, 60), width=1)
        d.text((x + 4, 12), f'{t:g} s', font=font('Inter-SemiBold.otf', 28), fill=(255, 255, 255))
    sheet.save(os.path.join(out_dir, reel_id + '_check.jpg'), quality=82)
    lo, hi = round(TEXT_SPAN[0]), round(TEXT_SPAN[1])
    ok = lo >= SAFE_TOP and hi <= SAFE_BOTTOM
    print(f"wrote {path}  {os.path.getsize(path) / 1e6:.1f} MB  text band {lo}-{hi} px  {'ok' if ok else 'OUT OF BOUNDS'}")
    if not ok:
        raise SystemExit(f'{reel_id}: text left the allowed band ({SAFE_TOP}-{SAFE_BOTTOM} px)')
    return path
