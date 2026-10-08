#!/usr/bin/env python3
"""Seção de oferta (Membro Fundador) mais conversiva, a partir da seção exportada do site.

Parte de entrada/secao-oferta-2026-10-08.json (com as imagens já escolhidas no site) e:

Bônus
  - faixa diagonal "BÔNUS 1", "BÔNUS 2"... no canto de cada cartão (sobre a imagem), com brilho
    passando de tempos em tempos;
  - valor de cada bônus de volta nos 4 cartões ("Valor R$ 677 · grátis para você"; no Doppler,
    "Valor R$ 1.500 · sorteio"), que tinha sumido dos 3 primeiros ao trocar o ícone pela imagem;
  - sai o ícone (a imagem já mostra o bônus);
  - texto agrupado num bloco: quem ganha (etiqueta), nome do bônus e valor;
  - celular: cartão horizontal (imagem 40% + texto 60%, larguras explícitas), em vez de 4 imagens
    grandes empilhadas.
Preço
  - "De R$ 11.800 por" no lugar de "Valor da pós-graduação: R$ 11.800" (ancoragem mais direta);
  - selo de economia "Economize R$ 8.300 no Pix" (11.800 − 3.500);
  - linha de confiança abaixo da microcopy: Pagamento seguro · Pix ou cartão em até 12x.
"O que recebe"
  - novo item que liga a lista aos bônus logo abaixo.
Celular/tablet
  - "Tudo o que o Membro Fundador recebe" aparece ANTES do cartão de preço (valor antes do preço).
As regras de CSS novas vão num widget HTML dentro da própria seção (funciona sem atualizar o hero).
Saída: ../secao-oferta-elementor.json

Uso:  python3 build_secao_oferta.py [export-da-secao.json]
"""
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entrada", "secao-oferta-2026-10-08.json")
OUT = os.path.join(HERE, "..", "secao-oferta-elementor.json")
CSS_FILE = os.path.join(HERE, "cz-oferta.css")

TEAL, SLATE, ROSE, WHITE = "#0F4F5C", "#3B5C66", "#CF8A86", "#FFFFFF"
LATO = "Lato"

# (valor, rótulo do benefício) na ordem dos cartões
BONUS_VALUES = [
    ("R$ 677", "grátis para você"),
    ("R$ 150", "grátis para você"),
    ("R$ 50", "grátis para você"),
    ("R$ 1.500", "sorteio"),
]

_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-oferta-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def gap(size):
    return {"column": str(size), "row": str(size), "isLinked": True, "unit": "px", "size": size}


def typo(size, weight, lh, ls=None, transform=None, size_m=None, lh_m=None):
    s = {"typography_typography": "custom", "typography_font_family": LATO,
         "typography_font_size": px(size), "typography_font_weight": str(weight),
         "typography_line_height": px(lh)}
    if ls is not None:
        s["typography_letter_spacing"] = px(ls)
    if transform:
        s["typography_text_transform"] = transform
    if size_m:
        s["typography_font_size_mobile"] = px(size_m)
    if lh_m:
        s["typography_line_height_mobile"] = px(lh_m)
    return s


def widget(kind, settings):
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": kind, "elements": [],
            "settings": settings}


def heading(title, color, typography, classes="", title_nav=None, extra=None):
    s = {"title": title, "header_size": "p", "align": "left", "title_color": color,
         "__globals__": {"title_color": "", "typography_typography": ""}}
    s.update(typography)
    if classes:
        s["_css_classes"] = classes
    if title_nav:
        s["_title"] = title_nav
    if extra:
        s.update(extra)
    return widget("heading", s)


def container(children, **settings):
    s = {"content_width": "full", "flex_direction": "column", "flex_gap": gap(0), "padding": dims(0)}
    s.update(settings)
    return {"id": new_id(), "elType": "container", "isInner": True, "elements": children, "settings": s}


def find(el, pred):
    if pred(el):
        return el
    for c in el.get("elements", []):
        r = find(c, pred)
        if r:
            return r
    return None


