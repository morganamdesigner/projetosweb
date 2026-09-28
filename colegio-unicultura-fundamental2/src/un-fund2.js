/* Colégio Unicultura | Ensino Fundamental II - linha do tempo dos "Três eixos" (CSS em un-fund2.css).
   Escreve --un-fill (0 a 1) em cada .un-timeline conforme ela passa pelo meio da tela.
   Não roda no editor do Elementor nem com "reduzir movimento" (a linha fica cheia). */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }
  var timelines = [];
  var ticking = false;

  function update() {
    ticking = false;
    var mark = window.innerHeight * 0.6;
    timelines.forEach(function (line) {
      var rect = line.getBoundingClientRect();
      var fill = (mark - rect.top) / (rect.height || 1);
      line.style.setProperty('--un-fill', Math.max(0, Math.min(1, fill)).toFixed(3));
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  // este script fica no topo da página: espera o resto do HTML carregar
  function start() {
    timelines = Array.prototype.slice.call(document.querySelectorAll('.un-timeline'));
    if (!timelines.length) {
      return;
    }
    update();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
