/* Colégio Unicultura | Home - hero "do primeiro dia à formatura" (CSS em un-story.css).
   Ciclo automático: primeiro dia (parado) -> a linha atravessa a foto revelando a formatura
   -> formatura (parada) -> volta. No computador, com o mouse sobre a foto, a posição do mouse
   controla a linha; ao sair, o ciclo continua.
   No editor do Elementor fica parado no "primeiro dia"; com "reduzir movimento", sem ciclo. */
(function () {
  var script = document.currentScript;
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  var card = script && script.closest('.un-hero');
  var story = card && card.querySelector('.un-story');
  if (!story) {
    return;
  }
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia('(hover: hover) and (min-width: 1025px)').matches;

  var HOLD = 3600;  // ms parado em cada foto
  var MOVE = 1700;  // ms da linha atravessando
  var CYCLE = 2 * (HOLD + MOVE);

  function ease(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function setP(p) {
    // a linha vai de 100% (direita) até -5% (a formatura cobre tudo)
    var x = 100 - p * 105;
    var lineOpacity = Math.max(0, Math.min(1, (x - 30) / 12)) * Math.min(1, (100 - x) / 4);
    story.style.setProperty('--x', x.toFixed(2) + '%');
    story.style.setProperty('--p', p.toFixed(3));
    story.style.setProperty('--lo', lineOpacity.toFixed(3));
    card.style.setProperty('--p', p.toFixed(3));
    card.classList.toggle('is-future', p > 0.5);
  }

  function auto(t) {
    var k = t % CYCLE;
    if (k < HOLD) {
      return 0;
    }
    if (k < HOLD + MOVE) {
      return ease((k - HOLD) / MOVE);
    }
    if (k < 2 * HOLD + MOVE) {
      return 1;
    }
    return 1 - ease((k - 2 * HOLD - MOVE) / MOVE);
  }

  setP(0);
  if (reduceMotion) {
    return;
  }

  var manual = null;   // p controlado pelo mouse (null = automático)
  var shown = 0;       // p mostrado (suavizado)
  var clock = 0;
  var last = null;

  function frame(now) {
    var dt = last === null ? 0 : Math.min(64, now - last);
    last = now;
    if (manual === null) {
      clock += dt;
      shown = auto(clock);
    } else {
      shown += (manual - shown) * 0.18;
    }
    setP(shown);
    window.requestAnimationFrame(frame);
  }
  window.requestAnimationFrame(frame);

  if (canHover) {
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect();
      var xPct = ((e.clientX - r.left) / r.width) * 100;
      if (xPct < 45) {        // sobre o texto: deixa o ciclo seguir
        manual = null;
        return;
      }
      manual = Math.max(0, Math.min(1, (100 - xPct) / 55));
    });
    card.addEventListener('pointerleave', function () {
      if (manual !== null) {
        // continua o ciclo a partir de onde o mouse deixou
        clock = manual > 0.5 ? HOLD + MOVE : 0;
      }
      manual = null;
    });
  }
})();
