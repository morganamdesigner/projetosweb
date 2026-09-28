#!/usr/bin/env python3
"""Gera o JSON da seção "Galeria" da Home (template de container do Elementor).

Substitui a seção atual da galeria (carrossel de imagens). Usa as 6 fotos que a galeria
atual já usa (IDs da Biblioteca de Mídia do site).
Saída: ../secao-galeria-elementor.json

Uso:  python3 build_secao_galeria.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import (  # noqa: E402
    HANKEN, add, anim, container, dims, gap, heading, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "secao-galeria-elementor.json")
CSS_FILE = os.path.join(HERE, "un-galeria.css")
JS_FILE = os.path.join(HERE, "un-galeria.js")

base._counter[0] = 13000  # faixa própria de IDs

UPLOADS = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/"
PHOTOS = [  # (id na Biblioteca de Mídia, arquivo) - as mesmas da galeria atual da Home
    (333, "foto-3-home.webp"),
    (334, "foto-4-home.webp"),
    (335, "foto-5-home.webp"),
    (336, "foto-6-home.webp"),
    (337, "foto2-home.webp"),
    (338, "has_eae_slider_elementor_element_elementor_element_733a2199_e_flex_e_con_boxed_e_con_e_child.webp"),
]
# As fotos são verticais (480x652, proporção 0,736): molduras verticais na mesma proporção.
# Uma faixa só, em "degraus" (fotos pares mais baixas, via CSS).
PHOTO_W, PHOTO_H = 340, 462          # desktop
PHOTO_W_M, PHOTO_H_M = 220, 299      # celular
GAP = 24

NAVY = "#010658"
INK = "#1C1F4F"
RED = "#F10505"
BG = "#F5F5F5"  # fundo atual da seção da galeria


def photo(index):
    id_, file = PHOTOS[index]
    return widget("image", {
        "image": {"id": id_, "url": UPLOADS + file, "alt": "", "source": "library", "size": ""},
        "image_size": "large",
        "align": "left",
        "link_to": "file",
        "open_lightbox": "yes",
        "width": px(100, "%"),
        "height": px(PHOTO_H),
        "height_mobile": px(PHOTO_H_M),
        "object-fit": "cover",
        "object-position": "center center",
        "image_border_radius": dims(24),
        "_element_width": "initial",
        "_element_custom_width": px(PHOTO_W),
        "_element_custom_width_mobile": px(PHOTO_W_M),
        "_css_classes": "un-gal-photo",
    })


def photo_set(duplicate=False):
    s = {
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_gap": gap(GAP),
        "flex_gap_mobile": gap(14),
        "flex_align_items": "flex-start",
        "padding": dims(0, GAP, 0, 0),  # = gap: a emenda com a cópia fica invisível
        "padding_mobile": dims(0, 14, 0, 0),
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "_flex_size": "none",
        "css_classes": "un-gal-set" + (" un-gal-dup" if duplicate else ""),
    }
    if duplicate:
        s["_attributes"] = "aria-hidden|true"  # cópia só para o movimento contínuo (Pro)
    # as 6 fotos 2x por conjunto (~4.400px): sem vão nem em monitores muito largos
    return container(s, [photo(i % len(PHOTOS)) for i in range(len(PHOTOS) * 2)])


def photo_row():
    track = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_gap": gap(0),
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "css_classes": "un-gal-track",
    }, [photo_set(), photo_set(duplicate=True)])
    return container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "overflow": "hidden",
        "padding": dims(0, 0, 56, 0),       # espaço para os "degraus"
        "padding_mobile": dims(0, 0, 28, 0),
        "css_classes": "un-gal-row",
    }, [track])


def header():
    eyebrow = heading("Nosso dia a dia", "p", RED,
                      typo("typography", HANKEN, 14, 700, lh=14, ls=1.4, transform="uppercase"), align="center")
    title = heading('Momentos que <span style="color:#42468D;font-style:italic;font-weight:400">fazem história</span>',
                    "h2", NAVY,
                    typo("typography", HANKEN, 52, 600, lh=56, ls=-2, size_t=44, size_m=34, lh_t=48, lh_m=38, ls_m=-1.2),
                    align="center")
    intro = text("<p>Descobertas, amizades, projetos e conquistas: um pouco do que se vive todos os dias na "
                 "Unicultura. <strong>Clique nas fotos para ampliar.</strong></p>",
                 INK, typo("typography", HANKEN, 17, 400, lh=26, size_m=16, lh_m=24), align="center",
                 extra={"_element_width": "initial", "_element_custom_width": px(620),
                        "_element_custom_width_tablet": px(100, "%")})
    return container({
        "content_width": "boxed",
        "boxed_width": px(760),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(16),
        "padding": dims(0, 24, 0, 24),
        "padding_mobile": dims(0, 16, 0, 16),
    }, [add(eyebrow, anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(intro, anim("fadeInUp", 200))])


def build_section():
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    js = open(JS_FILE, encoding="utf-8").read().strip()
    rows = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(GAP),
        "flex_gap_mobile": gap(12),
    }, [photo_row(),
        widget("html", {"html": "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"})])
    return container({
        "content_width": "full",
        "html_tag": "section",
        "flex_direction": "column",
        "flex_gap": gap(56),
        "flex_gap_mobile": gap(32),
        "padding": dims(110, 0, 110, 0),
        "padding_tablet": dims(88, 0, 88, 0),
        "padding_mobile": dims(64, 0, 64, 0),
        "background_background": "classic",
        "background_color": BG,
        "css_classes": "gt-root un-gal",
    }, [header(), add(rows, anim("fadeIn", 200))], inner=False)


def main():
    data = {"content": [build_section()], "page_settings": [], "version": "0.4",
            "title": "Unicultura - Seção Galeria", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
