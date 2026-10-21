/* 03b · Sem critério: painel com cantos chanfrados e seção presa com scrub.
   Registra-se no orquestrador (lp-boot.js), que cria as travas na ordem da página. */
(function () {
  if (window.__lpCrit) return;
  window.__lpCrit = true;

  function setup(sec) {
    return function (gsap) {
      var $ = function (s) { return sec.querySelector(s); };
      var over = $('.lp-crit-over'), left = $('.lp-crit-left'), right = $('.lp-crit-right'), word = $('.lp-crit-word');
      var path = $('.lp-crit-line path'), hint = $('.lp-crit-hint'), hex = $('.lp-crit-hex');
      if (!word || window.lpScroll.reduce) return;
      var title = word.querySelector('.elementor-heading-title') || word;
      var mm = gsap.matchMedia();
      mm.add({ mobile: '(max-width: 767px)', desktop: '(min-width: 768px)' }, function (ctx) {
        var mobile = ctx.conditions.mobile;
        // 2. Estado inicial da frase.
        if (over) gsap.set(over, { autoAlpha: 0, y: 14 });
        if (left) gsap.set(left, { xPercent: -140, autoAlpha: 0 });
        if (right) gsap.set(right, { xPercent: 140, autoAlpha: 0 });
        gsap.set(title, { scale: mobile ? 1.7 : 2.1, filter: 'blur(' + (mobile ? 16 : 26) + 'px)', autoAlpha: 0 });
        if (path) gsap.set(path, { '--draw': 1 });
        if (hint) gsap.set(hint, { autoAlpha: 0, y: 10 });
        // 3. Seção presa: data → metades pelas laterais → palavra em foco → traço → dica → pausa.
        var tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: sec, start: 'top top', end: mobile ? '+=170%' : '+=230%',
                           pin: true, scrub: window.lpScroll.scrub(), anticipatePin: window.lpScroll.anticipate() }
        });
        if (over) tl.to(over, { autoAlpha: 1, y: 0, duration: 0.08 });
        tl.to([left, right].filter(Boolean), { xPercent: 0, autoAlpha: 1, duration: 0.24, ease: 'power3.out' }, '>-0.02')
          .to(title, { autoAlpha: 1, duration: 0.06 }, '<0.12')
          .to(title, { scale: 1, filter: 'blur(0px)', duration: 0.36, ease: 'power2.out' }, '<')
          .set(title, { filter: 'none' }); // sem filtro depois do foco: camada leve na hora de soltar a trava
        if (path) tl.to(path, { '--draw': 0, duration: 0.16 }, '>-0.04');
        if (hint) tl.to(hint, { autoAlpha: 1, y: 0, duration: 0.07 }, '>-0.02');
        tl.to({}, { duration: 0.22 }); // segura a frase pronta antes de a seção seguir
        if (hex) tl.fromTo(hex, { y: 40 }, { y: -40, duration: tl.duration() }, 0);
        // 1. Entrada: o painel sobe com os cantos de cima chanfrados, que se abrem até a tela cheia.
        //    O recorte vale também para o espaço da trava (pin-spacer), que tem o fundo da seção.
        var spacer = sec.parentNode && sec.parentNode.classList.contains('pin-spacer') ? sec.parentNode : null;
        gsap.fromTo([sec, spacer].filter(Boolean), { '--chamfer': mobile ? '36px' : '84px' }, {
          '--chamfer': '0px', ease: 'none',
          scrollTrigger: { trigger: spacer || sec, start: 'top bottom', end: 'top top', scrub: true }
        });
      });
    };
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll('.lp-crit'), function (sec) {
      window.lpScroll.add(sec, setup(sec));
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
