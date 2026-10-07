/* Cicatrize 3X | Página de vendas da Pós-graduação. Vai DENTRO do widget HTML do topo da página.
   - barra de progresso de leitura
   - .cz-io       ganha .is-in ao entrar na tela (barras, riscos, assinatura, diagrama...)
   - .cz-split    título sobe palavra por palavra
   - .cz-scrub    frase acende palavra por palavra conforme a rolagem
   - .cz-par-N    parallax leve (só computador); N = intensidade
   - .cz-tilt     cartão inclina em 3D e o brilho segue o mouse
   - .cz-vagas    barra "vagas preenchidas" (data-percent)
   - .cz-countdown contagem regressiva (data-end)
   - .cz-sticky   CTA fixo no celular, aparece depois do hero */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var editor = document.body && document.body.classList.contains("elementor-editor-active");

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function once(el, key) {
    if (el.dataset[key]) return false;
    el.dataset[key] = "1";
    return true;
  }

  /* Envolve cada palavra dos nós de texto (mantendo <span>, <em>, <br> etc.) */
  function wrapWords(root, make) {
    var index = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var parts = child.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          parts.forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) frag.appendChild(document.createTextNode(part));
            else frag.appendChild(make(part, index++));
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1 && child.tagName !== "BR") {
          walk(child);
        }
      });
    })(root);
    return index;
  }

  ready(function () {
    /* ---------- barra de progresso ---------- */
    var bar = document.querySelector(".cz-progress");
    if (!bar && !editor) {
      bar = document.createElement("div");
      bar.className = "cz-progress";
      bar.setAttribute("aria-hidden", "true");
      document.body.appendChild(bar);
    }

    /* ---------- títulos palavra por palavra ---------- */
    document.querySelectorAll(".cz-split .elementor-heading-title").forEach(function (t) {
      if (!once(t, "czSplit")) return;
      wrapWords(t, function (word, i) {
        var outer = document.createElement("span");
        var inner = document.createElement("span");
        outer.className = "cz-w";
        inner.textContent = word;
        inner.style.setProperty("--i", i);
        outer.appendChild(inner);
        return outer;
      });
    });

    /* ---------- frase que acende com o scroll ---------- */
    var scrubs = [];
    document.querySelectorAll(".cz-scrub .elementor-heading-title").forEach(function (t) {
      if (!once(t, "czScrub")) return;
      var words = [];
      wrapWords(t, function (word) {
        var s = document.createElement("span");
        s.className = "cz-sw";
        s.textContent = word;
        words.push(s);
        return s;
      });
      scrubs.push({ el: t, words: words });
    });

    /* ---------- entra na tela ---------- */
    var ioTargets = document.querySelectorAll(".cz-io, .cz-rv, .cz-split, .cz-mark, .cz-swap, .cz-sign, .cz-strike");
    if ("IntersectionObserver" in window && !reduce) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add("is-in");
          io.unobserve(e.target);
          if (e.target.classList.contains("cz-vagas")) runVagas(e.target);
        });
      }, { threshold: 0.25, rootMargin: "0px 0px -4% 0px" });
      ioTargets.forEach(function (el) { io.observe(el); });
    } else {
      ioTargets.forEach(function (el) {
        el.classList.add("is-in");
        if (el.classList.contains("cz-vagas")) runVagas(el);
      });
    }

    /* ---------- vagas preenchidas ---------- */
    function runVagas(el) {
      var p = Math.max(0, Math.min(100, parseFloat(el.getAttribute("data-percent")) || 0));
      el.style.setProperty("--p", p + "%");
      var n = el.querySelector(".cz-vagas-n");
      if (!n) return;
      if (reduce) { n.textContent = p + "%"; return; }
      var start = null;
      function step(ts) {
        if (!start) start = ts;
        var k = Math.min(1, (ts - start) / 2000);
        var eased = 1 - Math.pow(1 - k, 3);
        n.textContent = Math.round(p * eased) + "%";
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    /* ---------- parallax, scrub, progresso e CTA fixo (um único loop de scroll) ---------- */
    var pars = [];
    document.querySelectorAll("[class*='cz-par-']").forEach(function (el) {
      var m = el.className.match(/cz-par-(\d+)/);
      if (m) pars.push({ el: el, speed: parseInt(m[1], 10) });
    });

    var sticky = document.querySelector(".cz-sticky");
    var hero = document.querySelector(".cz-hero");
    var stopZones = document.querySelectorAll(".cz-oferta, .cz-final");
    var ticking = false;

    function frame() {
      ticking = false;
      var vh = window.innerHeight;
      var doc = document.documentElement;
      var max = doc.scrollHeight - vh;

      if (bar) bar.style.transform = "scaleX(" + (max > 0 ? window.scrollY / max : 0) + ")";

      if (!reduce && window.innerWidth > 1024) {
        pars.forEach(function (p) {
          var r = p.el.getBoundingClientRect();
          var center = r.top + r.height / 2 - vh / 2;
          p.el.style.translate = "0 " + (center * -0.04 * p.speed).toFixed(1) + "px";
        });
      }

      scrubs.forEach(function (s) {
        var r = s.el.getBoundingClientRect();
        var k = (vh * 0.88 - r.top) / (vh * 0.88 - vh * 0.3);
        k = reduce ? 1 : Math.max(0, Math.min(1, k));
        var on = Math.round(k * s.words.length);
        s.words.forEach(function (w, i) { w.classList.toggle("on", i < on); });
      });

      if (sticky) {
        var past = hero ? hero.getBoundingClientRect().bottom < 0 : window.scrollY > vh;
        var blocked = false;
        stopZones.forEach(function (z) {
          var r = z.getBoundingClientRect();
          if (r.top < vh && r.bottom > 0) blocked = true;
        });
        sticky.classList.toggle("show", past && !blocked);
      }
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(frame);
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    frame();

    /* ---------- cartões 3D ---------- */
    if (!reduce && window.matchMedia("(hover: hover)").matches) {
      document.querySelectorAll(".cz-tilt").forEach(function (card) {
        if (!once(card, "czTilt")) return;
        card.addEventListener("pointermove", function (e) {
          var r = card.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width;
          var y = (e.clientY - r.top) / r.height;
          card.classList.add("is-tilting");
          card.style.setProperty("--ry", ((x - 0.5) * 8).toFixed(2) + "deg");
          card.style.setProperty("--rx", ((0.5 - y) * 8).toFixed(2) + "deg");
          card.style.setProperty("--mx", (x * 100).toFixed(1) + "%");
          card.style.setProperty("--my", (y * 100).toFixed(1) + "%");
        });
        card.addEventListener("pointerleave", function () {
          card.classList.remove("is-tilting");
          card.style.setProperty("--rx", "0deg");
          card.style.setProperty("--ry", "0deg");
        });
      });
    }

    /* ---------- contagem regressiva ---------- */
    document.querySelectorAll(".cz-countdown").forEach(function (cd) {
      if (!once(cd, "czCd")) return;
      var end = new Date(cd.getAttribute("data-end")).getTime();
      if (isNaN(end)) return;
      var units = {
        d: cd.querySelector("[data-u='d']"),
        h: cd.querySelector("[data-u='h']"),
        m: cd.querySelector("[data-u='m']"),
        s: cd.querySelector("[data-u='s']")
      };
      function pad(n) { return (n < 10 ? "0" : "") + n; }
      function tick() {
        var left = Math.max(0, end - Date.now());
        if (left <= 0) {
          cd.classList.add("is-over");
          var label = cd.querySelector(".cz-cd-label");
          if (label) label.textContent = cd.getAttribute("data-over") || "Bônus encerrados";
          return;
        }
        var s = Math.floor(left / 1000);
        if (units.d) units.d.textContent = pad(Math.floor(s / 86400));
        if (units.h) units.h.textContent = pad(Math.floor(s / 3600) % 24);
        if (units.m) units.m.textContent = pad(Math.floor(s / 60) % 60);
        if (units.s) units.s.textContent = pad(s % 60);
        setTimeout(tick, 1000);
      }
      tick();
    });
  });
})();
