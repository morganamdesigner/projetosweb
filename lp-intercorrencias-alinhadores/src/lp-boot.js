/* Orquestrador único das animações de scroll da LP. Vai repetido nos widgets que usam GSAP (estilos
   globais, 03b e notebook), mas só a primeira cópia roda. Carrega GSAP, ScrollTrigger e Lenis uma vez
   e cria as travas (pins) na ordem em que as seções aparecem na página: o ScrollTrigger calcula cada
   trava contando o espaço das anteriores, então criar fora de ordem desloca as seguintes. */
(function () {
  if (window.lpScroll) return;
  var queue = [], ready = false, started = false;
  var CDN = {
    gsap: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
    st: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
    lenis: 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js'
  };
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
  function libs() {
    var p = Promise.resolve();
    if (!window.gsap) p = p.then(function () { return load(CDN.gsap); });
    p = p.then(function () { if (!window.ScrollTrigger) return load(CDN.st); });
    if (desktop && !reduce) p = p.then(function () { if (!window.Lenis) return load(CDN.lenis); });
    return p;
  }
  function byPosition(a, b) {
    return a.el.compareDocumentPosition(b.el) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
  }
  function smooth() {
    if (window.__lpLenis || !window.Lenis || !desktop || reduce) return;
    var lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); } });
    window.__lpLenis = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
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
  /* O espaço reservado pela trava (pin-spacer) recebe o fundo da própria seção. Se o navegador
     perder um quadro ao soltar a trava (redesenho de camada pesada), aparece a cor da seção e não o
     fundo branco da página. */
  function paintSpacers() {
    ScrollTrigger.getAll().forEach(function (st) {
      if (!st.pin || !st.spacer || st.spacer === st.pin) return;
      var cs = getComputedStyle(st.pin);
      st.spacer.style.backgroundColor = cs.backgroundColor;
      st.spacer.style.backgroundImage = cs.backgroundImage;
    });
  }
  function run(item) {
    try { item.fn(window.gsap, window.ScrollTrigger); } catch (err) { if (window.console) console.error('[LP]', err); }
  }
  function start() {
    if (started) return;
    started = true;
    if (edit()) { queue.forEach(function (q) { if (q.edit) q.edit(); }); return; }
    libs().then(function () {
      if (!window.gsap || !window.ScrollTrigger) { queue.forEach(function (q) { if (q.fallback) q.fallback(); }); return; }
      gsap.registerPlugin(ScrollTrigger);
      ScrollTrigger.config({ ignoreMobileResize: true, autoRefreshEvents: 'visibilitychange,DOMContentLoaded,load' });
      smooth();
      queue.sort(byPosition).forEach(run);
      ready = true;
      paintSpacers();
      ScrollTrigger.addEventListener('refresh', paintSpacers);
      // Recalcular as travas no meio de uma rolagem faz a página pular. Os recálculos (fontes,
      // fim do carregamento, imagens tardias) esperam a rolagem parar.
      var idleTimer, lastY = -1;
      var refresh = function () {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(function () {
          var y = window.scrollY;
          if (y !== lastY) { lastY = y; return refresh(); } // ainda rolando: espera mais
          lastY = -1;
          ScrollTrigger.refresh();
        }, 250);
      };
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
      window.addEventListener('load', refresh);
      Array.prototype.forEach.call(document.images, function (img) {
        if (!img.complete) img.addEventListener('load', refresh, { once: true });
      });
    });
  }
  window.lpScroll = {
    /* el: elemento da seção (define a ordem); fn(gsap, ScrollTrigger): cria as animações;
       opts.edit: estado final no editor; opts.fallback: sem GSAP (CDN bloqueado). */
    add: function (el, fn, opts) {
      if (!el) return;
      var item = { el: el, fn: fn, edit: opts && opts.edit, fallback: opts && opts.fallback };
      queue.push(item);
      if (ready) { run(item); if (ScrollTrigger.sort) ScrollTrigger.sort(); ScrollTrigger.refresh(); }
    },
    reduce: reduce,
    /* Atraso das animações presas: com a rolagem suave (Lenis) ela já suaviza, então a animação
       acompanha direto; sem Lenis (celular), um atraso curto. */
    scrub: function () { return window.__lpLenis ? true : 0.4; },
    anticipate: function () { return window.__lpLenis ? 0 : 1; },
    /* Com a rolagem suave (desktop), a trava segura a seção com transform: ela nunca troca de
       "fixa na tela" para "no fluxo da página", troca que obriga o navegador a redesenhar a camada
       inteira e às vezes pular um quadro (a seção "some" ao soltar). No celular, rolagem nativa: fixed. */
    pinType: function () { return window.__lpLenis ? 'transform' : 'fixed'; }
  };
  // Espera os widgets registrarem as seções (eles fazem isso no DOMContentLoaded) antes de começar.
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(start, 0); });
  else setTimeout(start, 0);
})();
