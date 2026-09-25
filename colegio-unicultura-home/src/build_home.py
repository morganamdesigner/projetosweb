#!/usr/bin/env python3
"""Gera o JSON da Home (Colégio Unicultura) com o hero/menu no padrão da Garatuja.

Entradas:
  - Export da Home enviado pelo cliente (elementor-831-2026-09-25.json)
  - Hero/menu da Garatuja já ajustado (../../colegio-unicultura-garatuja/hero-menu-mobile-elementor.json)
Saída:
  ../home-elementor.json

O que faz:
  1. Troca o 1º bloco (hero-slider) pelo hero da Garatuja, com o conteúdo, os botões e as
     cores da Home; as duas fotos passam a ser o Slideshow de fundo nativo (Ken Burns).
  2. Corrige a hierarquia de títulos (H1 no hero; eyebrows como <p>; títulos dos cards como H3).
  3. Corrige a cor inválida "##FF0B0B" do carrossel de etapas.
  4. Adiciona animações de entrada e hovers nas demais seções (rodapé não está no arquivo).

Uso:  python3 build_home.py [caminho-do-export-da-home.json]
"""
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOME_SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/195424d6-elementor-831-2026-09-25.json")
GARATUJA_HERO = os.path.join(HERE, "..", "..", "colegio-unicultura-garatuja", "hero-menu-mobile-elementor.json")
CSS_FILE = os.path.join(HERE, "un-home.css")
JS_FILE = os.path.join(HERE, "un-home.js")
OUT = os.path.join(HERE, "..", "home-elementor.json")

PAGE_BG = "#FDFDFF"
RED = "#F10505"
HERO_PHOTOS = [
    "https://colegiounicultura.com.br/wp-content/uploads/2026/09/foto2-home-2.webp",
    "https://colegiounicultura.com.br/wp-content/uploads/2026/09/group_6.webp",
]

