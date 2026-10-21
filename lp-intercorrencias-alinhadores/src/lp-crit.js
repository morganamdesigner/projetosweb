/* 03b · Sem critério: o palco fica preso na tela (sticky) e a frase se monta com o scroll.
   O motor (lp-boot.js) entrega o progresso; aqui só se aplica na linha do tempo (pausada). */
(function () {
  if (window.__lpCrit) return;
  window.__lpCrit = true;

  function scene(sec) {
    var $ = function (s) { return sec.querySelector(s); };
    var over = $('.lp-crit-over'), left = $('.lp-crit-left'), right = $('.lp-crit-right'), word = $('.lp-crit-word');
    var path = $('.lp-crit-line path'), hint = $('.lp-crit-hint'), hex = $('.lp-crit-hex');
    if (!word) return;
    var title = word.querySelector('.elementor-heading-title') || word;
    var tl = null, chamfer = 0;
    window.lpScroll.scene(sec, {
      init: function (gsap) {
        if (!gsap) return;
        var mobile = window.matchMedia('(max-width: 767px)').matches;
        chamfer = mobile ? 36 : 84;
        tl = gsap.timeline({ paused: true, defaults: { ease: 'none' } });
        if (over) tl.fromTo(over, { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.08 });
        tl.fromTo(left, { xPercent: -140, autoAlpha: 0 }, { xPercent: 0, autoAlpha: 1, duration: 0.24, ease: 'power3.out' }, '>-0.02')
          .fromTo(right, { xPercent: 140, autoAlpha: 0 }, { xPercent: 0, autoAlpha: 1, duration: 0.24, ease: 'power3.out' }, '<')
          .fromTo(title, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.06 }, '<0.12')
          .fromTo(title, { scale: mobile ? 1.7 : 2.1, filter: 'blur(' + (mobile ? 16 : 26) + 'px)' },
                         { scale: 1, filter: 'blur(0px)', duration: 0.36, ease: 'power2.out' }, '<')
          .set(title, { filter: 'none' }); // sem filtro depois do foco: camada leve
        if (path) tl.fromTo(path, { '--draw': 1 }, { '--draw': 0, duration: 0.16 }, '>-0.04');
        if (hint) tl.fromTo(hint, { autoAlpha: 0, y: 10 }, { autoAlpha: 1, y: 0, duration: 0.07 }, '>-0.02');
        tl.to({}, { duration: 0.22 }); // segura a frase pronta antes de a seção seguir
        if (hex) tl.fromTo(hex, { y: 40 }, { y: -40, duration: tl.duration() }, 0);
        tl.progress(0);
      },
      update: function (p, enter) {
        // Cantos de cima chanfrados enquanto o painel sobe; abertos quando ele chega ao topo.
        sec.style.setProperty('--chamfer', (chamfer * (1 - enter)).toFixed(1) + 'px');
        if (tl) tl.progress(p);
      }
    });
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('.lp-crit'), scene); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
