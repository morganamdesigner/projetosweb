/* Colégio Unicultura | Home - adiciona .gt-scrolled ao topo da página após 40px de scroll.
   Usado pelo CSS do menu fixo (un-home.css). Não roda dentro do editor do Elementor. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var tops = document.querySelectorAll('.gt-top');
  function update() {
    var scrolled = window.scrollY > 40;
    tops.forEach(function (el) {
      el.classList.toggle('gt-scrolled', scrolled);
    });
  }
  update();
  window.addEventListener('scroll', update, { passive: true });
})();
