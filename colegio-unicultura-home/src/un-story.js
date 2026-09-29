/* Colégio Unicultura | Home - hero "do primeiro dia à formatura" (CSS em un-story.css).
   Ciclo automático e suave: primeiro dia (parado) -> a formatura surge num fade -> formatura
   (parada) -> volta. Só alterna a classe .is-future no cartão; a transição é feita no CSS.
   No editor do Elementor e com "reduzir movimento" fica parado no "primeiro dia". */
(function () {
  var script = document.currentScript;
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var card = script && script.closest('.un-hero');
  if (!card || !card.querySelector('.un-story')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  var HOLD = 5000;  // ms em cada foto (o fade dura ~1,8s, no CSS)

  window.setInterval(function () {
    if (!document.hidden) {
      card.classList.toggle('is-future');
    }
  }, HOLD);
})();
