#!/usr/bin/env python3
"""Seção 08 · Bônus e oferta, versão de alta conversão (a partir do export do site enviado pela cliente).

- Bônus como "presente": card com borda luminosa girando, fita "Bônus exclusivo · incluso hoje",
  capa da aula com play pulsando e selo +2, e o que as aulas ensinam com ícones.
- "O que você recebe": cada item com ícone próprio em círculo turquesa.
- Preço ancorado: De R$ 97,00 riscado, contagem 97 → 27 e selo "Economize 72%".
- Botão com anel pulsando e faixa de confiança com ícones.
- "Como você recebe" com ícones nos 4 passos.
Mantém a imagem do mockup e o link do botão do export.
Saída: ../secao-08-oferta-elementor.json
Uso:   python3 build_secao_oferta.py [export-da-secao.json]
"""
import json
import os
import sys

import el
from build_lp import (AZUL, AZC, CYAN_GRAD, INK, LINE, MED, MUTED, NOITE, PROF, TURQ, TXT, WHITE, body, btn_primary,
                      eyebrow, h2, section)
from el import (anim, border, button, cls, col, container, counter, dims, gap, grad, heading, html, icon, icon_list,
                image, px, row, setv, shadow, solid, typo)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "secao-08-oferta-elementor.json")
DEFAULT_EXPORT = "/root/.claude/uploads/302eadef-2a03-5162-b1d4-20b33bc74d43/e8ff68aa-elementor-298-2026-10-21.json"


def from_export(path):
    """Imagem do mockup e link do botão que a cliente já configurou."""
    img, url = None, "#checkout"
    if path and os.path.exists(path):
        def walk(e):
            nonlocal img, url
            s = e.get("settings", {})
            if e.get("widgetType") == "image" and not img:
                img = s.get("image")
            if e.get("widgetType") == "button" and s.get("link", {}).get("url"):
                url = s["link"]["url"]
            for c in e.get("elements", []):
                walk(c)
        for sec in json.load(open(path))["content"]:
            walk(sec)
    return img, url


def ico(value, size=18, pad=14, cls_name="lp-get-ico"):
    w = icon(value, WHITE, size, view="stacked", secondary=None, padding=pad)
    setv(w, primary_color=TURQ, secondary_color=WHITE, _flex_size="none")
    return cls(w, cls_name)


def bonus_card():
    ring = container({"css_classes": "lp-bonus-ring"}, [], "Borda luminosa (decorativa)")
    tag = cls(heading("Bônus exclusivo · incluso hoje", NOITE, typo("typography", 11, 800, lh=1.3, ls=1.6, transform="uppercase"),
                      _element_width="auto", _flex_align_self="flex-start", _padding=dims(7, 14),
                      _border_radius=dims(999), **solid(TURQ, "_background")), "lp-ribbon-tag")
    play = cls(icon("fas fa-play", TURQ, 26, view="stacked", secondary=NOITE, padding=28, align="center"), "lp-play")
    setv(play, primary_color=TURQ, secondary_color=NOITE)
    badge = cls(col([heading("+2", NOITE, typo("typography", 26, 900, lh=1), align="center"),
                     heading("aulas", NOITE, typo("typography", 9, 800, lh=1.2, ls=1.4, transform="uppercase"), align="center")],
                    0, "Selo +2 aulas", width=px(72), min_height=px(72), height=px(72), _flex_size="none", flex_justify_content="center",
                    flex_align_items="center", border_radius=dims(999), width_mobile=px(64), min_height_mobile=px(64), **grad(CYAN_GRAD[0], CYAN_GRAD[1], 135),
                    box_shadow_box_shadow_type="yes", box_shadow_box_shadow=shadow(0, 12, 30, -8, "rgba(0, 194, 199, 0.7)")),
                "lp-cover-badge")
    cover = col([badge, play, heading("Aula 1 · Avaliação na cadeira   ·   Aula 2 · Da avaliação à conduta", TXT,
                                      typo("typography", 11, 600, lh=1.4, size_m=10), align="center")],
                18, "Capa da aula", width=px(480), width_tablet=px(100, "%"), width_mobile=px(100, "%"), _flex_size="none",
                min_height=px(300), min_height_mobile=px(230), flex_justify_content="center", flex_align_items="center",
                padding=dims(24), **grad(MED, NOITE, 135), border_radius=dims(18), css_classes="lp-cover")

    learn = [("fas fa-search", "Como avaliar a intercorrência na própria consulta"),
             ("fas fa-route", "O passo a passo da avaliação até a decisão de conduta"),
             ("fas fa-redo", "Assista quando quiser e reveja sempre que precisar")]
    learn_rows = [row([ico(v, 14, 11), body(f"<p>{t}</p>", TXT, 15, weight=500, lh=1.45, m=14)], 14, t[:24],
                      flex_align_items="center") for v, t in learn]
    info = [
        tag,
        h2('2 aulas gravadas: como aplicar o guia <span class="lp-hl">na sua rotina clínica</span>', WHITE, 30, t=26, m=23,
           lh=1.25, tag="h3"),
        col(learn_rows, 12, "O que as aulas ensinam"),
        row([heading("O guia diz o quê. As aulas mostram como.", TURQ, typo("typography", 17, 700, lh=1.4, size_m=15),
                     _flex_size="shrink")], 0, "Frase", padding=dims(14, 18), border_radius=dims(14),
            **solid("rgba(0, 194, 199, 0.08)"), **border(1, "rgba(0, 194, 199, 0.3)")),
    ]
    for i, w in enumerate(info):
        anim(w, "fadeInUp", i * 80)
    card = row([ring, cover, col(info, 18, "Texto", _flex_size="shrink")], 40, "Card do bônus (presente)",
               flex_direction_tablet="column", flex_align_items="center", flex_align_items_tablet="stretch",
               padding=dims(32), padding_mobile=dims(18), **grad("#0B2D4A", "#011a30", 135), border_radius=dims(26),
               css_classes="lp-bonus", box_shadow_box_shadow_type="yes",
               box_shadow_box_shadow=shadow(0, 40, 80, -40, "rgba(0, 194, 199, 0.45)"))
    return anim(card, "fadeInUp")


