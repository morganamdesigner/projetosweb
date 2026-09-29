/* Garatuja | Seção "E depois da Garatuja?": marca a seção com .is-in quando ela aparece
   (a trilha se desenha e o marca-texto pinta o título). Sem JS/no editor, tudo aparece pronto. */
(function () {
  var script = document.currentScript;
  var section = script && script.closest('.gt-next');
  if (!section || document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    return;
  }
  section.classList.add('gt-js');
  var observer = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) {
      section.classList.add('is-in');
      observer.disconnect();
    }
  }, { threshold: 0.3 });
  observer.observe(section);
})();
