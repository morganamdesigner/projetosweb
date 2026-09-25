#!/usr/bin/env python3
"""Gera o JSON da seção "Escola bilíngue" (template de container do Elementor).

Seção nova, fora do Figma original: fica logo abaixo do hero, antes de "Duas etapas".
Saída: ../secao-bilingue-elementor.json

Uso:  python3 build_secao_bilingue.py
"""
import json
import os

import build_elementor_json as base
from build_elementor_json import (
    DMSANS, HANKEN, INTER, NAVY, WHITE, YELLOW,
    add, anim, button, container, dims, gap, heading, icon_list, image, px, text, typo, widget,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "secao-bilingue-elementor.json")
CSS_FILE = os.path.join(HERE, "gt-bilingue.css")

# IDs em outra faixa para não coincidir com os da página
base._counter[0] = 5000

WORD_PAIRS = [
    ("Brincar", "Play"),
    ("Cores", "Colors"),
    ("Amigos", "Friends"),
    ("Histórias", "Stories"),
]

MARQUEE_PAIRS = [
    ("Hello", "Olá"), ("Play", "Brincar"), ("Friends", "Amigos"), ("Colors", "Cores"),
    ("Stories", "Histórias"), ("Music", "Música"), ("Discover", "Descobrir"), ("Imagine", "Imaginar"),
]


# ---------------------------------------------------------------------------
# Coluna de texto
# ---------------------------------------------------------------------------

def text_column():
    tag = heading(
        "Escola bilíngue · Bilingual school", "p", YELLOW,
        typo("typography", DMSANS, 14, 700, lh=14, ls=0.8, transform="uppercase", size_m=12),
        extra={
            "_element_width": "auto",
            "_background_background": "classic",
            "_background_color": NAVY,
            "_border_radius": dims(999),
            "_padding": dims(9, 18, 9, 18),
        },
    )
    title = heading(
        'Aqui, a infância fala <span class="gt-highlight gt-highlight--navy">dois idiomas</span>',
        "h2", NAVY,
        typo("typography", HANKEN, 56, 700, lh=62, ls=-2.4,
             size_t=46, size_m=34, lh_t=52, lh_m=42, ls_m=-1.4),
    )
    body = text(
        "<p>Na Garatuja, o inglês faz parte da rotina desde a Educação Infantil. As crianças vivem "
        "a língua de forma natural — cantando, brincando, ouvindo histórias e descobrindo o mundo em "
        "dois idiomas, no seu próprio ritmo.</p>",
        NAVY,
        typo("typography", HANKEN, 18, 400, lh=27, ls=-0.1, size_m=16, lh_m=24),
    )
    points = icon_list(
        [
            {"text": "Aulas de inglês desde a Educação Infantil",
             "icon": {"value": "fas fa-check-circle", "library": "fa-solid"}},
            {"text": "Aprender brincando: músicas, histórias e brincadeiras em inglês",
             "icon": {"value": "fas fa-check-circle", "library": "fa-solid"}},
            {"text": "Inglês presente da Educação Infantil ao 2º ano do Fundamental",
             "icon": {"value": "fas fa-check-circle", "library": "fa-solid"}},
        ],
        typo("icon_typography", HANKEN, 17, 500, lh=24, size_m=16),
        NAVY, icon_color=NAVY, space=14, icon_size=20, text_indent=12,
    )
    cta = button(
        "Agendar uma visita", NAVY, WHITE,
        typo("typography", DMSANS, 16, 700, lh=22),
        dims(14, 24, 14, 32),
        radius="999",
        icon=16,
        css_classes="gt-btn-arrow",
        shadow={"horizontal": 0, "vertical": 6, "blur": 18, "spread": 0, "color": "rgba(1, 6, 88, 0.25)"},
    )
    return container({
        "content_width": "full",
        "width": px(560),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(20),
    }, [
        add(tag, anim("fadeInUp")),
        add(title, anim("fadeIn", 100)),
        add(body, anim("fadeInUp", 200)),
        add(points, anim("fadeInUp", 300)),
        add(cta, anim("fadeInUp", 400), extra_margin()),
    ])


def extra_margin():
    return {"_margin": dims(8, 0, 0, 0)}


# ---------------------------------------------------------------------------
# Foto com balões de fala
# ---------------------------------------------------------------------------

def bubble(label, color, modifier, x_side, x, y_side, y, x_m, y_m, delay):
    s = {
        "_position": "absolute",
        "_offset_orientation_h": x_side,
        "_offset_orientation_v": y_side,
        "_element_width": "auto",
        "_z_index": 2,
    }
    s["_offset_x" if x_side == "start" else "_offset_x_end"] = px(x)
    s["_offset_x_mobile" if x_side == "start" else "_offset_x_end_mobile"] = px(x_m)
    s["_offset_y" if y_side == "start" else "_offset_y_end"] = px(y)
    s["_offset_y_mobile" if y_side == "start" else "_offset_y_end_mobile"] = px(y_m)
    w = heading(label, "p", color,
                typo("typography", HANKEN, 30, 700, lh=30, ls=-0.8, size_m=20, lh_m=20),
                extra=s)
    return add(w, anim("zoomIn", delay), classes=f"gt-bubble gt-bubble--{modifier}")


