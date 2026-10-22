/* Notebook da seção 04: o palco fica preso na tela (sticky) e o notebook abre com o scroll.
   Etapas: a tampa sobe (0–55%), a tela acende (45–70%) e a página rola no leitor (70–100%).
   O motor (lp-boot.js) entrega o progresso. No editor e com movimento reduzido, fica aberto. */
(function () {
  if (window.__lpLaptop) return;
  window.__lpLaptop = true;
  var clamp = function (v) { return Math.min(1, Math.max(0, v)); };

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), function (el) {
      var set = function (p) {
        var a = clamp(p / 0.55), e = 1 - Math.pow(1 - a, 3);
        el.style.setProperty('--lid', (-80 + 80 * e).toFixed(2) + 'deg');
        el.style.setProperty('--lit', clamp((p - 0.45) / 0.25).toFixed(3));
        el.style.setProperty('--scroll', (-26 * clamp((p - 0.7) / 0.3)).toFixed(2) + '%');
      };
      set(0);
      // A página do guia carrega logo: o lazy load do WordPress não "vê" a imagem com a tampa inclinada.
      Array.prototype.forEach.call(el.querySelectorAll('.lp-screen-page img'), function (img) {
        img.loading = 'eager';
        img.removeAttribute('loading');
        if (img.dataset && img.dataset.src && !img.getAttribute('src')) img.src = img.dataset.src;
        if (img.dataset && img.dataset.lazySrc) img.src = img.dataset.lazySrc;
        if (img.dataset && img.dataset.srcset) img.srcset = img.dataset.srcset;
      });
      window.lpScroll.scene(el.closest('.lp-stage') || el, {
        update: function (p) { set(p); },
        done: function () { set(1); }
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
