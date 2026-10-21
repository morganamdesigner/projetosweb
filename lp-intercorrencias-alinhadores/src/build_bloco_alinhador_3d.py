#!/usr/bin/env python3
"""Bloco "Alinhador 3D montado no scroll" para inserir na seção 04 (Apresentação).

Trilha (lp-track--aligner) > palco preso na tela (lp-stage) > sobrelinha, título e a cena 3D
(widget HTML com canvas Three.js, o motor das cenas e a foto do alinhador de reserva).
Saída: ../bloco-alinhador-3d-elementor.json
Uso:   python3 build_bloco_alinhador_3d.py
"""
import json
import os

import el
from build_lp import AZUL, PROF, boot_js, eyebrow, h2, solid, track_css
from el import cls, col, container, dims, gap, html, px, setv

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = {
    # nome do arquivo: (fundo do palco, cor da sobrelinha, cor do título, sufixo do título do template)
    "bloco-alinhador-3d-elementor.json": ("#F2F6F9", AZUL, PROF, ""),
    "bloco-alinhador-3d-escuro-elementor.json": ("#011324", "#00C2C7", "#FFFFFF", " · fundo escuro"),
}
PHOTO = ("https://cdn.jsdelivr.net/gh/morganamdesigner/projetosweb@6b1cc2883363f3565ce71200e8f0ec280c351940/"
         "lp-intercorrencias-alinhadores/assets/alinhador-foto.webp")


def build(out, bg, over_color, title_color, suffix, seed):
    el._counter[0] = seed  # faixa própria de IDs
    css = track_css() + "\n" + open(os.path.join(HERE, "lp-aligner.css"), encoding="utf-8").read().strip()
    js = boot_js() + "\n" + open(os.path.join(HERE, "lp-aligner.js"), encoding="utf-8").read().strip()
    scene = setv(html(
        "<style>\n" + css + "\n</style>\n"
        '<div class="lp-al">'
        '<canvas role="img" aria-label="Alinhador transparente em 3D: os dentes se encaixam um a um na arcada"></canvas>'
        f'<img class="lp-al-fallback" src="{PHOTO}" alt="Alinhador transparente" loading="lazy" decoding="async">'
        '<div class="lp-al-hud" aria-hidden="true"><span class="lp-al-dot"></span><span class="lp-al-count">Encaixe 00/14</span></div>'
        "</div>\n<script>\n" + js + "\n</script>"),
        _title="Alinhador 3D (cena · não apagar)", _css_classes="lp-al-wrap")
    head = col([
        eyebrow("Cada peça no lugar", over_color, center=True),
        h2('Com critério, cada etapa <span class="lp-hl">encaixa</span>.', title_color, 40, "center", t=34, m=26),
    ], 12, "Título", flex_align_items="center", padding=dims(56, 24, 0, 24), padding_mobile=dims(40, 16, 0, 16),
        _flex_size="none")
    # A cor de fundo do palco é a do 3D: troque em Estilo > Fundo e a cena acompanha (clara ou escura).
    stage = container({"flex_direction": "column", "flex_align_items": "center", **solid(bg),
                       "css_classes": "lp-stage lp-stage--aligner", "_title": "Palco do alinhador (preso na tela)"},
                      [head, scene])
    track = container({"flex_direction": "column", "css_classes": "lp-track lp-track--aligner",
                       "_title": "Alinhador 3D · trilha do scroll"}, [stage], inner=False)
    data = {"content": [track], "page_settings": [], "version": "0.4",
            "title": "LP Alinhadores · Alinhador 3D (montagem no scroll)" + suffix, "type": "container"}
    path = os.path.join(HERE, "..", out)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(path), f"{os.path.getsize(path) / 1024:.0f} KB")


def main():
    for i, (out, v) in enumerate(VARIANTS.items()):
        build(out, *v, seed=70000 + i * 1000)


if __name__ == "__main__":
    main()
