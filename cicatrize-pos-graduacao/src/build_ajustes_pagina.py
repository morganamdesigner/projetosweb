#!/usr/bin/env python3
"""Ajustes de celular (e alguns gerais) na página completa exportada do site.

Parte da página como está publicada (entrada/pagina-completa-2026-10-07.json, com todas as edições
feitas no Elementor) e muda só o necessário. Os IDs são os do export, então tudo o que não está
listado aqui fica exatamente como estava.

Celular:
  1. Grade curricular: os cartões dos blocos ficam escuros (petróleo) no celular, para o texto branco
     ("BLOCO 01", "5 disciplinas") ter contraste. No computador continuam como estão. (CSS)
  2. Faixa "Turma de Membros Fundadores": tinha largura fixa de 432 px (maior que a tela) e por isso a
     fonte estava em 8 px. Agora ocupa 100% no celular e volta para 10 px.
  3. Botões verdes: cabem em uma linha (13 px, menos espaçamento entre letras e respiro lateral).
  4. Paradoxo: as 2 fotos ficam lado a lado no celular (antes, empilhadas, ocupavam quase 2 telas).
  5. Como funciona: os 8 cartões viram uma lista compacta (ícone à esquerda, texto à direita).
  6. Corpo docente: os cartões das professoras ficam horizontais (foto à esquerda, texto à direita).
  7. Quem é o Dr. Cicatriz: a moldura rosé atrás da foto não encosta mais na borda da tela. (CSS)
  8. Rodapé: textos centralizados.
Geral:
  9. CSS/JS embutido no hero atualizado (cz-page.css / cz-page.js).
Saída: ../pagina-completa-elementor.json

Uso:  python3 build_ajustes_pagina.py [export-da-pagina.json]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_cicatrize as bc  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entrada", "pagina-completa-2026-10-07.json")
OUT = os.path.join(HERE, "..", "pagina-completa-elementor.json")

_counter = [0]


def new_id():
    _counter[0] += 1
    return hashlib.md5(f"cicatrize-ajustes-{_counter[0]}".encode()).hexdigest()[:7]


px, dims, gap = bc.px, bc.dims, bc.gap


def index(data):
    m = {}

    def walk(e):
        m[e["id"]] = e
        for c in e["elements"]:
            walk(c)

    for c in data["content"]:
        walk(c)
    return m


def classes(e):
    s = e["settings"]
    return (s.get("css_classes", "") + " " + s.get("_css_classes", "")).split()


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    E = index(data)
    log = []

    # 9. CSS/JS embutido
    assets = next(e for e in E.values() if e.get("widgetType") == "html"
                  and "<style>" in e["settings"].get("html", "") and "cz-sticky" in e["settings"]["html"])
    assets["settings"]["html"] = bc.assets_html()
    log.append("CSS/JS embutido atualizado")

    # 2. faixa "Turma de Membros Fundadores" (hero)
    pill = next(e for e in E.values() if e.get("widgetType") == "heading"
                and e["settings"].get("title", "").startswith("Turma de Membros Fundadores")
                and e["settings"].get("header_size") == "p" and e["settings"].get("_element_width") == "initial")
    pill["settings"].update({
        "_element_custom_width_mobile": px(100, "%"),
        "typography_font_size_mobile": px(10),
        "typography_letter_spacing_mobile": px(1),
        "typography_line_height_mobile": px(14),
    })
    log.append("faixa do hero: 100% e 10 px no celular")

    # 3. botões verdes em uma linha no celular
    n = 0
    for e in E.values():
        if e.get("widgetType") == "button" and "cz-btn" in classes(e):
            e["settings"].update({
                "typography_font_size_mobile": px(13),
                "typography_letter_spacing_mobile": px(0.2),
                "typography_line_height_mobile": px(17),
                "text_padding_mobile": dims(18, 16, 18, 16),
            })
            n += 1
    log.append(f"{n} botões verdes ajustados")

    # 4. paradoxo: fotos lado a lado
    collage = next(e for e in E.values() if "cz-collage" in classes(e))
    collage["settings"].update({
        "flex_direction_mobile": "row",
        "flex_align_items_mobile": "flex-start",
        "flex_gap_mobile": gap(14),
    })
    for shot in collage["elements"]:
        if shot["elType"] != "container":
            continue
        shot["settings"]["width_mobile"] = px(48, "%")
        if "cz-shot-a" in classes(shot):
            shot["settings"]["_flex_align_self_mobile"] = "flex-start"
        if "cz-shot-b" in classes(shot):
            shot["settings"]["margin_mobile"] = dims(44, 0, 0, 0)
    log.append("paradoxo: fotos lado a lado")

    # 5. como funciona: lista compacta no celular
    n = 0
    for card in [e for e in E.values() if "cz-info" in classes(e)]:
        kids = card["elements"]
        icon = next(k for k in kids if k.get("widgetType") == "icon")
        texts = [k for k in kids if k.get("widgetType") == "heading"]
        if len(texts) != 2:
            continue
        label, value = texts
        label["settings"]["_margin_mobile"] = dims(0)
        inner = {"id": new_id(), "elType": "container", "isInner": True, "elements": texts, "settings": {
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": card["settings"].get("flex_gap", gap(12)),
            "flex_gap_mobile": gap(4),
            "padding": dims(0),
            "_title": "Texto",
        }}
        card["elements"] = [icon, inner]
        card["settings"].update({
            "flex_direction_mobile": "row",
            "flex_align_items_mobile": "flex-start",
            "flex_gap_mobile": gap(16),
            "padding_mobile": dims(18, 18, 18, 18),
        })
        icon["settings"]["icon_padding_mobile"] = px(11)
        n += 1
    log.append(f"como funciona: {n} cartões compactos")

    # 6. corpo docente: cartões horizontais no celular (só os das professoras, não o do coordenador)
    n = 0
    for card in [e for e in E.values() if "cz-prof" in classes(e)]:
        kids = card["elements"]
        if not kids or kids[0].get("widgetType") != "image":
            continue
        photo, info = kids[0], kids[1]
        card["settings"].update({
            "flex_direction_mobile": "row",
            "flex_align_items_mobile": "stretch",
        })
        photo["settings"].update({
            "_element_width_mobile": "initial",
            "_element_custom_width_mobile": px(36, "%"),
            "_flex_size_mobile": "none",
        })
        info["settings"].update({
            "padding_mobile": dims(16, 16, 18, 16),
            "flex_gap_mobile": gap(6),
        })
        for w in info["elements"]:
            s = w["settings"]
            if w.get("widgetType") == "heading" and s.get("header_size") == "h3":
                s.update({"typography_font_size_mobile": px(17), "typography_line_height_mobile": px(22)})
            elif w.get("widgetType") == "heading":
                s.update({"typography_font_size_mobile": px(12), "typography_line_height_mobile": px(17)})
            elif w.get("widgetType") == "text-editor":
                s.update({"typography_font_size_mobile": px(14), "typography_line_height_mobile": px(20)})
        n += 1
    log.append(f"corpo docente: {n} cartões horizontais")

    # 8. rodapé centralizado
    footer = next(e for e in data["content"] if e["settings"].get("html_tag") == "footer")
    for w in footer["elements"]:
        if w.get("widgetType") == "heading":
            w["settings"]["align_mobile"] = "center"
    log.append("rodapé centralizado")

    data["title"] = "Cicatrize - Página de vendas (ajustes de celular)"
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("\n".join("· " + l for l in log))
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
