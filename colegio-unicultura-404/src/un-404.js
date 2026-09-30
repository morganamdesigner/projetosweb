/* Colégio Unicultura | Página 404 (CSS em un-404.css).
   A agulha da bússola "procura" o caminho e depois aponta para o botão "Voltar para a Home".
   Com o mouse (ou o foco do teclado) num botão/link da página, ela aponta para ele. */
(function () {
  var script = document.currentScript;
  var page = script && script.closest('.un-404');
  var needle = page && page.querySelector('.un-404-needle');
  if (!needle) {
    return;
  }
  var home = null;  // o botão vem depois deste widget: procurado quando a página carrega
  var current = 0;

  function pointTo(target) {
    if (!target) {
      return;
    }
    var n = needle.getBoundingClientRect();
    var t = target.getBoundingClientRect();
    var dx = t.left + t.width / 2 - (n.left + n.width / 2);
    var dy = t.top + t.height / 2 - (n.top + n.height / 2);
    var angle = Math.atan2(dx, -dy) * 180 / Math.PI;
    // gira pelo caminho mais curto
    while (angle - current > 180) { angle -= 360; }
    while (angle - current < -180) { angle += 360; }
    current = angle;
    page.style.setProperty('--un-404-a', angle.toFixed(1) + 'deg');
  }

  function pointHome() {
    pointTo(home);
  }

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function start() {
    home = page.querySelector('.un-404-home .elementor-button');
    page.querySelectorAll('.elementor-button').forEach(function (btn) {
      btn.addEventListener('pointerenter', function () { pointTo(btn); });
      btn.addEventListener('focus', function () { pointTo(btn); });
      btn.addEventListener('pointerleave', pointHome);
      btn.addEventListener('blur', pointHome);
    });
    pointHome();
    if (!reduceMotion) {
      page.classList.add('is-seeking');
      needle.addEventListener('animationend', function () {
        page.classList.remove('is-seeking');
      }, { once: true });
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
  window.addEventListener('load', pointHome);
  window.addEventListener('resize', pointHome);
})();