def photo_column():
    photo = image(
        "bilingue-aula-de-ingles.jpg", "Crianças da Garatuja em aula de inglês",
        height=520, radius=32,
        extra={"height_tablet": px(460), "height_mobile": px(340)},
    )
    return container({
        "content_width": "full",
        "width": px(616),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "_flex_size": "grow",
        "css_classes": "gt-bi-photo",
    }, [
        add(photo, anim("fadeIn")),
        bubble("Hello!", NAVY, "light", "start", -24, "start", 40, -8, 20, 500),
        bubble("Olá!", YELLOW, "dark", "end", -24, "end", 48, -8, 24, 800),
    ])


# ---------------------------------------------------------------------------
# Cards que viram
# ---------------------------------------------------------------------------

def flip_face(lang_label, word, front):
    bg = WHITE if front else NAVY
    word_color = NAVY if front else YELLOW
    label_color = "rgba(1, 6, 88, 0.55)" if front else "rgba(255, 255, 255, 0.6)"
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "flex_gap": gap(8),
        "padding": dims(20),
        "background_background": "classic",
        "background_color": bg,
        "border_radius": dims(20),
        "css_classes": "gt-flip__face " + ("gt-flip__front" if front else "gt-flip__back"),
    }, [
        heading(lang_label, "p", label_color,
                typo("typography", INTER, 11, 700, lh=12, ls=1.4, transform="uppercase"),
                align="center"),
        heading(word, "p", word_color,
                typo("typography", HANKEN, 34, 700, lh=36, ls=-1, size_m=24, lh_m=28),
                align="center"),
    ])


def flip_card(i, pt, en):
    inner = container({
        "content_width": "full",
        "min_height": px(180),
        "min_height_mobile": px(130),
        "css_classes": "gt-flip__inner",
    }, [flip_face("Português", pt, True), flip_face("English", en, False)])
    return add(container({
        "content_width": "full",
        "flex_direction": "column",
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 10, "blur": 24, "spread": 0,
                                  "color": "rgba(1, 6, 88, 0.12)"},
        "border_radius": dims(20),
        "css_classes": "gt-flip",
    }, [inner]), anim("fadeInUp", i * 120))


def flip_row():
    label = heading(
        'Passe o mouse (ou toque) nos cards e descubra <strong>em inglês</strong>', "h3", NAVY,
        typo("typography", HANKEN, 22, 500, lh=28, ls=-0.4, size_m=18, lh_m=24),
    )
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "width": px(100, "%"),
        "grid_columns_grid": px(4, "fr"),
        "grid_columns_grid_mobile": px(2, "fr"),
        "grid_rows_grid": px(1, "fr"),
        "grid_rows_grid_mobile": px(2, "fr"),
        "grid_gaps": {"column": "20", "row": "20", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "12", "row": "12", "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }, [flip_card(i, pt, en) for i, (pt, en) in enumerate(WORD_PAIRS)])
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(16),
        "margin": dims(80, 0, 0, 0),
        "margin_mobile": dims(56, 0, 0, 0),
    }, [add(label, anim("fadeInUp")), grid])


# ---------------------------------------------------------------------------
# Faixa rolante
# ---------------------------------------------------------------------------

def marquee():
    chunk = "".join(
        f'<span style="color:#F2CA50">{en}</span> · {pt} &nbsp;✦&nbsp; ' for en, pt in MARQUEE_PAIRS
    )
    # 4 repetições: a animação desloca -50% (2 repetições), sem emenda visível em telas largas
    title = chunk * 4
    strip = heading(
        title, "div", WHITE,
        typo("typography", HANKEN, 28, 700, lh=28, ls=-0.5, transform="uppercase", size_m=18, lh_m=18),
        extra={"_attributes": "aria-hidden|true"},
    )
    return container({
        "content_width": "full",
        "flex_direction": "row",
        "padding": dims(22, 0, 22, 0),
        "padding_mobile": dims(14, 0, 14, 0),
        "margin": dims(72, -140, 40, -140),
        "margin_tablet": dims(64, -60, 36, -60),
        "margin_mobile": dims(48, -40, 28, -40),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-marquee",
    }, [strip])


# ---------------------------------------------------------------------------
# Seção
# ---------------------------------------------------------------------------

def build_section():
    with open(CSS_FILE, encoding="utf-8") as fh:
        css = fh.read().strip()

    row = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_align_items_tablet": "stretch",
        "flex_gap": gap(64),
        "flex_gap_tablet": gap(48),
        "flex_gap_mobile": gap(40),
    }, [text_column(), photo_column()])

    card = container({
        "content_width": "full",
        "flex_direction": "column",
        "padding": dims(96, 120, 0, 120),
        "padding_tablet": dims(72, 48, 0, 48),
        "padding_mobile": dims(48, 20, 0, 20),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": YELLOW,
        "border_radius": dims(40),
        "border_radius_mobile": dims(24),
        "css_classes": "gt-bi-card",
    }, [row, flip_row(), marquee()])

    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1480),
        "flex_direction": "column",
        "flex_gap": gap(0),
        "padding": dims(40, 0, 0, 0),
        "padding_mobile": dims(24, 0, 0, 0),
        "css_classes": "gt-root gt-bilingue",
    }, [card, widget("html", {"html": "<style>\n" + css + "\n</style>"})], inner=False)


def main():
    data = {
        "content": [build_section()],
        "page_settings": [],
        "version": "0.4",
        "title": "Garatuja - Seção Escola bilíngue",
        "type": "container",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
