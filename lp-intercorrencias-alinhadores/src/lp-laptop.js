/* Notebook da seção 04: a tela "trava" (pin) e o notebook abre aos poucos conforme o scroll.
   Etapas: a tampa sobe (0–55%), a tela acende (45–70%) e a página rola no leitor (70–100%).
   Com GSAP + ScrollTrigger usa pin + scrub (também no celular); sem GSAP, abre sem travar.
   No editor do Elementor e com movimento reduzido, fica aberto. */
(function () {
  if (window.__lpLaptop) return;
  window.__lpLaptop = true;
  var clamp = function (v) { return Math.min(1, Math.max(0, v)); };

  function setup(el) {
    if (el.dataset.lpLaptop) return;
    el.dataset.lpLaptop = '1';
    var set = function (p) {
      p = clamp(p);
      var a = clamp(p / 0.55), e = 1 - Math.pow(1 - a, 3);
      el.style.setProperty('--lid', (-80 + 80 * e).toFixed(2) + 'deg');
      el.style.setProperty('--lit', clamp((p - 0.45) / 0.25).toFixed(3));
      el.style.setProperty('--scroll', (-26 * clamp((p - 0.7) / 0.3)).toFixed(2) + '%');
    };
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var edit = document.body.classList.contains('elementor-editor-active');
    if (reduce || edit) { set(1); return; }
    set(0);
    if (window.gsap && window.ScrollTrigger) {
      gsap.registerPlugin(ScrollTrigger);
      ScrollTrigger.config({ ignoreMobileResize: true });
      var state = { p: 0 };
      gsap.to(state, {
        p: 1, ease: 'none', onUpdate: function () { set(state.p); },
        // Trava a seção inteira (não o notebook): o pai do notebook é flex e o espaçador do pin não
        // empurraria a próxima seção. A trava começa quando o notebook chega ao meio da tela.
        scrollTrigger: { trigger: el, start: 'center center', end: '+=160%', pin: el.closest('.lp-apres') || el,
                         scrub: 0.8, anticipatePin: 1, invalidateOnRefresh: true }
      });
      window.addEventListener('load', function () { ScrollTrigger.refresh(); });
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
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), setup); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
