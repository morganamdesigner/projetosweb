#!/usr/bin/env python3
"""Botão flutuante de WhatsApp (dúvidas) que só aparece depois de um tempo na página.

A página converte ali mesmo; o WhatsApp é só para dúvidas, então o botão:
  - aparece só quando a pessoa já passou do hero E está há pelo menos 25 s na página
    (as duas condições; ajustável em data-delay / data-after);
  - é petróleo com o ícone branco (o verde da página é só dos botões de ação);
  - ao aparecer, mostra por 7 s o balão "Dúvidas? Fale com a nossa equipe" (uma vez por visita;
    dá para fechar no ×);
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
DELAY_S = 25          # segundos na página antes de poder aparecer
AFTER = ".cz-hero"    # só depois de passar deste elemento (o hero)

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
.cz-wa{position:fixed;z-index:9990;right:22px;bottom:22px;display:flex;align-items:center;gap:12px;
  font-family:"Lato",sans-serif;pointer-events:none;opacity:0;transform:translateY(24px) scale(.9);
  transition:opacity .5s ease,transform .6s cubic-bezier(.2,.7,.2,1)}
.cz-wa.is-on{opacity:1;transform:none;pointer-events:auto}
.cz-wa-btn{position:relative;display:grid;place-items:center;width:60px;height:60px;border-radius:50%;
  background:#0F4F5C;color:#fff!important;text-decoration:none!important;
  box-shadow:0 14px 30px -10px rgba(11,60,70,.65),inset 0 0 0 2px rgba(207,138,134,.55);
  transition:transform .3s cubic-bezier(.2,.7,.2,1),background-color .3s ease}
.cz-wa-btn svg{width:30px;height:30px}
.cz-wa-btn::before{content:"";position:absolute;inset:0;border-radius:50%;
  animation:cz-wa-ring 2.8s ease-out infinite}
.cz-wa-btn:hover{transform:scale(1.06);background:#13606F}
.cz-wa-btn:focus-visible{outline:3px solid #CF8A86;outline-offset:3px}
@keyframes cz-wa-ring{0%{box-shadow:0 0 0 0 rgba(207,138,134,.45)}80%,100%{box-shadow:0 0 0 14px rgba(207,138,134,0)}}
.cz-wa-tip{position:relative;max-width:230px;padding:12px 34px 12px 14px;border-radius:14px 14px 4px 14px;
  background:#fff;color:#0F4F5C;box-shadow:0 14px 32px -12px rgba(11,60,70,.45);font-size:14px;line-height:1.35;
  opacity:0;transform:translateX(10px);transition:opacity .4s ease,transform .5s cubic-bezier(.2,.7,.2,1);
  pointer-events:none}
.cz-wa-tip b{display:block;font-weight:900}
.cz-wa-tip span{color:#3B5C66}
.cz-wa.tip-on .cz-wa-tip{opacity:1;transform:none;pointer-events:auto}
.cz-wa-x{position:absolute;top:6px;right:6px;width:22px;height:22px;border:0;border-radius:50%;cursor:pointer;
  background:rgba(15,79,92,.08);color:#0F4F5C;font:700 14px/22px "Lato",sans-serif;padding:0}
@media (max-width:767px){
  .cz-wa{right:14px;bottom:86px}
  .cz-wa-btn{width:54px;height:54px}.cz-wa-btn svg{width:27px;height:27px}
  .cz-wa-tip{max-width:200px;font-size:13px}}
@media (prefers-reduced-motion:reduce){.cz-wa,.cz-wa-tip{transition:none}.cz-wa-btn::before{animation:none}}
.elementor-editor-active .cz-wa{opacity:1;transform:none;pointer-events:auto}
""".strip()

JS = """
(function(){
  var root=document.currentScript&&document.currentScript.previousElementSibling;
  if(!root||!root.classList.contains('cz-wa'))root=document.querySelector('.cz-wa');
  if(!root||root.dataset.czInit)return;root.dataset.czInit='1';
  var delay=(parseFloat(root.getAttribute('data-delay'))||25)*1000;
  var after=document.querySelector(root.getAttribute('data-after')||'.cz-hero');
  var timeOk=false,scrollOk=!after,shown=false;
  function store(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){return null}}
  function check(){
    if(!scrollOk&&after){scrollOk=after.getBoundingClientRect().bottom<0}
    if(timeOk&&scrollOk&&!shown){
      shown=true;root.classList.add('is-on');window.removeEventListener('scroll',check);
      if(!store('czWaTip')){store('czWaTip','1');
        setTimeout(function(){root.classList.add('tip-on')},700);
        setTimeout(function(){root.classList.remove('tip-on')},7700);}
    }
  }
  setTimeout(function(){timeOk=true;check()},delay);
  window.addEventListener('scroll',check,{passive:true});
  var x=root.querySelector('.cz-wa-x');
  if(x)x.addEventListener('click',function(){root.classList.remove('tip-on')});
})();
""".strip()


def build_html():
    url = f"https://wa.me/{NUMERO}?text={urllib.parse.quote(MENSAGEM)}"
    return (f"<style>{CSS}</style>"
            f'<div class="cz-wa" data-delay="{DELAY_S}" data-after="{AFTER}">'
            f'<div class="cz-wa-tip" role="status"><b>Dúvidas?</b><span>Fale com a nossa equipe no WhatsApp.</span>'
            f'<button class="cz-wa-x" type="button" aria-label="Fechar aviso">×</button></div>'
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
        "_title": "WhatsApp flutuante (aparece depois de 25 s e do hero)",
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
