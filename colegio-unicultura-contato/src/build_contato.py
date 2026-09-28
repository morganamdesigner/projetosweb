#!/usr/bin/env python3
"""Gera o JSON da página "Contato" (Colégio Unicultura, URL sugerida /contato), sem o rodapé.

Mesma identidade das páginas Diferenciais e Parceiros (cabeçalho da Home, cartão azul no hero,
capítulos numerados). Os dados de contato ainda são placeholders [entre colchetes] - trocar pelos
dados reais (ver README). O mapa usa o widget Google Maps nativo do Elementor (sem chave de API).
Saída: ../contato-elementor.json

Uso:  python3 build_contato.py
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
    add, anim, base, button, col, container, dims, eyebrow, gap, h2, heading, html, link, para, px, row, typo,
    widget,
)

f1 = bd.f1
OUT = os.path.join(HERE, "..", "contato-elementor.json")
CSS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.css"), os.path.join(f1.HERE, "un-fund1.css"),
             os.path.join(bd.HERE, "un-dif.css"), os.path.join(HERE, "un-contato.css")]
JS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.js"), os.path.join(f1.HERE, "un-fund1.js"),
            os.path.join(bd.HERE, "un-dif.js")]

base._counter[0] = 27000  # faixa própria de IDs

bd.CHAPTERS = [("canais", "Fale com a gente"), ("onde-estamos", "Onde estamos"), ("redes", "Redes sociais")]

# ---------------------------------------------------------------------------
# DADOS DE CONTATO (placeholders: trocar aqui e gerar de novo, ou editar direto no Elementor)
# ---------------------------------------------------------------------------
TELEFONE = "[inserir telefone]"
TELEFONE_LINK = ""                 # ex.: "tel:+551130000000"
WHATSAPP = "[inserir número]"
WHATSAPP_LINK = ""                 # ex.: "https://wa.me/5511900000000"
EMAIL = "[inserir e-mail institucional]"
EMAIL_LINK = ""                    # ex.: "mailto:contato@colegiounicultura.com.br"
ENDERECO = "[inserir endereço completo — Colégio Unicultura]"
HORARIO = "[inserir horário]"
MAPA_BUSCA = "Colégio Unicultura"  # o que o mapa procura; trocar pelo endereço completo
COMO_CHEGAR = "https://www.google.com/maps/dir/?api=1&destination=Col%C3%A9gio+Unicultura"
REDES = [  # (ícone, nome, perfil, link) - manter só as redes que o colégio usa
    ("fab fa-instagram", "Instagram", "[@perfil]", ""),
    ("fab fa-facebook-f", "Facebook", "[/pagina]", ""),
    ("fab fa-youtube", "YouTube", "[canal]", ""),
]


def svg(name):
    return open(os.path.join(HERE, "ilustracoes", name), encoding="utf-8").read().strip()


def ext_link(url):
    return {"url": url, "is_external": "on" if url.startswith("http") else "", "nofollow": "",
            "custom_attributes": ""}


def whatsapp_button(label="Chamar no WhatsApp", dark_bg=True):
    return button(label, "#25D366", WHITE, typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                  dims(14, 26, 14, 22), radius="999", css_classes="un-btn-whatsapp",
                  extra={"link": ext_link(WHATSAPP_LINK),
                         "selected_icon": {"value": "fab fa-whatsapp", "library": "fa-brands"},
                         "icon_align": "left", "icon_indent": px(10),
                         "button_background_hover_color": "#1EBE5A"})


# ---------------------------------------------------------------------------
# Topo: cabeçalho da Home + cartão azul com a conversa animada
# ---------------------------------------------------------------------------

def build_top():
    pill = heading('<span class="un-dot"></span>Contato', "p", WHITE,
                   typo("typography", HANKEN, 13, 700, lh=16, ls=0.7, transform="uppercase", size_m=11, lh_m=14),
                   extra={"_element_width": "auto", "_background_background": "classic",
                          "_background_color": "rgba(255, 255, 255, 0.06)", "_border_border": "solid",
                          "_border_width": dims(1), "_border_color": "rgba(255, 255, 255, 0.28)",
                          "_border_radius": dims(999), "_padding": dims(10, 18, 10, 16),
                          "_padding_mobile": dims(8, 14, 8, 12)})
    title = heading(f'Vamos <span style="color:{ORANGE}">conversar?</span>', "h1", WHITE,
                    typo("typography", HANKEN, 76, 700, lh=76, ls=-3, size_t=60, size_m=42, lh_t=62, lh_m=44,
                         ls_m=-1.6))
    intro = para("Estamos à disposição para tirar suas dúvidas sobre o Colégio Unicultura e a Escola Garatuja — "
                 "sobre proposta pedagógica, matrículas ou qualquer outro assunto.",
                 "rgba(255, 255, 255, 0.85)", size=19, width=540)
    secondary = button("Ver todos os canais", "rgba(255, 255, 255, 0)", WHITE,
                       typo("typography", HANKEN, 17, 600, lh=22, size_m=16),
                       dims(14, 8, 14, 8), radius="999", css_classes="un-btn-link",
                       extra={"link": link("#canais"),
                              "selected_icon": {"value": "fas fa-arrow-down", "library": "fa-solid"},
                              "icon_align": "right", "icon_indent": px(10)})
    actions = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(12),
        "margin": dims(14, 0, 0, 0),
    }, [whatsapp_button(), secondary])
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
    art = container({
        "content_width": "full",
        "width": px(46, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
    }, [add(html(svg("conversa.svg"), "un-talk-wrap"), anim("zoomIn", 300))])
    card = container({
        "content_width": "full",
        "width": px(100, "%"),
        "min_height": px(640),
        "min_height_tablet": px(0),
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "center",
        "flex_gap": gap(32),
        "padding": dims(56, 64, 56, 88),
        "padding_tablet": dims(52, 44, 40, 44),
        "padding_mobile": dims(36, 22, 24, 22),
        "overflow": "hidden",
        "border_radius": dims(40),
        "border_radius_mobile": dims(28),
        "background_background": "classic",
        "background_color": CARD_BG,
        "css_classes": "un-hero un-hero--dif",
    }, [content, art])
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
# 01 Fale com a gente: cartão do WhatsApp em destaque + 4 cartões de canais
# ---------------------------------------------------------------------------

def channel(icon, label, value, url="", delay=0, library="fa-solid"):
    badge = widget("icon", {
        "selected_icon": {"value": icon, "library": library},
        "view": "stacked",
        "shape": "circle",
        "primary_color": "#EDEEFA",
        "secondary_color": NAVY,
        "size": px(20),
        "icon_padding": px(16),
        "align": "left",
        "_css_classes": "un-card-icon",
    })
    value_widget = heading(value, "p", NAVY, typo("typography", HANKEN, 20, 700, lh=27, ls=-0.3, size_m=18, lh_m=24),
                           extra={"_css_classes": "un-channel-value"})
    if url:
        value_widget["settings"]["link"] = ext_link(url)
    card = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(10),
        "padding": dims(28, 26, 28, 26),
        "padding_mobile": dims(22, 20, 22, 20),
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.08)",
        "border_radius": dims(24),
        "css_classes": "un-card un-channel",
    }, [badge,
        heading(label, "p", RED, typo("typography", HANKEN, 12, 700, lh=16, ls=1.3, transform="uppercase")),
        value_widget])
    return add(card, anim("fadeInUp", delay))


def build_canais():
    whats = container({
        "content_width": "full",
        "width": px(40, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_justify_content": "space-between",
        "flex_gap": gap(28),
        "padding": dims(44, 40, 40, 40),
        "padding_mobile": dims(32, 24, 28, 24),
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(32),
        "border_radius_mobile": dims(26),
        "css_classes": "un-whats-card",
    }, [
        widget("icon", {"selected_icon": {"value": "fab fa-whatsapp", "library": "fa-brands"}, "view": "stacked",
                        "shape": "circle", "primary_color": "#25D366", "secondary_color": WHITE, "size": px(30),
                        "icon_padding": px(20), "align": "left", "_css_classes": "un-whats-icon"}),
        container({"content_width": "full", "flex_direction": "column", "flex_gap": gap(8)}, [
            heading("WhatsApp", "p", ORANGE, typo("typography", HANKEN, 13, 700, lh=16, ls=1.4,
                                                  transform="uppercase")),
            heading(WHATSAPP, "p", WHITE, typo("typography", HANKEN, 34, 700, lh=40, ls=-1, size_m=26, lh_m=32)),
            para("O jeito mais rápido de falar com a gente.", "rgba(255, 255, 255, 0.75)", size=17),
        ]),
        whatsapp_button(),
    ])
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "width": px(60, "%"),
        "width_tablet": px(100, "%"),
        "grid_columns_grid": {"unit": "fr", "size": 2, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 1, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 2, "sizes": []},
        "grid_rows_grid_mobile": {"unit": "fr", "size": 4, "sizes": []},
        "grid_gaps": {"column": "16", "row": "16", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "12", "row": "12", "isLinked": True, "unit": "px"},
    }, [channel("fas fa-phone-alt", "Telefone", TELEFONE, TELEFONE_LINK, 0),
        channel("fas fa-envelope", "E-mail", EMAIL, EMAIL_LINK, 100),
        channel("fas fa-map-marker-alt", "Endereço", ENDERECO, "", 200),
        channel("fas fa-clock", "Horário da secretaria", HORARIO, "", 300)])
    head = col([add(eyebrow("Canais de atendimento"), anim("fadeInUp")),
                add(h2('Fale com <span class="un-mark">a gente</span>'), anim("fadeIn", 100),
                    classes="un-reveal un-io")], 100)
    body = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "stretch",
        "flex_gap": gap(20),
    }, [add(whats, anim("fadeInUp")), grid])
    return bd.chapter(1, PAGE_BG, [head, body])


# ---------------------------------------------------------------------------
# 02 Onde estamos: mapa grande com cartão de endereço por cima
# ---------------------------------------------------------------------------

def build_mapa():
    head = col([add(eyebrow("Visite a escola"), anim("fadeInUp")),
                add(h2("Onde estamos"), anim("fadeIn", 100), classes="un-reveal")], 100)
    gmap = widget("google_maps", {
        "address": MAPA_BUSCA,
        "zoom": px(16),
        "height": px(520),
        "height_tablet": px(440),
        "height_mobile": px(360),
        "_css_classes": "un-map",
    })
    info = container({
        "content_width": "full",
        "width": {"unit": "custom", "size": "min(380px, calc(100% - 32px))", "sizes": []},
        "flex_direction": "column",
        "flex_gap": gap(12),
        "padding": dims(28, 28, 28, 28),
        "background_background": "classic",
        "background_color": WHITE,
        "border_radius": dims(24),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {"horizontal": 0, "vertical": 24, "blur": 50, "spread": 0,
                                  "color": "rgba(1, 6, 88, 0.2)"},
        "css_classes": "un-map-card",
    }, [
        heading("Colégio Unicultura", "h3", NAVY, typo("typography", HANKEN, 22, 700, lh=28, ls=-0.4)),
        para(ENDERECO, INK, size=16),
        para(f"<strong>Secretaria:</strong> {HORARIO}", INK, size=15),
        button("Como chegar", NAVY, WHITE, typo("typography", HANKEN, 16, 700, lh=20), dims(12, 12, 12, 22),
               radius="999", icon=14, css_classes="un-btn-arrow", extra={"link": ext_link(COMO_CHEGAR)}),
    ])
    frame = container({
        "content_width": "full",
        "flex_direction": "column",
        "overflow": "hidden",
        "border_radius": dims(32),
        "border_radius_mobile": dims(24),
        "css_classes": "un-map-frame",
    }, [gmap, add(info, anim("fadeInUp", 300))])
    return bd.chapter(2, SOFT, [head, add(frame, anim("fadeIn", 100))])


# ---------------------------------------------------------------------------
# 03 Redes sociais: um cartão grande por rede
# ---------------------------------------------------------------------------

def social_tile(icon, name, handle, url, delay):
    tile = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(18),
        "padding": dims(24, 26, 24, 22),
        "background_background": "classic",
        "background_color": "rgba(255, 255, 255, 0.05)",
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(255, 255, 255, 0.14)",
        "border_radius": dims(24),
        "css_classes": "un-social un-social--" + name.lower(),
    }, [
        widget("icon", {"selected_icon": {"value": icon, "library": "fa-brands"}, "view": "stacked",
                        "shape": "circle", "primary_color": WHITE, "secondary_color": NAVY, "size": px(24),
                        "icon_padding": px(18), "_css_classes": "un-social-icon", "_flex_size": "none",
                        "link": ext_link(url)}),
        container({"content_width": "full", "flex_direction": "column", "flex_gap": gap(2)}, [
            heading(name, "h3", WHITE, typo("typography", HANKEN, 22, 700, lh=26, ls=-0.4),
                    extra={"link": ext_link(url)}),
            heading(handle, "p", "rgba(255, 255, 255, 0.65)", typo("typography", HANKEN, 15, 500, lh=20)),
        ]),
        widget("icon", {"selected_icon": {"value": "fas fa-arrow-right", "library": "fa-solid"},
                        "primary_color": ORANGE, "size": px(18), "_css_classes": "un-social-arrow",
                        "_flex_size": "none", "link": ext_link(url)}),
    ])
    return add(tile, anim("fadeInUp", delay))


def build_redes():
    head = row([
        col([add(eyebrow("Redes sociais", ORANGE), anim("fadeInUp")),
             add(h2(f'Siga a <span style="color:{ORANGE}">Unicultura</span>', WHITE), anim("fadeIn", 100),
                 classes="un-reveal")], 50),
        col([add(para("Acompanhe o dia a dia da escola, eventos e novidades pelas nossas redes:",
                      "rgba(255, 255, 255, 0.82)", size=19), anim("fadeInUp", 200))], 50),
    ], align="flex-end")
    tiles = bd.grid3([social_tile(icon, name, handle, url, i * 120) for i, (icon, name, handle, url)
                      in enumerate(REDES)], cols_tablet=1, gap_px=18, gap_m=12)
    return bd.chapter(3, NAVY, [head, tiles], dark=True, extra_classes="un-grid-bg")


def main():
    data = {
        "content": [build_top(), build_canais(), build_mapa(), build_redes()],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Contato",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
