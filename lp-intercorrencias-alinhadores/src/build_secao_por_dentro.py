#!/usr/bin/env python3
"""Seção 05 · Veja o guia por dentro, com o coverflow 3D automático (a partir do export do site).

Troca o carrossel aninhado (5 páginas mostradas de uma vez não têm para onde avançar) por um container
"lp-flow" com um container por página (imagem com ampliação + legenda, widgets nativos). Mantém as
imagens, as legendas e as configurações da seção do export. CSS/JS num widget HTML da própria seção.
Saída: ../secao-05-por-dentro-elementor.json
Uso:   python3 build_secao_por_dentro.py [export-da-secao.json]
"""
import copy
import json
import os
import sys

import el
from el import cls, container, html, px, setv

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "secao-05-por-dentro-elementor.json")
DEFAULT_EXPORT = "/root/.claude/uploads/302eadef-2a03-5162-b1d4-20b33bc74d43/0c9c65a4-elementor-449-2026-10-23.json"


def main(path):
    el._counter[0] = 90000  # faixa própria de IDs
    data = json.load(open(path))
    sec = data["content"][0]
    css = open(os.path.join(HERE, "lp-flow.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "lp-flow.js"), encoding="utf-8").read().strip()
    widget = setv(html("<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"),
                  _title="Carrossel · estilos e animação (não apagar)", _position="absolute",
                  _element_width="initial", _element_custom_width=px(0))

    out = []
    for ch in sec["elements"]:
        carousel = None
        if ch["elType"] == "container":
            carousel = next((w for w in ch["elements"] if w.get("widgetType") == "nested-carousel"), None)
        if not carousel:
            out.append(ch)
            continue
        items = []
        for slide in carousel["elements"]:
            slide = copy.deepcopy(slide)
            for w in slide["elements"]:
                s = w["settings"]
                if w.get("widgetType") == "image":
                    s["link_to"] = "file"
                    s["open_lightbox"] = "yes"
                    s.pop("image_box_shadow_box_shadow_type", None)   # a sombra vem do CSS (mais forte no centro)
                    s.pop("image_box_shadow_box_shadow", None)
                    if not s["image"].get("alt"):
                        cap = next((x["settings"].get("title") for x in slide["elements"] if x.get("widgetType") == "heading"), "")
                        s["image"]["alt"] = "Página do guia: " + cap if cap else "Página do guia"
            slide["settings"]["css_classes"] = (slide["settings"].get("css_classes", "") + " lp-flow-item").strip()
            slide["settings"]["flex_wrap_mobile"] = "nowrap"
            slide["isInner"] = True
            items.append(slide)
        flow = container({"flex_direction": "column", "css_classes": "lp-flow", "flex_wrap_mobile": "nowrap",
                          "_title": "Páginas do guia (coverflow automático)"}, items)
        out.append(container({"flex_direction": "column", "flex_align_items": "center", "content_width": "boxed",
                              "boxed_width": px(1200), "_title": "Carrossel"}, [widget, flow]))
    sec["elements"] = out
    sec["settings"].pop("custom_css", None)  # era das bolinhas do carrossel antigo
    data["title"] = "LP Alinhadores · 05 Por dentro (coverflow automático)"
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB", "páginas:", len(items))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXPORT)
