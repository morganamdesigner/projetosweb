#!/usr/bin/env python3
"""Faixa de aviso acima do hero: "Turma de Membros Fundadores · Vagas limitadas".

Faixa rosé (cor de destaque da identidade; o verde fica só para os botões de ação) com texto
petróleo em movimento contínuo, ponto pulsando, separadores em bolinha (sem símbolos) e brilho passando. A faixa inteira é um link para
a oferta (#oferta). Pausa ao passar o mouse; com "reduzir movimento" o texto fica parado e
centralizado. CSS embutido no próprio widget (funciona sozinha).
Saída: ../faixa-topo-elementor.json

Uso:  python3 build_faixa_topo.py
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "faixa-topo-elementor.json")

LINK = "#oferta"
ITEMS = ["Turma de Membros Fundadores", "Vagas limitadas", "Condição exclusiva da primeira turma"]

CSS = """
.cz-topbar{--tb-teal:#0F4F5C;--tb-rose:#CF8A86;display:block;position:relative;overflow:hidden;
  background:linear-gradient(90deg,#C47F7B,var(--tb-rose) 30%,#DDA19D 50%,var(--tb-rose) 70%,#C47F7B);
  color:var(--tb-teal)!important;text-decoration:none!important;font-family:"Lato",sans-serif;
  border-bottom:1px solid rgba(15,79,92,.18)}
.cz-topbar::after{content:"";position:absolute;top:0;left:-30%;width:20%;height:100%;pointer-events:none;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);
  animation:cz-tb-shine 5s ease-in-out infinite}
.cz-topbar-track{display:flex;width:max-content;animation:cz-tb-move 32s linear infinite}
.cz-topbar:hover .cz-topbar-track,.cz-topbar:focus-visible .cz-topbar-track{animation-play-state:paused}
.cz-topbar-group{display:flex;align-items:center;flex:none}
.cz-topbar-item{display:inline-flex;align-items:center;gap:10px;padding:12px 22px;white-space:nowrap;
  font-size:14px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;line-height:1}
.cz-topbar-sep{width:5px;height:5px;border-radius:50%;background:var(--tb-teal);opacity:.45;flex:none}
.cz-topbar-dot{width:8px;height:8px;border-radius:50%;background:var(--tb-teal);flex:none;
  box-shadow:0 0 0 0 rgba(15,79,92,.55);animation:cz-tb-ping 1.8s infinite}
.cz-topbar-cta{display:inline-flex;align-items:center;gap:6px;margin-left:4px;padding:6px 12px;border-radius:999px;
  background:var(--tb-teal);color:#fff;font-size:11px;letter-spacing:.12em}
.cz-topbar:focus-visible{outline:3px solid var(--tb-teal);outline-offset:-3px}
@keyframes cz-tb-move{to{transform:translateX(-50%)}}
@keyframes cz-tb-shine{0%,55%{left:-30%}100%{left:130%}}
@keyframes cz-tb-ping{0%{box-shadow:0 0 0 0 rgba(15,79,92,.55)}70%{box-shadow:0 0 0 8px rgba(15,79,92,0)}
  100%{box-shadow:0 0 0 0 rgba(15,79,92,0)}}
@media (max-width:767px){.cz-topbar-item{padding:11px 16px;font-size:12px;letter-spacing:.1em}
  .cz-topbar-track{animation-duration:24s}}
@media (prefers-reduced-motion:reduce){.cz-topbar::after,.cz-topbar-dot{animation:none}
  .cz-topbar-track{animation:none;width:auto;justify-content:center}
  .cz-topbar-group+.cz-topbar-group{display:none}.cz-topbar-group{flex-wrap:wrap;justify-content:center}}
""".strip()


def build_html():
    def group(hidden=False):
        parts = []
        for i, text in enumerate(ITEMS):
            dot = '<span class="cz-topbar-dot"></span>' if i == 0 else ""
            parts.append(f'<span class="cz-topbar-item">{dot}{text}</span>')
            parts.append('<span class="cz-topbar-sep" aria-hidden="true"></span>')
        parts.append('<span class="cz-topbar-item"><span class="cz-topbar-cta">Garantir minha vaga →</span></span>')
        parts.append('<span class="cz-topbar-sep" aria-hidden="true"></span>')
        aria = ' aria-hidden="true"' if hidden else ""
        return f'<span class="cz-topbar-group"{aria}>{"".join(parts * 2)}</span>'

    label = " · ".join(ITEMS) + ". Ir para a oferta."
    return (f"<style>{CSS}</style>"
            f'<a class="cz-topbar" href="{LINK}" aria-label="{label}">'
            f'<span class="cz-topbar-track">{group()}{group(hidden=True)}</span></a>')


def new_id(n):
    return hashlib.md5(f"cicatrize-faixa-topo-{n}".encode()).hexdigest()[:7]


def main():
    widget = {"id": new_id(1), "elType": "widget", "isInner": False, "widgetType": "html", "elements": [],
              "settings": {"html": build_html(), "_title": "Faixa: Turma de Membros Fundadores"}}
    container = {"id": new_id(2), "elType": "container", "isInner": False, "elements": [widget], "settings": {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
        "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
        "min_height": {"unit": "px", "size": 0, "sizes": []},
        "background_background": "classic",
        "background_color": "#CF8A86",
        "z_index": 5,
        "css_classes": "cz",
        "_title": "0 · FAIXA DO TOPO (acima do hero)",
    }}
    data = {"content": [container], "page_settings": [], "version": "0.4",
            "title": "Cicatrize - Faixa do topo", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
