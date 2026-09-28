#!/usr/bin/env python3
"""Gera o JSON da página "Diferenciais" (Colégio Unicultura) - página inteira, sem o rodapé.

Identidade das páginas Unicultura (azul-escuro #010658 + vermelho #F10505, Hanken Grotesk), mesmo
cabeçalho da Home. Cada diferencial é um "capítulo" (01 a 08) com número grande ao fundo, e um
índice lateral fixo mostra em qual capítulo o visitante está (un-dif.js).
As fotos ficam como placeholder do Elementor (o texto alternativo diz qual foto usar).
Saída: ../diferenciais-elementor.json

Uso:  python3 build_diferenciais.py
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-fundamental1", "src"))
sys.argv = sys.argv[:1]

import build_fund1 as f1  # noqa: E402
from build_fund1 import (  # noqa: E402
    CARD_BG, HANKEN, INK, NAVY, ORANGE, PAGE_BG, RED, WHITE,
    add, anim, base, button, container, dims, gap, heading, icon_list, parallax, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "diferenciais-elementor.json")
CSS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.css"), os.path.join(f1.HERE, "un-fund1.css"),
             os.path.join(HERE, "un-dif.css")]
JS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.js"), os.path.join(f1.HERE, "un-fund1.js"),
            os.path.join(HERE, "un-dif.js")]

base._counter[0] = 23000  # faixa própria de IDs

SOFT = "#F5F6FF"
PLACEHOLDER = "https://colegiounicultura.com.br/wp-content/plugins/elementor/assets/images/placeholder.png"

CHAPTERS = [  # (âncora, rótulo do índice)
    ("olimpiadas", "Olimpíadas"),
    ("monitoria", "Monitoria"),
    ("leitura", "Clube de Leitura"),
    ("computacional", "Pens. Computacional"),
    ("socioemocional", "Socioemocional"),
    ("bilingue", "Bilíngue"),
    ("projetos", "Projetos"),
    ("esportes", "Esportes"),
]


def link(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def placeholder(alt, height, height_t=None, height_m=None, radius=28, classes=""):
    """Imagem com o placeholder do Elementor. O "alt" descreve a foto que deve entrar."""
    s = {
        "image": {"id": "", "url": PLACEHOLDER, "alt": alt, "source": "library", "size": ""},
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(height),
        "object-fit": "cover",
        "object-position": "center center",
        "image_border_radius": dims(radius),
        "image_border_radius_mobile": dims(min(radius, 22)),
        "_css_classes": ("un-ph " + classes).strip(),
    }
    if height_t:
        s["height_tablet"] = px(height_t)
    if height_m:
        s["height_mobile"] = px(height_m)
    return widget("image", s)


def html(markup, classes=""):
    s = {"html": markup}
    if classes:
        s["_css_classes"] = classes
    return widget("html", s)


def eyebrow(label, color=RED, align="left"):
    return heading(label, "p", color, typo("typography", HANKEN, 13, 700, lh=16, ls=1.4, transform="uppercase"),
                   align=align)


def h2(title, color=NAVY, size=52, align="left", width=None):
    extra = {}
    if width:
        extra = {"_element_width": "initial", "_element_custom_width": px(width),
                 "_element_custom_width_tablet": px(100, "%")}
    return heading(title, "h2", color,
                   typo("typography", HANKEN, size, 700, lh=size + 4, ls=-size / 26, size_t=min(size, 44), size_m=32,
                        lh_t=min(size, 44) + 4, lh_m=36, ls_m=-1.1),
                   align=align, extra=extra)


def para(copy, color=INK, size=18, align="left", width=None):
    extra = {}
    if width:
        extra = {"_element_width": "initial", "_element_custom_width": px(width),
                 "_element_custom_width_tablet": px(100, "%")}
    return text(f"<p>{copy}</p>", color, typo("typography", HANKEN, size, 400, lh=round(size * 1.6), size_m=16, lh_m=25),
                align=align, extra=extra)


def checks(items, color=INK, icon_color=RED, inline=False):
    return icon_list([{"text": t, "icon": {"value": "fas fa-check", "library": "fa-solid"}} for t in items],
                     typo("icon_typography", HANKEN, 17, 600, lh=24, size_m=15), color, icon_color=icon_color,
                     inline=inline, space=12, icon_size=12, text_indent=12,
                     extra={"_css_classes": "un-checks" + (" un-checks--inline" if inline else "")})


def pills(items, dark=False):
    """Palavras-chave em pílulas (a cor vem do un-dif.css)."""
    return icon_list([{"text": t} for t in items], typo("icon_typography", HANKEN, 15, 600, lh=20, size_m=14),
                     WHITE if dark else NAVY, inline=True, space=8, icon_size=1, text_indent=0,
                     extra={"_css_classes": "un-pills" + (" un-pills--dark" if dark else "")})


def big_number(n, dark=False):
    """Número gigante vazado atrás do capítulo, com parallax."""
    num = heading(f"{n:02d}", "p", "rgba(0, 0, 0, 0)",
                  typo("typography", HANKEN, 260, 800, lh=220, ls=-12, size_t=200, size_m=140, lh_t=170, lh_m=120,
                       ls_m=-6),
                  extra={"_css_classes": "un-bignum" + (" un-bignum--dark" if dark else "")})
    return add(num, parallax(2))


def icon_card(icon, title, body_html, dark=False, delay=0, classes=""):
    badge = widget("icon", {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "stacked",
        "shape": "circle",
        "primary_color": "rgba(255, 255, 255, 0.1)" if dark else "#EDEEFA",
        "secondary_color": ORANGE if dark else NAVY,
        "size": px(22),
        "icon_padding": px(18),
        "align": "left",
        "_css_classes": "un-card-icon",
    })
    kids = [badge, heading(title, "h3", WHITE if dark else NAVY,
                           typo("typography", HANKEN, 22, 700, lh=28, ls=-0.5, size_m=19, lh_m=25))]
    if body_html:
        kids.append(text(body_html, "rgba(255, 255, 255, 0.75)" if dark else INK,
                         typo("typography", HANKEN, 16, 400, lh=25, size_m=15, lh_m=23)))
    card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(14),
        "padding": dims(30, 28, 30, 28),
        "padding_mobile": dims(24, 22, 24, 22),
        "background_background": "classic",
        "background_color": "rgba(255, 255, 255, 0.05)" if dark else WHITE,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(255, 255, 255, 0.12)" if dark else "rgba(1, 6, 88, 0.08)",
        "border_radius": dims(24),
        "css_classes": ("un-card " + classes).strip(),
    }, kids)
    return add(card, anim("fadeInUp", delay))


def row(children, gap_px=72, reverse=False, align="center"):
    return container({
        "content_width": "full",
        "flex_direction": "row-reverse" if reverse else "row",
        "flex_direction_tablet": "column",
        "flex_align_items": align,
        "flex_align_items_tablet": "stretch",
        "flex_gap": gap(gap_px),
        "flex_gap_tablet": gap(44),
        "flex_gap_mobile": gap(36),
    }, children)


def col(children, width, gap_px=22, classes=""):
    s = {
        "content_width": "full",
        "width": px(width, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(gap_px),
        "flex_gap_mobile": gap(16),
    }
    if classes:
        s["css_classes"] = classes
    return container(s, children)


def chapter(index, bg, children, dark=False, extra_classes=""):
    anchor, label = CHAPTERS[index - 1]
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "_element_id": anchor,
        "_attributes": f"data-chapter|{label}",
        "flex_direction": "column",
        "flex_gap": gap(56),
        "flex_gap_mobile": gap(36),
        "padding": dims(130, 24, 130, 24),
        "padding_tablet": dims(100, 24, 100, 24),
        "padding_mobile": dims(72, 16, 72, 16),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": bg,
        "css_classes": ("gt-root un-chapter " + ("un-chapter--dark " if dark else "") + extra_classes).strip(),
    }, [big_number(index, dark)] + children, inner=False)


# ---------------------------------------------------------------------------
# Ícones (SVG de linha, 24x24) usados na órbita do hero
# ---------------------------------------------------------------------------

ICONS = {
    "olimpiadas": '<circle cx="12" cy="15" r="6"/><path d="M8.5 10 6 3h4l2 5 2-5h4l-2.5 7"/>',
    "monitoria": '<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "leitura": '<path d="M3 5c3-1 6-1 9 1v13c-3-2-6-2-9-1zM21 5c-3-1-6-1-9 1v13c3-2 6-2 9-1z"/>',
    "computacional": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>',
    "socioemocional": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "bilingue": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "projetos": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    "esportes": '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6c3.2 3.2 3.2 9.6 0 12.8M18.4 5.6c-3.2 3.2-3.2 9.6 0 12.8M3 12h18"/>',
}


def svg_icon(key):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[key]}</svg>')


def orbit_html():
    items = []
    for i, (anchor, label) in enumerate(CHAPTERS):
        ring = 1 if i % 2 == 0 else 2
        angle = (i // 2) * 90 + (0 if ring == 1 else 45)
        items.append((ring, f'<a class="un-orbit-item" href="#{anchor}" style="--a:{angle}deg" aria-label="{label}">'
                            f'<span class="un-orbit-bubble">{svg_icon(anchor)}'
                            f'<span class="un-orbit-label">{label}</span></span></a>'))
    rings = "".join(f'<div class="un-orbit-ring un-orbit-ring--{r}">'
                    + "".join(markup for rr, markup in items if rr == r) + "</div>" for r in (1, 2))
    return ('<div class="un-orbit">'
            '<div class="un-orbit-core"><strong>8</strong><span>diferenciais</span></div>'
            f'{rings}</div>')


# ---------------------------------------------------------------------------
# Topo: cabeçalho da Home + cartão azul com a órbita dos 8 diferenciais
# ---------------------------------------------------------------------------

def build_top():
    pill = heading('<span class="un-dot"></span>Diferenciais Unicultura', "p", WHITE,
                   typo("typography", HANKEN, 13, 700, lh=16, ls=0.7, transform="uppercase", size_m=11, lh_m=14),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.06)", "_border_border": "solid",
                          "_border_width": dims(1), "_border_color": "rgba(255, 255, 255, 0.28)",
                          "_border_radius": dims(999), "_padding": dims(10, 18, 10, 16),
                          "_padding_mobile": dims(8, 14, 8, 12)})
    title = heading(f'Aprendizagem que <span style="color:{ORANGE}">ultrapassa a sala de aula</span>', "h1", WHITE,
                    typo("typography", HANKEN, 66, 700, lh=66, ls=-2.8, size_t=54, size_m=38, lh_t=56, lh_m=40,
                         ls_m=-1.5),
                    extra={"_element_width": "initial", "_element_custom_width": px(620),
                           "_element_custom_width_tablet": px(100, "%")})
    intro = para("Nossa formação acadêmica é complementada por experiências que ampliam repertórios, desenvolvem "
                 "talentos e proporcionam novos desafios aos estudantes — do 3º ano do Ensino Fundamental ao "
                 "Ensino Médio.", "rgba(255, 255, 255, 0.85)", size=19, width=560)
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
        "width": px(56, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(26),
        "flex_gap_mobile": gap(18),
        "css_classes": "un-hero-content",
    }, [add(pill, anim("fadeInUp")), add(title, anim("fadeInUp", 120)), add(intro, anim("fadeInUp", 240)),
        add(actions, anim("fadeInUp", 360))])
    orbit = container({
        "content_width": "full",
        "width": px(44, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
    }, [add(html(orbit_html(), "un-orbit-wrap"), anim("zoomIn", 300))])
    top_row = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(40),
    }, [content, orbit])

    nav_label = heading("Navegue:", "p", "rgba(255, 255, 255, 0.6)",
                        typo("typography", HANKEN, 14, 700, lh=20, ls=1, transform="uppercase"),
                        extra={"_flex_size": "none"})
    nav = icon_list([{"text": label, "url": f"#{anchor}", "icon": {"value": "fas fa-circle", "library": "fa-solid"}}
                     for anchor, label in CHAPTERS],
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
        "margin": dims(48, 0, 0, 0),
        "margin_mobile": dims(32, 0, 0, 0),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "rgba(255, 255, 255, 0.16)",
    }, [nav_label, nav])

    card = container({
        "content_width": "full",
        "width": px(100, "%"),
        "min_height": px(720),
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
# 01 Olimpíadas Científicas: medalha balançando + frase-manifesto
# ---------------------------------------------------------------------------

MEDAL_SVG = (
    '<svg class="un-medal" viewBox="0 0 200 270" aria-hidden="true">'
    '<path d="M58 0h38l26 96H86z" fill="#F10505"/>'
    '<path d="M142 0h-38L78 96h36z" fill="#FFFFFF" opacity=".92"/>'
    '<circle cx="100" cy="178" r="74" fill="#FFB867"/>'
    '<circle cx="100" cy="178" r="56" fill="none" stroke="#010658" stroke-opacity=".22" stroke-width="4"/>'
    '<path d="m100 138 11.5 23.5 26 3.6-18.8 18.2 4.5 25.7L100 196.9l-23.2 12.1 4.5-25.7-18.8-18.2 26-3.6z" '
    'fill="#010658"/>'
    '<circle class="un-medal-shine" cx="72" cy="150" r="10" fill="#FFFFFF" opacity=".5"/>'
    '</svg>'
)


def build_olimpiadas():
    left = col([
        add(eyebrow("Olimpíadas Científicas"), anim("fadeInUp")),
        add(h2('Desafiar também é uma forma de <span class="un-mark">ensinar.</span>', width=560),
            anim("fadeIn", 100), classes="un-reveal un-io"),
        add(para("Incentivamos a participação em Olimpíadas Científicas de diferentes áreas do conhecimento. "
                 "A preparação e a participação desenvolvem:"), anim("fadeInUp", 200)),
        add(pills(["Raciocínio lógico", "Pensamento científico", "Investigação", "Persistência", "Autonomia",
                   "Resolução de problemas"]), anim("fadeInUp", 300)),
    ], 54)
    medal_card = container({
        "content_width": "full",
        "width": px(46, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(28),
        "padding": dims(56, 48, 52, 48),
        "padding_mobile": dims(40, 26, 36, 26),
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(36),
        "border_radius_mobile": dims(28),
        "css_classes": "un-medal-card",
    }, [html(MEDAL_SVG, "un-medal-wrap"),
        heading("Mais do que medalhas, buscamos despertar talentos e desenvolver potencialidades.", "p", WHITE,
                typo("typography", HANKEN, 26, 600, lh=34, ls=-0.6, size_m=21, lh_m=28), align="center",
                extra={"_css_classes": "un-medal-quote"})])
    return chapter(1, PAGE_BG, [row([left, add(medal_card, anim("zoomIn", 150))])])


# ---------------------------------------------------------------------------
# 02 Plantão de Monitoria
# ---------------------------------------------------------------------------

def build_monitoria():
    media_col = col([
        add(placeholder("Foto: estudantes com monitor tirando dúvidas", 540, 460, 360, classes="un-clip"),
            anim("fadeIn")),
        container({
            "content_width": "full",
            "width": {"unit": "custom", "size": "max-content", "sizes": []},
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_gap": gap(12),
            "padding": dims(16, 22, 16, 18),
            "background_background": "classic",
            "background_color": WHITE,
            "border_radius": dims(18),
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {"horizontal": 0, "vertical": 18, "blur": 40, "spread": 0,
                                      "color": "rgba(1, 6, 88, 0.16)"},
            "css_classes": "un-float-badge",
        }, [widget("icon", {"selected_icon": {"value": "fas fa-user-graduate", "library": "fa-solid"},
                            "view": "stacked", "shape": "circle", "primary_color": RED,
                            "secondary_color": WHITE, "size": px(16), "icon_padding": px(12)}),
            heading("Anos Finais e<br>Ensino Médio", "p", NAVY,
                    typo("typography", HANKEN, 16, 700, lh=20))]),
    ], 48, classes="un-media un-io")
    text_col = col([
        add(eyebrow("Anos Finais e Ensino Médio"), anim("fadeInUp")),
        add(h2("Plantão de Monitoria"), anim("fadeIn", 100), classes="un-reveal"),
        add(para("Espaço destinado à revisão de conteúdos, esclarecimento de dúvidas e fortalecimento das "
                 "aprendizagens — um apoio próximo para quem precisa reforçar algum conteúdo ou simplesmente "
                 "aprofundar o que já aprendeu."), anim("fadeInUp", 200)),
        add(checks(["Revisão de conteúdos", "Esclarecimento de dúvidas", "Fortalecimento das aprendizagens"]),
            anim("fadeInUp", 300)),
    ], 52)
    return chapter(2, SOFT, [row([media_col, text_col])])


# ---------------------------------------------------------------------------
# 03 Clube de Leitura: as 5 palavras "se preenchem" ao passar pela tela
# ---------------------------------------------------------------------------

def build_leitura():
    words = ["Repertório", "Interpretação", "Argumentação", "Imaginação", "Pensamento crítico"]
    word_widgets = [heading(w, "p", NAVY,
                            typo("typography", HANKEN, 64, 800, lh=70, ls=-2.4, size_t=52, size_m=36, lh_t=58,
                                 lh_m=42, ls_m=-1.2),
                            extra={"_css_classes": "un-fill-word un-io"}) for w in words]
    left = col([
        add(eyebrow("Leitura e repertório"), anim("fadeInUp")),
        add(h2("Clube de Leitura"), anim("fadeIn", 100), classes="un-reveal"),
        add(para("Um espaço de encontro com a literatura para ampliar repertório, interpretação, argumentação, "
                 "imaginação e pensamento crítico."), anim("fadeInUp", 200)),
        add(placeholder("Foto: roda de leitura com estudantes", 360, 340, 260), anim("fadeInUp", 300),
            parallax(-1)),
    ], 44)
    right = col(word_widgets, 56, gap_px=4, classes="un-words-list")
    return chapter(3, PAGE_BG, [row([left, right], align="flex-start")])


# ---------------------------------------------------------------------------
# 04 Pensamento Computacional (azul, com grade de pontos e "terminal")
# ---------------------------------------------------------------------------

TERMINAL = ('<p class="un-term"><span class="un-term-prompt">&gt;</span> '
            '<span class="un-term-text">criar, testar, resolver</span><span class="un-term-caret"></span></p>')


def build_computacional():
    head = col([
        html(TERMINAL, "un-term-wrap"),
        add(h2("Pensamento Computacional", WHITE, width=640), anim("fadeIn", 100), classes="un-reveal"),
        add(para("Tecnologia, Cultura Maker e metodologia STEAM utilizadas para desenvolver pensamento "
                 "computacional, criatividade e resolução de problemas.", "rgba(255, 255, 255, 0.8)", width=620),
            anim("fadeInUp", 200)),
    ], 100)
    cards = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_gap": gap(20),
    }, [icon_card("fas fa-microchip", "Tecnologia", "", dark=True, delay=0, classes="un-tilt"),
        icon_card("fas fa-tools", "Cultura Maker", "", dark=True, delay=120, classes="un-tilt"),
        icon_card("fas fa-flask", "Metodologia STEAM", "", dark=True, delay=240, classes="un-tilt")])
    for c in cards["elements"]:
        c["settings"]["_flex_size"] = "grow"
    outcomes = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_align_items": "center",
        "flex_align_items_mobile": "flex-start",
        "flex_gap": gap(16),
    }, [heading("Para desenvolver", "p", ORANGE,
                typo("typography", HANKEN, 13, 700, lh=16, ls=1.4, transform="uppercase"),
                extra={"_flex_size": "none"}),
        pills(["Pensamento computacional", "Criatividade", "Resolução de problemas"], dark=True)])
    return chapter(4, NAVY, [head, cards, add(outcomes, anim("fadeInUp", 200))], dark=True,
                   extra_classes="un-grid-bg")


# ---------------------------------------------------------------------------
# 05 Educação Socioemocional, Financeira e Empreendedora
# ---------------------------------------------------------------------------

def build_socioemocional():
    head = row([
        col([add(eyebrow("Formação integral"), anim("fadeInUp")),
             add(h2("Educação Socioemocional, Financeira e Empreendedora", size=48), anim("fadeIn", 100),
                 classes="un-reveal")], 55),
        col([add(para("Formação que prepara nossos estudantes para lidar com emoções, relações, escolhas, "
                      "planejamento, recursos, desafios e projetos."), anim("fadeInUp", 200))], 45),
    ], align="flex-end")
    cards = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_gap": gap(20),
    }, [icon_card("fas fa-heart", "Socioemocional", "<p>Emoções · Relações · Escolhas</p>", delay=0),
        icon_card("fas fa-piggy-bank", "Financeira", "<p>Planejamento · Recursos</p>", delay=120),
        icon_card("fas fa-rocket", "Empreendedora", "<p>Desafios · Projetos</p>", delay=240)])
    for c in cards["elements"]:
        c["settings"]["_flex_size"] = "grow"
    banner = heading('Habilidades tão importantes <span class="un-mark">quanto o conteúdo acadêmico.</span>', "p",
                     NAVY, typo("typography", HANKEN, 34, 700, lh=42, ls=-1, size_m=24, lh_m=31), align="center",
                     extra={"_css_classes": "un-io un-banner"})
    return chapter(5, SOFT, [head, cards, add(banner, anim("fadeInUp"))])


# ---------------------------------------------------------------------------
# 06 Sistema Bilíngue: balões "Hello!" / "Olá!" sobre a foto
# ---------------------------------------------------------------------------

BUBBLES = ('<div class="un-bubbles" aria-hidden="true">'
           '<span class="un-bubble un-bubble--en">Hello!</span>'
           '<span class="un-bubble un-bubble--pt">Olá!</span></div>')


def build_bilingue():
    media_col = col([add(placeholder("Foto: aula de inglês no Fundamental", 520, 440, 340), anim("fadeIn")),
                     html(BUBBLES, "un-bubbles-wrap")], 48, classes="un-media")
    text_col = col([
        add(eyebrow("Ensino Fundamental — Anos Iniciais"), anim("fadeInUp")),
        add(h2('Sistema <span class="un-mark">Bilíngue</span>'), anim("fadeIn", 100), classes="un-reveal un-io"),
        add(para("Aprendizagem da língua inglesa de maneira contínua e contextualizada, ampliando as habilidades de "
                 "comunicação e o repertório cultural desde os primeiros anos do Fundamental."),
            anim("fadeInUp", 200)),
        add(checks(["Contínua e contextualizada", "Habilidades de comunicação", "Repertório cultural"]),
            anim("fadeInUp", 300)),
    ], 52)
    return chapter(6, PAGE_BG, [row([media_col, text_col], reverse=True)])


# ---------------------------------------------------------------------------
# 07 Projetos Pedagógicos: 3 etapas ligadas por uma linha que se desenha
# ---------------------------------------------------------------------------

def step(n, title):
    # sem Entrance Animation do Elementor: quem acende cada etapa é o scroll (un-dif.js)
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(12),
        "padding": dims(0, 12, 0, 0),
        "_flex_size": "grow",
        "css_classes": "un-step",
    }, [heading(f"{n:02d}", "p", WHITE, typo("typography", HANKEN, 18, 800, lh=18),
                extra={"_css_classes": "un-step-dot"}),
        heading(title, "h3", WHITE, typo("typography", HANKEN, 28, 700, lh=32, ls=-0.8, size_m=22, lh_m=27))])


# Linha das etapas: um elemento próprio (o ::before dos containers é a camada de sobreposição do Elementor,
# que força largura/altura de 100% e bordas). --un-p (0 a 1) vem do un-dif.js conforme o scroll.
def steps_line_html():
    # o CSS/JS da linha vão no próprio widget: a seção funciona mesmo sem o CSS do topo atualizado
    css = open(os.path.join(HERE, "un-projetos.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "un-projetos.js"), encoding="utf-8").read().strip()
    return ('<div class="un-steps-fill"></div>\n<style>\n' + css + '\n</style>\n<script>\n' + js
            + '\n</script>')


def build_projetos():
    head = row([
        col([add(eyebrow("Interdisciplinaridade", ORANGE), anim("fadeInUp")),
             add(h2("Projetos Pedagógicos", WHITE), anim("fadeIn", 100), classes="un-reveal")], 50),
        col([add(para("Experiências interdisciplinares que transformam conteúdos em investigação, produção e "
                      "conhecimento aplicado — conectando diferentes áreas do saber em torno de um mesmo desafio.",
                      "rgba(255, 255, 255, 0.8)"), anim("fadeInUp", 200))], 50),
    ], align="flex-end")
    steps = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(28),
        "padding": dims(8, 0, 0, 0),
        "css_classes": "un-steps",
    }, [html(steps_line_html(), "un-steps-line"),
        step(1, "Investigação"), step(2, "Produção"), step(3, "Conhecimento aplicado")])
    challenge = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_align_items": "center",
        "flex_align_items_mobile": "flex-start",
        "flex_justify_content": "space-between",
        "flex_gap": gap(24),
        "padding": dims(28, 32, 28, 32),
        "background_background": "classic",
        "background_color": "rgba(255, 255, 255, 0.05)",
        "border_border": "dashed",
        "border_width": dims(1),
        "border_color": "rgba(255, 184, 103, 0.5)",
        "border_radius": dims(24),
    }, [heading("Diferentes áreas do saber, <span style=\"color:#FFB867\">um mesmo desafio.</span>", "p", WHITE,
                typo("typography", HANKEN, 24, 700, lh=30, ls=-0.5, size_m=20, lh_m=26)),
        pills(["Linguagens", "Matemática", "Ciências", "Humanas", "Artes"], dark=True)])
    return chapter(7, NAVY, [head, steps, add(challenge, anim("fadeInUp", 200))], dark=True)


# ---------------------------------------------------------------------------
# 08 Escola de Esportes: bento com foto + 4 valores
# ---------------------------------------------------------------------------

def value_tile(icon, label, delay):
    return add(container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(12),
        "padding": dims(22),
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.08)",
        "border_radius": dims(20),
        "css_classes": "un-card un-value",
    }, [widget("icon", {"selected_icon": {"value": icon, "library": "fa-solid"}, "view": "stacked",
                        "shape": "circle", "primary_color": "#EDEEFA", "secondary_color": RED, "size": px(18),
                        "icon_padding": px(14), "align": "left", "_css_classes": "un-card-icon"}),
        heading(label, "h3", NAVY, typo("typography", HANKEN, 19, 700, lh=24, size_m=17, lh_m=22))]),
        anim("fadeInUp", delay))


def build_esportes():
    photo = add(placeholder("Foto: estudantes na Escola de Esportes", 620, 480, 360, radius=32, classes="un-clip"),
                anim("fadeIn"))
    values = container({
        "content_width": "full",
        "container_type": "grid",
        "grid_columns_grid": {"unit": "fr", "size": 2, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 2, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 2, "sizes": []},
        "grid_gaps": {"column": "14", "row": "14", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "10", "row": "10", "isLinked": True, "unit": "px"},
    }, [value_tile("fas fa-bullseye", "Disciplina", 0), value_tile("fas fa-hands-helping", "Cooperação", 100),
        value_tile("fas fa-mountain", "Perseverança", 200), value_tile("fas fa-handshake", "Respeito", 300)])
    text_col = col([
        add(eyebrow("Corpo e mente"), anim("fadeInUp")),
        add(h2("Escola de Esportes"), anim("fadeIn", 100), classes="un-reveal"),
        add(para("Práticas que contribuem para o desenvolvimento físico, emocional e social, trabalhando "
                 "disciplina, cooperação, perseverança e respeito."), anim("fadeInUp", 200)),
        add(pills(["Físico", "Emocional", "Social"]), anim("fadeInUp", 250)),
        values,
    ], 50)
    return chapter(8, SOFT, [row([col([photo], 50, classes="un-media"), text_col])])


# ---------------------------------------------------------------------------
# CTA final
# ---------------------------------------------------------------------------

def build_cta():
    title = heading(f'Quer conhecer de perto <span style="color:{ORANGE}">essas experiências?</span>', "h2", WHITE,
                    typo("typography", HANKEN, 56, 700, lh=60, ls=-2.2, size_t=46, size_m=32, lh_t=50, lh_m=36,
                         ls_m=-1.1),
                    align="center",
                    extra={"_element_width": "initial", "_element_custom_width": px(760),
                           "_element_custom_width_tablet": px(100, "%")})
    body = para("Agende uma visita e veja como cada um desses diferenciais entra na rotina do seu filho.",
                "rgba(255, 255, 255, 0.82)", size=19, align="center", width=560)
    primary = button("Agendar visita", WHITE, INK, typo("typography", HANKEN, 18, 700, lh=24, size_m=16),
                     dims(14, 14, 14, 28), radius="999", icon=18, css_classes="un-btn-arrow",
                     extra={"link": link("/matriculas")})
    whats = button("Falar pelo WhatsApp", "rgba(255, 255, 255, 0)", WHITE,
                   typo("typography", HANKEN, 18, 600, lh=24, size_m=16), dims(15, 26, 15, 22), radius="999",
                   css_classes="un-btn-whats",
                   extra={"link": {"url": "", "is_external": "on", "nofollow": "", "custom_attributes": ""},
                          "selected_icon": {"value": "fab fa-whatsapp", "library": "fa-brands"},
                          "icon_align": "left", "icon_indent": px(10), "border_border": "solid",
                          "border_width": dims(1), "border_color": "rgba(255, 255, 255, 0.4)"})
    actions = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "flex_gap": gap(16),
        "margin": dims(10, 0, 0, 0),
    }, [primary, whats])
    card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(22),
        "padding": dims(96, 40, 96, 40),
        "padding_mobile": dims(64, 22, 64, 22),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(40),
        "border_radius_mobile": dims(28),
        "css_classes": "un-cta-card",
        "_element_id": "contato",
    }, [add(eyebrow("Venha nos visitar", ORANGE, align="center"), anim("fadeInUp")),
        add(title, anim("fadeInUp", 100)), add(body, anim("fadeInUp", 200)), add(actions, anim("fadeInUp", 300))])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1432),
        "html_tag": "section",
        "flex_direction": "column",
        "padding": dims(40, 24, 110, 24),
        "padding_tablet": dims(32, 16, 88, 16),
        "padding_mobile": dims(24, 12, 64, 12),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-dif-cta",
    }, [add(card, anim("zoomIn"))], inner=False)


def main():
    data = {
        "content": [build_top(), build_olimpiadas(), build_monitoria(), build_leitura(), build_computacional(),
                    build_socioemocional(), build_bilingue(), build_projetos(), build_esportes(), build_cta()],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Diferenciais",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")
    # JSON só da seção Projetos (para trocar a seção sem reimportar a página)
    projetos = next(sec for sec in data["content"] if sec["settings"].get("_element_id") == "projetos")
    out = os.path.join(HERE, "..", "secao-projetos-elementor.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"content": [projetos], "page_settings": [], "version": "0.4",
                   "title": "Unicultura - Diferenciais - Projetos", "type": "container"},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
