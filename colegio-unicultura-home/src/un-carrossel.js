/* Colégio Unicultura | Carrossel de fotos (CSS em un-carrossel.css).
   Setas (uma foto por clique), contador "01 / 06", barra de progresso e arrastar com o mouse.
   No celular a trilha já desliza com o dedo (rolagem nativa com encaixe). */
(function () {
  var script = document.currentScript;
  var section = script && script.closest('.un-car');
  if (!section) {
    return;
  }

  // a trilha vem depois deste widget no HTML: começa quando a página terminar de carregar
  function start() {
    var track = section.querySelector('.un-car-track');
    if (!track) {
      return;
    }
    var items = Array.prototype.slice.call(track.querySelectorAll('.un-car-item'));
    var prev = section.querySelector('.un-car-prev');
    var next = section.querySelector('.un-car-next');
    var count = section.querySelector('.un-car-count');
    var progress = section.querySelector('.un-car-progress');
    var total = items.length;
    var smooth = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';

    function pad(n) {
      return (n < 10 ? '0' : '') + n;
    }

    function step() {
      if (items.length < 2) {
        return track.clientWidth;
      }
      return items[1].getBoundingClientRect().left - items[0].getBoundingClientRect().left;
    }

    function current() {
      var s = step() || 1;
      return Math.max(0, Math.min(total - 1, Math.round(track.scrollLeft / s)));
    }

    // fotos inteiras na tela agora (no computador são várias; no celular, uma)
    function visibleRange() {
      var box = track.getBoundingClientRect();
      var seen = [];
      items.forEach(function (item, i) {
        var r = item.getBoundingClientRect();
        if (r.left >= box.left - 2 && r.right <= box.right + 2) {
          seen.push(i);
        }
      });
      if (!seen.length) {
        var c = current();
        return [c, c];
      }
      return [seen[0], seen[seen.length - 1]];
    }

    function update() {
      var max = track.scrollWidth - track.clientWidth;
      var atEnd = track.scrollLeft >= max - 4;
      var range = visibleRange();
      if (count) {
        var label = range[0] === range[1] ? pad(range[0] + 1) : pad(range[0] + 1) + '–' + pad(range[1] + 1);
        count.innerHTML = '<b>' + label + '</b> / ' + pad(total);
      }
      if (prev) {
        prev.disabled = track.scrollLeft <= 4;
      }
      if (next) {
        next.disabled = atEnd;
      }
      if (progress) {
        var p = max > 0 ? track.scrollLeft / max : 1;
        progress.style.setProperty('--un-car-p', Math.max(1 / total, p).toFixed(3));
      }
    }

    function go(direction) {
      track.scrollBy({ left: direction * step(), behavior: smooth });
    }

    if (prev) {
      prev.addEventListener('click', function () { go(-1); });
    }
    if (next) {
      next.addEventListener('click', function () { go(1); });
    }
    track.setAttribute('tabindex', '0');
    track.setAttribute('aria-label', 'Galeria de fotos');
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
    });

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(function () {
          ticking = false;
          update();
        });
      }
    }, { passive: true });
    window.addEventListener('resize', update);

    // arrastar com o mouse (no toque a rolagem nativa já resolve)
    var drag = null;
    track.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) {
        return;
      }
      drag = { x: e.clientX, left: track.scrollLeft, moved: false };
    });
    window.addEventListener('pointermove', function (e) {
      if (!drag) {
        return;
      }
      var dx = e.clientX - drag.x;
      if (!drag.moved && Math.abs(dx) > 6) {
        drag.moved = true;
        track.classList.add('is-dragging');
      }
      if (drag.moved) {
        track.scrollLeft = drag.left - dx;
      }
    });
    window.addEventListener('pointerup', function () {
      if (!drag) {
        return;
      }
      var moved = drag.moved;
      drag = null;
      track.classList.remove('is-dragging');
      if (moved) {
        // solta no encaixe mais próximo e não abre a foto
        var s = step() || 1;
        track.scrollTo({ left: Math.round(track.scrollLeft / s) * s, behavior: smooth });
        var block = function (ev) {
          ev.preventDefault();
          ev.stopPropagation();
        };
        track.addEventListener('click', block, true);
        window.setTimeout(function () {
          track.removeEventListener('click', block, true);
        }, 60);
      }
    });

    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
