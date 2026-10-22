/* Notebook da seção 04: o palco fica preso na tela (sticky) e o notebook abre com o scroll.
   Etapas: a tampa sobe (0–45%), a tela acende (30–50%) e a página rola no leitor (70–100%).
   O motor (lp-boot.js) entrega o progresso. No editor e com movimento reduzido, fica aberto. */
(function () {
  if (window.__lpLaptop) return;
  window.__lpLaptop = true;
  var clamp = function (v) { return Math.min(1, Math.max(0, v)); };

  /* A página do guia dentro da tela. Plugins de otimização (LiteSpeed, WP Rocket, Smush, Jetpack...)
     trocam a imagem por um espaço reservado e guardam o endereço real em data-src, data-lazy-src,
     srcset ou <noscript>; com o notebook preso e girando, o carregamento deles às vezes nunca acontece
     e a tela fica vazia. Aqui o endereço real é encontrado e a imagem é recriada, fora do alcance deles. */
  function realSrc(img) {
    var ok = function (u) { return u && !/^data:/.test(u) && !/placeholder|blank\.gif|lazy_placeholder/i.test(u); };
    var best = function (set) {
      if (!set) return '';
      var items = set.split(',').map(function (x) { var p = x.trim().split(/\s+/); return { u: p[0], w: parseInt(p[1], 10) || 0 }; });
      items.sort(function (a, b) { return b.w - a.w; });
      return items.length ? items[0].u : '';
    };
    var c = [img.getAttribute('data-lazy-src'), img.getAttribute('data-src'), img.getAttribute('data-orig-src'),
             img.getAttribute('data-original'), img.getAttribute('data-ll-src'),
             best(img.getAttribute('data-lazy-srcset') || img.getAttribute('data-srcset')),
             best(img.getAttribute('srcset')), img.getAttribute('src')];
    for (var i = 0; i < c.length; i++) if (ok(c[i])) return c[i];
    var ns = img.parentNode && img.parentNode.querySelector('noscript');
    var m = ns && /src=["']([^"']+)["']/.exec(ns.textContent || ns.innerHTML);
    if (m && ok(m[1])) return m[1];
    return window.lpLaptopPage || '';
  }
  function fixPage(el) {
    Array.prototype.forEach.call(el.querySelectorAll('.lp-screen-page img'), function (img) {
      if (img.dataset.lpFixed) return;
      var url = realSrc(img);
      if (!url) return;
      var fresh = document.createElement('img');
      fresh.alt = img.alt || 'Página do guia';
      fresh.decoding = 'async';
      fresh.setAttribute('data-lp-fixed', '1');
      fresh.setAttribute('data-no-lazy', '1');        // LiteSpeed / WP Rocket: não mexer
      fresh.setAttribute('data-skip-lazy', '1');      // Jetpack / Smush: não mexer
      fresh.className = 'skip-lazy no-lazyload';
      fresh.src = url;
      img.parentNode.replaceChild(fresh, img);
      var ns = fresh.parentNode.querySelector('noscript');
      if (ns) ns.parentNode.removeChild(ns);
    });
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), function (el) {
      var set = function (p) {
        var a = clamp(p / 0.45), e = 1 - Math.pow(1 - a, 3);
        el.style.setProperty('--lid', (-80 + 80 * e).toFixed(2) + 'deg');
        el.style.setProperty('--lit', clamp((p - 0.3) / 0.2).toFixed(3));
        el.style.setProperty('--scroll', (-26 * clamp((p - 0.7) / 0.3)).toFixed(2) + '%');
      };
      set(0);
      fixPage(el);
      window.lpScroll.scene(el.closest('.lp-stage') || el, {
        update: function (p) { set(p); },
        done: function () { set(1); }
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  // De novo depois do carregamento: alguns plugins só trocam a imagem depois do DOM pronto.
  window.addEventListener('load', function () {
    Array.prototype.forEach.call(document.querySelectorAll('.lp-laptop'), fixPage);
  });
})();
