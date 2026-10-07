const STORE = "https://daralathari.com";
const COLORS = ["#7A2E2A", "#1F3B34", "#B07A1E", "#2B3A55", "#4A2F4F", "#33403A", "#8A4B2A", "#1E2F6B"];
const AR = {Aqeedah:"عقيدة", Hadith:"حديث", Fiqh:"فقه", Tafsir:"تفسير", Seerah:"سيرة", "Duas & Heart":"أذكار", Clothing:"لباس"};
// Snapshot of in-stock items from daralathari.com (7 Oct 2026). v = variant id for cart links; pick = size/colour must be chosen on the product page.
const BOOKS = [
  {t:"Kitab At-Tauhid (The Book of Monotheism)",s:"Kitab At-Tauhid",c:"Aqeedah",p:17.99,n:21,h:"kitab-at-tauhid-the-book-of-monotheism",v:41782826926151,w:44,hh:250},
  {t:"Commentary on the Three Fundamental Principles of Islam",s:"Three Fundamental Principles",c:"Aqeedah",p:19.99,n:28,h:"explanation-of-the-three-fundamental-principles-of-islam-shaykh-muhammad-ibn-saalih-al-uthaymeen",v:41780125630535,w:40,hh:225},
  {t:"The Book of Tawheed (Fawzan)",s:"Book of Tawheed",c:"Aqeedah",p:17,n:6,h:"the-book-of-tawheed-fawzan",v:42060204474439,w:40,hh:235},
  {t:"I’aanatul Mustafid bi Sharh Kitaab At-Tawheed",s:"I’aanatul Mustafid",c:"Aqeedah",p:45,n:9,h:"i-aanatul-mustafid-bi-sharh-kitaab-at-tawheed-sheikh-saleh-fawzan-إعانة-المستفيد-بشرح-كتاب-التوحيد",v:42554359152711,w:60,hh:285},
  {t:"Commentary on Kitab At Tawheed by Salih Al-‘Uthaimeen (2 Vol.)",s:"Kitab At Tawheed, 2 Vol.",c:"Aqeedah",p:50,n:6,h:"commentary-on-kitab-at-tawheed-by-salih-al-uthaimeen-2-volume-set",v:41842389123143,w:54,hh:270},
  {t:"An Explanation of Kitab al-Tawhid by Shaykh al-Sa'di",c:"Aqeedah",p:22.5,n:3,h:"an-explanation-of-kitab-al-tawhid-by-shaykh-al-sadi",v:41836190597191},
  {t:"Fath ul Majeed (Darussalam)",c:"Aqeedah",p:24,n:5,h:"fathul-majeed-darussalam-فتح-المجيد-شرح-كتاب-التوحيد",v:41974145515591},
  {t:"The Four Fundamental Principles Explained by Shaykh Fawzan",c:"Aqeedah",p:7,n:4,h:"the-four-fundamental-principles-explained-by-shaykh-fawzan",v:42305203535943},
  {t:"The Pillars of Islam and Iman",c:"Aqeedah",p:17,n:14,h:"the-pillars-of-islam-and-iman",v:41836190695495},
  {t:"A Summary of the Creed of Salaf Saalih",c:"Aqeedah",p:4,n:40,h:"a-summary-of-the-creed-of-salaf-saalih",v:41782935814215},
  {t:"Sharh as Sunnah, Imam al-Barbahari (2 Vol., Leather)",c:"Aqeedah",p:70,n:1,h:"sharh-as-sunnah-imam-al-barbahari-2-vol-set",v:41951665258567},
  {t:"The Crime of Tamayyu’ upon the Salafi Manhaj",c:"Aqeedah",p:12.5,n:2,h:"the-crime-of-tamayyu-upon-the-salafi-manhaj",v:41842333319239},
  {t:"Bulugh Al Maram",s:"Bulugh Al Maram",c:"Hadith",p:25.99,n:3,h:"bulugh-al-maram",v:41791891963975,w:46,hh:245},
  {t:"40 Hadith of An-Nawawi, Explained by Sheikh Fawzan (Leather)",s:"40 Hadith of An-Nawawi",c:"Hadith",p:34,n:13,h:"40-hadith-of-an-nawawi-explanation-sheikh-fawzan",v:41779256721479,w:38,hh:215},
  {t:"Fiqh According to the Qur’an and Sunnah (Vols. 1 & 2)",s:"Fiqh, Qur’an & Sunnah",c:"Fiqh",p:44.99,n:6,h:"fiqh-according-to-the-qur-an-and-sunnah-volumes-1-2",v:41805176176711,w:58,hh:280},
  {t:"The Description of Salah, Sheikh Salih al-Uthaymeen",c:"Fiqh",p:22,n:4,h:"the-description-of-salah-the-prayer-by-sheikh-salih-al-uthaymeen",v:41932841582663},
  {t:"Tafsir Ibn Kathir, 10 Volume",s:"Tafsir Ibn Kathir",c:"Tafsir",p:240,n:4,h:"tafsir-ibn-kathir-10-volume",v:41842399969351,w:66,hh:300},
  {t:"Tafsir As Sadi, 10 Volume",c:"Tafsir",p:240,n:2,h:"tafsir-as-sadi-10-volume",v:42060175179847},
  {t:"Stories of the Prophets",s:"Stories of the Prophets",c:"Seerah",p:24,n:3,h:"stories-of-the-prophets",v:41951666733127,w:50,hh:260,pick:true},
  {t:"When The Moon Split",c:"Seerah",p:25,n:1,h:"when-the-moon-split",v:42060056592455},
  {t:"Great Women of Islam",c:"Seerah",p:19,n:1,h:"great-women-of-islam",v:42060047351879},
  {t:"The Disease & The Cure, Imam Ibn al-Qayyim",s:"The Disease & The Cure",c:"Duas & Heart",p:60,n:7,h:"the-disease-the-cure-by-imam-ibn-al-qayyim-revised-second-edition",v:41836204195911,w:56,hh:270},
  {t:"Fortress Of The Muslim",c:"Duas & Heart",p:4,n:36,h:"fortress-of-the-muslim",v:41842406031431},
  {t:"Dar Al Athari Saudi Thobe (White)",c:"Clothing",p:45,n:37,h:"white-dar-al-athari-saudi-thobe",pick:true},
  {t:"Dar Al Athari Saudi Thobe (Black)",c:"Clothing",p:49.99,n:26,h:"black-dar-al-athari-saudi-thobe",pick:true},
  {t:"Classic Red Saudi Shemagh",c:"Clothing",p:25,n:2,h:"classic-red-white-saudi-shemagh",v:42428031402055},
  {t:"Pristine White Yemeni Shemagh",c:"Clothing",p:25,n:3,h:"pristine-white-yemeni-shemagh",v:42428144713799},
  {t:"Royal Navy Blue Yemeni Shemagh",c:"Clothing",p:25,n:1,h:"royal-navy-yemeni-shemagh",v:42428145762375},
  {t:"An-Nur Collection (shemagh)",c:"Clothing",p:25,n:4,h:"an-nur-collection",pick:true}
].map((b, i) => ({...b, id: i + 1, ar: AR[b.c], no: b.n}));
const SHELF = BOOKS.filter(b => b.w).map(b => ({...b, h: b.hh}));
const COLLECTIONS = [
  ["Aqeedah","aqeedah",126],["Books for beginners","books-for-beginners",25],["Arabic books","arabic-books-books-in-arabic",83],
  ["Fiqh","fiqh",20],["Hadith","hadith",17],["Thobes, shemaghs and kufis","thobes-shemaghs-kufis",28],
  ["Limited edition shemaghs","limited-edition-shemaghs",17],["Bundles and deals","bundles-deals",6],["Damaged books, 25–40% off","damaged-books-25-40-off",20]
];
const $ = s => document.querySelector(s);
const money = n => "$" + n.toFixed(2);
const safe = f => { try { return f(); } catch { return null; } };
const color = b => COLORS[(b.id - 1) % COLORS.length];
const url = b => STORE + "/products/" + encodeURIComponent(b.h);
let cart = safe(() => JSON.parse(localStorage.getItem("cart2"))) || {};
let cat = "All";

