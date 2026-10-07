/* The Book of Knowledge — promo film. seek(t) is a pure function of t (seconds). */
(function () {
  const DURATION = 57;
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, x) => a + (b - a) * x;
  const ss = (a, b, t) => { const x = clamp((t - a) / (b - a)); return x * x * (3 - 2 * x); };
  const E = {
    io: x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    out: x => 1 - Math.pow(1 - x, 3),
    lin: x => x,
  };
  // piecewise track: keys [[t, v, ease?]], ease applies to the segment that starts at the key
  function track(t, keys) {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 0; i < keys.length - 1; i++) {
      const [t0, v0, e] = keys[i], [t1, v1] = keys[i + 1];
      if (t < t1) return lerp(v0, v1, (e || E.io)(clamp((t - t0) / (t1 - t0))));
    }
    return keys[keys.length - 1][1];
  }
  const fade = (t, i0, i1, o0, o1) => ss(i0, i1, t) * (1 - ss(o0, o1, t));

  const stage = document.getElementById('stage');
  const mk = (cls, css, parent, tag = 'div') => {
    const d = document.createElement(tag); d.className = cls;
    if (css) Object.assign(d.style, css); (parent || stage).appendChild(d); return d;
  };

  // ---------- background motes ----------
  const motes = [];
  for (let i = 0; i < 38; i++) {
    const r = (n) => { const x = Math.sin(i * 127.1 + n * 311.7) * 43758.5453; return x - Math.floor(x); };
    const sz = 5 + r(1) * 13;
    motes.push({ el: mk('mote', { width: sz + 'px', height: sz + 'px' }, document.getElementById('motes')), x: r(2) * 1080, y: r(3) * 1920, sp: 8 + r(4) * 22, ph: r(5) * 6.28, a: .2 + r(6) * .5 });
  }

  // ---------- books ----------
  const HL = {
    en: [[0.13526, 0.62374, 0.82058, 0.64898], [0.13686, 0.65066, 0.68996, 0.67828]],
    ar: [[0.44885, 0.53423, 0.83160, 0.56164]],
  };
  function Book(c) {
    const { W, H, D, dir } = c;
    const wrap = mk('p3d', null, document.getElementById('books'));
    const R = mk('book', null, wrap);
    const img = u => ({ backgroundImage: `url(${u})` });
    const paper = '#e8dcc3';
    const face = (w, h, tf, css, parent) => mk('face', Object.assign({ width: w + 'px', height: h + 'px', left: -w / 2 + 'px', top: -h / 2 + 'px', transform: tf }, css), parent || R);
    // cube faces
    face(W, H, `rotateY(180deg) translateZ(${D / 2}px)`, img(c.back));
    face(D, H, `rotateY(${dir * 90}deg) translateZ(${W / 2}px)`, img(c.spine));
    face(D, H, `rotateY(${-dir * 90}deg) translateZ(${W / 2}px)`, { background: `repeating-linear-gradient(90deg,#efe5cf 0 2px,#cdbf9f 2px 3px)`, filter: 'brightness(.8)' });
    const edge = { background: `repeating-linear-gradient(180deg,#efe5cf 0 2px,#cdbf9f 2px 3px)` };
    face(W, D, `rotateX(90deg) translateZ(${H / 2}px)`, Object.assign({ filter: 'brightness(.95)' }, edge));
    face(W, D, `rotateX(-90deg) translateZ(${H / 2}px)`, Object.assign({ filter: 'brightness(.7)' }, edge));

    const zh = D / 2 - 12;
    const hx = dir < 0 ? -W / 2 : W / 2;
    const gA = dir < 0 ? '90deg' : '270deg', gB = dir < 0 ? '270deg' : '90deg';
    const gut = a => `linear-gradient(${a},rgba(70,45,20,.34),rgba(70,45,20,0) 16%),`;
    const leaf = (o, lw, lh, top, frontCss, backCss) => {
      const hinge = mk('hinge', { left: hx + 'px', top: -H / 2 + 'px', height: H + 'px' }, R);
      const lf = mk('leaf', { width: lw + 'px', height: lh + 'px', left: (dir < 0 ? 0 : -lw) + 'px', top: top + 'px', transform: `translateZ(${o}px)` }, hinge);
      const f = mk('face', Object.assign({ width: lw + 'px', height: lh + 'px', left: '0', top: '0', transform: 'translateZ(1px)' }, frontCss), lf);
      mk('face', Object.assign({ width: lw + 'px', height: lh + 'px', left: '0', top: '0', transform: 'rotateY(180deg) translateZ(1px)' }, backCss), lf);
      return { hinge, f };
    };
    // page plane (the photographed page) at the front of the page block
    const pl = mk('plane', {
      width: c.pw + 'px', height: c.ph + 'px', left: (dir < 0 ? -W / 2 : W / 2 - c.pw) + 'px', top: -c.ph / 2 + 'px',
      transform: `translateZ(${zh}px)`, backgroundImage: `url(${c.page})`, backgroundSize: '100% 100%'
    }, R);
    mk('plane', { inset: '0', background: `linear-gradient(${gA},rgba(60,38,16,.38),rgba(60,38,16,0) 22%)` }, pl);
    const hls = HL[c.id].map(([x0, y0, x1, y1]) => {
      const e = mk('hl', { left: x0 * c.pw + 'px', top: y0 * c.ph - 4 + 'px', width: (x1 - x0) * c.pw + 'px', height: (y1 - y0) * c.ph + 8 + 'px', transformOrigin: dir < 0 ? '0 50%' : '100% 50%', transform: 'scaleX(0)' }, pl);
      return { e, box: [x0, y0, x1, y1] };
    });
    // sheets (flip) and cover
    const sheets = [];
    for (let i = 0; i < 4; i++) {
      sheets.push(leaf(8 - i * 2, c.pw, c.ph, (H - c.ph) / 2,
        { background: gut(gA) + paper }, { background: gut(gB) + paper }));
    }
    const cover = leaf(12, W, H, 0, img(c.front), { background: gut(gB) + c.endpaper });
    const gloss = mk('gloss', null, cover.f);
    return { c, wrap, R, cover, sheets, hls, gloss, pl };
  }
  const EN = Book({ id: 'en', W: 1200, H: 1800, D: 190, dir: -1, pw: 1170, ph: 1740, front: 'assets/photos/en-front.jpg', back: 'assets/photos/en-back.jpg', spine: 'assets/photos/en-spine.jpg', page: 'assets/photos/en-page-definition.jpg', endpaper: '#e9dcc0' });
  const AR = Book({ id: 'ar', W: 1200, H: 1760, D: 165, dir: 1, pw: 1170, ph: 1700, front: 'assets/photos/ar-front.jpg', back: 'assets/photos/ar-back.jpg', spine: 'assets/photos/ar-spine.jpg', page: 'assets/photos/ar-page-definition.jpg', endpaper: '#d9cba8' });

  // focus points (book-local coords) for the page zooms
  const bbox = (hl) => [Math.min(...hl.map(h => h[0])), Math.min(...hl.map(h => h[1])), Math.max(...hl.map(h => h[2])), Math.max(...hl.map(h => h[3]))];
  const bE = bbox(HL.en), bA = bbox(HL.ar);
  const FE = { x: -600 + (bE[0] + bE[2]) / 2 * 1170, y: -870 + (bE[1] + bE[3]) / 2 * 1740 };
  const FA = { x: 600 - 1170 + (bA[0] + bA[2]) / 2 * 1170, y: -850 + (bA[1] + bA[3]) / 2 * 1700 };

  const flipT = (b0, i) => b0 + i * 0.3;
  function poseBook(B, t, P) {
    const W = B.c.W, dir = B.c.dir;
    const op = track(t, P.op);
    B.wrap.style.display = op <= 0.002 ? 'none' : 'block';
    B.wrap.style.opacity = op;
    if (op <= 0.002) return;
    const idle = P.idle(t);
    const x = track(t, P.x), y = track(t, P.y) + 7 * Math.sin(t * 1.1 + (dir > 0 ? 1 : 0)) * idle, z = track(t, P.z || [[0, 0]]);
    const rx = track(t, P.rx), ry = track(t, P.ry) + 2.6 * Math.sin(t * 1.3 + (dir > 0 ? 2 : 0)) * idle, s = track(t, P.s);
    const fx = track(t, P.fx), fy = track(t, P.fy || [[0, 0]]);
    B.R.style.transform = `translate3d(${x}px,${y}px,${z}px) rotateX(${rx}deg) rotateY(${ry}deg) scale(${s}) translate3d(${-fx}px,${-fy}px,0)`;
    const ca = track(t, P.cover) * 180;
    B.cover.hinge.style.transform = `translateZ(${B.c.D / 2 - 12}px) rotateY(${dir * ca}deg)`;
    B.sheets.forEach((sh, i) => {
      const a = track(t, [[P.flip0 + i * 0.3, 0], [P.flip0 + i * 0.3 + 0.55, 1], [P.hide, 1], [P.hide + .1, 0]]) * 180;
      sh.hinge.style.transform = `translateZ(${B.c.D / 2 - 12}px) rotateY(${dir * a}deg)`;
    });
    B.gloss.style.backgroundPosition = `${lerp(100, -100, ss(P.gl0, P.gl0 + 2.0, t))}% 0`;
    B.hls.forEach((h, i) => {
      const [a, b] = P.hl[i];
      const p = ss(a, b, t);
      h.e.style.transform = `scaleX(${p})`;
      h.e.style.opacity = p > 0 ? 1 : 0;
    });
  }

  const idleEntrance = t => (t > 9.7 && t < 15.6) || (t > 16.5 && t < 19.3) || (t > 51.4 && t < 52.8) ? 1 : 0;
  const PE = {
    op: [[7, 0], [7.35, 1], [30.0, 1], [30.9, 0], [49.6, 0], [50, 1], [52.6, 1], [53.3, 0]],
    x: [[7, 760], [19.4, 760], [20.7, 540], [30.0, 540], [30.9, 1500], [49.6, 1500], [52.1, 760, E.out]],
    y: [[7, 1250], [9.7, 900, E.out], [15.6, 900], [16.5, 1190], [19.4, 1190], [20.7, 880], [30.0, 880], [30.9, 700], [49.6, 700], [51.4, 950]],
    z: [[7, -2000], [9.7, 0, E.out], [52.6, 0], [53.4, -1200]],
    s: [[7, .33], [15.6, .33], [16.5, .3], [19.4, .3], [20.7, .42], [24, .42], [26.3, 1.17], [30.0, 1.17], [30.9, .3], [49.6, .3], [51.4, .33]],
    rx: [[7, 8], [9.7, 6, E.out], [19.4, 6], [20.7, 14], [22.7, 10], [24, 10], [26.3, 0], [30, 0], [30.9, 10], [52, 6]],
    ry: [[7, 112], [9.7, -16, E.out], [19.4, -16], [20.7, 0], [26.3, 0], [30, 0], [30.9, -35], [49.6, -35], [51.4, -16], [52.6, -16]],
    fx: [[0, 0], [20.8, 0], [22.7, -600], [24, -600], [26.3, FE.x], [30, FE.x], [30.9, 0]],
    fy: [[0, 0], [24, 0], [26.3, FE.y], [30, FE.y], [30.9, 0]],
    cover: [[20.8, 0], [22.7, 1], [30.9, 1], [31.0, 0]],
    flip0: 22.35, hide: 30.9, gl0: 9.5, hl: [[26.6, 27.7], [27.6, 28.4]], idle: idleEntrance,
  };
  const PA = {
    op: [[7, 0], [7.35, 1], [20.2, 1], [20.5, 0], [30.5, 0], [30.9, 1], [38.3, 1], [38.8, 0], [49.6, 0], [50, 1], [52.6, 1], [53.3, 0]],
    x: [[7, 290], [19.4, 290], [20.4, -520], [30.4, -520], [31.7, 540, E.out], [38.1, 540], [38.9, -600], [49.6, -600], [51.4, 290, E.out]],
    y: [[7, 1250], [9.7, 900, E.out], [15.6, 900], [16.5, 1190], [19.4, 1190], [30.4, 880], [38.1, 880], [38.9, 700], [49.6, 700], [51.4, 950]],
    z: [[7, -2000], [9.7, 0, E.out], [52.6, 0], [53.4, -1200]],
    s: [[7, .33], [15.6, .33], [16.5, .3], [19.4, .3], [30.4, .42], [34.7, .42], [36.4, 1.9], [38.1, 1.9], [38.9, .3], [49.6, .3], [51.4, .33]],
    rx: [[7, 8], [9.7, 6, E.out], [19.4, 6], [30.4, 14], [31.8, 14], [33.6, 10], [34.7, 10], [36.4, 0], [38.1, 0], [38.9, 10], [52, 6]],
    ry: [[7, -112], [9.7, 16, E.out], [19.4, 16], [20.4, 40], [30.5, -10], [31.7, 0], [38.1, 0], [38.9, 35], [49.6, 35], [51.4, 16], [52.6, 16]],
    fx: [[0, 0], [31.8, 0], [33.6, 600], [34.7, 600], [36.4, FA.x], [38.1, FA.x], [38.9, 0]],
    fy: [[0, 0], [34.7, 0], [36.4, FA.y], [38.1, FA.y], [38.9, 0]],
    cover: [[31.8, 0], [33.6, 1], [38.8, 1], [38.9, 0]],
    flip0: 33.3, hide: 38.8, gl0: 9.5, hl: [[36.5, 37.6]], idle: idleEntrance,
  };

  // ---------- text ----------
  const texts = [];
  const tx = (html, cls, y, size, spec, extra) => {
    const el = mk('t ' + cls, Object.assign({ top: y + 'px', fontSize: size + 'px', transform: 'translateY(-50%)' }, extra || {}), document.getElementById('texts'));
    el.innerHTML = html; texts.push(Object.assign({ el, rise: 26 }, spec)); return el;
  };
  const AR_H1 = '«مَنْ يُرِدِ اللهُ بِهِ خَيْرًا يُفَقِّهْهُ فِي الدِّينِ»';
  const AR_H2 = '«إِنَّ الأَنْبِيَاءَ لَمْ يُورِّثُوا دِينَارًا وَلَا دِرْهَمًا، وَإِنَّمَا وَرَّثُوا الْعِلْمَ، فَمَنْ أَخَذَهُ أَخَذَ بِحَظٍّ وَافِرٍ»';
  // 1 hook
  tx('Before you seek knowledge,', 'en it', 610, 78, { i: [0.1, 0.8], o: [3.0, 3.4] });
  tx('learn <b>how</b> to seek it.', 'en gold', 770, 100, { i: [0.7, 1.5], o: [3.0, 3.4], rise: 34 }, { fontWeight: 600 });
  // 2 problem
  tx('Everyone wants to seek knowledge.', 'en', 600, 70, { i: [3.6, 4.3], o: [6.9, 7.4] });
  tx('Few know how to begin,', 'en it', 800, 70, { i: [4.9, 5.6], o: [6.9, 7.4] });
  tx('or how to carry it.', 'en gold', 930, 82, { i: [5.9, 6.6], o: [6.9, 7.4] }, { fontWeight: 600 });
  // 3 titles
  tx('كتاب العلم', 'ar gold', 285, 124, { i: [10.3, 11.1], o: [15.2, 15.7] });
  tx('The Book of Knowledge', 'en', 440, 80, { i: [10.6, 11.4], o: [15.2, 15.7] }, { fontWeight: 600 });
  const lab = (h, x) => tx(h, 'en caps gold', 1272, 27, { i: [11.2, 11.9], o: [15.2, 15.7], rise: 14 }, { left: x - 235 + 'px', width: '470px', whiteSpace: 'nowrap', fontSize: '25px', letterSpacing: '.1em' });
  lab('The Arabic original', 290); lab('The English translation', 742);
  tx('Shaykh Muhammad ibn Salih al-Uthaymeen <span style="opacity:.75">(d. 1421H)</span>', 'en', 1415, 37, { i: [12.6, 13.4], o: [15.2, 15.7] }, { left: '20px', width: '900px', whiteSpace: 'nowrap' });
  // 4 pillars
  tx('In this book, Shaykh Ibn Uthaymeen explains', 'en it', 300, 48, { i: [16.1, 16.8], o: [19.0, 19.4] });
  tx('the <b>definition</b> and <b>virtue</b> of knowledge', 'en', 470, 56, { i: [16.6, 17.3], o: [19.0, 19.4] }, { left: '20px', width: '900px' });
  tx('the <b>manners</b> a student needs', 'en', 650, 56, { i: [17.4, 18.1], o: [19.0, 19.4] });
  tx('the <b>way</b> to seek it properly', 'en', 830, 56, { i: [18.2, 18.9], o: [19.0, 19.4] });
  // 5/6 page scenes
  const panel = (inner, y, spec, extra) => tx(inner, 'en panel', y, 36, spec, Object.assign({ left: '95px', width: '760px' }, extra || {}));
  panel('<span class="gold caps" style="font-size:26px">English translation · page 21</span><br>Section One: The Definition of Knowledge', 262, { i: [24.2, 24.9], o: [30.0, 30.4], rise: 12 });
  panel('Reported by <b>al-Bukhārī</b> (no. 71) and <b>Muslim</b> (no. 1037)', 1440, { i: [27.9, 28.6], o: [30.0, 30.4], rise: 12 }, { fontSize: '34px' });
  panel('<span class="gold caps" style="font-size:26px">The Arabic original · page 17</span><br><span class="ar" style="font-size:44px;line-height:1.5">تَعْرِيفُ العِلْمِ</span>', 262, { i: [34.7, 35.4], o: [38.1, 38.5], rise: 12 });
  panel('al-Bukhārī 71 · Muslim 1037', 1440, { i: [37.7, 38.2], o: [38.1, 38.5], rise: 12 }, { fontSize: '34px' });
  // 7 quote 1
  tx(AR_H1, 'ar', 575, 78, { i: [38.9, 39.8], o: [43.4, 43.9] }, { color: '#f4e7c8' });
  tx('“Whoever Allāh wants good for, He grants him understanding in the religion.”', 'en it', 905, 62, { i: [40.2, 41.0], o: [43.4, 43.9] });
  tx('al-Bukhārī 71 · Muslim 1037', 'en caps gold', 1165, 32, { i: [41.2, 41.9], o: [43.4, 43.9], rise: 12 });
  // 8 quote 2
  tx(AR_H2, 'ar', 520, 64, { i: [44.2, 45.2], o: [49.0, 49.6] }, { color: '#f4e7c8' });
  tx('“Indeed, the Prophets did not leave behind dīnars nor dirhams; rather, they only left behind knowledge. So whosoever takes it has indeed taken an abundant portion.”', 'en it', 960, 50, { i: [45.8, 46.7], o: [49.0, 49.6] });
  tx('Aḥmad · Abū Dāwūd 3641 · at-Tirmidhī 2682 · Ibn Mājah 223', 'en caps gold', 1265, 27, { i: [47.0, 47.7], o: [49.0, 49.6], rise: 12 });
  // 9 closing
  tx('It is the book to read', 'en it', 330, 70, { i: [50.0, 50.7], o: [52.5, 53.0] });
  tx('before you start any other.', 'en gold', 460, 76, { i: [50.7, 51.5], o: [52.5, 53.0] }, { fontWeight: 600 });
  // end
  tx('daralathari.com', 'en gold', 1250, 66, { i: [54.6, 55.5], o: [99, 100] }, { fontWeight: 600, letterSpacing: '.04em' });

  // ---------- gold thread (svg) ----------
  const svg = document.getElementById('thread');
  const threads = [];
  const th = (d, i, o) => { const p = document.createElementNS('http://www.w3.org/2000/svg', 'path'); p.setAttribute('d', d); p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 1'; svg.appendChild(p); threads.push({ p, i, o }); };
  th('M120 850 C 300 880, 520 825, 835 855', [1.3, 2.4], [3.0, 3.4]);
  th('M140 1010 C 300 1030, 480 990, 740 1015', [6.2, 7.0], [6.9, 7.4]);
  th('M120 1335 C 330 1318, 640 1352, 880 1332', [12.0, 13.0], [15.2, 15.7]);
  th('M300 565 H 650', [17.0, 17.5], [19.0, 19.4]);
  th('M300 740 H 650', [17.8, 18.3], [19.0, 19.4]);
  th('M250 1068 H 700', [40.9, 41.6], [43.4, 43.9]);
  th('M250 1175 H 700', [46.2, 46.9], [49.0, 49.6]);
  th('M180 600 H 820', [51.2, 52.0], [52.5, 53.0]);
  th('M220 1150 L 220 720 C 220 560, 390 470, 540 330 C 690 470, 860 560, 860 720 L 860 1150', [53.2, 54.7], [99, 100]);

  // ---------- logo ----------
  const logo = mk('', null, stage, 'img'); logo.id = 'logo'; logo.src = 'assets/logo.png';

  const glow = document.getElementById('glow'), vig = document.getElementById('vig');
  const idEl = id => document.getElementById(id);

  function seek(t) {
    // background + motes
    motes.forEach(m => {
      const y = ((m.y - t * m.sp) % 1920 + 1920) % 1920, x = m.x + 26 * Math.sin(t * .4 + m.ph);
      m.el.style.transform = `translate(${x}px,${y}px)`;
      m.el.style.opacity = m.a * (.6 + .4 * Math.sin(t * .9 + m.ph));
    });
    glow.style.opacity = (fade(t, 6.5, 8.5, 15.8, 16.8) + .5 * fade(t, 49.5, 51, 52.4, 53.4) + .35 * ss(52.8, 54, t)).toFixed(3);
    vig.style.opacity = 1;
    // books
    poseBook(EN, t, PE); poseBook(AR, t, PA);
    // text
    texts.forEach(x => {
      const o = fade(t, x.i[0], x.i[1], x.o[0], x.o[1]);
      x.el.style.opacity = o;
      x.el.style.display = o <= 0.001 ? 'none' : 'block';
      x.el.style.transform = `translateY(calc(-50% + ${(1 - ss(x.i[0], x.i[1], t)) * x.rise}px))`;
    });
    // thread
    threads.forEach(h => {
      const p = ss(h.i[0], h.i[1], t), o = 1 - ss(h.o[0], h.o[1], t);
      h.p.style.strokeDashoffset = 1 - p; h.p.style.opacity = p > 0 ? o : 0;
    });
    // logo
    logo.style.opacity = ss(53.9, 54.9, t);
    logo.style.transform = `scale(${lerp(.94, 1, ss(53.9, 56, t))})`;
    logo.style.display = t < 53.8 ? 'none' : 'block';
  }
  window.seek = seek; window.DURATION = DURATION;
  // report text elements that leave the safe zone (top 10%, bottom 20%, right 12%)
  window.auditSafe = function (t) {
    seek(t); const bad = [];
    texts.forEach(x => {
      if (parseFloat(x.el.style.opacity) < .05) return;
      const r = x.el.getBoundingClientRect(); const kids = x.el.querySelectorAll('*');
      // measure actual text extent
      const rg = document.createRange(); rg.selectNodeContents(x.el); const b = rg.getBoundingClientRect();
      if (b.top < 192 || b.bottom > 1536 || b.right > 950 || b.left < 0) bad.push([x.el.textContent.slice(0, 30), Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]);
    });
    return bad;
  };
  window.READY = Promise.all([
    document.fonts.load('600 40px CG'), document.fonts.load('italic 500 40px CG'), document.fonts.load('500 40px CG'), document.fonts.load('700 40px AM'), document.fonts.load('400 40px AM'),
    ...Array.from(document.images).map(i => i.decode().catch(() => {})),
    ...['en-front', 'en-back', 'en-spine', 'en-page-definition', 'ar-front', 'ar-back', 'ar-spine', 'ar-page-definition'].map(n => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = `assets/photos/${n}.jpg`; })),
  ]).then(() => document.fonts.ready).then(() => seek(0));
})();
