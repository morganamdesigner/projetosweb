#!/usr/bin/env python3
"""Gera o JSON da seção "Depoimentos" da Home (template de container do Elementor).

Substitui a seção atual "O que os pais dizem sobre nós?" da Home.
Saída: ../secao-depoimentos-elementor.json

ATENÇÃO: os 8 depoimentos são EXEMPLOS para substituir por depoimentos reais
(com autorização das famílias). No editor, cada card mostra a etiqueta "EXEMPLO".

Uso:  python3 build_secao_depoimentos.py
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "src"))

import build_elementor_json as base  # noqa: E402
from build_elementor_json import (  # noqa: E402
    HANKEN, add, anim, button, container, dims, gap, heading, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "secao-depoimentos-elementor.json")
CSS_FILE = os.path.join(HERE, "un-depoimentos.css")
JS_FILE = os.path.join(HERE, "un-depoimentos.js")

base._counter[0] = 9000  # faixa própria de IDs

BG = "#0D1261"          # fundo da seção atual de depoimentos da Home
RED = "#F10505"
ORANGE = "#FFB867"
INK = "#1C1F4F"
MUTED = "#5B5E88"
WHITE = "#FFFFFF"

SEGMENTS = {
    "Garatuja": ("#F2CA50", "#010658"),
    "Fundamental": ("#1B4FD9", WHITE),
    "Ensino Médio": (RED, WHITE),
}

# (segmento, depoimento, nome, relação, iniciais) - EXEMPLOS
TESTIMONIALS = [
    ("Garatuja", "A adaptação foi tão acolhedora que hoje ele pede para ir à escola até no fim de semana.",
     "Ana P.", "Mãe do Theo · Garatuja", "AP"),
    ("Fundamental", "Vemos a evolução na leitura e na autonomia dela todos os dias. A comunicação com a "
     "equipe é excelente.", "Ricardo S.", "Pai da Laura · 4º ano", "RS"),
    ("Ensino Médio", "Os professores conhecem cada aluno pelo nome e pelas dificuldades. Isso fez toda a "
     "diferença na preparação para o vestibular.", "Carla M.", "Mãe do Gabriel · 3ª série", "CM"),
    ("Garatuja", "O inglês entrou na rotina de forma natural. Ela canta músicas em inglês pela casa inteira!",
     "Juliana R.", "Mãe da Sofia · Garatuja", "JR"),
    ("Fundamental", "Encontramos uma escola que une exigência acadêmica e cuidado com o emocional. Ele "
     "está muito mais confiante.", "Marcelo T.", "Pai do Lucas · 8º ano", "MT"),
    ("Fundamental", "Os projetos em sala despertaram uma curiosidade que a gente nem conhecia nele.",
     "Patrícia A.", "Mãe do Davi · 5º ano", "PA"),
    ("Ensino Médio", "Estudo aqui desde pequena e me sinto preparada para o que vem depois. A escola é "
     "uma segunda casa.", "Beatriz L.", "Aluna · 2ª série", "BL"),
    ("Fundamental", "A parceria entre escola e família é de verdade. Somos ouvidos e sentimos que fazemos "
     "parte.", "Fernanda C.", "Mãe da Alice · 7º ano", "FC"),
]


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------

def card(segment, quote, name, relation, initials):
    seg_bg, seg_fg = SEGMENTS[segment]
    top = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_justify_content": "space-between",
        "flex_align_items": "flex-start",
    }, [
        heading("“", "div", RED, typo("typography", HANKEN, 72, 700, lh=72),
                extra={"_css_classes": "un-depo-quote", "_flex_size": "none"}),
        heading(segment, "span", seg_fg,
                typo("typography", HANKEN, 11, 700, lh=12, ls=0.8, transform="uppercase"),
                extra={"_element_width": "auto", "_background_background": "classic",
                       "_background_color": seg_bg, "_border_radius": dims(999),
                       "_padding": dims(6, 10, 6, 10), "_flex_size": "none"}),
    ])
    stars = heading("★★★★★", "div", ORANGE, typo("typography", HANKEN, 15, 400, lh=15, ls=2))
    body = text(f"<p>{quote}</p>", INK, typo("typography", HANKEN, 16, 400, lh=24))
    avatar = container({
        "content_width": "full",
        "width": px(44),
        "min_height": px(44),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_align_items": "center",
        "background_background": "classic",
        "background_color": "#F0F2FA",
        "border_radius": dims(999),
        "css_classes": "un-depo-avatar",
    }, [heading(initials, "div", "#010658", typo("typography", HANKEN, 14, 700, lh=14), align="center")])
    who = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(2),
    }, [
        heading(name, "p", INK, typo("typography", HANKEN, 15, 700, lh=20)),
        heading(relation, "p", MUTED, typo("typography", HANKEN, 13, 400, lh=18)),
    ])
    footer = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(12),
        "padding": dims(16, 0, 0, 0),
        "border_border": "solid",
        "border_width": dims(1, 0, 0, 0),
        "border_color": "#ECEDF5",
    }, [avatar, who])
    return container({
        "content_width": "full",
        "html_tag": "article",
        "flex_direction": "column",
        "flex_gap": gap(14),
        "padding": dims(24, 26, 22, 26),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(24),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 12, "blur": 30, "spread": 0,
                                  "color": "rgba(0, 0, 0, 0.25)"},
        "css_classes": "un-depo-card",
    }, [top, stars, body, footer])


def card_set(items, duplicate=False):
    s = {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(20),
        "padding": dims(0, 0, 20, 0),  # espaço igual entre o fim de um conjunto e o início do próximo
        "css_classes": "un-depo-set" + (" un-depo-dup" if duplicate else ""),
    }
    if duplicate:
        s["_attributes"] = "aria-hidden|true"  # cópia só para a rolagem sem emenda (Pro)
    return container(s, [card(*t) for t in items])


def track(items, down=False):
    return container({
        "content_width": "full",
        "width": px(50, "%"),
        "flex_direction": "column",
        "css_classes": "un-depo-track" + (" un-depo-track--down" if down else ""),
    }, [card_set(items), card_set(items, duplicate=True)])


# ---------------------------------------------------------------------------
# Seção
# ---------------------------------------------------------------------------

def stat(number_html, label, count=False):
    num = heading(number_html, "p", WHITE, typo("typography", HANKEN, 44, 700, lh=44, ls=-1.5, size_m=36, lh_m=38))
    if count:
        add(num, classes="un-depo-count")
    return container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(6),
        "padding": dims(0, 0, 0, 16),
        "border_border": "solid",
        "border_width": dims(0, 0, 0, 3),
        "border_color": RED,
    }, [num, heading(label, "p", "rgba(255, 255, 255, 0.75)", typo("typography", HANKEN, 14, 400, lh=20))])


def left_column(html_widget):
    pill = heading("★★★★★ &nbsp;Famílias Unicultura", "p", WHITE,
                   typo("typography", HANKEN, 13, 600, lh=14, ls=0.3),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.08)", "_border_radius": dims(999),
                          "_border_border": "solid", "_border_width": dims(1),
                          "_border_color": "rgba(255, 255, 255, 0.18)", "_padding": dims(8, 16, 8, 16)})
    title = heading(
        'O que os pais <span style="font-style:italic;font-weight:300;color:#FFB867">dizem sobre nós?</span>',
        "h2", WHITE,
        typo("typography", HANKEN, 57, 500, lh=60, ls=-2, size_t=46, size_m=36, lh_t=50, lh_m=40, ls_m=-1.2))
    intro = text("<p>Histórias reais de famílias que escolheram a Unicultura e viram a transformação acontecer.</p>",
                 "rgba(255, 255, 255, 0.85)", typo("typography", HANKEN, 18, 400, lh=26, size_m=16, lh_m=24))
    stats = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_gap": gap(40),
        "flex_gap_mobile": gap(24),
        "margin": dims(12, 0, 8, 0),
    }, [
        stat("+1.200", "famílias confiam<br>na nossa escola", count=True),
        stat("2", "escolas, uma<br>trajetória completa"),
    ])
    cta = button(
        "Agendar visita", WHITE, "#010658",
        typo("typography", HANKEN, 16, 700, lh=22),
        dims(14, 22, 14, 28), radius="999",
        shadow={"horizontal": 0, "vertical": 6, "blur": 20, "spread": 0, "color": "rgba(241, 5, 5, 0.35)"},
        icon=12, css_classes="un-btn-arrow")
    return container({
        "content_width": "full",
        "width": px(460),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "flex-start",
        "flex_gap": gap(22),
        "_flex_size": "none",
    }, [
        add(pill, anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(intro, anim("fadeInUp", 200)),
        add(stats, anim("fadeInUp", 300)),
        add(cta, anim("fadeInUp", 400)),
        html_widget,
    ])


def build_section():
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    # CSS do botão com seta em círculo vermelho (a Home não tem .gt-btn-arrow)
    css += '''

/* Botão "Agendar visita": seta em círculo vermelho que gira no hover */
.un-depo .un-btn-arrow .elementor-button-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background-color: #F10505;
  color: #FFFFFF;
  fill: #FFFFFF;
  font-size: 12px;
  transition: transform 0.4s ease;
}

.un-depo .un-btn-arrow .elementor-button-icon svg {
  width: 1em;
  height: 1em;
  fill: currentColor;
}

.un-depo .un-btn-arrow .elementor-button-icon i,
.un-depo .un-btn-arrow .elementor-button-icon svg {
  transform: rotate(-45deg);
}

.un-depo .un-btn-arrow .elementor-button:hover .elementor-button-icon {
  transform: rotate(45deg);
}'''
    cols = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",  # Elementor força "wrap" em linhas no mobile; aqui precisa ser carrossel
        "flex_gap": gap(20),
        "_flex_size": "grow",
        "css_classes": "un-depo-cols",
    }, [track(TESTIMONIALS[:4]), track(TESTIMONIALS[4:], down=True)])
    js = open(JS_FILE, encoding="utf-8").read().strip()
    html_widget = widget("html", {"html": "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"})
    return container({
        "content_width": "boxed",
        "html_tag": "section",
        "boxed_width": px(1240),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_align_items_tablet": "stretch",
        "flex_gap": gap(64),
        "flex_gap_tablet": gap(48),
        "flex_gap_mobile": gap(36),
        "padding": dims(100, 24, 100, 24),
        "padding_tablet": dims(80, 24, 80, 24),
        "padding_mobile": dims(64, 16, 56, 16),
        "background_background": "classic",
        "background_color": BG,
        "css_classes": "gt-root un-depo",
    }, [
        left_column(html_widget),
        add(cols, anim("fadeIn", 200)),
    ], inner=False)


def main():
    data = {
        "content": [build_section()],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Seção Depoimentos",
        "type": "container",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