// Fallback CSS shelf (hidden when WebGL is available)
$("#shelf").innerHTML = SHELF.map((b, i) =>
  `<a class="spine" href="#catalogue" data-find="${b.id}" style="background:${color(b)};width:${b.w}px;height:${b.h}px" title="${b.t}"><i lang="ar">${b.ar}</i>${b.s || b.t}</a>` +
  (i % 3 === 1 ? `<span class="spine blank" aria-hidden="true" style="background:${COLORS[(i + 3) % COLORS.length]};width:${24 + i * 3}px;height:${170 + i * 9}px"></span>` : "")
).join("");
$("#shelf").onclick = e => { const a = e.target.closest("[data-find]"); if (!a) return;
  e.preventDefault(); cat = "All"; $("#search").value = a.title; syncTabs(); render(); $("#catalogue").scrollIntoView({behavior:"smooth"}); };

// Catalogue
const cats = ["All", ...new Set(BOOKS.map(b => b.c))];
$("#tabs").innerHTML = cats.map(c => `<button class="tab" role="tab" data-c="${c}" aria-selected="${c === "All"}">${c}</button>`).join("");
function syncTabs() { document.querySelectorAll(".tab").forEach(x => x.setAttribute("aria-selected", x.dataset.c === cat)); }
function render() {
  const q = $("#search").value.toLowerCase(), s = $("#sort").value;
  const list = BOOKS.filter(b => (cat === "All" || b.c === cat) && b.t.toLowerCase().includes(q));
  if (s) list.sort((x, y) => s === "asc" ? x.p - y.p : y.p - x.p);
  $("#ledger").innerHTML = list.map(b => `
    <li class="row">
      <div class="thumb" lang="ar" style="background:${color(b)}">${b.ar}</div>
      <div class="ttl"><b><a href="${url(b)}" target="_blank" rel="noopener">${b.t}</a></b></div>
      <div class="cat">${b.c}</div>
      <div class="fmt">${b.n <= 3 ? "Last " + b.n + " in stock" : b.n + " in stock"}</div>
      <div class="price">${b.pick ? "from " : ""}${money(b.p)}</div>
      ${b.v && !b.pick ? `<button class="add" data-id="${b.id}" type="button">Add</button>` : `<a class="add" href="${url(b)}" target="_blank" rel="noopener">Choose</a>`}
    </li>`).join("");
  $("#empty").hidden = list.length > 0;
}
$("#tabs").onclick = e => { const c = e.target.dataset.c; if (!c) return; cat = c; syncTabs(); render(); };
$("#search").oninput = render; $("#sort").onchange = render;
$("#ledger").onclick = e => { const id = e.target.dataset.id; if (id) { cart[id] = Math.min((cart[id] || 0) + 1, BOOKS[id - 1].n); saveCart(); openCart(); } };

