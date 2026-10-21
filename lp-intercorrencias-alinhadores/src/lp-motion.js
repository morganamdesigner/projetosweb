/* LP · Intercorrências com Alinhadores
   Interações que o Elementor não faz sozinho. Cada bloco procura as classes lp-* dos containers
   e widgets nativos e sai em silêncio se a seção não existir. As travas com GSAP (seções 03,
   03b e 04) são criadas pelo orquestrador (lp-boot.js), na ordem da página. */
(function () {
  if (window.__lpMotion) return;
  window.__lpMotion = true;

  var doc = document.documentElement;
  doc.classList.add('lp-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  var pad = function (n, l) { n = String(n); while (n.length < l) n = '0' + n; return n; };
  var title = function (el) { return el && (el.querySelector('.elementor-heading-title') || el); };

  /* Revela uma vez ao entrar na tela (threshold 20%). A checagem no scroll cobre saltos por
     âncora e scroll muito rápido, quando o elemento passa sem chegar a "entrar" na tela. */
  function onceInView(els, cb, threshold) {
    if (!els.length) return;
    var pending = els.slice(), tick = false;
    var fire = function (el) { var i = pending.indexOf(el); if (i > -1) { pending.splice(i, 1); cb(el); } };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); fire(e.target); } });
      }, { threshold: threshold || 0.2 });
      els.forEach(function (el) { io.observe(el); });
    }
    var check = function () {
      tick = false;
      pending.slice().forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight * 0.8) fire(el); });
      if (!pending.length) window.removeEventListener('scroll', onScroll);
    };
    var onScroll = function () { if (!tick) { tick = true; requestAnimationFrame(check); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    check();
  }

  function initReveal() {
    onceInView($$('.lp-io'), function (el) { el.classList.add('is-inview'); });
  }

  /* 00 e 02 · Marquee: duplica os itens até cobrir duas larguras de tela */
  function initMarquee() {
    $$('.lp-marquee__track').forEach(function (track) {
      if (track.dataset.lpReady) return;
      track.dataset.lpReady = '1';
      var items = $$(':scope > .elementor-element', track);
      if (!items.length) return;
      var guard = 0;
      while (track.scrollWidth < window.innerWidth * 1.2 && guard++ < 12) {
        items.forEach(function (it) { track.appendChild(it.cloneNode(true)); });
      }
      $$(':scope > .elementor-element', track).forEach(function (it) {
        var c = it.cloneNode(true); c.setAttribute('aria-hidden', 'true'); track.appendChild(c);
      });
    });
  }

  /* 03 · Dor: cena de 150 quadros dirigida pelo scroll */
  function initScene() {
    var box = $('.lp-scene');
    var sec = box && box.closest('.lp-dor');
    if (!sec) return;
    var cv = $('canvas', box), ctx = cv.getContext('2d');
    var tpl = box.getAttribute('data-frames'), N = parseInt(box.getAttribute('data-count'), 10) || 150;
    var stops = [];
    try { stops = JSON.parse(box.getAttribute('data-stops') || '[]'); } catch (e) { stops = []; }
    var rows = $$('.lp-dor-row', sec), q = $('.lp-dor-q', sec);
    var ring = $('.lp-scene__ring', box), lab = $('.lp-scene__label', box), bars = $$('.lp-scene__prog span', box);
    var imgs = new Array(N), want = 0, last = -1, started = false;

    function draw(k, force) {
      for (var j = k; j >= 0; j--) {
        var im = imgs[j];
        if (im && im.complete && im.naturalWidth) {
          if (j === last && !force) return;
          ctx.clearRect(0, 0, cv.width, cv.height);
          ctx.drawImage(im, 0, 0, cv.width, cv.height);
          last = j;
          return;
        }
      }
    }
    function load() {
      if (started || !tpl) return;
      started = true;
      for (var i = 0; i < N; i++) {
        (function (i) {
          var im = new Image();
          im.decoding = 'async';
          im.onload = function () { if (i === 0 || i <= want) draw(want, true); };
          im.src = tpl.replace('{n}', pad(i, 3));
          imgs[i] = im;
        })(i);
      }
    }
    function update(p) {
      want = Math.round(p * (N - 1));
      draw(want);
      rows.forEach(function (r, i) { var on = stops[i] ? p >= stops[i].from : p > 0.9; r.classList.toggle('is-on', on); if (bars[i]) bars[i].classList.toggle('is-on', on); });
      if (q) q.classList.toggle('is-on', p >= 0.9);
      var s = null;
      stops.forEach(function (st) { if (p >= st.from && p < st.to) s = st; });
      if (lab) {
        lab.classList.toggle('is-show', !!s);
        if (s) { lab.firstElementChild.textContent = s.n; lab.lastElementChild.textContent = s.t; }
      }
      if (ring) ring.classList.toggle('is-show', !!s && s.ring !== false);
    }

    onceInView([sec], load, 0);
    if ('IntersectionObserver' in window) {
      var pre = new IntersectionObserver(function (e) { if (e[0].isIntersecting) { load(); pre.disconnect(); } }, { rootMargin: '1200px 0px' });
      pre.observe(sec);
    } else { load(); }

    if (reduce) { update(1); return; }
    var scrollFallback = function () {
      var tick = false;
      var calc = function () {
        tick = false;
        var r = sec.getBoundingClientRect(), vh = window.innerHeight;
        update(clamp((vh * 0.65 - r.top) / Math.max(1, r.height), 0, 1));
      };
      window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(calc); } }, { passive: true });
      calc();
    };
    // A trava é criada pelo orquestrador (lp-boot.js), na ordem da página.
    window.lpScroll.add(sec, function (gsap, ScrollTrigger) {
      var mm = gsap.matchMedia();
      mm.add('(min-width: 768px)', function () {
        ScrollTrigger.create({ trigger: sec, start: 'top top', end: '+=300%', pin: true,
                               anticipatePin: window.lpScroll.anticipate(), pinType: window.lpScroll.pinType(),
                               onUpdate: function (st) { update(st.progress); } });
      });
      mm.add('(max-width: 767px)', function () {
        ScrollTrigger.create({ trigger: sec, start: 'top 65%', end: 'bottom 35%', onUpdate: function (st) { update(st.progress); } });
      });
    }, { edit: function () { update(1); }, fallback: scrollFallback });
  }

  /* 06 · Agenda: a linha AGORA desce com o scroll e acende o card da vez */
  function initAgenda() {
    var wrap = $('.lp-slots');
    if (!wrap) return;
    var slots = $$('.lp-slot', wrap), now = $('.lp-now', wrap);
    var count = title($('.lp-agenda-count')), bar = $('.lp-agenda-bar');
    if (!slots.length) return;
    var current = -1, tick = false;
    function set(k) {
      if (k === current) return;
      current = k;
      slots.forEach(function (s, i) { s.classList.toggle('is-done', i < k); s.classList.toggle('is-active', i === k); });
      if (now) wrap.style.setProperty('--lp-now', Math.max(0, slots[k].offsetTop - 22) + 'px');
      if (count) count.textContent = pad(k + 1, 2);
      if (bar) bar.style.setProperty('--lp-p', ((k + 1) / slots.length * 100) + '%');
    }
    function calc() {
      tick = false;
      var ref = window.innerHeight * 0.45, top = wrap.getBoundingClientRect().top, k = 0;
      slots.forEach(function (s, i) { if (top + s.offsetTop <= ref) k = i; });
      set(k);
    }
    if (now) now.style.top = '0';
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(calc); } }, { passive: true });
    window.addEventListener('resize', calc);
    calc();
  }

  /* 07 · Teste de compatibilidade: interruptores ligam em sequência e o medidor acompanha */
  function initSwitches() {
    var list = $('.lp-switches');
    if (!list) return;
    var rows = $$('.lp-switch--yes', list), meter = $('.lp-meter'), ring = $('.lp-meter-ring');
    var num = title($('.lp-meter-num'));
    var total = rows.length;
    function refresh() {
      var n = rows.filter(function (r) { return r.classList.contains('is-on'); }).length;
      if (ring) ring.style.setProperty('--lp-deg', (n / total * 360).toFixed(1));
      if (num) num.textContent = n + '/' + total;
      if (meter) meter.classList.toggle('is-full', n === total);
    }
    refresh();
    onceInView([list], function () {
      rows.forEach(function (r, i) {
        setTimeout(function () { r.classList.add('is-on'); refresh(); }, reduce ? 0 : 300 + i * 140);
      });
    }, 0.3);
    if (window.matchMedia('(hover: hover) and (min-width: 1025px)').matches) {
      rows.forEach(function (r) {
        r.setAttribute('role', 'switch');
        r.setAttribute('tabindex', '0');
        var toggle = function () { r.classList.toggle('is-on'); r.setAttribute('aria-checked', r.classList.contains('is-on')); refresh(); };
        r.addEventListener('click', toggle);
        r.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); } });
      });
    }
  }

  /* 08 · Barra fixa no celular: aparece depois do hero e some na oferta */
  function initMobileBar() {
    var bar = $('.lp-mbar'), hero = $('.lp-hero'), offer = document.getElementById('oferta');
    if (!bar || !hero) return;
    var tick = false;
    function calc() {
      tick = false;
      var afterHero = hero.getBoundingClientRect().bottom < 0;
      var inOffer = false;
      if (offer) { var r = offer.getBoundingClientRect(); inOffer = r.top < window.innerHeight && r.bottom > 0; }
      bar.classList.toggle('is-visible', afterHero && !inOffer);
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(calc); } }, { passive: true });
    calc();
  }

  function init() {
    initMarquee();
    initReveal();
    initScene();
    initAgenda();
    initSwitches();
    initMobileBar();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