def walk(el):
    yield el
    for c in el.get("elements", []):
        yield from walk(c)


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    sec = data["content"][0]
    log = []

    # ------------------------------------------------------------------ bônus
    grid = find(sec, lambda e: e["settings"].get("container_type") == "grid")
    for i, card in enumerate(grid["elements"]):
        ws = list(walk(card))
        img = next(w for w in ws if w.get("widgetType") == "image")
        who = next(w for w in ws if "cz-bonus-who" in w["settings"].get("_css_classes", ""))
        name = next(w for w in ws if w.get("widgetType") == "heading" and w["settings"].get("header_size") == "h4")
        value, label = BONUS_VALUES[i]

        img["settings"].update({"width": px(100, "%"), "align": "center", "_css_classes": "cz-bonus-img"})
        img_wrap = container([img], css_classes="cz-bonus-media", _title="Imagem do bônus")

        value_w = heading(f'<span>Valor</span> <s>{value}</s> <b>{label}</b>', WHITE,
                          typo(13, 700, 18, ls=0.2), classes="cz-bonus-price",
                          title_nav="Valor do bônus")
        name["settings"].pop("_margin", None)
        name["settings"].update({"typography_font_size_mobile": px(15), "typography_line_height_mobile": px(20)})
        info = container([who, name, value_w], flex_gap=gap(10), flex_gap_mobile=gap(6),
                         css_classes="cz-bonus-info", _title="Texto do bônus")

        ribbon = heading(f"Bônus {i + 1}", WHITE, typo(12, 900, 14, ls=1.8, transform="uppercase"),
                         classes="cz-ribbon", title_nav=f"Faixa diagonal: Bônus {i + 1}")

        card["elements"] = [ribbon, img_wrap, info]
        card["settings"].update({
            "overflow": "hidden",
            "padding": dims(18, 18, 22, 18),
            "padding_mobile": dims(14, 14, 14, 14),
            "flex_gap": gap(16),
            "flex_direction_mobile": "row",
            "flex_align_items_mobile": "center",
            "flex_gap_mobile": gap(14),
            "background_background": "classic",
            "background_color": "rgba(255, 255, 255, 0.06)",
            "border_border": "solid",
            "border_width": dims(1),
            "border_color": "rgba(207, 138, 134, 0.35)",
            "__globals__": {"background_color": "", "border_color": ""},
        })
    grid["settings"]["grid_gaps"] = {"column": "20", "row": "20", "isLinked": True, "unit": "px"}
    grid["settings"]["grid_columns_grid_mobile"] = px(1, "fr")
    log.append("bônus: faixa diagonal, valor nos 4, sem ícone, horizontal no celular")

    # ------------------------------------------------------------------ preço
    price = find(sec, lambda e: "cz-price" in e["settings"].get("css_classes", "").split())
    strike = find(price, lambda e: "cz-strike" in e["settings"].get("_css_classes", ""))
    strike["settings"]["title"] = "De <s>R$ 11.800</s> por"
    pix = find(price, lambda e: "à vista no Pix" in str(e["settings"].get("title", "")))
    save = heading("Economize R$ 8.300 pagando no Pix", WHITE, typo(13, 800, 16, ls=0.4),
                   classes="cz-save", title_nav="Selo de economia (11.800 − 3.500)")
    kids = price["elements"]
    kids.insert(kids.index(pix) + 1, save)

    trust = widget("icon-list", {
        "view": "inline",
        "icon_list": [
            {"_id": new_id(), "text": "Pagamento seguro", "selected_icon": {"value": "fas fa-shield-alt",
                                                                            "library": "fa-solid"}},
            {"_id": new_id(), "text": "Pix ou cartão em até 12x", "selected_icon": {"value": "fas fa-credit-card",
                                                                                    "library": "fa-solid"}},
        ],
        "space_between": px(18),
        "icon_align": "left",
        "icon_align_mobile": "center",
        "text_color": SLATE, "text_color_hover": SLATE,
        "icon_color": TEAL, "icon_color_hover": TEAL,
        "icon_size": px(13), "text_indent": px(8),
        "icon_typography_typography": "custom", "icon_typography_font_family": LATO,
        "icon_typography_font_size": px(13), "icon_typography_font_weight": "700",
        "icon_typography_line_height": px(18),
        "_css_classes": "cz-trust",
        "_margin": dims(4, 0, 0, 0),
        "_title": "Linha de confiança",
        "__globals__": {"text_color": "", "icon_color": "", "icon_typography_typography": ""},
    })
    kids.append(trust)
    log.append("preço: 'De R$ 11.800 por', selo de economia, linha de confiança")

    # ------------------------------------------------------------------ o que recebe
    gets = find(sec, lambda e: "cz-gets" in e["settings"].get("css_classes", "").split())
    lst = find(gets, lambda e: e.get("widgetType") == "icon-list")
    items = lst["settings"]["icon_list"]
    bonus_item = copy.deepcopy(items[0])
    bonus_item.update({"_id": new_id(),
                       "text": "Chance de levar os bônus exclusivos da Aula Magna (veja abaixo)",
                       "selected_icon": {"value": "fas fa-gift", "library": "fa-solid"}})
    items.append(bonus_item)
    log.append("o que recebe: item dos bônus")

    # valor antes do preço no celular/tablet
    row = find(sec, lambda e: price in e.get("elements", []))
    row["settings"]["flex_direction_tablet"] = "column-reverse"
    row["settings"]["flex_direction_mobile"] = "column-reverse"
    log.append("celular/tablet: 'o que recebe' antes do preço")

    # ------------------------------------------------------------------ CSS embutido
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    sec["elements"].insert(0, widget("html", {"html": "<style>\n" + css + "\n</style>",
                                              "_css_classes": "cz-assets",
                                              "_title": "CSS da oferta (não apagar)"}))

    data["title"] = "Cicatrize - Oferta (Membro Fundador)"
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("\n".join("· " + l for l in log))
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