def offer_box(img, url):
    gets = [
        ("fas fa-book-medical", "Guia Prático em PDF", "As 15 intercorrências mais comuns em sinais, avaliação e conduta"),
        ("fas fa-play-circle", "2 aulas gravadas (bônus)", "Como aplicar o guia na rotina clínica"),
        ("fas fa-mobile-alt", "Consulta em qualquer tela", "Celular, tablet ou computador, na hora da consulta"),
        ("fas fa-bolt", "Acesso imediato", "Liberado no seu e-mail assim que o pagamento é confirmado"),
    ]
    rows = []
    for v, t, d in gets:
        txt = col([heading(t, PROF, typo("typography", 16, 800, lh=1.3, size_m=15)),
                   body(f"<p>{d}</p>", INK, 14, lh=1.45, m=13)], 2, "Texto", _flex_size="shrink")
        extra = []
        if "bônus" in t:
            extra = [cls(heading("Incluso", NOITE, typo("typography", 10, 800, lh=1.3, ls=1.2, transform="uppercase"),
                                 _padding=dims(5, 10), _border_radius=dims(999), **solid(TURQ, "_background")), "lp-free")]
        rows.append(row([ico(v)] + [txt] + extra, 14, t, flex_align_items="center", padding=dims(12, 14),
                        border_radius=dims(16), **solid("#F4F8FB"), css_classes="lp-get-row"))
    price = row([
        heading("por", PROF, typo("typography", 22, 600, lh=1.2), _margin=dims(0, 0, 14, 0)),
        counter(97, 27, "R$ ", AZUL, typo("typography_number", 88, 800, lh=1, size_m=64), duration=1400),
        col([cls(heading("Economize 72%", NOITE, typo("typography", 11, 800, lh=1.2, ls=1, transform="uppercase"),
                         _padding=dims(6, 12), _border_radius=dims(999), _element_width="auto", _flex_align_self="flex-start",
                         **solid("#FFD24D", "_background")), "lp-save"),
             heading("pagamento único", MUTED, typo("typography", 14, 500, lh=1.3))], 6, "Selo e condição",
            _margin=dims(0, 0, 12, 0), flex_align_items="flex-start"),
    ], 12, "Preço", flex_align_items="flex-end", flex_wrap="wrap")
    cta = cls(btn_primary("Quero o guia + as 2 aulas por R$ 27", url, full=True), "lp-cta-pulse")
    trust = cls(icon_list([{"text": "Compra segura", "icon": "fas fa-lock"},
                           {"text": "Garantia de 7 dias", "icon": "fas fa-shield-alt"},
                           {"text": "Acesso imediato", "icon": "fas fa-bolt"},
                           {"text": "Pix ou cartão", "icon": "fas fa-credit-card"}], MUTED,
                          typo("icon_typography", 12, 600, lh=1.4), icon_color=TURQ, icon_size=13, inline=True,
                          space=18, indent=6), "lp-trustbar")
    buy = [
        eyebrow("O que você recebe", AZUL),
        col(rows, 10, "Itens"),
        cls(heading("De R$ 97,00", MUTED, typo("typography", 20, 500, lh=1.3), _margin=dims(8, 0, 0, 0)), "lp-old lp-io"),
        price,
        body("<p>Menos do que você cobra por <strong>uma única consulta de retorno</strong>.</p>", INK, 16),
        cta, trust,
    ]
    mock = image(img["url"] if img else "", img.get("alt") or "Guia Intercorrências com Alinhadores no tablet e as aulas bônus"
                 if img else "Guia e aulas", width=(100, "%"))
    if img:
        mock["settings"]["image"] = dict(img, alt=img.get("alt") or "Guia Intercorrências com Alinhadores e as 2 aulas bônus")
    box = row([
        col([anim(mock, "zoomIn")], 0, "Mockup guia + aula", width=px(44, "%"), width_tablet=px(100, "%"),
            width_mobile=px(100, "%"), flex_justify_content="center", flex_align_items="center", padding=dims(40, 24),
            **grad("#F4F8FB", "#E1E9F0", 160)),
        col(buy, 16, "Compra", width=px(56, "%"), width_tablet=px(100, "%"), width_mobile=px(100, "%"),
            padding=dims(48, 52), padding_mobile=dims(30, 20), flex_justify_content="center"),
    ], 0, "Caixa da oferta", flex_direction_tablet="column", flex_align_items="stretch", **solid(WHITE),
        border_radius=dims(28), overflow="hidden", box_shadow_box_shadow_type="yes",
        box_shadow_box_shadow=shadow(0, 50, 100, -40, "rgba(0, 194, 199, 0.4)"))
    return anim(box, "fadeInUp")


