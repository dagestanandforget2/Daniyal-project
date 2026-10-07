const COLORS = ["#7A2E2A", "#1F3B34", "#B07A1E", "#2B3A55", "#4A2F4F", "#33403A", "#8A4B2A", "#1E2F6B"];
const BOOKS = [
  {id:1,no:"DA-0101",t:"The Foundations of Belief",a:"Author name",c:"Aqeedah",p:18.5,pg:162,bind:"Paperback",ar:"عقيدة",w:44,h:250},
  {id:2,no:"DA-0102",t:"Purification of the Heart",a:"Author name",c:"Character",p:14,pg:174,bind:"Paperback",ar:"تزكية",w:38,h:220},
  {id:3,no:"DA-0103",t:"Arabic Made Easy, Vol. 1",a:"Author name",c:"Arabic",p:24,pg:380,bind:"Hardback",ar:"عربية",w:58,h:280},
  {id:4,no:"DA-0104",t:"Stories of the Prophets",a:"Author name",c:"Seerah",p:29,pg:520,bind:"Hardback",ar:"سيرة",w:64,h:300},
  {id:5,no:"DA-0105",t:"A Guide to Daily Prayer",a:"Author name",c:"Fiqh",p:12,pg:96,bind:"Paperback",ar:"صلاة",w:36,h:265},
  {id:6,no:"DA-0106",t:"Tafsir for Beginners",a:"Author name",c:"Qur’an",p:32,pg:430,bind:"Hardback",ar:"تفسير",w:56,h:270},
  {id:7,no:"DA-0107",t:"Forty Hadith, Explained",a:"Author name",c:"Hadith",p:16.5,pg:204,bind:"Paperback",ar:"حديث",w:40,h:235},
  {id:8,no:"DA-0108",t:"Raising Muslim Children",a:"Author name",c:"Family",p:21,pg:248,bind:"Paperback",ar:"أسرة",w:46,h:245}
];
const $ = s => document.querySelector(s);
const money = n => "£" + n.toFixed(2);
const safe = f => { try { return f(); } catch { return null; } };
const color = b => COLORS[(b.id - 1) % COLORS.length];
let cart = safe(() => JSON.parse(localStorage.getItem("cart"))) || {};
let cat = "All";

// Shelf: real titles plus a few filler spines and one leaning book
$("#shelf").innerHTML = BOOKS.map((b, i) =>
  `<a class="spine${i === 4 ? " lean" : ""}" href="#catalogue" data-find="${b.id}" style="background:${color(b)};width:${b.w}px;height:${b.h}px" title="${b.t}"><i lang="ar">${b.ar}</i>${b.t}<em>${b.no}</em></a>` +
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
      <div class="ttl"><b>${b.t}</b><span>${b.a}</span></div>
      <div class="cat">${b.c}</div>
      <div class="fmt">${b.bind}, ${b.pg} pp<span class="no">${b.no}</span></div>
      <div class="price">${money(b.p)}</div>
      <button class="add" data-id="${b.id}" type="button">Add</button>
    </li>`).join("");
  $("#empty").hidden = list.length > 0;
}
$("#tabs").onclick = e => { const c = e.target.dataset.c; if (!c) return; cat = c; syncTabs(); render(); };
$("#search").oninput = render; $("#sort").onchange = render;
$("#ledger").onclick = e => { const id = e.target.dataset.id; if (id) { cart[id] = (cart[id] || 0) + 1; saveCart(); openCart(); } };

// Cart
function saveCart() { safe(() => localStorage.setItem("cart", JSON.stringify(cart))); drawCart(); }
function drawCart() {
  const items = Object.entries(cart).map(([id, q]) => ({b: BOOKS.find(x => x.id == id), q})).filter(i => i.b);
  $("#cartList").innerHTML = items.length ? items.map(({b, q}) => `
    <li><div><b>${b.t}</b><br><small>${money(b.p)}</small></div>
    <div class="qty"><button data-d="-1" data-id="${b.id}" type="button" aria-label="Remove one">−</button>${q}<button data-d="1" data-id="${b.id}" type="button" aria-label="Add one">+</button></div></li>`).join("")
    : "<li>Nothing in the cart yet.</li>";
  $("#cartCount").textContent = items.reduce((n, i) => n + i.q, 0);
  $("#cartTotal").textContent = money(items.reduce((n, i) => n + i.q * i.b.p, 0));
}
$("#cartList").onclick = e => { const {id, d} = e.target.dataset; if (!d) return;
  cart[id] = (cart[id] || 0) + +d; if (cart[id] <= 0) delete cart[id]; saveCart(); };
function openCart() { $("#drawer").classList.add("open"); $("#drawer").setAttribute("aria-hidden", "false"); $("#scrim").hidden = false; }
function closeCart() { $("#drawer").classList.remove("open"); $("#drawer").setAttribute("aria-hidden", "true"); $("#scrim").hidden = true; }
$("#cartOpen").onclick = openCart; $("#cartClose").onclick = closeCart; $("#scrim").onclick = closeCart;
document.onkeydown = e => { if (e.key === "Escape") closeCart(); };
$("#checkout").onclick = e => { e.target.textContent = "Demo only: checkout is not connected"; setTimeout(() => e.target.textContent = "Checkout (demo)", 2500); };

// Theme, menu, newsletter, dates
const root = document.documentElement;
const saved = safe(() => localStorage.getItem("theme"));
if (saved) root.dataset.theme = saved;
$("#theme").onclick = () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark"; safe(() => localStorage.setItem("theme", root.dataset.theme));
};
$("#burger").onclick = () => $("#links").classList.toggle("open");
$("#links").onclick = () => $("#links").classList.remove("open");
$("#newsletter").onsubmit = e => { e.preventDefault(); $("#nlMsg").textContent = "Thank you. You are on the list (demo)."; e.target.reset(); };
const now = new Date();
$("#yr").textContent = "© " + now.getFullYear();
safe(() => {
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
  BOOKS.forEach((b, i) => {
    items.push({book: b, t: b.t, ar: b.ar, col: color(b), th: b.w / 13, h: b.h / 9.5});
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
