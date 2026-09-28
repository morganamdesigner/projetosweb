#!/usr/bin/env python3
"""Gera o JSON da página "Sobre o Colégio Unicultura" - página inteira, sem o rodapé.

Mantém os textos e imagens do export atual e aplica o padrão das outras páginas: cabeçalho da Home,
cartão azul no hero (uma foto só), faixa de palavras, galeria em movimento, Poliedro e CTA final.
Seções próprias: trajetória (colagem de fotos + chamada para a Garatuja), proposta pedagógica
(título fixo + 3 cartões que acendem) e "O que buscamos formar" (10 capacidades com ícones próprios).
Saída: ../sobre-elementor.json

Uso:  python3 build_sobre.py [export-da-pagina-sobre.json]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("colegio-unicultura-fundamental1", "colegio-unicultura-fundamental2", "colegio-unicultura-diferenciais"):
    sys.path.insert(0, os.path.join(HERE, "..", "..", d, "src"))

SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/2b5d1091-elementor-1404-2026-09-28.json")
sys.argv = sys.argv[:1]

import build_fund1 as f1  # noqa: E402
import build_fund2 as f2  # noqa: E402
import build_diferenciais as bd  # noqa: E402
from build_fund1 import (  # noqa: E402
    HANKEN, INK, NAVY, PAGE_BG, RED, WHITE,
    add, anim, base, button, container, dims, gap, heading, icon_list, parallax, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "sobre-elementor.json")

# as funções das outras páginas passam a ler este export
f1.page = json.load(open(SRC, encoding="utf-8"))
f2.page = f1.page
find, src_text, media = f1.find, f1.src_text, f1.media
page = f1.page
f1.CSS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.css"), os.path.join(f1.HERE, "un-fund1.css"),
                os.path.join(os.path.dirname(f2.__file__), "un-fund2.css"),
                os.path.join(bd.HERE, "un-dif.css"), os.path.join(HERE, "un-sobre.css")]
f1.JS_FILES = [os.path.join(f1.HOME_SRC_DIR, "un-home-v2.js"), os.path.join(f1.HERE, "un-fund1.js")]

base._counter[0] = 29000  # faixa própria de IDs

SOFT = "#F5F6FF"

HERO_SOBRE = {
    "pill": "Sobre o Colégio Unicultura",
    # sem amarelo: o destaque é um marca-texto vermelho suave (como no hero da Home)
    "title": 'Conhecimento para ir <span class="un-mark-red">cada vez mais longe.</span>',
    "intro_id": "71f8f924",
    "secondary": ("Conhecer a proposta", "#proposta"),
    "photo": (404, "colegio-unicultura-bg-sobre.webp"),
    "segment": 0,  # página institucional: nenhum segmento em destaque
}

f2.MARQUEE_WORDS = ["Excelência acadêmica", "Acolhimento", "Autonomia", "Protagonismo", "Formação integral"]


def eyebrow(label, color=RED, align="left"):
    return f1.eyebrow(label, color, align)


def link(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def section(anchor, bg, children, classes, direction="column", gap_px=56, padding=None):
    s = {
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "flex_direction": direction,
        "flex_gap": gap(gap_px),
        "flex_gap_mobile": gap(36),
        "padding": padding or dims(120, 24, 120, 24),
        "padding_tablet": dims(96, 24, 96, 24),
        "padding_mobile": dims(72, 16, 72, 16),
        "background_background": "classic",
        "background_color": bg,
        "css_classes": "gt-root " + classes,
    }
    if anchor:
        s["_element_id"] = anchor
    return container(s, children, inner=False)


# ---------------------------------------------------------------------------
# 2. Uma trajetória construída com propósito (colagem de fotos + Garatuja)
# ---------------------------------------------------------------------------

def build_trajetoria():
    paragraphs = src_text("4bc2d0e7", "editor").split("</p>")
    first = paragraphs[0].replace("<p>", "").strip()
    quote = paragraphs[1].replace("<p>", "").strip()

    big = widget("image", {
        "image": find(page["content"], "592882ba")["settings"]["image"],
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(560),
        "height_tablet": px(460),
        "height_mobile": px(360),
        "object-fit": "cover",
        "image_border_radius": dims(32),
        "image_border_radius_mobile": dims(24),
        "_css_classes": "un-clip",
    })
    small = widget("image", {
        "image": find(page["content"], "67cb6bd4")["settings"]["image"],
        "image_size": "full",
        "width": px(100, "%"),
        "height": px(260),
        "height_mobile": px(170),
        "object-fit": "cover",
        "image_border_radius": dims(24),
        "_element_width": "initial",
        "_element_custom_width": px(250),
        "_element_custom_width_mobile": px(160),
        "_css_classes": "un-collage-small",
    })
    badge = container({
        "content_width": "full",
        "width": {"unit": "custom", "size": "max-content", "sizes": []},
        "flex_direction": "column",
        "flex_gap": gap(2),
        "padding": dims(16, 22, 16, 22),
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(18),
        "css_classes": "un-collage-badge",
    }, [heading("3º ano do Fundamental", "p", WHITE, typo("typography", HANKEN, 15, 700, lh=20)),
        heading("→ 3ª série do Médio", "p", "#FF8A8A", typo("typography", HANKEN, 15, 700, lh=20))])
    media_col = container({
        "content_width": "full",
        "width": px(48, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "css_classes": "un-collage un-io",
    }, [add(big, anim("fadeIn"), parallax(-1)), add(small, parallax(2)), badge])

    title = heading(src_text("61cafc45"), "h2", NAVY,
                    typo("typography", HANKEN, 50, 700, lh=54, ls=-1.8, size_t=42, size_m=32, lh_t=46, lh_m=36,
                         ls_m=-1.2))
    body = text("<p>" + first + "</p>", INK, typo("typography", HANKEN, 18, 400, lh=29, size_m=16, lh_m=26))
    manifesto = heading(quote.replace("Queremos prepará-los",
                                      'Queremos <span class="un-mark">prepará-los</span>'), "p", NAVY,
                        typo("typography", HANKEN, 26, 600, lh=34, ls=-0.6, size_m=21, lh_m=28),
                        extra={"_padding": dims(4, 0, 4, 24), "_border_border": "solid",
                               "_border_width": dims(0, 0, 0, 3), "_border_color": RED,
                               "_css_classes": "un-quote un-io"})
    garatuja = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_align_items": "center",
        "flex_gap": gap(18),
        "padding": dims(18, 22, 18, 18),
        "margin": dims(8, 0, 0, 0),
        "background_background": "classic",
        "background_color": SOFT,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.08)",
        "border_radius": dims(20),
        "css_classes": "un-garatuja",
    }, [
        widget("image", {"image": media(27, "logo-garatuha.webp"), "image_size": "full", "width": px(100, "%"),
                         "_element_width": "initial", "_element_custom_width": px(64),
                         "_element_custom_width_mobile": px(52), "_flex_size": "none"}),
        container({"content_width": "full", "flex_direction": "column", "flex_gap": gap(4)}, [
            heading("Procurando uma escola para a Educação Infantil ou os primeiros anos?", "p", INK,
                    typo("typography", HANKEN, 15, 500, lh=21, size_m=14, lh_m=19)),
            heading("Conheça a Escola Garatuja →", "p", RED, typo("typography", HANKEN, 17, 700, lh=22),
                    extra={"link": link("https://colegiounicultura.com.br/garatuja/"),
                           "_css_classes": "un-garatuja-link"}),
        ]),
    ])
    text_col = container({
        "content_width": "full",
        "width": px(52, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(22),
    }, [add(eyebrow("Nossa história"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(body, anim("fadeInUp", 200)),
        add(manifesto, anim("fadeInUp", 300)),
        add(garatuja, anim("fadeInUp", 400))])
    return section("trajetoria", PAGE_BG, [media_col, text_col], "un-trajetoria", direction="row", gap_px=80,
                   padding=dims(110, 24, 120, 24))


def patch_direction(sec):
    s = sec["settings"]
    s["flex_direction_tablet"] = "column"
    s["flex_align_items"] = "center"
    s["flex_gap_tablet"] = gap(56)
    return sec


# ---------------------------------------------------------------------------
# 4. Nossa proposta pedagógica (azul): título fixo + 3 cartões que acendem
# ---------------------------------------------------------------------------

PROPOSTA_LABELS = ["Cada etapa respeitada", "Uma trajetória contínua", "Base sólida e parceiros"]


def build_proposta():
    raw = src_text("3db1035f")
    parts = [p.strip() for p in raw.replace("\n", " ").split("<br><br>") if p.strip()]
    cards = []
    for i, (label, copy) in enumerate(zip(PROPOSTA_LABELS, parts)):
        cards.append(add(container({
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": gap(10),
            "padding": dims(30, 32, 32, 32),
            "padding_mobile": dims(24, 22, 26, 22),
            "background_background": "classic",
            "background_color": "rgba(255, 255, 255, 0.05)",
            "border_border": "solid",
            "border_width": dims(1),
            "border_color": "rgba(255, 255, 255, 0.12)",
            "border_radius": dims(24),
            "css_classes": "un-pcard un-io",
        }, [heading(f"{i + 1:02d}", "p", "#FF8A8A", typo("typography", HANKEN, 14, 800, lh=16, ls=1.4)),
            heading(label, "h3", WHITE, typo("typography", HANKEN, 24, 700, lh=30, ls=-0.6, size_m=20, lh_m=26)),
            text("<p>" + copy + "</p>", "rgba(255, 255, 255, 0.8)",
                 typo("typography", HANKEN, 17, 400, lh=27, size_m=15, lh_m=24))]), anim("fadeInUp", i * 120)))
    pill = heading(src_text("2ed06df7"), "p", WHITE,
                   typo("typography", HANKEN, 12, 700, lh=16, ls=1.2, transform="uppercase"),
                   extra={"_element_width": "auto", "_background_background": "classic", "_background_color": RED,
                          "_border_radius": dims(999), "_padding": dims(8, 14, 8, 14)})
    title = heading(src_text("7723825c"), "h2", WHITE,
                    typo("typography", HANKEN, 52, 700, lh=56, ls=-2, size_t=44, size_m=34, lh_t=48, lh_m=38,
                         ls_m=-1.2))
    values = bd.pills(["Excelência acadêmica", "Acolhimento", "Autonomia", "Protagonismo", "Formação integral"],
                      dark=True)
    cta = button("Agendar visita", WHITE, INK, typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                 dims(12, 12, 12, 26), radius="999", icon=16, css_classes="un-btn-arrow",
                 extra={"link": link("/matriculas"), "_flex_align_self": "flex-start"})
    side = container({
        "content_width": "full",
        "width": px(40, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(20),
        "css_classes": "un-sticky",
    }, [add(pill, anim("fadeInUp")), add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(values, anim("fadeInUp", 200)), add(cta, anim("fadeInUp", 300))])
    stack = container({
        "content_width": "full",
        "width": px(60, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_gap": gap(18),
    }, cards)
    sec = section("proposta", NAVY, [side, stack], "un-proposta-sobre un-grid-bg", direction="row",
                  gap_px=64)
    sec["settings"]["flex_direction_tablet"] = "column"
    sec["settings"]["flex_align_items"] = "flex-start"
    return sec


# ---------------------------------------------------------------------------
# 5. O que buscamos formar: 10 capacidades, cada uma com seu ícone
# ---------------------------------------------------------------------------

CAPACIDADES_ICONS = {
    "Aprender com autonomia": "fas fa-compass",
    "Criar e inovar": "fas fa-lightbulb",
    "Pensar criticamente": "fas fa-brain",
    "Conviver e trabalhar coletivamente": "fas fa-users",
    "Comunicar suas ideias": "fas fa-comments",
    "Compreender suas emoções": "fas fa-heart",
    "Investigar e resolver problemas": "fas fa-search",
    "Fazer escolhas responsáveis": "fas fa-balance-scale",
    "Utilizar a tecnologia de maneira consciente": "fas fa-laptop",
    "Transformar conhecimento em ação": "fas fa-rocket",
}
CAPACIDADES_IDS = ["37749f7", "7a9545ce", "4a5e1ff5", "21de47dc", "1cba9a26", "37cdec19", "2c637123", "1da7b6d0",
                   "148e33e4", "7a73f45b"]


def build_formar():
    items = [find(page["content"], i)["settings"]["icon_list"][0]["text"] for i in CAPACIDADES_IDS]
    cards = []
    for i, label in enumerate(items):
        card = f1.priority_card({"text": label, "selected_icon": {
            "value": CAPACIDADES_ICONS.get(label, "fas fa-star"), "library": "fa-solid"}}, i)
        card["settings"].update({
            "icon_size": px(24),
            "icon_size_mobile": px(20),
            "view": "stacked",
            "shape": "circle",
            "primary_color": "#EDEEFA",
            "secondary_color": NAVY,
            "icon_padding": px(16),
            "icon_space": px(16),
            **typo("title_typography", HANKEN, 17, 600, lh=22, ls=-0.2, size_m=15, lh_m=20),
        })
        card["settings"]["_animation_delay"] = (i % 5) * 90
        cards.append(card)
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "grid_columns_grid": {"unit": "fr", "size": 5, "sizes": []},
        "grid_columns_grid_tablet": {"unit": "fr", "size": 3, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 2, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 2, "sizes": []},
        "grid_rows_grid_tablet": {"unit": "fr", "size": 4, "sizes": []},
        "grid_rows_grid_mobile": {"unit": "fr", "size": 5, "sizes": []},
        "grid_gaps": {"column": "16", "row": "16", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "10", "row": "10", "isLinked": True, "unit": "px"},
    }, cards)
    title = heading('O que buscamos <span class="un-pill">formar</span>', "h2", NAVY,
                    typo("typography", HANKEN, 52, 700, lh=62, ls=-2, size_t=44, size_m=34, lh_t=54, lh_m=44,
                         ls_m=-1.2),
                    align="center", extra={"_css_classes": "un-io"})
    lead = text("<p>" + src_text("63262c6f") + "</p>", INK,
                typo("typography", HANKEN, 19, 400, lh=29, size_m=16, lh_m=25), align="center")
    head = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(16),
    }, [add(eyebrow("Nosso método de ensino", align="center"), anim("fadeInUp")),
        add(title, anim("fadeIn", 100), classes="un-reveal"),
        add(lead, anim("fadeInUp", 200))])
    return section("formar", SOFT, [head, grid], "un-prioridades un-formar")


def main():
    cta = bd.build_cta('Quer conhecer o Unicultura <span class="un-mark-red">de perto?</span>',
                       "Agende uma visita e converse com nossa equipe pedagógica.")
    data = {
        "content": [
            f1.build_top(HERO_SOBRE),
            f2.build_marquee(),
            patch_direction(build_trajetoria()),
            f1.build_galeria(),
            build_proposta(),
            build_formar(),
            f1.build_poliedro(("66f6ebca", "76dbc12e", "156f3fc1")),
            cta,
        ],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Sobre",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
