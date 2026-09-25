/* Garatuja | Seção "Escola bilíngue" - a bandeira aparece no card conforme o scroll.
   A imagem é o Background Overlay do container .gt-bi-card (Estilo → Background Overlay).
   A opacidade definida lá no editor é o MÁXIMO; este script vai de 0 até esse máximo
   enquanto o card sobe na tela. Não roda dentro do editor do Elementor. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var cards = document.querySelectorAll('.gt-bilingue .gt-bi-card');
  if (!cards.length) {
    return;
  }
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = Array.prototype.map.call(cards, function (card) {
    var max = parseFloat(getComputedStyle(card).getPropertyValue('--overlay-opacity'));
    return { el: card, max: isNaN(max) ? 0.28 : max };
  });
  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;
    items.forEach(function (item) {
      var top = item.el.getBoundingClientRect().top;
      // 0 quando o topo do card entra pela base da tela (90%); 1 quando chega a 20% da altura
      var progress = Math.min(1, Math.max(0, (vh * 0.9 - top) / (vh * 0.7)));
      item.el.style.setProperty('--overlay-opacity', ((reduceMotion ? 1 : progress) * item.max).toFixed(3));
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  update();
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
})();
