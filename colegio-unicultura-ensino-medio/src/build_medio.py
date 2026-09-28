#!/usr/bin/env python3
"""Gera o JSON da página "Ensino Médio" (Colégio Unicultura) - página inteira, sem o rodapé.

Segue o modelo das páginas do Fundamental I e II (hero da Home com uma foto só, faixa de palavras,
cartão com foto, galeria, Poliedro, equipe e CTA) e acrescenta:
- "Uma trajetória que consolida": os 14 itens em cards com ícone, o de ENEM/vestibulares em destaque;
- manifesto "Mais do que uma universidade, um caminho próprio": um caminho desenhado com o scroll
  e a frase acendendo palavra por palavra.
Saída: ../ensino-medio-elementor.json

Uso:  python3 build_medio.py [export-da-pagina-ensino-medio.json]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-fundamental1", "src"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "colegio-unicultura-fundamental2", "src"))

EM_SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/b50cfc36-elementor-1062-2026-09-28.json")
sys.argv = sys.argv[:1]  # os outros geradores também leem sys.argv

import build_fund1 as f1  # noqa: E402
import build_fund2 as f2  # noqa: E402
from build_fund1 import (  # noqa: E402
    HANKEN, INK, NAVY, ORANGE, PAGE_BG, WHITE,
    add, anim, base, button, container, dims, eyebrow, gap, heading, px, text, typo, widget,
)

OUT = os.path.join(HERE, "..", "ensino-medio-elementor.json")

# as funções do Fundamental I/II passam a ler esta página
f1.page = json.load(open(EM_SRC, encoding="utf-8"))
f1.CSS_FILES = f1.CSS_FILES + [os.path.join(HERE, "un-medio.css")]
f1.JS_FILES = f1.JS_FILES + [os.path.join(HERE, "un-medio.js")]
f2.page = f1.page
find, src_text = f1.find, f1.src_text
page = f1.page

base._counter[0] = 21000  # faixa própria de IDs

HERO_EM = {
    "pill": "Ensino Médio · 1ª à 3ª série",
    "title": f'Excelência acadêmica. <span style="color:{ORANGE}">Preparação para o futuro.</span>',
    "intro_id": "578663c8",
    "secondary": ("Conhecer a proposta", "#a-proposta"),
    # a página atual não tinha foto no fundo do hero (só o slideshow antigo): usamos a 2ª foto dele
    "photo": (361, "foto2-home-2.webp"),
    "segment": 4,  # "Ensino Médio" em destaque
}

f2.MARQUEE_WORDS = ["ENEM", "Vestibulares", "Pensamento crítico", "Projeto de vida", "Autonomia intelectual",
                    "Vida universitária"]


# ---------------------------------------------------------------------------
# 3. Uma trajetória que consolida (14 cards)
# ---------------------------------------------------------------------------

HIGHLIGHT = "Preparação para ENEM e vestibulares"


def proposta_card(item, index):
    card = f1.priority_card(item, index)
    s = card["settings"]
    s.update({
        "position": "inline-start",
        "content_vertical_alignment": "middle",
        "icon_space": px(16),
        "icon_size": px(44),
        "icon_size_mobile": px(38),
        "_padding": dims(18, 22, 18, 18),
        "_padding_mobile": dims(14, 16, 14, 14),
        **typo("title_typography", HANKEN, 17, 600, lh=22, ls=-0.2, size_m=15, lh_m=20),
    })
    if item["text"] == HIGHLIGHT:
        s.update({"_background_color": NAVY, "title_color": WHITE, "hover_title_color": WHITE,
                  "_css_classes": s["_css_classes"] + " un-prio--hl"})
    return card


def build_proposta():
    lists = [find(page["content"], i)["settings"]["icon_list"] for i in ("6ea938e8", "5e5c64f6", "746b1143")]
    # ordem de leitura por linhas: as 3 listas originais eram as colunas
    items = [lst[r] for r in range(max(map(len, lists))) for lst in lists if r < len(lst)]
    grid = container({
        "content_width": "full",
        "container_type": "grid",
        "grid_columns_grid": {"unit": "fr", "size": 3, "sizes": []},
        "grid_columns_grid_tablet": {"unit": "fr", "size": 2, "sizes": []},
        "grid_columns_grid_mobile": {"unit": "fr", "size": 1, "sizes": []},
        "grid_rows_grid": {"unit": "fr", "size": 5, "sizes": []},
        "grid_rows_grid_tablet": {"unit": "fr", "size": 7, "sizes": []},
        "grid_rows_grid_mobile": {"unit": "fr", "size": 14, "sizes": []},
        "grid_gaps": {"column": "16", "row": "16", "isLinked": True, "unit": "px"},
        "grid_gaps_mobile": {"column": "10", "row": "10", "isLinked": True, "unit": "px"},
        "grid_auto_flow": "row",
    }, [proposta_card(it, i) for i, it in enumerate(items)])

    title = heading('Uma trajetória que <span class="un-pill">consolida:</span>', "h2", NAVY,
                    typo("typography", HANKEN, 52, 700, lh=62, ls=-2, size_t=44, size_m=34, lh_t=54, lh_m=44,
                         ls_m=-1.2),
                    extra={"_css_classes": "un-io"})
    body = text("<p>" + src_text("500f974d", "editor").strip() + "</p>", INK,
                typo("typography", HANKEN, 18, 400, lh=29, size_m=16, lh_m=26))
    head = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "flex-end",
        "flex_align_items_tablet": "flex-start",
        "flex_justify_content": "space-between",
        "flex_gap": gap(56),
        "flex_gap_tablet": gap(18),
    }, [
        container({"content_width": "full", "width": px(52, "%"), "width_tablet": px(100, "%"),
                   "flex_direction": "column", "flex_gap": gap(18)},
                  [add(eyebrow("Nossa proposta"), anim("fadeInUp")),
                   add(title, anim("fadeIn", 100), classes="un-reveal")]),
        container({"content_width": "full", "width": px(42, "%"), "width_tablet": px(100, "%"),
                   "flex_direction": "column"}, [add(body, anim("fadeInUp", 200))]),
    ])
    cta = button("Agendar visita", NAVY, WHITE, typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                 dims(12, 12, 12, 26), radius="999", icon=16, css_classes="un-btn-arrow", align="center")
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "_element_id": "a-proposta",
        "flex_direction": "column",
        "flex_gap": gap(56),
        "flex_gap_mobile": gap(32),
        "padding": dims(96, 24, 120, 24),
        "padding_tablet": dims(80, 24, 96, 24),
        "padding_mobile": dims(56, 16, 72, 16),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-prioridades un-proposta",
    }, [head, grid, add(cta, anim("fadeInUp"))], inner=False)


# ---------------------------------------------------------------------------
# 4. Diferenciais que fazem parte dessa fase (bento: cartão azul + 3 cards)
#    Antes era um cartão com foto-estudante-uni-bg.webp de fundo, mas essa imagem é uma
#    composição pronta (feita para "contain") e ficava estranha cortada atrás do texto.
# ---------------------------------------------------------------------------

DIFERENCIAIS = [  # (ícone, título, apoio) - os 3 diferenciais citados no texto da seção
    ("fas fa-chalkboard-teacher", "Plantão de Monitoria", "Revisão de conteúdos e esclarecimento de dúvidas."),
    ("fas fa-book-open", "Clube de Leitura", "Leitura, conversa e repertório cultural."),
    ("fas fa-chart-line", "Simulados e análise de desempenho", "Preparação intensiva para o ENEM e os vestibulares."),
]


def dif_tile(index, icon, title, note):
    badge = widget("icon", {
        "selected_icon": {"value": icon, "library": "fa-solid"},
        "view": "stacked",
        "shape": "circle",
        "primary_color": "#EDEEFA",
        "secondary_color": NAVY,
        "size": px(22),
        "size_mobile": px(18),
        "icon_padding": px(18),
        "icon_padding_mobile": px(15),
        "_flex_size": "none",
        "_css_classes": "un-dif-icon",
    })
    body = container({
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": gap(4),
        # sem "_flex_size": o padrão (encolher) faz o texto ocupar só o espaço ao lado do ícone
    }, [
        heading(f"{index:02d}", "p", "#F10505", typo("typography", HANKEN, 13, 700, lh=16, ls=1.3)),
        heading(title, "h3", NAVY, typo("typography", HANKEN, 22, 700, lh=28, ls=-0.5, size_m=18, lh_m=24)),
        text("<p>" + note + "</p>", INK, typo("typography", HANKEN, 16, 400, lh=24, size_m=15, lh_m=22)),
    ])
    tile = container({
        "content_width": "full",
        "flex_direction": "row",
        "flex_direction_mobile": "row",
        "flex_wrap_mobile": "nowrap",
        "flex_align_items": "center",
        "flex_gap": gap(22),
        "flex_gap_mobile": gap(16),
        "padding": dims(26, 28, 26, 26),
        "padding_mobile": dims(20, 18, 20, 18),
        "background_background": "classic",
        "background_color": WHITE,
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(1, 6, 88, 0.08)",
        "border_radius": dims(24),
        "border_radius_mobile": dims(20),
        "css_classes": "un-dif-tile",
    }, [badge, body])
    return add(tile, anim("fadeInLeft", 150 + index * 130))


def build_diferenciais():
    title = heading(f'Diferenciais que fazem parte <span style="color:{ORANGE}">dessa fase</span>', "h2", WHITE,
                    typo("typography", HANKEN, 52, 700, lh=56, ls=-2, size_t=46, size_m=34, lh_t=50, lh_m=38,
                         ls_m=-1.2))
    body = text("<p>" + src_text("6c98a39f", "editor").strip() + "</p>", "rgba(255, 255, 255, 0.82)",
                typo("typography", HANKEN, 19, 400, lh=30, size_m=16, lh_m=25))
    cta = button("Ver todos os diferenciais", WHITE, INK, typo("typography", HANKEN, 17, 700, lh=22, size_m=15),
                 dims(12, 12, 12, 26), radius="999", icon=16, css_classes="un-btn-arrow",
                 extra={"_flex_align_self": "flex-start"})
    card = container({
        "content_width": "full",
        "width": px(50, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_gap": gap(22),
        "padding": dims(64, 56, 64, 56),
        "padding_tablet": dims(52, 44, 52, 44),
        "padding_mobile": dims(40, 24, 40, 24),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "border_radius": dims(32),
        "border_radius_mobile": dims(26),
        "css_classes": "un-dif-card",
    }, [add(eyebrow("No dia a dia", ORANGE), anim("fadeInUp", 100)),
        add(title, anim("fadeIn", 200), classes="un-reveal"),
        add(body, anim("fadeInUp", 300)),
        add(cta, anim("fadeInUp", 400))])
    tiles = container({
        "content_width": "full",
        "width": px(50, "%"),
        "width_tablet": px(100, "%"),
        "flex_direction": "column",
        "flex_justify_content": "center",
        "flex_gap": gap(16),
        "flex_gap_mobile": gap(12),
    }, [dif_tile(i + 1, *d) for i, d in enumerate(DIFERENCIAIS)])
    return container({
        "content_width": "boxed",
        "boxed_width": px(1240),
        "html_tag": "section",
        "flex_direction": "row",
        "flex_direction_tablet": "column",
        "flex_align_items": "stretch",
        "flex_gap": gap(24),
        "flex_gap_mobile": gap(16),
        "padding": dims(40, 24, 120, 24),
        "padding_tablet": dims(32, 24, 96, 24),
        "padding_mobile": dims(24, 16, 72, 16),
        "background_background": "classic",
        "background_color": PAGE_BG,
        "css_classes": "gt-root un-diferenciais",
    }, [add(card, anim("fadeInUp")), tiles], inner=False)


# ---------------------------------------------------------------------------
# 7. Manifesto: "Mais do que uma universidade, um caminho próprio"
# ---------------------------------------------------------------------------

PATH_SVG = (
    '<svg class="un-path" viewBox="0 0 1440 640" preserveAspectRatio="none" aria-hidden="true">'
    '<path class="un-path-line" pathLength="1" d="M-40 560 C 220 520, 260 300, 520 330 S 860 560, 1040 380 '
    'S 1260 120, 1480 90"/>'
    '<circle class="un-path-dot" r="7" cx="0" cy="0"/>'
    '</svg>'
)


def build_manifesto():
    title_text = src_text("3ac952c4").strip() + ' <span class="un-way">' + src_text("2c51fd7d").strip() + "</span>"
    title = heading(title_text, "h2", WHITE,
                    typo("typography", HANKEN, 72, 700, lh=74, ls=-2.8, size_t=56, size_m=38, lh_t=60, lh_m=42,
                         ls_m=-1.4),
                    align="center",
                    extra={"_element_width": "initial", "_element_custom_width": px(900),
                           "_element_custom_width_tablet": px(100, "%")})
    quote = text("<p>" + src_text("10cfd74f", "editor").strip() + "</p>", WHITE,
                 typo("typography", HANKEN, 30, 500, lh=42, ls=-0.6, size_t=26, size_m=21, lh_t=36, lh_m=30),
                 align="center",
                 extra={"_element_width": "initial", "_element_custom_width": px(820),
                        "_element_custom_width_tablet": px(100, "%"), "_css_classes": "un-scrub"})
    cta = button("Agendar visita", WHITE, INK, typo("typography", HANKEN, 17, 700, lh=22, size_m=16),
                 dims(12, 12, 12, 26), radius="999", icon=16, css_classes="un-btn-arrow", align="center")
    path = widget("html", {"html": PATH_SVG, "_css_classes": "un-path-wrap"})
    return container({
        "content_width": "boxed",
        "boxed_width": px(1100),
        "html_tag": "section",
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_gap": gap(30),
        "flex_gap_mobile": gap(22),
        "padding": dims(150, 24, 150, 24),
        "padding_tablet": dims(112, 24, 112, 24),
        "padding_mobile": dims(88, 16, 88, 16),
        "overflow": "hidden",
        "background_background": "classic",
        "background_color": NAVY,
        "css_classes": "gt-root un-manifesto",
    }, [path,
        add(eyebrow("Nosso propósito", ORANGE, align="center"), anim("fadeInUp")),
        add(title, anim("fadeInUp", 100)),
        quote,
        add(cta, anim("fadeInUp", 200))], inner=False)


def main():
    data = {
        "content": [
            f1.build_top(HERO_EM),
            f2.build_marquee(),
            build_proposta(),
            build_diferenciais(),
            f1.build_poliedro(("39895257", "251c7720", "12f4fb8c")),
            f1.build_galeria(),
            build_manifesto(),
            f1.build_equipe("620da8d6"),
            f1.build_cta("759fdd5f"),
        ],
        "page_settings": [],
        "version": "0.4",
        "title": "Unicultura - Ensino Médio",
        "type": "page",
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")
    write_section(data["content"][3], OUT_DIFERENCIAIS, "Unicultura - Ensino Médio - Diferenciais")


# ---------------------------------------------------------------------------
# JSON só da seção "Diferenciais" (para trocar a seção sem reimportar a página)
# ---------------------------------------------------------------------------

OUT_DIFERENCIAIS = os.path.join(HERE, "..", "secao-diferenciais-elementor.json")


def css_between(path, start, end=None):
    css = open(path, encoding="utf-8").read()
    i = css.index(start)
    j = css.index(end, i + 1) if end else len(css)
    return css[i:j].strip()


def section_css():
    """O CSS que esta seção usa, para ela funcionar sozinha (repetir o do topo não tem problema)."""
    home_css = os.path.join(f1.HOME_SRC_DIR, "un-home-v2.css")
    medio_css = os.path.join(HERE, "un-medio.css")
    parts = [
        css_between(home_css, "/* Entradas mais suaves", "/* ----"),                    # entradas de 32px
        css_between(home_css, "/* Títulos das seções", "/* ----"),                      # cortina do título
        css_between(home_css, "/* Botões com seta", "/* Link \"Conhecer"),              # botão com seta
        css_between(medio_css, "/* ----------------------------------------------------------------------"
                               "----\n   DIFERENCIAIS", "/* ----------------------------------------------------------------------"
                               "----\n   MANIFESTO"),
        "@media (prefers-reduced-motion: reduce) {\n"
        "  .un-diferenciais .un-dif-card::before {\n    animation: none;\n  }\n}",
    ]
    return "\n\n".join(parts)


def write_section(section, out, title):
    section = json.loads(json.dumps(section))
    section["elements"].append(widget("html", {"html": "<style>\n" + section_css() + "\n</style>"}))
    data = {"content": [section], "page_settings": [], "version": "0.4", "title": title, "type": "container"}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
