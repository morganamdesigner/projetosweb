#!/usr/bin/env python3
"""Duas faixas diagonais cruzadas (em X) com texto em movimento, cada uma para um lado.

Faixa A: verde-água escuro (#0E7C72, a mesma da faixa do topo), texto branco, inclinada para cima,
         texto andando para a esquerda.
Faixa B: rosé (#CF8A86), texto petróleo, inclinada para baixo, texto andando para a direita.
Separadores em bolinha (CSS, sem símbolos). Pausa ao passar o mouse; com "reduzir movimento" para.
CSS embutido no widget HTML (funciona sozinho). O container tem margem negativa (metade da altura em cima e embaixo) e z-index 20, para ficar
metade sobre o hero e metade sobre a seção seguinte; fundo transparente e sem bloquear cliques.
Saídas: ../faixas-cruzadas-elementor.json e ../faixas-cruzadas-codigo.html

Uso:  python3 build_faixas_cruzadas.py
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "faixas-cruzadas-elementor.json")
OUT_HTML = os.path.join(HERE, "..", "faixas-cruzadas-codigo.html")

ITEMS = ["Pós-graduação online", "Reconhecida pelo MEC", "Sem TCC", "Feridas e Podiatria",
         "Faculdade Anhanguera"]

CSS = """
.cz-x{position:relative;height:210px;overflow:hidden;font-family:"Lato",sans-serif;pointer-events:none}
.cz-x-band{position:absolute;top:50%;left:-10%;width:120%;overflow:hidden;
  box-shadow:0 18px 36px -18px rgba(7,34,37,.55)}
.cz-x-a{z-index:1;background:linear-gradient(90deg,#0A615A,#0E7C72 40%,#13917F 60%,#0E7C72);color:#fff;
  transform:translateY(-50%) rotate(-4deg)}
.cz-x-b{z-index:2;background:linear-gradient(90deg,#C47F7B,#CF8A86 40%,#DDA19D 60%,#CF8A86);color:#0F4F5C;
  transform:translateY(-50%) rotate(4deg)}
.cz-x-track{display:flex;width:max-content}
.cz-x-a .cz-x-track{animation:cz-x-left 40s linear infinite}
.cz-x-b .cz-x-track{animation:cz-x-right 40s linear infinite}
.cz-x:hover .cz-x-track{animation-play-state:paused}
.cz-x-group{display:flex;align-items:center;flex:none}
.cz-x-item{padding:18px 26px;white-space:nowrap;font-size:20px;font-weight:900;letter-spacing:.08em;
  text-transform:uppercase;line-height:1}
.cz-x-sep{width:8px;height:8px;border-radius:50%;background:currentColor;opacity:.55;flex:none}
@keyframes cz-x-left{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes cz-x-right{from{transform:translateX(-50%)}to{transform:translateX(0)}}
@media (max-width:1024px){.cz-x{height:170px}.cz-x-item{font-size:17px;padding:15px 20px}}
@media (max-width:767px){.cz-x{height:160px}
  .cz-x-a{transform:translateY(-50%) rotate(-9deg)}.cz-x-b{transform:translateY(-50%) rotate(9deg)}
  .cz-x-item{font-size:13px;padding:12px 14px;letter-spacing:.06em}.cz-x-sep{width:6px;height:6px}
  .cz-x-a .cz-x-track,.cz-x-b .cz-x-track{animation-duration:26s}}
@media (prefers-reduced-motion:reduce){.cz-x-track{animation:none!important}}
""".strip()


def build_html():
    def group(hidden):
        parts = []
        for t in ITEMS * 2:
            parts.append(f'<span class="cz-x-item">{t}</span><span class="cz-x-sep"></span>')
        aria = ' aria-hidden="true"' if hidden else ""
        return f'<span class="cz-x-group"{aria}>{"".join(parts)}</span>'

    def band(cls, hidden):
        aria = ' aria-hidden="true"' if hidden else ""
        return (f'<div class="cz-x-band {cls}"{aria}>'
                f'<div class="cz-x-track">{group(False)}{group(True)}</div></div>')

    label = " · ".join(ITEMS)
    return (f"<style>{CSS}</style>"
            f'<div class="cz-x" role="img" aria-label="{label}">'
            f'{band("cz-x-a", False)}{band("cz-x-b", True)}</div>')


def new_id(n):
    return hashlib.md5(f"cicatrize-faixas-x-{n}".encode()).hexdigest()[:7]


def main():
    html = build_html()
    widget = {"id": new_id(1), "elType": "widget", "isInner": False, "widgetType": "html", "elements": [],
              "settings": {"html": html, "_title": "Faixas cruzadas (textos em ITEMS)"}}
    container = {"id": new_id(2), "elType": "container", "isInner": False, "elements": [widget], "settings": {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
        "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
        "overflow": "hidden",
        # metade por cima do hero, metade por cima da seção seguinte (altura: 210 / 170 / 160 px)
        "margin": {"unit": "px", "top": "-105", "right": "0", "bottom": "-105", "left": "0", "isLinked": False},
        "margin_tablet": {"unit": "px", "top": "-85", "right": "0", "bottom": "-85", "left": "0", "isLinked": False},
        "margin_mobile": {"unit": "px", "top": "-80", "right": "0", "bottom": "-80", "left": "0", "isLinked": False},
        "z_index": 20,
        "css_classes": "cz",
        "_title": "Faixas cruzadas em X (entre o hero e a seção 2)",
    }}
    data = {"content": [container], "page_settings": [], "version": "0.4",
            "title": "Cicatrize - Faixas cruzadas", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html + "\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
