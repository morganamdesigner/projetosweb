#!/usr/bin/env python3
"""Hero da Home "do primeiro dia de aula à formatura", aplicado sobre o export atual da Home.

Troca o slideshow do cartão azul por uma "linha do tempo": a linha de luz atravessa a foto do
primeiro dia revelando a formatura, e o título destaca o trecho da foto atual (un-story.css/js,
embutidos num widget HTML dentro do próprio cartão). Mantém tudo o mais do export.
Saídas: ../home-story-elementor.json (página inteira) e ../hero-home-story-elementor.json (só o topo)

Uso:  python3 build_home_story.py [export-da-home.json]
"""
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else (
    "/root/.claude/uploads/598d857a-d11e-584d-95fc-cd62f5fdb11e/52f62b9c-elementor-1369-2026-09-28.json")
OUT_PAGE = os.path.join(HERE, "..", "home-story-elementor.json")
OUT_HERO = os.path.join(HERE, "..", "hero-home-story-elementor.json")

PHOTO_FORMATURA = "https://colegiounicultura.com.br/wp-content/uploads/2026/09/bg_1_unicultura.webp"

TITLE = ('Do <span class="un-hl un-hl--a">primeiro dia de aula</span> à '
         '<span class="un-hl un-hl--b">formatura</span>, aqui começa a <strong>trajetória</strong> do seu filho.')


def find(elements, pred):
    for e in elements:
        if pred(e):
            return e
        r = find(e.get("elements", []), pred)
        if r:
            return r


def classes(e):
    s = e["settings"] if isinstance(e["settings"], dict) else {}
    return (s.get("css_classes") or s.get("_css_classes") or "").split()


def story_widget(photo_a, photo_b):
    css = open(os.path.join(HERE, "un-story.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "un-story.js"), encoding="utf-8").read().strip()
    markup = (
        '<div class="un-story" aria-hidden="true">'
        f'<div class="un-story-img un-story-img--a" style="background-image:url(\'{photo_a}\')"></div>'
        f'<div class="un-story-img un-story-img--b" style="background-image:url(\'{photo_b}\')"></div>'
        '<div class="un-story-shade"></div>'
        '<div class="un-story-line"><span class="un-story-handle">‹›</span></div>'
        '</div>'
    )
    return {
        "id": hashlib.md5(b"unicultura-home-story").hexdigest()[:7],
        "elType": "widget",
        "isInner": False,
        "widgetType": "html",
        "settings": {"html": markup + "\n<style>\n" + css + "\n</style>\n<script>\n" + js + "\n</script>",
                     "_css_classes": "un-story-wrap"},
        "elements": [],
    }


def main():
    page = json.load(open(SRC, encoding="utf-8"))
    top = page["content"][0]
    card = find([top], lambda e: "un-hero" in classes(e))
    s = card["settings"]
    photos = [img["url"] for img in s.get("background_slideshow_gallery", [])]
    if len(photos) < 2:
        sys.exit("O cartão .un-hero precisa ter as 2 fotos no slideshow (primeiro dia, formatura).")
    photos[1] = PHOTO_FORMATURA  # a cliente trocou a foto da formatura

    # o fundo passa a ser só a cor; fotos e degradê agora vêm do widget da história
    for k in list(s):
        if k.startswith("background_slideshow_") or k.startswith("background_overlay_"):
            del s[k]
    s["background_background"] = "classic"
    s["background_color"] = "#0D1261"
    card["elements"].insert(0, story_widget(photos[0], photos[1]))

    # sem amarelo nos textos do hero: estrelas brancas, hover dos segmentos em vermelho suave
    def recolor(e):
        st = e["settings"] if isinstance(e["settings"], dict) else {}
        if st.get("title_color", "").upper() == "#FFB867":
            st["title_color"] = "#FFFFFF"
        if st.get("text_color_hover", "").upper() == "#FFB867":
            st["text_color_hover"] = "#FF8A8A"
        for c in e.get("elements", []):
            recolor(c)
    recolor(card)

    title = find([card], lambda e: e.get("widgetType") == "heading" and "trajetória" in e["settings"].get("title", ""))
    if title:
        title["settings"]["title"] = TITLE
        title["settings"]["header_size"] = "h1"

    with open(OUT_PAGE, "w", encoding="utf-8") as fh:
        json.dump(page, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    hero = {"content": [copy.deepcopy(top)], "page_settings": [], "version": page.get("version", "0.4"),
            "title": "Unicultura - Home Hero (primeiro dia -> formatura)", "type": "container"}
    with open(OUT_HERO, "w", encoding="utf-8") as fh:
        json.dump(hero, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("fotos:", photos)
    print(f"OK: {os.path.normpath(OUT_PAGE)}\nOK: {os.path.normpath(OUT_HERO)}")


if __name__ == "__main__":
    main()
