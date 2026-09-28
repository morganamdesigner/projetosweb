/* Colégio Unicultura | Ensino Fundamental I - efeitos de scroll (CSS em un-fund1.css).
   Não roda no editor do Elementor; com "reduzir movimento", tudo aparece direto. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion || !('IntersectionObserver' in window)) {
    return;
  }
  document.documentElement.classList.add('un-js');

  /* 1. .un-io ganha .is-in quando entra na tela (selo da foto, marca-texto, pílula).
        Este script fica no topo da página: espera o resto do HTML carregar. */
  function watch() {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.35 });
    document.querySelectorAll('.un-io').forEach(function (el) {
      observer.observe(el);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }

  /* 2. Hero: --un-out vai de 0 a 1 enquanto o cartão sai da tela (o CSS usa só no desktop) */
  var hero = document.querySelector('.un-top .un-hero');
  if (!hero) {
    return;
  }
  var ticking = false;
  function update() {
    ticking = false;
    var height = hero.offsetHeight || 1;
    var out = Math.max(0, Math.min(1, window.scrollY / height));
    hero.style.setProperty('--un-out', out.toFixed(3));
  }
  window.addEventListener('scroll', function () {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }, { passive: true });
  update();
})();
