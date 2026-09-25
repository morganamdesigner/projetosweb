/* Unicultura | Seção Depoimentos - contador dos números (classe .un-depo-count).
   Independente do script da Home. Não roda dentro do editor do Elementor. */
(function () {
  if (document.body.classList.contains('elementor-editor-active')) {
    return;
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    return;
  }
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
    var start = null;
    function frame(now) {
      if (start === null) {
        start = now;
      }
      var t = Math.min(1, (now - start) / 1600);
      node.nodeValue = before + Math.round(target * (1 - Math.pow(1 - t, 3))).toLocaleString('pt-BR') + after;
      if (t < 1) {
        window.requestAnimationFrame(frame);
      }
    }
    node.nodeValue = before + '0' + after;
    window.requestAnimationFrame(frame);
  }
  document.querySelectorAll('.un-depo .un-depo-count').forEach(function (widget) {
    var title = widget.querySelector('.elementor-heading-title');
    if (!title) {
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        observer.disconnect();
        window.setTimeout(function () { countUp(title); }, 300);
      }
    }, { threshold: 0.6 });
    observer.observe(widget);
  });
})();
