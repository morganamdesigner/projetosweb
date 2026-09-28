#!/usr/bin/env python3
"""Gera o JSON da página "Ensino Fundamental I" (Colégio Unicultura) - página inteira, sem o rodapé.

- Topo: o mesmo cabeçalho + cartão azul do hero v2 da Home, mas com UMA foto de fundo
  (background-ensino-fundamental-1.webp), sem slideshow.
- Seções seguintes: os mesmos textos e imagens da página atual, redesenhados, com animações de
  entrada e efeitos de scroll (CSS/JS embutidos em widgets HTML).
Saída: ../fundamental1-elementor.json

Uso:  python3 build_fund1.py [export-da-pagina-fundamental-1.json]
"""
import copy
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOME_SRC_DIR = os.path.join(HERE, "..", "..", "colegio-unicultura-home", "src")
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))
sys.path.insert(0, HOME_SRC_DIR)

F1_SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/941f6dc2-elementor-973-2026-09-28.json")
sys.argv = sys.argv[:1]  # os módulos da Home também leem sys.argv

import build_elementor_json as base  # noqa: E402
import build_home_hero as home_hero  # noqa: E402  (cabeçalho da Home)
# a Garatuja também tem um build_secao_galeria.py: carrega o da Home pelo caminho
_spec = importlib.util.spec_from_file_location("home_galeria", os.path.join(HOME_SRC_DIR, "build_secao_galeria.py"))
galeria = importlib.util.module_from_spec(_spec)  # faixa de fotos em movimento
_spec.loader.exec_module(galeria)
from build_elementor_json import (  # noqa: E402
    HANKEN, add, anim, button, container, dims, gap, heading, icon_list, parallax, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "fundamental1-elementor.json")
CSS_FILES = [os.path.join(HOME_SRC_DIR, "un-home-v2.css"), os.path.join(HERE, "un-fund1.css")]
JS_FILES = [os.path.join(HOME_SRC_DIR, "un-home-v2.js"), os.path.join(HERE, "un-fund1.js")]

base._counter[0] = 17000  # faixa própria de IDs

PAGE_BG = "#FDFDFF"
CARD_BG = "#0D1261"
NAVY = "#010658"
INK = "#1C1F4F"
RED = "#F10505"
ORANGE = "#FFB867"
WHITE = "#FFFFFF"
UPLOADS = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/"

page = json.load(open(F1_SRC, encoding="utf-8"))


def find(elements, id_):
    for e in elements:
        if e["id"] == id_:
            return e
        r = find(e.get("elements", []), id_)
        if r:
            return r


def src(id_):
    """Cópia de um elemento da página atual (mantém o ID original)."""
    return copy.deepcopy(find(page["content"], id_))


def src_text(id_, key="title"):
    return find(page["content"], id_)["settings"][key]


def media(id_, file):
    return {"id": id_, "url": UPLOADS + file, "alt": "", "source": "library", "size": ""}


def hanken(el):
    """Troca Poppins por Hanken Grotesk em todas as tipografias do elemento (e filhos)."""
    s = el["settings"]
    if isinstance(s, dict):
        for k, v in list(s.items()):
            if k.endswith("_font_family") and v == "Poppins":
                s[k] = HANKEN
    for c in el.get("elements", []):
        hanken(c)
    return el


def eyebrow(label, color=RED, align="left"):
    return heading(label, "p", color, typo("typography", HANKEN, 13, 700, lh=16, ls=1.4, transform="uppercase"),
                   align=align)


def html_widget(css_files, js_files):
    css = "\n\n".join(open(f, encoding="utf-8").read().strip() for f in css_files)
    js = "\n\n".join(open(f, encoding="utf-8").read().strip() for f in js_files)
    return widget("html", {"html": "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"})


# ---------------------------------------------------------------------------
# 1. Topo: cabeçalho da Home + cartão azul com a foto do Fundamental I
# ---------------------------------------------------------------------------

def avatars():
    imgs = []
    for id_, file in ((18, "container-5.webp"), (19, "2.webp"), (20, "3.webp")):  # fotos da prova social atual
        imgs.append(widget("image", {
            "image": media(id_, file),
            "image_size": "thumbnail",
            "width": px(100, "%"),
            "height": px(38),
            "object-fit": "cover",
            "image_border_radius": dims(999),
            "image_border_border": "solid",
            "image_border_width": dims(2),
            "image_border_color": CARD_BG,
            "_element_width": "initial",
            "_element_custom_width": px(38),
        }))
    return container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_align_items": "center",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},  # senão 100% sem encolher
        "_flex_size": "none",
        "css_classes": "un-avatars",
    }, imgs)


