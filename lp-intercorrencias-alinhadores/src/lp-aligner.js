/* Alinhador 3D montado pelo scroll (bloco da seção Apresentação).
   14 dentes translúcidos chegam soltos no espaço e se encaixam um a um na arcada (do centro para
   trás); cada encaixe acende em turquesa. Depois a borda do alinhador se desenha em volta da arcada
   e a peça pronta gira até a vista de 3/4, como na foto. O palco fica preso na tela (sticky) e o
   motor (lp-boot.js) entrega o progresso da trilha. Three.js vem do CDN (só o núcleo).
   Sem WebGL ou se o CDN falhar, fica a foto do alinhador flutuando. */
(function () {
  if (window.__lpAligner) return;
  window.__lpAligner = true;

  var THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js';
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };
  var easeInOut = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  function rng(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }

  // Do centro para trás: incisivo central, lateral, canino, pré-molares e molares.
  var TEETH = [
    { w: 0.86, h: 1.05, d: 0.55, flat: true },
    { w: 0.70, h: 0.95, d: 0.52, flat: true },
    { w: 0.78, h: 1.05, d: 0.68, point: true },
    { w: 0.72, h: 0.86, d: 0.82, cusps: 1 },
    { w: 0.70, h: 0.84, d: 0.82, cusps: 1 },
    { w: 1.00, h: 0.78, d: 0.98, cusps: 2 },
    { w: 0.95, h: 0.74, d: 0.95, cusps: 2 }
  ];

  function toothGeometry(THREE, t) {
    var g = new THREE.CapsuleGeometry(0.5, 0.5, 8, 20); // altura 1,5 no eixo y
    var pos = g.attributes.position, v = new THREE.Vector3();
    for (var i = 0; i < pos.count; i++) {
      v.fromBufferAttribute(pos, i);
      var top = clamp((v.y - 0.15) / 0.6, 0, 1);
      if (t.flat && v.y > 0.35) v.y = 0.35 + (v.y - 0.35) * 0.4;                       // borda incisal reta
      if (t.point) v.y += top * top * 0.28 * Math.max(0, 1 - Math.abs(v.x) * 1.8);    // ponta do canino
      if (t.cusps) {                                                                   // cúspides
        var cx = Math.cos(v.x * Math.PI * (t.cusps + 0.5)), cz = Math.cos(v.z * Math.PI * (t.cusps > 1 ? 2.2 : 1.2));
        v.y += top * 0.1 * cx * cz - top * 0.06;
      }
      v.x *= t.w; v.y *= t.h / 1.5; v.z *= t.d;
      pos.setXYZ(i, v.x, v.y, v.z);
    }
    g.computeVertexNormals();
    return g;
  }

  function softShadowTexture(THREE, dark) {
    var c = document.createElement('canvas'); c.width = c.height = 256;
    var x = c.getContext('2d'), gr = x.createRadialGradient(128, 128, 0, 128, 128, 128);
    var rgb = dark ? '0,194,199' : '11,45,74', a = dark ? [0.55, 0.18] : [0.32, 0.12];
    gr.addColorStop(0, 'rgba(' + rgb + ',' + a[0] + ')'); gr.addColorStop(0.55, 'rgba(' + rgb + ',' + a[1] + ')'); gr.addColorStop(1, 'rgba(' + rgb + ',0)');
    x.fillStyle = gr; x.fillRect(0, 0, 256, 256);
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }

  function build(THREE, box) {
    var canvas = box.querySelector('canvas'), label = box.querySelector('.lp-al-count');
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;

    var scene = new THREE.Scene();
    // Fundo: a cor de fundo do palco no Elementor (ou --al-bg, se definida). Fundo escuro liga o
    // modo escuro: brilho turquesa por baixo no lugar da sombra e luz de contorno mais forte.
    var bg = (getComputedStyle(box).getPropertyValue('--al-bg') || '').trim();
    if (!bg) {
      for (var n = box; n && n !== document.body; n = n.parentElement) {
        var c = getComputedStyle(n).backgroundColor;
        if (c && c !== 'transparent' && !/rgba\(.*,\s*0\)$/.test(c)) { bg = c; break; }
      }
    }
    var bgColor = new THREE.Color(bg ? (bg.indexOf('rgb') === 0 ? bg.replace(/rgba?\(([^)]+)\)/, function (m, v) {
      var a = v.split(',').map(function (x) { return parseFloat(x); }); return 'rgb(' + a[0] + ',' + a[1] + ',' + a[2] + ')'; }) : bg) : '#F2F6F9');
    var dark = (0.2126 * bgColor.r + 0.7152 * bgColor.g + 0.0722 * bgColor.b) < 0.35;
    if (dark) box.classList.add('is-dark');
    scene.background = bgColor;

    // Estúdio para os reflexos do material (caixas de luz brancas e uma turquesa).
    var pmrem = new THREE.PMREMGenerator(renderer), env = new THREE.Scene(), cube = new THREE.BoxGeometry(1, 1, 1);
    env.background = new THREE.Color('#d9e3ea');
    [['#ffffff', 3.2, [0, 6, 0], [12, 0.2, 12]], ['#ffffff', 2.2, [-6, 2, 2], [0.2, 4, 7]],
     ['#6fe6ee', 2.4, [6, 1.5, -2], [0.2, 4, 6]], ['#ffffff', 1.6, [0, 1.5, 7], [9, 3, 0.2]]].forEach(function (b) {
      var m = new THREE.Mesh(cube, new THREE.MeshBasicMaterial({ color: new THREE.Color(b[0]).multiplyScalar(b[1]) }));
      m.position.fromArray(b[2]); m.scale.fromArray(b[3]); env.add(m);
    });
    scene.environment = pmrem.fromScene(env, 0.04).texture;
    scene.add(new THREE.HemisphereLight('#ffffff', dark ? '#0b2d4a' : '#cfe4ec', dark ? 0.9 : 0.6));
    var key = new THREE.DirectionalLight('#ffffff', dark ? 1.8 : 1.4); key.position.set(3, 6, 5); scene.add(key);
    if (dark) { var rim = new THREE.DirectionalLight('#5fe6ee', 2.2); rim.position.set(-4, 3, -6); scene.add(rim); }

    var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
    var arch = new THREE.Group(); scene.add(arch);

    // Arcada: curva em U; os dentes são posicionados pelo comprimento da curva.
    var curve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(-2.35, 0, -2.7), new THREE.Vector3(-2.2, 0, -1.3), new THREE.Vector3(-1.75, 0, -0.15),
      new THREE.Vector3(-0.95, 0, 0.65), new THREE.Vector3(0, 0, 0.95), new THREE.Vector3(0.95, 0, 0.65),
      new THREE.Vector3(1.75, 0, -0.15), new THREE.Vector3(2.2, 0, -1.3), new THREE.Vector3(2.35, 0, -2.7)
    ]);
    var L = curve.getLength(), half = TEETH.reduce(function (s, t) { return s + t.w; }, 0);
    var k = (L * 0.94) / (half * 2);                       // escala para a arcada ficar cheia

    var material = new THREE.MeshPhysicalMaterial({
      color: dark ? '#f2fffd' : '#eafcf9', roughness: 0.16, metalness: 0, transmission: 1, thickness: 0.6, ior: 1.42,
      attenuationColor: new THREE.Color('#9fe3dc'), attenuationDistance: 1.4,
      clearcoat: 1, clearcoatRoughness: 0.1, envMapIntensity: dark ? 1.8 : 1.3, specularIntensity: 1
    });
    var rand = rng(7), teeth = [], center = new THREE.Vector3(0, 0, -0.9);
    TEETH.forEach(function (t, idx) {
      var geo = toothGeometry(THREE, t), s = 0;
      for (var j = 0; j < idx; j++) s += TEETH[j].w;
      s = (s + t.w / 2) * k;
      [1, -1].forEach(function (side) {
        var u = 0.5 + side * s / L, p = curve.getPointAt(u), tan = curve.getTangentAt(u);
        var mat = material.clone(); mat.emissive = new THREE.Color('#00C2C7'); mat.emissiveIntensity = 0;
        var mesh = new THREE.Mesh(geo, mat);
        mesh.scale.setScalar(k);
        var endPos = new THREE.Vector3(p.x, (t.h * k) / 2, p.z);
        var endQ = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.atan2(-tan.z, tan.x));
        var a = rand() * Math.PI * 2, r = 4.5 + rand() * 3.5;
        var startPos = new THREE.Vector3(Math.cos(a) * r, -1.5 + rand() * 5, center.z + Math.sin(a) * r * 0.8);
        var startQ = new THREE.Quaternion().setFromEuler(new THREE.Euler(rand() * 6.3, rand() * 6.3, rand() * 6.3));
        var rank = idx * 2 + (side > 0 ? 0 : 1);
        teeth.push({ mesh: mesh, startPos: startPos, endPos: endPos, startQ: startQ, endQ: endQ,
                     t0: 0.1 + rank * 0.034, spin: rand() * 2 - 1 });
        arch.add(mesh);
      });
    });

    // Borda do alinhador: dois frisos (por fora e por dentro) que se desenham em volta da arcada.
    var u0 = 0.5 - (half * k) / L, u1 = 0.5 + (half * k) / L, bands = [];
    [1, -1].forEach(function (dir) {
      var pts = [];
      for (var i = 0; i <= 80; i++) {
        var u = u0 + (u1 - u0) * i / 80, p = curve.getPointAt(u), tan = curve.getTangentAt(u);
        var out = new THREE.Vector3(-tan.z, 0, tan.x).multiplyScalar(dir * 0.38 * k);
        pts.push(new THREE.Vector3(p.x + out.x, 0.1 * k, p.z + out.z));
      }
      var geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 240, 0.07 * k, 10, false);
      var mesh = new THREE.Mesh(geo, material);
      geo.setDrawRange(0, 0);
      bands.push(mesh); arch.add(mesh);
    });

    var shadow = new THREE.Mesh(new THREE.PlaneGeometry(9, 7), new THREE.MeshBasicMaterial({
      map: softShadowTexture(THREE, dark), transparent: true, depthWrite: false, opacity: 0,
      blending: dark ? THREE.AdditiveBlending : THREE.NormalBlending }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.set(0, -0.02, center.z); arch.add(shadow);

    var tmpQ = new THREE.Quaternion(), aspect = 1;
    function resize() {
      var w = box.clientWidth, h = box.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      aspect = w / h; camera.aspect = aspect; camera.updateProjectionMatrix();
    }

    function pose(p, time) {
      var landed = 0;
      teeth.forEach(function (o) {
        var raw = (p - o.t0) / 0.2, t = clamp(raw, 0, 1), e = easeOut(t);
        o.mesh.position.lerpVectors(o.startPos, o.endPos, e);
        o.mesh.position.y += Math.sin(Math.PI * t) * 1.1;
        if (t < 1) o.mesh.position.y += Math.sin(time * 0.9 + o.spin * 3) * 0.08 * (1 - t);
        tmpQ.slerpQuaternions(o.startQ, o.endQ, easeInOut(t));
        o.mesh.quaternion.copy(tmpQ);
        o.mesh.material.opacity = 1;
        var glow = raw >= 1 ? clamp(1 - (p - o.t0 - 0.2) / 0.07, 0, 1) : 0;
        o.mesh.material.emissiveIntensity = glow * 0.55;
        if (raw >= 1) landed++;
      });
      var b = easeInOut(clamp((p - 0.7) / 0.16, 0, 1));
      bands.forEach(function (m) { var n = m.geometry.index.count; m.geometry.setDrawRange(0, Math.floor(n * b / 6) * 6); });
      shadow.material.opacity = 0.15 + 0.4 * easeOut(clamp((p - 0.25) / 0.5, 0, 1));

      // Câmera: de frente, perto e baixa (peças soltas) para a vista de 3/4 de cima (peça pronta).
      var c = easeInOut(clamp(p / 0.9, 0, 1));
      var az = -0.55 * c, el = 0.14 + 0.5 * c, r = 10.5 - 1.2 * c;
      // A arcada (≈ 6,4 de largura com folga) sempre cabe na largura da tela, inclusive no celular.
      var fovH = 2 * Math.atan(Math.tan(camera.fov * Math.PI / 360) * aspect);
      r = Math.max(r, 2.95 / Math.tan(fovH / 2) + 1.8);
      camera.position.set(center.x + Math.sin(az) * Math.cos(el) * r, 0.5 + Math.sin(el) * r, center.z + Math.cos(az) * Math.cos(el) * r);
      camera.lookAt(center.x, 0.45, center.z);
      arch.rotation.y = 0.35 * easeInOut(clamp((p - 0.82) / 0.18, 0, 1)) + Math.sin(time * 0.5) * 0.03;
      arch.position.y = Math.sin(time * 0.8) * 0.05;

      if (label) {
        var txt = b >= 1 ? 'Encaixe perfeito ✓' : 'Encaixe ' + pad(landed) + '/14';
        if (label.textContent !== txt) label.textContent = txt;
      }
    }

    resize();
    if (window.ResizeObserver) new ResizeObserver(resize).observe(box);
    return { pose: pose, render: function () { renderer.render(scene, camera); } };
  }

  function setup(box) {
    var stage = box.closest('.lp-stage') || box;
    var target = 0, current = 0, api = null, visible = true, running = false, t0 = performance.now();
    window.lpScroll.scene(stage, { update: function (p) { target = p; }, done: function () { target = current = 1; } });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; if (visible) loop(); }, { rootMargin: '200px 0px' }).observe(box);
    }
    function loop() {
      if (running || !api) return;
      running = true;
      (function tick(now) {
        if (!visible) { running = false; return; }
        current += (target - current) * 0.2;                  // suaviza sem atrasar a rolagem
        if (Math.abs(target - current) < 0.0005) current = target;
        api.pose(current, (now - t0) / 1000);
        api.render();
        requestAnimationFrame(tick);
      })(performance.now());
    }
    var gl = document.createElement('canvas');
    if (!(gl.getContext('webgl2') || gl.getContext('webgl'))) { box.classList.add('is-fallback'); return; }
    import(THREE_URL).then(function (THREE) {
      api = build(THREE, box);
      api.pose(current, 0); api.render();
      box.classList.add('is-3d');
      loop();
    }).catch(function () { box.classList.add('is-fallback'); });
  }

  function init() { Array.prototype.forEach.call(document.querySelectorAll('.lp-al'), setup); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
