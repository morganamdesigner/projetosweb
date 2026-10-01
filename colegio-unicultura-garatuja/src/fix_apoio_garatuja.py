#!/usr/bin/env python3
"""Hero da Garatuja: acrescenta o botão "Apoio aos pais", sem mudar mais nada.

- Computador e tablet: botão discreto (contorno branco, amarelo no hover) no fim da barra de
  menu, depois das redes sociais. No menu fixo (ao rolar) ele acompanha as redes à direita.
- Celular: ao lado do recorte dos logos só sobram ~110px (cabe apenas o menu), então o botão
  entra logo abaixo do "Quero fazer a matrícula", como botão secundário com a seta amarela.
Saída: ../hero-garatuja-apoio-elementor.json

Uso:  python3 fix_apoio_garatuja.py [export-do-hero.json]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/d564bcf5-elementor-2067-2026-10-01.json")
OUT = os.path.join(HERE, "..", "hero-garatuja-apoio-elementor.json")

# CONFERIR: é o mesmo link da Home (identificador=210); se a Garatuja tiver outro, troque aqui
APOIO_URL = "https://apoioaospais.com.br/login.php?identificador=210"
NAVY = "#010658"
YELLOW = "#F2CA50"


def find(elements, pred):
    for e in elements:
        if pred(e):
            return e
        r = find(e.get("elements", []), pred)
        if r:
            return r


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(t, r, b, l):
    return {"unit": "px", "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": False}


def uid(seed):
    return hashlib.md5(seed.encode()).hexdigest()[:7]


def apoio_button(id_, extra):
    s = {
        "text": "Apoio aos pais",
        "link": {"url": APOIO_URL, "is_external": "", "nofollow": "", "custom_attributes": ""},
        "align": "left",
        "size": "sm",
        "button_text_color": "#FFFFFF",
        "hover_color": NAVY,
        "background_background": "classic",
        "background_color": "rgba(255, 255, 255, 0.06)",
        "button_background_hover_background": "classic",
        "button_background_hover_color": YELLOW,
        "border_border": "solid",
        "border_width": {"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
        "border_color": "rgba(255, 255, 255, 0.3)",
        "button_hover_border_color": YELLOW,
        "border_radius": {"unit": "px", "top": "999", "right": "999", "bottom": "999", "left": "999", "isLinked": True},
        "typography_typography": "custom",
        "typography_font_family": "Hanken Grotesk",
        "typography_font_weight": "700",
    }
    s.update(extra)
    return {"id": id_, "settings": s, "elements": [], "isInner": False, "widgetType": "button", "elType": "widget"}


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    els = data["content"]
    navbar = find(els, lambda e: "gt-navbar" in (e["settings"].get("css_classes") or "").split())
    cta_row = find(els, lambda e: e.get("elType") == "container"
                   and find(e.get("elements", []), lambda w: w.get("widgetType") == "button"
                            and "matr" in w["settings"].get("text", "")) is not None
                   and len(e.get("elements", [])) == 1)
    content_col = find(els, lambda e: cta_row in e.get("elements", []))

    # 1) computador e tablet: no fim da barra de menu
    navbar["elements"].append(apoio_button(uid("garatuja-apoio-nav"), {
        "typography_font_size": px(13),
        "typography_line_height": px(16),
        "text_padding": dims(10, 18, 10, 18),
        "_flex_size": "none",
        "hide_mobile": "hidden-mobile",
    }))

    # 2) celular: logo abaixo do botão de matrícula
    i = content_col["elements"].index(cta_row)
    content_col["elements"].insert(i + 1, apoio_button(uid("garatuja-apoio-mobile"), {
        "typography_font_size": px(15),
        "typography_line_height": px(18),
        "text_padding": dims(8, 8, 8, 20),
        "selected_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
        "icon_align": "right",
        "icon_indent": px(12),
        "_css_classes": "gt-btn-arrow",
        "hide_desktop": "hidden-desktop",
        "hide_tablet": "hidden-tablet",
        "_animation": "fadeInUp",
        "animation_duration": "fast",
        "_animation_delay": 420,
    }))

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
