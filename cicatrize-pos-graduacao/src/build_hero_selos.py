#!/usr/bin/env python3
"""Hero com os selos do MEC e da Anhanguera separados, a partir do hero exportado do site.

Parte do container de conteúdo do hero como está publicado (com as edições feitas no site:
logo, margens, tamanhos no celular, faixa "Turma de Membros Fundadores" etc.) e:
  1. coloca a classe "cz" no container, para as animações (título palavra por palavra, brilho do
     botão...) funcionarem mesmo que o container de fora tenha perdido as classes "cz cz-hero";
  2. devolve o fundo "vidro" do cartão dos ícones com configurações nativas (Estilo > Fundo/Borda),
     sem depender do CSS;
  3. troca os 2 chips brancos da coluna da direita pelos selos em imagem, separados:
     selo "Reconhecido pelo MEC" e logo da Anhanguera num cartão branco, flutuando sobre a foto
     (sai também o brilho rosé dessa coluna, que ficaria por cima do rosto do expert).
     No computador eles ficam soltos sobre a foto de fundo (posição nativa do Elementor, ajustável em
     Avançado > Posição); no tablet e no celular aparecem lado a lado, logo abaixo do texto de apoio.
Entrada: entrada/hero-atual-2026-10-07.json (export do Elementor)
Saídas:  ../hero-selos-elementor.json     só o container de conteúdo (para trocar dentro do hero)
         ../hero-completo-elementor.json  o hero inteiro num arquivo só: container da foto de fundo
                                          (classes "cz cz-hero"), conteúdo com os selos, barra de vagas
                                          e o CSS/JS da página embutido (substitui o "⚙ Estilos e animações")

Uso:  python3 build_hero_selos.py [export-do-hero.json]
"""
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entrada", "hero-atual-2026-10-07.json")
OUT = os.path.join(HERE, "..", "hero-selos-elementor.json")
OUT_FULL = os.path.join(HERE, "..", "hero-completo-elementor.json")

# Endereço que os arquivos terão depois de enviados para a Biblioteca de Mídia em outubro/2026
# (mesma pasta do logo que já está no site). Arquivos em ../assets/.
UPLOADS = "https://lp.morganamdesigner.com/wp-content/uploads/2026/10/"
MEC_IMG = {"url": UPLOADS + "selo-reconhecido-mec.webp", "id": "", "size": "", "source": "library",
           "alt": "Selo: curso reconhecido pelo MEC"}
ANH_IMG = {"url": UPLOADS + "logo-anhanguera.svg", "id": "", "size": "", "source": "library",
           "alt": "Diploma emitido pela Faculdade Anhanguera"}

_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-hero-selos-{_counter[0]}".encode()).hexdigest()[:7]


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dims(top, right=None, bottom=None, left=None, unit="px"):
    if right is None:
        right = bottom = left = top
    return {"unit": unit, "top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left),
            "isLinked": top == right == bottom == left}


def find(el, id_):
    if el.get("id") == id_:
        return el
    for c in el.get("elements", []):
        r = find(c, id_)
        if r:
            return r
    return None


def add_class(settings, key, cls):
    current = settings.get(key, "").split()
    for c in cls.split():
        if c not in current:
            current.append(c)
    settings[key] = " ".join(current)


def image(img, width, title, classes, extra=None):
    s = {
        "image": dict(img),
        "image_size": "full",
        "align": "center",
        "width": px(100, "%"),
        "_element_width": "initial",
        "_element_custom_width": px(width),
        "_flex_size": "none",
        "_css_classes": classes,
        "_title": title,
    }
    if extra:
        s.update(extra)
    return {"id": new_id(), "elType": "widget", "isInner": False, "widgetType": "image",
            "settings": s, "elements": []}


def selo_mec(width, extra=None):
    return image(MEC_IMG, width, "Selo Reconhecido pelo MEC", "cz-selo cz-selo-mec", extra)


