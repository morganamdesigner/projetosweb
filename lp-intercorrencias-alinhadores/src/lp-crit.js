/* 03b · Sem critério: seção presa com scrub. Também liga a rolagem suave (Lenis) no desktop,
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
    var content = $('.lp-crit-content'), over = $('.lp-crit-over'), l1 = $('.lp-crit-l1'), word = $('.lp-crit-word');
    var path = $('.lp-crit-line path'), hint = $('.lp-crit-hint'), hex = $('.lp-crit-hex'), fade = $('.lp-crit-fade');
    if (!content || !word) return;
    var title = word.querySelector('.elementor-heading-title') || word;
    var mobile = window.matchMedia('(max-width: 767px)').matches;

    gsap.set([over, l1].filter(Boolean), { autoAlpha: 0, y: 34, filter: 'blur(8px)' });
    gsap.set(title, { scale: mobile ? 1.18 : 1.3, filter: 'blur(' + (mobile ? 14 : 22) + 'px)', autoAlpha: 0.25 });
    if (path) gsap.set(path, { '--draw': 1 });
    if (hint) gsap.set(hint, { autoAlpha: 0, y: 10 });

    var tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: sec, start: 'top top', end: mobile ? '+=140%' : '+=190%',
        pin: true, scrub: mobile ? 0.6 : 1, invalidateOnRefresh: true
      }
    });
    tl.to([over, l1].filter(Boolean), { autoAlpha: 1, y: 0, filter: 'blur(0px)', stagger: 0.06, duration: 0.22, ease: 'power2.out' })
      .to(title, { scale: 1, filter: 'blur(0px)', autoAlpha: 1, duration: 0.42, ease: 'power2.out' }, '<0.05');
    if (path) tl.to(path, { '--draw': 0, duration: 0.22 }, '>-0.08');
    if (hint) tl.to(hint, { autoAlpha: 1, y: 0, duration: 0.08 }, '>-0.05');
    tl.to({}, { duration: 0.14 }) // segura a frase nítida por um instante
      .to(content, { scale: 0.92, y: -30, autoAlpha: 0, filter: 'blur(10px)', duration: 0.26, ease: 'power1.in' })
      .to(fade, { opacity: 1, duration: 0.26, ease: 'power1.in' }, '<0.04');
    if (hex) tl.fromTo(hex, { y: 30 }, { y: -50, duration: tl.duration() }, 0);
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
