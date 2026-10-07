#!/usr/bin/env python3
"""Cards "O que muda na sua prática" (seção 2 em 1) com imagem grande no lugar do ícone.

Parte do grid exportado do site (mantém IDs, textos e ajustes) e, em cada card:
  - tira a linha de cima (ícone + número);
  - põe uma imagem que ocupa a largura toda do topo do card (altura fixa com recorte "cobrir",
    zoom suave no hover, nativo do Elementor);
  - o número (01, 02, 03) vira uma etiqueta sobre a imagem (posição absoluta nativa);
  - título, linha rosé e texto vão para um bloco com o respiro interno que o card tinha.
O card passa a ter padding 0 e "overflow: hidden", para a imagem acompanhar os cantos arredondados.
As imagens ficam com o placeholder do Elementor (nome no Navegador diz qual foto entra).
Entrada: entrada/grid-2em1-atual-2026-10-07.json
Saída:   ../grid-2em1-imagens-elementor.json

Uso:  python3 build_grid_2em1.py [export-do-grid.json]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entrada", "grid-2em1-atual-2026-10-07.json")
OUT = os.path.join(HERE, "..", "grid-2em1-imagens-elementor.json")

# o que cada imagem deve mostrar (vai no nome do widget no Navegador)
PHOTOS = [
    "📷 Card 01: avaliação clínica de uma ferida",
    "📷 Card 02: curativo / ferida em cicatrização",
    "📷 Card 03: avaliação podológica do pé",
]

_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-grid-2em1-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def photo(title):
    """Imagem sem arquivo (placeholder do Elementor). Altura fixa + recorte, zoom no hover."""
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": "image", "elements": [],
            "settings": {
                "image_size": "full",
                "align": "center",
                "width": px(100, "%"),
                "height": px(240),
                "height_tablet": px(320),
                "height_mobile": px(210),
                "object-fit": "cover",
                "object-position": "center center",
                "image_border_radius": dims(0),
                "hover_animation": "grow",
                "_title": title,
            }}


def number_tag(num_widget):
    """O "01" vira etiqueta sobre a imagem (canto superior direito)."""
    s = num_widget["settings"]
    s.update({
        "title_color": "#FFFFFF",
        "typography_font_size": px(13),
        "typography_line_height": px(16),
        "typography_letter_spacing": px(1.2),
        "_background_background": "classic",
        "_background_color": "rgba(15, 79, 92, 0.88)",
        "_padding": dims(8, 14, 8, 14),
        "_border_radius": dims(999),
        "_border_border": "solid",
        "_border_width": dims(1),
        "_border_color": "rgba(207, 138, 134, 0.6)",
        "_position": "absolute",
        "_offset_orientation_h": "end",
        "_offset_x_end": px(16),
        "_offset_orientation_v": "start",
        "_offset_y": px(16),
        "_z_index": 2,
        "_element_width": "auto",
        "_title": "Número do card (sobre a imagem)",
    })
    s.pop("_flex_size", None)
    s.setdefault("__globals__", {}).update({"_background_color": "", "_border_color": ""})
    return num_widget


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    grid = data["content"][0]
    grid["settings"]["_title"] = "Cards 2 em 1 (com imagens)"
    # mobile: 1 coluna (o export só trazia tablet = 1)
    grid["settings"]["grid_columns_grid_mobile"] = px(1, "fr")

    for i, card in enumerate(grid["elements"]):
        top_row, *rest = card["elements"]
        num = next(e for e in top_row["elements"] if e.get("widgetType") == "heading")
        title = rest[0]
        title["settings"].pop("_margin", None)

        body = {"id": new_id(), "elType": "container", "isInner": True, "elements": rest, "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": gap(14),
            "padding": dims(26, 30, 32, 30),
            "padding_mobile": dims(22, 22, 26, 22),
            "_title": "Texto do card",
        }}
        card["elements"] = [photo(PHOTOS[i]), number_tag(num), body]
        card["settings"].update({
            "padding": dims(0),
            "padding_mobile": dims(0),
            "flex_gap": gap(0),
            "overflow": "hidden",
        })

    out = {"content": [grid], "page_settings": [], "version": "0.4",
           "title": "Cicatrize - Cards 2 em 1 com imagens", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
