/* Colégio Unicultura | Diferenciais - 07 Projetos (CSS em un-projetos.css).
   A linha (--un-p) se preenche enquanto as etapas sobem de 85% a 35% da tela,
   e cada etapa acende (.is-on) quando a linha chega nela. Volta ao rolar para cima.
   Não roda no editor do Elementor nem com "reduzir movimento" (fica tudo aceso). */
(function () {
  var script = document.currentScript;
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }
  var block = script && script.closest('.un-steps');
  if (!block || block.classList.contains('un-steps--js')) {
    return;
  }
  block.classList.add('un-steps--js');
  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;
    var top = block.getBoundingClientRect().top;
    var p = Math.max(0, Math.min(1, (vh * 0.85 - top) / (vh * 0.5)));
    block.style.setProperty('--un-p', p.toFixed(3));
    var items = block.querySelectorAll('.un-step');
    items.forEach(function (item, i) {
      var at = items.length > 1 ? i / (items.length - 1) : 0;
      item.classList.toggle('is-on', p > 0 && p >= at - 0.02);
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  // as etapas vêm depois deste widget no HTML: começa quando a página terminar de carregar
  function start() {
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
