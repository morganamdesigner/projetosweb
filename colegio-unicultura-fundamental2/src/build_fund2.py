#!/usr/bin/env python3
"""Gera o JSON da página "Ensino Fundamental II" (Colégio Unicultura) - página inteira, sem o rodapé.

Segue o modelo da página do Fundamental I (colegio-unicultura-fundamental1/src/build_fund1.py):
mesmo cabeçalho e cartão azul do hero da Home (uma foto só), galeria em movimento, Poliedro,
equipe e CTA. As seções próprias do Fundamental II (três eixos, "Aprofundar...", apoio/monitoria)
foram redesenhadas aqui, com os textos da página atual.
Saída: ../fundamental2-elementor.json

Uso:  python3 build_fund2.py [export-da-pagina-fundamental-2.json]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F1_DIR = os.path.join(HERE, "..", "..", "colegio-unicultura-fundamental1", "src")
sys.path.insert(0, F1_DIR)

F2_SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/8d2ff482-elementor-1030-2026-09-28.json")
sys.argv = sys.argv[:1]  # o build_fund1 também lê sys.argv

import build_fund1 as f1  # noqa: E402
from build_fund1 import (  # noqa: E402
    CARD_BG, HANKEN, INK, NAVY, ORANGE, PAGE_BG, RED, WHITE,
    add, anim, base, button, container, dims, eyebrow, gap, heading, icon_list, media, parallax, px, text, typo,
    widget,
)

OUT = os.path.join(HERE, "..", "fundamental2-elementor.json")
HOME_SRC_DIR = f1.HOME_SRC_DIR

# as funções do Fundamental I passam a ler esta página
f1.page = json.load(open(F2_SRC, encoding="utf-8"))
f1.CSS_FILES = f1.CSS_FILES + [os.path.join(HERE, "un-fund2.css")]
f1.JS_FILES = f1.JS_FILES + [os.path.join(HERE, "un-fund2.js")]
find, src_text = f1.find, f1.src_text
page = f1.page

base._counter[0] = 19000  # faixa própria de IDs

HERO_F2 = {
    "pill": "Ensino Fundamental · 5º ao 9º ano",
    "title": f'Conhecimento, autonomia e <span style="color:{ORANGE}">novos desafios.</span>',
    "intro_id": "78d5a52d",
    "secondary": ("Conhecer os eixos", "#os-eixos"),
    # a página atual não tinha foto no fundo do hero (só o slideshow antigo): usamos a 1ª foto dele
    "photo": (357, "group_6.webp"),
    "segment": 3,  # "Fundamental II" em destaque
}


# ---------------------------------------------------------------------------
# 2. Faixa em movimento com as palavras-chave da etapa
# ---------------------------------------------------------------------------

MARQUEE_WORDS = ["Autonomia", "Cultura Digital", "Cultura Olímpica", "Plantão de Monitoria",
                 "Sistema Poliedro", "Novos desafios"]


def build_marquee():
    line = "".join(f'{w}<span class="un-star">✦</span>' for w in MARQUEE_WORDS) * 2

    def words(hidden=False):
        extra = {"_css_classes": "un-mq-text"}
        if hidden:
            extra["_attributes"] = "aria-hidden|true"  # cópia só para o movimento contínuo (Pro)
        return heading(line, "p", WHITE,
                       typo("typography", HANKEN, 40, 700, lh=48, ls=-1.2, size_m=26, lh_m=32, ls_m=-0.6),
                       extra=extra)

    track = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "css_classes": "un-mq-track",
    }, [words(), words(hidden=True)])
    band = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "padding": dims(22, 0, 22, 0),
        "padding_mobile": dims(14, 0, 14, 0),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "un-mq-band",
    }, [track])
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "padding": dims(64, 0, 24, 0),
        "padding_mobile": dims(44, 0, 8, 0),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-mq",
    }, [band], inner=False)


# ---------------------------------------------------------------------------
# 3. Três eixos que ganham força nessa fase (foto fixa + linha do tempo que se preenche)
# ---------------------------------------------------------------------------

def eixo_card(index, item):
    title_html, desc = item["text"].split("<br>", 1)
    title = title_html.replace("<b>", "").replace("</b>", "").strip().rstrip(".")
    card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(8),
        "padding": dims(26, 30, 28, 30),
        "padding_mobile": dims(22, 22, 24, 22),
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(22),
        "border_radius_mobile": dims(18),
        "css_classes": "un-eixo un-io",
    }, [
        heading(f"{index:02d}", "p", ORANGE, typo("typography", HANKEN, 14, 700, lh=16, ls=1.4)),
        heading(title, "h3", WHITE, typo("typography", HANKEN, 24, 700, lh=30, ls=-0.6, size_m=20, lh_m=26)),
        text("<p>" + desc.strip() + "</p>", "rgba(255, 255, 255, 0.78)",
             typo("typography", HANKEN, 17, 400, lh=26, size_m=15, lh_m=23)),
    ])
    return card


def build_eixos():
    items = find(page["content"], "61f3e254")["settings"]["icon_list"]
    photo = widget("image", {
        "image": find(page["content"], "4ddbaa2a")["settings"]["image"],
        "image_size": "full",
        "width": px(100, "%"),
        "_css_classes": "un-eixos-photo",
    })
    photo_col = container({
        "content_width": "full",
        "width": px(46, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "css_classes": "un-sticky",
    }, [add(photo, anim("zoomIn"))])

    title = heading(src_text("6388db9e"), "h2", NAVY,
                    typo("typography", HANKEN, 48, 700, lh=52, ls=-1.8, size_t=42, size_m=32, lh_t=46, lh_m=36,
                         ls_m=-1.2))
    lead = text("<p>" + src_text("66cc3c02") + "</p>", INK,
                typo("typography", HANKEN, 18, 400, lh=28, size_m=16, lh_m=25))
    timeline = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(18),
        "flex_gap_mobile": gap(14),
        "padding": dims(0, 0, 0, 44),
        "padding_mobile": dims(0, 0, 0, 30),
        "margin": dims(14, 0, 0, 0),
        "css_classes": "un-timeline",
    }, [eixo_card(i + 1, it) for i, it in enumerate(items)])
    text_col = container({
        "content_width": "full",
        "width": px(54, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(20),
    }, [add(eyebrow("Anos Finais"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(lead, anim("fadeInUp", 200)),
        timeline])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "_element_id": "os-eixos",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "flex-start",
        "flex_align_items_tablet": "stretch",
        "flex_gap": gap(80),
        "flex_gap_tablet": gap(48),
        "flex_gap_mobile": gap(36),
        "padding": dims(96, 24, 120, 24),
        "padding_tablet": dims(80, 24, 96, 24),
        "padding_mobile": dims(56, 16, 72, 16),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-eixos",
    }, [photo_col, text_col], inner=False)


# ---------------------------------------------------------------------------
# 4. Aprofundar, argumentar e investigar (cartão com a foto do estudante)
# ---------------------------------------------------------------------------

def build_aprofundar():
    title = heading(
        '<span class="un-word">Aprofundar,</span> <span class="un-word">argumentar</span> '
        f'<span class="un-word">e <span style="color:{ORANGE}">investigar.</span></span>',
        "h2", WHITE,
        typo("typography", HANKEN, 64, 700, lh=66, ls=-2.4, size_t=52, size_m=36, lh_t=56, lh_m=40, ls_m=-1.3),
        extra={"_css_classes": "un-words un-io", "_element_width": "initial", "_element_custom_width": px(560),
               "_element_custom_width_tablet": px(100, "%")})
    body = text("<p>" + src_text("7338ad53", "editor").strip() + "</p>", "rgba(255, 255, 255, 0.85)",
                typo("typography", HANKEN, 19, 400, lh=30, size_m=16, lh_m=25),
                extra={"_element_width": "initial", "_element_custom_width": px(460),
                       "_element_custom_width_mobile": px(100, "%")})
    content = container({
        "content_width": "full",
        "width": px(600),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(22),
    }, [add(eyebrow("Rumo ao Ensino Médio", ORANGE), anim("fadeInUp")), title,
        add(body, anim("fadeInUp", 500))])
    return photo_card_section(content, find(page["content"], "4f893229")["settings"]["background_image"],
                              "un-aprofundar")


def photo_card_section(content, background_image, section_class):
    """Cartão azul com foto (degradê como o do hero; no celular a foto fica no topo)."""
    content["settings"]["margin_mobile"] = {"unit": "vw", "top": "62", "right": "0", "bottom": "0",
                                            "left": "0", "isLinked": False}
    card = container({
        "content_width": "full",
        "min_height": px(640),
        "min_height_tablet": px(0),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "padding": dims(88),
        "padding_tablet": dims(64, 48, 64, 48),
        "padding_mobile": dims(24, 22, 36, 22),
        "overflow": "hidden",
        "border_radius": dims(40),
        "border_radius_mobile": dims(28),
        "background_background": "classic",
        "background_color": CARD_BG,
        "background_image": background_image,
        "background_position": "center right",
        "background_repeat": "no-repeat",
        "background_size": "cover",
        "background_position_mobile": "initial",
        "background_xpos_mobile": px(88, "%"),
        "background_ypos_mobile": px(0),
        "background_size_mobile": "initial",
        "background_bg_width_mobile": px(230, "%"),
        "background_overlay_background": "gradient",
        "background_overlay_color": CARD_BG,
        "background_overlay_color_stop": px(34, "%"),
        "background_overlay_color_stop_tablet": px(45, "%"),
        "background_overlay_color_stop_mobile": px(52, "%"),
        "background_overlay_color_b": "rgba(13, 18, 97, 0)",
        "background_overlay_color_b_stop": px(70, "%"),
        "background_overlay_color_b_stop_tablet": px(95, "%"),
        "background_overlay_color_b_stop_mobile": px(74, "%"),
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": px(90, "deg"),
        "background_overlay_gradient_angle_mobile": px(0, "deg"),
        "background_overlay_opacity": px(1),
        "css_classes": "un-photo-card",
    }, [content])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1432),
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(24, 24, 110, 24),
        "padding_tablet": dims(16, 16, 88, 16),
        "padding_mobile": dims(8, 12, 64, 12),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root " + section_class,
    }, [add(card, anim("fadeInUp"))], inner=False)


# ---------------------------------------------------------------------------
# 5. Apoio que acompanha de perto (Plantão de Monitoria)
# ---------------------------------------------------------------------------

def build_apoio():
    logo = widget("image", {
        "image": find(page["content"], "77fbef3f")["settings"]["image"],
        "image_size": "full",
        "width": px(100, "%"),
        "_element_width": "initial",
        "_element_custom_width": px(340),
        "_element_custom_width_tablet": px(260),
        "_element_custom_width_mobile": px(180),
        "_css_classes": "un-float",
    })
    logo_col = container({
        "content_width": "full",
        "width": px(42, "%"),
        "width_tablet": px(100, "%"),
        "min_height": px(420),
        "min_height_tablet": px(320),
        "min_height_mobile": px(240),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "css_classes": "un-apoio-logo",
    }, [add(logo, anim("zoomIn"), parallax(-1))])

    title = heading(f'Apoio que acompanha <span style="color:{ORANGE}">de perto</span>', "h2", WHITE,
                    typo("typography", HANKEN, 54, 700, lh=58, ls=-2, size_t=44, size_m=34, lh_t=48, lh_m=38,
                         ls_m=-1.2),
                    extra={"_element_width": "initial", "_element_custom_width": px(520),
                           "_element_custom_width_tablet": px(100, "%")})
    body = text("<p>" + src_text("12c38bb9", "editor").strip() + "</p>", "rgba(255, 255, 255, 0.82)",
                typo("typography", HANKEN, 19, 400, lh=30, size_m=16, lh_m=25),
                extra={"_element_width": "initial", "_element_custom_width": px(500),
                       "_element_custom_width_tablet": px(100, "%")})
    checks = icon_list(
        [{"text": t, "icon": {"value": "fas fa-check", "library": "fa-solid"}}
         for t in ("Revisão de conteúdos", "Esclarecimento de dúvidas", "Fortalecimento das aprendizagens")],
        typo("icon_typography", HANKEN, 17, 600, lh=24, size_m=15),
        WHITE, icon_color=ORANGE, space=14, icon_size=13, text_indent=14,
        extra={"_css_classes": "un-checks"})
    cta = button("Ver todos os diferenciais", WHITE, INK, typo("typography", HANKEN, 17, 700, lh=22, size_m=15),
                 dims(12, 12, 12, 26), radius="999", icon=16, css_classes="un-btn-arrow",
                 extra={"_flex_align_self": "flex-start"})
    text_col = container({
        "content_width": "full",
        "width": px(58, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(22),
    }, [add(eyebrow("Plantão de Monitoria", ORANGE), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(body, anim("fadeInUp", 200)),
        add(checks, anim("fadeInUp", 300)),
        add(cta, anim("fadeInUp", 400))])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(64),
        "flex_gap_tablet": gap(24),
        "padding": dims(120, 24, 120, 24),
        "padding_tablet": dims(88, 24, 96, 24),
        "padding_mobile": dims(64, 16, 72, 16),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-root un-apoio",
    }, [logo_col, text_col], inner=False)


def main():
    data = {
        "content": [
            f1.build_top(HERO_F2),
            build_marquee(),
            build_eixos(),
            build_aprofundar(),
            build_apoio(),
            f1.build_galeria(),
            f1.build_poliedro(("c5191e0", "56820ec3", "6748ce5a")),
            f1.build_equipe("5c3af80f"),
            f1.build_cta("3ee35c23"),
        ],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Ensino Fundamental II",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
