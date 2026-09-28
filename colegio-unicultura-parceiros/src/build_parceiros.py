#!/usr/bin/env python3
"""Gera o JSON da página "Parceiros" (Colégio Unicultura, URL sugerida /parceiros), sem o rodapé.

Mesma identidade e estrutura da página Diferenciais (cabeçalho da Home, cartão azul no hero,
capítulos numerados com índice lateral, CTA final). As imagens são ilustrações SVG próprias,
animadas (pasta ilustracoes/), embutidas em widgets HTML. Os logos dos parceiros ficam em
widgets Imagem (Poliedro já com o logo da biblioteca; os outros com o placeholder do Elementor).
Saída: ../parceiros-elementor.json

Uso:  python3 build_parceiros.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-diferenciais", "src"))
sys.argv = sys.argv[:1]

import build_diferenciais as bd  # noqa: E402
from build_diferenciais import (  # noqa: E402
    CARD_BG, HANKEN, INK, NAVY, ORANGE, PAGE_BG, RED, SOFT, WHITE,
    add, anim, base, button, col, container, dims, eyebrow, gap, h2, heading, html, icon_list, link, para, pills,
    px, row, typo, widget,
)

f1 = bd.f1
OUT = os.path.join(HERE, "..", "parceiros-elementor.json")
ILLU = os.path.join(HERE, "ilustracoes")
CSS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.css"), os.path.join(f1.HERE, "un-fund1.css"),
             os.path.join(bd.HERE, "un-dif.css"), os.path.join(HERE, "un-par.css")]
JS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.js"), os.path.join(f1.HERE, "un-fund1.js"),
            os.path.join(bd.HERE, "un-dif.js")]

base._counter[0] = 25000  # faixa própria de IDs

# capítulos (âncora, rótulo do índice lateral) - o chapter() do build_diferenciais lê esta lista
bd.CHAPTERS = [
    ("poliedro", "Poliedro"),
    ("lidere", "Lidere"),
    ("sim-inova", "Sim Inova"),
    ("simple-education", "Simple Education"),
]


def svg(name):
    return open(os.path.join(ILLU, name), encoding="utf-8").read().strip()


def logo_slot(alt, image=None):
    """Espaço do logo do parceiro (widget Imagem). Sem imagem: placeholder do Elementor."""
    img = image or {"id": "", "url": bd.PLACEHOLDER, "alt": alt, "source": "library", "size": ""}
    return widget("image", {
        "image": img,
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(56),
        "object-fit": "contain",
        "_element_width": "initial",
        "_element_custom_width": px(170),
        "_element_custom_width_mobile": px(130),
        "_css_classes": "un-logo",
    })


# ---------------------------------------------------------------------------
# Topo: cabeçalho da Home + cartão azul com a rede de parceiros
# ---------------------------------------------------------------------------

def build_top():
    pill = heading('<span class="un-dot"></span>Parceiros educacionais', "p", WHITE,
                   typo("typography", HANKEN, 13, 700, lh=16, ls=0.7, transform="uppercase", size_m=11, lh_m=14),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.06)", "_border_border": "solid",
                          "_border_width": dims(1), "_border_color": "rgba(255, 255, 255, 0.28)",
                          "_border_radius": dims(999), "_padding": dims(10, 18, 10, 16),
                          "_padding_mobile": dims(8, 14, 8, 12)})
    title = heading(f'Parceiros que <span style="color:{ORANGE}">fortalecem nossa proposta</span>', "h1", WHITE,
                    typo("typography", HANKEN, 66, 700, lh=66, ls=-2.8, size_t=54, size_m=38, lh_t=56, lh_m=40,
                         ls_m=-1.5),
                    extra={"_element_width": "initial", "_element_custom_width": px(620),
                           "_element_custom_width_tablet": px(100, "%")})
    intro = para("Contamos com parceiros educacionais especializados para entregar, em cada etapa, uma formação "
                 "estruturada, atualizada e conectada às demandas do presente e do futuro.",
                 "rgba(255, 255, 255, 0.85)", size=19, width=560)
    primary = button("Agende uma visita", WHITE, INK, typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                     dims(14, 14, 14, 28), radius="999", icon=18, css_classes="un-btn-arrow",
                     shadow={"horizontal": 0, "vertical": 8, "blur": 24, "spread": 0,
                             "color": "rgba(241, 5, 5, 0.25)"},
                     extra={"link": link("/matriculas")})
    secondary = button("Fale com a gente", "rgba(255, 255, 255, 0)", WHITE,
                       typo("typography", HANKEN, 18, 600, lh=24, size_m=16),
                       dims(14, 8, 14, 8), radius="999", css_classes="un-btn-link",
                       extra={"link": link("#contato"),
                              "selected_icon": {"value": "far fa-comment-dots", "library": "fa-regular"},
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
        "width": px(54, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(26),
        "flex_gap_mobile": gap(18),
        "css_classes": "un-hero-content",
    }, [add(pill, anim("fadeInUp")), add(title, anim("fadeInUp", 120)), add(intro, anim("fadeInUp", 240)),
        add(actions, anim("fadeInUp", 360))])
    network = container({
        "content_width": "full",
        "width": px(46, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
    }, [add(html(svg("rede-parceiros.svg"), "un-net-wrap"), anim("zoomIn", 300))])
    top_row = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(32),
    }, [content, network])

    nav_label = heading("Nossos parceiros:", "p", "rgba(255, 255, 255, 0.6)",
                        typo("typography", HANKEN, 14, 700, lh=20, ls=1, transform="uppercase"),
                        extra={"_flex_size": "none"})
    nav = icon_list([{"text": label, "url": f"#{anchor}", "icon": {"value": "fas fa-circle", "library": "fa-solid"}}
                     for anchor, label in bd.CHAPTERS],
                    typo("icon_typography", HANKEN, 15, 600, lh=22, size_m=14), WHITE, icon_color=RED,
                    inline=True, space=18, icon_size=6, text_indent=10,
                    extra={"_css_classes": "un-hero-nav", "text_color_hover": ORANGE})
    strip = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_align_items": "center",
        "flex_align_items_mobile": "flex-start",
        "flex_gap": gap(20),
        "flex_gap_mobile": gap(10),
        "padding": dims(28, 0, 30, 0),
        "margin": dims(40, 0, 0, 0),
        "margin_mobile": dims(28, 0, 0, 0),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.16)",
    }, [nav_label, nav])
    card = container({
        "content_width": "full",
        "width": px(100, "%"),
        "min_height": px(700),
        "min_height_tablet": px(0),
        "flex_direction": "column",
        "flex_justify_content": "space-between",
        "padding": dims(64, 72, 0, 88),
        "padding_tablet": dims(56, 44, 0, 44),
        "padding_mobile": dims(36, 22, 0, 22),
        "overflow": "hidden",
        "border_radius": dims(40),
        "border_radius_mobile": dims(28),
        "background_background": "classic",
        "background_color": CARD_BG,
        "css_classes": "un-hero un-hero--dif",
    }, [top_row, add(strip, anim("fadeIn", 500))])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1480),
        "flex_direction": "column",
        "padding": dims(0, 24, 0, 24),
        "padding_tablet": dims(0, 16, 0, 16),
        "padding_mobile": dims(0, 12, 0, 12),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-top",
    }, [f1.home_hero.header(), card, f1.html_widget(CSS_FILES, JS_FILES)], inner=False)


# ---------------------------------------------------------------------------
# Capítulos dos parceiros: ilustração animada + logo flutuante + texto
# ---------------------------------------------------------------------------

def partner(index, name, stage, copy, chips, illustration, logo, bg, dark=False, reverse=False):
    badge = container({
        "content_width": "full",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "flex_direction": "column",
        "flex_align_items": "center",
        "padding": dims(16, 22, 16, 22),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(20),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 18, "blur": 40, "spread": 0,
                                  "color": "rgba(1, 6, 88, 0.18)"},
        "css_classes": "un-float-badge un-logo-badge",
    }, [logo])
    media_col = col([add(html(svg(illustration), "un-illu"), anim("zoomIn")), badge], 48,
                    classes="un-media un-io")
    text_kids = [add(eyebrow(f"Parceiro {index:02d}", ORANGE if dark else RED), anim("fadeInUp")),
                 add(h2(name, WHITE if dark else NAVY), anim("fadeIn", 100), classes="un-reveal")]
    if stage:
        text_kids.append(add(heading(stage, "p", WHITE if dark else NAVY,
                                     typo("typography", HANKEN, 14, 700, lh=18, ls=0.4),
                                     extra={"_css_classes": "un-stage" + (" un-stage--dark" if dark else ""),
                                            "_element_width": "auto"}), anim("fadeInUp", 150)))
    text_kids += [add(para(copy, "rgba(255, 255, 255, 0.82)" if dark else INK, size=19), anim("fadeInUp", 200)),
                  add(pills(chips, dark=dark), anim("fadeInUp", 300))]
    text_col = col(text_kids, 52, gap_px=20)
    return bd.chapter(index, bg, [row([media_col, text_col], reverse=reverse)], dark=dark,
                      extra_classes="un-grid-bg" if dark else "")


def build_partners():
    poliedro_logo = f1.find(f1.page["content"], "29d6236e")["settings"]["image"]  # logo já na biblioteca
    return [
        partner(1, "Sistema de Ensino Poliedro", "3º ano do Fundamental → 3ª série do Médio",
                "Parceiro central da nossa proposta acadêmica, integrando material didático, tecnologia, "
                "avaliações e recursos de acompanhamento da aprendizagem — do 3º ano do Ensino Fundamental à "
                "3ª série do Ensino Médio.",
                ["Material didático", "Tecnologia", "Avaliações", "Acompanhamento da aprendizagem"],
                "poliedro.svg", logo_slot("Logo Sistema de Ensino Poliedro", dict(poliedro_logo)), PAGE_BG),
        partner(2, "Programa Lidere", "Toda a trajetória no Unicultura",
                "Educação Socioemocional, Financeira e Empreendedora integrada à formação dos estudantes, ao longo "
                "de toda a trajetória no Colégio Unicultura.",
                ["Socioemocional", "Financeira", "Empreendedora"],
                "lidere.svg", logo_slot("Logo Programa Lidere"), SOFT, reverse=True),
        partner(3, "Sim Inova", "Tecnologia · Maker · STEAM",
                "Pensamento Computacional e Robótica Educacional, tecnologia, Cultura Maker e metodologia STEAM — "
                "desenvolvendo raciocínio lógico e capacidade de resolver problemas.",
                ["Pensamento computacional", "Robótica educacional", "Cultura Maker", "STEAM"],
                "sim-inova.svg", logo_slot("Logo Sim Inova"), NAVY, dark=True),
        partner(4, "Simple Education", "Ensino Fundamental — Anos Iniciais",
                "Sistema Bilíngue para o Ensino Fundamental — Anos Iniciais, com aprendizagem da língua inglesa de "
                "maneira contínua e contextualizada.",
                ["Sistema Bilíngue", "Língua inglesa", "Contínua e contextualizada"],
                "simple-education.svg", logo_slot("Logo Simple Education"), PAGE_BG, reverse=True),
    ]


def main():
    cta = bd.build_cta(
        f'Quer conhecer de perto <span style="color:{ORANGE}">como cada parceria funciona na prática?</span>',
        "Agende uma visita e converse com nossa equipe pedagógica.")
    data = {
        "content": [build_top()] + build_partners() + [cta],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Parceiros",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
