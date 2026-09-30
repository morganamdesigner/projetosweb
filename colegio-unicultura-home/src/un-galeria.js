/* Unicultura | Seção Galeria - as fileiras deslizam em sentidos opostos com o scroll.
   Escreve --un-gal-shift em cada .un-gal-row (o CSS aplica o translate).
   Não roda no editor do Elementor nem com "reduzir movimento". */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }
  var sections = document.querySelectorAll('.un-gal');
  if (!sections.length) {
    return;
  }
  var ticking = false;

  function update() {
    ticking = false;
    var vh = window.innerHeight;
    sections.forEach(function (section) {
      var rect = section.getBoundingClientRect();
      if (rect.bottom < 0 || rect.top > vh) {
        return;
      }
      // -1 quando a seção entra por baixo, +1 quando sai por cima
      var progress = ((vh - rect.top) / (vh + rect.height)) * 2 - 1;
      var amount = Math.max(-1, Math.min(1, progress)) * 120;
      section.querySelectorAll('.un-gal-row').forEach(function (row) {
        var dir = row.classList.contains('un-gal-row--right') ? 1 : -1;
        row.style.setProperty('--un-gal-shift', (amount * dir).toFixed(1) + 'px');
      });
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  requestUpdate();  // no próximo quadro, não durante o carregamento
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
})();
