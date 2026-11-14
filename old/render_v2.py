"""Format v2 Trial Reels (plan doc, Nov 11): one book, 9 s, only the first second changes.
0-1 s opening (O1..O3 built; O4-O6 to add), 1-7 s body (front, spine, back; a set shows its volumes; title + author by 3 s),
7-9 s end card (one more product fact, logo, daralathari.com).
Usage: python3 -I render_v2.py <books_dir> <out_dir> <reel_id>:<opening>:<book> [...]
  e.g. 1112-01:O1:zad 1112-02:O2:mt
Every line below comes from the Shopify product page or the cover (checked Nov 12)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
JOBS = sys.argv[3:]
sys.argv = sys.argv[:3]
from reelkit import *  # noqa: F401,F403
from PIL import ImageChops

AR_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'Amiri-Bold.ttf')
DUR = 9.0

BOOKS_V2 = {
    'zad': dict(kind='set', img='zad_set.jpg',
                title="Zad al-Ma’ad", by='Imam Ibn Qayyim al-Jawziyyah',
                ar='زاد المعاد', en="Zad al-Ma’ad",
                o1='All 7 volumes of Zad al-Ma’ad.',
                end='Arabic hardcover, 7 volumes, Dar Ataat al-Ilm'),
    'mt': dict(kind='single', front='mt_front.jpg', spine='mt_spine.jpg', back='mt_back.jpg',
               title="Al-Mutoon al-Jami’ah li Talib al-‘Ilm", by='Compiled by Shaykh Dr. Abdul Muhsin al-Qasim',
               ar='المتون الجامعة لطالب العلم', en="Al-Mutoon al-Jami’ah li Talib al-‘Ilm",
               o1='15 texts in one volume.',
               end='Arabic hardcover, 712 pages'),
    'ft': dict(kind='single', front='ft_front.jpg', spine='ft_spine.jpg', back=None,
               title='Beautiful Commentary on the Five Foundational Treatises of Creed',
               by='Explained by Shaykh Ahmad ibn Yahya an-Najmi',
               ar='التعليقات البهية', en='Beautiful Commentary on the Five Foundational Treatises of Creed',
               o1='5 treatises in one book.',
               end='English edition, Hikmah Publications'),
    'tp': dict(kind='single', front='tp_front.jpg', spine='tp_spine.jpg', back=None,
               title='Commentary on the Three Fundamental Principles of Islam',
               by='Shaykh Muhammad ibn Salih al-Uthaymeen',
               ar='شرح ثلاثة الأصول', en='Commentary on the Three Fundamental Principles of Islam',
               o1='260 pages.',
               end='English hardcover, Darussalam'),
    'k_tw': dict(kind='single', front='k_tw_front.jpg', spine=None, back=None,
                 title='Kitab at-Tawhid', by='Imam Muhammad ibn Abd al-Wahhab',
                 ar='كتاب التوحيد', en='Kitab at-Tawhid, The Book of Monotheism',
                 o1='192 pages.',
                 end='English hardcover, Darussalam'),
}


def turn_box(front, spine, back, FH):
    front = fit_h(front, FH)
    SW = round(front.width * 0.16)
    spine = spine.resize((SW, FH), Image.LANCZOS) if spine is not None else None
    back = back.resize((front.width, FH), Image.LANCZOS) if back is not None else front

    def box(fr, ang, cx, cy, scale):
        if spine is None:
            ang = 0
        a = ang % 360
        r = math.radians(a)
        fw = abs(math.cos(r)) * front.width
        sw = abs(math.sin(r)) * SW if spine is not None else 0
        face = front if (a < 90 or a >= 270) else back
        parts = [(spine, sw), (face, fw)] if (a < 90 or 180 <= a < 270) else [(face, fw), (spine, sw)]
        parts = [p for p in parts if p[0] is not None]
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


def arabic_title(fr, text, en, t, y=200):
    """O2: Arabic title writes in right to left (done by 0.45 s), English under it."""
    f = ImageFont.truetype(AR_FONT, 112, layout_engine=ImageFont.Layout.RAQM)
    lay = Image.new('RGBA', (W, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bb = d.textbbox((0, 0), text, font=f, direction='rtl', language='ar')
    tw = bb[2] - bb[0]
    d.text(((W - tw) / 2 - bb[0], 10), text, font=f, fill=GOLD + (255,), direction='rtl', language='ar')
    k = ease_out(prog(t, 0, .45))
    out_a = 1 - prog(t, 1.0, 1.3)
    if out_a <= 0:
        return
    x_left = (W - tw) / 2
    edge = x_left + tw * (1 - k) - 30          # reveal from the right edge towards the left
    m = Image.new('L', lay.size, 0)
    md = ImageDraw.Draw(m)
    md.rectangle([edge + 30, 0, W, 260], fill=int(255 * out_a))
    for i in range(30):
        md.line([(edge + i, 0), (edge + i, 260)], fill=int(255 * out_a * i / 30))
    fr.paste(lay, (0, y), ImageChops.multiply(m, lay.split()[3]))
    text_block(fr, en, 'InterDisplay-Bold.otf', 50, y + 225, alpha=ease_out(prog(t, .05, .3)) * out_a, maxw=920)


def opening_text(fr, t, txt, size=88, y=250):
    a = ease_out(prog(t, 0, .12)) * (1 - prog(t, 1.0, 1.3))
    if a > 0:
        size = 120 if len(txt) <= 12 else size
        text_block(fr, txt, 'InterDisplay-ExtraBold.otf', size, y, alpha=a, maxw=760)


def reel(reel_id, op, code):
    b = BOOKS_V2[code]

    def intro(t):
        # O3 motion only: the book pushes in from close up during the first second, no text
        return 1 + .16 * (1 - ease_out(prog(t, 0, 1.0))) if op == 'O3' else 1
    if b['kind'] == 'set':
        st = fit_h(load(b['img']), 820)
        if st.width > 980:
            st = st.resize((980, round(st.height * 980 / st.width)), Image.LANCZOS)
        SH = st.height

        def book(fr, t):
            z = (.92 + .1 * prog(t, 0, 7)) * intro(t)
            img = st.copy()
            g = prog(t, 3.4, 4.4)
            if 0 < g < 1:
                gl = Image.new('L', img.size, 0)
                gx = lerp(img.width + 200, -200, g)
                ImageDraw.Draw(gl).polygon([(gx, 0), (gx + 120, 0), (gx - 80, SH), (gx - 200, SH)], fill=70)
                img.paste((255, 236, 200), (0, 0), gl.filter(ImageFilter.GaussianBlur(30)))
            img = img.resize((round(img.width * z), round(img.height * z)), Image.BILINEAR)
            paste_book(fr, img, W / 2 + lerp(-20, 20, prog(t, 0, 7)), 1120)
    else:
        box = turn_box(load(b['front']), load(b['spine']) if b['spine'] else None,
                       load(b['back']) if b['back'] else None, 1000)
        has_back = b['back'] is not None
        spine_ok = b['spine'] is not None

        def book(fr, t):
            if has_back:
                ang = lerp(0, 360, ease_io(prog(t, 3.2, 6.2)))
            else:
                ang = -lerp(0, 50, ease_io(prog(t, 3.4, 4.4))) * (1 - ease_io(prog(t, 5.0, 6.0)))
            if op == 'O3' and spine_ok:
                ang += -35 * (1 - ease_out(prog(t, 0, 1.0)))
            sc = (.76 + .05 * prog(t, 0, 7)) * intro(t)
            box(fr, ang, W / 2, 1150 + 12 * math.sin(t * 1.6), sc)

    def draw(fr, t):
        wordmark(fr)
        book(fr, t)
        if op == 'O1':
            opening_text(fr, t, b['o1'])
        elif op == 'O2':
            arabic_title(fr, b['ar'], b['en'], t)
        elif op == 'O3':
            pass                      # motion only: no text until the title at 1 s
        else:
            raise SystemExit(f'{op} not built yet')
        t_in = 1.0 if op == 'O3' else 1.3
        a = ease_out(prog(t, t_in, t_in + .4)) * (1 - prog(t, 6.8, 7.0))
        if a > 0:
            yy = text_block(fr, b['title'], 'InterDisplay-ExtraBold.otf', 76, 230, alpha=a, rise=(1 - a) * 24, maxw=940)
            text_block(fr, b['by'], 'Inter-Medium.otf', 42, yy + 10, color=MUTE, alpha=a, maxw=900)
        end_card(fr, t, 7.0, b['end'], 'daralathari.com')
    render(reel_id, DUR, draw)


for job in JOBS:
    rid, op, code = job.split(':')
    name = f"{rid}_{op}_{code.replace('_', '')}"
    reel(name, op, code)