HERO_F1 = {
    "pill": "Ensino Fundamental · 3º ao 5º ano",
    "title": f'Consolidar conhecimentos. <span style="color:{ORANGE}">Desenvolver autonomia.</span>',
    "intro_id": "38dccf55",
    "secondary": ("Conhecer a etapa", "#a-etapa"),
    "photo": (473, "background-ensino-fundamental-1.webp"),
    "segment": 2,  # "Fundamental I" em destaque
}


def hero_card(cfg=HERO_F1):
    pill = heading('<span class="un-dot"></span>' + cfg["pill"], "p", WHITE,
                   typo("typography", HANKEN, 13, 700, lh=16, ls=0.7, transform="uppercase", size_m=11, lh_m=14),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.06)", "_border_border": "solid",
                          "_border_width": dims(1), "_border_color": "rgba(255, 255, 255, 0.28)",
                          "_border_radius": dims(999), "_padding": dims(10, 18, 10, 16),
                          "_padding_mobile": dims(8, 14, 8, 12)})
    title = heading(cfg["title"], "h1", WHITE,
                    typo("typography", HANKEN, 66, 700, lh=66, ls=-2.8, size_t=54, size_m=38, lh_t=56, lh_m=40,
                         ls_m=-1.5),
                    extra={"_element_width": "initial", "_element_custom_width": px(620),
                           "_element_custom_width_tablet": px(100, "%")})
    intro = text("<p>" + src_text(cfg["intro_id"], "editor").strip() + "</p>", "rgba(255, 255, 255, 0.85)",
                 typo("typography", HANKEN, 19, 400, lh=30, size_m=16, lh_m=25),
                 extra={"_element_width": "initial", "_element_custom_width": px(540),
                        "_element_custom_width_mobile": px(100, "%")})
    primary = button("Agendar visita", WHITE, INK, typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                     dims(14, 14, 14, 28), radius="999", icon=18, css_classes="un-btn-arrow",
                     shadow={"horizontal": 0, "vertical": 8, "blur": 24, "spread": 0,
                             "color": "rgba(241, 5, 5, 0.25)"})
    secondary = button(cfg["secondary"][0], "rgba(255, 255, 255, 0)", WHITE,
                       typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                       dims(14, 8, 14, 8), radius="999", css_classes="un-btn-link",
                       extra={"link": {"url": cfg["secondary"][1], "is_external": "", "nofollow": "", "custom_attributes": ""},
                              "selected_icon": {"value": "fas fa-arrow-down", "library": "fa-solid"},
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
        "css_classes": "un-hero-content",
    }, [
        add(pill, anim("fadeInUp")),
        add(title, anim("fadeInUp", 120)),
        add(intro, anim("fadeInUp", 240)),
        add(actions, anim("fadeInUp", 360)),
    ])
    # celular: o conteúdo começa abaixo da foto
    content["settings"]["margin_mobile"] = {"unit": "vw", "top": "62", "right": "0", "bottom": "0",
                                            "left": "0", "isLinked": False}

    proof = heading('<strong style="font-weight:700;color:#FFFFFF">+1.200 famílias</strong> confiam na nossa escola',
                    "p", "rgba(255, 255, 255, 0.8)", typo("typography", HANKEN, 16, 400, lh=22, size_m=15),
                    extra={"_css_classes": "un-count", "_attributes": "data-delay|700"})
    social_proof = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_align_items": "center",
        "flex_gap": gap(14),
    }, [avatars(), proof])
    segments = icon_list(
        [{"text": t, "icon": {"value": "fas fa-circle", "library": "fa-solid"}}
         for t in ("Educação Infantil", "Fundamental I", "Fundamental II", "Ensino Médio")],
        typo("icon_typography", HANKEN, 16, 600, lh=22, size_m=14),
        "rgba(255, 255, 255, 0.72)", icon_color=RED, inline=True, space=20, icon_size=6, text_indent=18,
        extra={"_css_classes": "un-segments un-segments--%d" % cfg["segment"], "text_color_hover": ORANGE,
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

    return container({
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
        # uma foto só (sem slideshow)
        "background_background": "classic",
        "background_color": CARD_BG,
        "background_image": media(*cfg["photo"]),
        "background_position": "center right",
        "background_repeat": "no-repeat",
        "background_size": "cover",
        # celular: foto no topo do cartão (230% da largura, ancorada à direita), dissolvendo no azul
        "background_position_mobile": "initial",
        "background_xpos_mobile": px(88, "%"),
        "background_ypos_mobile": px(0),
        "background_size_mobile": "initial",
        "background_bg_width_mobile": px(230, "%"),
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


def build_top(cfg=HERO_F1):
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
    }, [home_hero.header(), hero_card(cfg), html_widget(CSS_FILES, JS_FILES)], inner=False)


# ---------------------------------------------------------------------------
# 2. Uma etapa de transição e consolidação
# ---------------------------------------------------------------------------

def build_etapa():
    photo = widget("image", {
        # A imagem desta seção estava vazia na página atual: usamos uma foto da galeria (trocar à vontade)
        "image": media(337, "foto2-home.webp"),
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(580),
        "height_tablet": px(480),
        "height_mobile": px(380),
        "object-fit": "cover",
        "object-position": "center center",
        "image_border_radius": dims(32),
        "image_border_radius_mobile": dims(24),
        "_css_classes": "un-clip",
    })
    add(photo, anim("fadeIn"), parallax(-1))
    badge = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(2),
        "padding": dims(18, 24, 18, 24),
        "padding_mobile": dims(14, 18, 14, 18),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(20),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 18, "blur": 40, "spread": 0,
                                  "color": "rgba(1, 6, 88, 0.16)"},
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "css_classes": "un-badge",
    }, [
        heading("3º · 4º · 5º ano", "p", NAVY, typo("typography", HANKEN, 26, 700, lh=30, ls=-0.8, size_m=20, lh_m=24)),
        heading("Ensino Fundamental I", "p", RED,
                typo("typography", HANKEN, 12, 700, lh=16, ls=1.2, transform="uppercase")),
    ])
    media_col = container({
        "content_width": "full",
        "width": px(46, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "css_classes": "un-etapa-media un-io",
    }, [photo, badge])

    title = heading(src_text("20ec98ec"), "h2", NAVY,
                    typo("typography", HANKEN, 48, 700, lh=52, ls=-1.8, size_t=42, size_m=32, lh_t=46, lh_m=36,
                         ls_m=-1.2))
    body = text(src_text("24c9733a", "editor"), INK, typo("typography", HANKEN, 18, 400, lh=29, size_m=16, lh_m=26))
    quote = heading(src_text("133d0dc5").replace('class="vermelho"', 'class="un-mark"'), "h3", NAVY,
                    typo("typography", HANKEN, 30, 600, lh=36, ls=-0.9, size_m=24, lh_m=30),
                    extra={"_padding": dims(4, 0, 4, 24), "_border_border": "solid",
                           "_border_width": dims(0, 0, 0, 3), "_border_color": RED,
                           "_css_classes": "un-quote un-io", "_margin": dims(12, 0, 0, 0)})
    text_col = container({
        "content_width": "full",
        "width": px(54, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(22),
        "flex_gap_mobile": gap(16),
    }, [
        add(eyebrow("A etapa"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(body, anim("fadeInUp", 200)),
        add(quote, anim("fadeInUp", 300)),
    ])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "_element_id": "a-etapa",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(88),
        "flex_gap_tablet": gap(56),
        "flex_gap_mobile": gap(48),
        "padding": dims(130, 24, 120, 24),
        "padding_tablet": dims(96, 24, 88, 24),
        "padding_mobile": dims(72, 16, 64, 16),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-etapa",
    }, [media_col, text_col], inner=False)


# ---------------------------------------------------------------------------
# 3. O que priorizamos nessa etapa (12 cards; título fixo ao rolar no desktop)
# ---------------------------------------------------------------------------

def priority_card(item, index):
    card = widget("icon-box", {
        "selected_icon": item["selected_icon"],
        "title_text": item["text"],
        "description_text": "",
        "title_size": "h3",
        "position": "block-start",
        "text_align": "start",
        "icon_space": px(18),
        "icon_size": px(48),
        "icon_size_mobile": px(40),
        "title_color": NAVY,
        "hover_title_color": NAVY,
        **typo("title_typography", HANKEN, 18, 600, lh=24, ls=-0.3, size_m=15, lh_m=20),
        "_padding": dims(26, 24, 26, 24),
        "_padding_mobile": dims(18, 16, 18, 16),
        "_background_background": "classic",
        "_background_color": WHITE,
        "_border_border": "solid",
        "_border_width": dims(1),
        "_border_color": "rgba(1, 6, 88, 0.08)",
        "_border_radius": dims(22),
        "_border_radius_mobile": dims(18),
        "_css_classes": "un-prio",
    })
    return add(card, anim("fadeInUp", (index % 3) * 110))


def build_prioridades():
    items = []
    for list_id in ("66765b14", "3a9747a2", "53af84df"):
        items += find(page["content"], list_id)["settings"]["icon_list"]
    # ordem de leitura por linhas (3 colunas): intercala as 3 listas originais
    ordered = [items[c * 4 + r] for r in range(4) for c in range(3)]
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "width": px(62, "%"),
        "width_tablet": px(100, "%"),
        "grid_columns_grid": {"unit": "fr", "size": 3, "sizes": []},
        "grid_columns_grid_tablet": {"unit": "fr", "size": 2, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 2, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 4, "sizes": []},
        "grid_rows_grid_tablet": {"unit": "fr", "size": 6, "sizes": []},
        "grid_rows_grid_mobile": {"unit": "fr", "size": 6, "sizes": []},
        "grid_gaps": {"column": "18", "row": "18", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "10", "row": "10", "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }, [priority_card(it, i) for i, it in enumerate(ordered)])

    title = heading('O que priorizamos <span class="un-pill">nessa etapa:</span>', "h2", NAVY,
                    typo("typography", HANKEN, 52, 700, lh=62, ls=-2, size_t=42, size_m=34, lh_t=52, lh_m=44,
                         ls_m=-1.2),
                    extra={"_css_classes": "un-io"})
    lead = text("<p>Doze frentes que caminham juntas, do 3º ao 5º ano.</p>", INK,
                typo("typography", HANKEN, 18, 400, lh=28, size_m=16, lh_m=25))
    side = container({
        "content_width": "full",
        "width": px(38, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(18),
        "css_classes": "un-sticky",
    }, [add(eyebrow("Prioridades"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(lead, anim("fadeInUp", 200))])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(56),
        "flex_gap_tablet": gap(40),
        "flex_gap_mobile": gap(28),
        "padding": dims(120, 24, 120, 24),
        "padding_tablet": dims(96, 24, 96, 24),
        "padding_mobile": dims(72, 16, 72, 16),
        "background_background": "classic",
        "background_color": "#EDEEFA",
        "css_classes": "gt-root un-prioridades",
    }, [side, grid], inner=False)


# ---------------------------------------------------------------------------
# 4. Galeria: faixa de fotos em movimento (mesmo modelo da Home, mesmas 6 fotos)
# ---------------------------------------------------------------------------

def build_galeria():
    rows = container({
        "content_width": "full",
        "width": px(100, "%"),
        "flex_direction": "column",
    }, [galeria.photo_row(),
        html_widget([os.path.join(HOME_SRC_DIR, "un-galeria.css")], [os.path.join(HOME_SRC_DIR, "un-galeria.js")])])
    return container({
        "content_width": "full",
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(96, 0, 72, 0),
        "padding_mobile": dims(56, 0, 44, 0),
        "background_background": "classic",
        "background_color": "#F5F5F5",
        "css_classes": "gt-root un-gal",
    }, [add(rows, anim("fadeIn"))], inner=False)


# ---------------------------------------------------------------------------
# 5. Sistema de ensino (Poliedro)
# ---------------------------------------------------------------------------

def build_poliedro(ids=("182465e6", "64cbc719", "29d6236e")):
    title_id, text_id, logo_id = ids
    title = heading(src_text(title_id), "h2", NAVY,
                    typo("typography", HANKEN, 46, 700, lh=50, ls=-1.6, size_t=40, size_m=32, lh_t=44, lh_m=36,
                         ls_m=-1.1))
    body = text("<p>" + src_text(text_id, "editor").strip() + "</p>", INK,
                typo("typography", HANKEN, 18, 400, lh=29, size_m=16, lh_m=26))
    text_col = container({
        "content_width": "full",
        "width": px(58, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(18),
    }, [add(eyebrow("Parceria pedagógica"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(body, anim("fadeInUp", 200))])
    logo = widget("image", {
        "image": find(page["content"], logo_id)["settings"]["image"],
        "image_size": "full",
        "width": px(100, "%"),
        "_element_width": "initial",
        "_element_custom_width": px(300),
        "_element_custom_width_mobile": px(220),
        "_css_classes": "un-float",
    })
    logo_col = container({
        "content_width": "full",
        "width": px(42, "%"),
        "width_tablet": px(100, "%"),
        "min_height": px(280),
        "min_height_mobile": px(200),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": "#F4F5FB",
        "border_radius": dims(28),
        "css_classes": "un-poliedro-logo",
    }, [add(logo, anim("zoomIn", 200))])
    card = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(56),
        "flex_gap_mobile": gap(32),
        "padding": dims(56),
        "padding_tablet": dims(44),
        "padding_mobile": dims(28, 22, 22, 22),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(36),
        "border_radius_mobile": dims(28),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 24, "blur": 60, "spread": 0,
                                  "color": "rgba(1, 6, 88, 0.08)"},
    }, [text_col, logo_col])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1140),
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(110, 24, 110, 24),
        "padding_tablet": dims(88, 24, 88, 24),
        "padding_mobile": dims(64, 12, 64, 12),
        "background_background": "classic",
        "background_color": "#E6E7F2",
        "css_classes": "gt-root un-poliedro",
    }, [add(card, anim("fadeInUp"))], inner=False)


# ---------------------------------------------------------------------------
# 6. Nossa equipe de professores (carrossel nativo da página atual, corrigido)
# ---------------------------------------------------------------------------

TEACHER_NAMES = {  # foto do slide -> nome; estavam errados na página atual (CONFIRMAR)
    "camila.webp": "Camila",   # o nome estava "Beatriz" (repetido)
    "lucas.webp": "Lucas",     # o nome estava "Nome do Professor"
}


def teacher_name(slide):
    photo = slide["elements"][0]["settings"].get("image", {}).get("url", "")
    fixed = TEACHER_NAMES.get(photo.rsplit("/", 1)[-1])
    return fixed or slide["elements"][1]["settings"]["title"]


def build_equipe(section_id="44663ada"):
    sec = src(section_id)
    hanken(sec)
    s = sec["settings"]
    s["css_classes"] = "gt-root un-equipe"
    s["html_tag"] = "section"
    s["padding_mobile"] = dims(72, 20, 120, 20)  # o título estava colado no topo no celular

    eyebrow_box, title, carousel = sec["elements"]
    add(eyebrow_box, anim("fadeInUp"))
    add(title, anim("fadeIn", 100), classes="un-reveal")
    title["settings"]["title"] = 'Nossa <span class="un-it">equipe</span> de professores'
    title["settings"].pop("custom_css", None)  # o destaque agora vem do un-fund1.css

    # só os 4 slides com conteúdo (os outros 6 estavam vazios e apareciam como cards brancos)
    carousel["elements"] = [c for c in carousel["elements"] if c["elements"]]
    cs = carousel["settings"]
    cs["carousel_items"] = [{"slide_title": teacher_name(c), "_id": item["_id"]}
                            for c, item in zip(carousel["elements"], cs["carousel_items"])]
    for slide in carousel["elements"]:
        slide["settings"]["css_classes"] = "un-teacher"
        photo, name = slide["elements"][0], slide["elements"][1]
        photo["settings"]["_css_classes"] = "un-teacher-photo"
        name["settings"]["header_size"] = "h3"  # nomes eram H2
        name["settings"]["typography_font_style"] = "normal"
        name["settings"]["typography_font_weight"] = "600"
        name["settings"]["title"] = teacher_name(slide)
    add(carousel, anim("fadeInUp", 200))
    return sec


# ---------------------------------------------------------------------------
# 7. Quer conhecer o colégio de perto? (formulário da página atual)
# ---------------------------------------------------------------------------

def build_cta(section_id="1792b8a5"):
    sec = src(section_id)
    hanken(sec)
    sec["settings"]["css_classes"] = "gt-root un-cta"
    sec["settings"]["html_tag"] = "section"
    card = sec["elements"][0]
    add(card, anim("zoomIn"))
    photo = card["elements"][0]
    photo["settings"]["_css_classes"] = "un-cta-photo"
    icon, title, body, form = card["elements"][1]["elements"]
    add(icon, anim("fadeInUp", 200))
    add(title, anim("fadeInUp", 300))
    add(body, anim("fadeInUp", 400))
    add(form, anim("fadeInUp", 500), classes="un-form")
    return sec


def main():
    data = {
        "content": [build_top(), build_etapa(), build_prioridades(), build_galeria(), build_poliedro(),
                    build_equipe(), build_cta()],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Ensino Fundamental I",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