home = json.load(open(HOME_SRC, encoding="utf-8"))
garatuja = json.load(open(GARATUJA_HERO, encoding="utf-8"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def index(elements):
    found = {}

    def walk(e):
        found[e["id"]] = e
        for c in e["elements"]:
            walk(c)
    for e in elements:
        walk(e)
    return found


H = index(home["content"])
_taken = set(H)
_seq = [0]


def new_id():
    while True:
        _seq[0] += 1
        candidate = hashlib.md5(f"unicultura-home-{_seq[0]}".encode()).hexdigest()[:7]
        if candidate not in _taken:
            _taken.add(candidate)
            return candidate


def reid(element):
    """Novos IDs para tudo que foi clonado da Garatuja (evita IDs repetidos na Home)."""
    element["id"] = new_id()
    for c in element["elements"]:
        reid(c)
    return element


def px(v, unit="px"):
    return {"unit": unit, "size": v, "sizes": []}


def anim(el, name="fadeInUp", delay=0):
    s = el["settings"]
    prefix = "_" if el["elType"] == "widget" else ""
    s[f"{prefix}animation"] = name
    s["animation_duration"] = "fast"
    if delay:
        s[f"{prefix}animation_delay"] = delay
    return el


def add_class(el, cls):
    key = "_css_classes" if el["elType"] == "widget" else "css_classes"
    current = el["settings"].get(key, "")
    if cls not in current.split():
        el["settings"][key] = (current + " " + cls).strip()
    return el


def home_widget(id_):
    return copy.deepcopy(H[id_])


# ---------------------------------------------------------------------------
# 1. HERO + MENU no padrão da Garatuja
# ---------------------------------------------------------------------------

def build_hero():
    top = copy.deepcopy(garatuja["content"][0])
    # remove "Duas etapas" (é da Garatuja): fica só o hero
    top["elements"] = [e for e in top["elements"] if "gt-hero" in e["settings"].get("css_classes", "")]
    reid(top)
    G = index([top])
    hero = top["elements"][0]

    # --- wrapper do topo --------------------------------------------------
    ts = top["settings"]
    ts["background_color"] = PAGE_BG
    ts["padding"] = {"unit": "px", "top": "11", "right": "20", "bottom": "0", "left": "20", "isLinked": False}
    ts["css_classes"] = "gt-root gt-top"

    # --- recortes com a cor de fundo da Home ------------------------------
    for e in G.values():
        if "gt-notch" in e["settings"].get("css_classes", ""):
            e["settings"]["background_color"] = PAGE_BG

    # --- fundo do hero: slideshow nativo com as duas fotos ---------------
    hs = hero["settings"]
    for k in ("background_image", "background_position", "background_xpos", "background_ypos",
              "background_repeat", "background_size", "background_bg_width",
              "background_position_tablet", "background_size_tablet",
              "background_position_mobile", "background_size_mobile",
              "background_xpos_mobile", "background_ypos_mobile", "background_bg_width_mobile"):
        hs.pop(k, None)
    hs.update({
        "background_background": "slideshow",
        "background_slideshow_gallery": [{"id": "", "url": u} for u in HERO_PHOTOS],
        "background_slideshow_loop": "yes",
        "background_slideshow_slide_duration": 6000,
        "background_slideshow_slide_transition": "fade",
        "background_slideshow_transition_duration": 1500,
        "background_slideshow_background_size": "cover",
        "background_slideshow_background_position": "center center",
        "background_slideshow_ken_burns": "yes",
        "background_slideshow_ken_burns_zoom_direction": "in",
    })

    # --- menu -------------------------------------------------------------
    nav = next(e for e in G.values() if "gt-navbar" in e["settings"].get("css_classes", "").split())
    new_children = []
    for child in nav["elements"]:
        wt = child.get("widgetType")
        if wt == "nav-menu":
            ms = child["settings"]
            ms["pointer_color_menu_item_hover"] = RED
            ms["color_dropdown_item_hover"] = "#010658"
            ms["background_color_dropdown_item_hover"] = "#F0F2FA"
            new_children.append(child)
        elif wt == "social-icons":
            social = home_widget("32651c50")
            social["id"] = new_id()
            social["settings"].update({"_flex_size": "none", "hide_mobile": "hidden-mobile"})
            for k in ("_element_width", "_element_custom_width", "_element_custom_width_mobile"):
                social["settings"].pop(k, None)
            new_children.append(social)
        elif wt == "button":
            btn = home_widget("277c35a6")
            btn["id"] = new_id()
            btn["settings"].update({"_flex_size": "none", "hide_mobile": "hidden-mobile"})
            for k in ("_element_width", "_element_custom_width", "_element_custom_width_mobile"):
                btn["settings"].pop(k, None)
            new_children.append(btn)
        else:
            new_children.append(child)  # logos do menu fixo
    nav["elements"] = new_children

    # --- conteúdo do hero: widgets da Home --------------------------------
    content = next(e for e in hero["elements"]
                   if e["elType"] == "container" and not e["settings"].get("css_classes"))
    tag = home_widget("75683788")
    tag["settings"]["header_size"] = "p"
    title = home_widget("593460ec")
    title["settings"]["header_size"] = "h1"
    text = home_widget("41268dca")
    text["settings"]["_element_custom_width_mobile"] = px(100, "%")  # era 222px: texto espremido no celular
    buttons = home_widget("259b49ac")
    buttons["settings"]["width"] = px(100, "%")
    proof = home_widget("9d83c1a")  # já tem animação própria (CSS, 3,5 s)
    # "+1.200 famílias": contador (un-home.js) começa quando a prova social aparece (3,5 s)
    count = next(c for c in proof["elements"] if c["id"] == "62825cdb")
    add_class(count, "un-count")
    count["settings"]["_attributes"] = "data-delay|3500"
    content["settings"]["flex_gap"] = {"column": "10", "row": "10", "isLinked": True, "unit": "px", "size": 10}
    content["settings"]["flex_gap_mobile"] = {"column": "10", "row": "10", "isLinked": True, "unit": "px", "size": 10}
    content["elements"] = [
        anim(tag), anim(title, delay=120), anim(text, delay=240), anim(buttons, delay=360), proof,
    ]

    # --- CSS + JS da página (widget HTML sem altura, no fim do topo) --------
    css = open(CSS_FILE, encoding="utf-8").read().strip()
    js = open(JS_FILE, encoding="utf-8").read().strip()
    top["elements"].append({
        "id": new_id(), "elType": "widget", "isInner": False, "widgetType": "html",
        "settings": {"html": "<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>"},
        "elements": [],
    })
    return top


# ---------------------------------------------------------------------------
# 2. Demais seções: SEO, correção e animações
# ---------------------------------------------------------------------------

def parallax(el, speed=1):
    """Elementor Pro > Motion Effects > Vertical Scroll (só desktop)."""
    el["settings"].update({
        "motion_fx_motion_fx_scrolling": "yes",
        "motion_fx_translateY_effect": "yes",
        "motion_fx_translateY_speed": px(speed),
        "motion_fx_translateY_affectedRange": {"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
        "motion_fx_devices": ["desktop"],
    })
    return el


def improve_sections():
    # títulos: eyebrow "TIRE SUAS DÚVIDAS" vira <p>; títulos dos cards do carrossel viram H3
    H["22d1cd18"]["settings"]["header_size"] = "p"
    for i in ("4f3f7275", "7034d7d8", "6c43ab76"):
        H[i]["settings"]["header_size"] = "h3"

    # cor inválida no carrossel de etapas
    s = H["5155babc"]["settings"]
    s["custom_css"] = s.get("custom_css", "").replace("##FF0B0B", "#FF0B0B")

    # todas as seções recebem gt-root (entradas suaves de 32px definidas no CSS)
    for sec in home["content"][1:]:
        add_class(sec, "gt-root")

    # Duas escolas
    anim(H["2b30f144"]); anim(H["4d140c6e"], delay=100)
    anim(H["7bc7e482"]); anim(H["312664f6"])
    add_class(H["d74b1cc"], "un-zoom"); add_class(H["2e6e5e76"], "un-zoom")
    # Carrossel de fotos
    anim(H["ee1e916"], "fadeIn")
    # Nossa Proposta
    anim(H["7b9bea32"]); anim(H["4ba47a7b"], delay=100); anim(H["1e746b21"], "fadeIn", 200)
    anim(H["47fe924"], delay=150); anim(H["36d37280"], delay=300)
    # Etapas Unicultura
    anim(H["1b53f357"]); anim(H["4f6d53cb"], delay=100)
    anim(H["708852e2"], delay=200); anim(H["2b4e1424"], delay=260)
    anim(H["5155babc"], "fadeIn", 200)
    # Diferenciais (cards em cascata, linha a linha)
    anim(H["4db5acb0"])
    for row in ("2d514f96", "671f95d6", "490cfe39"):
        for i, card in enumerate(H[row]["elements"]):
            anim(card, delay=i * 120)
    anim(H["31db3c0e"])
    # Depoimentos
    anim(H["7c49bc4c"]); anim(H["244e4aa9"], delay=100); anim(H["2423b54a"], "fadeIn", 200)
    # CTA com formulário
    anim(H["7f3dea3c"])
    # FAQ
    anim(H["22d1cd18"]); anim(H["4b7a45c4"], delay=100); anim(H["6e28a468"], delay=200)

    # Títulos das seções: "cortina" da esquerda para a direita (CSS .un-reveal)
    for i in ("2b30f144", "7b9bea32", "4ba47a7b", "4f6d53cb", "7c49bc4c", "4b7a45c4"):
        H[i]["settings"]["_animation"] = "fadeIn"
        add_class(H[i], "un-reveal")

    # Parallax leve nas fotos (Duas escolas e Nossa Proposta)
    for i in ("d74b1cc", "2e6e5e76", "1e746b21"):
        parallax(H[i])


def main():
    improve_sections()
    home["content"][0] = build_hero()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(home, fh, ensure_ascii=False)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
