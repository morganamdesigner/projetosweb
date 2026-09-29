#!/usr/bin/env python3
"""Seção "E depois da Garatuja?" (página Garatuja) - versão redesenhada.

Leão flutuando sobre um círculo amarelo com estrelas, título com marca-texto amarelo e uma
"trilha" Garatuja (até o 2º ano) -> Unicultura (do 3º ano ao Ensino Médio): a linha se desenha
do amarelo ao vermelho quando aparece e um ponto viaja por ela. CSS/JS dentro da própria seção.
Mantém o título, o texto, o leão (placeholder) e o divisor azul do export atual.
Saída: ../secao-depois-garatuja-elementor.json

Uso:  python3 build_secao_depois.py [export-da-secao.json]
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_elementor_json as base  # noqa: E402
from build_elementor_json import HANKEN, add, anim, button, container, dims, gap, heading, px, text, typo, widget  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/40a74c10-elementor-1633-2026-09-29.json")
OUT = os.path.join(HERE, "..", "secao-depois-garatuja-elementor.json")
CSS_FILE = os.path.join(HERE, "gt-depois.css")
JS_FILE = os.path.join(HERE, "gt-depois.js")

NAVY = "#010658"
YELLOW = "#F2CA50"
UPLOADS = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/"

base._counter[0] = 33000  # faixa própria de IDs

DECOR = (
    '<div class="gt-next-decor" aria-hidden="true">'
    '<span class="gt-next-blob"></span>'
    '<svg class="gt-star gt-star--1" viewBox="0 0 24 24"><path d="M12 2l2.6 6.6L21 11l-6.4 2.4L12 20l-2.6-6.6L3 11l6.4-2.4z"/></svg>'
    '<svg class="gt-star gt-star--2" viewBox="0 0 24 24"><path d="M12 2l2.6 6.6L21 11l-6.4 2.4L12 20l-2.6-6.6L3 11l6.4-2.4z"/></svg>'
    '<svg class="gt-star gt-star--3" viewBox="0 0 24 24"><path d="M12 2l2.6 6.6L21 11l-6.4 2.4L12 20l-2.6-6.6L3 11l6.4-2.4z"/></svg>'
    '<span class="gt-next-dot gt-next-dot--1"></span><span class="gt-next-dot gt-next-dot--2"></span>'
    '</div>'
)
LINE = '<div class="gt-trail-line" aria-hidden="true"><span class="gt-trail-fill"></span><i class="gt-trail-dot"></i></div>'


def find(elements, pred):
    for e in elements:
        if pred(e):
            return e
        r = find(e.get("elements", []), pred)
        if r:
            return r


def school_chip(logo_id, logo_file, alt, label, css):
    logo = widget("image", {
        "image": {"id": logo_id, "url": UPLOADS + logo_file, "alt": alt, "source": "library", "size": ""},
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(46),
        "height_mobile": px(38),
        "object-fit": "contain",
        "align": "center",
        "_element_width": "initial",
        "_element_custom_width": px(130),
        "_element_custom_width_mobile": px(120),
    })
    return container({
        "content_width": "full",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(10),
        "flex_gap_mobile": gap(6),
        "padding": dims(16, 18, 14, 18),
        "padding_mobile": dims(12, 12, 10, 12),
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.1)",
        "border_radius": dims(20),
        "border_radius_mobile": dims(16),
        "_flex_size": "none",
        "css_classes": "gt-chip " + css,
    }, [logo, heading(label, "p", NAVY, typo("typography", HANKEN, 13, 700, lh=16, ls=0.3, size_m=11, lh_m=14),
                      align="center")])


def main():
    src = json.load(open(SRC, encoding="utf-8"))
    old = src["content"][0]
    lion_old = find([old], lambda e: "gt-lion" in (e["settings"].get("_css_classes") or ""))
    title_txt = find([old], lambda e: e.get("widgetType") == "heading")["settings"]["title"]
    body_html = find([old], lambda e: e.get("widgetType") == "text-editor")["settings"]["editor"]
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    js = open(JS_FILE, encoding="utf-8").read().strip()

    # --- coluna do leão ---
    lion = copy.deepcopy(lion_old)
    lion["id"] = base.new_id()
    ls = lion["settings"]
    ls.update({"_element_custom_width": px(420), "_element_custom_width_tablet": px(320),
               "_element_custom_width_mobile": px(220), "_animation": "zoomIn", "animation_duration": "fast",
               "_css_classes": "gt-lion gt-next-lion", "align": "center"})
    decor = widget("html", {"html": DECOR + "\n<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>",
                            "_css_classes": "gt-next-decor-wrap"})
    media = container({
        "content_width": "full",
        "width": px(42, "%"),
        "width_tablet": px(100, "%"),
        "min_height": px(460),
        "min_height_tablet": px(360),
        "min_height_mobile": px(260),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "css_classes": "gt-next-media",
    }, [decor, lion])

    # --- coluna do texto ---
    eyebrow = heading("Próximo capítulo", "p", NAVY,
                      typo("typography", HANKEN, 12, 800, lh=14, ls=1.6, transform="uppercase"),
                      extra={"_element_width": "auto", "_background_background": "classic",
                             "_background_color": YELLOW, "_border_radius": dims(999),
                             "_padding": dims(8, 14, 8, 14), "_css_classes": "gt-next-eyebrow"})
    title = heading(title_txt.replace("Garatuja?", '<span class="gt-mark">Garatuja?</span>'), "h2", NAVY,
                    typo("typography", HANKEN, 62, 700, lh=66, ls=-3.1, size_t=52, size_m=36, lh_t=58, lh_m=40,
                         ls_m=-1.5),
                    extra={"_css_classes": "gt-next-title"})
    body = text(body_html, NAVY, typo("typography", HANKEN, 26, 300, lh=34, style="italic", size_t=24, size_m=19,
                                      lh_t=32, lh_m=27),
                extra={"_element_width": "initial", "_element_custom_width": px(560),
                       "_element_custom_width_tablet": px(100, "%")})
    trail = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",  # celular: Garatuja em cima, a linha desce, Unicultura embaixo
        "flex_wrap": "nowrap",
        "flex_align_items": "center",
        "flex_gap": gap(14),
        "flex_gap_mobile": gap(10),
        "width": px(100, "%"),
        "margin": dims(8, 0, 0, 0),
        "css_classes": "gt-trail",
    }, [school_chip(27, "logo-garatuha.webp", "Escola Garatuja", "até o 2º ano", "gt-chip--garatuja"),
        widget("html", {"html": LINE, "_css_classes": "gt-trail-line-wrap"}),
        school_chip(79, "logo-unicultura-svg-1.svg", "Colégio Unicultura", "do 3º ano ao Ensino Médio",
                    "gt-chip--unicultura")])
    cta = button("Conheça o Colégio Unicultura", NAVY, "#FFFFFF", typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                 dims(14, 14, 14, 26), radius="999", icon=16, css_classes="gt-next-btn",
                 extra={"link": {"url": "https://colegiounicultura.com.br/", "is_external": "", "nofollow": "",
                                 "custom_attributes": ""}, "button_background_hover_color": "#F10505"})
    text_col = container({
        "content_width": "full",
        "width": px(58, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_align_items_tablet": "center",
        "flex_gap": gap(22),
        "flex_gap_mobile": gap(18),
        "css_classes": "gt-next-text",
    }, [add(eyebrow, anim("fadeInUp")), add(title, anim("fadeInUp", 100)), add(body, anim("fadeInUp", 200)),
        add(trail, anim("fadeInUp", 300)), add(cta, anim("fadeInUp", 400))])

    # --- seção (mantém fundo, divisor azul e espaçamentos do export) ---
    s = copy.deepcopy(old["settings"])
    s.update({
        "boxed_width": px(1200),
        "flex_gap": gap(56),
        "flex_gap_tablet": gap(24),
        "flex_align_items": "center",
        "padding": dims(120, 24, 110, 24),
        "css_classes": "gt-root gt-depois gt-next",
    })
    section = container(s, [media, text_col], inner=False)
    data = {"content": [section], "page_settings": [], "version": "0.4",
            "title": "Garatuja - E depois da Garatuja?", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
