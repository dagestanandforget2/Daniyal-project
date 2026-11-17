"""Trial Reels format v3: one book, 9 seconds, built to the frame rules in the plan doc.

  0-2 s  opening (O1..O6). The real book is on screen from the first frame, at least half the
         frame tall, and it is turning or pushing in for the whole first second. An opening line,
         when the opening has one, is large, written in word by word and stays up for 2 seconds.
  2-7 s  body: title and author on top, the book keeps moving and turns to show spine and back.
  7-9 s  end card: one more product fact, DAR AL ATHARI, daralathari.com.

No text is ever drawn in the top 15% or the bottom 25% of the frame (the renderer stops if it is).

Usage:
  python3 render_v3.py --list
  python3 render_v3.py <out_dir> <reel_id>:<opening>:<book> [...]
  e.g. python3 render_v3.py out 1115-01:O1:zad 1115-02:O4:tp

Every line in BOOKS_T is a product fact read from the cover or the Shopify product page.
Before a book is used, check its lines against the live product page; fix the table if they differ.
O1 is only for books with a real count on them (volumes, texts, treatises). Never a page count."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import *  # noqa: F401,F403

DUR = 9.0
TOP = 690          # the book's top edge; its height is at least 960 px (half the frame)
FH = 1000          # single book height in px at rest

# rtl=True: Arabic binding, spine on the right of the front cover.
BOOKS_T = {
    'zad': dict(kind='set', img='zad_set.jpg', rtl=True,
                title="Zad al-Ma’ad", by='Imam Ibn Qayyim al-Jawziyyah', ar='زاد المعاد',
                o1='All 7 volumes of Zad al-Ma’ad.',
                o4='By Imam Ibn Qayyim al-Jawziyyah.',
                o5='Arabic hardcover. Dar Ataat al-Ilm.',
                end='Arabic hardcover, 7 volumes, Dar Ataat al-Ilm'),
    'sb9': dict(kind='set', img='sb9_set.jpg', rtl=False,
                title='Sahih al-Bukhari', by='Translated by Dr. Muhammad Muhsin Khan', ar='صحيح البخاري',
                o1='All 9 volumes of Sahih al-Bukhari.',
                o4='Translated by Dr. Muhammad Muhsin Khan.',
                o5='Arabic and English. Darussalam hardcover.',
                end='Arabic-English, 9 volumes, Darussalam'),
    'mt': dict(kind='single', back=True, rtl=True,
               title="Al-Mutoon al-Jami’ah li Talib al-‘Ilm", by='Compiled by Shaykh Dr. Abdul Muhsin al-Qasim',
               ar='متون طالب العلم',
               o1='15 texts in one volume.',
               o4='Compiled by Shaykh Dr. Abdul Muhsin al-Qasim.',
               o5='Arabic hardcover, fully vocalised.',
               end='Arabic hardcover, 712 pages'),
    'ft': dict(kind='single', back=True, rtl=False,
               title='Beautiful Commentary on the Five Foundational Treatises of Creed',
               by='Explained by Shaykh Ahmad ibn Yahya an-Najmi', ar='التعليقات البهية',
               o1='5 treatises in one book.',
               o4='Explained by Shaykh Ahmad an-Najmi.',
               o5='English edition. Hikmah Publications.',
               end='English edition, Hikmah Publications'),
    'tp': dict(kind='single', back=True, rtl=False,
               title='Commentary on the Three Fundamental Principles of Islam',
               by='Shaykh Muhammad ibn Salih al-Uthaymeen', ar='شرح ثلاثة الأصول',
               o1=None,
               o4='Commentary by Shaykh Ibn al-Uthaymeen.',
               o5='English hardcover. Darussalam.',
               end='English hardcover, Darussalam'),
    'k_tw': dict(kind='single', spine=False, back=False, rtl=False,
                 title='Kitab at-Tawhid', by='Imam Muhammad ibn Abd al-Wahhab', ar='كتاب التوحيد',
                 o1=None,
                 o4='By Imam Muhammad ibn Abd al-Wahhab.',
                 o5='English hardcover. Darussalam.',
                 end='English hardcover, Darussalam'),
    'sth': dict(kind='single', back=True, rtl=True,
                title='Sharh Thalathat al-Usul', by='Shaykh Muhammad ibn Salih al-Uthaymeen', ar='شرح ثلاثة الأصول',
                o1=None,
                o4='Explained by Shaykh Ibn al-Uthaymeen.',
                o5='Arabic hardcover. Ibn Uthaymeen Charitable Foundation.',
                end='Arabic hardcover, Ibn Uthaymeen Charitable Foundation'),
    'ks': dict(kind='single', back=True, rtl=True,
               title='Sharh Kashf ash-Shubuhat', by='Shaykh Muhammad ibn Salih al-Uthaymeen', ar='شرح كشف الشبهات',
               o1='2 explanations in one volume.',
               o4='Explained by Shaykh Ibn al-Uthaymeen.',
               o5='Arabic hardcover. Ibn Uthaymeen Charitable Foundation.',
               end='With Sharh al-Usul as-Sittah. Arabic hardcover'),
    'bi': dict(kind='single', back=True, rtl=False,
               title='The Great Blessing in Collecting the Beliefs of the Imams of the Sunnah',
               by='Compiled by Shaykh Dr. Khalid al-Dhafiri', ar=None,
               o1=None,
               o4='Compiled by Shaykh Dr. Khalid al-Dhafiri.',
               o5='English paperback. Hikmah Publications.',
               end='English paperback, Hikmah Publications'),
    'pi': dict(kind='single', back=True, rtl=False,
               title='The Pillars of Islam & Iman', by='Shaykh Muhammad bin Jamil Zeno', ar='أركان الإسلام والإيمان',
               o1=None,
               o4='By Shaykh Muhammad bin Jamil Zeno.',
               o5='English hardcover. Darussalam.',
               end='English hardcover, Darussalam'),
    'ts': dict(kind='single', back=True, rtl=True,
               title='Tafsir as-Sa’di', by='Shaykh Abd ar-Rahman ibn Nasir as-Sa’di', ar='تيسير الكريم الرحمن',
               o1='Tafsir as-Sa’di in 1 volume.',
               o4='By Shaykh Abd ar-Rahman as-Sa’di.',
               o5='Arabic, one volume. Dar Ibn al-Jawzi.',
               end='Arabic, one volume, Dar Ibn al-Jawzi'),
    'fw': dict(kind='single', back=False, rtl=True,
               title='Al-Fawa’id', by='Imam Ibn Qayyim al-Jawziyyah', ar='الفوائد',
               o1=None,
               o4='By Imam Ibn Qayyim al-Jawziyyah.',
               o5='Arabic hardcover. Dar Ataat al-Ilm.',
               end='Arabic hardcover, Dar Ataat al-Ilm'),
    'fh': dict(kind='single', back=True, rtl=False,
               title='The Explanation of an-Nawawi’s Forty Hadith', by='Explained by Shaykh Dr. Saleh al-Fawzan',
               ar='المنحة الربانية',
               o1='An-Nawawi’s 40 Hadith, explained.',
               o4='Explained by Shaykh Dr. Saleh al-Fawzan.',
               o5='English leather hardcover. Dar Makkah International.',
               end='English leather hardcover, Dar Makkah International'),
    'sn': dict(kind='single', back=True, rtl=False,
               title='The Sealed Nectar', by='Shaykh Safiur-Rahman al-Mubarakpuri', ar='الرحيق المختوم',
               o1=None,
               o4='By Shaykh Safiur-Rahman al-Mubarakpuri.',
               o5='English hardcover. Darussalam.',
               end='English hardcover, Darussalam'),
    'sb': dict(kind='single', back=True, rtl=False,
               title='Summarized Sahih al-Bukhari', by='Translated by Dr. Muhammad Muhsin Khan', ar='مختصر صحيح البخاري',
               o1='Arabic and English in 1 volume.',
               o4='Translated by Dr. Muhammad Muhsin Khan.',
               o5='Arabic-English hardcover. Darussalam.',
               end='Arabic-English hardcover, Darussalam'),
}

# Opening motion in the first second: (start angle in degrees, start zoom, seconds to settle).
MOTION = {'O1': (38, 1.14, 1.0), 'O2': (38, 1.14, 1.0), 'O4': (38, 1.14, 1.0), 'O5': (38, 1.14, 1.0),
          'O3': (62, 1.30, 1.0), 'O6': (88, 1.36, 1.15)}
TITLE_IN = {'O3': 1.0, 'O6': 1.2}        # openings without a line bring the title in early
HOOK_OUT = 2.0


def openings_for(code):
    b = BOOKS_T[code]
    ops = ['O2', 'O3', 'O4', 'O5']
    if b.get('o1'):
        ops.insert(0, 'O1')
    if b['kind'] == 'set' or b.get('spine', True):
        ops.append('O6')
    return ops


def turn_box(front, spine, back):
    front = fit_h(front, FH)
    SW = 0
    if spine is not None:
        SW = round(clamp(spine.width / spine.height * FH, .05 * front.width, .32 * front.width))
        spine = spine.resize((SW, FH), Image.LANCZOS)
    back = back.resize((front.width, FH), Image.LANCZOS) if back is not None else front

    def box(fr, ang, top, scale):
        if spine is None:
            ang = 0
        a = ang % 360
        r = math.radians(a)
        fw = abs(math.cos(r)) * front.width
        sw = abs(math.sin(r)) * SW
        face = front if (a < 90 or a >= 270) else back
        parts = [(spine, sw), (face, fw)] if (a < 90 or 180 <= a < 270) else [(face, fw), (spine, sw)]
        parts = [p for p in parts if p[0] is not None]
        tot = sum(p[1] for p in parts) * scale
        x = W / 2 - tot / 2
        hh = round(FH * scale)
        s, pad = shadow_for((max(1, round(tot)), hh))
        fr.paste((0, 0, 0), (round(x) - pad, round(top) - pad), s)
        for img, w_ in parts:
            ww = round(w_ * scale)
            if ww >= 1:
                im = img.resize((ww, hh), Image.BILINEAR)
                k = .62 if img is spine else lerp(.6, 1, w_ / front.width)
                if k < .999:
                    im = ImageEnhance.Brightness(im).enhance(k)
                fr.paste(im, (round(x), round(top)))
            x += w_ * scale
    return box


def glint(img, g):
    if not 0 < g < 1:
        return img
    img = img.copy()
    gl = Image.new('L', img.size, 0)
    gx = lerp(img.width + 220, -220, g)
    ImageDraw.Draw(gl).polygon([(gx, 0), (gx + 130, 0), (gx - 90, img.height), (gx - 220, img.height)], fill=80)
    img.paste((255, 236, 200), (0, 0), gl.filter(ImageFilter.GaussianBlur(30)))
    return img


def reel(out_dir, reel_id, op, code):
    b = BOOKS_T[code]
    if op not in openings_for(code):
        raise SystemExit(f'{code} cannot use {op}. It can use: {", ".join(openings_for(code))}')
    a0, s0, T1 = MOTION[op]
    d = -1 if b['rtl'] else 1

    if b['kind'] == 'set':
        st = load(b['img'])
        h = max(960, round(st.height * 1040 / st.width))
        st = fit_h(st, h)

        def book(fr, t):
            k = ease_out(prog(t, 0, T1))
            z = lerp(1 + (s0 - 1) * 1.6, 1, k) * (1 + .06 * prog(t, 1, 7))
            pan = lerp(d * st.width * (.30 if op == 'O6' else .10), 0, k) + lerp(-16, 16, prog(t, 1, 7))
            img = glint(st, prog(t, 3.4, 4.4)) if t > 3 else (glint(st, prog(t, .15, 1.1)) if op == 'O3' else st)
            img = img.resize((round(img.width * z), round(img.height * z)), Image.BILINEAR)
            paste_book(fr, img, W / 2 + pan * z, TOP + img.height / 2 + 6 * math.sin(t * 1.6))
    else:
        has_spine, has_back = b.get('spine', True), b.get('back', False)
        box = turn_box(load(f'{code}_front.jpg'),
                       load(f'{code}_spine.jpg') if has_spine else None,
                       load(f'{code}_back.jpg') if has_back else None)

        def book(fr, t):
            k = ease_out(prog(t, 0, T1))
            ang = a0 * (1 - k)
            sc = lerp(s0, 1, k) * (1 + .05 * prog(t, 1, 7))
            if has_back:
                ang += lerp(0, 360, ease_io(prog(t, 3.4, 6.4)))
            else:
                ang += lerp(0, 55, ease_io(prog(t, 3.4, 4.4))) * (1 - ease_io(prog(t, 5.2, 6.2)))
            ang += 7 * math.sin((t - 1) * 1.7) * prog(t, 1.0, 1.5) * (1 - prog(t, 3.0, 3.4))   # never still
            if not has_spine:
                sc *= 1 + .03 * math.sin(t * 1.9)
            box(fr, d * ang, TOP + 8 * math.sin(t * 1.6), sc)

    line = {'O1': b.get('o1'), 'O4': b['o4'], 'O5': b['o5']}.get(op)
    t_title = TITLE_IN.get(op, HOOK_OUT + .2)
    BAND0, BAND1 = 304, 650                      # text lives between these two lines, above the book

    ts_, _, th_ = fit_text(b['title'], 'InterDisplay-ExtraBold.otf', (84, 76, 68, 60, 54, 48), 960, 3, max_h=BAND1 - BAND0 - 70)
    bs_, _, bh_ = fit_text(b['by'], 'Inter-Medium.otf', (42, 38), 940, 2)
    y_title = BAND0 + max(0, (BAND1 - BAND0 - th_ - 14 - bh_) / 2)

    def draw(fr, t):
        book(fr, t)
        out_a = 1 - prog(t, HOOK_OUT, HOOK_OUT + .25)
        if line and out_a > 0:
            s, _, hh = fit_text(line, 'InterDisplay-ExtraBold.otf', (112, 100, 92, 84, 76, 68, 60), 940, 3, max_h=BAND1 - BAND0)
            text_block(fr, line, 'InterDisplay-ExtraBold.otf', s, BAND0 + (BAND1 - BAND0 - hh) / 2,
                       alpha=out_a, stagger=(t + .16, .07), gold_digits=True)
        elif op == 'O2' and out_a > 0:
            if b.get('ar'):
                s, _, hh = fit_text(b['title'], 'InterDisplay-Bold.otf', (56, 50, 44), 940, 2)
                y2 = arabic_line(fr, b['ar'], BAND0 + 20, t, HOOK_OUT)
                text_block(fr, b['title'], 'InterDisplay-Bold.otf', s, min(y2 + 44, BAND1 - hh),
                           alpha=ease_out(prog(t, -.05, .3)) * out_a)
            else:
                s, _, hh = fit_text(b['title'], 'InterDisplay-ExtraBold.otf', (100, 92, 84, 76, 68, 60), 960, 3, max_h=BAND1 - BAND0)
                text_block(fr, b['title'], 'InterDisplay-ExtraBold.otf', s, BAND0 + (BAND1 - BAND0 - hh) / 2,
                           color=GOLD, alpha=out_a, stagger=(t + .16, .06))
        a = ease_out(prog(t, t_title, t_title + .4)) * (1 - prog(t, 6.8, 7.0))
        if a > 0:
            yy = text_block(fr, b['title'], 'InterDisplay-ExtraBold.otf', ts_, y_title, alpha=a, rise=(1 - a) * 22, maxw=960)
            text_block(fr, b['by'], 'Inter-Medium.otf', bs_, yy + 14, color=MUTE, alpha=a)
        end_card(fr, t, 7.0, b['end'], 'daralathari.com')

    return render(out_dir, reel_id, DUR, draw)


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == '--list':
        for c, b in BOOKS_T.items():
            print(f"{c:5} {'set' if b['kind'] == 'set' else 'book':4} {' '.join(openings_for(c)):18} {b['title']}")
        sys.exit(0)
    for job in sys.argv[2:]:
        rid, op, code = job.split(':')
        reel(sys.argv[1], f"{rid}_{op}_{code.replace('_', '')}", op, code)
