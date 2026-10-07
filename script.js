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
