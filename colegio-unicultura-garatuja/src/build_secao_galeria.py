#!/usr/bin/env python3
"""Gera o JSON da seção "Galeria de polaroids" (template de container do Elementor).

Seção nova, fora do Figma original. Sugestão de posição: entre "Experiências que
enriquecem a aprendizagem" e "E depois da Garatuja?" (mesmo fundo azul das Experiências,
então a curva azul do topo de "E depois" continua encaixando).
Saída: ../secao-galeria-polaroids-elementor.json

Uso:  python3 build_secao_galeria.py
"""
import json
import os

import build_elementor_json as base
from build_elementor_json import (
    DMSANS, HANKEN, NAVY, WHITE, YELLOW,
    add, anim, container, dims, gap, heading, px, text, typo, widget,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "secao-galeria-polaroids-elementor.json")
CSS_FILE = os.path.join(HERE, "gt-galeria.css")

# IDs em outra faixa para não coincidir com os da página nem da seção bilíngue
base._counter[0] = 7000

# Placeholder real (baixável na importação): vira 1 imagem na Biblioteca de Mídia,
# repetida nos 10 slides. Troque pelas fotos em Content → Add Images.
PLACEHOLDER_PHOTO = "https://placehold.co/960x1200/F2CA50/010658.png"
PHOTOS = 10


def header():
    return container({
        "content_width": "full",
        "width": px(720),
        "width_mobile": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(18),
    }, [
        add(heading("Nosso dia a dia", "p", YELLOW,
                    typo("typography", DMSANS, 14, 700, lh=14, ls=1.4, transform="uppercase"),
                    align="center"), anim("fadeInUp")),
        add(heading('Momentos que viram <span style="color:#F2CA50">memória</span>', "h2", WHITE,
                    typo("typography", HANKEN, 52, 700, lh=56, ls=-2.2,
                         size_t=44, size_m=34, lh_t=48, lh_m=38, ls_m=-1.4),
                    align="center"), anim("fadeInUp", 100)),
        add(text("<p>Um pouco do que as crianças vivem na Garatuja: descobertas, amizades, "
                 "brincadeiras e muito aprendizado — todos os dias.</p>",
                 "rgba(255, 255, 255, 0.75)",
                 typo("typography", HANKEN, 18, 400, lh=27, size_m=16, lh_m=24),
                 align="center"), anim("fadeInUp", 200)),
    ])


def carousel():
    return widget("image-carousel", {
        "carousel_name": "Galeria Garatuja",
        "carousel": [{"id": "", "url": PLACEHOLDER_PHOTO} for _ in range(PHOTOS)],
        "thumbnail_size": "large",
        "slides_to_show": "4",
        "slides_to_show_tablet": "3",
        "slides_to_show_mobile": "1",
        "slides_to_scroll": "1",
        "image_stretch": "yes",
        "navigation": "both",
        "link_to": "file",
        "open_lightbox": "yes",
        "caption_type": "caption",
        "lazyload": "yes",
        "autoplay": "yes",
        "pause_on_hover": "yes",
        "pause_on_interaction": "yes",
        "autoplay_speed": 3500,
        "infinite": "yes",
        "effect": "slide",
        "speed": 700,
        "arrows_position": "outside",
        "arrows_size": px(18),
        "arrows_color": NAVY,
        "dots_position": "outside",
        "dots_size": px(9),
        "dots_gap": px(8),
        "dots_inactive_color": "rgba(255, 255, 255, 0.35)",
        "dots_color": YELLOW,
        "gallery_vertical_align": "center",
        "image_spacing": "custom",
        "image_spacing_custom": px(28),
        "image_spacing_custom_mobile": px(16),
        "caption_align": "center",
        "caption_text_color": NAVY,
        "caption_space": px(12),
        **typo("caption_typography", "Caveat", 24, 600, lh=28),
        "_css_classes": "gt-polaroids",
    })


def build_section():
    with open(CSS_FILE, encoding="utf-8") as fh:
        css = fh.read().strip()
    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1400),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(28),
        "flex_gap_mobile": gap(16),
        "padding": dims(96, 24, 110, 24),
        "padding_tablet": dims(80, 24, 96, 24),
        "padding_mobile": dims(64, 16, 80, 16),
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-root gt-galeria-polaroid",
    }, [
        header(),
        add(container({
            "content_width": "full",
            "width": px(100, "%"),
            "flex_direction": "column",
        }, [carousel(), widget("html", {"html": "<style>\n" + css + "\n</style>"})]),
            anim("fadeIn", 250)),
    ], inner=False)


def main():
    data = {
        "content": [build_section()],
        "page_settings": [],
        "version": "0.4",
        "title": "Garatuja - Seção Galeria de polaroids",
        "type": "container",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
