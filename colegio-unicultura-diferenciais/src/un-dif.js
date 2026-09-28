/* Colégio Unicultura | Diferenciais - comportamentos da página (CSS em un-dif.css).
   1. Índice lateral fixo: um ponto por capítulo ([data-chapter]), o atual fica vermelho.
   2. Cards .un-tilt inclinam em 3D seguindo o mouse.
   Não roda no editor do Elementor. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function buildNav() {
    var chapters = Array.prototype.slice.call(document.querySelectorAll('[data-chapter]'));
    if (!chapters.length || !('IntersectionObserver' in window)) {
      return;
    }
    var nav = document.createElement('ol');
    nav.className = 'un-chapnav';
    nav.setAttribute('aria-label', 'Diferenciais');
    var links = chapters.map(function (section, i) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + section.id;
      a.innerHTML = '<span>' + String(i + 1).padStart(2, '0') + ' · ' + section.getAttribute('data-chapter') +
        '</span>';
      a.setAttribute('aria-label', section.getAttribute('data-chapter'));
      li.appendChild(a);
      nav.appendChild(li);
      return a;
    });
    document.body.appendChild(nav);

    // capítulo atual = o que cruza a faixa do meio da tela
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var i = chapters.indexOf(entry.target);
          links.forEach(function (a, j) {
            a.classList.toggle('is-active', i === j);
          });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    chapters.forEach(function (section) {
      observer.observe(section);
    });

    // o índice só aparece entre o primeiro e o último capítulo
    var first = chapters[0];
    var last = chapters[chapters.length - 1];
    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      var visible = first.getBoundingClientRect().top < vh * 0.6 && last.getBoundingClientRect().bottom > vh * 0.4;
      nav.classList.toggle('is-visible', visible);
    }
    window.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(update);
      }
    }, { passive: true });
    update();
  }

  function tilt() {
    if (reduceMotion || !window.matchMedia('(hover: hover)').matches) {
      return;
    }
    document.querySelectorAll('.un-tilt').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(800px) rotateX(' + (-y * 8).toFixed(2) + 'deg) rotateY(' +
          (x * 10).toFixed(2) + 'deg) translateY(-4px)';
      });
      card.addEventListener('pointerleave', function () {
        card.style.transform = '';
      });
    });
  }

  // este script fica no topo da página: espera o resto do HTML carregar
  function start() {
    buildNav();
    tilt();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
