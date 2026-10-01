#!/usr/bin/env python3
"""Hero da Home: mostra o botão "Apoio aos pais" também no celular, sem mudar mais nada.

No celular o botão vira um selo compacto em 2 linhas ("Apoio / aos pais", sem ícone), da
mesma altura do botão do menu, encaixado entre os logos e o menu. Só no celular:
  - botão: aparece; fonte 11px, padding menor, CSS próprio (2 linhas, sem ícone)
  - logos coloridos: largura do conteúdo (os logos continuam do mesmo tamanho)
  - menu: fica por último e não estica (o ícone continua no canto direito)
  - cabeçalho: espaço entre os itens 16 -> 10px
Saída: ../hero-home-apoio-mobile-elementor.json

Uso:  python3 fix_apoio_mobile.py [export-do-hero.json]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/29785923-elementor-2047-2026-10-01.json")
OUT = os.path.join(HERE, "..", "hero-home-apoio-mobile-elementor.json")

BUTTON_CSS = """@media (max-width: 767px) {
  selector { margin-left: auto; }
  selector .elementor-button-icon { display: none; }
  selector .elementor-button-text { display: block; max-width: 4em; text-align: center; }
}"""


def find(elements, pred):
    for e in elements:
        if pred(e):
            return e
        r = find(e.get("elements", []), pred)
        if r:
            return r


def px(size):
    return {"unit": "px", "size": size, "sizes": []}


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    els = data["content"]
    header = find(els, lambda e: "un-header" in (e["settings"].get("css_classes") or "").split())
    logos = find([header], lambda e: "un-logos--color" in (e["settings"].get("css_classes") or "").split())
    nav = find([header], lambda e: e.get("widgetType") == "nav-menu")
    btn = find([header], lambda e: e.get("widgetType") == "button" and "Apoio aos pais" in e["settings"].get("text", ""))

    b = btn["settings"]
    b.pop("hide_mobile", None)
    b.update({
        "typography_font_size_mobile": px(11),
        "typography_line_height_mobile": px(13),
        "text_padding_mobile": {"unit": "px", "top": "7", "right": "13", "bottom": "7", "left": "13", "isLinked": False},
        "custom_css": BUTTON_CSS,
    })
    logos["settings"]["width_mobile"] = {"unit": "custom", "size": "max-content", "sizes": []}
    nav["settings"].update({"_flex_order_mobile": "end", "_flex_size_mobile": "none"})
    header["settings"]["flex_gap_mobile"] = {"column": "10", "row": "10", "isLinked": True, "unit": "px", "size": 10}

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False)
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
