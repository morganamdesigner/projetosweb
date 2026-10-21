/* Notebook da seção 04: a seção trava (pin) e o notebook abre aos poucos com o scroll.
   Etapas: a tampa sobe (0–55%), a tela acende (45–70%) e a página rola no leitor (70–100%).
   Registra-se no orquestrador (lp-boot.js). No editor, sem GSAP ou com movimento reduzido, fica aberto. */
(function () {
  if (window.__lpLaptop) return;
  window.__lpLaptop = true;
  var clamp = function (v) { return Math.min(1, Math.max(0, v)); };

  function setter(el) {
    return function (p) {
      p = clamp(p);
      var a = clamp(p / 0.55), e = 1 - Math.pow(1 - a, 3);
      el.style.setProperty('--lid', (-80 + 80 * e).toFixed(2) + 'deg');
      el.style.setProperty('--lit', clamp((p - 0.45) / 0.25).toFixed(3));
      el.style.setProperty('--scroll', (-26 * clamp((p - 0.7) / 0.3)).toFixed(2) + '%');
    };
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), function (el) {
      var set = setter(el), open = function () { set(1); };
      var sec = el.closest('.lp-apres') || el;
      window.lpScroll.add(el, function (gsap) {
        if (window.lpScroll.reduce) return open();
        set(0);
        var state = { p: 0 };
        // Trava a seção inteira quando o notebook chega ao meio da tela. fromTo com valores fixos:
        // um recálculo das travas no meio da abertura não pode reler o ponto de partida.
        gsap.fromTo(state, { p: 0 }, {
          p: 1, ease: 'none', onUpdate: function () { set(state.p); },
          scrollTrigger: { trigger: el, start: 'center center', end: '+=160%', pin: sec,
                           scrub: window.lpScroll.scrub(), anticipatePin: window.lpScroll.anticipate() }
        });
      }, { edit: open, fallback: open });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
