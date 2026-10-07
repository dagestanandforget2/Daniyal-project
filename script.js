const BOOKS = [
  {id:1,t:"The Foundations of Belief",a:"Demo Author",c:"Aqeedah",p:18.5,h:162,ar:"عقيدة"},
  {id:2,t:"Purification of the Heart",a:"Demo Author",c:"Character",p:14,h:174,ar:"تزكية"},
  {id:3,t:"Arabic Made Easy, Vol. 1",a:"Demo Author",c:"Arabic",p:24,h:38,ar:"عربية"},
  {id:4,t:"Stories of the Prophets",a:"Demo Author",c:"Seerah",p:29,h:30,ar:"سيرة"},
  {id:5,t:"A Guide to Daily Prayer",a:"Demo Author",c:"Fiqh",p:12,h:200,ar:"صلاة"},
  {id:6,t:"Tafsir for Beginners",a:"Demo Author",c:"Qur’an",p:32,h:150,ar:"تفسير"},
  {id:7,t:"Forty Hadith, Explained",a:"Demo Author",c:"Hadith",p:16.5,h:20,ar:"حديث"},
  {id:8,t:"Raising Muslim Children",a:"Demo Author",c:"Family",p:21,h:10,ar:"أسرة"}
];
const $ = s => document.querySelector(s);
const money = n => "$" + n.toFixed(2);
const safe = f => { try { return f(); } catch { return null; } };
let cart = safe(() => JSON.parse(localStorage.getItem("cart"))) || {};
let cat = "All";

// Catalogue
const cats = ["All", ...new Set(BOOKS.map(b => b.c))];
$("#chips").innerHTML = cats.map(c => `<button class="chip${c==="All"?" on":""}" data-c="${c}">${c}</button>`).join("");
function render() {
  const q = $("#search").value.toLowerCase(), s = $("#sort").value;
  let list = BOOKS.filter(b => (cat==="All"||b.c===cat) && (b.t+b.a).toLowerCase().includes(q));
  if (s) list.sort((x,y) => s==="asc" ? x.p-y.p : y.p-x.p);
  $("#grid").innerHTML = list.map(b => `
    <article class="book reveal">
      <div class="cover" style="background:linear-gradient(150deg,hsl(${b.h} 45% 28%),hsl(${b.h} 50% 14%))"><i>${b.ar}</i><b>${b.t}</b></div>
      <div class="binfo"><small>${b.c} · ${b.a}</small><div class="row"><b>${money(b.p)}</b><button class="add" data-id="${b.id}">Add</button></div></div>
    </article>`).join("");
  $("#empty").hidden = list.length > 0;
  observe();
}
$("#chips").onclick = e => { const c = e.target.dataset.c; if (!c) return; cat = c;
  document.querySelectorAll(".chip").forEach(x => x.classList.toggle("on", x.dataset.c===c)); render(); };
$("#search").oninput = render; $("#sort").onchange = render;
$("#grid").onclick = e => { const id = e.target.dataset.id; if (id) { cart[id] = (cart[id]||0)+1; saveCart(); openCart(); } };

// Cart
function saveCart() { safe(() => localStorage.setItem("cart", JSON.stringify(cart))); drawCart(); }
function drawCart() {
  const items = Object.entries(cart).map(([id,q]) => ({b:BOOKS.find(x => x.id==id), q})).filter(i => i.b);
  $("#cartList").innerHTML = items.length ? items.map(({b,q}) => `
    <li><div><b>${b.t}</b><br><small>${money(b.p)}</small></div>
    <div class="qty"><button data-d="-1" data-id="${b.id}" aria-label="Less">−</button>${q}<button data-d="1" data-id="${b.id}" aria-label="More">+</button></div></li>`).join("")
    : "<li>Your cart is empty.</li>";
  $("#cartCount").textContent = items.reduce((n,i) => n+i.q, 0);
  $("#cartTotal").textContent = money(items.reduce((n,i) => n+i.q*i.b.p, 0));
}
$("#cartList").onclick = e => { const {id,d} = e.target.dataset; if (!d) return;
  cart[id] = (cart[id]||0) + +d; if (cart[id] <= 0) delete cart[id]; saveCart(); };
function openCart() { $("#drawer").classList.add("open"); $("#drawer").setAttribute("aria-hidden","false"); $("#scrim").hidden = false; }
function closeCart() { $("#drawer").classList.remove("open"); $("#drawer").setAttribute("aria-hidden","true"); $("#scrim").hidden = true; }
$("#cartOpen").onclick = openCart; $("#cartClose").onclick = closeCart; $("#scrim").onclick = closeCart;
document.onkeydown = e => { if (e.key === "Escape") closeCart(); };
$("#checkout").onclick = () => { alert("Demo only — connect Shopify/Stripe here."); };

// Theme, menu, newsletter
const root = document.documentElement;
const saved = safe(() => localStorage.getItem("theme"));
if (saved ? saved==="dark" : matchMedia("(prefers-color-scheme: dark)").matches) root.dataset.theme = "dark";
$("#theme").onclick = () => { const d = root.dataset.theme === "dark"; root.dataset.theme = d ? "light" : "dark"; safe(() => localStorage.setItem("theme", root.dataset.theme)); };
$("#burger").onclick = () => $("#links").classList.toggle("open");
$("#links").onclick = () => $("#links").classList.remove("open");
$("#newsletter").onsubmit = e => { e.preventDefault(); $("#nlMsg").textContent = "JazakAllahu khayran — you're subscribed (demo)."; e.target.reset(); };
$("#yr").textContent = new Date().getFullYear();

// Reveal + counters
let io;
function observe() {
  io ||= new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), {threshold:.1});
  document.querySelectorAll(".reveal:not(.in),.card,.feat,blockquote").forEach(el => { el.classList.add("reveal"); io.observe(el); });
}
document.querySelectorAll("[data-count]").forEach(el => {
  const end = +el.dataset.count, t0 = performance.now();
  (function step(t) { const p = Math.min((t-t0)/1400, 1); el.textContent = Math.round(end*p).toLocaleString() + (p===1?"+":""); if (p<1) requestAnimationFrame(step); })(t0);
});

render(); drawCart();
