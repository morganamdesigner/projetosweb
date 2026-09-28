/* Colégio Unicultura | Diferenciais - 07 Projetos (CSS em un-projetos.css).
   1. Mede as bolinhas numeradas e posiciona a linha do centro da primeira ao da última
      (horizontal se estão lado a lado, vertical se estão empilhadas).
   2. A linha (--un-p) se preenche enquanto as etapas sobem de 85% a 35% da tela e cada
      etapa acende (.is-on) quando a linha chega nela. Volta ao rolar para cima.
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

  function dotCenter(step, box) {
    var dot = step.querySelector('.un-step-dot .elementor-heading-title') || step;
    var r = dot.getBoundingClientRect();
    return { x: r.left + r.width / 2 - box.left, y: r.top + r.height / 2 - box.top };
  }

  function place() {
    var items = block.querySelectorAll('.un-step');
    if (items.length < 2) {
      return;
    }
    var box = block.getBoundingClientRect();
    var a = dotCenter(items[0], box);
    var b = dotCenter(items[items.length - 1], box);
    var vertical = Math.abs(b.y - a.y) > Math.abs(b.x - a.x);
    block.classList.toggle('un-steps--v', vertical);
    if (vertical) {
      block.style.setProperty('--un-lx', (a.x - 1).toFixed(1) + 'px');
      block.style.setProperty('--un-ly', a.y.toFixed(1) + 'px');
      block.style.setProperty('--un-lb', (box.height - b.y).toFixed(1) + 'px');
    } else {
      block.style.setProperty('--un-lx', a.x.toFixed(1) + 'px');
      block.style.setProperty('--un-lr', (box.width - b.x).toFixed(1) + 'px');
      block.style.setProperty('--un-ly', (a.y - 1).toFixed(1) + 'px');
    }
  }

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
    place();
    update();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', function () {
      place();
      requestUpdate();
    });
    window.addEventListener('load', place); // fontes carregadas mudam o tamanho das bolinhas
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
