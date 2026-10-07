/* 3D book shelf. Reads window.SHELF (set by the hero section). Falls back to the plain link shelf. */
(function () {
  var data = window.SHELF || [];
  var stage = document.getElementById("stage");
  if (!stage || !window.THREE || !data.length) return;
  var canvas = document.getElementById("gl"), tip = document.getElementById("tip");
  var renderer;
  try { renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true }); } catch (e) { return; }

  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  stage.hidden = false; document.body.classList.add("has3d");
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  var COLORS = ["#7A2E2A", "#1F3B34", "#B07A1E", "#2B3A55", "#4A2F4F", "#33403A", "#8A4B2A", "#1E2F6B"];
  var hash = function (s) { var h = 0; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; return h; };
  var arabic = function (t) {
    t = t.toLowerCase();
    if (/tafsir/.test(t)) return "تفسير";
    if (/hadith|bulugh|riyad|bukhari|musnad/.test(t)) return "حديث";
    if (/fiqh|salah|prayer/.test(t)) return "فقه";
    if (/tawh|tauh|aqeed|creed|sunnah|principles|wasit|pillars/.test(t)) return "عقيدة";
    if (/prophet|seerah|biograph|women|moon/.test(t)) return "سيرة";
    if (/arabic|madinah/.test(t)) return "عربية";
    if (/thobe|shemagh|kufi/.test(t)) return "لباس";
    return "كتاب";
  };
  var short = function (t) { return t.replace(/\(.*?\)/g, "").split(/ by | - |: /)[0].trim(); };

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 1, 600);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8a80, 0.85));
  var sun = new THREE.DirectionalLight(0xfff3e0, 0.9);
  sun.position.set(-40, 70, 60); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 50, bottom: -20, near: 10, far: 220 });
  sun.shadow.bias = -0.0005; scene.add(sun);

  var group = new THREE.Group(); scene.add(group);
  var wall = new THREE.Mesh(new THREE.PlaneGeometry(400, 200), new THREE.ShadowMaterial({ opacity: 0.16 }));
  wall.position.set(0, 60, -9); wall.receiveShadow = true; group.add(wall);
  var boardMat = new THREE.MeshStandardMaterial({ roughness: 0.8 });
  var board = new THREE.Mesh(new THREE.BoxGeometry(100, 2, 26), boardMat);
  board.position.set(0, -1, 2); board.receiveShadow = true; group.add(board);
  var ink = function () { return getComputedStyle(document.documentElement).getPropertyValue("--ink").trim() || "#171D1B"; };

  var items = data.map(function (d, i) {
    var h = hash(d.t);
    return { d: d, s: short(d.t), ar: arabic(d.t), col: COLORS[i % COLORS.length], th: 2.8 + ((h % 100) / 100) * 2.6, h: 21 + (((h >> 8) % 100) / 100) * 9 };
  });

  function spineTexture(it) {
    var W = 160, H = Math.round(W * it.h / it.th), c = document.createElement("canvas"); c.width = W; c.height = H;
    var g = c.getContext("2d");
    g.fillStyle = it.col; g.fillRect(0, 0, W, H);
    g.fillStyle = "rgba(255,255,255,.35)"; g.fillRect(0, 0, W, 5); g.fillRect(0, H - 5, W, 5);
    g.fillStyle = "rgba(0,0,0,.18)"; g.fillRect(0, 0, 6, H); g.fillRect(W - 6, 0, 6, H);
    g.fillStyle = "#F3EEE0"; g.textAlign = "center";
    g.font = "700 " + Math.round(W * 0.36) + "px Amiri, serif"; g.fillText(it.ar, W / 2, W * 0.5);
    g.fillStyle = "rgba(243,238,224,.6)"; g.fillRect(W * 0.25, W * 0.68, W * 0.5, 2);
    g.save(); g.translate(W / 2, W * 0.9); g.rotate(Math.PI / 2); g.textAlign = "left"; g.textBaseline = "middle";
    var fs = Math.round(W * 0.3), room = H - W * 1.15, face = function (n) { return n + 'px "Young Serif", Georgia, serif'; };
    g.font = face(fs);
    while (g.measureText(it.s).width > room && fs > 10) { fs -= 2; g.font = face(fs); }
    g.fillText(it.s, 0, 0); g.restore();
    var t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = 4; return t;
  }

  var total = items.reduce(function (n, it) { return n + it.th + 0.25; }, 0);
  var x = -total / 2, meshes = [];
  function build() {
    items.forEach(function (it, i) {
      var back = new THREE.MeshStandardMaterial({ color: it.col, roughness: 0.7 });
      var front = new THREE.MeshStandardMaterial({ color: it.col, roughness: 0.7 });
      var pages = new THREE.MeshStandardMaterial({ color: 0xe9e2cf, roughness: 0.95 });
      var spine = new THREE.MeshStandardMaterial({ map: spineTexture(it), roughness: 0.65 });
      var m = new THREE.Mesh(new THREE.BoxGeometry(it.th, it.h, 16), [front, back, pages, pages, spine, pages]);
      m.position.set(x + it.th / 2, it.h / 2, 0); x += it.th + 0.25;
      m.castShadow = m.receiveShadow = true;
      m.userData = { it: it, front: front, lift: 0, rot: 0, cover: false };
      meshes.push(m); group.add(m);
    });
  }
  var fonts = document.fonts && document.fonts.load
    ? Promise.all([document.fonts.load("700 40px Amiri"), document.fonts.load('40px "Young Serif"')]).catch(function () {})
    : Promise.resolve();
  fonts.then(build);

  function loadCover(m) {
    var d = m.userData; if (d.cover || !d.it.d.img) return; d.cover = true;
    var loader = new THREE.TextureLoader(); loader.setCrossOrigin("anonymous");
    loader.load(d.it.d.img, function (t) {
      t.encoding = THREE.sRGBEncoding; t.anisotropy = 4;
      d.front.map = t; d.front.color.set(0xffffff); d.front.needsUpdate = true;
    });
  }

  var tx = 0, ty = 0, cx = 0, cy = 0, hover = null, vis = true, tick = 0;
  var ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
  function point(e) { var r = canvas.getBoundingClientRect(); mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); return r; }
  canvas.addEventListener("pointermove", function (e) {
    var r = point(e); tx = mouse.x * 0.45; ty = mouse.y * 0.12;
    ray.setFromCamera(mouse, camera); var hit = ray.intersectObjects(meshes)[0];
    hover = hit ? hit.object : null; canvas.style.cursor = hover ? "pointer" : "grab";
    tip.hidden = !hover;
    if (hover) { loadCover(hover); var d = hover.userData.it.d; tip.textContent = d.t + "  " + d.p; tip.style.left = e.clientX - r.left + "px"; tip.style.top = e.clientY - r.top + "px"; }
  });
  canvas.addEventListener("pointerleave", function () { hover = null; tip.hidden = true; tx = ty = 0; });
  canvas.addEventListener("click", function (e) {
    point(e); ray.setFromCamera(mouse, camera);
    var hit = ray.intersectObjects(meshes)[0];
    if (hit) location.href = hit.object.userData.it.d.u;
  });

  function fit() {
    var w = stage.clientWidth, h = stage.clientHeight; renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    var t = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    var d = Math.max((total / 2 * 1.12) / (t * camera.aspect), 19 / t) + 8;
    camera.position.set(0, 17, d); camera.lookAt(0, 15, 0);
  }
  new ResizeObserver(fit).observe(stage); fit();
  new IntersectionObserver(function (es) { vis = es[0].isIntersecting; }).observe(stage);

  function frame(time) {
    requestAnimationFrame(frame); if (!vis) return;
    if (++tick % 20 === 0) boardMat.color.set(ink());
    var k = reduce ? 1 : 0.07, sc = Math.min(scrollY / 700, 1);
    cx += (tx + sc * 0.5 - cx) * k; cy += (ty - cy) * k;
    group.rotation.y = cx + (reduce ? 0 : Math.sin(time / 3500) * 0.04); group.rotation.x = -cy;
    meshes.forEach(function (m) {
      var d = m.userData, on = m === hover;
      d.lift += ((on ? 16 : 0) - d.lift) * 0.14; d.rot += ((on ? -Math.PI / 2 : 0) - d.rot) * 0.14;
      m.position.z = d.lift; m.rotation.y = d.rot;
    });
    renderer.render(scene, camera);
  }
  boardMat.color.set(ink()); requestAnimationFrame(frame);
})();
