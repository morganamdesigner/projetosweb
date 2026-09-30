#!/usr/bin/env python3
"""Página 404 (Não encontrada) do Colégio Unicultura - template do Theme Builder (Elementor Pro).

Fundo azul, "4 [bússola] 4": a agulha procura o caminho e aponta para "Voltar para a Home"
(e para o link em que o mouse estiver). Título com marca-texto vermelho suave, texto explicando
que o site foi renovado, botões e atalhos para as principais páginas. CSS/JS no widget HTML.
Saída: ../pagina-404-elementor.json

Uso:  python3 build_404.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import HANKEN, add, anim, button, container, dims, gap, heading, px, text, typo, widget  # noqa: E402

OUT = os.path.join(HERE, "..", "pagina-404-elementor.json")

NAVY = "#010658"
RED = "#F10505"
SITE = "https://colegiounicultura.com.br/"
UPLOADS = SITE + "wp-content/uploads/2026/09/"

# CONFERIR: endereços (slugs) das páginas no site novo
LINKS = [
    ("Fundamental I", SITE + "fundamental-1/"),
    ("Fundamental II", SITE + "fundamental-2/"),
    ("Ensino Médio", SITE + "ensino-medio/"),
    ("Diferenciais", SITE + "diferenciais/"),
    ("Garatuja", SITE + "garatuja/"),
]
CONTATO = SITE + "contato/"

STAR = '<svg viewBox="0 0 20 60"><path d="M10 0L20 30H0z" fill="#F10505"/><path d="M0 30h20L10 60z" fill="#FFFFFF"/></svg>'
ART = (
    '<div class="un-404-art" role="img" aria-label="Erro 404">'
    '<span class="un-404-glow"></span>'
    '<span class="un-404-dot un-404-dot--1"></span><span class="un-404-dot un-404-dot--2"></span>'
    '<span class="un-404-dot un-404-dot--3"></span><span class="un-404-dot un-404-dot--4"></span>'
    '<span class="un-404-digit">4</span>'
    '<span class="un-404-compass"><span class="un-404-ring"></span>'
    '<span class="un-404-ticks"><i></i><i></i><i></i><i></i></span>'
    '<span class="un-404-needle">' + STAR + '</span><span class="un-404-pin"></span></span>'
    '<span class="un-404-digit">4</span>'
    '</div>'
)


def lnk(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def pill(label, url):
    return button(label, "rgba(255, 255, 255, 0.06)", "#FFFFFF",
                  typo("typography", HANKEN, 15, 600, lh=18, size_m=14),
                  dims(12, 20, 12, 20), css_classes="un-404-pill",
                  extra={"link": lnk(url), "border_border": "solid", "border_width": dims(1),
                         "border_color": "rgba(255, 255, 255, 0.22)",
                         "button_background_hover_color": RED, "button_hover_border_color": RED})


def build():
    base._counter[0] = 34000  # faixa própria de IDs
    css = open(os.path.join(HERE, "un-404.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "un-404.js"), encoding="utf-8").read().strip()

    logo = widget("image", {
        "image": {"id": 814, "url": UPLOADS + "logo-branca-uni-1.svg", "alt": "Colégio Unicultura",
                  "source": "library", "size": ""},
        "image_size": "full",
        "link_to": "custom",
        "link": lnk(SITE),
        "width": px(100, "%"),
        "align": "center",
        "_element_width": "initial",
        "_element_custom_width": px(170),
        "_element_custom_width_mobile": px(140),
    })
    art = widget("html", {"html": ART + "\n<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>",
                          "_css_classes": "un-404-art-wrap"})
    eyebrow = heading("Página não encontrada", "p", "#FFFFFF",
                      typo("typography", HANKEN, 12, 800, lh=14, ls=1.6, transform="uppercase"),
                      align="center",
                      extra={"_element_width": "auto", "_background_background": "classic",
                             "_background_color": RED, "_border_radius": dims(999),
                             "_padding": dims(8, 14, 8, 14)})
    title = heading('Ops! Esta página <span class="un-mark-red">mudou de endereço</span>', "h1", "#FFFFFF",
                    typo("typography", HANKEN, 52, 700, lh=58, ls=-2, size_t=44, size_m=32, lh_t=50, lh_m=38,
                         ls_m=-1),
                    align="center")
    body = text("<p>Nosso site foi renovado e alguns links antigos deixaram de existir. "
                "Mas não se preocupe: a gente te ajuda a encontrar o caminho.</p>",
                "rgba(255, 255, 255, 0.82)", typo("typography", HANKEN, 19, 400, lh=29, size_m=16, lh_m=25),
                align="center",
                extra={"_element_width": "initial", "_element_custom_width": px(600),
                       "_element_custom_width_mobile": px(100, "%")})
    home_btn = button("Voltar para a Home", RED, "#FFFFFF", typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                      dims(16, 28, 16, 28), icon=14, css_classes="un-404-home",
                      shadow={"horizontal": 0, "vertical": 14, "blur": 30, "spread": 0,
                              "color": "rgba(241, 5, 5, 0.35)"},
                      extra={"link": lnk(SITE), "button_background_hover_color": "#FFFFFF",
                             "hover_color": NAVY})
    contact_btn = button("Fale com a gente", "rgba(255, 255, 255, 0)", "#FFFFFF",
                         typo("typography", HANKEN, 17, 700, lh=22, size_m=16), dims(15, 26, 15, 26),
                         css_classes="un-404-contact",
                         extra={"link": lnk(CONTATO), "border_border": "solid", "border_width": dims(1),
                                "border_color": "rgba(255, 255, 255, 0.4)",
                                "button_background_hover_color": "#FFFFFF", "hover_color": NAVY,
                                "button_hover_border_color": "#FFFFFF"})
    actions = container({
        "content_width": "full",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "width_mobile": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "flex_align_items_mobile": "stretch",
        "flex_gap": gap(14),
        "margin": dims(10, 0, 0, 0),
    }, [home_btn, contact_btn])
    for b in actions["elements"]:
        b["settings"]["align_mobile"] = "justify"

    shortcuts_label = heading("Ou vá direto para:", "p", "rgba(255, 255, 255, 0.6)",
                              typo("typography", HANKEN, 14, 600, lh=18, ls=0.4), align="center")
    shortcuts = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap": "wrap",
        "flex_wrap_mobile": "wrap",
        "flex_justify_content": "center",
        "flex_gap": gap(10),
        "flex_gap_mobile": gap(8),
    }, [pill(label, url) for label, url in LINKS])

    center = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
        "flex_gap": gap(18),
        "flex_gap_mobile": gap(14),
        "_flex_size": "grow",
    }, [add(art, anim("fadeIn")), add(eyebrow, anim("fadeInUp", 200)), add(title, anim("fadeInUp", 300)),
        add(body, anim("fadeInUp", 400)), add(actions, anim("fadeInUp", 500)),
        add(container({"content_width": "full", "flex_direction": "column", "flex_align_items": "center",
                       "flex_gap": gap(12), "margin": dims(26, 0, 0, 0), "margin_mobile": dims(14, 0, 0, 0)},
                      [shortcuts_label, shortcuts]), anim("fadeInUp", 600))])
    center["settings"].pop("_flex_size")  # só centraliza; sem "grow" + 100%

    return container({
        "content_width": "boxed",
        "boxed_width": px(1000),
        "html_tag": "main",
        "min_height": px(100, "vh"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "space-between",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(28),
        "padding": dims(36, 24, 64, 24),
        "padding_mobile": dims(24, 16, 48, 16),
        "background_background": "gradient",
        "background_color": NAVY,
        "background_color_stop": px(0, "%"),
        "background_color_b": "#0D1261",
        "background_color_b_stop": px(100, "%"),
        "background_gradient_type": "radial",
        "background_gradient_position": "center center",
        "css_classes": "gt-root un-404",
    }, [add(logo, anim("fadeInDown")), center, widget("spacer", {"space": px(1)})], inner=False)


def main():
    data = {"content": [build()], "page_settings": [], "version": "0.4",
            "title": "Unicultura - Página 404", "type": "error-404"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