// Collections
$("#collections-body").innerHTML = COLLECTIONS.map(([n, h, k]) => `<tr><td><b>${n}</b></td><td class="m">${k} titles</td><td><a class="link" href="${STORE}/collections/${h}" target="_blank" rel="noopener">Browse</a></td></tr>`).join("");

// Cart: checkout uses a Shopify cart permalink on the real store
function saveCart() { safe(() => localStorage.setItem("cart2", JSON.stringify(cart))); drawCart(); }
function drawCart() {
  const items = Object.entries(cart).map(([id, q]) => ({b: BOOKS[id - 1], q})).filter(i => i.b);
  $("#cartList").innerHTML = items.length ? items.map(({b, q}) => `
    <li><div><b>${b.t}</b><br><small>${money(b.p)}</small></div>
    <div class="qty"><button data-d="-1" data-id="${b.id}" type="button" aria-label="Remove one">−</button>${q}<button data-d="1" data-id="${b.id}" type="button" aria-label="Add one">+</button></div></li>`).join("")
    : "<li>Nothing in the cart yet.</li>";
  $("#cartCount").textContent = items.reduce((n, i) => n + i.q, 0);
  $("#cartTotal").textContent = money(items.reduce((n, i) => n + i.q * i.b.p, 0));
  const co = $("#checkout");
  co.href = items.length ? STORE + "/cart/" + items.map(i => i.b.v + ":" + i.q).join(",") : STORE;
  co.textContent = items.length ? "Checkout on daralathari.com" : "Visit daralathari.com";
}
$("#cartList").onclick = e => { const {id, d} = e.target.dataset; if (!d) return;
  cart[id] = Math.min((cart[id] || 0) + +d, BOOKS[id - 1].n); if (cart[id] <= 0) delete cart[id]; saveCart(); };
