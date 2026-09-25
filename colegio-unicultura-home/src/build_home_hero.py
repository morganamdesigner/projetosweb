#!/usr/bin/env python3
"""Gera o JSON do HERO v2 da Home (cabeçalho branco + cartão azul com foto à direita).

Substitui o 1º bloco da Home (o topo com hero/menu). Traz também, num widget HTML,
o CSS/JS da página inteira (animações, parallax, barra de progresso, contador).
Saída: ../hero-home-elementor.json

Uso:  python3 build_home_hero.py [export-da-home.json]
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import (  # noqa: E402
    HANKEN, add, anim, button, container, dims, gap, heading, icon_list, px, text, typo, widget,
)

HOME_SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/195424d6-elementor-831-2026-09-25.json")
OUT = os.path.join(HERE, "..", "hero-home-elementor.json")
CSS_FILE = os.path.join(HERE, "un-home-v2.css")
JS_FILE = os.path.join(HERE, "un-home-v2.js")

base._counter[0] = 11000  # faixa própria de IDs

PAGE_BG = "#FDFDFF"
CARD_BG = "#0D1261"
NAVY = "#010658"
INK = "#1C1F4F"
RED = "#F10505"
ORANGE = "#FFB867"
WHITE = "#FFFFFF"
UPLOADS = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/"
HERO_PHOTOS = [UPLOADS + "foto2-home-2.webp", UPLOADS + "group_6.webp"]

home = json.load(open(HOME_SRC, encoding="utf-8"))


def find(elements, id_):
    for e in elements:
        if e["id"] == id_:
            return e
        r = find(e["elements"], id_)
        if r:
            return r


def logo(id_, url, alt, width, width_m):
    return widget("image", {
        "image": {"id": id_, "url": UPLOADS + url, "alt": alt, "source": "library", "size": ""},
        "image_size": "full",
        "align": "left",
        "width": px(100, "%"),
        "_element_width": "initial",
        "_element_custom_width": px(width),
        "_element_custom_width_mobile": px(width_m),
    })


def logos(color):
    if color:
        imgs = [logo(79, "logo-unicultura-svg-1.svg", "Colégio Unicultura", 104, 82),
                logo(27, "logo-garatuha.webp", "Garatuja", 80, 62)]
    else:
        imgs = [logo(715, "logo-branca-uni.svg", "Colégio Unicultura", 84, 70),
                logo(716, "logo-garatuja-branca.webp", "Garatuja", 70, 58)]
    return container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(14),
        "flex_gap_mobile": gap(10),
        "_flex_size": "none",
        "css_classes": "un-logos--color" if color else "un-logos--white",
    }, imgs)


# ---------------------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------------------

def header():
    nav = copy.deepcopy(find(home["content"], "5f9d9c1d"))  # menu do WordPress da Home (menu 3)
    nav["id"] = base.new_id()
    ns = nav["settings"]
    for k in ("hide_mobile", "_element_width", "_element_custom_width", "_element_custom_width_mobile",
              "_element_custom_width_tablet"):
        ns.pop(k, None)
    ns.update({
        "pointer": "none",               # o ponto vermelho do item ativo vem do CSS
        "align_items": "center",
        "color_menu_item": INK,
        "color_menu_item_hover": RED,
        "color_menu_item_active": INK,
        "menu_typography_typography": "custom",
        "menu_typography_font_family": HANKEN,
        "menu_typography_font_size": px(16),
        "menu_typography_font_weight": "500",
        "padding_horizontal_menu_item": px(16),
        "toggle_color": NAVY,
        "toggle_background_color": "#F0F2FA",
        "_flex_size": "grow",
    })
    social = widget("social-icons", {
        "social_icon_list": [
            {"_id": base.new_id(), "social_icon": {"value": "fab fa-facebook-f", "library": "fa-brands"},
             "link": {"url": "", "is_external": "true", "nofollow": "", "custom_attributes": ""}},
            {"_id": base.new_id(), "social_icon": {"value": "fab fa-instagram", "library": "fa-brands"},
             "link": {"url": "", "is_external": "true", "nofollow": "", "custom_attributes": ""}},
        ],
        "shape": "circle",
        "icon_color": "custom",
        "icon_primary_color": "rgba(255, 255, 255, 0)",
        "icon_secondary_color": INK,
        "icon_size": px(15),
        "icon_padding": px(0.95, "em"),
        "icon_spacing": px(10),
        "image_border_border": "solid",
        "image_border_width": dims(1),
        "image_border_color": "#D7D8E5",
        "hover_primary_color": RED,
        "hover_secondary_color": WHITE,
        "_flex_size": "none",
        "hide_mobile": "hidden-mobile",
        "__globals__": {"icon_primary_color": "", "icon_secondary_color": "", "image_border_color": ""},
    })
    cta = button("Agendar visita", NAVY, WHITE, typo("typography", HANKEN, 16, 700, lh=22),
                 dims(12, 12, 12, 24), radius="999", icon=14, css_classes="un-btn-arrow",
                 extra={"_flex_size": "none", "hide_mobile": "hidden-mobile"})
    bar = container({
        "content_width": "full",
        "html_tag": "header",
        "width": px(100, "%"),
        "min_height": px(100),
        "min_height_mobile": px(72),
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_justify_content": "space-between",
        "flex_wrap_mobile": "nowrap",
        "flex_gap": gap(16),
        "padding": dims(0, 20, 0, 44),
        "padding_tablet": dims(0, 12, 0, 20),
        "padding_mobile": dims(0, 4, 0, 4),
        "css_classes": "un-header",
    }, [logos(True), logos(False), nav, social, cta])
    return container({  # guarda a altura do cabeçalho quando ele vira flutuante
        "content_width": "full",
        "min_height": px(100),
        "min_height_mobile": px(72),
        "flex_direction": "column",
        "z_index": 20,
        "css_classes": "un-header-wrap",
    }, [bar])


# ---------------------------------------------------------------------------
# Cartão do hero
# ---------------------------------------------------------------------------

def hero_card():
    pill = heading('<span class="un-dot"></span>Educação Infantil ao Ensino Médio', "p", WHITE,
                   typo("typography", HANKEN, 13, 700, lh=16, ls=0.7, transform="uppercase", size_m=11, lh_m=14),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.06)", "_border_border": "solid",
                          "_border_width": dims(1), "_border_color": "rgba(255, 255, 255, 0.28)",
                          "_border_radius": dims(999), "_padding": dims(10, 18, 10, 16),
                          "_padding_mobile": dims(8, 14, 8, 12)})
    title = heading(
        f'Do primeiro dia de aula à formatura, aqui começa a <span style="color:{ORANGE}">trajetória</span> '
        'do seu filho.', "h1", WHITE,
        typo("typography", HANKEN, 66, 700, lh=66, ls=-2.8, size_t=54, size_m=38, lh_t=56, lh_m=40, ls_m=-1.5),
        extra={"_element_width": "initial", "_element_custom_width": px(640),
               "_element_custom_width_tablet": px(100, "%")})
    intro = text("<p>Acompanhamos cada fase com acolhimento, intencionalidade pedagógica e excelência "
                 "acadêmica.</p>", "rgba(255, 255, 255, 0.85)",
                 typo("typography", HANKEN, 19, 400, lh=30, size_m=16, lh_m=25),
                 extra={"_element_width": "initial", "_element_custom_width": px(470),
                        "_element_custom_width_mobile": px(100, "%")})
    primary = button("Agendar visita", WHITE, INK, typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                     dims(14, 14, 14, 28), radius="999", icon=18, css_classes="un-btn-arrow",
                     shadow={"horizontal": 0, "vertical": 8, "blur": 24, "spread": 0,
                             "color": "rgba(241, 5, 5, 0.25)"})
    secondary = button("Conhecer a proposta", "rgba(255, 255, 255, 0)", WHITE,
                       typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                       dims(14, 8, 14, 8), radius="999", css_classes="un-btn-link",
                       extra={"selected_icon": {"value": "fas fa-arrow-down", "library": "fa-solid"},
                              "icon_align": "right", "icon_indent": px(10)})
    actions = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(28),
        "flex_gap_mobile": gap(12),
        "margin": dims(14, 0, 0, 0),
    }, [primary, secondary])
    content = container({
        "content_width": "full",
        "width": px(700),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(26),
        "flex_gap_mobile": gap(18),
    }, [
        add(pill, anim("fadeInUp")),
        add(title, anim("fadeInUp", 120)),
        add(intro, anim("fadeInUp", 240)),
        add(actions, anim("fadeInUp", 360)),
    ])

    stars = heading("★★★★★", "p", ORANGE, typo("typography", HANKEN, 18, 400, lh=18, ls=3),
                    extra={"_flex_size": "none"})
    proof = heading('<strong style="font-weight:700;color:#FFFFFF">+1.200 famílias</strong> confiam na nossa escola',
                    "p", "rgba(255, 255, 255, 0.8)", typo("typography", HANKEN, 16, 400, lh=22, size_m=15),
                    extra={"_css_classes": "un-count", "_attributes": "data-delay|700"})
    social_proof = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_align_items": "center",
        "flex_gap": gap(14),
    }, [stars, proof])
    segments = icon_list(
        [{"text": t, "icon": {"value": "fas fa-circle", "library": "fa-solid"}}
         for t in ("Educação Infantil", "Fundamental I", "Fundamental II", "Ensino Médio")],
        typo("icon_typography", HANKEN, 16, 600, lh=22, size_m=14),
        WHITE, icon_color=RED, inline=True, space=20, icon_size=6, text_indent=18,
        extra={"_css_classes": "un-segments", "text_color_hover": ORANGE,
               "space_between_mobile": px(10), "text_indent_mobile": px(10)})
    strip = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "space-between",
        "flex_align_items": "center",
        "flex_align_items_mobile": "flex-start",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(14),
        "padding": dims(30, 0, 34, 0),
        "padding_mobile": dims(22, 0, 26, 0),
        "margin": dims(64, 0, 0, 0),
        "margin_mobile": dims(40, 0, 0, 0),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.16)",
    }, [social_proof, segments])

    card = container({
        "content_width": "full",
        "width": px(100, "%"),
        "min_height": px(768),
        "min_height_tablet": px(0),
        "min_height_mobile": px(0),
        "flex_direction": "column",
        "flex_justify_content": "space-between",
        "padding": dims(76, 88, 0, 88),
        "padding_tablet": dims(64, 48, 0, 48),
        "padding_mobile": dims(24, 22, 0, 22),
        "overflow": "hidden",
        "border_radius": dims(40),
        "border_radius_mobile": dims(28),
        "background_background": "slideshow",
        "background_color": CARD_BG,
        "background_slideshow_gallery": [{"id": "", "url": u} for u in HERO_PHOTOS],
        "background_slideshow_loop": "yes",
        "background_slideshow_slide_duration": 6000,
        "background_slideshow_slide_transition": "fade",
        "background_slideshow_transition_duration": 1500,
        "background_slideshow_background_size": "cover",
        "background_slideshow_background_position": "center right",
        "background_slideshow_ken_burns": "yes",
        "background_slideshow_ken_burns_zoom_direction": "in",
        # azul sólido à esquerda dissolvendo na foto à direita; no celular, de baixo para cima
        "background_overlay_background": "gradient",
        "background_overlay_color": CARD_BG,
        "background_overlay_color_stop": px(36, "%"),
        "background_overlay_color_stop_tablet": px(40, "%"),
        "background_overlay_color_stop_mobile": px(52, "%"),
        "background_overlay_color_b": "rgba(13, 18, 97, 0)",
        "background_overlay_color_b_stop": px(72, "%"),
        "background_overlay_color_b_stop_tablet": px(95, "%"),
        "background_overlay_color_b_stop_mobile": px(74, "%"),
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": px(90, "deg"),
        "background_overlay_gradient_angle_mobile": px(0, "deg"),
        "background_overlay_opacity": px(1),
        "css_classes": "un-hero",
    }, [content, add(strip, anim("fadeIn", 500))])
    # celular: o conteúdo começa abaixo da foto
    content["settings"]["margin_mobile"] = {"unit": "vw", "top": "62", "right": "0", "bottom": "0",
                                            "left": "0", "isLinked": False}
    return card


def build():
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    js = open(JS_FILE, encoding="utf-8").read().strip()
    return container({
        "content_width": "boxed",
        "boxed_width": px(1480),
        "flex_direction": "column",
        "flex_gap": gap(0),
        "padding": dims(0, 24, 0, 24),
        "padding_tablet": dims(0, 16, 0, 16),
        "padding_mobile": dims(0, 12, 0, 12),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-top",
    }, [header(), hero_card(),
        widget("html", {"html": "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"})],
        inner=False)


def main():
    data = {"content": [build()], "page_settings": [], "version": "0.4",
            "title": "Unicultura - Home Hero v2", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
