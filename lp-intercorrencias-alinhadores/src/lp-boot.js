/* Motor das cenas presas no scroll (03 Dor, 03b Sem critério, notebook da 04). Vai repetido nos
   widgets que usam cenas, mas só a primeira cópia roda.

   Sem "pin" por JavaScript: cada cena fica num palco (.lp-stage) com position: sticky dentro de uma
   trilha alta (.lp-track). Quem segura o palco na tela é o próprio navegador, sem tremor e sem troca
   de camada. Este motor só mede quanto da trilha já foi rolado (0 → 1) e entrega esse progresso
   para cada cena, no mesmo quadro da rolagem. No desktop, a rolagem suave (Lenis) roda no mesmo laço. */
(function () {
  if (window.lpScroll) return;
  var CDN = {
    gsap: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
    lenis: 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js'
  };
  var scenes = [], started = false, needLayout = true, lastY = -1, lenis = null;
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var edit = function () {
    return document.body.classList.contains('elementor-editor-active') ||
      !!(window.elementorFrontend && elementorFrontend.isEditMode && elementorFrontend.isEditMode());
  };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var desktop = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function load(src) {
    return new Promise(function (ok) {
      var s = document.createElement('script');
      s.src = src; s.onload = ok; s.onerror = ok;
      document.head.appendChild(s);
    });
  }

  // Mede a posição das trilhas (só quando o layout muda; nunca a cada quadro).
  function layout() {
    needLayout = false;
    var y = window.scrollY, vh = window.innerHeight;
    scenes.forEach(function (s) {
      var r = s.track.getBoundingClientRect();
      s.top = r.top + y;
      s.height = r.height;
      s.stageH = s.stage.offsetHeight;
      s.sticky = getComputedStyle(s.stage).position === 'sticky' && s.height > s.stageH + 10;
      s.vh = vh;
    });
  }
  function frame() {
    if (needLayout) { layout(); lastY = -1; }
    var y = window.scrollY;
    if (y === lastY) return;
    lastY = y;
    scenes.forEach(function (s) {
      var p, enter = clamp((y + s.vh - s.top) / s.vh);
      if (s.sticky) p = clamp((y - s.top) / (s.height - s.stageH));
      else p = clamp((y + s.vh * 0.65 - s.top) / Math.max(1, s.height)); // celular sem palco preso
      if (p !== s.p || enter !== s.enter) { s.p = p; s.enter = enter; s.fn(p, enter); }
    });
  }
  function loop(t) {
    if (lenis) lenis.raf(t);
    frame();
    requestAnimationFrame(loop);
  }
  function smooth() {
    if (!window.Lenis || !desktop || reduce) return;
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    window.__lpLenis = lenis;
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href');
      var target = id.length > 1 && document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      lenis.scrollTo(target, { offset: -50 });
    }, true);
  }
  function start() {
    if (started) return;
    started = true;
    if (edit() || reduce) {
      document.documentElement.classList.add('lp-static');
      scenes.forEach(function (s) { if (s.done) s.done(); });
      return;
    }
    var p = Promise.resolve();
    if (!window.gsap) p = p.then(function () { return load(CDN.gsap); });
    if (desktop && !window.Lenis) p = p.then(function () { return load(CDN.lenis); });
    p.then(function () {
      scenes.forEach(function (s) { if (s.init) s.init(window.gsap); });
      smooth();
      var dirty = function () { needLayout = true; };
      window.addEventListener('resize', dirty);
      window.addEventListener('load', dirty);
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(dirty);
      if (window.ResizeObserver) new ResizeObserver(dirty).observe(document.body);
      requestAnimationFrame(loop);
    });
  }

  window.lpScroll = {
    /* stage: o palco (.lp-stage) dentro da trilha (.lp-track).
       opts.init(gsap): prepara a cena; opts.update(p, enter): progresso da trilha (0–1) e da
       entrada da seção na tela (0–1); opts.done(): estado final (editor, movimento reduzido). */
    scene: function (stage, opts) {
      if (!stage) return;
      var track = stage.closest('.lp-track') || stage;
      scenes.push({ stage: stage, track: track, init: opts.init, fn: opts.update, done: opts.done, p: -1, enter: -1 });
      needLayout = true;
    },
    reduce: reduce
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(start, 0); });
  else setTimeout(start, 0);
})();