function openCart() { $("#drawer").classList.add("open"); $("#drawer").setAttribute("aria-hidden", "false"); $("#scrim").hidden = false; }
function closeCart() { $("#drawer").classList.remove("open"); $("#drawer").setAttribute("aria-hidden", "true"); $("#scrim").hidden = true; }
$("#cartOpen").onclick = openCart; $("#cartClose").onclick = closeCart; $("#scrim").onclick = closeCart;
document.onkeydown = e => { if (e.key === "Escape") closeCart(); };

// Theme, menu, dates
const root = document.documentElement;
const saved = safe(() => localStorage.getItem("theme"));
if (saved) root.dataset.theme = saved;
$("#theme").onclick = () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark"; safe(() => localStorage.setItem("theme", root.dataset.theme));
};
$("#burger").onclick = () => $("#links").classList.toggle("open");
$("#links").onclick = () => $("#links").classList.remove("open");
$("#yr").textContent = "© " + new Date().getFullYear();
safe(() => {
  const now = new Date();
  const g = now.toLocaleDateString("en-GB", {weekday: "short", day: "numeric", month: "short", year: "numeric"});
  const h = new Intl.DateTimeFormat("en-u-ca-islamic-umalqura", {day: "numeric", month: "long", year: "numeric"}).format(now);
  $("#dates").textContent = g + "  ·  " + h;
});

render(); drawCart();

