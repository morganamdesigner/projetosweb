#!/usr/bin/env python3
"""Botão flutuante de WhatsApp (dúvidas), só o ícone.

  - aparece quando a 3ª seção ("A pós 2 em 1", .cz-2em1) entra na tela, sem esperar tempo
    (ajustável em data-show-at);
  - verde (#1FBF5C), escurece no hover; anel pulsando;
  - no celular fica acima da barra verde fixa "Quero minha vaga";
  - abre o WhatsApp com uma mensagem pronta.
CSS e JS embutidos no widget HTML (funciona sozinho, em qualquer lugar da página).
Saídas: ../whatsapp-flutuante-elementor.json e ../whatsapp-flutuante-codigo.html

Uso:  python3 build_whatsapp.py
"""
import hashlib
import json
import os
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "whatsapp-flutuante-elementor.json")
OUT_HTML = os.path.join(HERE, "..", "whatsapp-flutuante-codigo.html")

NUMERO = "55SUBSTITUIR-NUMERO"  # DDI + DDD + número, só dígitos. Ex.: 5534999999999
MENSAGEM = "Olá! Tenho uma dúvida sobre a Pós-graduação em Tratamento de Feridas e Podiatria."
SHOW_AT = ".cz-2em1"  # aparece quando esta seção (3 · A pós 2 em 1) entra na tela

ICON = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.04 3C8.88 3 '
        '3.07 8.82 3.07 15.98c0 2.29.6 4.52 1.75 6.49L3 29l6.72-1.76a13 13 0 0 0 6.31 1.6h.01c7.16 0 12.97-5.83 '
        '12.97-12.99 0-3.47-1.35-6.73-3.8-9.18A12.9 12.9 0 0 0 16.04 3Zm0 23.65h-.01a10.8 10.8 0 0 1-5.5-1.5l-.4-.24'
        '-3.99 1.04 1.07-3.88-.26-.4a10.72 10.72 0 0 1-1.65-5.7c0-5.95 4.85-10.79 10.8-10.79 2.88 0 5.59 1.12 7.62 '
        '3.16a10.7 10.7 0 0 1 3.16 7.63c0 5.95-4.85 10.68-10.84 10.68Zm5.92-8.08c-.32-.16-1.92-.95-2.22-1.06-.3-.11-'
        '.51-.16-.73.16-.21.32-.84 1.06-1.03 1.27-.19.22-.38.24-.7.08-.32-.16-1.37-.5-2.6-1.6a9.78 9.78 0 0 1-1.8-'
        '2.24c-.19-.32-.02-.5.14-.65.15-.15.32-.38.48-.57.16-.19.21-.32.32-.54.11-.21.05-.4-.03-.56-.08-.16-.73-1.76'
        '-1-2.41-.26-.63-.53-.55-.73-.56h-.62c-.21 0-.56.08-.86.4-.3.32-1.13 1.1-1.13 2.69 0 1.58 1.16 3.12 1.32 '
        '3.33.16.21 2.28 3.48 5.53 4.88.77.33 1.37.53 1.84.68.77.25 1.48.21 2.03.13.62-.09 1.92-.78 2.19-1.54.27-.76'
        '.27-1.41.19-1.54-.08-.13-.29-.21-.61-.37Z"/></svg>')

CSS = """
.cz-wa{position:fixed;z-index:9990;right:22px;bottom:22px;pointer-events:none;opacity:0;
  transform:translateY(24px) scale(.9);transition:opacity .5s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.cz-wa.is-on{opacity:1;transform:none;pointer-events:auto}
.cz-wa-btn{position:relative;display:grid;place-items:center;width:60px;height:60px;border-radius:50%;
  background:#1FBF5C;color:#fff!important;text-decoration:none!important;
  box-shadow:0 14px 30px -10px rgba(11,60,70,.65);
  transition:transform .3s cubic-bezier(.2,.7,.2,1),background-color .3s ease}
.cz-wa-btn svg{width:30px;height:30px}
.cz-wa-btn::before{content:"";position:absolute;inset:0;border-radius:50%;
  animation:cz-wa-ring 2.8s ease-out infinite}
.cz-wa-btn:hover{transform:scale(1.06);background:#169C4B}
.cz-wa-btn:focus-visible{outline:3px solid #0F4F5C;outline-offset:3px}
@keyframes cz-wa-ring{0%{box-shadow:0 0 0 0 rgba(31,191,92,.5)}80%,100%{box-shadow:0 0 0 14px rgba(31,191,92,0)}}
@media (max-width:767px){
  .cz-wa{right:14px;bottom:86px}
  .cz-wa-btn{width:54px;height:54px}.cz-wa-btn svg{width:27px;height:27px}}
@media (prefers-reduced-motion:reduce){.cz-wa{transition:none}.cz-wa-btn::before{animation:none}}
.elementor-editor-active .cz-wa{opacity:1;transform:none;pointer-events:auto}
""".strip()

JS = """
(function(){
  var root=document.currentScript&&document.currentScript.previousElementSibling;
  if(!root||!root.classList.contains('cz-wa'))root=document.querySelector('.cz-wa');
  if(!root||root.dataset.czInit)return;root.dataset.czInit='1';
  var target=document.querySelector(root.getAttribute('data-show-at')||'.cz-2em1');
  function check(){
    var ok=!target||target.getBoundingClientRect().top<window.innerHeight*0.85;
    if(ok){root.classList.add('is-on');window.removeEventListener('scroll',check)}
  }
  window.addEventListener('scroll',check,{passive:true});
  check();
})();
""".strip()


def build_html():
    url = f"https://wa.me/{NUMERO}?text={urllib.parse.quote(MENSAGEM)}"
    return (f"<style>{CSS}</style>"
            f'<div class="cz-wa" data-show-at="{SHOW_AT}">'
            f'<a class="cz-wa-btn" href="{url}" target="_blank" rel="noopener" '
            f'aria-label="Tirar dúvidas pelo WhatsApp">{ICON}</a></div>'
            f"<script>{JS}</script>")


def new_id(n):
    return hashlib.md5(f"cicatrize-whatsapp-{n}".encode()).hexdigest()[:7]


def main():
    html = build_html()
    widget = {"id": new_id(1), "elType": "widget", "isInner": False, "widgetType": "html", "elements": [],
              "settings": {"html": html, "_title": "WhatsApp flutuante (número no link wa.me)"}}
    container = {"id": new_id(2), "elType": "container", "isInner": False, "elements": [widget], "settings": {
        "content_width": "full",
        "flex_direction": "column",
        "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
        "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True},
        "min_height": {"unit": "px", "size": 0, "sizes": []},
        "_title": "WhatsApp flutuante (aparece na seção 3)",
    }}
    data = {"content": [container], "page_settings": [], "version": "0.4",
            "title": "Cicatrize - WhatsApp flutuante", "type": "container"}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html + "\n")
    print(f"OK: {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
