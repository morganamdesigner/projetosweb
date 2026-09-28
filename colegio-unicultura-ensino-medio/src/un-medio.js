/* Colégio Unicultura | Ensino Médio - manifesto "caminho próprio" (CSS em un-medio.css).
   1. Separa a frase .un-scrub em palavras e acende cada uma conforme o scroll.
   2. Desenha o caminho (--un-draw de 0 a 1) e leva o ponto vermelho pela linha.
   Não roda no editor do Elementor nem com "reduzir movimento" (tudo aparece completo). */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }
  var sections = [];
  var ticking = false;

  function splitWords(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) {
      if (walker.currentNode.nodeValue.trim()) {
        nodes.push(walker.currentNode);
      }
    }
    nodes.forEach(function (node) {
      var frag = document.createDocumentFragment();
      node.nodeValue.split(/(\s+)/).forEach(function (part) {
        if (!part) {
          return;
        }
        if (/^\s+$/.test(part)) {
          frag.appendChild(document.createTextNode(part));
        } else {
          var span = document.createElement('span');
          span.className = 'un-w';
          span.textContent = part;
          frag.appendChild(span);
        }
      });
      node.parentNode.replaceChild(frag, node);
    });
    return Array.prototype.slice.call(root.querySelectorAll('.un-w'));
  }

  function progress(el, start, end) {
    // 0 quando o topo do elemento está em start*altura da tela, 1 quando está em end*altura
    var vh = window.innerHeight;
    var top = el.getBoundingClientRect().top;
    return Math.max(0, Math.min(1, (vh * start - top) / (vh * (start - end))));
  }

  function update() {
    ticking = false;
    sections.forEach(function (s) {
      if (s.words.length) {
        var lit = Math.round(progress(s.scrub, 0.85, 0.35) * s.words.length);
        s.words.forEach(function (w, i) {
          w.classList.toggle('is-on', i < lit);
        });
      }
      var draw = progress(s.el, 1, 0.1);
      s.el.style.setProperty('--un-draw', draw.toFixed(3));
      if (s.line && s.dot && s.length) {
        var point = s.line.getPointAtLength(s.length * Math.max(0.001, draw));
        s.dot.setAttribute('cx', point.x.toFixed(1));
        s.dot.setAttribute('cy', point.y.toFixed(1));
      }
    });
  }

  function requestUpdate() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  // este script fica no topo da página: espera o resto do HTML carregar
  function start() {
    document.querySelectorAll('.un-manifesto').forEach(function (el) {
      var scrub = el.querySelector('.un-scrub');
      var line = el.querySelector('.un-path-line');
      sections.push({
        el: el,
        scrub: scrub,
        words: scrub ? splitWords(scrub) : [],
        line: line,
        dot: el.querySelector('.un-path-dot'),
        length: line && line.getTotalLength ? line.getTotalLength() : 0
      });
    });
    if (!sections.length) {
      return;
    }
    update();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
