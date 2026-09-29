#!/usr/bin/env python3
"""Gera o JSON da seção "Galeria" em carrossel (páginas Unicultura: Home, Fundamental I e II,
Ensino Médio, Sobre). Substitui a faixa em movimento (un-galeria), que não funcionava bem no
celular e não tinha setas.

Trilha com rolagem nativa + encaixe (desliza com o dedo), setas, contador, barra de progresso,
arrastar com o mouse e lightbox. CSS/JS vão num widget HTML dentro da própria seção.
Saída: ../secao-galeria-carrossel-elementor.json

Uso:  python3 build_secao_carrossel.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import HANKEN, add, anim, container, dims, gap, heading, px, text, typo, widget  # noqa: E402

OUT = os.path.join(HERE, "..", "secao-galeria-carrossel-elementor.json")

NAVY = "#010658"
INK = "#1C1F4F"
RED = "#F10505"
BG = "#F5F5F5"
UPLOADS = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/"
PHOTOS = [  # as mesmas 6 fotos das galerias atuais (IDs da Biblioteca de Mídia)
    (333, "foto-3-home.webp"),
    (334, "foto-4-home.webp"),
    (335, "foto-5-home.webp"),
    (336, "foto-6-home.webp"),
    (337, "foto2-home.webp"),
    (338, "has_eae_slider_elementor_element_elementor_element_733a2199_e_flex_e_con_boxed_e_con_e_child.webp"),
]

ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>')
NAV_HTML = (
    '<div class="un-car-nav">'
    '<button type="button" class="un-car-btn un-car-prev" aria-label="Foto anterior">'
    + ARROW.format(d="M15 5l-7 7 7 7") + '</button>'
    '<span class="un-car-count" aria-live="polite"><b>01</b> / 06</span>'
    '<button type="button" class="un-car-btn un-car-next" aria-label="Próxima foto">'
    + ARROW.format(d="M9 5l7 7-7 7") + '</button>'
    '</div>'
)


def photo(id_, file, n):
    return widget("image", {
        "image": {"id": id_, "url": UPLOADS + file, "alt": f"Dia a dia no Colégio Unicultura - foto {n}",
                  "source": "library", "size": ""},
        "image_size": "large",
        "link_to": "file",
        "open_lightbox": "yes",
        "width": px(100, "%"),
        "image_border_radius": dims(24),
        "_css_classes": "un-car-item",
    })


def build_carrossel(with_header=True):
    base._counter[0] = 31000  # faixa própria de IDs
    css = open(os.path.join(HERE, "un-carrossel.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "un-carrossel.js"), encoding="utf-8").read().strip()
    nav = widget("html", {"html": NAV_HTML + "\n<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>",
                          "_css_classes": "un-car-nav-wrap", "_flex_size": "none"})

    head_kids = []
    if with_header:
        head_kids.append(container({
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": gap(12),
            "_flex_size": "grow",
            "width": px(100, "%"),
        }, [
            add(heading("Nosso dia a dia", "p", RED,
                        typo("typography", HANKEN, 13, 700, lh=16, ls=1.4, transform="uppercase")), anim("fadeInUp")),
            add(heading('Momentos que <span class="un-mark-red">fazem história</span>', "h2", NAVY,
                        typo("typography", HANKEN, 48, 700, lh=52, ls=-1.8, size_t=40, size_m=30, lh_t=44, lh_m=34,
                             ls_m=-1)), anim("fadeInUp", 100)),
            add(text("<p>Descobertas, amizades, projetos e conquistas. Toque nas fotos para ampliar.</p>", INK,
                     typo("typography", HANKEN, 17, 400, lh=26, size_m=15, lh_m=23)), anim("fadeInUp", 200)),
        ]))
    # o texto encolhe (sem "grow" + 100%, que empurraria as setas para fora)
    if head_kids:
        head_kids[0]["settings"].pop("_flex_size")
    head = container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "flex_direction": "row",
        "flex_direction_mobile": "column",  # celular: título em cima, setas embaixo
        "flex_align_items": "flex-end",
        "flex_align_items_mobile": "flex-start",
        "flex_justify_content": "space-between",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(18),
        "padding": dims(0, 24, 0, 24),
        "padding_mobile": dims(0, 16, 0, 16),
    }, head_kids + [nav])

    track = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap": "nowrap",
        "flex_wrap_mobile": "nowrap",
        "flex_gap": gap(20),
        "css_classes": "un-car-track",
    }, [photo(id_, file, i + 1) for i, (id_, file) in enumerate(PHOTOS)])
    progress = widget("html", {"html": '<div class="un-car-progress" aria-hidden="true"><i></i></div>'})

    return container({
        "content_width": "full",
        "html_tag": "section",
        "flex_direction": "column",
        "flex_gap": gap(36),
        "flex_gap_mobile": gap(24),
        "padding": dims(110, 0, 100, 0),
        "padding_tablet": dims(88, 0, 80, 0),
        "padding_mobile": dims(64, 0, 56, 0),
        "background_background": "classic",
        "background_color": BG,
        "css_classes": "gt-root un-car",
    }, [head, add(track, anim("fadeIn", 150)), progress], inner=False)


def main():
    data = {"content": [build_carrossel()], "page_settings": [], "version": "0.4",
            "title": "Unicultura - Seção Galeria (carrossel)", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
