/* Colégio Unicultura | Home - comportamentos da página (CSS em un-home.css).
   Nenhum deles roda dentro do editor do Elementor. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Menu fixo: adiciona .gt-scrolled ao topo da página após 40px de scroll */
  var tops = document.querySelectorAll('.gt-top');

  /* 2. Barra de progresso de leitura (vermelha, no topo da tela) */
  var bar = document.createElement('div');
  bar.className = 'un-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);

  var ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.scrollY;
    tops.forEach(function (el) {
      el.classList.toggle('gt-scrolled', y > 40);
    });
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
  }
  function requestScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(onScroll);
    }
  }
  onScroll();
  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', requestScroll);

  /* 3. Contador: o primeiro número do título com a classe .un-count (ex.: "+1.200 famílias")
        conta de 0 até o valor quando aparece. data-delay (ms) espera outra animação terminar. */
  function countUp(title) {
    var node = title.firstChild;
    if (!node || node.nodeType !== 3) {
      return;
    }
    var match = node.nodeValue.match(/([\d.]+)/);
    if (!match) {
      return;
    }
    var target = parseInt(match[1].replace(/\./g, ''), 10);
    var before = node.nodeValue.slice(0, match.index);
    var after = node.nodeValue.slice(match.index + match[1].length);
    var duration = 1600;
    var start = null;
    function frame(now) {
      if (start === null) {
        start = now;
      }
      var t = Math.min(1, (now - start) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      node.nodeValue = before + Math.round(target * eased).toLocaleString('pt-BR') + after;
      if (t < 1) {
        window.requestAnimationFrame(frame);
      }
    }
    node.nodeValue = before + '0' + after;
    window.requestAnimationFrame(frame);
  }

  if (!reduceMotion && 'IntersectionObserver' in window) {
    document.querySelectorAll('.un-count').forEach(function (widget) {
      var title = widget.querySelector('.elementor-heading-title');
      if (!title) {
        return;
      }
      var delay = parseInt(widget.getAttribute('data-delay') || '0', 10);
      var observer = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) {
          observer.disconnect();
          window.setTimeout(function () {
            countUp(title);
          }, delay);
        }
      }, { threshold: 0.6 });
      observer.observe(widget);
    });
  }
})();
