/* Notebook da seção 04: abre conforme o scroll (GSAP ScrollTrigger se estiver na página; senão,
   cálculo próprio no scroll). No editor do Elementor e com movimento reduzido, fica aberto. */
(function () {
  if (window.__lpLaptop) return;
  window.__lpLaptop = true;

  function init() {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var edit = document.body.classList.contains('elementor-editor-active');
    Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), function (el) {
      var lid = el.querySelector('.lp-lid');
      if (!lid) return;
      var set = function (p) {
        p = Math.min(1, Math.max(0, p));
        var e = 1 - Math.pow(1 - p, 3);
        el.style.setProperty('--lid', (-100 + 100 * e).toFixed(2) + 'deg');
        el.style.setProperty('--lit', Math.max(0, (p - 0.45) / 0.55).toFixed(3));
        el.style.setProperty('--scroll', (-22 * Math.max(0, (p - 0.6) / 0.4)).toFixed(2) + '%');
      };
      if (reduce || edit) { set(1); return; }
      set(0);
      if (window.gsap && window.ScrollTrigger) {
        gsap.registerPlugin(ScrollTrigger);
        ScrollTrigger.create({ trigger: el, start: 'top 90%', end: 'center 45%', onUpdate: function (st) { set(st.progress); } });
        return;
      }
      var tick = false;
      var calc = function () {
        tick = false;
        var r = el.getBoundingClientRect(), vh = window.innerHeight;
        var start = vh * 0.9, end = vh * 0.45 - r.height / 2;
        set((start - r.top) / Math.max(1, start - end));
      };
      window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(calc); } }, { passive: true });
      window.addEventListener('resize', calc);
      calc();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