// ---- 3D shelf (Three.js). Falls back to the CSS shelf if WebGL is unavailable. ----
(function shelf3d() {
  if (!window.THREE) return;
  const stage = $("#stage"), canvas = $("#gl"), tip = $("#tip");
  let renderer;
  try { renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: true}); } catch { return; }
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  stage.hidden = false; document.body.classList.add("has3d");
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 1, 600);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8a80, .85));
  const sun = new THREE.DirectionalLight(0xfff3e0, .9);
  sun.position.set(-40, 70, 60); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, {left: -60, right: 60, top: 50, bottom: -20, near: 10, far: 220});
  sun.shadow.bias = -.0005; scene.add(sun);

  const group = new THREE.Group(); scene.add(group);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(400, 200), new THREE.ShadowMaterial({opacity: .16}));
  wall.position.set(0, 60, -9); wall.receiveShadow = true; group.add(wall);
  const boardMat = new THREE.MeshStandardMaterial({roughness: .8});
  const board = new THREE.Mesh(new THREE.BoxGeometry(100, 2, 26), boardMat);
  board.position.set(0, -1, 2); board.receiveShadow = true; group.add(board);

  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const tex = (b, w, h) => {
    const W = 160, H = Math.round(W * h / w), c = document.createElement("canvas"); c.width = W; c.height = H;
    const g = c.getContext("2d"); g.fillStyle = b.col; g.fillRect(0, 0, W, H);
    g.fillStyle = "rgba(255,255,255,.35)"; g.fillRect(0, 0, W, 5); g.fillRect(0, H - 5, W, 5);
    g.fillStyle = "rgba(0,0,0,.18)"; g.fillRect(0, 0, 6, H); g.fillRect(W - 6, 0, 6, H);
    if (b.t) {
      g.fillStyle = "#F3EEE0"; g.textAlign = "center";
      g.font = '700 ' + Math.round(W * .36) + 'px Amiri, serif'; g.fillText(b.ar, W / 2, W * .5);
      g.fillStyle = "rgba(243,238,224,.6)"; g.fillRect(W * .25, W * .68, W * .5, 2);
      g.save(); g.translate(W / 2, W * .9); g.rotate(Math.PI / 2); g.textAlign = "left";
      let fs = Math.round(W * .3); g.font = fs + 'px "Young Serif", Georgia, serif';
      const room = H - W * 1.15; while (g.measureText(b.t).width > room && fs > 10) { fs -= 2; g.font = fs + 'px "Young Serif", Georgia, serif'; }
      g.textBaseline = "middle"; g.fillText(b.t, 0, 0); g.restore();
    }
    const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; return t;
  };
  const items = [];
  SHELF.forEach((b, i) => {
    items.push({book: b, t: b.s || b.t, ar: b.ar, col: color(b), th: b.w / 13, h: b.h / 9.5});
    if (i % 3 === 1) items.push({t: "", col: COLORS[(i + 3) % COLORS.length], th: 2 + i * .25, h: 17 + i * .8});
  });
  const total = items.reduce((n, it) => n + it.th + .25, 0);
  let x = -total / 2; const meshes = [];
  const build = () => items.forEach((it, i) => {
    const side = new THREE.MeshStandardMaterial({color: it.col, roughness: .7});
    const pages = new THREE.MeshStandardMaterial({color: 0xe9e2cf, roughness: .95});
    const spine = new THREE.MeshStandardMaterial({map: tex(it, it.th, it.h), roughness: .65});
    const m = new THREE.Mesh(new THREE.BoxGeometry(it.th, it.h, 16), [side, side, pages, pages, spine, pages]);
    m.position.set(x + it.th / 2, it.h / 2, i === 4 ? 3 : 0); x += it.th + .25;
    m.castShadow = m.receiveShadow = true; m.userData = {it, z0: m.position.z, lift: 0};
    if (it.book) meshes.push(m); group.add(m);
  });
  (document.fonts && document.fonts.load ? Promise.all([document.fonts.load('700 40px Amiri'), document.fonts.load('40px "Young Serif"')]).catch(() => {}) : Promise.resolve()).then(build);

  let tx = 0, ty = 0, cx = 0, cy = 0, hover = null, vis = true, tick = 0;
  const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
  const point = e => { const r = canvas.getBoundingClientRect(); mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); return r; };
  canvas.addEventListener("pointermove", e => {
    const r = point(e); tx = mouse.x * .45; ty = mouse.y * .12;
    ray.setFromCamera(mouse, camera); const hit = ray.intersectObjects(meshes)[0];
    hover = hit ? hit.object : null; canvas.style.cursor = hover ? "pointer" : "grab";
    tip.hidden = !hover;
    if (hover) { const b = hover.userData.it.book; tip.textContent = b.t + "  " + money(b.p); tip.style.left = e.clientX - r.left + "px"; tip.style.top = e.clientY - r.top + "px"; }
  });
  canvas.addEventListener("pointerleave", () => { hover = null; tip.hidden = true; tx = ty = 0; });
  canvas.addEventListener("click", () => {
    if (!hover) return; cat = "All"; $("#search").value = hover.userData.it.book.t; syncTabs(); render();
    $("#catalogue").scrollIntoView({behavior: "smooth"});
  });

  const fit = () => {
    const w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    const t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const d = Math.max((total / 2 * 1.12) / (t * camera.aspect), 19 / t) + 8;
    camera.position.set(0, 17, d); camera.lookAt(0, 15, 0);
  };
  new ResizeObserver(fit).observe(stage); fit();
  new IntersectionObserver(es => vis = es[0].isIntersecting).observe(stage);

  const frame = time => {
    requestAnimationFrame(frame); if (!vis) return;
    if (++tick % 20 === 0) { boardMat.color.set(css("--ink") || "#171D1B"); }
    const k = reduce ? 1 : .07, sc = Math.min(scrollY / 700, 1);
    cx += (tx + sc * .5 - cx) * k; cy += (ty - cy) * k;
    group.rotation.y = cx + (reduce ? 0 : Math.sin(time / 3500) * .04); group.rotation.x = -cy;
    group.children.forEach(m => { const d = m.userData; if (!d.it) return;
      const want = m === hover ? 5 : 0; d.lift += (want - d.lift) * .15; m.position.z = d.z0 + d.lift; m.position.y = d.it.h / 2 + d.lift * .12; });
    renderer.render(scene, camera);
  };
  boardMat.color.set(css("--ink") || "#171D1B"); requestAnimationFrame(frame);
})();
