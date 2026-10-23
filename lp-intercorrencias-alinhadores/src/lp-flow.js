/* 05 · Por dentro: coverflow 3D automático. A página do centro avança sozinha a cada 3,2 s, pausa
   com o mouse em cima, aceita arrastar e clique nas laterais (traz para o centro); o clique na página
   do centro abre a ampliação do Elementor. Só anima com a seção na tela. */
(function () {
  if (window.__lpFlow) return;
  window.__lpFlow = true;
  var DUR = 3200;
  var LEVELS = { // distância do centro: deslocamento (em larguras), escala, giro, opacidade, brilho
    desktop: [[0, 1, 0, 1, 1], [0.7, 0.8, -28, 0.9, 0.72], [1.25, 0.64, -38, 0.55, 0.5]],
    mobile: [[0, 1, 0, 1, 1], [0.62, 0.8, -26, 0.85, 0.7], [1.05, 0.62, -34, 0.0, 0.5]]
  };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var svg = function (d) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="' + d + '"/></svg>'; };

  function setup(flow) {
    var items = Array.prototype.filter.call(flow.children, function (c) { return c.classList.contains('lp-flow-item'); });
    var n = items.length;
    if (n < 2) return;
    var active = 0, timer = null, visible = false, hover = false, mobile = false;

    var glow = document.createElement('div'); glow.className = 'lp-flow-glow'; flow.insertBefore(glow, flow.firstChild);
    var nav = document.createElement('div'); nav.className = 'lp-flow-nav';
    nav.innerHTML = '<button type="button" class="lp-flow-btn" aria-label="Página anterior">' + svg('M15 5l-7 7 7 7') + '</button>' +
      '<div class="lp-flow-dots" role="tablist"></div>' +
      '<button type="button" class="lp-flow-btn" aria-label="Próxima página">' + svg('M9 5l7 7-7 7') + '</button>';
    flow.parentNode.insertBefore(nav, flow.nextSibling);
    var dotsBox = nav.querySelector('.lp-flow-dots'), dots = [];
    items.forEach(function (it, i) {
      var d = document.createElement('button');
      d.type = 'button'; d.className = 'lp-flow-dot'; d.setAttribute('aria-label', 'Ir para a página ' + (i + 1));
      d.addEventListener('click', function () { go(i); });
      dotsBox.appendChild(d); dots.push(d);
    });
    nav.firstChild.addEventListener('click', function () { go(active - 1); });
    nav.lastChild.addEventListener('click', function () { go(active + 1); });
    flow.style.setProperty('--dur', DUR + 'ms');

    function layout() {
      mobile = window.matchMedia('(max-width: 767px)').matches;
      var L = mobile ? LEVELS.mobile : LEVELS.desktop;
      items.forEach(function (it, i) {
        var d = ((i - active) % n + n) % n;
        if (d > n / 2) d -= n;                                  // distância com sinal, dando a volta
        var a = Math.abs(d), s = d < 0 ? -1 : 1, v = L[Math.min(a, 2)];
        it.style.setProperty('--x', (s * v[0]).toFixed(3));
        it.style.setProperty('--s', v[1]);
        it.style.setProperty('--r', (s * v[2]).toFixed(1));
        it.style.setProperty('--o', a > 2 ? 0 : v[3]);
        it.style.setProperty('--b', v[4]);
        it.style.setProperty('--z', 10 - a);
        it.classList.toggle('is-active', a === 0);
        it.setAttribute('aria-hidden', a === 0 ? 'false' : 'true');
      });
      dots.forEach(function (d, i) {
        d.classList.remove('is-active');
        if (i === active) { void d.offsetWidth; d.classList.add('is-active'); } // reinicia a barra de tempo
      });
    }
    function go(i) { active = ((i % n) + n) % n; layout(); schedule(); }
    function schedule() {
      clearTimeout(timer);
      var run = visible && !hover && !reduce && !document.hidden;
      flow.classList.toggle('is-paused', !run);
      if (run) timer = setTimeout(function () { go(active + 1); }, DUR);
    }

    // Clique: lateral vem para o centro; centro abre a ampliação (lightbox do Elementor).
    var dragX = null, dragged = false;
    flow.addEventListener('click', function (e) {
      var it = e.target.closest('.lp-flow-item');
      if (dragged || (it && !it.classList.contains('is-active'))) {
        e.preventDefault(); e.stopPropagation();
        if (!dragged && it) go(items.indexOf(it));
      }
      dragged = false;
    }, true);
    flow.addEventListener('pointerdown', function (e) { dragX = e.clientX; dragged = false; });
    window.addEventListener('pointerup', function (e) {
      if (dragX === null) return;
      var dx = e.clientX - dragX; dragX = null;
      if (Math.abs(dx) > 40) { dragged = true; go(active + (dx < 0 ? 1 : -1)); }
    });
    flow.addEventListener('dragstart', function (e) { e.preventDefault(); });
    flow.addEventListener('mouseenter', function () { hover = true; schedule(); });
    flow.addEventListener('mouseleave', function () { hover = false; schedule(); });
    document.addEventListener('visibilitychange', schedule);
    window.addEventListener('resize', function () { var m = window.matchMedia('(max-width: 767px)').matches; if (m !== mobile) layout(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; schedule(); }, { threshold: 0.25 }).observe(flow);
    } else { visible = true; }

    layout();
    flow.classList.add('is-ready');
    schedule();
  }

  function init() {
    if (document.body.classList.contains('elementor-editor-active')) return;
    Array.prototype.forEach.call(document.querySelectorAll('.lp-flow'), setup);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