def selo_anh(width, extra=None):
    """Logo da Anhanguera dentro de um cartão branco (fundo, borda e raio nativos do widget)."""
    s = {
        "_background_background": "classic",
        "_background_color": "#FFFFFF",
        "_padding": dims(14, 20, 14, 20),
        "_padding_mobile": dims(10, 14, 10, 14),
        "_border_radius": dims(14),
        "__globals__": {"_background_color": ""},
    }
    if extra:
        s.update(extra)
    return image(ANH_IMG, width, "Logo Faculdade Anhanguera", "cz-selo cz-selo-anh", s)


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    hero = data["content"][0]

    # 1. escopo das animações/estilos no próprio container
    add_class(hero["settings"], "css_classes", "cz cz-hero-content")
    hero["settings"]["_title"] = "1 · HERO · conteúdo"

    # 2. cartão dos ícones: fundo e borda nativos
    seals = find(hero, "4eddc539")
    seals["settings"].update({
        "background_background": "classic",
        "background_color": "rgba(255, 255, 255, 0.06)",
        "border_border": "solid",
        "border_width": dims(1),
        "border_color": "rgba(255, 255, 255, 0.14)",
        "__globals__": {"background_color": "", "border_color": ""},
    })

    # 3a. coluna da direita (computador): selos soltos sobre a foto de fundo
    right = find(hero, "5635289f")
    # o brilho rosé (widget HTML .cz-orb) sai: agora a foto do expert está no fundo e ele ficaria por cima
    mec_abs = selo_mec(150, {
        "_animation": "zoomIn",
        "_animation_delay": 500,
        "_position": "absolute",
        "_offset_orientation_h": "start",
        "_offset_x": px(4, "%"),
        "_offset_orientation_v": "end",
        "_offset_y_end": px(12, "%"),
        "_z_index": 3,
        "_element_custom_width_laptop": px(130),
    })
    anh_abs = selo_anh(190, {
        "_animation": "fadeInDown",
        "_animation_delay": 750,
        "_position": "absolute",
        "_offset_orientation_h": "end",
        "_offset_x_end": px(0, "%"),
        "_offset_orientation_v": "start",
        "_offset_y": px(14, "%"),
        "_z_index": 3,
        "_element_custom_width_laptop": px(170),
    })
    right["elements"] = [mec_abs, anh_abs]
    right["settings"].update({
        "min_height": px(560),
        "min_height_laptop": px(500),
        "hide_tablet": "hidden-tablet",
        "hide_mobile": "hidden-mobile",
        "_title": "Selos sobre a foto (só computador) — ajuste em Avançado > Posição",
    })

    # 3b. tablet e celular: selos lado a lado, abaixo do texto de apoio
    row = {
        "id": new_id(),
        "elType": "container",
        "isInner": True,
        "settings": {
            "content_width": "full",
            "flex_direction": "row",
            "flex_direction_mobile": "row",
            "flex_wrap": "nowrap",
            "flex_justify_content": "flex-start",
            "flex_justify_content_mobile": "center",
            "flex_align_items": "center",
            "flex_gap": {"column": "18", "row": "18", "isLinked": True, "unit": "px", "size": 18},
            "flex_gap_mobile": {"column": "14", "row": "14", "isLinked": True, "unit": "px", "size": 14},
            "padding": dims(0),
            "hide_desktop": "hidden-desktop",
            "hide_laptop": "hidden-laptop",
            "animation": "fadeInUp",
            "animation_delay": 300,
            "_title": "Selos lado a lado (só tablet e celular)",
        },
        "elements": [
            selo_mec(96, {"_element_custom_width_mobile": px(78)}),
            selo_anh(170, {"_element_custom_width_mobile": px(140)}),
        ],
    }
    left = find(hero, "614852df")
    sub_index = next(i for i, e in enumerate(left["elements"]) if e["id"] == "2f51f14f")
    left["elements"].insert(sub_index + 1, row)

    out = {"content": [hero], "page_settings": [], "version": "0.4",
           "title": "Cicatrize - Hero com selos MEC e Anhanguera", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")

    # hero completo: mesmo container da foto de fundo da página (build_cicatrize), com este conteúdo
    sys.path.insert(0, HERE)
    import build_cicatrize as bc  # noqa: E402
    full = bc.build_hero()
    full["elements"][0] = copy.deepcopy(hero)
    assets = bc.html_widget(bc.assets_html(), classes="cz-assets", title="⚙ CSS + JS da página (não apagar)")
    full["elements"].insert(0, assets)
    full["settings"].update({
        "css_classes": "cz cz-hero",  # sem cz-camada: a foto de fundo já vem tratada no design
        "background_position_mobile": "top center",
        "_title": "1 · HERO completo (foto de fundo em Estilo > Fundo, computador e celular)",
    })
    out = {"content": [full], "page_settings": [], "version": "0.4",
           "title": "Cicatrize - Hero completo", "type": "container"}
    with open(OUT_FULL, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT_FULL)}")


if __name__ == "__main__":
    main()