def steps():
    data = [("fas fa-credit-card", "Finalize o pagamento com Pix ou cartão"),
            ("fas fa-envelope-open-text", "Receba no e-mail o acesso à plataforma assim que o pagamento for confirmado"),
            ("fas fa-cloud-download-alt", "Assista às aulas e faça o download do guia completo"),
            ("fas fa-tooth", "Abra o guia na próxima consulta, no celular, no tablet ou no computador")]
    cards = []
    for i, (v, t) in enumerate(data, 1):
        top = row([cls(icon(v, TURQ, 20, view="framed", secondary="transparent", padding=13, border_width=dims(1.5),
                            _flex_size="none"), "lp-step-ico"),
                   heading(f"{i:02d}", "rgba(126, 211, 230, 0.35)", typo("typography", 26, 800, lh=1))],
                  12, "Ícone e número", flex_align_items="center", flex_justify_content="space-between")
        cards.append(anim(col([top, body(f"<p>{t}</p>", TXT, 15, lh=1.55, m=14)], 16, f"Passo {i}",
                              padding=dims(24), **solid("rgba(255, 255, 255, 0.04)"), **border(1, LINE, 18)),
                          "fadeInUp", (i - 1) * 120))
    grid = container({"container_type": "grid", "grid_columns_grid": px(4, "fr"), "grid_columns_grid_tablet": px(2, "fr"),
                      "grid_columns_grid_mobile": px(1, "fr"), "grid_rows_grid": px(1, "fr"),
                      "grid_rows_grid_tablet": px(2, "fr"), "grid_rows_grid_mobile": px(4, "fr"), "grid_gaps": gap(20),
                      "css_classes": "lp-steps lp-io", "margin": dims(14, 0, 0, 0)}, cards, "Passos")
    return col([heading("Como você recebe:", WHITE, typo("typography", 24, 700, lh=1.3, size_m=20), tag="h3"), grid],
               18, "Como você recebe")


def build(export=DEFAULT_EXPORT):
    el._counter[0] = 80000  # faixa própria de IDs
    img, url = from_export(export)
    css = open(os.path.join(HERE, "lp-offer.css"), encoding="utf-8").read().strip()
    style = setv(html("<style>\n" + css + "\n</style>"), _title="Oferta · estilos e animação (não apagar)",
                 _position="absolute", _element_width="initial", _element_custom_width=px(0))
    head = anim(col([eyebrow("Bônus e oferta", TURQ, center=True),
                     h2('Tudo para decidir com <span class="lp-hl">critério</span> na próxima consulta.', WHITE, 42,
                        "center", t=34, m=27)], 14, "Título", flex_align_items="center", content_width="boxed",
                    boxed_width=px(820)), "fadeInUp")
    sec = section({"_element_id": "oferta", "flex_gap": gap(64), "flex_gap_mobile": gap(44),
                   **grad(NOITE, "#0A3756", 180), "overflow": "hidden"},
                  [style, head, bonus_card(), offer_box(img, url), steps()], "08 · Bônus e oferta (#oferta)",
                  "lp-offer lp-orbits")
    from build_lp import fix_rows
    return fix_rows(sec)


def main():
    sec = build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXPORT)
    data = {"content": [sec], "page_settings": [], "version": "0.4",
            "title": "LP Alinhadores · 08 Bônus e oferta (alta conversão)", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print("ok:", os.path.relpath(OUT), f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
