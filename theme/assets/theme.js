(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var T = window.THEME || { currency: "USD", routes: { cart: "/cart", add: "/cart/add", change: "/cart/change" } };
  var money = function (cents) {
    try { return new Intl.NumberFormat(T.locale || undefined, { style: "currency", currency: T.currency }).format(cents / 100); }
    catch (e) { return "$" + (cents / 100).toFixed(2); }
  };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var safe = function (f) { try { return f(); } catch (e) { return null; } };

  // Theme toggle, menu, dates
  var root = document.documentElement;
  var saved = safe(function () { return localStorage.getItem("theme"); });
  if (saved) root.dataset.theme = saved;
  var themeBtn = $("#theme");
  if (themeBtn) themeBtn.onclick = function () {
    var dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    safe(function () { localStorage.setItem("theme", root.dataset.theme); });
  };
  var burger = $("#burger"), links = $("#links");
  if (burger && links) { burger.onclick = function () { links.classList.toggle("open"); }; links.onclick = function () { links.classList.remove("open"); }; }
  safe(function () {
    var now = new Date();
    var g = now.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", year: "numeric" });
    var h = new Intl.DateTimeFormat("en-u-ca-islamic-umalqura", { day: "numeric", month: "long", year: "numeric" }).format(now);
    $("#dates").textContent = g + "  ·  " + h;
  });

  // Cart drawer on the Shopify AJAX cart API
  var drawer = $("#drawer"), scrim = $("#scrim");
  function openCart() { drawer.classList.add("open"); drawer.setAttribute("aria-hidden", "false"); scrim.hidden = false; }
  function closeCart() { drawer.classList.remove("open"); drawer.setAttribute("aria-hidden", "true"); scrim.hidden = true; }
  var cartLink = $("#cartOpen");
  if (cartLink) cartLink.addEventListener("click", function (e) { if (location.pathname === T.routes.cart) return; e.preventDefault(); refresh().then(openCart); });
  $("#cartClose").onclick = closeCart; scrim.onclick = closeCart;
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeCart(); });

  function draw(cart) {
    document.querySelectorAll("[data-cart-count]").forEach(function (n) { n.textContent = cart.item_count; });
    $("#cartTotal").textContent = money(cart.total_price);
    $("#cartList").innerHTML = cart.items.length ? cart.items.map(function (i) {
      return '<li><div><b>' + esc(i.product_title) + '</b>' +
        (i.variant_title ? '<br><small>' + esc(i.variant_title) + '</small>' : '') +
        '<br><small>' + money(i.final_price) + '</small></div>' +
        '<div class="qty"><button type="button" data-key="' + esc(i.key) + '" data-q="' + (i.quantity - 1) + '" aria-label="Remove one">&minus;</button>' + i.quantity +
        '<button type="button" data-key="' + esc(i.key) + '" data-q="' + (i.quantity + 1) + '" aria-label="Add one">+</button></div></li>';
    }).join("") : "<li>Nothing in the cart yet.</li>";
    $("#checkout").textContent = cart.items.length ? "View cart and check out" : "Keep browsing";
    $("#checkout").href = cart.items.length ? T.routes.cart : "#catalogue";
  }
  function refresh() { return fetch(T.routes.cart + ".js", { headers: { Accept: "application/json" } }).then(function (r) { return r.json(); }).then(function (c) { draw(c); return c; }); }
  $("#cartList").addEventListener("click", function (e) {
    var b = e.target.closest("[data-key]"); if (!b) return;
    fetch(T.routes.change + ".js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ id: b.dataset.key, quantity: +b.dataset.q }) })
      .then(function (r) { return r.json(); }).then(draw);
  });

  function add(body, btn) {
    var label = btn && btn.textContent; if (btn) btn.disabled = true;
    return fetch(T.routes.add + ".js", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.description || j.message || "Could not add this item"); return j; }); })
      .then(function () { return refresh(); }).then(openCart)
      .catch(function (err) { if (btn) { btn.textContent = err.message; setTimeout(function () { btn.textContent = label; }, 2500); } })
      .then(function () { if (btn) btn.disabled = false; });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-add]"); if (!b) return;
    e.preventDefault(); add({ id: +b.dataset.variant, quantity: 1 }, b);
  });
  document.addEventListener("submit", function (e) {
    var f = e.target.closest("[data-add-form]"); if (!f) return;
    e.preventDefault(); var fd = new FormData(f);
    add({ id: +fd.get("id"), quantity: +fd.get("quantity") || 1 }, f.querySelector("[type=submit]"));
  });

  // Product page: price follows the selected variant
  document.querySelectorAll("[data-variant-select]").forEach(function (sel) {
    sel.addEventListener("change", function () {
      var o = sel.selectedOptions[0], p = $("[data-price]"); if (p) p.textContent = o.dataset.price;
    });
  });
  // Collection sort
  var sort = $("[data-sort]");
  if (sort) sort.addEventListener("change", function () { var u = new URL(location.href); u.searchParams.set("sort_by", sort.value); u.searchParams.delete("page"); location.href = u.toString(); });

  refresh().catch(function () {});
})();
