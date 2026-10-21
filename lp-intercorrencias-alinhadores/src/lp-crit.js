/* 03b · Sem critério: entrada do painel com cantos chanfrados e seção presa com scrub. Também liga a rolagem suave (Lenis) no desktop,
   sincronizada com o ScrollTrigger, para as passagens entre seções ficarem fluidas.
   Carrega GSAP/ScrollTrigger/Lenis do CDN se ainda não estiverem na página. */
(function () {
  if (window.__lpCrit) return;
  window.__lpCrit = true;

  var CDN = {
    gsap: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js',
    st: 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js',
    lenis: 'https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js'
  };
  function load(src, ok) {
    var s = document.createElement('script');
    s.src = src; s.onload = ok; s.onerror = ok;
    document.head.appendChild(s);
  }
  function need(cb) {
    var steps = [];
    if (!window.gsap) steps.push(CDN.gsap);
    if (!window.ScrollTrigger) steps.push(CDN.st);
    if (!window.Lenis) steps.push(CDN.lenis);
    (function next() { if (!steps.length) return cb(); load(steps.shift(), next); })();
  }

  var edit = function () { return document.body.classList.contains('elementor-editor-active'); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function smoothScroll() {
    if (window.__lpLenis || !window.Lenis || reduce || edit()) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return; // só desktop
    var lenis = new Lenis({ duration: 1.15, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); } });
    window.__lpLenis = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
    // Links de âncora (#oferta, #por-dentro) com a mesma rolagem suave.
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute('href');
      var target = id.length > 1 && document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      lenis.scrollTo(target, { offset: -50 });
    }, true);
  }

  function section(sec) {
    var $ = function (s) { return sec.querySelector(s); };
    var over = $('.lp-crit-over'), left = $('.lp-crit-left'), right = $('.lp-crit-right'), word = $('.lp-crit-word');
    var path = $('.lp-crit-line path'), hint = $('.lp-crit-hint'), hex = $('.lp-crit-hex');
    if (!word) return;
    var title = word.querySelector('.elementor-heading-title') || word;
    var mobile = window.matchMedia('(max-width: 767px)').matches;

    // 1. Entrada: o painel sobe com os cantos de cima chanfrados, que se abrem até a tela cheia.
    gsap.fromTo(sec, { '--chamfer': mobile ? '36px' : '84px' }, {
      '--chamfer': '0px', ease: 'none',
      scrollTrigger: { trigger: sec, start: 'top bottom', end: 'top top', scrub: true }
    });

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
      scrollTrigger: {
        trigger: sec, start: 'top top', end: mobile ? '+=170%' : '+=230%',
        pin: true, scrub: mobile ? 0.6 : 1, invalidateOnRefresh: true
      }
    });
    if (over) tl.to(over, { autoAlpha: 1, y: 0, duration: 0.08 });
    tl.to([left, right].filter(Boolean), { xPercent: 0, autoAlpha: 1, duration: 0.24, ease: 'power3.out' }, '>-0.02')
      .to(title, { autoAlpha: 1, duration: 0.06 }, '<0.12')
      .to(title, { scale: 1, filter: 'blur(0px)', duration: 0.36, ease: 'power2.out' }, '<');
    if (path) tl.to(path, { '--draw': 0, duration: 0.16 }, '>-0.04');
    if (hint) tl.to(hint, { autoAlpha: 1, y: 0, duration: 0.07 }, '>-0.02');
    tl.to({}, { duration: 0.22 }); // segura a frase pronta antes de a seção seguir
    if (hex) tl.fromTo(hex, { y: 40 }, { y: -40, duration: tl.duration() }, 0);
  }

  function init() {
    var secs = document.querySelectorAll('.lp-crit');
    if (!secs.length) return;
    if (reduce || edit()) return; // conteúdo fica visível e parado
    need(function () {
      if (!window.gsap || !window.ScrollTrigger) return;
      gsap.registerPlugin(ScrollTrigger);
      ScrollTrigger.config({ ignoreMobileResize: true });
      smoothScroll();
      Array.prototype.forEach.call(secs, section);
      var refresh = function () { ScrollTrigger.refresh(); };
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(refresh);
      window.addEventListener('load', refresh);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
